# view/customer_main_view.py
import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from PIL import Image
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CustomerMainView:
    def __init__(self, controllers, customer_info):
        self.controllers = controllers
        self.customer_info = customer_info
        self.current_frame = None
        
        self.root = ctk.CTk()
        self.root.title(f"AutoCare Pro - Khách hàng: {customer_info['ho_ten']}")
        self.root.geometry("1300x750")
        self.center_window()
        
        self.setup_ui()
        self.show_dashboard()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def center_window(self):
        self.root.update_idletasks()
        width, height = 1300, 750
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        # Main container
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        # Sidebar
        self.setup_sidebar()
        
        # Content area
        self.content_area = ctk.CTkFrame(self.main_container, fg_color="#2b2b2b", corner_radius=0)
        self.content_area.pack(side="right", fill="both", expand=True)
        
        # Header
        self.setup_header()
        
        # Main content frame
        self.content_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self.main_container, width=260, corner_radius=0, fg_color="#1a1a2e")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Logo
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=30)
        
        ctk.CTkLabel(logo_frame, text="🚗", font=ctk.CTkFont(size=48), text_color="#4a9eff").pack()
        ctk.CTkLabel(logo_frame, text="AutoCare Pro", font=ctk.CTkFont(size=20, weight="bold"), text_color="#4a9eff").pack(pady=(5, 0))
        ctk.CTkLabel(logo_frame, text="Khách hàng", font=ctk.CTkFont(size=12), text_color="#888888").pack()
        
        ctk.CTkFrame(self.sidebar, height=2, fg_color="#2a2a3e").pack(fill="x", padx=20, pady=15)
        
        # Menu items
        menu_items = [
            ("📊 Dashboard", self.show_dashboard),
            ("🚘 Xe của tôi", self.show_my_cars),
            ("📅 Đặt lịch", self.show_booking),
            ("📋 Lịch sử dịch vụ", self.show_history),
            ("👤 Thông tin cá nhân", self.show_profile),
            ("🔑 Đổi mật khẩu", self.show_change_password),
        ]
        
        self.menu_buttons = {}
        for text, command in menu_items:
            btn = ctk.CTkButton(
                self.sidebar, text=text, command=command,
                fg_color="transparent", text_color="#e0e0e0", hover_color="#2a2a3e",
                anchor="w", height=45, font=ctk.CTkFont(size=14), corner_radius=8
            )
            btn.pack(fill="x", padx=20, pady=5)
            self.menu_buttons[text] = btn
        
        # User info
        user_frame = ctk.CTkFrame(self.sidebar, fg_color="#15152a", corner_radius=10)
        user_frame.pack(side="bottom", fill="x", padx=15, pady=20)
        
        ctk.CTkLabel(user_frame, text="👤", font=ctk.CTkFont(size=40)).pack(pady=10)
        ctk.CTkLabel(user_frame, text=self.customer_info['ho_ten'], 
                    font=ctk.CTkFont(size=14, weight="bold"), text_color="#ffffff").pack()
        ctk.CTkLabel(user_frame, text=self.customer_info['so_dien_thoai'], 
                    font=ctk.CTkFont(size=11), text_color="#888888").pack()
        
        ctk.CTkButton(user_frame, text="Đăng xuất", command=self.logout,
                     fg_color="#d32f2f", hover_color="#b71c1c", height=35,
                     font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 15), padx=20, fill="x")
    
    def setup_header(self):
        self.header = ctk.CTkFrame(self.content_area, height=60, fg_color="#1a1a2e", corner_radius=0)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)
        
        self.header_title = ctk.CTkLabel(
            self.header, text="Dashboard",
            font=ctk.CTkFont(size=24, weight="bold"), text_color="#4a9eff"
        )
        self.header_title.place(x=30, y=15)
        
        # Time
        time_frame = ctk.CTkFrame(self.header, fg_color="#2a2a3e", corner_radius=10)
        time_frame.place(x=1050, y=12)
        
        self.time_label = ctk.CTkLabel(
            time_frame, text="", font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#4a9eff", padx=15, pady=8
        )
        self.time_label.pack()
        self.update_time()
    
    def update_time(self):
        if not self.root.winfo_exists():
            return
        self.time_label.configure(text=datetime.now().strftime("%H:%M:%S • %d/%m/%Y"))
        self.root.after(1000, self.update_time)
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def highlight_menu(self, menu_text):
        for text, btn in self.menu_buttons.items():
            if text == menu_text:
                btn.configure(fg_color="#2a2a3e", text_color="#4a9eff")
            else:
                btn.configure(fg_color="transparent", text_color="#e0e0e0")
    
    # ==================== DASHBOARD ====================
    def show_dashboard(self):
        self.clear_content()
        self.header_title.configure(text="Dashboard")
        self.highlight_menu("📊 Dashboard")
        
        # Thống kê nhanh
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=20)
        
        # Lấy dữ liệu thống kê - THÊM XỬ LÝ LỖI
        try:
            cars = self.controllers['xe'].get_by_khach_hang(self.customer_info['id'])
        except:
            cars = []
        
        try:
            bookings = self.controllers['dat_lich'].get_by_khach_hang(self.customer_info['id'])
        except:
            bookings = []
        
        try:
            invoices = self.controllers['hoa_don'].get_by_khach_hang(self.customer_info['id'])
        except:
            invoices = []
        
        stats = [
            ("🚘", "Xe đang quản lý", str(len(cars)), "#4a9eff"),
            ("📅", "Lịch hẹn", str(len(bookings)), "#ff9800"),
            ("📄", "Hóa đơn", str(len(invoices)), "#00c853"),
        ]
        
        for i, (icon, title, value, color) in enumerate(stats):
            card = ctk.CTkFrame(stats_frame, fg_color="#1a1a2e", corner_radius=15, height=120)
            card.pack(side="left", padx=10, fill="x", expand=True)
            
            icon_frame = ctk.CTkFrame(card, fg_color=color, corner_radius=12, width=50, height=50)
            icon_frame.pack_propagate(False)
            icon_frame.place(x=20, y=20)
            ctk.CTkLabel(icon_frame, text=icon, font=ctk.CTkFont(size=28), text_color="white").pack(expand=True)
            
            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=12), text_color="#888888").place(x=85, y=30)
            ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=28, weight="bold"), text_color=color).place(x=85, y=60)
        
        # Lịch hẹn sắp tới
        upcoming_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a2e", corner_radius=15)
        upcoming_frame.pack(fill="both", expand=True, pady=20)
        
        ctk.CTkLabel(upcoming_frame, text="📅 Lịch hẹn sắp tới", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15, padx=20, anchor="w")
        
        # Tạo treeview
        tree_frame = ctk.CTkFrame(upcoming_frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        columns = ("Ngày hẹn", "Giờ hẹn", "Dịch vụ", "Trạng thái")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor="center")
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Lấy dữ liệu lịch hẹn sắp tới
        if bookings:
            upcoming_bookings = [b for b in bookings if b.get('trang_thai') in ['cho_xac_nhan', 'da_xac_nhan', 'dang_thuc_hien']]
            
            for b in upcoming_bookings:
                status_text = {
                    'cho_xac_nhan': '⏳ Chờ xác nhận',
                    'da_xac_nhan': '✅ Đã xác nhận',
                    'dang_thuc_hien': '🔧 Đang thực hiện',
                    'hoan_thanh': '🏁 Hoàn thành',
                    'da_huy': '❌ Đã hủy'
                }.get(b.get('trang_thai', ''), b.get('trang_thai', ''))
                
                tree.insert("", "end", values=(
                    b.get('ngay_hen', ''),
                    str(b.get('gio_hen', ''))[:5] if b.get('gio_hen') else '',
                    b.get('ten_dich_vu', ''),
                    status_text
                ))
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    # ==================== XE CỦA TÔI ====================
    def show_my_cars(self):
        self.clear_content()
        self.header_title.configure(text="Xe của tôi")
        self.highlight_menu("🚘 Xe của tôi")
        
        cars = self.controllers['xe'].get_by_khach_hang(self.customer_info['id'])
        
        # Nút thêm xe
        add_btn = ctk.CTkButton(
            self.content_frame, text="➕ Thêm xe mới", command=self.show_add_car_form,
            fg_color="#4a9eff", height=40, width=150
        )
        add_btn.pack(anchor="e", pady=10)
        
        # Danh sách xe
        if not cars:
            empty_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a2e", corner_radius=15)
            empty_frame.pack(fill="both", expand=True)
            
            ctk.CTkLabel(empty_frame, text="🚗", font=ctk.CTkFont(size=64)).pack(pady=50)
            ctk.CTkLabel(empty_frame, text="Bạn chưa có xe nào", font=ctk.CTkFont(size=18), text_color="#888888").pack()
            ctk.CTkLabel(empty_frame, text="Hãy thêm xe mới để sử dụng dịch vụ", font=ctk.CTkFont(size=14), text_color="#666666").pack()
            return
        
        # Hiển thị danh sách xe dạng card
        cars_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        cars_frame.pack(fill="both", expand=True)
        
        for i, car in enumerate(cars):
            card = ctk.CTkFrame(cars_frame, fg_color="#1a1a2e", corner_radius=15)
            card.pack(fill="x", pady=10, padx=10)
            
            # Icon
            ctk.CTkLabel(card, text="🚘", font=ctk.CTkFont(size=40)).pack(side="left", padx=20, pady=15)
            
            # Thông tin
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
            
            ctk.CTkLabel(info_frame, text=f"{car['hieu_xe']} {car.get('model', '')}", 
                        font=ctk.CTkFont(size=16, weight="bold"), text_color="#4a9eff").pack(anchor="w")
            ctk.CTkLabel(info_frame, text=f"Biển số: {car['bien_so']}", 
                        font=ctk.CTkFont(size=13)).pack(anchor="w", pady=2)
            ctk.CTkLabel(info_frame, text=f"Màu sắc: {car.get('mau_sac', 'Chưa cập nhật')} | Năm SX: {car.get('nam_sx', 'Chưa cập nhật')}", 
                        font=ctk.CTkFont(size=12), text_color="#888888").pack(anchor="w")
            
            # Nút thao tác
            btn_frame = ctk.CTkFrame(card, fg_color="transparent")
            btn_frame.pack(side="right", padx=20)
            
            ctk.CTkButton(btn_frame, text="✏️ Sửa", command=lambda c=car: self.show_edit_car_form(c),
                         fg_color="#ff9800", width=80, height=35).pack(side="left", padx=5)
            ctk.CTkButton(btn_frame, text="🗑️ Xóa", command=lambda cid=car['id']: self.delete_car(cid),
                         fg_color="#d32f2f", width=80, height=35).pack(side="left", padx=5)
            ctk.CTkButton(btn_frame, text="📅 Đặt lịch", command=lambda c=car: self.show_booking_with_car(c),
                         fg_color="#00c853", width=100, height=35).pack(side="left", padx=5)
    
    def show_add_car_form(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Thêm xe mới")
        dialog.geometry("500x550")
        dialog.grab_set()
        
        main_frame = ctk.CTkFrame(dialog, fg_color="transparent", padx=30, pady=30)
        main_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(main_frame, text="THÊM XE MỚI", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        entries = {}
        fields = [
            ("Biển số *", "bien_so"),
            ("Hiệu xe *", "hieu_xe"),
            ("Model", "model"),
            ("Màu sắc", "mau_sac"),
            ("Năm sản xuất", "nam_sx"),
        ]
        
        for label, key in fields:
            frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            frame.pack(fill="x", pady=10)
            
            ctk.CTkLabel(frame, text=label, width=120, anchor="w").pack(side="left")
            entry = ctk.CTkEntry(frame, width=250)
            entry.pack(side="right")
            entries[key] = entry
        
        def save():
            data = {k: v.get().strip() for k, v in entries.items()}
            
            if not data['bien_so'] or not data['hieu_xe']:
                messagebox.showerror("Lỗi", "Vui lòng nhập biển số và hiệu xe")
                return
            
            try:
                nam_sx = int(data['nam_sx']) if data['nam_sx'] else None
            except ValueError:
                nam_sx = None
            
            result = self.controllers['xe'].add(
                data['bien_so'], data['hieu_xe'], data['model'],
                data['mau_sac'], nam_sx, self.customer_info['id']
            )
            
            if result:
                messagebox.showinfo("Thành công", "Thêm xe thành công")
                dialog.destroy()
                self.show_my_cars()
            else:
                messagebox.showerror("Lỗi", "Thêm xe thất bại. Biển số có thể đã tồn tại")
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=30)
        
        ctk.CTkButton(btn_frame, text="Lưu", command=save, fg_color="#00c853", width=120, height=40).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Hủy", command=dialog.destroy, fg_color="#757575", width=120, height=40).pack(side="left", padx=10)
    
    def show_edit_car_form(self, car):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Sửa thông tin xe")
        dialog.geometry("500x550")
        dialog.grab_set()
        
        main_frame = ctk.CTkFrame(dialog, fg_color="transparent", padx=30, pady=30)
        main_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(main_frame, text="SỬA THÔNG TIN XE", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        entries = {}
        fields = [
            ("Biển số *", "bien_so", car['bien_so']),
            ("Hiệu xe *", "hieu_xe", car['hieu_xe']),
            ("Model", "model", car.get('model', '')),
            ("Màu sắc", "mau_sac", car.get('mau_sac', '')),
            ("Năm sản xuất", "nam_sx", str(car.get('nam_sx', '')) if car.get('nam_sx') else ''),
        ]
        
        for label, key, value in fields:
            frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            frame.pack(fill="x", pady=10)
            
            ctk.CTkLabel(frame, text=label, width=120, anchor="w").pack(side="left")
            entry = ctk.CTkEntry(frame, width=250)
            entry.insert(0, value)
            entry.pack(side="right")
            entries[key] = entry
        
        def save():
            data = {k: v.get().strip() for k, v in entries.items()}
            
            if not data['bien_so'] or not data['hieu_xe']:
                messagebox.showerror("Lỗi", "Vui lòng nhập biển số và hiệu xe")
                return
            
            try:
                nam_sx = int(data['nam_sx']) if data['nam_sx'] else None
            except ValueError:
                nam_sx = None
            
            result = self.controllers['xe'].update(
                car['id'], data['bien_so'], data['hieu_xe'], data['model'],
                data['mau_sac'], nam_sx, self.customer_info['id']
            )
            
            if result:
                messagebox.showinfo("Thành công", "Cập nhật xe thành công")
                dialog.destroy()
                self.show_my_cars()
            else:
                messagebox.showerror("Lỗi", "Cập nhật thất bại")
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=30)
        
        ctk.CTkButton(btn_frame, text="Lưu", command=save, fg_color="#00c853", width=120, height=40).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Hủy", command=dialog.destroy, fg_color="#757575", width=120, height=40).pack(side="left", padx=10)
    
    def delete_car(self, car_id):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa xe này?"):
            if self.controllers['xe'].delete(car_id):
                messagebox.showinfo("Thành công", "Xóa xe thành công")
                self.show_my_cars()
            else:
                messagebox.showerror("Lỗi", "Xóa xe thất bại")
    
    # ==================== ĐẶT LỊCH ====================
    def show_booking(self):
        self.clear_content()
        self.header_title.configure(text="Đặt lịch dịch vụ")
        self.highlight_menu("📅 Đặt lịch")
        
        # Form đặt lịch
        form_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a2e", corner_radius=15)
        form_frame.pack(fill="x", pady=20, padx=20)
        
        ctk.CTkLabel(form_frame, text="📅 ĐẶT LỊCH DỊCH VỤ MỚI", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        # Chọn xe
        cars = self.controllers['xe'].get_by_khach_hang(self.customer_info['id'])
        car_options = [f"{c['id']} - {c['bien_so']} ({c['hieu_xe']})" for c in cars] if cars else ["Chưa có xe"]
        
        row_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        row_frame.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(row_frame, text="Chọn xe:", width=120, anchor="w").pack(side="left")
        car_var = ctk.StringVar(value=car_options[0] if car_options else "Chưa có xe")
        car_combo = ctk.CTkComboBox(row_frame, values=car_options, variable=car_var, width=250)
        car_combo.pack(side="left", padx=10)
        
        # Chọn dịch vụ
        row_frame2 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row_frame2.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(row_frame2, text="Chọn dịch vụ:", width=120, anchor="w").pack(side="left")
        services = self.controllers['dich_vu'].get_all()
        service_options = [f"{s['id']} - {s['ten_dich_vu']} ({s['don_gia']:,.0f}đ)" for s in services]
        service_var = ctk.StringVar(value=service_options[0] if service_options else "")
        service_combo = ctk.CTkComboBox(row_frame2, values=service_options, variable=service_var, width=250)
        service_combo.pack(side="left", padx=10)
        
        # Số lượng
        row_frame3 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row_frame3.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(row_frame3, text="Số lượng:", width=120, anchor="w").pack(side="left")
        sl_entry = ctk.CTkEntry(row_frame3, width=100)
        sl_entry.insert(0, "1")
        sl_entry.pack(side="left", padx=10)
        
        # Ngày hẹn
        row_frame4 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row_frame4.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(row_frame4, text="Ngày hẹn:", width=120, anchor="w").pack(side="left")
        ngay_entry = ctk.CTkEntry(row_frame4, width=150, placeholder_text="YYYY-MM-DD")
        ngay_entry.pack(side="left", padx=10)
        ngay_entry.insert(0, (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))
        
        # Giờ hẹn
        gio_options = [f"{h:02d}:{m:02d}" for h in range(7, 19) for m in (0, 30)]
        row_frame5 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row_frame5.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(row_frame5, text="Giờ hẹn:", width=120, anchor="w").pack(side="left")
        gio_var = ctk.StringVar(value="08:00")
        gio_combo = ctk.CTkComboBox(row_frame5, values=gio_options, variable=gio_var, width=150)
        gio_combo.pack(side="left", padx=10)
        
        # Ghi chú
        row_frame6 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row_frame6.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(row_frame6, text="Ghi chú:", width=120, anchor="w").pack(side="left")
        ghichu_entry = ctk.CTkEntry(row_frame6, width=300)
        ghichu_entry.pack(side="left", padx=10)
        
        def submit_booking():
            if not cars:
                messagebox.showerror("Lỗi", "Vui lòng thêm xe trước khi đặt lịch")
                return
            
            car_val = car_var.get()
            if car_val == "Chưa có xe" or not car_val:
                messagebox.showerror("Lỗi", "Vui lòng chọn xe")
                return
            
            car_id = int(car_val.split(' - ')[0])
            
            service_val = service_var.get()
            if not service_val:
                messagebox.showerror("Lỗi", "Vui lòng chọn dịch vụ")
                return
            
            service_id = int(service_val.split(' - ')[0])
            
            try:
                so_luong = int(sl_entry.get())
                if so_luong <= 0:
                    so_luong = 1
            except ValueError:
                so_luong = 1
            
            ngay = ngay_entry.get().strip()
            gio = gio_var.get().strip()
            ghichu = ghichu_entry.get().strip()
            
            if not ngay:
                messagebox.showerror("Lỗi", "Vui lòng nhập ngày hẹn")
                return
            
            # Tạo danh sách dịch vụ
            danh_sach_dv = [{'id_dich_vu': service_id, 'so_luong': so_luong, 'ghi_chu': ''}]
            
            result, msg = self.controllers['dat_lich'].add(
                self.customer_info['id'], car_id, ngay, gio, ghichu, danh_sach_dv
            )
            
            if result:
                messagebox.showinfo("Thành công", msg)
                # Reset form
                sl_entry.delete(0, 'end')
                sl_entry.insert(0, "1")
                ngay_entry.delete(0, 'end')
                ngay_entry.insert(0, (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))
                ghichu_entry.delete(0, 'end')
            else:
                messagebox.showerror("Lỗi", msg)
        
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(pady=30)
        
        ctk.CTkButton(btn_frame, text="📅 Đặt lịch ngay", command=submit_booking,
                     fg_color="#00c853", height=45, width=200, font=ctk.CTkFont(size=14, weight="bold")).pack()
    
    def show_booking_with_car(self, car):
        self.show_booking()
        # Có thể auto chọn xe ở đây
    
    # ==================== LỊCH SỬ DỊCH VỤ ====================
    def show_history(self):
        self.clear_content()
        self.header_title.configure(text="Lịch sử dịch vụ")
        self.highlight_menu("📋 Lịch sử dịch vụ")
        
        # Lấy lịch sử
        try:
            bookings = self.controllers['dat_lich'].get_by_khach_hang(self.customer_info['id'])
        except:
            bookings = []
        
        if not bookings or len(bookings) == 0:
            empty_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a2e", corner_radius=15)
            empty_frame.pack(fill="both", expand=True)
            
            ctk.CTkLabel(empty_frame, text="📋", font=ctk.CTkFont(size=64)).pack(pady=50)
            ctk.CTkLabel(empty_frame, text="Chưa có lịch sử dịch vụ", font=ctk.CTkFont(size=18), text_color="#888888").pack()
            ctk.CTkLabel(empty_frame, text="Hãy đặt lịch dịch vụ đầu tiên", font=ctk.CTkFont(size=14), text_color="#666666").pack()
            return
        
        # Hiển thị bảng
        table_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a2e", corner_radius=15)
        table_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(table_frame, text="📋 LỊCH SỬ ĐẶT LỊCH", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)
        
        tree_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        columns = ("Mã lịch", "Xe", "Ngày hẹn", "Giờ hẹn", "Dịch vụ", "Trạng thái", "Ghi chú")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        col_widths = [100, 120, 110, 80, 200, 130, 150]
        for col, width in zip(columns, col_widths):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="center")
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        for b in bookings:
            status_text = {
                'cho_xac_nhan': '⏳ Chờ xác nhận',
                'da_xac_nhan': '✅ Đã xác nhận',
                'dang_thuc_hien': '🔧 Đang thực hiện',
                'hoan_thanh': '🏁 Hoàn thành',
                'da_huy': '❌ Đã hủy'
            }.get(b.get('trang_thai', ''), b.get('trang_thai', ''))
            
            tree.insert("", "end", values=(
                b.get('ma_lich', ''),
                b.get('bien_so_xe', ''),
                b.get('ngay_hen', ''),
                str(b.get('gio_hen', ''))[:5] if b.get('gio_hen') else '',
                b.get('ten_dich_vu', ''),
                status_text,
                (b.get('ghi_chu', '')[:50] + ('...' if len(b.get('ghi_chu', '')) > 50 else '')) if b.get('ghi_chu') else ''
            ))
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    # ==================== THÔNG TIN CÁ NHÂN ====================
    def show_profile(self):
        self.clear_content()
        self.header_title.configure(text="Thông tin cá nhân")
        self.highlight_menu("👤 Thông tin cá nhân")
        
        main_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a2e", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=50, pady=30)
        
        ctk.CTkLabel(main_frame, text="👤 THÔNG TIN CÁ NHÂN", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(pady=30)
        
        entries = {}
        fields = [
            ("Họ tên *", "ho_ten", self.customer_info['ho_ten']),
            ("Số điện thoại *", "so_dien_thoai", self.customer_info['so_dien_thoai']),
            ("Email", "email", self.customer_info.get('email', '')),
            ("Địa chỉ", "dia_chi", self.customer_info.get('dia_chi', '')),
        ]
        
        for label, key, value in fields:
            row = ctk.CTkFrame(main_frame, fg_color="transparent")
            row.pack(fill="x", padx=80, pady=10)
            
            ctk.CTkLabel(row, text=label, width=120, anchor="w", font=ctk.CTkFont(size=14)).pack(side="left")
            entry = ctk.CTkEntry(row, width=300, height=40)
            entry.insert(0, str(value) if value else "")
            entry.pack(side="left", padx=10)
            entries[key] = entry
        
        def save_profile():
            data = {k: v.get().strip() for k, v in entries.items()}
            
            if not data['ho_ten'] or not data['so_dien_thoai']:
                messagebox.showerror("Lỗi", "Họ tên và số điện thoại không được để trống")
                return
            
            result = self.controllers['khach_hang'].update(
                self.customer_info['id'], data['ho_ten'], data['so_dien_thoai'],
                data['email'], data['dia_chi']
            )
            
            if result:
                messagebox.showinfo("Thành công", "Cập nhật thông tin thành công")
                self.customer_info.update(data)
            else:
                messagebox.showerror("Lỗi", "Cập nhật thất bại")
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=30)
        
        ctk.CTkButton(btn_frame, text="💾 Cập nhật", command=save_profile,
                     fg_color="#00c853", width=150, height=45, font=ctk.CTkFont(size=14, weight="bold")).pack()
    
    # ==================== ĐỔI MẬT KHẨU ====================
    def show_change_password(self):
        self.clear_content()
        self.header_title.configure(text="Đổi mật khẩu")
        self.highlight_menu("🔑 Đổi mật khẩu")
        
        main_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a2e", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=50, pady=50)
        
        ctk.CTkLabel(main_frame, text="🔑 ĐỔI MẬT KHẨU", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(pady=30)
        
        # Mật khẩu cũ
        row1 = ctk.CTkFrame(main_frame, fg_color="transparent")
        row1.pack(fill="x", padx=80, pady=15)
        ctk.CTkLabel(row1, text="Mật khẩu cũ:", width=120, anchor="w").pack(side="left")
        old_pass = ctk.CTkEntry(row1, width=250, height=40, show="*")
        old_pass.pack(side="left", padx=10)
        
        # Mật khẩu mới
        row2 = ctk.CTkFrame(main_frame, fg_color="transparent")
        row2.pack(fill="x", padx=80, pady=15)
        ctk.CTkLabel(row2, text="Mật khẩu mới:", width=120, anchor="w").pack(side="left")
        new_pass = ctk.CTkEntry(row2, width=250, height=40, show="*")
        new_pass.pack(side="left", padx=10)
        
        # Xác nhận mật khẩu
        row3 = ctk.CTkFrame(main_frame, fg_color="transparent")
        row3.pack(fill="x", padx=80, pady=15)
        ctk.CTkLabel(row3, text="Xác nhận mật khẩu:", width=120, anchor="w").pack(side="left")
        confirm_pass = ctk.CTkEntry(row3, width=250, height=40, show="*")
        confirm_pass.pack(side="left", padx=10)
        
        def change_password():
            old = old_pass.get().strip()
            new = new_pass.get().strip()
            confirm = confirm_pass.get().strip()
            
            if not old or not new:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
                return
            
            if new != confirm:
                messagebox.showerror("Lỗi", "Mật khẩu mới và xác nhận không khớp")
                return
            
            if len(new) < 6:
                messagebox.showerror("Lỗi", "Mật khẩu mới phải có ít nhất 6 ký tự")
                return
            
            # Xác thực mật khẩu cũ
            from model.database import Database
            hashed_old = Database.hash_password(old)
            
            check_query = "SELECT id FROM tai_khoan_khach_hang WHERE id = %s AND password = %s"
            db = Database()
            user = db.fetch_one(check_query, (self.customer_info['id'], hashed_old))
            
            if not user:
                messagebox.showerror("Lỗi", "Mật khẩu cũ không đúng")
                return
            
            # Cập nhật mật khẩu mới
            hashed_new = Database.hash_password(new)
            update_query = "UPDATE tai_khoan_khach_hang SET password = %s WHERE id = %s"
            result = db.update(update_query, (hashed_new, self.customer_info['id']))
            
            if result:
                messagebox.showinfo("Thành công", "Đổi mật khẩu thành công")
                old_pass.delete(0, 'end')
                new_pass.delete(0, 'end')
                confirm_pass.delete(0, 'end')
            else:
                messagebox.showerror("Lỗi", "Đổi mật khẩu thất bại")
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=30)
        
        ctk.CTkButton(btn_frame, text="Đổi mật khẩu", command=change_password,
                     fg_color="#4a9eff", width=200, height=45, font=ctk.CTkFont(size=14, weight="bold")).pack()
    
    def logout(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            self.root.destroy()
            # Quay lại màn hình đăng nhập
            from view.login_view import LoginView
            def start_app(user):
                from view.modern_main_view import ModernMainView
                ModernMainView({
                    'khach_hang': self.controllers['khach_hang'],
                    'xe': self.controllers['xe'],
                    'dich_vu': self.controllers['dich_vu'],
                    'hoa_don': self.controllers['hoa_don'],
                    'dat_lich': self.controllers['dat_lich'],
                    'user': user
                })
            LoginView(start_app)
    
    def on_closing(self):
        if messagebox.askyesno("Thoát", "Bạn có chắc muốn thoát chương trình?"):
            self.root.destroy()