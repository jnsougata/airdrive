## AirDrive
AirDrive lets you store **unlimited** files to cloud for **free**.**Upload** & **download** files from your personal drive at any time using its super-fast API. 

### Installation
`pip install airdrive`

### Import
`from airdrive import AirDrive`

### Creating New Drive
`drive = AirDrive.create(username: str, password: str)`

### Logging In
`drive = AirDrive.login(username: str, password:str)`

### Methods
- `files`  returns list of file names existing in the drive
- `download(file_name: str)` downloads file from the drive
- `download_all` downloads all files from the drive
- `upload(local_file_path: str, remote_file_name: str)` uploads file to the drive
- `rename(old_file_name: str, new_file_name: str)` re-uploads file with new name ⚠
- `cache(file_name: str)` caches a file from the drive
- `delete(file_name: str)` deletes file from the drive permanently ⚠
- `delete_all` deletes all files from the drive permanently ⚠
- `delete_account`   deletes airdrive account permanently ⚠
