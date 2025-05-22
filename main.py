from utils import *

class VCB:
    def __init__(self, username: str = "", password: str = "", browserID = "", proxies: dict = {}, session: object = None) -> None:
        if session:
            self.session = session
        else:
            self.session = requests.Session()
        self.username = username
        self.password = password
        self.browserID = browserID
        if proxies:
            self.session.proxies.update(
                {
                    "http": proxies.get("http"),
                    "https": proxies.get("https")
                }
            )
        self.session.headers.update(self._headers())
        update_cookies = self.session.get("https://vcbdigibank.vietcombank.com.vn/auth")
        self.private_key, self.public_key = gen_keys()
        login_data = self._login()
        try:
            self.login_message = login_data["message"]
        except:
            self.login_message = ""
        self.login_logs = login_data["message"]
        self.is_login = login_data["status"]

    def _headers(self) -> dict:
        return {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
            'cache-control': 'no-cache',
            'dnt': '1',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        }
    
    def _post_headers(self) -> dict:
        return {
                'accept'            : 'application/json, text/plain, */*',
                'accept-language'   : 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
                'cache-control'     : 'no-cache',
                'content-type'      : 'application/json',
                'dnt'               : '1',
                'origin'            : 'https://vcbdigibank.vietcombank.com.vn',
                'pragma'            : 'no-cache',
                'priority'          : 'u=1, i',
                'referer'           : 'https://vcbdigibank.vietcombank.com.vn/',
                'sec-ch-ua'         : '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
                'sec-ch-ua-mobile'  : '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest'    : 'empty',
                'sec-fetch-mode'    : 'cors',
                'sec-fetch-site'    : 'same-site',
                'user-agent'        : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
                'x-channel'         : 'Web',
                'x-lim-id'          : '',
                'x-request-id'      : ''
            }
    
    def _login(self) -> dict:
        captcha_guid = create_guid()
        fake_data = {
            "DT": "Windows",
            "E": None,
            "OV": "10",
            "PM": "Chrome 136.0.0.0",
            "appVersion": "",
            "browserId": self.browserID, #sử dụng id của trình duyệt để tự dộng đăng nhập
            "captchaToken": captcha_guid,
            "captchaValue": Captcha(captcha_guid).solving(),
            "cif": None,
            "lang": "vi",
            "mid": 6,
            "password": self.password,
            "user": self.username
        }
        enc = encrypt_request(fake_data, self.public_key, LOCAL["publicKey"])
        response = self.session.post(
            url = "https://digiapp.vietcombank.com.vn/authen-service/v1/login", 
            json=enc, 
            headers = self._post_headers()
        ).json()
        dec = decrypt_response(response, self.private_key)
        if dec["code"] == "019":
            return {
                "status": False,
                "message" : "chưa mở login web setting",
                "data" : dec
            }
        elif dec["code"] == "20231":
            return {
                "status": False,
                "message" : "browser is not activated",
                "data" : dec
            }
        elif dec["code"] == "0111":
            """captcha not fit"""
            return self._login()
        elif dec["code"] == "9993":
            return {
                "status": False,
                "message" : "Data format error",
                "data" : dec
            }
        elif dec["code"] == "3005":
            return {
                "status": False,
                "message" : "Unable username or password",
                "data" : dec
            }
        elif dec["code"] == "00":
            self.session_id = dec["sessionId"]
            self.access_key = dec["accessKey"]
            self.cif        = dec["userInfo"]["cif"]
            self.mobileId   = dec["userInfo"]["mobileId"]
            self.accountNo  = dec["userInfo"]["defaultAccount"]
            self.clientId   = dec["userInfo"]["clientId"]
            
            return {
                "status": True,
                "message" : "login success",
                "data" : dec
            }
    
    def _checksum():
        #khong can thiet :D
        pass

    def _bank_soft_otp():
        #khong can thiet :D
        pass

    def _get_home_popup():
        #khong can thiet :D
        pass

    def _get_config_value():
        #khong can thiet :D
        pass

    def _get_insight_token():
        #khong can thiet :D
        pass

    def _get_list_account_via_cif():
        #khong can thiet :D
        pass

    def _get_account_detai():
        #khong can thiet :D
        pass

    def _transaction_history(self, from_date: str ="", to_date: str = "", page_index: int = 0):
        """
        "fromDate": "12/05/2025",
        "toDate": "19/05/2025",
        """
        json_data = {
            "DT": "Windows",
            "E": None,
            "OV": "10",
            "PM": "Chrome 136.0.0.0",
            "accountNo": self.accountNo,
            "accountType": "D",
            "appVersion": "",
            "browserId": self.browserID,
            "cif": self.cif,
            "clientId": self.clientId,
            "clientPubKey": self.public_key,
            "fromDate": from_date,
            "lang": "vi",
            "lengthInPage": 10,
            "mid": 14,
            "mobileId": self.mobileId,
            "pageIndex": page_index,
            "sessionId": self.session_id,
            "toDate": to_date,
            "user": self.username
        }
        history = []
        enc = encrypt_request(json_data, self.public_key, LOCAL["publicKey"])
        response = self.session.post(
            url = "https://digiapp.vietcombank.com.vn/bank-service/v1/transaction-history", 
            json=enc, 
            headers = self._post_headers()
        ).json()
        dec = decrypt_response(response, self.private_key)
        if dec["code"] == "00":
            return {
                "code" : dec["code"],
                "status" : True,
                "history" : dec["transactions"],
                "next_index" : dec["nextIndex"]
            }
        
        elif dec["code"] == "108":
            self._login()
            return self._transaction_history(from_date, to_date)
        
        return {
            "status" : False,
            "code" : dec["code"],
            "full_content" : dec
        }

    def get_full_transation_history(self, from_date: str = "", to_date: str = ""):
        if not self.is_login:
            raise Exception(f"Cannot login! : {self.login_logs}")
        
        def initalizing_response(data: dict = {}) -> list:
            if data["status"]:return data["history"]
            return []
        
        page_index = 0
        history = []
        while True:
            page_data = self._transaction_history(from_date, to_date, page_index)
            if int(page_data["next_index"]) == 1:
                transactions = initalizing_response(page_data)
            else:
                break
            history.extend(transactions)
            page_index += 1
        return {
            "code" : "00",
            "status" : True,
            "history" : history
        }
    
if __name__ == "__main__":
    userdata = json.loads(open("config/user.json", "r", encoding="utf-8").read())
    username, password, browser_id = userdata["username"], userdata["password"], userdata["browser_id"]
    
    print(
        VCB(
            username=username, 
            password=password, 
            browserID=browser_id
        ).get_full_transation_history(*get_date())
    )
