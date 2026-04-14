import customtkinter as ctk
from tkinter import messagebox
import customtkinter as ctk
from tkinter import messagebox, ttk  # Thêm ttk

class ModernDichVuView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Thiết lập giao diện quản lý dịch vụ"""
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)
        
        self.setup_toolbar()
        self.setup_table()
        self.setup_form()
    
    def setup_toolbar(self):
        """Thanh công cụ"""
        toolbar = ctk.CTkFrame(self.main_frame, fg_color="#1f1f1f", corner_radius=10)
        toolbar.pack(fill="x", pady=(0, 20))
        
        self.add_btn = ctk.CTkButton(
            toolbar,
            text="➕ Thêm dịch vụ",
            command=self.show_add_form,
            fg_color="#4a9eff",
            height=40,
            corner_radius=10
        )
        self.add_btn.pack(side="left", padx=10, pady=10)
        
        search_frame = ctk.CTkFrame(toolbar, fg_color="#2b2b2b", corner_radius=10)
        search_frame.pack(side="right", padx=10, pady=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Tìm kiếm dịch vụ...",
            width=300,
            height=40
        )
        self.search_entry.pack(side="left", padx=10)
        
        self.search_btn = ctk.CTkButton(
            search_frame,
            text="Tìm kiếm",
            command=self.search,
            width=100,
            height=40
        )
        self.search_btn.pack(side="right", padx=10)
        
        refresh_btn = ctk.CTkButton(
            toolbar,
            text="🔄 Làm mới",
            command=self.load_data,
            fg_color="#757575",
            height=40,
            width=100
        )
        refresh_btn.pack(side="right", padx=10, pady=10)
    
    def setup_table(self):
        """Bảng hiển thị dịch vụ"""
        self.table_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="#1f1f1f",
            corner_radius=10,
            height=500
        )
        self.table_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        headers = ["ID", "Mã DV", "Tên dịch vụ", "Đơn giá", "Thời gian", "Mô tả", "Thao tác"]
        column_widths = [50, 100, 200, 150, 100, 200, 100]
        
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
    
    def load_data(self):
        """Tải danh sách dịch vụ"""
        for row in self.table_rows:
            for widget in row:
                widget.destroy()
        self.table_rows.clear()
        
        dich_vus = self.controller.get_all()
        
        for row_idx, dv in enumerate(dich_vus, start=2):
            row_widgets = []
            
            # ID
            id_label = ctk.CTkLabel(self.table_frame, text=str(dv['id']))
            id_label.grid(row=row_idx, column=0, padx=5, pady=8, sticky="w")
            row_widgets.append(id_label)
            
            # Mã DV
            ma_label = ctk.CTkLabel(self.table_frame, text=dv['ma_dv'])
            ma_label.grid(row=row_idx, column=1, padx=5, pady=8, sticky="w")
            row_widgets.append(ma_label)
            
            # Tên dịch vụ
            ten_label = ctk.CTkLabel(
                self.table_frame,
                text=dv['ten_dich_vu'],
                font=ctk.CTkFont(size=13, weight="bold")
            )
            ten_label.grid(row=row_idx, column=2, padx=5, pady=8, sticky="w")
            row_widgets.append(ten_label)
            
            # Đơn giá
            don_gia_label = ctk.CTkLabel(
                self.table_frame,
                text=f"{dv['don_gia']:,.0f} VNĐ",
                text_color="#00c853"
            )
            don_gia_label.grid(row=row_idx, column=3, padx=5, pady=8, sticky="w")
            row_widgets.append(don_gia_label)
            
            # Thời gian
            thoi_gian_label = ctk.CTkLabel(
                self.table_frame,
                text=f"{dv['thoi_gian_du_kien']} phút" if dv['thoi_gian_du_kien'] else "—"
            )
            thoi_gian_label.grid(row=row_idx, column=4, padx=5, pady=8, sticky="w")
            row_widgets.append(thoi_gian_label)
            
            # Mô tả
            mo_ta_label = ctk.CTkLabel(
                self.table_frame,
                text=dv['mo_ta'] or "—",
                wraplength=180
            )
            mo_ta_label.grid(row=row_idx, column=5, padx=5, pady=8, sticky="w")
            row_widgets.append(mo_ta_label)
            
            # Thao tác
            action_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
            action_frame.grid(row=row_idx, column=6, padx=5, pady=5)
            
            edit_btn = ctk.CTkButton(
                action_frame,
                text="✏️",
                width=35,
                height=35,
                fg_color="#ff9800",
                corner_radius=8,
                command=lambda d=dv: self.show_edit_form(d)
            )
            edit_btn.pack(side="left", padx=2)
            
            delete_btn = ctk.CTkButton(
                action_frame,
                text="🗑️",
                width=35,
                height=35,
                fg_color="#d32f2f",
                corner_radius=8,
                command=lambda d=dv: self.delete_service(d['id'])
            )
            delete_btn.pack(side="left", padx=2)
            
            row_widgets.append(action_frame)
            self.table_rows.append(row_widgets)
    
    def setup_form(self):
        """Form nhập liệu dịch vụ"""
        self.form_frame = ctk.CTkFrame(self.main_frame, fg_color="#1f1f1f", corner_radius=15)
        
        self.form_title = ctk.CTkLabel(
            self.form_frame,
            text="Thông tin dịch vụ",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.form_title.pack(pady=20)
        
        form_fields = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        form_fields.pack(pady=20, padx=40)
        
        self.form_entries = {}
        fields = [
            ("Mã dịch vụ *", "ma_dv"),
            ("Tên dịch vụ *", "ten_dich_vu"),
            ("Đơn giá *", "don_gia"),
            ("Thời gian (phút)", "thoi_gian"),
            ("Mô tả", "mo_ta")
        ]
        
        for i, (label, key) in enumerate(fields):
            frame = ctk.CTkFrame(form_fields, fg_color="transparent")
            frame.pack(fill="x", pady=10)
            
            lbl = ctk.CTkLabel(frame, text=label, width=120, font=ctk.CTkFont(size=14))
            lbl.pack(side="left")
            
            entry = ctk.CTkEntry(frame, width=350, height=40, font=ctk.CTkFont(size=14))
            entry.pack(side="right")
            self.form_entries[key] = entry
        
        btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        self.save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Lưu lại",
            command=self.save_service,
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
        
        self.current_service_id = None
    
    def show_add_form(self):
        """Hiển thị form thêm dịch vụ"""
        print("Đang hiển thị form thêm dịch vụ")
        
        # Xóa dữ liệu cũ
        for entry in self.form_entries.values():
            entry.delete(0, 'end')
        
        self.current_service_id = None
        self.form_title.configure(text="➕ Thêm dịch vụ mới")
        
        # Ẩn table frame
        self.table_frame.pack_forget()
        
        # Hiển thị form
        self.form_frame.pack(fill="x", pady=(0, 20))
        self.form_frame.lift()
        
        # Cập nhật UI
        self.main_frame.update_idletasks()

    def hide_form(self):
        """Ẩn form và hiện lại bảng"""
        print("Đang ẩn form")
        self.form_frame.pack_forget()
        self.table_frame.pack(fill="both", expand=True, pady=(0, 20))
    
    def show_edit_form(self, service):
        """Hiển thị form sửa dịch vụ"""
        self.current_service_id = service['id']
        self.form_entries['ma_dv'].delete(0, 'end')
        self.form_entries['ma_dv'].insert(0, service['ma_dv'])
        self.form_entries['ten_dich_vu'].delete(0, 'end')
        self.form_entries['ten_dich_vu'].insert(0, service['ten_dich_vu'])
        self.form_entries['don_gia'].delete(0, 'end')
        self.form_entries['don_gia'].insert(0, str(service['don_gia']))
        self.form_entries['thoi_gian'].delete(0, 'end')
        self.form_entries['thoi_gian'].insert(0, str(service['thoi_gian_du_kien']) if service['thoi_gian_du_kien'] else "")
        self.form_entries['mo_ta'].delete(0, 'end')
        self.form_entries['mo_ta'].insert(0, service['mo_ta'] or "")
        
        self.form_title.configure(text="✏️ Sửa thông tin dịch vụ")
        self.form_frame.pack(fill="x", pady=(20, 0))
        self.form_frame.lift()
    
    def hide_form(self):
        """Ẩn form"""
        self.form_frame.pack_forget()
    
    def save_service(self):
        """Lưu dịch vụ"""
        ma_dv = self.form_entries['ma_dv'].get().strip()
        ten_dv = self.form_entries['ten_dich_vu'].get().strip()
        don_gia_str = self.form_entries['don_gia'].get().strip()
        thoi_gian_str = self.form_entries['thoi_gian'].get().strip()
        mo_ta = self.form_entries['mo_ta'].get().strip()
        
        print(f"Đang lưu dịch vụ: {ma_dv}, {ten_dv}, {don_gia_str}, {thoi_gian_str}, {mo_ta}")
        
        if not ma_dv or not ten_dv or not don_gia_str:
            messagebox.showerror("Lỗi", "Mã DV, tên DV và đơn giá không được để trống")
            return
        
        try:
            don_gia = float(don_gia_str)
            thoi_gian = int(thoi_gian_str) if thoi_gian_str else None
        except ValueError:
            messagebox.showerror("Lỗi", "Đơn giá phải là số, thời gian phải là số nguyên")
            return
        
        if self.current_service_id:  # Update
            result = self.controller.update(self.current_service_id, ma_dv, ten_dv, don_gia, thoi_gian, mo_ta)
            print(f"Kết quả update: {result}")
            if result:
                messagebox.showinfo("Thành công", "Cập nhật dịch vụ thành công")
                self.hide_form()
                self.load_data()
            else:
                messagebox.showerror("Lỗi", "Cập nhật thất bại")
        else:  # Insert
            result = self.controller.add(ma_dv, ten_dv, don_gia, thoi_gian, mo_ta)
            print(f"Kết quả insert: {result}")
            if result:
                messagebox.showinfo("Thành công", "Thêm dịch vụ thành công")
                self.hide_form()
                self.load_data()
            else:
                messagebox.showerror("Lỗi", "Thêm dịch vụ thất bại\nMã dịch vụ có thể đã tồn tại")
    
    def delete_service(self, service_id):
        """Xóa dịch vụ"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa dịch vụ này?"):
            if self.controller.delete(service_id):
                messagebox.showinfo("Thành công", "Xóa dịch vụ thành công")
                self.load_data()
            else:
                messagebox.showerror("Lỗi", "Xóa dịch vụ thất bại")
    
    def search(self):
        """Tìm kiếm dịch vụ"""
        keyword = self.search_entry.get().strip()
        if keyword:
            results = self.controller.search(keyword)
            messagebox.showinfo("Kết quả", f"Tìm thấy {len(results)} dịch vụ")