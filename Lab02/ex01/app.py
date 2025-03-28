from flask import Flask, render_template, request
from cipher.caesar import CaesarCipher
from cipher.railfence import RailFenceCipher
from cipher.transposition import TranspositionCipher
from cipher.vigenere import VigenereCipher    
app = Flask(__name__)

# Router cho trang chủ
@app.route("/")
def home():
    return render_template('index.html')

# Router cho mã hóa Caesar
@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/encrypt_caesar", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    Caesar = CaesarCipher()
    
    encrypted_text = Caesar.encrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/decrypt_caesar", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    Caesar = CaesarCipher()
    
    decrypted_text = Caesar.decrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"
# Router cho mã hóa Rail Fence
@app.route("/railfence")
def railfence():
    return render_template('railfence.html')

@app.route("/encrypt_railfence", methods=['POST'])
def railfence_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    RailFence = RailFenceCipher()

    encrypted_text = RailFence.encrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/decrypt_railfence", methods=['POST'])
def railfence_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    RailFence = RailFenceCipher()

    decrypted_text = RailFence.decrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"
# Router cho mã hóa Transposition
@app.route("/transposition")
def transposition():
    return render_template('transposition.html')

@app.route("/encrypt_transposition", methods=['POST'])
def transposition_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    transposition = TranspositionCipher()
    
    encrypted_text = transposition.encrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/decrypt_transposition", methods=['POST'])
def transposition_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    transposition = TranspositionCipher()
    
    decrypted_text = transposition.decrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"
# Router cho mã hóa Vigenère
@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')

@app.route("/encrypt_vigenere", methods=['POST'])
def vigenere_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    vigenere = VigenereCipher()
    
    encrypted_text = vigenere.encrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/decrypt_vigenere", methods=['POST'])
def vigenere_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    vigenere = VigenereCipher()
    
    decrypted_text = vigenere.decrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"
# Hàm main để chạy server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
