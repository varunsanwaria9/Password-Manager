import base64 

class stringenc:
    def __init__(self):
        self.__key = "desiJr564@we!SCB120Zalatan"

    def encrypted(self,string):
        enc = []
        for i in range(len(string)):
            key_c = self.__key[i % len(self.__key)]
            enc.append(chr( (ord(string[i]) + ord(key_c)) % 256 ))
        return base64.urlsafe_b64encode("".join(enc).encode()).decode()

    def decrypted(self,string):
        dec = []
        string = base64.urlsafe_b64decode(string).decode()
        for i in range(len(string)):
            key_c = self.__key[i % len(self.__key)]
            dec.append(chr((256 + ord(string[i]) - ord(key_c)) % 256))    
        return "".join(dec)


