import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from .modern_khach_hang_view import ModernKhachHangView
from .modern_xe_view import ModernXeView
from .modern_dich_vu_view import ModernDichVuView
from .modern_hoa_don_view import ModernHoaDonView
from view.login_view import LoginView
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Cài đặt theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModernMainView:
    def __init__(self, controllers):
        self.controllers = controllers
        self.current_frame = None
        self.current_view = None
        self.after_id = None
        
        # Cấu hình cửa sổ chính
        self.root = ctk.CTk()
        self.root.title("AutoCare Pro - Quản lý dịch vụ chăm sóc xe ô tô")
        self.root.geometry("1400x800")
        
        # Lấy thông tin user từ controllers
        self.current_user = controllers.get('user', None)
        
        # Tạo layout
        self.setup_ui()
        
        # Hiển thị dashboard mặc định
        self.show_dashboard()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
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
        
        # Hiển thị thông tin user nếu có
        if self.current_user:
            user_name = ctk.CTkLabel(
                user_frame,
                text=self.current_user.get('ho_ten', 'Admin User'),
                font=ctk.CTkFont(size=14, weight="bold")
            )
            user_name.pack()
            
            user_role = ctk.CTkLabel(
                user_frame,
                text="Quản trị viên" if self.current_user.get('vai_tro') == 'admin' else "Nhân viên",
                font=ctk.CTkFont(size=12),
                text_color="#888888"
            )
            user_role.pack()
        else:
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
        if not self.root.winfo_exists():
            return

        now = datetime.now()
        self.time_label.configure(text=now.strftime("%H:%M:%S - %d/%m/%Y"))
        self.after_id = self.root.after(1000, self.update_time)
    
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
        try:
            total_kh = self.controllers['khach_hang'].model.get_total()
        except:
            total_kh = len(self.controllers['khach_hang'].get_all())
        
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
        
        # Lấy dữ liệu doanh thu - Lấy tất cả hóa đơn
        try:
            from_date = (datetime.now().date() - timedelta(days=7)).strftime("%Y-%m-%d")
            to_date = datetime.now().strftime("%Y-%m-%d")
            
            print(f"DEBUG Dashboard: from_date={from_date}, to_date={to_date}")
            
            # Kiểm tra trực tiếp database để debug
            check_query = """SELECT id, ma_hd, ngay_lap, trang_thai, tong_tien 
                            FROM hoa_don 
                            WHERE DATE(ngay_lap) BETWEEN %s AND %s"""
            all_invoices = self.controllers['hoa_don'].model.db.fetch_all(check_query, (from_date, to_date))
            print(f"DEBUG Dashboard: Tổng số hóa đơn trong 7 ngày: {len(all_invoices) if all_invoices else 0}")
            
            if all_invoices:
                for inv in all_invoices:
                    print(f"DEBUG Dashboard: HD {inv.get('id')} - {inv.get('ma_hd')} - Ngày: {inv.get('ngay_lap')} - Tiền: {inv.get('tong_tien')} - Status: {inv.get('trang_thai')}")
            
            # Gọi thống kê
            thong_ke = self.controllers['hoa_don'].thong_ke(from_date, to_date, include_all_status=True)
            print(f"DEBUG Dashboard: Kết quả thống kê: {thong_ke}")
            
        except Exception as e:
            print(f"DEBUG Dashboard Lỗi: {e}")
            import traceback
            traceback.print_exc()
            thong_ke = []
        
        # Tạo frame cho biểu đồ
        if thong_ke and len(thong_ke) > 0:
            chart_canvas = ctk.CTkFrame(chart_frame, fg_color="transparent")
            chart_canvas.pack(fill="both", expand=True, padx=20, pady=20)

            # ===== Chuẩn bị dữ liệu =====
            dates = []
            revenues = []

            for stat in thong_ke[:7]:
                ngay = stat['ngay']

                if isinstance(ngay, datetime):
                    dates.append(ngay.strftime("%d/%m"))
                else:
                    try:
                        dates.append(datetime.strptime(str(ngay), "%Y-%m-%d").strftime("%d/%m"))
                    except:
                        dates.append(str(ngay))

                revenues.append(float(stat['doanh_thu']))

            # ===== STYLE DARK CHO ĐẸP =====
            plt.style.use('dark_background')

            fig, ax = plt.subplots(figsize=(8, 4), dpi=100)

            bars = ax.bar(dates, revenues)

            # ===== Màu sắc đẹp hơn =====
            for bar in bars:
                bar.set_alpha(0.85)

            # ===== Title =====
            ax.set_title("Doanh thu 7 ngày gần nhất", fontsize=14, pad=15)

            # ===== Format tiền =====
            ax.yaxis.set_major_formatter(
                plt.FuncFormatter(lambda x, _: f"{int(x):,}")
            )

            # ===== Grid =====
            ax.grid(True, linestyle='--', alpha=0.3)

            # ===== Hiển thị giá trị trên cột =====
            for i, v in enumerate(revenues):
                ax.text(i, v, f"{int(v):,}", ha='center', va='bottom', fontsize=9)

            # ===== Xoay ngày =====
            plt.xticks(rotation=30)

            # ===== Nhúng vào Tkinter =====
            canvas = FigureCanvasTkAgg(fig, master=chart_canvas)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
    
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
        
        # === Thêm bộ lọc trạng thái ===
        filter_frame = ctk.CTkFrame(stats_frame, fg_color="#1f1f1f", corner_radius=15)
        filter_frame.pack(fill="x", pady=10, padx=10)
        
        filter_title = ctk.CTkLabel(
            filter_frame,
            text="🔍 Bộ lọc thống kê",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        filter_title.pack(pady=10)
        
        filter_row = ctk.CTkFrame(filter_frame, fg_color="transparent")
        filter_row.pack(pady=10)
        
        ctk.CTkLabel(filter_row, text="Trạng thái:", font=ctk.CTkFont(size=13)).pack(side="left", padx=10)
        
        status_filter_var = ctk.StringVar(value="all")
        
        status_options = [
            ("📊 Tất cả", "all"),
            ("✅ Hoàn thành", "hoan_thanh"),
            ("🟡 Đang xử lý", "dang_xu_ly"),
            ("🔴 Đã hủy", "da_huy")
        ]
        
        for text, value in status_options:
            radio = ctk.CTkRadioButton(
                filter_row, 
                text=text, 
                variable=status_filter_var, 
                value=value,
                command=lambda: self.load_thong_ke_data(stats_frame, status_filter_var)
            )
            radio.pack(side="left", padx=15)
        
        # Khung hiển thị kết quả thống kê
        self.thong_ke_container = ctk.CTkFrame(stats_frame, fg_color="transparent")
        self.thong_ke_container.pack(fill="both", expand=True, pady=10)
        
        # Load dữ liệu ban đầu
        self.load_thong_ke_data(stats_frame, status_filter_var)

    def load_thong_ke_data(self, parent_frame, status_filter_var):
        """Tải dữ liệu thống kê theo bộ lọc (FIX FULL)"""

        # Xóa UI cũ
        for widget in self.thong_ke_container.winfo_children():
            widget.destroy()

        monthly_frame = ctk.CTkFrame(self.thong_ke_container, fg_color="#1f1f1f", corner_radius=15)
        monthly_frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(
            monthly_frame,
            text="📊 Thống kê doanh thu theo tháng",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=15)

        # ===== LẤY DATA =====
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)

        status_filter = status_filter_var.get()

        try:
            if status_filter == "all":
                query = """
                    SELECT ngay_lap, tong_tien, trang_thai
                    FROM hoa_don
                    WHERE ngay_lap BETWEEN %s AND %s
                """
                params = (start_date, end_date)
            else:
                query = """
                    SELECT ngay_lap, tong_tien, trang_thai
                    FROM hoa_don
                    WHERE trang_thai = %s
                    AND ngay_lap BETWEEN %s AND %s
                """
                params = (status_filter, start_date, end_date)

            rows = self.controllers['hoa_don'].model.db.fetch_all(query, params)

            print("DEBUG rows:", rows)

        except Exception as e:
            print("Lỗi query:", e)
            rows = []

        # ===== XỬ LÝ GROUP THEO THÁNG =====
        monthly_data = {}

        for r in rows:
            ngay = r.get("ngay_lap")
            tien = float(r.get("tong_tien") or 0)
            status = r.get("trang_thai")

            # Convert ngày an toàn
            if isinstance(ngay, str):
                try:
                    ngay = datetime.strptime(ngay, "%Y-%m-%d %H:%M:%S")
                except:
                    try:
                        ngay = datetime.strptime(ngay, "%Y-%m-%d")
                    except:
                        continue

            if not isinstance(ngay, datetime):
                continue

            month_key = ngay.strftime("%m/%Y")

            if month_key not in monthly_data:
                monthly_data[month_key] = {
                    "count": 0,
                    "revenue": 0
                }

            monthly_data[month_key]["count"] += 1
            monthly_data[month_key]["revenue"] += tien

        # ===== HIỂN THỊ =====
        if monthly_data:
            columns = ("Tháng", "Số hóa đơn", "Doanh thu", "Trung bình")
            tree = ttk.Treeview(monthly_frame, columns=columns, show="headings", height=10)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center", width=180)

            # Sort theo tháng mới nhất
            sorted_data = sorted(monthly_data.items(), key=lambda x: datetime.strptime(x[0], "%m/%Y"), reverse=True)

            for month, data in sorted_data:
                avg = data["revenue"] / data["count"] if data["count"] else 0

                tree.insert("", "end", values=(
                    month,
                    data["count"],
                    f"{data['revenue']:,.0f} VNĐ",
                    f"{avg:,.0f} VNĐ"
                ))

            tree.pack(fill="both", expand=True, padx=10, pady=10)

            # ===== TỔNG DOANH THU =====
            total_revenue = sum(m["revenue"] for m in monthly_data.values())

            ctk.CTkLabel(
                monthly_frame,
                text=f"💰 Tổng doanh thu: {total_revenue:,.0f} VNĐ",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#00c853"
            ).pack(pady=10)

        else:
            ctk.CTkLabel(
                monthly_frame,
                text="📭 Không có dữ liệu",
                font=ctk.CTkFont(size=14),
                text_color="#888888"
            ).pack(pady=50)

        # ===== TOP DỊCH VỤ (GIỮ NGUYÊN + FIX NHẸ) =====
        top_services_frame = ctk.CTkFrame(self.thong_ke_container, fg_color="#1f1f1f", corner_radius=15)
        top_services_frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(
            top_services_frame,
            text="🏆 Top dịch vụ được sử dụng nhiều nhất",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=15)

        try:
            top_query = """
                SELECT dv.ten_dich_vu,
                    COUNT(*) as so_lan_su_dung,
                    SUM(ct.so_luong) as tong_so_luong
                FROM chi_tiet_hoa_don ct
                JOIN dich_vu dv ON ct.id_dich_vu = dv.id
                GROUP BY ct.id_dich_vu
                ORDER BY so_lan_su_dung DESC
                LIMIT 5
            """

            top_services = self.controllers['hoa_don'].model.db.fetch_all(top_query)

            if top_services:
                cols = ("Tên dịch vụ", "Số lần", "Tổng SL")
                tree = ttk.Treeview(top_services_frame, columns=cols, show="headings", height=5)

                for col in cols:
                    tree.heading(col, text=col)
                    tree.column(col, anchor="center", width=200)

                for s in top_services:
                    tree.insert("", "end", values=(
                        s.get("ten_dich_vu"),
                        s.get("so_lan_su_dung", 0),
                        s.get("tong_so_luong", 0)
                    ))

                tree.pack(fill="both", expand=True, padx=10, pady=10)
            else:
                ctk.CTkLabel(top_services_frame, text="Chưa có dữ liệu", text_color="#888").pack(pady=30)

        except Exception as e:
            ctk.CTkLabel(top_services_frame, text=f"Lỗi: {e}", text_color="#888").pack(pady=30)
    
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
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            if self.after_id:
                self.root.after_cancel(self.after_id)
            self.root.destroy()

            def start_app(user):
                from controller.khach_hang_controller import KhachHangController
                from controller.xe_controller import XeController
                from controller.dich_vu_controller import DichVuController
                from controller.hoa_don_controller import HoaDonController

                controllers = {
                    'khach_hang': KhachHangController(),
                    'xe': XeController(),
                    'dich_vu': DichVuController(),
                    'hoa_don': HoaDonController(),
                    'user': user
                }

                ModernMainView(controllers)

            LoginView(start_app)
    
    def on_closing(self):
        if messagebox.askyesno("Thoát", "Bạn có chắc muốn thoát chương trình?"):
            if self.after_id:
                self.root.after_cancel(self.after_id)
            self.root.destroy()