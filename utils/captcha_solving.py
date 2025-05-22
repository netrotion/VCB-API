from ._algorithm import *

def gen_captcha_token(e: int) -> str:
    t = ""
    for _ in range(e):
        rand = int(65536 * (1 + os.urandom(1)[0] / 255))
        hex_str = hex(rand)[2:].zfill(4)[1:]
        t += hex_str
    return t

def create_guid() -> str:
    return "-".join([
        gen_captcha_token(2),
        gen_captcha_token(1),
        gen_captcha_token(1),
        gen_captcha_token(1),
        gen_captcha_token(3)
    ])



class Captcha:
    def __init__(self, captcha_guid: str, proxies: dict = {}) -> None:
        self.guid = captcha_guid
        self.session = requests.Session()
        if proxies:
            self.session.proxies.update(
                {
                    "http": proxies.get("http"),
                    "https": proxies.get("https")
                }
            )
        self.session.headers.update(self._headers())
    
    def _headers(self) -> dict:
        return {
            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
            'cache-control': 'no-cache',
            'dnt': '1',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://vcbdigibank.vietcombank.com.vn/',
            'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'image',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        }
    
    def solving(self):
        url = "https://hngl2808-predict.hf.space/predict"
        images = self.session.get(
            f"https://digiapp.vietcombank.com.vn/utility-service/v2/captcha/MASS/{self.guid}"
        ).content
        b64encimg = base64.b64encode(images).decode("utf-8")
        js = {"data": f"data:image/jpeg;base64,{b64encimg}"}
        response = self.session.post(url, json=js)
        if response.status_code == 200:
            return response.json()["result"]
        else:
            print("Error:", response.status_code, response.text)
            return None
