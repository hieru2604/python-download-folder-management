import os
import shutil

if os.name == 'nt':
    import ctypes
    from ctypes import windll, wintypes
    from uuid import UUID

    # ctypes GUID copied from MSDN sample code
    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", wintypes.BYTE * 8)
        ] 

        def __init__(self, uuidstr):
            uuid = UUID(uuidstr)
            ctypes.Structure.__init__(self)
            self.Data1, self.Data2, self.Data3, \
                self.Data4[0], self.Data4[1], rest = uuid.fields
            for i in range(2, 8):
                self.Data4[i] = rest>>(8-i-1)*8 & 0xff

    SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(GUID), wintypes.DWORD,
        wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
    ]

    def _get_known_folder_path(uuidstr):
        pathptr = ctypes.c_wchar_p()
        guid = GUID(uuidstr)
        if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(pathptr)):
            raise ctypes.WinError()
        return pathptr.value

    FOLDERID_Download = '{374DE290-123F-4565-9164-39C4925E467B}'

    def get_download_folder():
        return _get_known_folder_path(FOLDERID_Download)
else:
    def get_download_folder():
        home = os.path.expanduser("~")
        return os.path.join(home, "Downloads")
    
# all the above to get the download path @@
directory = get_download_folder()


extensions = {
".jpg"  : "Images",
".jpeg" : "Images",
".png"  : "Images",
".gif"  : "Images",

".mp4"  : "Videos",
".mov"  : "Videos",
".wmv"  : "Videos",
".avi"  : "Videos",

".doc"  : "Documents",
".docx" : "Documents",
".pdf"  : "Documents",
".ppt"  : "Documents",
".txt"  : "Documents",
".xlsx" : "Documents",

".mp3"  : "Music",
".wav"  : "Music",
".flac"  : "Music"
}

for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)

    if os.path.isfile(file_path):

        # lower file extension incase its upper. like WAV?
        extension = os.path.splitext(filename)[1].lower()

        if extension in extensions:
            folder_name = extensions[extension]

            # make dir incase it doesnt exist
            folder_path = os.path.join(directory, folder_name)
            os.makedirs(folder_path, exist_ok = True)

            # 
            destination_path = os.path.join(folder_path,filename)
            shutil.move(file_path, destination_path)

            print(f"Moved {filename} to {folder_name} folder.")
        else:
            print(f"skipped {filename}. Unknown file extension.")
    else:
        print(f"skipped {filename}. It is a directory.")

print("File organization completed.")