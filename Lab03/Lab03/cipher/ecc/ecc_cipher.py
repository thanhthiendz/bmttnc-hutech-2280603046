import ecdsa
import os

class ECCCipher:
    def __init__(self):
        self.private_key_path = "cipher/ecc/keys/privateKey.pem"
        self.public_key_path = "cipher/ecc/keys/publicKey.pem"
        
        # Tạo thư mục lưu trữ khóa nếu chưa tồn tại
        if not os.path.exists("cipher/ecc/keys"):
            os.makedirs("cipher/ecc/keys")

    def generate_keys(self):
        """Tạo cặp khóa ECC và lưu vào tệp"""
        sk = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
        vk = sk.get_verifying_key()
        
        with open(self.private_key_path, "wb") as p:
            p.write(sk.to_pem())
        with open(self.public_key_path, "wb") as p:
            p.write(vk.to_pem())
        
        return "Keys generated successfully"

    def load_keys(self):
        """Tải khóa từ tệp"""
        with open(self.private_key_path, "rb") as p:
            sk = ecdsa.SigningKey.from_pem(p.read())
        with open(self.public_key_path, "rb") as p:
            vk = ecdsa.VerifyingKey.from_pem(p.read())
        
        return sk, vk

    def sign(self, message):
        """Ký dữ liệu bằng khóa riêng tư"""
        sk, _ = self.load_keys()
        return sk.sign(message.encode('utf-8')).hex()

    def verify(self, message, signature):
        """Xác minh chữ ký bằng khóa công khai"""
        _, vk = self.load_keys()
        try:
            return vk.verify(bytes.fromhex(signature), message.encode('utf-8'))
        except ecdsa.BadSignatureError:
            return False