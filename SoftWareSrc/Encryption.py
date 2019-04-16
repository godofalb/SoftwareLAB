class Encryption:
    key = ""
    cycle = None
    hashlib = None
    def __init__(self, key:str=""):
        self.key = key
        from itertools import cycle
        self.cycle = cycle
        import hashlib
        self.hashlib = hashlib

    def __generateMd5(self, source:str):
        source_utf8 = source.encode(encoding='utf-8')
        md5 = self.hashlib.md5()
        md5.update(source_utf8)
        string = md5.hexdigest()
        return string

    def __encrypt(self,source:str):
        result = ""
        temp = self.cycle(self.key)
        for ch in source:
            result = result + chr(ord(ch) ^ ord(next(temp)))
        return result
    def EncryptSring(self, source:str):
        md5_str = self.__generateMd5(source)
        new_source = md5_str + source
        # length of md5_str = 32
        source_encry = self.__encrypt(new_source)
        return source_encry.encode(encoding='utf-8')
    def DecryptString(self, byte_stream:str):
        source_encry = byte_stream.decode()
        source = self.__encrypt(source_encry)
        org_md5_str = source[:32]
        org_source = source[32:]
        md5_str = self.__generateMd5(org_source)
        if org_md5_str != md5_str:
            print(org_md5_str)
            print(md5_str)
            return None
        return org_source

    def ViewKey(self):
        return self.key
    def LoadKey(self, key:str):
        self.key = key


if __name__ == '__main__':
    en = Encryption("test")
    print("old key:", en.ViewKey())
    en.LoadKey("litou")
    print("new key:",en.ViewKey())
    byte_stream = en.EncryptSring("apple")
    print("byte-stream length:", len(byte_stream))
    print("encrypt message:", byte_stream)
    print("decrypt message:", en.DecryptString(byte_stream))
