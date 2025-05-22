from curl_cffi import requests
import base64
import os
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Util import Counter
from Crypto.Random import get_random_bytes
from Crypto import Random
from datetime import datetime, timezone, timedelta

VN_TZ = timezone(timedelta(hours=7))

#static
LOCAL = {
    "name": "production",
    "production": True,
    "manifestPath": "/assets/module-federation.manifest.production.json",
    "mobileCallUrl": "https://callapi-iframe.vietcombank.com.vn/",
    "apiUrl": "https://digiapp.vietcombank.com.vn",
    "mediaBaseUrl": "https://digibankm5.vietcombank.com.vn/get_file",
    "uploadAvatarUrl": "https://digibankm5.vietcombank.com.vn/upfile/avatar_upload",
    "removeAvatarUrl": "https://digibankm5.vietcombank.com.vn/contact/remove_my_avatar",
    "uploadAES": "2dcd8b543bd95a83",
    "uploadHMac": "94280a1454bc5634a33181125fcedc08",
    "token": "dmNiOjI3YWNkNDM1YmRiMjU5NTRhY2Q2NDliNmE1MTNmYmI5",
    "publicKey": "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUFpa3FRckl6WkprVXZIaXNqZnU1WkNOK1RMeS8vNDNDSWM1aEpFNzA5VElLM0hiY0M5dnVjMitQUEV0STZwZVNVR3FPbkZvWU93bDNpOHJSZFNhSzE3RzJSWk4wMU1JcVJJSi82YWM5SDRMMTFkdGZRdFI3S0hxRjdLRDBmajZ2VTRrYjUrMGN3UjNSdW1CdkRlTWxCT2FZRXBLd3VFWTlFR3F5OWJjYjVFaE5HYnh4TmZiVWFvZ3V0VndHNUMxZUtZSXR6YVlkNnRhbzNncTdzd05IN3A2VWRsdHJDcHhTd0ZFdmM3ZG91RTJzS3JQRHA4MDdaRzJkRnNsS3h4bVI0V0hESFdmSDBPcHpyQjVLS1dRTnl6WHhUQlhlbHFyV1pFQ0xSeXBOcTdQKzFDeWZnVFNkUTM1ZmRPN00xTW5pU0JUMVYzM0xkaFhvNzMvOXFENWU1VlFJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0t",
    "pciEndpoint": "https://iframe.vietcombank.com.vn",
    "secretKey": "79a96ccb09b127f81a0f48c23ef7c084e5132862a39c643c3964b6bd24e98685",
    "crcKey": "6q93-@u9",
    "uploadRemittanceUrl": "https://uploadgw.vietcombank.com.vn",
    "downloadRemittanceUrl": "https://downloadgw-cde.vietcombank.com.vn",
    "insightEndpoint": "https://vcbinsight.vietcombank.com.vn",
    "storeKey": {
        "HERCU": "vcb.hercu"
    },
    "vdn": {
        "MASS_VI": "5301",
        "MASS_VI_ERROR": "5302",
        "MASS_EN": "5303",
        "VIP_VI": "5304",
        "VIP_EN": "5305"
    },
    "loyaltyRewards": "https://loyalty.vietcombank.com.vn/portal-web/"
}

def get_date() -> tuple:
    """
    Trả về tuple (from_date, to_date) dạng 'dd/mm/yyyy'.
    from_date: 30 ngày trước hôm nay
    to_date: hôm nay
    """
    now = datetime.now(VN_TZ)
    to_date = now.strftime("%d/%m/%Y")
    from_date = (now - timedelta(days=30)).strftime("%d/%m/%Y")
    return from_date, to_date

def gen_keys() -> tuple:
    key = RSA.generate(1024)
    private_key = key.export_key().decode()
    public_key = key.publickey().export_key().decode().replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", "").replace("\n", "")
    return private_key, public_key

def aes_encrypt(data: str, key: str, iv: str) -> bytes:
    ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    return cipher.encrypt(data)

def aes_decrypt(ciphertext: bytes, key: str, iv: str) -> str:
    ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    return cipher.decrypt(ciphertext)

def encrypt_request(data: dict, client_pub_key_str: str, server_pub_key_base64: str) -> dict:
    try:
        m = get_random_bytes(32) 
        O = get_random_bytes(16) 
        f = {
            "clientPubKey": client_pub_key_str,
            **data
        }
        cipher = AES.new(m, AES.MODE_CTR, nonce=b'', initial_value=O)
        plaintext = json.dumps(f).encode("utf-8")
        ciphertext = cipher.encrypt(plaintext)
        encrypted_data = O + ciphertext
        d_base64 = base64.b64encode(encrypted_data).decode()
        server_pub_key_pem = base64.b64decode(server_pub_key_base64).decode()
        rsa_key = RSA.importKey(server_pub_key_pem)
        cipher_rsa = PKCS1_v1_5.new(rsa_key)
        encrypted_key = cipher_rsa.encrypt(base64.b64encode(m))
        k_base64 = base64.b64encode(encrypted_key).decode()
        return {
            "d": d_base64,
            "k": k_base64
        }

    except Exception as e:
        print("Encryption error:", e)
        return {
            "d": "",
            "k": ""
        }
    
def decrypt_response(enc_obj: dict, private_key_pem: str) -> dict:
    k = base64.b64decode(enc_obj["k"])
    d = base64.b64decode(enc_obj["d"])
    rsa_key = RSA.import_key(private_key_pem)
    cipher_rsa = PKCS1_v1_5.new(rsa_key)
    sentinel = Random.new().read(15)
    aes_key_base64 = cipher_rsa.decrypt(k, sentinel)
    aes_key = base64.b64decode(aes_key_base64)
    iv = d[:16]
    data = d[16:]
    decrypted_data = aes_decrypt(data, aes_key, iv)
    return json.loads(decrypted_data.decode())
