from django.shortcuts import render
import requests

OAUTH_TOKEN = "OAuth y0_AgAAAAB0kcnmAAxwrwAAAAERAbWhAACAfWv5JWNJyIbLGFGSCzc37wU3lA"
PUBLIC_BASE_URL = "https://cloud-api.yandex.net/v1/disk/public/resources/"
BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources/"

DEFAULT_HEADERS = {
    "Authorization": OAUTH_TOKEN,
    "Accept": "application/json"
}
DEFAULT_PATH = "disk:/Приложения/TestForMycego/"


def api_request(url, method='GET', params=None, headers=None):
    """
    Makes request to API and serialize response to JSON
    :param url: url for request
    :param method: method for request
    :param params: params for request
    :param headers: headers for request
    :return: if response is ok returns JSON else None
    """
    try:
        response = requests.request(method, url, params=params, headers=headers)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        print(e)
        return None


def get_public_key(path) -> str:
    """

    :param path: relative path to public folder
    :return: Return public key. If return None then not published source.
    """
    params = {
        "path": DEFAULT_PATH + f"{path}/" if path else DEFAULT_PATH,
        "fields": "public_key"
    }
    response = api_request(url=BASE_URL, method="GET", params=params, headers=DEFAULT_HEADERS)

    return response.get('public_key')


def get_public_files(public_key: str) -> list:
    params = {
        "public_key": public_key,
    }
    return api_request(url=PUBLIC_BASE_URL, method="GET", params=params,
                       headers=DEFAULT_HEADERS)['_embedded']['items']


def index(request, path=None):
    if request.method == "POST":
        pass

    public_key = get_public_key(path)
    if not public_key:
        return render(request, "NotPublic.html")
    data = {"items": get_public_files(public_key)}

    if path:
        data["backlink"] = 'localhost:8000'

    return render(request, "index.html", {"data": data})
