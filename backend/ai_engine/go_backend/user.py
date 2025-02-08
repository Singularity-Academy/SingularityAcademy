import json
from dataclasses import dataclass

import requests


@dataclass()
class User:
    ID: int
    Username: str
    Email: str
    def __init__(self, jwt: str):
        print(jwt)
        response = requests.get('http://127.0.0.1:1298/api/me', headers={'Authorization': f'Bearer {jwt}'})
        # 检查http状态码
        if response.status_code != 200:
            raise RuntimeError(response.text)
        # 检查返回格式是否为json
        try:
            info = response.json()
        except json.decoder.JSONDecodeError:
            raise RuntimeError(response.text)
        # 检查返回的json格式是否正确
        if info.keys() != {'id', 'name', 'email'}:
            raise RuntimeError(response.text)
        self.ID = info['id']
        self.Username = info['name']
        self.Email = info['email']