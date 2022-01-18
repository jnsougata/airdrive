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
                print(f"Account `{username}` already exists!")
                print(f"Logged in as `{username}` instead.")
                print('-----')
                return cls.login(username, password, private_key)
            print(f"Account `{username}` created!")
            drive.put(name='.air', data=b'')
            return cls(drive)
        except AssertionError:
            raise ValueError("Used an invalid login token!")

    @classmethod
    def login(cls, username: str, password: str, private_key: str = None):
        key = private_key if private_key else KEY
        try:
            drive = Deta(key).Drive(f'{username}_{password}')
            files = drive.list().get('names')
            if files:
                print(f"Logged in as `{username}`.")
                print('-----')
                return cls(drive)
            else:
                raise Exception(f"Account `{username}` doesn't exist!")
        except AssertionError:
            raise ValueError("Used an invalid login token!")

    def files(self):
        return self.drive.list().get('names')

    def upload(self, local_file_path: str, remote_file_name: str):
        with open(local_file_path, "rb") as f:
            content = f.read()
            self.drive.put(name=remote_file_name, data=content)
            print(f"[↑] {remote_file_name} | {round(len(content) * 10 ** (-6), 3)} MB")

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

    def delete(self, file_name: str = None, file_names: list = None):
        if file_name:
            self.drive.delete(file_name)
            print(f"[!] Deleted `{file_name}`")
        if file_names:
            self.drive.delete_many(file_names)
            print(f"[!] Deleted `{' , '.join(file_names)}`")

    def delete_all(self):
        files = self.files()
        try:
            files.remove('.air')
        except ValueError:
            self.drive.put(name='.air', data=b'')
        self.drive.delete_many(files)
        print("[!] Deleted all files!")

    def delete_account(self):
        try:
            self.drive.delete_many(self.files())
            print("[!] Account deleted!")
        except AssertionError:
            print("[!] Account not found!")
