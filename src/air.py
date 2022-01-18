import io
from .key import KEY
from deta import Deta
from typing import Union


class AirDrive:
    def __init__(self, drive: Deta.Drive):
        self.drive = drive

    def __repr__(self):
        return f"<AirDrive>"

    @classmethod
    def create(cls, username: str, password: str, private_key: str = None):
        """
        Create a new account
        :param username : new username for the account
        :param password: password for the account
        :param private_key: https://deta.sh project key (optional)
        :return: AirDrive object
        """
        key = private_key if private_key else KEY
        if len(username) < 5:
            raise ValueError("Use at least 5 characters!")
        if password == KEY:
            raise ValueError("Don't use project key as password!")
        if len(password) < 8:
            raise ValueError("Use at least 8 characters!")
        if username == password:
            raise ValueError("Username and password can't be the same!")
        try:
            drive = Deta(key).Drive(f'{username}_{password}')
            files = drive.list().get('names')
            if files:
                return cls.login(username, password, private_key)
            print(f"Account `{username}` created!")
            drive.put(name='.air', data=b' ')
            return cls(drive)
        except AssertionError:
            raise ValueError("Used an invalid login token!")

    @classmethod
    def login(cls, username: str, password: str, private_key: str = None):
        """
        Login to an existing account
        :param username: username associated the account
        :param password: password associated the account
        :param private_key: https://deta.sh project key (optional)
        :return: AirDrive object
        """
        key = private_key if private_key else KEY
        try:
            drive = Deta(key).Drive(f'{username}_{password}')
            files = drive.list().get('names')
            if files:
                print(f"Logged in as `{username}`")
                print('-----')
                return cls(drive)
            else:
                raise Exception(f"Account `{username}` doesn't exist!")
        except AssertionError:
            raise ValueError("Used an invalid login token!")

    def files(self) -> list:
        """
        :return: list of files in the account
        """
        return self.drive.list().get('names')

    def create_folder(self, folder_name: str) -> None:
        """
        Create a new folder in the drive
        :param folder_name: the name of the folder to create
        :return: None
        """
        path = f'{folder_name}/.air'
        self.drive.put(name=path, data=b' ')
        print(f"[+] Created folder `{folder_name}`")

    def upload(
            self,
            remote_file_name: str,
            local_file_path: str = None,
            file_content: Union[bytes, str, io.TextIOBase, io.BufferedIOBase, io.RawIOBase] = None,
            folder_name: str = None
    ) -> None:
        """
        Upload a file to the drive
        :param local_file_path: path to the local file
        :param remote_file_name: name with which the file will be saved on the drive
        :param folder_name: folder in which the file will be saved on the drive (optional)
        :param file_content: content of the file to be sent (optional)
        :return: None
        """
        if local_file_path:
            with open(local_file_path, "rb") as f:
                content = f.read()
        elif file_content:
            content = file_content
        else:
            raise ValueError("You must specify a file path or content!")
        if folder_name:
            path = f'{folder_name}/{remote_file_name}'.replace('//', '/')
            self.drive.put(name=path, data=content)
            print(f"[↑] {path} | {round(len(content) * 10 ** (-6), 3)} MB")
        else:
            self.drive.put(name=remote_file_name, data=content)
            print(f"[↑] {remote_file_name} | {round(len(content) * 10 ** (-6), 3)} MB")

    def rename(self, old_name: str, new_name: str) -> None:
        """
        Rename a file on the drive
        :param old_name: old name of the file
        :param new_name: new name of the file to be saved
        :return: None
        """
        content = self.cache(old_name)
        self.drive.put(name=new_name, data=content)
        print(f"[!] Renamed `{old_name}` to `{new_name}`")

    def download(self, file_name: str) -> None:
        """
        Download a file from the drive
        :param file_name: name/path of the file to download
        :return: None
        """
        resp = self.drive.get(file_name)
        if resp:
            print(f'[↓] Downloading `{file_name}`...')
            with open(file_name, "wb") as f:
                size = 0
                for chunk in resp.iter_chunks(1024):
                    if chunk:
                        size += len(chunk)
                        f.write(chunk)
            print(f"[↓] Completed: {file_name} | {round(size * 10 ** (-6), 3)} MB")
        else:
            raise FileNotFoundError(f"file `{file_name}` does not exist!")

    def file_stream(self, file_name: str) -> bytes:
        """
        Download a file from the drive and return its content (streamable)
        :param file_name: name/path of the file to stream
        :return: bytes
        """
        stream = self.drive.get(file_name)
        if stream:
            return stream
        raise FileNotFoundError(f"file `{file_name}` does not exist!")

    def cache(self, file_name: str) -> bytes:
        """
        Download a file from the drive and return its content (bytes)
        :param file_name: name/path of the file to cache
        :return: bytes
        """
        resp = self.drive.get(file_name)
        if resp:
            print(f'[🗎] Caching `{file_name}`...')
            byte_list = [chunk for chunk in resp.iter_chunks(1024)]
            print(f'[🗎] Done: `{file_name}`...')
            return b''.join(byte_list)
        raise FileNotFoundError(f"file `{file_name}` does not exist!")

    def download_all(self) -> None:
        """
        Download all files in the account to the current directory
        :return: None
        """
        for file_name in self.files():
            self.download(file_name)

    def delete(self, file_name: str = None, file_names: list = None) -> None:
        """
        Delete a file from the drive
        :param file_name: file name/path to delete
        :param file_names: list of file names/paths to delete
        :return: None
        """
        if file_name:
            self.drive.delete(file_name)
            print(f"[!] Deleted `{file_name}`")
        if file_names:
            self.drive.delete_many(file_names)
            print(f"[!] Deleted `{' , '.join(file_names)}`")

    def delete_all(self) -> None:
        """
        Delete all files in the drive
        :return: None
        """
        files = self.files()
        try:
            files.remove('.air')
        except ValueError:
            self.drive.put(name='.air', data=b' ')
        self.drive.delete_many(files)
        print("[!] Deleted all files!")

    def delete_account(self) -> None:
        """
        Deletes the entire account
        :return: None
        """
        try:
            self.drive.delete_many(self.files())
        except AssertionError:
            raise Exception("Account not found!")
