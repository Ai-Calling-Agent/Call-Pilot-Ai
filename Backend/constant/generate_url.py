from constant.keys import base_url


def generate_url(path: str) -> str:
    return base_url + "/" + path