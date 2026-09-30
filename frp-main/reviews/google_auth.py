from google_auth_oauthlib.flow import Flow
from django.conf import settings
GOOGLE_SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
]
def create_google_flow(state=None, code_verifier=None):
    client_config = {
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [
                settings.GOOGLE_REDIRECT_URI
            ],
        }
    }
    if code_verifier:
        flow = Flow.from_client_config(
            client_config,
            scopes=GOOGLE_SCOPES,
            state=state,
            code_verifier=code_verifier
        )
    else:
        flow = Flow.from_client_config(
            client_config,
            scopes=GOOGLE_SCOPES,
            autogenerate_code_verifier=True
        )
    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
    return flow