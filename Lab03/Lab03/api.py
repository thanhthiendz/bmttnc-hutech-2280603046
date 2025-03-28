from flask import Flask, request, jsonify
import string
from cipher.ecc import ECCCipher
from cipher.rsa import RSACipher
app = Flask(__name__)

# Hàm mã hóa Caesar Cipher
def caesar_encrypt(plain_text, key):
    encrypted_message = []
    for char in plain_text:
        if char.isalpha():
            shift = key % 26
            start = 65 if char.isupper() else 97
            encrypted_message.append(chr((ord(char) - start + shift) % 26 + start))
        else:
            encrypted_message.append(char)
    return ''.join(encrypted_message)

# Hàm giải mã Caesar Cipher
def caesar_decrypt(cipher_text, key):
    decrypted_message = []
    for char in cipher_text:
        if char.isalpha():
            shift = key % 26
            start = 65 if char.isupper() else 97
            decrypted_message.append(chr((ord(char) - start - shift) % 26 + start))
        else:
            decrypted_message.append(char)
    return ''.join(decrypted_message)

# API endpoint để mã hóa
@app.route('/api/caesar/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    plain_text = data.get('plain_text', '')
    key = int(data.get('key', 0))  # Chuyển key thành số
    encrypted_message = caesar_encrypt(plain_text, key)
    return jsonify({"encrypted_message": encrypted_message})

# API endpoint để giải mã
@app.route('/api/caesar/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    cipher_text = data.get('cipher_text', '')
    key = int(data.get('key', 0))  # Chuyển key thành số
    decrypted_message = caesar_decrypt(cipher_text, key)
    return jsonify({"decrypted_message": decrypted_message})
# ECC CIPHER ALGORITHM
ecc_cipher = ECCCipher()

# API để tạo cặp khóa ECC
@app.route('/api/ecc/generate_keys', methods=['GET'])
def ecc_generate_keys():
    ecc_cipher.generate_keys()
    return jsonify({'message': 'Keys generated successfully'})

# API để ký dữ liệu bằng ECC
@app.route('/api/ecc/sign', methods=['POST'])
def ecc_sign_message():
    data = request.json
    message = data.get('message', '')

    if not message:
        return jsonify({'error': 'Message is required'}), 400

    signature = ecc_cipher.sign(message)  # Ký message
    return jsonify({'signature': signature})  # Trả về signature dưới dạng hex

# API để xác minh chữ ký
@app.route('/api/ecc/verify', methods=['POST'])
def ecc_verify_signature():
    data = request.json
    message = data.get('message', '')
    signature_hex = data.get('signature', '')

    if not message or not signature_hex:
        return jsonify({'error': 'Message and signature are required'}), 400

    is_verified = ecc_cipher.verify(message, signature_hex)  # Xác minh chữ ký
    return jsonify({'is_verified': is_verified})
# RSA CIPHER ALGORITHM
rsa_cipher = RSACipher()

@app.route('/api/rsa/generate_keys', methods=['GET'])
def rsa_generate_keys():
    rsa_cipher.generate_keys()
    return jsonify({'message': 'Keys generated successfully'})

@app.route("/api/rsa/encrypt", methods=["POST"])
def rsa_encrypt():
    data = request.json
    message = data['message']
    key_type = data['key_type']
    
    private_key, public_key = rsa_cipher.load_keys()
    
    if key_type == 'public':
        key = public_key
    elif key_type == 'private':
        key = private_key
    else:
        return jsonify({'error': 'Invalid key type'})

    encrypted_message = rsa_cipher.encrypt(message, key)
    encrypted_hex = encrypted_message.hex()
    return jsonify({'encrypted_message': encrypted_hex})

@app.route("/api/rsa/decrypt", methods=["POST"])
def rsa_decrypt():
    data = request.json
    ciphertext_hex = data['ciphertext']
    key_type = data['key_type']

    private_key, public_key = rsa_cipher.load_keys()
    
    if key_type == 'public':
        key = public_key
    elif key_type == 'private':
        key = private_key
    else:
        return jsonify({'error': 'Invalid key type'})

    ciphertext = bytes.fromhex(ciphertext_hex)
    decrypted_message = rsa_cipher.decrypt(ciphertext, key)
    
    return jsonify({'decrypted_message': decrypted_message})

@app.route('/api/rsa/sign', methods=['POST'])
def rsa_sign_message():
    data = request.json
    message = data['message']
    
    private_key, _ = rsa_cipher.load_keys()
    signature = rsa_cipher.sign(message, private_key)
    signature_hex = signature.hex()
    
    return jsonify({'signature': signature_hex})

@app.route('/api/rsa/verify', methods=['POST'])
def rsa_verify_signature():
    data = request.json
    message = data['message']
    signature_hex = data['signature']
    
    public_key, _ = rsa_cipher.load_keys()
    signature = bytes.fromhex(signature_hex)
    
    is_verified = rsa_cipher.verify(message, signature, public_key)
    
    return jsonify({'is_verified': is_verified})
if __name__ == '__main__':
    app.run(debug=True)
