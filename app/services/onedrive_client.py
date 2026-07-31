import msal
import requests

from app.core.config import settings

AUTHORITY = "https://login.microsoftonline.com/consumers"
SCOPES = ["Files.Read.All"]
GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"


def _get_msal_app() -> msal.PublicClientApplication:
    return msal.PublicClientApplication(
        client_id=settings.ms_client_id,
        authority=AUTHORITY,
    )


def get_access_token() -> str:
    app = _get_msal_app()

    flow = app.initiate_device_flow(scopes=SCOPES)

    if "user_code" not in flow:
        raise RuntimeError("Impossible de démarrer le flux d'authentification Microsoft.")

    print(flow["message"])

    result = app.acquire_token_by_device_flow(flow)

    if "access_token" not in result:
        raise RuntimeError(f"Échec de l'authentification : {result.get('error_description')}")

    return result["access_token"]


def list_files_in_folder(access_token: str, folder_name: str) -> list[dict]:
    headers = {"Authorization": f"Bearer {access_token}"}

    url = f"{GRAPH_BASE_URL}/me/drive/root:/{folder_name}:/children"
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    items = response.json()["value"]

    return [item for item in items if "file" in item]


def download_file_content(file_item: dict) -> bytes:
    download_url = file_item["@microsoft.graph.downloadUrl"]
    response = requests.get(download_url)
    response.raise_for_status()
    return response.content