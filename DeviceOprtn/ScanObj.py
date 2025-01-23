import os
import os.path
import time
import pickle
import logging 

def GetFilesNameTime():
    logging.info("GetFilesNameTime function is being executed...")
    folder_path = ""       #ENTER THE NAME OF THE FOLDER TO BE UPLOADED
    files_present = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        nmodification_time = time.ctime(os.path.getmtime(file_path))

        creation_time = time.ctime(os.path.getctime(file_path))

        omodification_time = ''

        grp = [file_name, creation_time, nmodification_time, omodification_time, False]

        files_present.append(grp)
    
    WriteMtd(files_present, 0)
    logging.info("GetFilesNameTime has completed the task.")

def WriteMtd(files, action):
    #actions: 0 -> Creation of the file, 1 -> Appending the data, 2 -> Deleting the data
    logging.info("WriteMtd is being executed...")
    if action == 0:
        logging.info("Function creating FilesRcord.infofl...")
        with open("", 'wb') as record:          #Enter the location of the folder from where you want to read the files.
            pickle.dump(files, record)
        logging.info("Writing Task completed.")

    elif action == 1:
        logging.info("Function extending the record file...")
        with open("", 'rb') as record:          #Enter the location of the folder from where you want to read the files.
            data = pickle.load(record)
        for file in files:
            if file not in data:
                data.append(file)
        with open("", 'wb') as record:          #Enter the location of the folder from where you want to read the files.
            pickle.dump(data, record)
        logging.info("Appending Task completed.")

    elif action == 2:
        logging.info("Function deleting the deleted files record.")
        with open("", 'rb') as record:          #Enter the location of the folder from where you want to read the files.
            data = pickle.load(record)
        for file in files:
            if file in data:
                ind = data.index(file)
                del data[ind]
        with open("", 'wb') as record:          #Enter the location of the folder from where you want to read the files.
            pickle.dump(data, record)
        logging.info("Deletion Task completed.")


def ReadMtd():
    logging.info("ReadMtd is being executed...")
    with open("", 'rb') as record:          #Enter the location of the folder from where you want to read the files.
        data = pickle.load(record)
    logging.info("ReadMtd has completed the task.")
    return data

def ManageFilesRecord():
    logging.info("ManageFilesRecord function is being executed...")
    RcodFiles = ReadMtd()
    ActalFiles = []

    for file_name in os.listdir('\\'):           #Enter the folder to be uploaded/maintained 
        file_path = os.path.join('\\', file_name)        #Enter the folder to be uploaded/maintained 
        modification_time = time.ctime(os.path.getmtime(file_path))
        creation_time = time.ctime(os.path.getctime(file_path))
        grp = [file_name, creation_time, modification_time, ' ', False]
        ActalFiles.append(grp)

    if len(RcodFiles) > len(ActalFiles):
        logging.info("Checking files that are to be deleted and updating their modification time")
        TdFiles = []
        for file in RcodFiles:
            if file not in ActalFiles:
                TdFiles.append(file)
            else:
                i = ActalFiles.index(file)
                file[3] = file[2]
                file[2] = ActalFiles[i][2]
        WriteMtd(TdFiles, 2)
        logging.info("Files from record has been removed")

    elif len(RcodFiles) < len(ActalFiles):
        logging.info("Checking files that are newly created and updating their modification time")
        NwFiles = []
        for file in ActalFiles:
            if file not in RcodFiles:
                NwFiles.append(file)
            else:
                i = RcodFiles.index(file)
                RcodFiles[i][3] = RcodFiles[i][2]
                RcodFiles[i][2] = file[2]
        WriteMtd(NwFiles, 1)
        logging.info("Files in the record has been added.")

    else:
        logging.info("Record and actual files are same in number and updating the modification time only.")
        notLocated = []
        for file in ActalFiles:
            Aind = ActalFiles.index(file)
            try:
                Rind = RcodFiles.index(file)
                RcodFiles[Rind][3] = RcodFiles[Rind][2]
                RcodFiles[Rind][2] = ActalFiles[Aind][2]
            except ValueError:
                notLocated.append(file) 
        if notLocated != []:
            WriteMtd(notLocated,1)
            ManageFilesRecord()
            logging.info("Missing files has been updaetd in the record")
        else:
            WriteMtd(RcodFiles,0)
            logging.info("The modification time has been updated.")

# #_______testing__________
# GetFilesNameTime()
# with open("./DeviceOprtn/FilesRcord.infofl", 'rb') as record:
#     data = pickle.load(record)
# try:
#     data = ReadMtd()
#     for file in data:
#         print(file)
# except Exception as e:
#     print(e)