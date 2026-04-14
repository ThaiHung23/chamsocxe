import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox, ttk  # Thêm ttk
from datetime import datetime

class ModernKhachHangView:
    def __init__(self, parent, controller, on_refresh_callback=None):
        self.parent = parent
        self.controller = controller
        self.on_refresh = on_refresh_callback
        self.current_page = 1
        self.items_per_page = 20
        self.total_items = 0
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Thiết lập giao diện quản lý khách hàng"""
        
        # Frame chính
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)
        
        # Thanh công cụ
        self.setup_toolbar()
        
        # Bảng dữ liệu
        self.setup_table()
        
        # Phân trang
        self.setup_pagination()
        
        # Form nhập liệu (ẩn ban đầu)
        self.setup_form()
    
    def setup_toolbar(self):
        """Thanh công cụ với các nút chức năng"""
        toolbar = ctk.CTkFrame(self.main_frame, fg_color="#1f1f1f", corner_radius=10)
        toolbar.pack(fill="x", pady=(0, 20))
        
        # Nút thêm
        self.add_btn = ctk.CTkButton(
            toolbar,
            text="➕ Thêm khách hàng",
            command=self.show_add_form,
            fg_color="#4a9eff",
            hover_color="#357ae8",
            height=40,
            corner_radius=10
        )
        self.add_btn.pack(side="left", padx=10, pady=10)
        
        # Nút xuất Excel
        export_btn = ctk.CTkButton(
            toolbar,
            text="📊 Xuất Excel",
            command=self.export_to_excel,
            fg_color="#00c853",
            hover_color="#00a844",
            height=40,
            corner_radius=10
        )
        export_btn.pack(side="left", padx=5, pady=10)
        
        # Nút xuất PDF
        pdf_btn = ctk.CTkButton(
            toolbar,
            text="📄 Xuất PDF",
            command=self.export_to_pdf,
            fg_color="#ff9800",
            hover_color="#f57c00",
            height=40,
            corner_radius=10
        )
        pdf_btn.pack(side="left", padx=5, pady=10)
        
        # Ô tìm kiếm
        search_frame = ctk.CTkFrame(toolbar, fg_color="#2b2b2b", corner_radius=10)
        search_frame.pack(side="right", padx=10, pady=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Tìm kiếm theo tên, SĐT, mã KH...",
            width=350,
            height=40,
            font=ctk.CTkFont(size=13)
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
        refresh_btn.pack(side="right", padx=10, pady=10)
    
    def setup_table(self):
        """Bảng hiển thị dữ liệu"""
        
        # Frame chứa bảng
        self.table_frame = ctk.CTkScrollableFrame(
            self.main_frame, 
            fg_color="#1f1f1f", 
            corner_radius=10,
            height=500
        )
        self.table_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Header bảng
        headers = ["ID", "Mã KH", "Họ tên", "Số điện thoại", "Email", "Địa chỉ", "Ngày tạo", "Thao tác"]
        self.column_widths = [50, 100, 150, 120, 180, 200, 120, 100]
        
        for i, (header, width) in enumerate(zip(headers, self.column_widths)):
            header_label = ctk.CTkLabel(
                self.table_frame,
                text=header,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#4a9eff",
                width=width
            )
            header_label.grid(row=0, column=i, padx=5, pady=10, sticky="w")
        
        # Line separator
        separator = ctk.CTkFrame(self.table_frame, height=2, fg_color="#4a9eff")
        separator.grid(row=1, column=0, columnspan=len(headers), sticky="ew", pady=(0, 10))
        
        self.table_rows = []
    
    def load_data(self):
        """Tải dữ liệu từ database"""
        # Xóa dữ liệu cũ
        for row in self.table_rows:
            for widget in row:
                widget.destroy()
        self.table_rows.clear()
        
        # Lấy dữ liệu
        offset = (self.current_page - 1) * self.items_per_page
        all_data = self.controller.get_all()
        self.total_items = len(all_data)
        
        # Phân trang
        start = offset
        end = min(offset + self.items_per_page, self.total_items)
        page_data = all_data[start:end]
        
        # Hiển thị dữ liệu
        for row_idx, kh in enumerate(page_data, start=2):
            row_widgets = []
            
            # ID
            id_label = ctk.CTkLabel(
                self.table_frame,
                text=str(kh['id']),
                font=ctk.CTkFont(size=13)
            )
            id_label.grid(row=row_idx, column=0, padx=5, pady=8, sticky="w")
            row_widgets.append(id_label)
            
            # Mã KH
            ma_label = ctk.CTkLabel(
                self.table_frame,
                text=kh['ma_kh'],
                font=ctk.CTkFont(size=13)
            )
            ma_label.grid(row=row_idx, column=1, padx=5, pady=8, sticky="w")
            row_widgets.append(ma_label)
            
            # Họ tên
            ten_label = ctk.CTkLabel(
                self.table_frame,
                text=kh['ho_ten'],
                font=ctk.CTkFont(size=13, weight="bold")
            )
            ten_label.grid(row=row_idx, column=2, padx=5, pady=8, sticky="w")
            row_widgets.append(ten_label)
            
            # SĐT
            sdt_label = ctk.CTkLabel(
                self.table_frame,
                text=kh['so_dien_thoai'],
                font=ctk.CTkFont(size=13)
            )
            sdt_label.grid(row=row_idx, column=3, padx=5, pady=8, sticky="w")
            row_widgets.append(sdt_label)
            
            # Email
            email_text = kh['email'] if kh['email'] else "—"
            email_label = ctk.CTkLabel(
                self.table_frame,
                text=email_text,
                font=ctk.CTkFont(size=12),
                text_color="#888888"
            )
            email_label.grid(row=row_idx, column=4, padx=5, pady=8, sticky="w")
            row_widgets.append(email_label)
            
            # Địa chỉ
            diachi_text = kh['dia_chi'] if kh['dia_chi'] else "—"
            diachi_label = ctk.CTkLabel(
                self.table_frame,
                text=diachi_text,
                font=ctk.CTkFont(size=12),
                wraplength=180
            )
            diachi_label.grid(row=row_idx, column=5, padx=5, pady=8, sticky="w")
            row_widgets.append(diachi_label)
            
            # Ngày tạo
            ngay_tao = kh['ngay_tao'].strftime("%d/%m/%Y") if kh['ngay_tao'] else "—"
            ngay_label = ctk.CTkLabel(
                self.table_frame,
                text=ngay_tao,
                font=ctk.CTkFont(size=12)
            )
            ngay_label.grid(row=row_idx, column=6, padx=5, pady=8, sticky="w")
            row_widgets.append(ngay_label)
            
            # Nút thao tác
            action_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
            action_frame.grid(row=row_idx, column=7, padx=5, pady=5)
            
            edit_btn = ctk.CTkButton(
                action_frame,
                text="✏️",
                width=35,
                height=35,
                fg_color="#ff9800",
                hover_color="#f57c00",
                corner_radius=8,
                command=lambda k=kh: self.show_edit_form(k)
            )
            edit_btn.pack(side="left", padx=2)
            
            delete_btn = ctk.CTkButton(
                action_frame,
                text="🗑️",
                width=35,
                height=35,
                fg_color="#d32f2f",
                hover_color="#b71c1c",
                corner_radius=8,
                command=lambda k=kh: self.delete_customer(k['id'])
            )
            delete_btn.pack(side="left", padx=2)
            
            view_xe_btn = ctk.CTkButton(
                action_frame,
                text="🚘",
                width=35,
                height=35,
                fg_color="#2196f3",
                hover_color="#1976d2",
                corner_radius=8,
                command=lambda k=kh: self.view_customer_cars(k)
            )
            view_xe_btn.pack(side="left", padx=2)
            
            row_widgets.append(action_frame)
            self.table_rows.append(row_widgets)
        
        # Cập nhật phân trang
        self.update_pagination_info()
    
    def setup_pagination(self):
        """Phân trang"""
        self.pagination_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.pagination_frame.pack(fill="x", pady=10)
        
        self.page_label = ctk.CTkLabel(
            self.pagination_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.page_label.pack(side="left", padx=10)
        
        btn_frame = ctk.CTkFrame(self.pagination_frame, fg_color="transparent")
        btn_frame.pack(side="right")
        
        self.prev_btn = ctk.CTkButton(
            btn_frame,
            text="◀ Trước",
            command=self.prev_page,
            width=100,
            height=30,
            corner_radius=8
        )
        self.prev_btn.pack(side="left", padx=5)
        
        self.next_btn = ctk.CTkButton(
            btn_frame,
            text="Sau ▶",
            command=self.next_page,
            width=100,
            height=30,
            corner_radius=8
        )
        self.next_btn.pack(side="left", padx=5)
    
    def update_pagination_info(self):
        """Cập nhật thông tin phân trang"""
        total_pages = (self.total_items + self.items_per_page - 1) // self.items_per_page
        self.page_label.configure(
            text=f"Hiển thị {min(1 + (self.current_page-1)*self.items_per_page, self.total_items)} - "
                 f"{min(self.current_page*self.items_per_page, self.total_items)} / {self.total_items} khách hàng"
        )
        
        # Enable/disable buttons
        self.prev_btn.configure(state="normal" if self.current_page > 1 else "disabled")
        self.next_btn.configure(state="normal" if self.current_page < total_pages else "disabled")
    
    def prev_page(self):
        """Trang trước"""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_data()
    
    def next_page(self):
        """Trang sau"""
        total_pages = (self.total_items + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_data()
    
    def setup_form(self):
        """Form nhập liệu (ẩn ban đầu)"""
        self.form_frame = ctk.CTkFrame(self.main_frame, fg_color="#1f1f1f", corner_radius=15)
        
        # Title
        self.form_title = ctk.CTkLabel(
            self.form_frame,
            text="Thông tin khách hàng",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.form_title.pack(pady=20)
        
        # Form fields
        form_fields = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        form_fields.pack(pady=20, padx=40)
        
        self.form_entries = {}
        fields = [
            ("Họ tên *", "ho_ten"),
            ("Số điện thoại *", "so_dien_thoai"),
            ("Email", "email"),
            ("Địa chỉ", "dia_chi")
        ]
        
        for i, (label, key) in enumerate(fields):
            frame = ctk.CTkFrame(form_fields, fg_color="transparent")
            frame.pack(fill="x", pady=10)
            
            lbl = ctk.CTkLabel(frame, text=label, width=120, font=ctk.CTkFont(size=14))
            lbl.pack(side="left")
            
            entry = ctk.CTkEntry(frame, width=350, height=40, font=ctk.CTkFont(size=14))
            entry.pack(side="right")
            self.form_entries[key] = entry
        
        # Buttons
        btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        self.save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Lưu lại",
            command=self.save_customer,
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
        
        self.current_customer_id = None
    
    def show_add_form(self):
        """Hiển thị form thêm khách hàng"""
        print("Đang hiển thị form thêm khách hàng")
        
        # Xóa dữ liệu cũ
        for entry in self.form_entries.values():
            entry.delete(0, 'end')
        
        self.current_customer_id = None
        self.form_title.configure(text="➕ Thêm khách hàng mới")
        
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
    
    def show_edit_form(self, customer):
        """Hiển thị form sửa"""
        self.current_customer_id = customer['id']
        self.form_entries['ho_ten'].delete(0, 'end')
        self.form_entries['ho_ten'].insert(0, customer['ho_ten'])
        self.form_entries['so_dien_thoai'].delete(0, 'end')
        self.form_entries['so_dien_thoai'].insert(0, customer['so_dien_thoai'])
        self.form_entries['email'].delete(0, 'end')
        self.form_entries['email'].insert(0, customer['email'] or "")
        self.form_entries['dia_chi'].delete(0, 'end')
        self.form_entries['dia_chi'].insert(0, customer['dia_chi'] or "")
        
        self.form_title.configure(text="✏️ Sửa thông tin khách hàng")
        self.form_frame.pack(fill="x", pady=(20, 0))
        self.form_frame.lift()
    
    def hide_form(self):
        """Ẩn form"""
        self.form_frame.pack_forget()
    
    def save_customer(self):
        """Lưu khách hàng"""
        ho_ten = self.form_entries['ho_ten'].get().strip()
        sdt = self.form_entries['so_dien_thoai'].get().strip()
        email = self.form_entries['email'].get().strip()
        dia_chi = self.form_entries['dia_chi'].get().strip()
        
        print(f"Đang lưu khách hàng: {ho_ten}, {sdt}, {email}, {dia_chi}")
        
        if not ho_ten or not sdt:
            messagebox.showerror("Lỗi", "Họ tên và số điện thoại không được để trống")
            return
        
        if self.current_customer_id:  # Update
            result = self.controller.update(self.current_customer_id, ho_ten, sdt, email, dia_chi)
            print(f"Kết quả update: {result}")
            if result:
                messagebox.showinfo("Thành công", "Cập nhật khách hàng thành công")
                self.hide_form()
                self.load_data()
                if self.on_refresh:
                    self.on_refresh()
            else:
                messagebox.showerror("Lỗi", "Cập nhật thất bại")
        else:  # Insert
            result = self.controller.add(ho_ten, sdt, email, dia_chi)
            print(f"Kết quả insert: {result}")
            if result:
                messagebox.showinfo("Thành công", "Thêm khách hàng thành công")
                self.hide_form()
                self.load_data()
                if self.on_refresh:
                    self.on_refresh()
            else:
                messagebox.showerror("Lỗi", "Thêm khách hàng thất bại\nKiểm tra lại thông tin và kết nối database")
    
    def delete_customer(self, customer_id):
        """Xóa khách hàng"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa khách hàng này?\nLưu ý: Sẽ xóa luôn các xe của khách hàng!"):
            if self.controller.delete(customer_id):
                messagebox.showinfo("Thành công", "Xóa khách hàng thành công")
                self.load_data()
                if self.on_refresh:
                    self.on_refresh()
            else:
                messagebox.showerror("Lỗi", "Xóa khách hàng thất bại")
    
    def search(self):
        """Tìm kiếm khách hàng"""
        keyword = self.search_entry.get().strip()
        if keyword:
            results = self.controller.search(keyword)
            
            # Xóa dữ liệu cũ
            for row in self.table_rows:
                for widget in row:
                    widget.destroy()
            self.table_rows.clear()
            
            # Hiển thị kết quả
            for row_idx, kh in enumerate(results, start=2):
                # ... (tương tự như load_data)
                pass
            
            messagebox.showinfo("Kết quả", f"Tìm thấy {len(results)} khách hàng")
    
    def export_to_excel(self):
        """Xuất danh sách ra Excel"""
        try:
            from utils.excel_export import ExcelExporter
            data = self.controller.get_all()
            filename = f"khach_hang_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            ExcelExporter.export_khach_hang(data, filename)
            messagebox.showinfo("Thành công", f"Đã xuất file: {filename}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Xuất Excel thất bại: {str(e)}")
    
    def export_to_pdf(self):
        """Xuất danh sách ra PDF"""
        try:
            from utils.pdf_export import PDFExporter
            data = self.controller.get_all()
            filename = f"khach_hang_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            PDFExporter.export_khach_hang(data, filename)
            messagebox.showinfo("Thành công", f"Đã xuất file: {filename}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Xuất PDF thất bại: {str(e)}")
    
    def view_customer_cars(self, customer):
        """Xem danh sách xe của khách hàng"""
        # Tạo dialog hiển thị xe
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title(f"Danh sách xe của {customer['ho_ten']}")
        dialog.geometry("800x500")
        dialog.grab_set()
        
        # TODO: Lấy danh sách xe từ controller
        messagebox.showinfo("Thông tin", "Tính năng đang phát triển")