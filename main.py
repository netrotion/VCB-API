from utils import *

#https://vcbdigibank.vietcombank.com.vn/default-libs_shared_services_src_index_ts.3ac1e1e8a8a6e65f.

class VCB:
    def __init__(self, username: str = "", password: str = "", browserID = "", proxies: dict = {}, session: object = None) -> None:
        if session:
            self.session = session
        else:
            self.session = requests.Session()
            if proxies:
                self.session.proxies.update(
                    {
                        "http": proxies.get("http"),
                        "https": proxies.get("https")
                    }
                )
                self.session.headers.update(self._headers())
                update_cookies = self.session.get("https://vcbdigibank.vietcombank.com.vn/auth")
        
        self.mid = {
            "login" : 6,
            "balance" : 13,
            "transaction_history" : 14,
            "nquiry_holdername" : 917

        }
        self.session_id = ""
        self.access_key = ""
        self.cif        = None
        self.mobileId   = ""
        self.accountNo  = ""
        self.clientId   = ""
        self.login_message = ""
        self.x_lim_id = ""
        self.x_requests_id = ""
        self.is_login = False
        self.username = username
        self.password = password
        self.browserID = browserID
        self.BANKLISTS = BANK_CODE()
        self.private_key, self.public_key = gen_keys()
        login_data = self._login()
        try:
            self.login_message = login_data["message"]
        except:
            self.login_message = ""
        self.login_logs = login_data["message"]
        self.is_login = login_data["status"]

    def  _get_default_json(self, additional_dict: dict = {}) -> dict:
        default = {
            "DT": "Windows",
            "E": None,
            "OV": "10",
            "PM": "Chrome 136.0.0.0",
            "accountType": "D",
            "appVersion": "",
            "browserId": self.browserID,
            "cif": None,
            "clientPubKey": self.public_key,
            "lang": "vi",
            "user": self.username,
        }
        if self.access_key:
            default["accountNo"] = self.accountNo
            default["clientId"] = self.clientId
            default["cif"] = self.cif
            default["mobileId"] = self.mobileId
            default["sessionId"] = self.session_id
            self.x_lim_id = x_lim_id(self.username)
            self.x_requests_id = x_requests_id(self.username)
        return {
            **default,
            **additional_dict
        }
    
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
    
    def _post_headers(self, additional_dict: dict = {}) -> dict:
        headers = {
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
            'x-lim-id'          : self.x_lim_id,
            'x-request-id'      : self.x_requests_id,
            **additional_dict
        }
        return headers
    
    def _login(self) -> dict:
        """dang nhap web"""
        captcha_guid = create_guid()
        response = self.session.post(
            url = "https://digiapp.vietcombank.com.vn/authen-service/v1/login", 
            json=encrypt_request(
                data=self._get_default_json(
                    {
                        "captchaToken": captcha_guid,
                        "captchaValue": Captcha(captcha_guid).solving(),
                        "mid": self.mid["login"],
                        "password": self.password,
                    }
                ), 
                client_pub_key_str=self.public_key, 
                server_pub_key_base64=LOCAL["publicKey"]
            ), 
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

    def _nquiry_holdername(self, accountNo: str = "", bankCode: str = ""):
        """kiem tra so tai khoan bank trong nuoc"""

        response = self.session.post(
            url="https://digiapp.vietcombank.com.vn/napas-service/v1/inquiry-holdername",
            json=encrypt_request(
                data=self._get_default_json(
                    {
                        "mid": self.mid["nquiry_holdername"],
                        "accountNo": accountNo,
                        "bankCode": bankCode
                    }
                ), 
                client_pub_key_str=self.public_key, 
                server_pub_key_base64=LOCAL["publicKey"]
            ),
            headers=self._post_headers()
        ).json()
        return decrypt_response(response, self.private_key)
        
    def _get_account_balance(self, format: object = int) -> dict:
        """lay so du hien tai"""
        response = self.session.post(
            url="https://digiapp.vietcombank.com.vn/bank-service/v2/get-account-detail",
            json= encrypt_request(
                data = self._get_default_json(
                    {"mid" : self.mid["balance"]}
                ), 
                client_pub_key_str=self.public_key, 
                server_pub_key_base64=LOCAL["publicKey"]
            ),
            headers=self._post_headers()
        ).json()
        dec = decrypt_response(response, self.private_key)
        if dec["code"] == "00":
            balance = dec["accountDetail"]["availBalance"]
            if format == int:
                balance = int(balance.replace(",","").replace(".",""))
            return {
                "code" : dec["code"],
                "status" : True,
                "balance" : balance,
                "full_content" : dec
            }
        
        elif dec["code"] in ["108", "917"]:
            self._login()
            return self._get_account_balance(format=format)
        
        return {
            "status" : False,
            "code" : dec["code"],
            "full_content" : dec
        }

    def _transaction_history(self, from_date: str ="", to_date: str = "", page_index: int = 0) -> json:
        """
        lay danh sach lich su giao dich
        "fromDate": "12/05/2025",
        "toDate": "19/05/2025",
        """
        history = []
        response = self.session.post(
            url = "https://digiapp.vietcombank.com.vn/bank-service/v1/transaction-history", 
            json=encrypt_request(
            data = self._get_default_json(
                {
                    "mid" : self.mid["transaction_history"],
                    "lengthInPage": 10,
                    "pageIndex": page_index,
                    "fromDate": from_date,
                    "toDate": to_date,
                }
            ), 
            client_pub_key_str=self.public_key, 
            server_pub_key_base64=LOCAL["publicKey"]
            ), 
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
        
        elif dec["code"] in ["108", "917"]:
            self._login()
            return self._transaction_history(from_date, to_date)
        
        return {
            "status" : False,
            "code" : dec["code"],
            "full_content" : dec
        }

    def get_full_transation_history(self, from_date: str = "", to_date: str = ""):
        """lay tat ca danh sach lich su giao dich"""
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
        ).get_full_transation_history(*get_date())#._nquiry_holdername("<banknumber>", BANK_CODE().MB["bankcode"])#_get_account_balance()
    )
