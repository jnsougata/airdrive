import json
from .key import KEY
from deta import Deta


class AirDrive:
    def __init__(self, drive: Deta.Drive):
        self.drive = drive

    def __repr__(self):
        return f"<AirDrive>"

    @classmethod
    def create(cls, username: str, password: str, private_key: str = None):
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
                raise Exception(f"Account `{username}` already exists!")
            print(f"Account `{username}` created!")
            return cls(drive)
        except AssertionError:
            raise ValueError(f"Invalid login token used!")

    @classmethod
    def login(cls, username: str, password: str, private_key: str = None):
        key = private_key if private_key else KEY
        try:
            drive = Deta(key).Drive(f'{username}_{password}')
            files = drive.list().get('names')
            if files:
                return cls(drive)
            else:
                raise Exception(f"Account `{username}` doesn't exist!")
        except AssertionError:
            raise ValueError(f"Invalid login token used!")

    def files(self):
        return self.drive.list().get('names')

    def upload(self, local_file_path: str, remote_file_name: str):
        with open(file_path, "rb") as f:
            content = f.read()
            self.drive.put(name=file_name, data=content)
            print(f"[↑] {file_name} | {round(len(content) * 10 ** (-6), 3)} MB")

    def rename(self, old_name: str, new_name: str):
        content = self.cache(old_name)
        self.drive.put(name=new_name, data=content)
        print(f"[!] Renamed `{old_name}` to `{new_name}`")

    def download(self, file_name: str):
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

    def cache(self, file_name: str):
        resp = self.drive.get(file_name)
        if resp:
            print(f'[🗎] Caching `{file_name}`...')
            byte_list = [chunk for chunk in resp.iter_chunks(1024)]
            print(f'[🗎] Done: `{file_name}`...')
            return b''.join(byte_list)
        raise FileNotFoundError(f"file `{file_name}` does not exist!")

    def download_all(self):
        for file_name in self.files():
            self.download(file_name)

    def delete(self, file_name: str = None, file_name_list: list = None):
        if file_name:
            self.drive.delete(file_name)
            print(f"[!] Deleted `{file_name}`")
        if file_name_list:
            self.drive.delete_many(file_name_list)
            print(f"[!] Deleted `{' , '.join(file_name_list)}`")

    def delete_all(self):
        self.drive.delete_many(self.files())
        self.drive.put(name='.air', data=b' ')
        print("[!] Deleted all files!")

    def delete_account(self):
        try:
            self.drive.delete_many(self.files())
            print("[!] Account deleted!")
        except AssertionError:
            print("[!] Account not found!")
