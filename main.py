import sys
import os
import customtkinter as ctk

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controller.khach_hang_controller import KhachHangController
from controller.xe_controller import XeController
from controller.dich_vu_controller import DichVuController
from controller.hoa_don_controller import HoaDonController
from view.login_view import LoginView
from view.modern_main_view import ModernMainView

def main():
    # Cấu hình CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    def start_app(user):
        """Khởi động ứng dụng chính sau khi đăng nhập thành công"""
        # Khởi tạo controllers
        controllers = {
            'khach_hang': KhachHangController(),
            'xe': XeController(),
            'dich_vu': DichVuController(),
            'hoa_don': HoaDonController(),
            'user': user
        }
        
        # Khởi tạo view chính
        app = ModernMainView(controllers)
    
    # Hiển thị màn hình đăng nhập
    login = LoginView(start_app)

if __name__ == "__main__":
    main()