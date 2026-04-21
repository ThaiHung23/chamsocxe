import customtkinter as ctk
from tkinter import messagebox, ttk

class ModernXeView:
    def __init__(self, parent, controller, khach_hang_controller, on_refresh_callback=None):
        self.parent = parent
        self.controller = controller
        self.khach_hang_controller = khach_hang_controller
        self.on_refresh = on_refresh_callback
        self.current_page = 1
        self.items_per_page = 20
        self.current_car_id = None
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Thiết lập giao diện quản lý xe"""
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)
        
        self.setup_toolbar()
        self.setup_table()
        self.setup_form()  # Tạo form nhưng chưa hiển thị
    
    def setup_toolbar(self):
        """Thanh công cụ"""
        toolbar = ctk.CTkFrame(self.main_frame, fg_color="#1f1f1f", corner_radius=10)
        toolbar.pack(fill="x", pady=(0, 20))
        
        # Nút thêm
        self.add_btn = ctk.CTkButton(
            toolbar,
            text="➕ Thêm xe mới",
            command=self.show_add_form,
            fg_color="#4a9eff",
            hover_color="#357ae8",
            height=40,
            corner_radius=10
        )
        self.add_btn.pack(side="left", padx=10, pady=10)
        
        # Nút làm mới
        refresh_btn = ctk.CTkButton(
            toolbar,
            text="🔄 Làm mới",
            command=self.load_data,
            fg_color="#757575",
            hover_color="#616161",
            height=40,
            width=100,
            corner_radius=10
        )
        refresh_btn.pack(side="left", padx=5, pady=10)
        
        # Ô tìm kiếm
        search_frame = ctk.CTkFrame(toolbar, fg_color="#2b2b2b", corner_radius=10)
        search_frame.pack(side="right", padx=10, pady=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Tìm kiếm theo biển số, hiệu xe...",
            width=300,
            height=40
        )
        self.search_entry.pack(side="left", padx=10)
        
        self.search_btn = ctk.CTkButton(
            search_frame,
            text="Tìm kiếm",
            command=self.search,
            width=100,
            height=40,
            corner_radius=10
        )
        self.search_btn.pack(side="right", padx=10)
    
    def setup_table(self):
        """Bảng hiển thị xe"""
        # Frame chứa bảng và form
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)
        
        # Table frame
        self.table_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="#1f1f1f",
            corner_radius=10,
            height=450
        )
        self.table_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Header
        headers = ["ID", "Biển số", "Hiệu xe", "Model", "Màu sắc", "Năm SX", "Chủ xe", "Thao tác"]
        column_widths = [50, 120, 150, 120, 100, 80, 150, 100]
        
        for i, (header, width) in enumerate(zip(headers, column_widths)):
            header_label = ctk.CTkLabel(
                self.table_frame,
                text=header,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#4a9eff",
                width=width
            )
            header_label.grid(row=0, column=i, padx=5, pady=10, sticky="w")
        
        separator = ctk.CTkFrame(self.table_frame, height=2, fg_color="#4a9eff")
        separator.grid(row=1, column=0, columnspan=len(headers), sticky="ew", pady=(0, 10))
        
        self.table_rows = []
    
    def setup_form(self):
        """Form nhập liệu xe - ẨN ban đầu"""
        self.form_frame = ctk.CTkFrame(self.content_frame, fg_color="#1f1f1f", corner_radius=15)
        # KHÔNG pack ngay, để ẩn
        
        self.form_title = ctk.CTkLabel(
            self.form_frame,
            text="Thông tin xe",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.form_title.pack(pady=20)
        
        form_fields = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        form_fields.pack(pady=20, padx=40)
        
        self.form_entries = {}
        fields = [
            ("Biển số *", "bien_so"),
            ("Hiệu xe *", "hieu_xe"),
            ("Model", "model"),
            ("Màu sắc", "mau_sac"),
            ("Năm sản xuất", "nam_sx"),
            ("ID Khách hàng *", "id_khach_hang")
        ]
        
        for i, (label, key) in enumerate(fields):
            frame = ctk.CTkFrame(form_fields, fg_color="transparent")
            frame.pack(fill="x", pady=10)
            
            lbl = ctk.CTkLabel(frame, text=label, width=120, font=ctk.CTkFont(size=14))
            lbl.pack(side="left")
            
            entry = ctk.CTkEntry(frame, width=350, height=40, font=ctk.CTkFont(size=14))
            entry.pack(side="right")
            self.form_entries[key] = entry
        
        # Nút chọn khách hàng
        select_kh_btn = ctk.CTkButton(
            form_fields,
            text="📋 Chọn từ danh sách khách hàng",
            command=self.select_customer,
            fg_color="#2196f3",
            height=35
        )
        select_kh_btn.pack(pady=10)
        
        # Buttons
        btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        self.save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Lưu lại",
            command=self.save_car,
            fg_color="#4a9eff",
            height=40,
            width=120,
            corner_radius=10
        )
        self.save_btn.pack(side="left", padx=10)
        
        self.cancel_btn = ctk.CTkButton(
            btn_frame,
            text="❌ Hủy bỏ",
            command=self.hide_form,
            fg_color="#757575",
            height=40,
            width=120,
            corner_radius=10
        )
        self.cancel_btn.pack(side="left", padx=10)
    
    def show_add_form(self):
        """Hiển thị form thêm xe"""
        print("Đang hiển thị form thêm xe")
        
        # Xóa dữ liệu cũ
        for entry in self.form_entries.values():
            entry.delete(0, 'end')
        
        self.current_car_id = None
        self.form_title.configure(text="➕ Thêm xe mới")
        
        # Ẩn table frame
        self.table_frame.pack_forget()
        
        # Hiển thị form
        self.form_frame.pack(fill="x", pady=(0, 20))
        self.form_frame.lift()
        
        # Cập nhật UI
        self.main_frame.update_idletasks()
    
    def show_edit_form(self, car):
        """Hiển thị form sửa xe"""
        print(f"Đang hiển thị form sửa xe ID: {car['id']}")
        
        self.current_car_id = car['id']
        self.form_entries['bien_so'].delete(0, 'end')
        self.form_entries['bien_so'].insert(0, car['bien_so'])
        self.form_entries['hieu_xe'].delete(0, 'end')
        self.form_entries['hieu_xe'].insert(0, car['hieu_xe'])
        self.form_entries['model'].delete(0, 'end')
        self.form_entries['model'].insert(0, car['model'] or "")
        self.form_entries['mau_sac'].delete(0, 'end')
        self.form_entries['mau_sac'].insert(0, car['mau_sac'] or "")
        self.form_entries['nam_sx'].delete(0, 'end')
        self.form_entries['nam_sx'].insert(0, str(car['nam_sx']) if car['nam_sx'] else "")
        self.form_entries['id_khach_hang'].delete(0, 'end')
        self.form_entries['id_khach_hang'].insert(0, str(car['id_khach_hang']))
        
        self.form_title.configure(text="✏️ Sửa thông tin xe")
        
        # Ẩn table frame
        self.table_frame.pack_forget()
        
        # Hiển thị form
        self.form_frame.pack(fill="x", pady=(0, 20))
        self.form_frame.lift()
    
    def hide_form(self):
        """Ẩn form và hiện lại bảng"""
        print("Đang ẩn form")
        self.form_frame.pack_forget()
        self.table_frame.pack(fill="both", expand=True, pady=(0, 20))
    
    def load_data(self):
        """Tải danh sách xe"""
        # Xóa dữ liệu cũ
        for row in self.table_rows:
            for widget in row:
                widget.destroy()
        self.table_rows.clear()
        
        # Lấy dữ liệu
        xe_list = self.controller.get_all()
        print(f"Đã tải {len(xe_list)} xe")
        
        for row_idx, xe in enumerate(xe_list, start=2):
            row_widgets = []
            
            # ID
            id_label = ctk.CTkLabel(self.table_frame, text=str(xe['id']))
            id_label.grid(row=row_idx, column=0, padx=5, pady=8, sticky="w")
            row_widgets.append(id_label)
            
            # Biển số
            bien_so_label = ctk.CTkLabel(
                self.table_frame,
                text=xe['bien_so'],
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#ff9800"
            )
            bien_so_label.grid(row=row_idx, column=1, padx=5, pady=8, sticky="w")
            row_widgets.append(bien_so_label)
            
            # Hiệu xe
            hieu_xe_label = ctk.CTkLabel(self.table_frame, text=xe['hieu_xe'])
            hieu_xe_label.grid(row=row_idx, column=2, padx=5, pady=8, sticky="w")
            row_widgets.append(hieu_xe_label)
            
            # Model
            model_label = ctk.CTkLabel(self.table_frame, text=xe['model'] or "—")
            model_label.grid(row=row_idx, column=3, padx=5, pady=8, sticky="w")
            row_widgets.append(model_label)
            
            # Màu sắc
            mau_label = ctk.CTkLabel(self.table_frame, text=xe['mau_sac'] or "—")
            mau_label.grid(row=row_idx, column=4, padx=5, pady=8, sticky="w")
            row_widgets.append(mau_label)
            
            # Năm SX
            nam_label = ctk.CTkLabel(self.table_frame, text=str(xe['nam_sx']) if xe['nam_sx'] else "—")
            nam_label.grid(row=row_idx, column=5, padx=5, pady=8, sticky="w")
            row_widgets.append(nam_label)
            
            # Chủ xe
            chu_xe_label = ctk.CTkLabel(self.table_frame, text=xe.get('ten_chu_xe', 'N/A'))
            chu_xe_label.grid(row=row_idx, column=6, padx=5, pady=8, sticky="w")
            row_widgets.append(chu_xe_label)
            
            # Thao tác
            action_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
            action_frame.grid(row=row_idx, column=7, padx=5, pady=5)
            
            edit_btn = ctk.CTkButton(
                action_frame,
                text="✏️",
                width=35,
                height=35,
                fg_color="#ff9800",
                corner_radius=8,
                command=lambda x=xe: self.show_edit_form(x)
            )
            edit_btn.pack(side="left", padx=2)
            
            delete_btn = ctk.CTkButton(
                action_frame,
                text="🗑️",
                width=35,
                height=35,
                fg_color="#d32f2f",
                corner_radius=8,
                command=lambda x=xe: self.delete_car(x['id'])
            )
            delete_btn.pack(side="left", padx=2)
            
            row_widgets.append(action_frame)
            self.table_rows.append(row_widgets)
    
    def select_customer(self):
        """Mở dialog chọn khách hàng"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Chọn khách hàng")
        dialog.geometry("600x500")
        dialog.grab_set()
        
        # Lấy danh sách khách hàng
        customers = self.khach_hang_controller.get_all()
        
        main_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        label = ctk.CTkLabel(
            main_frame,
            text="Chọn khách hàng chủ xe:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label.pack(pady=10)
        
        # Treeview
        tree_frame = ctk.CTkFrame(main_frame, fg_color="#1f1f1f", corner_radius=10)
        tree_frame.pack(fill="both", expand=True, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=("ID", "Mã", "Tên", "SĐT"), show="headings", height=15)
        
        tree.heading("ID", text="ID")
        tree.heading("Mã", text="Mã KH")
        tree.heading("Tên", text="Họ tên")
        tree.heading("SĐT", text="Số điện thoại")
        
        tree.column("ID", width=50)
        tree.column("Mã", width=100)
        tree.column("Tên", width=200)
        tree.column("SĐT", width=120)
        
        for kh in customers:
            tree.insert("", "end", values=(kh['id'], kh['ma_kh'], kh['ho_ten'], kh['so_dien_thoai']))
        
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        def select():
            selected = tree.selection()
            if selected:
                values = tree.item(selected[0])['values']
                self.form_entries['id_khach_hang'].delete(0, 'end')
                self.form_entries['id_khach_hang'].insert(0, values[0])
                dialog.destroy()
        
        select_btn = ctk.CTkButton(
            main_frame,
            text="Chọn",
            command=select,
            fg_color="#4a9eff",
            height=40,
            width=150
        )
        select_btn.pack(pady=10)
    
    def save_car(self):
        """Lưu thông tin xe"""
        bien_so = self.form_entries['bien_so'].get().strip()
        hieu_xe = self.form_entries['hieu_xe'].get().strip()
        model = self.form_entries['model'].get().strip()
        mau_sac = self.form_entries['mau_sac'].get().strip()
        nam_sx_str = self.form_entries['nam_sx'].get().strip()
        id_kh_str = self.form_entries['id_khach_hang'].get().strip()
        
        print(f"Đang lưu xe: {bien_so}, {hieu_xe}, {id_kh_str}")
        
        if not bien_so or not hieu_xe or not id_kh_str:
            messagebox.showerror("Lỗi", "Biển số, hiệu xe và ID khách hàng không được để trống")
            return
        
        try:
            nam_sx = int(nam_sx_str) if nam_sx_str else 0
            id_kh = int(id_kh_str)
        except ValueError:
            messagebox.showerror("Lỗi", "Năm sản xuất và ID khách hàng phải là số")
            return
        
        # Kiểm tra khách hàng
        check_kh = self.khach_hang_controller.get_by_id(id_kh)
        if not check_kh:
            messagebox.showerror("Lỗi", f"Không tìm thấy khách hàng với ID = {id_kh}")
            return
        
        if self.current_car_id:  # Update
            result = self.controller.update(self.current_car_id, bien_so, hieu_xe, model, mau_sac, nam_sx, id_kh)
            if result:
                messagebox.showinfo("Thành công", "Cập nhật xe thành công")
                self.hide_form()
                self.load_data()
                if self.on_refresh:
                    self.on_refresh()
            else:
                messagebox.showerror("Lỗi", "Cập nhật thất bại")
        else:  # Insert
            result = self.controller.add(bien_so, hieu_xe, model, mau_sac, nam_sx, id_kh)
            if result:
                messagebox.showinfo("Thành công", "Thêm xe thành công")
                self.hide_form()
                self.load_data()
                if self.on_refresh:
                    self.on_refresh()
            else:
                messagebox.showerror("Lỗi", "Thêm xe thất bại\nKiểm tra lại biển số (có thể đã tồn tại)")
    
    def delete_car(self, car_id):
        """Xóa xe"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa xe này?"):
            if self.controller.delete(car_id):
                messagebox.showinfo("Thành công", "Xóa xe thành công")
                self.load_data()
                if self.on_refresh:
                    self.on_refresh()
            else:
                messagebox.showerror("Lỗi", "Xóa xe thất bại")
    
    def search(self):
        """Tìm kiếm xe"""
        keyword = self.search_entry.get().strip()
        if keyword:
            results = self.controller.search(keyword)
            messagebox.showinfo("Kết quả", f"Tìm thấy {len(results)} xe")
            # Có thể hiển thị kết quả tìm kiếm ở đây