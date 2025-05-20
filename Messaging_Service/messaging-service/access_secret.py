from google.cloud import secretmanager
import google.auth

def get_project_id():
    credentials, project_id = google.auth.default()
    return project_id

def access_secret(secret_id):

    project_id = get_project_id()

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")

