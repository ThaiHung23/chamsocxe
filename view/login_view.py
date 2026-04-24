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
        self.username_entry.insert(0, "admin")  # Thêm giá trị mặc định để test
        
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
        self.password_entry.insert(0, "123456")  # Thêm giá trị mặc định để test
        
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
        """Xử lý đăng nhập"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        print(f"Đang đăng nhập với username: {username}")
        print(f"Mật khẩu nhập: {password}")
        
        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu")
            return
        
        # Hash mật khẩu
        hashed_password = Database.hash_password(password)
        print(f"Mật khẩu đã hash: {hashed_password}")
        
        # Kiểm tra đăng nhập
        query = "SELECT * FROM nguoi_dung WHERE username = %s AND password = %s AND trang_thai = 1"
        user = self.db.fetch_one(query, (username, hashed_password))
        
        if user:
            print(f"Đăng nhập thành công: {user['ho_ten']}")
            # messagebox.showinfo("Thành công", f"Chào mừng {user['ho_ten']}!")
            self.root.destroy()
            self.on_login_success(user)
        else:
            # Debug: Kiểm tra xem user có tồn tại không
            check_user = self.db.fetch_one("SELECT * FROM nguoi_dung WHERE username = %s", (username,))
            if check_user:
                print(f"Tìm thấy user nhưng sai mật khẩu. Hash trong DB: {check_user['password']}")
                print(f"Hash nhập vào: {hashed_password}")
            else:
                print(f"Không tìm thấy user: {username}")
            
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng")