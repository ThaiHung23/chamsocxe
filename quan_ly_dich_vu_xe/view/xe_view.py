import customtkinter as ctk
from tkinter import messagebox, ttk

class ModernXeView:
    def __init__(self, parent, controller, khach_hang_controller, on_refresh_callback=None):
        self.parent = parent
        self.controller = controller
        self.khach_hang_controller = khach_hang_controller
        self.on_refresh = on_refresh_callback
        
        # Biến quản lý trạng thái
        self.current_car_id = None
        self.all_cars_data = []  # Lưu trữ dữ liệu gốc để search/filter
        
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        """Khởi tạo giao diện chính"""
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # 1. Toolbar (Tìm kiếm & Nút thêm)
        self.setup_toolbar()

        # 2. Container nội dung (Chứa Bảng hoặc Form)
        self.content_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True)

        self.setup_table()
        self.setup_form()

    def setup_toolbar(self):
        toolbar = ctk.CTkFrame(self.main_frame, fg_color="#1f1f1f", corner_radius=10)
        toolbar.pack(fill="x", pady=(0, 15))

        # Nhóm bên trái: Thêm mới
        left_f = ctk.CTkFrame(toolbar, fg_color="transparent")
        left_f.pack(side="left", padx=10, pady=10)
        
        ctk.CTkButton(left_f, text="➕ Thêm xe mới", command=self.show_add_form,
                      fg_color="#4a9eff", hover_color="#357ae8", height=38).pack(side="left", padx=5)
        
        ctk.CTkButton(left_f, text="🔄 Làm mới", command=self.load_data,
                      fg_color="#757575", width=100, height=38).pack(side="left", padx=5)

        # Nhóm bên phải: Tìm kiếm
        search_f = ctk.CTkFrame(toolbar, fg_color="#2b2b2b", corner_radius=8)
        search_f.pack(side="right", padx=10)

        self.search_entry = ctk.CTkEntry(search_f, placeholder_text="Biển số, Hiệu xe...", width=250, border_width=0)
        self.search_entry.pack(side="left", padx=10, pady=5)
        self.search_entry.bind("<Return>", lambda e: self.search())

        ctk.CTkButton(search_f, text="Tìm kiếm", command=self.search, width=80, height=30).pack(side="left", padx=5)

    def setup_table(self):
        """Bảng hiển thị xe sử dụng CTkScrollableFrame để hiển thị tốt hơn"""
        self.table_frame = ctk.CTkScrollableFrame(self.content_container, fg_color="#1f1f1f", corner_radius=10)
        self.table_frame.pack(fill="both", expand=True)

        headers = ["ID", "Biển số", "Hiệu xe", "Model", "Màu sắc", "Năm SX", "Chủ xe", "Thao tác"]
        # Tỉ lệ chiều rộng các cột
        self.col_widths = [50, 110, 130, 110, 90, 80, 140, 120]

        for i, (header, width) in enumerate(zip(headers, self.col_widths)):
            lbl = ctk.CTkLabel(self.table_frame, text=header, font=ctk.CTkFont(size=13, weight="bold"),
                               text_color="#4a9eff", width=width, anchor="w")
            lbl.grid(row=0, column=i, padx=10, pady=12)

        self.rows_widgets = []

    def setup_form(self):
        """Form nhập liệu - Ẩn mặc định"""
        self.form_frame = ctk.CTkFrame(self.content_container, fg_color="#1f1f1f", corner_radius=15)
        
        self.form_title = ctk.CTkLabel(self.form_frame, text="Thông tin xe", font=ctk.CTkFont(size=20, weight="bold"))
        self.form_title.pack(pady=20)

        fields = [
            ("Biển số *", "bien_so"), ("Hiệu xe *", "hieu_xe"), 
            ("Model", "model"), ("Màu sắc", "mau_sac"), 
            ("Năm SX", "nam_sx"), ("ID Chủ xe *", "id_khach_hang")
        ]
        
        self.entries = {}
        for label, key in fields:
            f = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            f.pack(fill="x", padx=100, pady=8)
            ctk.CTkLabel(f, text=label, width=120, anchor="w").pack(side="left")
            entry = ctk.CTkEntry(f, width=300, height=35)
            entry.pack(side="left", padx=10)
            self.entries[key] = entry

        # Nút chức năng Form
        btn_f = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        btn_f.pack(pady=30)
        ctk.CTkButton(btn_f, text="💾 Lưu xe", command=self.save_car, fg_color="#00c853", width=120).pack(side="left", padx=10)
        ctk.CTkButton(btn_f, text="❌ Hủy", command=self.hide_form, fg_color="#d32f2f", width=120).pack(side="left", padx=10)

    # --- HÀM LOGIC XỬ LÝ DỮ LIỆU ---

    def render_table(self, data_list):
        """Vẽ lại bảng dữ liệu"""
        # Xóa các widget cũ
        for widgets in self.rows_widgets:
            for w in widgets: w.destroy()
        self.rows_widgets.clear()

        for i, xe in enumerate(data_list, start=1):
            current_row = []
            display_data = [
                xe['id'], xe['bien_so'], xe['hieu_xe'], 
                xe.get('model', '—'), xe.get('mau_sac', '—'),
                xe.get('nam_sx', '—'), xe.get('ten_chu_xe', 'N/A')
            ]

            for col, text in enumerate(display_data):
                color = "#ff9800" if col == 1 else "white" # Highlight biển số
                l = ctk.CTkLabel(self.table_frame, text=str(text), text_color=color, width=self.col_widths[col], anchor="w")
                l.grid(row=i, column=col, padx=10, pady=8)
                current_row.append(l)

            # Cột thao tác
            act_f = ctk.CTkFrame(self.table_frame, fg_color="transparent")
            act_f.grid(row=i, column=7, padx=5)
            
            ctk.CTkButton(act_f, text="✏️", width=35, fg_color="#ff9800", command=lambda x=xe: self.show_edit_form(x)).pack(side="left", padx=2)
            ctk.CTkButton(act_f, text="🗑️", width=35, fg_color="#d32f2f", command=lambda x=xe: self.delete_car(x['id'])).pack(side="left", padx=2)
            
            current_row.append(act_f)
            self.rows_widgets.append(current_row)

    def load_data(self):
        """Tải dữ liệu từ database"""
        self.all_cars_data = self.controller.get_all()
        self.render_table(self.all_cars_data)

    def search(self):
        """Tìm kiếm (Sửa lỗi không tìm kiếm được)"""
        kw = self.search_entry.get().strip().lower()
        if not kw:
            self.load_data()
            return
        
        # Gọi controller tìm kiếm
        results = self.controller.search(kw)
        self.render_table(results)
        if not results:
            messagebox.showinfo("Kết quả", "Không tìm thấy xe phù hợp")

    def delete_car(self, car_id):
        """Xóa xe (Sửa lỗi không xóa được)"""
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa xe ID: {car_id}?"):
            # CHÚ Ý: Đảm bảo controller.delete nhận tham số là INT
            success = self.controller.delete(int(car_id))
            if success:
                messagebox.showinfo("Thành công", "Đã xóa xe khỏi hệ thống")
                self.load_data() # Load lại bảng ngay lập tức
                if self.on_refresh: self.on_refresh()
            else:
                messagebox.showerror("Lỗi", "Không thể xóa. Xe này có thể đang liên quan đến hóa đơn.")

    def save_car(self):
        """Lưu hoặc cập nhật xe"""
        data = {k: v.get().strip() for k, v in self.entries.items()}
        
        if not data['bien_so'] or not data['hieu_xe'] or not data['id_khach_hang']:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đủ các trường có dấu *")
            return

        try:
            if self.current_car_id:
                success = self.controller.update(self.current_car_id, **data)
            else:
                success = self.controller.add(**data)
            
            if success:
                messagebox.showinfo("Thành công", "Dữ liệu xe đã được lưu")
                self.hide_form()
                self.load_data()
            else:
                messagebox.showerror("Lỗi", "Lỗi thực thi Database")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Sai định dạng dữ liệu: {e}")

    # --- ĐIỀU KHIỂN HIỂN THỊ ---

    def show_add_form(self):
        self.current_car_id = None
        self.form_title.configure(text="➕ THÊM XE MỚI")
        for e in self.entries.values(): e.delete(0, 'end')
        self.table_frame.pack_forget()
        self.form_frame.pack(fill="both", expand=True)

    def show_edit_form(self, xe):
        self.current_car_id = xe['id']
        self.form_title.configure(text="✏️ SỬA THÔNG TIN XE")
        for key in self.entries.keys():
            self.entries[key].delete(0, 'end')
            val = xe.get(key, "")
            self.entries[key].insert(0, str(val) if val is not None else "")
        self.table_frame.pack_forget()
        self.form_frame.pack(fill="both", expand=True)

    def hide_form(self):
        self.form_frame.pack_forget()
        self.table_frame.pack(fill="both", expand=True)