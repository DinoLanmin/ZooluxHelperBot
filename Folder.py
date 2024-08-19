import Aggregator

gauth = Aggregator.GoogleAuth()
gauth.credentials = Aggregator.ServiceAccountCredentials.from_json_keyfile_name(
    'credentials.json',
    scopes=['https://www.googleapis.com/auth/drive'])

drive = Aggregator.GoogleDrive(gauth)


def upload_photo(file_path, file_name, folder_id):
    gfile = drive.CreateFile({'title': file_name, 'parents': [{'id': folder_id}]})
    gfile.SetContentFile(file_path)
    gfile.Upload()
    return gfile['id']
