import customtkinter as ctk
from tkinter import messagebox
from model.database import Database

class LoginView:
    def __init__(self, on_login_success):
        self.on_login_success = on_login_success
        self.db = Database()
        
        # Cấu hình cửa sổ login
        self.root = ctk.CTk()
        self.root.title("Đăng nhập - AutoCare Pro")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        
        # Center window
        self.root.eval('tk::PlaceWindow . center')
        
        self.setup_ui()
        self.root.mainloop()
    
    def setup_ui(self):
        """Thiết kế giao diện đăng nhập"""
        
        # Main frame
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Logo
        logo_label = ctk.CTkLabel(
            main_frame,
            text="🚗 AutoCare Pro",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#4a9eff"
        )
        logo_label.pack(pady=(0, 10))
        
        slogan_label = ctk.CTkLabel(
            main_frame,
            text="Phần mềm quản lý dịch vụ chăm sóc xe ô tô",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        slogan_label.pack(pady=(0, 40))
        
        # Form đăng nhập
        form_frame = ctk.CTkFrame(main_frame, fg_color="#1f1f1f", corner_radius=15)
        form_frame.pack(fill="both", expand=True)
        
        title_label = ctk.CTkLabel(
            form_frame,
            text="ĐĂNG NHẬP",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Username
        username_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        username_frame.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkLabel(username_frame, text="Tên đăng nhập", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.username_entry = ctk.CTkEntry(
            username_frame,
            placeholder_text="Nhập tên đăng nhập",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.username_entry.pack(fill="x", pady=(5, 0))
        # self.username_entry.insert(0, "admin")  # Thêm giá trị mặc định để test
        
        # Password
        password_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        password_frame.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkLabel(password_frame, text="Mật khẩu", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="Nhập mật khẩu",
            show="•",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.password_entry.pack(fill="x", pady=(5, 0))
        # self.password_entry.insert(0, "123456")  # Thêm giá trị mặc định để test
        
        # Bind Enter key
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # Login button
        self.login_btn = ctk.CTkButton(
            form_frame,
            text="ĐĂNG NHẬP",
            command=self.login,
            fg_color="#4a9eff",
            hover_color="#357ae8",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        self.login_btn.pack(fill="x", padx=30, pady=20)
        
        # Thông tin demo
        demo_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        demo_frame.pack(fill="x", padx=30, pady=10)
        
        demo_label = ctk.CTkLabel(
            demo_frame,
            text="📝 Tài khoản demo:\nAdmin: admin / 123456\nNhân viên: nhanvien1 / 123456",
            font=ctk.CTkFont(size=11),
            text_color="#888888",
            justify="center"
        )
        demo_label.pack()
        
        # Footer
        footer_label = ctk.CTkLabel(
            main_frame,
            text="© 2024 AutoCare Pro - Bản quyền thuộc về AutoCare",
            font=ctk.CTkFont(size=10),
            text_color="#555555"
        )
        footer_label.pack(side="bottom", pady=20)
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu")
            return
        
        hashed_password = Database.hash_password(password)
        print(f"DEBUG: Username: {username}")
        print(f"DEBUG: Hashed password: {hashed_password}")
        
        # 1. Kiểm tra đăng nhập admin/nhân viên
        query_staff = """
            SELECT id, username, ho_ten, vai_tro, trang_thai 
            FROM nguoi_dung 
            WHERE username = %s AND password = %s AND trang_thai = 1
        """
        staff = self.db.fetch_one(query_staff, (username, hashed_password))
        print(f"DEBUG: Staff query result: {staff}")
        
        if staff:
            # Tạo user object cho staff
            user = {
                'id': staff['id'],
                'username': staff['username'],
                'ho_ten': staff['ho_ten'],
                'vai_tro': staff['vai_tro'],
                'user_type': 'staff'  # Quan trọng: đánh dấu là staff
            }
            print(f"DEBUG: Staff login success: {user}")
            self.root.destroy()
            self.on_login_success(user)
            return
        
        # 2. Kiểm tra đăng nhập khách hàng
        query_customer = """
            SELECT 
                tk.id as tk_id,
                tk.username,
                tk.id_khach_hang,
                kh.id as kh_id,
                kh.ma_kh,
                kh.ho_ten,
                kh.so_dien_thoai,
                kh.email,
                kh.dia_chi,
                kh.ngay_tao
            FROM tai_khoan_khach_hang tk
            INNER JOIN khach_hang kh ON tk.id_khach_hang = kh.id
            WHERE tk.username = %s AND tk.password = %s AND tk.trang_thai = 1
        """
        customer_data = self.db.fetch_one(query_customer, (username, hashed_password))
        print(f"DEBUG: Customer query result: {customer_data}")
        
        if customer_data:
            # Tạo user object cho customer
            user = {
                'id': customer_data['kh_id'],  # ID khách hàng
                'tk_id': customer_data['tk_id'],
                'username': customer_data['username'],
                'ho_ten': customer_data['ho_ten'],
                'so_dien_thoai': customer_data['so_dien_thoai'],
                'email': customer_data.get('email', ''),
                'dia_chi': customer_data.get('dia_chi', ''),
                'ma_kh': customer_data.get('ma_kh', ''),
                'user_type': 'customer'  # Quan trọng: đánh dấu là customer
            }
            print(f"DEBUG: Customer login success: {user}")
            print(f"DEBUG: user_type = {user['user_type']}")
            self.root.destroy()
            self.on_login_success(user)
            return
        
        print("DEBUG: Login failed - No matching user found")
        messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng")