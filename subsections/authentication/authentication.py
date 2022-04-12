import json, time, random

class Authentication():

    def __init__(self, expTime: int = 60, encryptionLength: int = 30):
        
        self.ENCRYPTION_LENGTH = encryptionLength
        self.EXPIRATION_TIME = expTime

        self.cookiePath = './subsections/authentication/data/cookies.json'

    def getCookies(self) -> list:
        with open(self.cookiePath, 'r') as a:
            return json.loads(a.read())

    def writeCookies(self, data: list) -> None:
        with open(self.cookiePath, 'w') as a:
            a.write(json.dumps(data, indent=2, sort_keys=True))

    def deleteCookie(self, cookie: str) -> None:
        cookies = self.getCookies()
        for i in cookies:
            if i["cookie"] == cookie:
                cookies.pop(cookies.index(i))
        self.writeCookies(cookies)
                
    def checkCookie(self, cookie: str) -> bool:
        cookies = self.getCookies()
        for i in cookies:
            if i["cookie"] == cookie and i["expiration"] > time.time():
                i["expiration"] = time.time() + self.EXPIRATION_TIME
                return True
            elif i["cookie"] == cookie and i["expiration"] < time.time():
                self.deleteCookie(cookie)
                return False
    
    def getRandomString(self, length: int) -> str:
        returnStr = ""
        exludedChars = ['\\']
        i1 = 0
        while i1 < length:
            a = random.randint(45, 125)
            for i in range(len(exludedChars)):
                if a == ord(exludedChars[i]):
                    a = ord(self.getRandomString(1))
            returnStr += chr(a)
            i1 += 1
        return returnStr
    
    def getCookie(self, cookie: str):
        a = self.getCookies()
        for i in a:
            if i["cookie"] == cookie:
                return i

    def addCookie(self, cookie: str, accountId: int) -> None:
        a = self.getCookies()
        a.append({ "cookie": cookie, "expiration": time.time() + self.EXPIRATION_TIME, "accountId": accountId})
        self.writeCookies(a)