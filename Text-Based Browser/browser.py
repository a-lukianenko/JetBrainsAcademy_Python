import os
import sys
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore


class Browser:

    def __init__(self):
        self.web_stack = deque()
        self.response = None
        self.headers = {'user-agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64)'
                                      'AppleWebKit / 537.36(KHTML, like Gecko)'
                                      'Chrome / 85.0.418..121'
                                      'Safari / 537.36'}
        self.tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']

    def is_saved(self, directory, url):
        for wp in os.listdir(directory):
            return url == wp

    def save_webpage(self, directory, url, text):
        tab = url.rsplit(".", 1)[0]
        with open(os.path.join(directory, tab), 'w') as file:
            file.write(text)

    def read_saved_wp(self, directory, wp):
        with open(os.path.join(directory, wp), 'r') as file:
            print(file.read())

    def get_page(self, url):
        return requests.get(f"https://{url}", headers=self.headers)

    def extract_text(self, response):
        text = ''
        soup = BeautifulSoup(response.content, 'html.parser')
        tags = soup.find_all(self.tags)
        for tag in tags:
            if tag.name == "a":
                text += Fore.BLUE + tag.text + '\n'
            else:
                text += tag.text + '\n'
        return text

    def start(self):
        directory = sys.argv[-1]
        if not os.path.exists(directory):
            os.mkdir(directory)
        while True:
            url = input()
            if url == "exit":
                return
            elif url == "back" and len(self.web_stack) <= 1:
                continue
            elif url == "back":
                self.web_stack.pop()
                self.read_saved_wp(directory, self.web_stack[-1])
                continue
            elif self.is_saved(directory, url):
                self.read_saved_wp(directory, url)
                continue
            else:
                try:
                    self.response = self.get_page(url)
                except requests.exceptions.ConnectionError:
                    print("Error: Incorrect URL")
                    continue
                else:
                    self.web_stack.append(url)
                    text = self.extract_text(self.response)
                    self.save_webpage(directory, url, text)
                    print(text)
                    continue


Browser().start()
