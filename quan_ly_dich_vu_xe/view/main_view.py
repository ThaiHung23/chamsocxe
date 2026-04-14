import tkinter as tk
from tkinter import ttk, messagebox
from .khach_hang_view import KhachHangView
from .xe_view import XeView
from .dich_vu_view import DichVuView
from .hoa_don_view import HoaDonView

class MainView:
    def __init__(self, controllers):
        self.controllers = controllers
        self.root = tk.Tk()
        self.root.title("Phần mềm quản lý dịch vụ chăm sóc xe ô tô")
        self.root.geometry("1200x700")
        
        # Tạo notebook (tab)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Khởi tạo các tab
        self.khach_hang_view = KhachHangView(self.notebook, controllers['khach_hang'])
        self.xe_view = XeView(self.notebook, controllers['xe'])
        self.dich_vu_view = DichVuView(self.notebook, controllers['dich_vu'])
        self.hoa_don_view = HoaDonView(self.notebook, controllers['hoa_don'])
        
        # Thêm các tab vào notebook
        self.notebook.add(self.khach_hang_view, text="Quản lý khách hàng")
        self.notebook.add(self.xe_view, text="Quản lý xe")
        self.notebook.add(self.dich_vu_view, text="Quản lý dịch vụ")
        self.notebook.add(self.hoa_don_view, text="Quản lý hóa đơn")
        
        # Menu bar
        self.create_menu()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Thống kê", command=self.show_thong_ke)
        file_menu.add_separator()
        file_menu.add_command(label="Thoát", command=self.on_closing)
        
        # Menu Help
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Trợ giúp", menu=help_menu)
        help_menu.add_command(label="Hướng dẫn", command=self.show_help)
        help_menu.add_command(label="Thông tin", command=self.show_about)
    
    def show_thong_ke(self):
        from tkinter import Toplevel
        from datetime import datetime, timedelta
        
        thong_ke_window = Toplevel(self.root)
        thong_ke_window.title("Thống kê doanh thu")
        thong_ke_window.geometry("800x500")
        
        # Frame chọn ngày
        frame_date = ttk.Frame(thong_ke_window)
        frame_date.pack(pady=10)
        
        ttk.Label(frame_date, text="Từ ngày:").grid(row=0, column=0, padx=5)
        from_date = ttk.Entry(frame_date, width=15)
        from_date.grid(row=0, column=1, padx=5)
        from_date.insert(0, (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        
        ttk.Label(frame_date, text="Đến ngày:").grid(row=0, column=2, padx=5)
        to_date = ttk.Entry(frame_date, width=15)
        to_date.grid(row=0, column=3, padx=5)
        to_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Treeview hiển thị thống kê
        columns = ("Ngày", "Số lượng hóa đơn", "Doanh thu")
        tree = ttk.Treeview(thong_ke_window, columns=columns, show="headings", height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        def load_thong_ke():
            # Xóa dữ liệu cũ
            for item in tree.get_children():
                tree.delete(item)
            
            # Lấy dữ liệu thống kê
            stats = self.controllers['hoa_don'].thong_ke(from_date.get(), to_date.get())
            for stat in stats:
                tree.insert("", "end", values=(
                    stat['ngay'],
                    stat['so_luong'],
                    f"{stat['doanh_thu']:,.0f} VNĐ"
                ))
        
        ttk.Button(frame_date, text="Xem thống kê", command=load_thong_ke).grid(row=0, column=4, padx=10)
        load_thong_ke()
    
    def show_help(self):
        messagebox.showinfo("Hướng dẫn", 
            "1. Quản lý khách hàng: Thêm, sửa, xóa, tìm kiếm khách hàng\n"
            "2. Quản lý xe: Đăng ký xe cho khách hàng\n"
            "3. Quản lý dịch vụ: Tạo các dịch vụ chăm sóc xe\n"
            "4. Quản lý hóa đơn: Tạo hóa đơn dịch vụ cho xe")
    
    def show_about(self):
        messagebox.showinfo("Thông tin", 
            "Phần mềm quản lý dịch vụ chăm sóc xe ô tô\n"
            "Phiên bản 1.0\n"
            "© 2024 - Dự án học tập")
    
    def on_closing(self):
        if messagebox.askokcancel("Thoát", "Bạn có chắc muốn thoát chương trình?"):
            self.root.destroy()