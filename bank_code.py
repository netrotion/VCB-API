

class BANK_CODE:
    def __init__(self, comment: str = "This class is used to store bank codes for Vietcombank. "):

        bank_data = open("params.json", "r", encoding="utf-8").read()
        bank_data = eval(bank_data)
        for banks in bank_data:
            shortname = banks["name"].replace(" ", "_").replace("-", "_").replace(".", "_").upper()
            fullname = banks["sub"]
            bankcode = banks["supportChannel"][0]["bankCode"]
            sub_name = banks["sub"].upper()
            if "TP Hồ Chí Minh".upper() in sub_name:
                shortname += "_TPHCM"
            elif "Hà Nội".upper() in sub_name:
                shortname += "_HN"
            setattr(self, shortname, {
                "fullname": fullname,
                "bankcode": bankcode,
                "sub_name": sub_name
            })
        

    def __getattr__(self, item):
        raise AttributeError(f"'BANK_CODE' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise AttributeError(f"Cannot modify existing attribute '{key}'")
        self.__dict__[key] = value
    
    def __delattr__(self, item):
        if item in self.__dict__:
            raise AttributeError(f"Cannot delete attribute '{item}'")
        raise AttributeError(f"'BANK_CODE' object has no attribute '{item}'")
    
    def __repr__(self):
        return f"BANK_CODE({', '.join(f'{k}={v}' for k, v in self.__dict__.items())})"
    


BANK_CODE = BANK_CODE()

#print all attributes of BANK_CODE
def print_bank_codes():
    for attr in dir(BANK_CODE):
        if not attr.startswith("__"):
            print(f"{attr}: {getattr(BANK_CODE, attr)}")


code = """
class BANK_CODE:
    def __init__(self):
{code}

"""
code = code.format(
    code="\n".join(
        [
            f"\tself.{k} = {str(v)}" for k, v in BANK_CODE.__dict__.items() if not k.startswith("__") and not callable(getattr(BANK_CODE, k))
        ]
    )
)
code = code.replace("'", '"')
with open("bank_code.py", "w", encoding="utf-8") as f:
    f.write(code.replace("'", '"'))