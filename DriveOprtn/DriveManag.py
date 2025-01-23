import os
import io
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
import pickle
import sys
import logging

module_path = os.path.abspath("./DriveOprtn")
if module_path not in sys.path:
    sys.path.append(module_path)
from NotGoogle import Create_Service

module_path = os.path.abspath("./DeviceOprtn")
if module_path not in sys.path:
    sys.path.append(module_path)
import ScanObj

def find_file_id(service, filename, folder_id):
    query = f"'{folder_id}' in parents and name='{filename}' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    return files[0]['id'] if files else None

def upload_or_replace(service, file, folder_id, dat):
    fileName = file
    exten = file.split('.')[-1]  # Split on the last period to get the extension

    MimeType = next((mime[1] for mime in dat if mime[0] == exten), None)

    if MimeType is None:
        logging.warning(f"Unknown MIME type for file: {file}")
        return

    file_id = find_file_id(service, fileName, folder_id)

    file_metadata = {
        'name': fileName,
        'parents': [folder_id]
    }
    media = MediaFileUpload(f'Location from where you want to upload', mimetype=MimeType)   #Update the folder from where you want to upload.

    if file_id:
        # If the file exists, update it
        service.files().update(
            fileId=file_id,
            media_body=media
        ).execute()
        logging.info(f"File {fileName} updated successfully.")
    else:
        # If the file doesn't exist, create it
        service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        logging.info(f"File {fileName} uploaded successfully.")

def UploadFiles(filen):
    logging.info("Uploading files that are passed...")
    CLIENT_SECERET_FILE = 'File that contains the KEY '
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service = Create_Service(CLIENT_SECERET_FILE, API_NAME, API_VERSION, SCOPES)
    with open('./DriveOprtn/MIMETypes.mtypd', 'rb') as rcod:            #Create the file that contains the All the MIME types.  
        dat = pickle.load(rcod)

    folder_id = 'Drive folder ID for performing any operation'      #Input the folder ID in which you want to perform tasks

    if isinstance(filen, list):
        for file in filen:
            upload_or_replace(service, file, folder_id, dat)
    else:
        upload_or_replace(service, filen, folder_id, dat)

def DeleteFiles(file_ids):
    logging.info("Deleting files that are not present in the system...")
    CLIENT_SECERET_FILE = 'File that contains the KEY '
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service = Create_Service(CLIENT_SECERET_FILE, API_NAME, API_VERSION, SCOPES)
    if isinstance(file_ids, list):
        for file_id in file_ids:
            try:
                service.files().delete(fileId=file_id).execute()
                # print(f"File with ID {file_id} has been deleted.")
            except Exception as e:
                print(f"An error occurred: {e}")
    else:
        try:
            service.files().delete(fileId=file_id).execute()
            # print(f"File with ID {file_id} has been deleted.")
        except Exception as e:
            print(f"An error occurred: {e}")
    logging.info("The files has been successfully deleted.")
        

def DownloadFiles(file_name, file_id):
    CLIENT_SECERET_FILE = 'File that contains the KEY '
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service = Create_Service(CLIENT_SECERET_FILE, API_NAME, API_VERSION, SCOPES)
    reqeust = service.files().get_media(fileId=file_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd = fh, request=reqeust)
    done = False

    while not done:
        status, done = downloader.next_chunk()          #next_chunk() returns a Tuple which gives 2 values is the reason why we are assigning 2 variables.
        print('Download progress {0}'.format(status.progress()*100))
    
    fh.seek(0)

    with open(os.path.join('Folder that contain the file', file_name), 'wb') as f:
        f.write(fh.read())

def ScnFiles(object, mode):
    logging.info("ScnFiles function has started...")
    CLIENT_SECERET_FILE = 'File that contains the KEY '
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service = Create_Service(CLIENT_SECERET_FILE, API_NAME, API_VERSION, SCOPES)
    folder_id = 'Drive folder ID for performing any operation'      #Input the folder ID in which you want to perform tasks

    query = f"'{folder_id}' in parents" 
    results = service.files().list(
        q=query,
        spaces='drive',
        fields='nextPageToken, files(id, name, createdTime)'
    ).execute()

    items = results.get('files', [])
    # print(items)
    # Operations:-
    # 0 -> To return everything, 1 -> To return the name if object is ID, 2 -> To return the ID of the object name

    if mode == 0:
        logging.info("Function completed and returning all the data.")
        return items
    
    elif mode == 1:
        logging.info("Function completed and returning only the IDs of files.")
        for item in items:
            if item['id'] == object:
                return item['name']
            
    elif mode == 2:
        logging.info("Function completed and returning only the Names of files.")
        for item in items:
            if item['name'] == object:
                return item['id']

def ManageFiles():
    logging.info("ManageFiles function has started...")
    dat = ScanObj.ReadMtd()
    ddat = ScnFiles(None, 0)
    lddat = [file['name'] for file in ddat]
    ldat = [file[0] for file in dat]
    
    if len(ldat) > len(lddat):
        sdat = set(ldat)
        sddat = set(lddat)
        NPresent = list(sdat - sddat)
        UploadFiles(NPresent)
        logging.info("Uploaded files which are not in drive.")
    
    elif len(ldat) < len(lddat):
        sdat = set(ldat)
        sddat = set(lddat)
        ToDelete = list(sddat - sdat)
        Dlst = [item['id'] for file in ToDelete for item in ddat if file == item['name']]
        DeleteFiles(Dlst)
        logging.info("Deleted files that are not in system.")
    
    else:
        Mod = [items[0] for items in dat if items[2] != items[3]]
        UploadFiles(Mod)
        logging.info("Uploaded files that has been modified.")