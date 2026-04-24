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
        
        # Center window
        self.center_window()
        
        # Lấy thông tin user từ controllers
        self.current_user = controllers.get('user', None)
        
        # Tạo layout
        self.setup_ui()
        
        # Hiển thị dashboard mặc định
        self.show_dashboard()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def center_window(self):
        """Căn giữa cửa sổ"""
        self.root.update_idletasks()
        width = 1400
        height = 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
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
            fg_color="#1a1a2e"
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Logo và tên công ty
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=30)
        
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="🚗",
            font=ctk.CTkFont(size=48),
            text_color="#4a9eff"
        )
        logo_label.pack()
        
        title_label = ctk.CTkLabel(
            logo_frame,
            text="AutoCare Pro",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#4a9eff"
        )
        title_label.pack(pady=(5, 0))
        
        slogan_label = ctk.CTkLabel(
            logo_frame,
            text="Chăm sóc xe chuyên nghiệp",
            font=ctk.CTkFont(size=11),
            text_color="#888888"
        )
        slogan_label.pack()
        
        # Separator
        separator = ctk.CTkFrame(self.sidebar, height=2, fg_color="#2a2a3e")
        separator.pack(fill="x", padx=20, pady=15)
        
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
                text_color="#e0e0e0",
                hover_color="#2a2a3e",
                anchor="w",
                height=45,
                font=ctk.CTkFont(size=14),
                corner_radius=8
            )
            btn.pack(fill="x", padx=20, pady=5)
            self.menu_buttons[text] = btn
        
        # User info ở cuối sidebar
        user_frame = ctk.CTkFrame(self.sidebar, fg_color="#15152a", corner_radius=10)
        user_frame.pack(side="bottom", fill="x", padx=15, pady=20)
        
        avatar_label = ctk.CTkLabel(
            user_frame,
            text="👤",
            font=ctk.CTkFont(size=40)
        )
        avatar_label.pack(pady=10)
        
        # Hiển thị thông tin user nếu có
        if self.current_user:
            user_name = ctk.CTkLabel(
                user_frame,
                text=self.current_user.get('ho_ten', 'Admin User'),
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#ffffff"
            )
            user_name.pack()
            
            user_role = ctk.CTkLabel(
                user_frame,
                text="Quản trị viên" if self.current_user.get('vai_tro') == 'admin' else "Nhân viên",
                font=ctk.CTkFont(size=11),
                text_color="#888888"
            )
            user_role.pack()
        else:
            user_name = ctk.CTkLabel(
                user_frame,
                text="Admin User",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#ffffff"
            )
            user_name.pack()
            
            user_role = ctk.CTkLabel(
                user_frame,
                text="Quản trị viên",
                font=ctk.CTkFont(size=11),
                text_color="#888888"
            )
            user_role.pack()
        
        logout_btn = ctk.CTkButton(
            user_frame,
            text="Đăng xuất",
            command=self.logout,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        logout_btn.pack(pady=(10, 15), padx=20, fill="x")
    
    def setup_header(self):
        """Thiết kế header cho content area"""
        self.header = ctk.CTkFrame(
            self.content_area,
            height=70,
            fg_color="#1a1a2e",
            corner_radius=0
        )
        self.header.pack(fill="x")
        self.header.pack_propagate(False)
        
        # Title
        self.header_title = ctk.CTkLabel(
            self.header,
            text="Dashboard",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#4a9eff"
        )
        self.header_title.place(x=30, y=18)
        
        # Date time
        time_frame = ctk.CTkFrame(self.header, fg_color="#2a2a3e", corner_radius=10)
        time_frame.place(x=1100, y=18)
        
        self.time_label = ctk.CTkLabel(
            time_frame,
            text="",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#4a9eff",
            padx=15,
            pady=8
        )
        self.time_label.pack()
        self.update_time()
    
    def update_time(self):
        if not self.root.winfo_exists():
            return

        now = datetime.now()
        self.time_label.configure(text=now.strftime("%H:%M:%S • %d/%m/%Y"))
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
                btn.configure(fg_color="#2a2a3e", text_color="#4a9eff")
            else:
                btn.configure(fg_color="transparent", text_color="#e0e0e0")
    
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
        chart_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a2e", corner_radius=15)
        chart_frame.pack(fill="both", expand=True, pady=20)
        
        chart_title = ctk.CTkLabel(
            chart_frame,
            text="📊 Doanh thu 7 ngày gần nhất",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        chart_title.pack(pady=20)
        
        # Lấy dữ liệu doanh thu - Lấy tất cả hóa đơn
        try:
            from_date = (datetime.now().date() - timedelta(days=7)).strftime("%Y-%m-%d")
            to_date = datetime.now().strftime("%Y-%m-%d")
            
            # Gọi thống kê
            thong_ke = self.controllers['hoa_don'].thong_ke(from_date, to_date, include_all_status=True)
            
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

            bars = ax.bar(dates, revenues, color='#4a9eff', alpha=0.8, edgecolor='white', linewidth=1)

            # ===== Title =====
            ax.set_title("Doanh thu 7 ngày gần nhất", fontsize=14, pad=15, color='white')

            # ===== Format tiền =====
            ax.yaxis.set_major_formatter(
                plt.FuncFormatter(lambda x, _: f"{int(x):,}")
            )

            # ===== Grid =====
            ax.grid(True, linestyle='--', alpha=0.3)
            ax.set_facecolor('#1a1a2e')
            fig.patch.set_facecolor('#1a1a2e')
            
            # ===== Màu trục =====
            ax.spines['bottom'].set_color('#888888')
            ax.spines['left'].set_color('#888888')
            ax.tick_params(colors='white')

            # ===== Hiển thị giá trị trên cột =====
            for i, (bar, v) in enumerate(zip(bars, revenues)):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f"{int(v):,}", ha='center', va='bottom', 
                       fontsize=9, color='white', rotation=0)

            # ===== Xoay ngày =====
            plt.xticks(rotation=30)

            # ===== Nhúng vào Tkinter =====
            canvas = FigureCanvasTkAgg(fig, master=chart_canvas)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        else:
            no_data_label = ctk.CTkLabel(
                chart_frame,
                text="📭 Chưa có dữ liệu doanh thu",
                font=ctk.CTkFont(size=14),
                text_color="#888888"
            )
            no_data_label.pack(expand=True, pady=50)
    
    def create_stat_card(self, parent, icon, title, value, color, column):
        """Tạo card thống kê"""
        card = ctk.CTkFrame(
            parent,
            fg_color="#1a1a2e",
            corner_radius=15,
            height=130
        )
        card.pack(side="left", padx=10, fill="x", expand=True)
        
        # Icon với nền màu
        icon_frame = ctk.CTkFrame(card, fg_color=color, corner_radius=12, width=50, height=50)
        icon_frame.pack_propagate(False)
        icon_frame.place(x=20, y=20)
        
        icon_label = ctk.CTkLabel(
            icon_frame,
            text=icon,
            font=ctk.CTkFont(size=28),
            text_color="white"
        )
        icon_label.pack(expand=True)
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        title_label.place(x=85, y=30)
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=color
        )
        value_label.place(x=85, y=60)
    
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
        filter_frame = ctk.CTkFrame(stats_frame, fg_color="#1a1a2e", corner_radius=15)
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

        monthly_frame = ctk.CTkFrame(self.thong_ke_container, fg_color="#1a1a2e", corner_radius=15)
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

        except Exception as e:
            print("Lỗi query:", e)
            rows = []

        # ===== XỬ LÝ GROUP THEO THÁNG =====
        monthly_data = {}

        for r in rows:
            ngay = r.get("ngay_lap")
            tien = float(r.get("tong_tien") or 0)

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
            
            # Tạo frame chứa treeview
            tree_frame = ctk.CTkFrame(monthly_frame, fg_color="transparent")
            tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Tạo scrollbar
            scrollbar = ttk.Scrollbar(tree_frame)
            scrollbar.pack(side="right", fill="y")
            
            tree = ttk.Treeview(tree_frame, columns=columns, show="headings", 
                               yscrollcommand=scrollbar.set, height=10)
            
            # Style cho treeview
            style = ttk.Style()
            style.configure("Treeview", 
                          background="#1a1a2e", 
                          foreground="white", 
                          fieldbackground="#1a1a2e",
                          rowheight=30)
            style.configure("Treeview.Heading", 
                          background="#2a2a3e", 
                          foreground="white", 
                          font=('Arial', 10, 'bold'))
            style.map('Treeview', background=[('selected', '#4a9eff')])

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center", width=180)

            scrollbar.config(command=tree.yview)

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

            tree.pack(fill="both", expand=True)

            # ===== TỔNG DOANH THU =====
            total_revenue = sum(m["revenue"] for m in monthly_data.values())
            total_invoices = sum(m["count"] for m in monthly_data.values())
            avg_revenue = total_revenue / total_invoices if total_invoices > 0 else 0

            summary_frame = ctk.CTkFrame(monthly_frame, fg_color="#2a2a3e", corner_radius=10)
            summary_frame.pack(fill="x", padx=10, pady=10)
            
            summary_text = f"📊 Tổng số hóa đơn: {total_invoices} | 💰 Tổng doanh thu: {total_revenue:,.0f} VNĐ | 📈 Trung bình/hóa đơn: {avg_revenue:,.0f} VNĐ"
            summary_label = ctk.CTkLabel(
                summary_frame,
                text=summary_text,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#4a9eff",
                padx=10,
                pady=10
            )
            summary_label.pack()

        else:
            ctk.CTkLabel(
                monthly_frame,
                text="📭 Không có dữ liệu",
                font=ctk.CTkFont(size=14),
                text_color="#888888"
            ).pack(pady=50)

        # ===== TOP DỊCH VỤ =====
        top_services_frame = ctk.CTkFrame(self.thong_ke_container, fg_color="#1a1a2e", corner_radius=15)
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
                    SUM(ct.so_luong) as tong_so_luong,
                    SUM(ct.thanh_tien) as tong_doanh_thu
                FROM chi_tiet_hoa_don ct
                JOIN dich_vu dv ON ct.id_dich_vu = dv.id
                GROUP BY ct.id_dich_vu
                ORDER BY so_lan_su_dung DESC
                LIMIT 5
            """

            top_services = self.controllers['hoa_don'].model.db.fetch_all(top_query)

            if top_services:
                # Tạo frame chứa treeview
                tree_frame = ctk.CTkFrame(top_services_frame, fg_color="transparent")
                tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
                
                scrollbar = ttk.Scrollbar(tree_frame)
                scrollbar.pack(side="right", fill="y")
                
                cols = ("Tên dịch vụ", "Số lần SD", "Tổng SL", "Doanh thu")
                tree = ttk.Treeview(tree_frame, columns=cols, show="headings",
                                   yscrollcommand=scrollbar.set, height=5)

                for col in cols:
                    tree.heading(col, text=col)
                    tree.column(col, anchor="center", width=150)

                scrollbar.config(command=tree.yview)

                for s in top_services:
                    tree.insert("", "end", values=(
                        s.get("ten_dich_vu", "N/A"),
                        s.get("so_lan_su_dung", 0),
                        s.get("tong_so_luong", 0),
                        f"{s.get('tong_doanh_thu', 0):,.0f} VNĐ"
                    ))

                tree.pack(fill="both", expand=True)
            else:
                ctk.CTkLabel(top_services_frame, text="📭 Chưa có dữ liệu", 
                            text_color="#888888", pady=30).pack()

        except Exception as e:
            ctk.CTkLabel(top_services_frame, text=f"⚠️ Lỗi: {str(e)}", 
                        text_color="#ff5252", pady=30).pack()
    
    # ==================== CÀI ĐẶT ====================
    
    def show_settings(self):
        """Hiển thị giao diện cài đặt"""
        self.clear_content()
        self.header_title.configure(text="Cài đặt hệ thống")
        self.highlight_menu("⚙️ Cài đặt")
        
        # Theme settings
        theme_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a2e", corner_radius=15)
        theme_frame.pack(fill="x", pady=20, padx=20)
        
        theme_title = ctk.CTkLabel(
            theme_frame,
            text="🎨 Giao diện",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        theme_title.pack(pady=20)
        
        theme_var = ctk.StringVar(value="dark")
        
        def change_theme():
            ctk.set_appearance_mode(theme_var.get())
        
        dark_radio = ctk.CTkRadioButton(
            theme_frame,
            text="🌙 Dark Mode",
            variable=theme_var,
            value="dark",
            command=change_theme
        )
        dark_radio.pack(pady=10)
        
        light_radio = ctk.CTkRadioButton(
            theme_frame,
            text="☀️ Light Mode",
            variable=theme_var,
            value="light",
            command=change_theme
        )
        light_radio.pack(pady=10)
        
        # Database settings
        db_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a2e", corner_radius=15)
        db_frame.pack(fill="x", pady=20, padx=20)
        
        db_title = ctk.CTkLabel(
            db_frame,
            text="💾 Dữ liệu",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        db_title.pack(pady=20)
        
        backup_btn = ctk.CTkButton(
            db_frame,
            text="📦 Sao lưu dữ liệu",
            command=self.backup_database,
            fg_color="#4a9eff",
            height=40,
            width=200,
            corner_radius=8
        )
        backup_btn.pack(pady=10)
        
        # Thông tin hệ thống
        info_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a2e", corner_radius=15)
        info_frame.pack(fill="x", pady=20, padx=20)
        
        info_title = ctk.CTkLabel(
            info_frame,
            text="ℹ️ Thông tin hệ thống",
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