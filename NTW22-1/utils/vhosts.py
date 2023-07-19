from __future__ import annotations

from pathlib import Path
from typing import Dict

from settings import VHOSTS_FILE


from http.response import HttpResponseNotFound, HttpResponseForbidden


class Vhost:
    __hostname = None
    __index = None
    __name = None
    __email = None

    def __init__(self, hostname: str, index: str, name: str, email: str):
        self.__hostname = hostname
        self.__index = index
        self.__name = name
        self.__email = email

    @staticmethod
    def parse_file(file: str = VHOSTS_FILE) -> Dict[str, Vhost]:
        out = {}
        # Get the root of the server
        root_server = Path().parent
        # Open the file from the root of the server
        with open(root_server.joinpath(file).absolute(), 'r') as f:
            for line in f.readlines():
                # Start parsing the virtual host line and, if any error appears, discard the line
                line = line.strip()
                if line == "":
                    continue
                # Line should have 4 items
                splitted = [e.strip() for e in line.split(",")]
                if len(splitted) != 4:
                    continue
                # If any element is empty, discard
                hostname, index, name, email = splitted
                if hostname == "" or index == "" or name == "" or email == "":
                    continue
                hostname = hostname.lower()

                # Check if the specified path for the host exists
                root_host = root_server.joinpath(hostname)
                if not root_host.exists() or root_host.is_file():
                    continue
                # Check if the root file exists
                root_file = root_host.joinpath(index)
                if not root_file.exists() or not root_file.is_file():
                    continue
                # Create the Vhost and add it
                vhost = Vhost(hostname, index, name, email)
                out[hostname] = vhost
        return out

    def get_hostname(self) -> str:
        return self.__hostname

    def get_index_file(self) -> str:
        return self.__index

    def get_server_admin_name(self) -> str:
        return self.__name

    def get_server_admin_email(self) -> str:
        return self.__email

    def get_host_root_path(self) -> Path:
        return Path().parent.joinpath(self.__hostname).absolute()

    @staticmethod
    def is_secure_path(path: str) -> bool:
        """
        Given a path, check if it is secure, i.e. does not go outside the virtual host filesystem
        :param path: path to be checked
        :return: True if path never leaves host folder
        """

        parts = path.split("/")
        level = 0
        for part in parts:
            # If an empty path is found (//) or a dot (/./), it means no change
            if part == '' or part == '.':
                continue
            # If "previous" path is found (/../), we substract one to the level
            elif part == '..':
                level -= 1
            # Otherwise, we increase by one the subfolder level
            else:
                level += 1

            # If we ever go outside this folder, return False
            if level < 0:
                return False
        # If we never left filesystem root folder, it is safe
        return True

    def __str__(self) -> str:
        return "{}({})".format(self.__hostname, self.__email)

    @staticmethod
    def get_file_contents(path: Path) -> str:
        try:
            with open(path, mode='rb') as f:
                return f.read()        
        except FileNotFoundError:
            raise HttpResponseNotFound()
        except PermissionError:
            raise HttpResponseForbidden()
    
    
    @staticmethod
    def delete_file(path: Path, root: Path) -> str:
        """
        Deletes the file and then deletes the folder
        and its parents only if they are empty
        """
        try:
            path.unlink()
            path = path.parent
        except PermissionError:
            raise HttpResponseForbidden()

        while path != root:
            try:
                path.rmdir()
                path = path.parent
            except PermissionError:
                break
            except OSError:
                break
