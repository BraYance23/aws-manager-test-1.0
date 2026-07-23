import requests

def get_ip_public()-> str|None:

    urls = [
        "https://icanhazip.com",
        "https://wtfismyip.com/text",
        "https://ifconfig.me"
        ]
    
    for url in urls:
        try:
            response = requests.get(url,timeout=3).text.strip()
            if response:
                ip_public = f"{response}/32"
                return ip_public
            continue
        except requests.exceptions.Timeout:
            continue
        except Exception:
            continue
    return None