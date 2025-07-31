import os

try:
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
except ImportError:
    GoogleAuth = None
    GoogleDrive = None

def authenticate_drive():
    if GoogleAuth is None:
        raise ImportError("PyDrive module not installed.")
    
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.json")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()  # Creates local webserver and auto handles auth
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("credentials.json")
    drive = GoogleDrive(gauth)
    return drive

def upload_file(filepath):
    if not os.path.exists(filepath):
        return "File not found, upload failed."
    drive = authenticate_drive()
    file = drive.CreateFile({'title': os.path.basename(filepath)})
    file.SetContentFile(filepath)
    file.Upload()
    return f"File '{os.path.basename(filepath)}' uploaded successfully."

def download_file(file_id, local_path):
    drive = authenticate_drive()
    file = drive.CreateFile({'id': file_id})
    file.GetContentFile(local_path)
    return f"File downloaded successfully to {local_path}."
