import json
import os

import requests
import base64

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")


def recogwav(user_wav):
    url = "https://vop.baidu.com/server_api"
    f = open('static/' + user_wav, "rb")
    enc = base64.b64encode(f.read()).decode()
    # print(enc)
    # "dev_pid": 1537中文 1737英文
    payload = json.dumps({
        "format": "wav",
        "rate": 16000,
        "channel": 1,
        "cuid": "cuid",
        "token": get_access_token(),
        "speech": enc,
        "len": f.tell(),
        "dev_pid": 1737
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    words = json.loads(response.text)
    try:
        return words["result"][0]
    except KeyError:
        return


def speechtts(text):
    url = "https://tsn.baidu.com/text2audio"
    payload = 'tex=' + text + '&tok=' + get_access_token() + '&cuid=cuid&ctp=1&lan=zh&spd=5&pit=5&per=5118&aue=6'
    # print(text)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return base64.b64encode(response.content)


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
