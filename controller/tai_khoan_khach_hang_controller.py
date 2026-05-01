# controller/tai_khoan_khach_hang_controller.py
from model.tai_khoan_khach_hang_model import TaiKhoanKhachHangModel

class TaiKhoanKhachHangController:
    def __init__(self):
        self.model = TaiKhoanKhachHangModel()
    
    def login(self, username, password):
        try:
            return self.model.login(username, password)
        except Exception as e:
            print(f"Lỗi đăng nhập: {e}")
            return None