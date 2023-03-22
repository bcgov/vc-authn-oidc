from api.core.config import settings

ex_client_config_create = {
    "client_id": settings.KEYCLOAK_CLIENT_ID,
    "client_name": settings.KEYCLOAK_CLIENT_NAME,
    "client_secret": "**********",
    "response_types": ["code", "id_token", "token"],
    "token_endpoint_auth_method": "client_secret_basic",
    "redirect_uris": [settings.KEYCLOAK_REDIRECT_URI],
}
