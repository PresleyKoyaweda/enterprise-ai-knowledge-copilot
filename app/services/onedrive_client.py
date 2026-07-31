import msal

from app.core.config import settings

AUTHORITY = f"https://login.microsoftonline.com/{settings.ms_tenant_id}"
SCOPES = ["Files.Read.All"]


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