from constant.keys import base_url,base_Socket_url


def generate_url(path: str) -> str:
    return base_url + "/" + path



def generate_Socket_url(path: str) -> str:
    return base_Socket_url + "/" + path