import json

class Login():

    def __init__(self):
        self.LOGIN_PATH = './subsections/login/data/accounts.json'

    def getAccounts(self) -> list: 
        with open(self.LOGIN_PATH, 'r') as a: return json.loads(a.read())

    def writeAccounts(self, accounts: list) -> None:
        with open(self.LOGIN_PATH, 'w') as a: a.write(json.dumps(accounts))

    def check(self, username: str, password: str) -> bool:
        accounts = self.getAccounts()
        for i in accounts:
            if i["username"] == username and i["password"] == password:
                return True
            elif i["username"] == username and not i["password"] == password:
                return False
        return False

    def getByID(self, id):
        accounts = self.getAccounts()
        for i in accounts:
            if i["id"] == id:
                return i

    def getID(self, username: str) -> int:
        accounts = self.getAccounts()
        for i in accounts:
            if i["username"] == username:
                return i["id"]

    def checkPermission(self, username: str) -> str:
        accounts = self.getAccounts()
        for i in accounts:
            if i["username"] == username:
                return i["permission"]