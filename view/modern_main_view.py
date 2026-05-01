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
from .modern_dat_lich_view import ModernDatLichView   

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModernMainView:
    def __init__(self, controllers):
        self.controllers = controllers
        self.current_frame = None
        self.current_view = None
        self.after_id = None
        self.root = ctk.CTk()
        self.root.title("AutoCare Pro - Quản lý dịch vụ chăm sóc xe ô tô")
        self.root.geometry("1400x800")
        self.center_window()
        self.current_user = controllers.get('user', None)
        self.setup_ui()
        self.show_dashboard()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def center_window(self):
        self.root.update_idletasks()
        width, height = 1400, 800
        x = (self.root.winfo_screenwidth()  // 2) - (width  // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        self.setup_sidebar()
        self.content_area = ctk.CTkFrame(self.main_container, fg_color="#2b2b2b", corner_radius=0)
        self.content_area.pack(side="right", fill="both", expand=True)
        self.setup_header()
        self.content_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self.main_container, width=280, corner_radius=0, fg_color="#1a1a2e")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # ========== PHẦN TRÊN CÙNG ==========
        # Logo frame - gắn vào top
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(side="top", fill="x", pady=30)
        
        ctk.CTkLabel(logo_frame, text="🚗", font=ctk.CTkFont(size=48), text_color="#4a9eff").pack()
        ctk.CTkLabel(logo_frame, text="AutoCare Pro", font=ctk.CTkFont(size=22, weight="bold"), text_color="#4a9eff").pack(pady=(5,0))
        ctk.CTkLabel(logo_frame, text="Chăm sóc xe chuyên nghiệp", font=ctk.CTkFont(size=11), text_color="#888888").pack()
        
        # Separator
        sep = ctk.CTkFrame(self.sidebar, height=2, fg_color="#2a2a3e")
        sep.pack(side="top", fill="x", padx=20, pady=15)
        
        # ========== PHẦN MENU ==========
        # Tạo một frame chứa menu để có thể scroll nếu cần
        menu_container = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent", scrollbar_button_color="#2a2a3e")
        menu_container.pack(side="top", fill="both", expand=True, padx=20, pady=0)
        
        menu_items = [
            ("📊 Dashboard", self.show_dashboard),
            ("👥 Khách hàng", self.show_khach_hang),
            ("🚘 Xe", self.show_xe),
            ("🔧 Dịch vụ", self.show_dich_vu),
            ("📄 Hóa đơn", self.show_hoa_don),
            ("📅 Đặt lịch", self.show_lich_hen),
            ("📈 Thống kê", self.show_thong_ke),
            ("⚙️ Cài đặt", self.show_settings),
        ]
        
        self.menu_buttons = {}
        for text, command in menu_items:
            btn = ctk.CTkButton(
                menu_container, 
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
            btn.pack(fill="x", pady=5)
            self.menu_buttons[text] = btn
        
        # ========== PHẦN DƯỚI CÙNG (USER + LOGOUT) ==========
        # Frame này luôn nằm dưới cùng
        bottom_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x", padx=15, pady=(0, 20))
        
        # User info card
        user_card = ctk.CTkFrame(bottom_frame, fg_color="#15152a", corner_radius=10)
        user_card.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(user_card, text="👤", font=ctk.CTkFont(size=35)).pack(pady=(10, 5))
        
        if self.current_user:
            ctk.CTkLabel(
                user_card, 
                text=self.current_user.get('ho_ten', 'Admin User'),
                font=ctk.CTkFont(size=13, weight="bold"), 
                text_color="#ffffff"
            ).pack()
            
            role_text = "Quản trị viên" if self.current_user.get('vai_tro') == 'admin' else "Nhân viên"
            ctk.CTkLabel(
                user_card, 
                text=role_text, 
                font=ctk.CTkFont(size=11), 
                text_color="#888888"
            ).pack(pady=(0, 10))
        else:
            ctk.CTkLabel(
                user_card, 
                text="Admin User", 
                font=ctk.CTkFont(size=13, weight="bold"), 
                text_color="#ffffff"
            ).pack(pady=(0, 10))
        
        # Nút Đăng xuất - Màu đỏ, rõ ràng
        logout_btn = ctk.CTkButton(
            bottom_frame,
            text="🚪 ĐĂNG XUẤT",
            command=self.logout,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            height=45,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        logout_btn.pack(fill="x", pady=(0, 0))
    
    def setup_header(self):
        self.header = ctk.CTkFrame(self.content_area, height=70, fg_color="#1a1a2e", corner_radius=0)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)
        self.header_title = ctk.CTkLabel(self.header, text="Dashboard",
            font=ctk.CTkFont(size=28, weight="bold"), text_color="#4a9eff")
        self.header_title.place(x=30, y=18)
        time_frame = ctk.CTkFrame(self.header, fg_color="#2a2a3e", corner_radius=10)
        time_frame.place(x=1100, y=18)
        self.time_label = ctk.CTkLabel(time_frame, text="", font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#4a9eff", padx=15, pady=8)
        self.time_label.pack()
        self.update_time()
    
    def update_time(self):
        if not self.root.winfo_exists(): return
        self.time_label.configure(text=datetime.now().strftime("%H:%M:%S • %d/%m/%Y"))
        self.after_id = self.root.after(1000, self.update_time)
    
    def clear_content(self):
        self.current_view = None
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
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=20)
        try:    total_kh = self.controllers['khach_hang'].model.get_total()
        except: total_kh = len(self.controllers['khach_hang'].get_all())
        total_xe = len(self.controllers['xe'].get_all())
        total_dv = len(self.controllers['dich_vu'].get_all())
        total_hd = len(self.controllers['hoa_don'].get_all())
        self.create_stat_card(stats_frame, "👥", "Khách hàng",      str(total_kh), "#4a9eff", 0)
        self.create_stat_card(stats_frame, "🚘", "Xe đang quản lý", str(total_xe), "#00c853", 1)
        self.create_stat_card(stats_frame, "🔧", "Dịch vụ",         str(total_dv), "#ff9800", 2)
        self.create_stat_card(stats_frame, "📄", "Hóa đơn",         str(total_hd), "#e91e63", 3)
        chart_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a2e", corner_radius=15)
        chart_frame.pack(fill="both", expand=True, pady=20)
        ctk.CTkLabel(chart_frame, text="📊 Doanh thu 7 ngày gần nhất", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        try:
            from_date = (datetime.now().date() - timedelta(days=7)).strftime("%Y-%m-%d")
            thong_ke  = self.controllers['hoa_don'].thong_ke(from_date, datetime.now().strftime("%Y-%m-%d"), include_all_status=True)
        except: thong_ke = []
        if thong_ke:
            cc = ctk.CTkFrame(chart_frame, fg_color="transparent")
            cc.pack(fill="both", expand=True, padx=20, pady=20)
            dates, revenues = [], []
            for s in thong_ke[:7]:
                ngay = s['ngay']
                dates.append(ngay.strftime("%d/%m") if isinstance(ngay,datetime) else str(ngay)[-5:])
                revenues.append(float(s['doanh_thu']))
            plt.style.use('dark_background')
            fig, ax = plt.subplots(figsize=(8,4), dpi=100)
            bars = ax.bar(dates, revenues, color='#4a9eff', alpha=0.8, edgecolor='white', linewidth=1)
            ax.set_title("Doanh thu 7 ngày gần nhất", fontsize=14, pad=15, color='white')
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"{int(x):,}"))
            ax.grid(True, linestyle='--', alpha=0.3)
            ax.set_facecolor('#1a1a2e'); fig.patch.set_facecolor('#1a1a2e')
            ax.spines['bottom'].set_color('#888888'); ax.spines['left'].set_color('#888888')
            ax.tick_params(colors='white')
            for bar,v in zip(bars,revenues):
                ax.text(bar.get_x()+bar.get_width()/2., bar.get_height(), f"{int(v):,}", ha='center', va='bottom', fontsize=9, color='white')
            plt.xticks(rotation=30)
            canvas = FigureCanvasTkAgg(fig, master=cc)
            canvas.draw(); canvas.get_tk_widget().pack(fill="both", expand=True)
        else:
            ctk.CTkLabel(chart_frame, text="📭 Chưa có dữ liệu doanh thu", font=ctk.CTkFont(size=14), text_color="#888888").pack(expand=True, pady=50)
    
    def create_stat_card(self, parent, icon, title, value, color, column):
        card = ctk.CTkFrame(parent, fg_color="#1a1a2e", corner_radius=15, height=130)
        card.pack(side="left", padx=10, fill="x", expand=True)
        icon_frame = ctk.CTkFrame(card, fg_color=color, corner_radius=12, width=50, height=50)
        icon_frame.pack_propagate(False); icon_frame.place(x=20, y=20)
        ctk.CTkLabel(icon_frame, text=icon, font=ctk.CTkFont(size=28), text_color="white").pack(expand=True)
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=12), text_color="#888888").place(x=85, y=30)
        ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=28, weight="bold"), text_color=color).place(x=85, y=60)
    
    # ==================== CÁC MÀN HÌNH ====================
    def show_khach_hang(self):
        self.clear_content()
        self.header_title.configure(text="Quản lý khách hàng")
        self.highlight_menu("👥 Khách hàng")
        self.current_view = ModernKhachHangView(self.content_frame, self.controllers['khach_hang'], on_refresh_callback=self.refresh_dashboard_stats)
        self.current_view.main_frame.pack(fill="both", expand=True)
    
    def show_xe(self):
        self.clear_content()
        self.header_title.configure(text="Quản lý xe")
        self.highlight_menu("🚘 Xe")
        self.current_view = ModernXeView(self.content_frame, self.controllers['xe'], self.controllers['khach_hang'], on_refresh_callback=self.refresh_dashboard_stats)
        self.current_view.main_frame.pack(fill="both", expand=True)
    
    def show_dich_vu(self):
        self.clear_content()
        self.header_title.configure(text="Quản lý dịch vụ")
        self.highlight_menu("🔧 Dịch vụ")
        self.current_view = ModernDichVuView(self.content_frame, self.controllers['dich_vu'])
        self.current_view.main_frame.pack(fill="both", expand=True)
    
    def show_hoa_don(self):
        self.clear_content()
        self.header_title.configure(text="Quản lý hóa đơn")
        self.highlight_menu("📄 Hóa đơn")
        self.current_view = ModernHoaDonView(self.content_frame, self.controllers['hoa_don'], self.controllers['xe'], self.controllers['dich_vu'])
        self.current_view.main_frame.pack(fill="both", expand=True)
    
    # ==================== ĐẶT LỊCH ✅ ====================
    def show_lich_hen(self):
        """Hiển thị giao diện quản lý đặt lịch hẹn"""
        self.clear_content()
        self.header_title.configure(text="Quản lý lịch hẹn")
        self.highlight_menu("📅 Đặt lịch")
        self.current_view = ModernDatLichView(
            self.content_frame,
            self.controllers['dat_lich'],
            self.controllers['khach_hang'],
            self.controllers['xe'],
            self.controllers['dich_vu'],
            on_refresh_callback=self.refresh_dashboard_stats
        )
        self.current_view.main_frame.pack(fill="both", expand=True)
    
    # ==================== THỐNG KÊ ====================
    def show_thong_ke(self):
        self.clear_content()
        self.header_title.configure(text="Thống kê & Báo cáo")
        self.highlight_menu("📈 Thống kê")
        
        # Main container
        main_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        # Filter frame
        filter_frame = ctk.CTkFrame(main_container, fg_color="#1a1a2e", corner_radius=15)
        filter_frame.pack(fill="x", pady=(0, 20), padx=0)
        
        ctk.CTkLabel(filter_frame, text="🔍 BỘ LỌC THỐNG KÊ", 
                    font=ctk.CTkFont(size=18, weight="bold"), text_color="#4a9eff").pack(pady=15)
        
        filter_row = ctk.CTkFrame(filter_frame, fg_color="transparent")
        filter_row.pack(pady=10, padx=20)
        
        ctk.CTkLabel(filter_row, text="Trạng thái:", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=10)
        
        status_filter_var = ctk.StringVar(value="all")
        status_buttons_frame = ctk.CTkFrame(filter_row, fg_color="transparent")
        status_buttons_frame.pack(side="left", padx=10)
        
        status_options = [
            ("📊 Tất cả", "all"),
            ("✅ Hoàn thành", "hoan_thanh"),
            ("🟡 Đang xử lý", "dang_xu_ly"),
            ("🔴 Đã hủy", "da_huy")
        ]
        
        for text, value in status_options:
            rb = ctk.CTkRadioButton(
                status_buttons_frame, text=text, variable=status_filter_var, value=value,
                font=ctk.CTkFont(size=13)
            )
            rb.pack(side="left", padx=15)
        
        # Scrollable container for stats
        stats_scroll = ctk.CTkScrollableFrame(main_container, fg_color="transparent")
        stats_scroll.pack(fill="both", expand=True)
        
        # Container cho dữ liệu thống kê
        self.thong_ke_container = ctk.CTkFrame(stats_scroll, fg_color="transparent")
        self.thong_ke_container.pack(fill="both", expand=True)
        
        # Hàm reload dữ liệu
        def reload_stats():
            self.load_thong_ke_data(self.thong_ke_container, status_filter_var)
        
        # Gán command cho các radio button
        for text, value in status_options:
            # Tìm và gán command
            for child in status_buttons_frame.winfo_children():
                if isinstance(child, ctk.CTkRadioButton) and child.cget("text") == text:
                    child.configure(command=reload_stats)
        
        # Load dữ liệu lần đầu
        self.load_thong_ke_data(self.thong_ke_container, status_filter_var)

    def load_thong_ke_data(self, container, status_filter_var):
        """Tải dữ liệu thống kê"""
        # Xóa nội dung cũ
        for widget in container.winfo_children():
            widget.destroy()
        
        # ========== PHẦN 1: THỐNG KÊ DOANH THU THEO THÁNG ==========
        monthly_frame = ctk.CTkFrame(container, fg_color="#1a1a2e", corner_radius=15)
        monthly_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        # Tiêu đề
        title_frame = ctk.CTkFrame(monthly_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=15, padx=20)
        
        ctk.CTkLabel(title_frame, text="📊 THỐNG KÊ DOANH THU THEO THÁNG", 
                    font=ctk.CTkFont(size=18, weight="bold"), text_color="#4a9eff").pack(side="left")
        
        # Separator
        ctk.CTkFrame(monthly_frame, height=2, fg_color="#2a2a3e").pack(fill="x", padx=20)
        
        # Lấy dữ liệu
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        sf = status_filter_var.get()
        
        try:
            if sf == "all":
                rows = self.controllers['hoa_don'].model.db.fetch_all(
                    "SELECT ngay_lap, tong_tien FROM hoa_don WHERE ngay_lap BETWEEN %s AND %s",
                    (start_date, end_date)
                )
            else:
                rows = self.controllers['hoa_don'].model.db.fetch_all(
                    "SELECT ngay_lap, tong_tien FROM hoa_don WHERE trang_thai=%s AND ngay_lap BETWEEN %s AND %s",
                    (sf, start_date, end_date)
                )
        except Exception as e:
            print(f"Lỗi lấy dữ liệu: {e}")
            rows = []
        
        # Nhóm dữ liệu theo tháng
        monthly_data = {}
        for r in rows:
            ngay = r.get("ngay_lap")
            tien = float(r.get("tong_tien") or 0)
            
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
                monthly_data[month_key] = {"count": 0, "revenue": 0}
            monthly_data[month_key]["count"] += 1
            monthly_data[month_key]["revenue"] += tien
        
        if monthly_data:
            # Bảng dữ liệu
            table_frame = ctk.CTkFrame(monthly_frame, fg_color="transparent")
            table_frame.pack(fill="both", expand=True, padx=20, pady=15)
            
            # Tạo Treeview với style đẹp
            scrollbar = ttk.Scrollbar(table_frame)
            scrollbar.pack(side="right", fill="y")
            
            columns = ("Tháng", "Số hóa đơn", "Doanh thu", "Trung bình")
            tree = ttk.Treeview(table_frame, columns=columns, show="headings", 
                            yscrollcommand=scrollbar.set, height=8)
            
            # Style cho Treeview
            style = ttk.Style()
            style.configure("Treeview", background="#1a1a2e", foreground="white", 
                        fieldbackground="#1a1a2e", rowheight=35)
            style.configure("Treeview.Heading", background="#2a2a3e", foreground="#4a9eff", 
                        font=('Arial', 11, 'bold'))
            style.map('Treeview', background=[('selected', '#4a9eff')])
            
            # Cấu hình cột
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center", width=200)
            
            scrollbar.config(command=tree.yview)
            
            # Thêm dữ liệu vào bảng
            sorted_months = sorted(monthly_data.items(), key=lambda x: datetime.strptime(x[0], "%m/%Y"), reverse=True)
            for month, data in sorted_months:
                avg = data["revenue"] / data["count"] if data["count"] else 0
                tree.insert("", "end", values=(
                    month,
                    data["count"],
                    f"{data['revenue']:,.0f} VNĐ",
                    f"{avg:,.0f} VNĐ"
                ))
            
            tree.pack(side="left", fill="both", expand=True)
            
            # Tổng kết
            total_rev = sum(m["revenue"] for m in monthly_data.values())
            total_inv = sum(m["count"] for m in monthly_data.values())
            avg_rev = total_rev / total_inv if total_inv else 0
            
            summary_frame = ctk.CTkFrame(monthly_frame, fg_color="#2a2a3e", corner_radius=10)
            summary_frame.pack(fill="x", padx=20, pady=(0, 15))
            
            summary_text = f"📊 Tổng số hóa đơn: {total_inv}  |  💰 Tổng doanh thu: {total_rev:,.0f} VNĐ  |  📈 Trung bình/hóa đơn: {avg_rev:,.0f} VNĐ"
            ctk.CTkLabel(summary_frame, text=summary_text, 
                        font=ctk.CTkFont(size=13, weight="bold"), 
                        text_color="#4a9eff", padx=15, pady=12).pack()
        else:
            ctk.CTkLabel(monthly_frame, text="📭 Không có dữ liệu thống kê", 
                        font=ctk.CTkFont(size=14), text_color="#888888").pack(pady=50)
        
        # ========== PHẦN 2: TOP DỊCH VỤ ĐƯỢC SỬ DỤNG NHIỀU NHẤT ==========
        top_frame = ctk.CTkFrame(container, fg_color="#1a1a2e", corner_radius=15)
        top_frame.pack(fill="x", pady=(0, 10), padx=10)
        
        # Tiêu đề
        title_frame2 = ctk.CTkFrame(top_frame, fg_color="transparent")
        title_frame2.pack(fill="x", pady=15, padx=20)
        
        ctk.CTkLabel(title_frame2, text="🏆 TOP DỊCH VỤ ĐƯỢC SỬ DỤNG NHIỀU NHẤT", 
                    font=ctk.CTkFont(size=18, weight="bold"), text_color="#ff9800").pack(side="left")
        
        # Separator
        ctk.CTkFrame(top_frame, height=2, fg_color="#2a2a3e").pack(fill="x", padx=20)
        
        try:
            top_services = self.controllers['hoa_don'].model.db.fetch_all("""
                SELECT dv.ten_dich_vu, 
                    COUNT(DISTINCT ct.id_hoa_don) as so_lan_su_dung,
                    SUM(ct.so_luong) as tong_so_luong, 
                    SUM(ct.thanh_tien) as tong_doanh_thu
                FROM chi_tiet_hoa_don ct
                JOIN dich_vu dv ON ct.id_dich_vu = dv.id
                GROUP BY ct.id_dich_vu
                ORDER BY so_lan_su_dung DESC
                LIMIT 5
            """)
            
            if top_services:
                # Bảng top dịch vụ
                table_frame2 = ctk.CTkFrame(top_frame, fg_color="transparent")
                table_frame2.pack(fill="both", expand=True, padx=20, pady=15)
                
                scrollbar2 = ttk.Scrollbar(table_frame2)
                scrollbar2.pack(side="right", fill="y")
                
                columns2 = ("Tên dịch vụ", "Số lần sử dụng", "Tổng số lượng", "Doanh thu")
                tree2 = ttk.Treeview(table_frame2, columns=columns2, show="headings", 
                                    yscrollcommand=scrollbar2.set, height=5)
                
                # Style cho Treeview
                style2 = ttk.Style()
                style2.configure("Treeview2.Treeview", background="#1a1a2e", foreground="white", 
                                fieldbackground="#1a1a2e", rowheight=35)
                style2.configure("Treeview2.Heading", background="#2a2a3e", foreground="#ff9800", 
                                font=('Arial', 11, 'bold'))
                
                for col in columns2:
                    tree2.heading(col, text=col)
                    if col == "Tên dịch vụ":
                        tree2.column(col, anchor="w", width=250)
                    else:
                        tree2.column(col, anchor="center", width=150)
                
                scrollbar2.config(command=tree2.yview)
                
                # Thêm dữ liệu
                for s in top_services:
                    tree2.insert("", "end", values=(
                        s.get("ten_dich_vu", "N/A"),
                        s.get("so_lan_su_dung", 0),
                        s.get("tong_so_luong", 0),
                        f"{s.get('tong_doanh_thu', 0):,.0f} VNĐ"
                    ))
                
                tree2.pack(side="left", fill="both", expand=True)
            else:
                empty_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
                empty_frame.pack(fill="both", expand=True, pady=40)
                ctk.CTkLabel(empty_frame, text="📭 Chưa có dữ liệu dịch vụ", 
                            font=ctk.CTkFont(size=14), text_color="#888888").pack()
        except Exception as e:
            error_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
            error_frame.pack(fill="both", expand=True, pady=40)
            ctk.CTkLabel(error_frame, text=f"⚠️ Lỗi tải dữ liệu: {str(e)}", 
                        font=ctk.CTkFont(size=14), text_color="#ff5252").pack()
    
    # ==================== CÀI ĐẶT ====================
    def show_settings(self):
        self.clear_content()
        self.header_title.configure(text="Cài đặt hệ thống")
        self.highlight_menu("⚙️ Cài đặt")
        theme_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a2e", corner_radius=15)
        theme_frame.pack(fill="x", pady=20, padx=20)
        ctk.CTkLabel(theme_frame, text="🎨 Giao diện", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        theme_var = ctk.StringVar(value="dark")
        def change_theme(): ctk.set_appearance_mode(theme_var.get())
        ctk.CTkRadioButton(theme_frame, text="🌙 Dark Mode",  variable=theme_var, value="dark",  command=change_theme).pack(pady=10)
        ctk.CTkRadioButton(theme_frame, text="☀️ Light Mode", variable=theme_var, value="light", command=change_theme).pack(pady=10)
        db_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a2e", corner_radius=15)
        db_frame.pack(fill="x", pady=20, padx=20)
        ctk.CTkLabel(db_frame, text="💾 Dữ liệu", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        ctk.CTkButton(db_frame, text="📦 Sao lưu dữ liệu", command=self.backup_database, fg_color="#4a9eff", height=40, width=200, corner_radius=8).pack(pady=10)
        info_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a2e", corner_radius=15)
        info_frame.pack(fill="x", pady=20, padx=20)
        ctk.CTkLabel(info_frame, text="ℹ️ Thông tin hệ thống", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        ctk.CTkLabel(info_frame, text="AutoCare Pro - Phần mềm quản lý dịch vụ chăm sóc xe ô tô\nPhiên bản 2.0\n© 2024",
            font=ctk.CTkFont(size=12), text_color="#888888", justify="center").pack(pady=20)
    
    def backup_database(self):
        import subprocess, os
        backup_dir = "backup"
        if not os.path.exists(backup_dir): os.makedirs(backup_dir)
        backup_file = f"{backup_dir}/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
        try:
            subprocess.run(f'mysqldump -u root quan_ly_dich_vu_xe > "{backup_file}"', shell=True, check=True)
            messagebox.showinfo("Thành công", f"Sao lưu thành công tại: {backup_file}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Sao lưu thất bại: {str(e)}\nVui lòng sao lưu thủ công từ phpMyAdmin")
    
    def refresh_dashboard_stats(self):
        if self.header_title.cget("text") == "Dashboard":
            self.show_dashboard()
    
    def logout(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            if self.after_id: self.root.after_cancel(self.after_id)
            self.root.destroy()
            def start_app(user):
                from controller.khach_hang_controller import KhachHangController
                from controller.xe_controller import XeController
                from controller.dich_vu_controller import DichVuController
                from controller.hoa_don_controller import HoaDonController
                from controller.dat_lich_controller import DatLichController
                controllers = {
                    'khach_hang': KhachHangController(), 'xe': XeController(),
                    'dich_vu': DichVuController(),       'hoa_don': HoaDonController(),
                    'dat_lich': DatLichController(),      'user': user
                }
                ModernMainView(controllers)
            LoginView(start_app)
    
    def on_closing(self):
        if messagebox.askyesno("Thoát", "Bạn có chắc muốn thoát chương trình?"):
            if self.after_id: self.root.after_cancel(self.after_id)
            self.root.destroy()