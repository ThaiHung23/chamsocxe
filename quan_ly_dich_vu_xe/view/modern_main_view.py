import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
from .modern_khach_hang_view import ModernKhachHangView
from .modern_xe_view import ModernXeView
from .modern_dich_vu_view import ModernDichVuView
from .modern_hoa_don_view import ModernHoaDonView

# Cài đặt theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModernMainView:
    def __init__(self, controllers):
        self.controllers = controllers
        self.current_frame = None
        self.current_view = None
        
        # Cấu hình cửa sổ chính
        self.root = ctk.CTk()
        self.root.title("AutoCare Pro - Quản lý dịch vụ chăm sóc xe ô tô")
        self.root.geometry("1400x800")
        
        # Tạo layout
        self.setup_ui()
        
        # Hiển thị dashboard mặc định
        self.show_dashboard()
        
        self.root.mainloop()
    
    def setup_ui(self):
        """Tạo layout chính với sidebar và content area"""
        
        # Frame chính
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        # Sidebar (thanh bên trái)
        self.setup_sidebar()
        
        # Content area (bên phải)
        self.content_area = ctk.CTkFrame(
            self.main_container, 
            fg_color="#2b2b2b",
            corner_radius=0
        )
        self.content_area.pack(side="right", fill="both", expand=True)
        
        # Header cho content area
        self.setup_header()
        
        # Frame để chứa nội dung động
        self.content_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    def setup_sidebar(self):
        """Thiết kế sidebar chuyên nghiệp"""
        self.sidebar = ctk.CTkFrame(
            self.main_container, 
            width=280, 
            corner_radius=0,
            fg_color="#1a1a1a"
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Logo và tên công ty
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=30)
        
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="🚗 AutoCare Pro",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#4a9eff"
        )
        logo_label.pack()
        
        slogan_label = ctk.CTkLabel(
            logo_frame,
            text="Chăm sóc xe chuyên nghiệp",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        slogan_label.pack()
        
        # Menu items
        menu_items = [
            ("📊 Dashboard", self.show_dashboard),
            ("👥 Khách hàng", self.show_khach_hang),
            ("🚘 Xe", self.show_xe),
            ("🔧 Dịch vụ", self.show_dich_vu),
            ("📄 Hóa đơn", self.show_hoa_don),
            ("📈 Thống kê", self.show_thong_ke),
            ("⚙️ Cài đặt", self.show_settings)
        ]
        
        self.menu_buttons = {}
        for text, command in menu_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                fg_color="transparent",
                text_color="#ffffff",
                hover_color="#3a3a3a",
                anchor="w",
                height=45,
                font=ctk.CTkFont(size=14)
            )
            btn.pack(fill="x", padx=20, pady=5)
            self.menu_buttons[text] = btn
        
        # User info ở cuối sidebar
        user_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        user_frame.pack(side="bottom", pady=20, fill="x", padx=20)
        
        avatar_label = ctk.CTkLabel(
            user_frame,
            text="👤",
            font=ctk.CTkFont(size=40)
        )
        avatar_label.pack()
        
        user_name = ctk.CTkLabel(
            user_frame,
            text="Admin User",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        user_name.pack()
        
        user_role = ctk.CTkLabel(
            user_frame,
            text="Quản trị viên",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        user_role.pack()
        
        logout_btn = ctk.CTkButton(
            user_frame,
            text="Đăng xuất",
            command=self.logout,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            height=35
        )
        logout_btn.pack(pady=10)
    
    def setup_header(self):
        """Thiết kế header cho content area"""
        self.header = ctk.CTkFrame(
            self.content_area,
            height=70,
            fg_color="#1f1f1f",
            corner_radius=0
        )
        self.header.pack(fill="x")
        self.header.pack_propagate(False)
        
        # Title
        self.header_title = ctk.CTkLabel(
            self.header,
            text="Dashboard",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#4a9eff"
        )
        self.header_title.place(x=30, y=20)
        
        # Date time
        self.time_label = ctk.CTkLabel(
            self.header,
            text="",
            font=ctk.CTkFont(size=14),
            text_color="#888888"
        )
        self.time_label.place(x=1100, y=25)
        self.update_time()
    
    def update_time(self):
        """Cập nhật thời gian thực"""
        now = datetime.now()
        self.time_label.configure(text=now.strftime("%H:%M:%S - %d/%m/%Y"))
        self.root.after(1000, self.update_time)
    
    def clear_content(self):
        """Xóa nội dung hiện tại"""
        if self.current_view:
            self.current_view = None
        
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def highlight_menu(self, menu_text):
        """Highlight menu item đang được chọn"""
        for text, btn in self.menu_buttons.items():
            if text == menu_text:
                btn.configure(fg_color="#3a3a3a")
            else:
                btn.configure(fg_color="transparent")
    
    # ==================== CÁC CHỨC NĂNG CHÍNH ====================
    
    def show_dashboard(self):
        """Hiển thị Dashboard với các thống kê"""
        self.clear_content()
        self.header_title.configure(text="Dashboard")
        self.highlight_menu("📊 Dashboard")
        
        # Frame chứa các card thống kê
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=20)
        
        # Lấy dữ liệu thống kê
        total_kh = self.controllers['khach_hang'].model.get_total()
        total_xe = len(self.controllers['xe'].get_all())
        total_dv = len(self.controllers['dich_vu'].get_all())
        total_hd = len(self.controllers['hoa_don'].get_all())
        
        # Card 1: Khách hàng
        self.create_stat_card(stats_frame, "👥", "Khách hàng", str(total_kh), "#4a9eff", 0)
        # Card 2: Xe
        self.create_stat_card(stats_frame, "🚘", "Xe đang quản lý", str(total_xe), "#00c853", 1)
        # Card 3: Dịch vụ
        self.create_stat_card(stats_frame, "🔧", "Dịch vụ", str(total_dv), "#ff9800", 2)
        # Card 4: Hóa đơn
        self.create_stat_card(stats_frame, "📄", "Hóa đơn", str(total_hd), "#e91e63", 3)
        
        # Biểu đồ doanh thu
        chart_frame = ctk.CTkFrame(self.content_frame, fg_color="#1f1f1f", corner_radius=15)
        chart_frame.pack(fill="both", expand=True, pady=20)
        
        chart_title = ctk.CTkLabel(
            chart_frame,
            text="Doanh thu 7 ngày gần nhất",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        chart_title.pack(pady=20)
        
        # Lấy dữ liệu doanh thu
        thong_ke = self.controllers['hoa_don'].thong_ke(
            (datetime.now().date() - timedelta(days=7)).strftime("%Y-%m-%d"),
            datetime.now().strftime("%Y-%m-%d")
        )
        
        # Tạo frame cho biểu đồ
        if thong_ke:
            chart_canvas = ctk.CTkFrame(chart_frame, fg_color="transparent")
            chart_canvas.pack(pady=20, padx=40, fill="x")
            
            max_doanh_thu = max([s['doanh_thu'] for s in thong_ke]) if thong_ke else 1
            
            for i, stat in enumerate(thong_ke[:7]):
                col_frame = ctk.CTkFrame(chart_canvas, fg_color="transparent")
                col_frame.pack(side="left", expand=True, fill="x")
                
                height = (stat['doanh_thu'] / max_doanh_thu) * 150
                bar = ctk.CTkFrame(
                    col_frame,
                    height=height,
                    width=50,
                    fg_color="#4a9eff",
                    corner_radius=5
                )
                bar.pack(pady=5)
                
                value_label = ctk.CTkLabel(
                    col_frame,
                    text=f"{stat['doanh_thu']:,.0f}",
                    font=ctk.CTkFont(size=10)
                )
                value_label.pack()
                
                date_label = ctk.CTkLabel(
                    col_frame,
                    text=stat['ngay'].strftime("%d/%m") if isinstance(stat['ngay'], datetime) else stat['ngay'],
                    font=ctk.CTkFont(size=10)
                )
                date_label.pack()
        else:
            no_data_label = ctk.CTkLabel(
                chart_frame,
                text="Chưa có dữ liệu doanh thu",
                font=ctk.CTkFont(size=14),
                text_color="#888888"
            )
            no_data_label.pack(pady=50)
    
    def create_stat_card(self, parent, icon, title, value, color, column):
        """Tạo card thống kê"""
        card = ctk.CTkFrame(
            parent,
            fg_color="#1f1f1f",
            corner_radius=15,
            width=250,
            height=120
        )
        card.pack(side="left", padx=10, fill="x", expand=True)
        
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=40)
        )
        icon_label.place(x=20, y=20)
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        title_label.place(x=80, y=30)
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=color
        )
        value_label.place(x=80, y=60)
    
    # ==================== QUẢN LÝ KHÁCH HÀNG ====================
    
    def show_khach_hang(self):
        """Hiển thị giao diện quản lý khách hàng"""
        self.clear_content()
        self.header_title.configure(text="Quản lý khách hàng")
        self.highlight_menu("👥 Khách hàng")
        
        # Tạo view quản lý khách hàng
        self.current_view = ModernKhachHangView(
            self.content_frame,
            self.controllers['khach_hang'],
            on_refresh_callback=self.refresh_dashboard_stats
        )
        self.current_view.main_frame.pack(fill="both", expand=True)
    
    # ==================== QUẢN LÝ XE ====================
    
    def show_xe(self):
        """Hiển thị giao diện quản lý xe"""
        self.clear_content()
        self.header_title.configure(text="Quản lý xe")
        self.highlight_menu("🚘 Xe")
        
        # Tạo view quản lý xe
        self.current_view = ModernXeView(
            self.content_frame,
            self.controllers['xe'],
            self.controllers['khach_hang'],
            on_refresh_callback=self.refresh_dashboard_stats
        )
        self.current_view.main_frame.pack(fill="both", expand=True)
    
    # ==================== QUẢN LÝ DỊCH VỤ ====================
    
    def show_dich_vu(self):
        """Hiển thị giao diện quản lý dịch vụ"""
        self.clear_content()
        self.header_title.configure(text="Quản lý dịch vụ")
        self.highlight_menu("🔧 Dịch vụ")
        
        # Tạo view quản lý dịch vụ
        self.current_view = ModernDichVuView(
            self.content_frame,
            self.controllers['dich_vu']
        )
        self.current_view.main_frame.pack(fill="both", expand=True)
    
    # ==================== QUẢN LÝ HÓA ĐƠN ====================
    
    def show_hoa_don(self):
        """Hiển thị giao diện quản lý hóa đơn"""
        self.clear_content()
        self.header_title.configure(text="Quản lý hóa đơn")
        self.highlight_menu("📄 Hóa đơn")
        
        # Tạo view quản lý hóa đơn
        self.current_view = ModernHoaDonView(
            self.content_frame,
            self.controllers['hoa_don'],
            self.controllers['xe'],
            self.controllers['dich_vu']
        )
        self.current_view.main_frame.pack(fill="both", expand=True)
    
    # ==================== THỐNG KÊ NÂNG CAO ====================
    
    def show_thong_ke(self):
        """Hiển thị giao diện thống kê nâng cao"""
        self.clear_content()
        self.header_title.configure(text="Thống kê & Báo cáo")
        self.highlight_menu("📈 Thống kê")
        
        # Tạo frame thống kê
        stats_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        stats_frame.pack(fill="both", expand=True)
        
        # Thống kê theo tháng
        monthly_frame = ctk.CTkFrame(stats_frame, fg_color="#1f1f1f", corner_radius=15)
        monthly_frame.pack(fill="x", pady=10, padx=10)
        
        monthly_title = ctk.CTkLabel(
            monthly_frame,
            text="📊 Thống kê doanh thu theo tháng",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        monthly_title.pack(pady=15)
        
        # Lấy thống kê 6 tháng gần nhất
        from datetime import datetime, timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)
        
        stats = self.controllers['hoa_don'].thong_ke(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )
        
        if stats:
            # Tạo bảng thống kê
            columns = ("Tháng", "Số lượng hóa đơn", "Doanh thu", "Trung bình/đơn")
            tree = ttk.Treeview(monthly_frame, columns=columns, show="headings", height=10)
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=200)
            
            # Nhóm theo tháng
            monthly_data = {}
            for stat in stats:
                if isinstance(stat['ngay'], datetime):
                    month_key = stat['ngay'].strftime("%m/%Y")
                    if month_key not in monthly_data:
                        monthly_data[month_key] = {'count': 0, 'revenue': 0}
                    monthly_data[month_key]['count'] += stat['so_luong']
                    monthly_data[month_key]['revenue'] += stat['doanh_thu']
            
            for month, data in sorted(monthly_data.items()):
                avg = data['revenue'] / data['count'] if data['count'] > 0 else 0
                tree.insert("", "end", values=(
                    month,
                    data['count'],
                    f"{data['revenue']:,.0f} VNĐ",
                    f"{avg:,.0f} VNĐ"
                ))
            
            tree.pack(fill="both", expand=True, padx=10, pady=10)
        else:
            no_data_label = ctk.CTkLabel(
                monthly_frame,
                text="Chưa có dữ liệu thống kê",
                font=ctk.CTkFont(size=14),
                text_color="#888888"
            )
            no_data_label.pack(pady=50)
        
        # Top dịch vụ
        top_services_frame = ctk.CTkFrame(stats_frame, fg_color="#1f1f1f", corner_radius=15)
        top_services_frame.pack(fill="x", pady=10, padx=10)
        
        top_title = ctk.CTkLabel(
            top_services_frame,
            text="🏆 Top dịch vụ được sử dụng nhiều nhất",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        top_title.pack(pady=15)
        
        top_info = ctk.CTkLabel(
            top_services_frame,
            text="Tính năng đang phát triển",
            font=ctk.CTkFont(size=14),
            text_color="#888888"
        )
        top_info.pack(pady=30)
    
    # ==================== CÀI ĐẶT ====================
    
    def show_settings(self):
        """Hiển thị giao diện cài đặt"""
        self.clear_content()
        self.header_title.configure(text="Cài đặt hệ thống")
        self.highlight_menu("⚙️ Cài đặt")
        
        # Theme settings
        theme_frame = ctk.CTkFrame(self.content_frame, fg_color="#1f1f1f", corner_radius=15)
        theme_frame.pack(fill="x", pady=20, padx=20)
        
        theme_title = ctk.CTkLabel(
            theme_frame,
            text="Giao diện",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        theme_title.pack(pady=20)
        
        theme_var = ctk.StringVar(value="dark")
        
        def change_theme():
            ctk.set_appearance_mode(theme_var.get())
        
        dark_radio = ctk.CTkRadioButton(
            theme_frame,
            text="Dark Mode",
            variable=theme_var,
            value="dark",
            command=change_theme
        )
        dark_radio.pack(pady=10)
        
        light_radio = ctk.CTkRadioButton(
            theme_frame,
            text="Light Mode",
            variable=theme_var,
            value="light",
            command=change_theme
        )
        light_radio.pack(pady=10)
        
        # Database settings
        db_frame = ctk.CTkFrame(self.content_frame, fg_color="#1f1f1f", corner_radius=15)
        db_frame.pack(fill="x", pady=20, padx=20)
        
        db_title = ctk.CTkLabel(
            db_frame,
            text="Dữ liệu",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        db_title.pack(pady=20)
        
        backup_btn = ctk.CTkButton(
            db_frame,
            text="📦 Sao lưu dữ liệu",
            command=self.backup_database,
            fg_color="#4a9eff",
            height=40,
            width=200
        )
        backup_btn.pack(pady=10)
        
        # Thông tin hệ thống
        info_frame = ctk.CTkFrame(self.content_frame, fg_color="#1f1f1f", corner_radius=15)
        info_frame.pack(fill="x", pady=20, padx=20)
        
        info_title = ctk.CTkLabel(
            info_frame,
            text="Thông tin hệ thống",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        info_title.pack(pady=20)
        
        info_text = ctk.CTkLabel(
            info_frame,
            text="AutoCare Pro - Phần mềm quản lý dịch vụ chăm sóc xe ô tô\n"
                 "Phiên bản 2.0\n"
                 "© 2024 - Bản quyền thuộc về AutoCare Pro",
            font=ctk.CTkFont(size=12),
            text_color="#888888",
            justify="center"
        )
        info_text.pack(pady=20)
    
    def backup_database(self):
        """Sao lưu database"""
        import subprocess
        import os
        from datetime import datetime
        
        backup_dir = "backup"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        backup_file = f"{backup_dir}/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
        
        try:
            # Sử dụng mysqldump
            cmd = f'mysqldump -u root quan_ly_dich_vu_xe > "{backup_file}"'
            subprocess.run(cmd, shell=True, check=True)
            messagebox.showinfo("Thành công", f"Sao lưu thành công tại: {backup_file}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Sao lưu thất bại: {str(e)}\nVui lòng sao lưu thủ công từ phpMyAdmin")
    
    def refresh_dashboard_stats(self):
        """Làm mới thống kê trên dashboard (khi có thay đổi dữ liệu)"""
        # Nếu đang ở dashboard thì refresh
        if self.header_title.cget("text") == "Dashboard":
            self.show_dashboard()
    
    def logout(self):
        """Đăng xuất"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            self.root.destroy()
            # Có thể mở lại màn hình login ở đây