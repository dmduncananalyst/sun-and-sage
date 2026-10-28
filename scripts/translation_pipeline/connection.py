"""Existing local ADC only. Tokens remain memory-only; imports never authenticate."""
import os
from pathlib import Path

PROJECT = 'project-2e0d7d9d-d482-4fcf-b6d'

def private_path(variable, filename):
    if Path(filename).name != filename:
        raise ValueError('Private file must be a basename')
    path = Path(os.environ.get(variable, str(Path.home() / 'translation-budget' / filename))).expanduser()
    if not path.is_absolute():
        raise ValueError('Private path must be absolute')
    # Reject every Git checkout, including ignored files and linked worktrees.
    resolved = path.resolve()
    if any((parent / '.git').exists() for parent in resolved.parents):
        raise ValueError('Shared accounting must remain outside Git repositories')
    return resolved

def access_token():
    import google.auth
    from google.auth.transport.requests import Request
    existing = Path(__file__).resolve().parents[2] / '.tools/gcloud-profile/application_default_credentials.json'
    # Same existing ADC path as Paper Trail's approved blog runner. Never create keys.
    credential_path = Path(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', str(existing))).resolve()
    if not credential_path.is_file():
        raise RuntimeError('Existing Google application-default credentials are unavailable')
    try:
        credentials, _ = google.auth.load_credentials_from_file(str(credential_path), scopes=['https://www.googleapis.com/auth/cloud-platform'], quota_project_id=PROJECT)
        credentials.refresh(Request())
        if not credentials.token:
            raise ValueError('No access token')
        return credentials.token
    except Exception as error:
        # Provider exceptions may contain credential details. Do not forward them.
        raise RuntimeError('Existing Google ADC authentication failed; owner reauthentication may be required') from None
