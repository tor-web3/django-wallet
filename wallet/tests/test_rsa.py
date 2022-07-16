import base64
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA


class RsaCode:
    rsa_private_key = """-----BEGIN RSA PRIVATE KEY-----
    MIICXAIBAAKBgQDvluFNiF8IrIsddK0OXBAvVBJH11OKvy9er1tRGn9yEJoHCJY3
    EU/xz2LasCK8AwgRIqGJbvDBgRa70c3QT9j+wPqNqqJCSoSEKifnDUk1RgUReJT6
    iqWaJyfM+WM3aHnKl61RZL4NV5qKe4CHMtaH/JtBCC/JzpuFER1P1IhCtQIDAQAB
    AoGAaFYQb68/k4twWbeB1YsKEVJPU7HV08pGWrmKztr3PTk1mnKG2BxV8DwcFJg3
    yCCZ1rx6FFuXxOzudYR8WIctO4wdsEbFky/cEGsfc6JJjiktmZaQ7MvobGNwnoFJ
    QvRxDd+5uD87JE19iBSgUpLVtXbv+pZxSpD70vitnMdSctECQQD66Z5HsuC8DUPu
    OLQHNN4ra5Op179Xlq7LiEFW4GaVgonw24kiLX23c7CK7295Rgxct1fwQKyuU9br
    n2uj8toDAkEA9HJ85BWlm2OfUm6VI3Q99rjlpCnhRyz70+sEtf7if1SpctVxNTkX
    UOnXlpPTohjAHNhzh9fa1hh/ySH9sRMu5wJAa//8uh3br/YBxFsx2lw+OPBQGe4c
    lSXtzPu0LCHg5f/PQhYs28I696jbV6IiGFA3Z/0e4/HiohLCUp9HJMWWYwJACE53
    pfyCUyRwfomZccn6bQ7dZtWxfQyvRgU/dLvDkJYc5/UO0sMs4qf/lnNRhrmWlaRZ
    UK1qF0pf1ULdbw360wJBAObrYopW2kvIlE09j9SEgNtgVsmfZlf85c4EAZrFJP/T
    8nMNKQGo92Gd3HvbjJ+ZBOP1IFt+FDAsXeSLWLAwJrg=
    -----END RSA PRIVATE KEY-----"""

    rsa_public_key = """-----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDvluFNiF8IrIsddK0OXBAvVBJH
    11OKvy9er1tRGn9yEJoHCJY3EU/xz2LasCK8AwgRIqGJbvDBgRa70c3QT9j+wPqN
    qqJCSoSEKifnDUk1RgUReJT6iqWaJyfM+WM3aHnKl61RZL4NV5qKe4CHMtaH/JtB
    CC/JzpuFER1P1IhCtQIDAQAB
    -----END PUBLIC KEY-----
    """

    def encrypt(self, msg):
        msg = msg.encode('utf-8')
        rsakey = RSA.importKey(self.rsa_public_key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(msg))
        return cipher_text

    def decrypt(self, cipher_text):
        rsakey = RSA.importKey(self.rsa_private_key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        random_generator = Random.new().read
        text = cipher.decrypt(base64.b64decode(cipher_text), random_generator)
        return text.decode('utf8')

    def long_encrypt(self, msg):
        msg = msg.encode('utf-8')
        length = len(msg)
        default_length = 117
        # 公钥加密
        pubobj = Cipher_pkcs1_v1_5.new(RSA.importKey(self.rsa_public_key))
        # 长度不用分段
        if length < default_length:
            return base64.b64encode(pubobj.encrypt(msg))
        # 需要分段
        offset = 0
        res = []
        while length - offset > 0:
            if length - offset > default_length:
                res.append(pubobj.encrypt(msg[offset:offset + default_length]))
            else:
                res.append(pubobj.encrypt(msg[offset:]))
            offset += default_length
        byte_data = b''.join(res)
        return base64.b64encode(byte_data)

    def long_decrypt(self, msg):
        msg = base64.b64decode(msg)
        length = len(msg)
        default_length = 128
        # 私钥解密
        priobj = Cipher_pkcs1_v1_5.new(RSA.importKey(self.rsa_private_key))
        # 长度不用分段
        if length <= default_length:
            return priobj.decrypt(msg, b'xyz').decode('utf8')
        # 需要分段
        offset = 0
        res = []
        while length - offset > 0:
            if length - offset > default_length:
                res.append(priobj.decrypt(
                    msg[offset:offset + default_length], b'xyz'))
            else:
                res.append(priobj.decrypt(msg[offset:], b'xyz'))
            offset += default_length

        return b''.join(res).decode('utf8')


# '''13911236661f954d35bf966491b982b021478241908＃android＃Nexus 6＃6.0.1＃WIFI＃Nexus 6＃zh＃CN＃google＃2392_1440＃58好借＃2.3.0＃GMT+08:00＃＃＃adcfb20011000000＃856104k＃＃＃"BSTDATA-15F-5G"＃10.15.1.74＃＃＃1＃＃0＃＃0＃2ce10d59284c091b
message = '''1
'''

test = RsaCode()
res_en = test.long_encrypt(message)
print('res_en', res_en)
res_de = test.decrypt(res_en)
print('res_de', res_de)
