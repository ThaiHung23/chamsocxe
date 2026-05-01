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
from controller.dat_lich_controller import DatLichController
from view.customer_main_view import CustomerMainView

def main():
    # Cấu hình CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # main.py
    def start_app(user):
        if user.get('user_type') == 'customer':
            # Mở giao diện khách hàng
            controllers = {
                'khach_hang': KhachHangController(),
                'xe': XeController(),
                'dich_vu': DichVuController(),
                'hoa_don': HoaDonController(),
                'dat_lich': DatLichController(),
            }
            from view.customer_main_view import CustomerMainView
            # Thêm controllers vào tham số
            CustomerMainView(controllers, user)
        else:
            # Mở giao diện admin/nhân viên
            controllers = {
                'khach_hang': KhachHangController(),
                'xe': XeController(),
                'dich_vu': DichVuController(),
                'hoa_don': HoaDonController(),
                'dat_lich': DatLichController(),
                'user': user  # user đã được thêm đúng
            }
            from view.modern_main_view import ModernMainView
            ModernMainView(controllers)
    
    # Hiển thị màn hình đăng nhập
    login = LoginView(start_app)

if __name__ == "__main__":
    main()