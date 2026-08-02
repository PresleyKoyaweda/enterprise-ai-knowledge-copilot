from pathlib import Path

import msal
import requests

from app.core.config import settings

AUTHORITY = "https://login.microsoftonline.com/consumers"
SCOPES = ["Files.Read.All"]
GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"
TOKEN_CACHE_PATH = Path("data/.msal_token_cache.json")


def _load_token_cache() -> msal.SerializableTokenCache:
    cache = msal.SerializableTokenCache()

    if TOKEN_CACHE_PATH.exists():
        cache.deserialize(TOKEN_CACHE_PATH.read_text())

    return cache


def _save_token_cache(cache: msal.SerializableTokenCache) -> None:
    if cache.has_state_changed:
        TOKEN_CACHE_PATH.write_text(cache.serialize())


def _get_msal_app(cache: msal.SerializableTokenCache) -> msal.PublicClientApplication:
    return msal.PublicClientApplication(
        client_id=settings.ms_client_id,
        authority=AUTHORITY,
        token_cache=cache,
    )


def get_access_token() -> str:
    cache = _load_token_cache()
    app = _get_msal_app(cache)

    accounts = app.get_accounts()

    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            _save_token_cache(cache)
            return result["access_token"]

    flow = app.initiate_device_flow(scopes=SCOPES)

    if "user_code" not in flow:
        raise RuntimeError(
            "Impossible de démarrer le flux d'authentification Microsoft."
        )

    print(flow["message"])

    result = app.acquire_token_by_device_flow(flow)

    if "access_token" not in result:
        raise RuntimeError(
            f"Échec de l'authentification : {result.get('error_description')}"
        )

    _save_token_cache(cache)

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
