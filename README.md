![logo](https://raw.githubusercontent.com/jnsougata/AirDrive/main/ui/air.png)   
## AirDrive
AirDrive lets you store **unlimited** files to cloud for **free**. **Upload** & **download** files from your personal drive at any time using its super-fast API. 

## Installation
### `pip install airdrive`

## Import
### `from airdrive import AirDrive`

## Creating New Account
### `drive = AirDrive.create(username, password, silent = True)`
- Parameters:
  - **username** (str): Name of the user
  - **password** (str): Password of the user
  - **silent** (bool): If True, it will not show any prompts

## Logging In
### `drive = AirDrive.login(username, password, silent = True)`
- Parameters:
  - **username** (str): Name of the user
  - **password** (str): Password of the user
  - **silent** (bool): If True, it will not show any prompts

## Methods

### `files`  
- `files()`
  - #### Returns:
    Returns list of file names existing in the drive
### `create_folder`
- `create_folder(folder_name)`
  - Parameters:
  - **folder_name** (str): Name of the folder to be created
  - #### Returns:
    Returns the name of the folder created
### `download`
- `download(file_name)`
    - Parameters:
      - **file_name** (str): Name of the file to be downloaded
    - #### Returns:
      Returns None & downloads the file to the current directory
    - #### Raises:
      - `FileNotFoundError`: If the file is not found in the drive
### `download_all`
- `download_all()`
    - #### Returns:
      - Returns None & downloads all files in the drive to the current directory
### `upload`
- `upload(remote_file_name, )`
    - Parameters:
      - **remote_file_name** (str): The name with the file to be uploaded
      - **folder_name** (str): The name of the folder to upload the file to (optional)
      - **local_file_path** (str): Path to the file to be uploaded (optional)
      - **file_content** (Union[bytes | str | io.TextIOBase | io.BufferedIOBase | io.RawIOBase]): Content of the file to be uploaded (optional)
      - Note: If `local_file_path` is not provided, `file_content` must be provided
    - #### Returns:
      Returns None & uploads the file to the drive
    - ### Note:
      - If the file already exists in the drive, it will be overwritten
### `upolad_from_url`
- `upload_from_url(url, file_name, folder_name)`
    - Parameters:
      - **url** (str): URL of the file to be uploaded
      - **file_name** (str): The name with the file to be uploaded
      - **folder_name** (str): The name of the folder to upload the file to(optional)
    - #### Returns:
      Returns the file content (bytes)
    - ### Raises:
      - `ValueError`: If the url is invalid
    - ### Note:
      - If the file already exists in the drive, it will be overwritten
### `rename`
- `rename(old_file_name, new_file_name)`
    - Parameters:
      - **old_file_name** (str): The old name of file to be renamed
      - **new_file_name** (str): New name of the file
    - #### Returns:
      Returns None & re-uploads the file in the drive with new name
    - ### Note:
      - Might take a while for large files
### `cache`
- `cache(file_name)`
    - Parameters:
      - **file_name** (str): Name of the file to be cached
    - #### Returns:
      Returns the file content as bytes
    - ### Raises:
      - `FileNotFoundError`: If the file is not found in the drive
### `file_stream`
- `file_stream(file_name)`
    - Parameters:
      - **file_name** (str): Name of the file to be streamed
    - #### Returns:
      Returns the file content as stream
    - ### Raises:
      - `FileNotFoundError`: If the file is not found in the drive
### `delete`
- `delete(file_name)`
    - Parameters:
      - **file_name** (str): Name of the file to be deleted
    - #### Returns:
      Returns None & deletes the file from the drive permanently
### `delete_all`
- `delete_all()`
    - #### Returns:
      Returns None & deletes all files from the drive permanently
### `delete_account`
- `delete_account()`
    - #### Returns:
      Returns None & deletes the account from the drive permanently
    - ### Raises:
      - `Exception`: If the account does not exist
      