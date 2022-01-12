from deta import Deta
from src.key import KEY


class BlackHole:
    def __init__(self, drive: Deta.Drive):
        self.drive = drive

    @classmethod
    def private_login(cls, project_key: str, username: str, password: str):
        if len(username) < 5:
            raise ValueError("Use at least 5 characters!")
        if password == project_key:
            raise ValueError("Don't use project key as password!")
        if len(password) < 8:
            raise ValueError("Use at least 8 characters!")
        if username == password:
            raise ValueError("Username and password can't be the same!")
        drive = Deta(project_key).Drive(f'{username}_{password}')
        drive.put(name='.blackhole', data=b'54 48 49 53 20 49 53 20 46 52 45 45 20 44 57 21')
        return cls(drive=drive)

    @classmethod
    def login(cls, username: str, password: str):
        if len(username) < 5:
            raise ValueError("Use at least 5 characters!")
        if password == KEY:
            raise ValueError("Don't use project key as password!")
        if len(password) < 8:
            raise ValueError("Use at least 8 characters!")
        if username == password:
            raise ValueError("Username and password can't be the same!")
        drive = Deta(KEY).Drive(f'{username}_{password}')
        drive.put(name='.blackhole', data=b'54 48 49 53 20 49 53 20 46 52 45 45 20 44 57 21')
        return cls(drive=drive)

    def files(self):
        return self.drive.list().get('names')

    def upload(self, file_path: str, file_name: str):
        with open(file_path, "rb") as f:
            content = f.read()
            self.drive.put(name=file_name, data=content)
            print(f"[↑] {file_name} | {round(len(content) * 10 ** (-6), 3)} MB")

    def download(self, file_name: str):
        resp = self.drive.get(file_name)
        if resp:
            with open(file_name, "wb") as f:
                size = 0
                for chunk in resp.iter_chunks(1024):
                    if chunk:
                        size += len(chunk)
                        f.write(chunk)
            print(f"[↓] {file_name} | {round(size * 10 ** (-6), 3)} MB")
        else:
            raise FileNotFoundError(f"file `{file_name}` does not exist!")

    def cache(self, file_name: str):
        resp = self.drive.get(file_name)
        if resp:
            byte_list = [chunk for chunk in resp.iter_chunks(1024)]
            return b''.join(byte_list)

    def delete(self, file_name: str = None, file_name_list: list = None):
        if file_name:
            self.drive.delete(file_name)
            print(f"[!] Deleted `{file_name}`")
        if file_name_list:
            self.drive.delete_many(file_name_list)
            print(f"[!] Deleted `{' , '.join(file_name_list)}`")

    def delete_all(self):
        self.drive.delete_many(self.files())
        self.drive.put(name='.blackhole', data=b'54 48 49 53 20 49 53 20 46 52 45 45 20 44 57 21')
        print("[!] Deleted all files!")

    def delete_account(self):
        try:
            self.drive.delete_many(self.files())
            print("[!] Account deleted!")
        except AssertionError:
            print("[!] Account not found!")
