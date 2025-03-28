import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.ecc import Ui_MainWindow  # Import giao diện từ Qt Designer
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối sự kiện button với hàm API
        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        """Gọi API tạo cặp khóa ECC"""
        url = "http://127.0.0.1:5000/api/ecc/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.show_message("Success", data["message"], QMessageBox.Information)
            else:
                self.show_message("Error", "Failed to generate keys", QMessageBox.Warning)
        except requests.exceptions.RequestException as e:
            self.show_message("Error", f"Request failed: {e}", QMessageBox.Critical)

    def call_api_sign(self):
        """Gọi API ký dữ liệu"""
        url = "http://127.0.0.1:5000/api/ecc/sign"
        payload = {"message": self.ui.txt_info.toPlainText()}

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_sign.setPlainText(data["signature"])
                self.show_message("Success", "Signed Successfully", QMessageBox.Information)
            else:
                self.show_message("Error", "Signing failed", QMessageBox.Warning)
        except requests.exceptions.RequestException as e:
            self.show_message("Error", f"Request failed: {e}", QMessageBox.Critical)

    def call_api_verify(self):
        """Gọi API xác minh chữ ký"""
        url = "http://127.0.0.1:5000/api/ecc/verify"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
            "signature": self.ui.txt_sign.toPlainText()
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if data["is_verified"]:
                    self.show_message("Success", "Verified Successfully", QMessageBox.Information)
                else:
                    self.show_message("Failed", "Verification Failed", QMessageBox.Warning)
            else:
                self.show_message("Error", "Verification request failed", QMessageBox.Warning)
        except requests.exceptions.RequestException as e:
            self.show_message("Error", f"Request failed: {e}", QMessageBox.Critical)

    def show_message(self, title, text, icon):
        """Hiển thị thông báo popup"""
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())