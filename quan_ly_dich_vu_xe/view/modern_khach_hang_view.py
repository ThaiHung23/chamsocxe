import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime

class ModernKhachHangView:
    def __init__(self, parent, controller, on_refresh_callback=None):
        self.parent = parent
        self.controller = controller
        self.on_refresh = on_refresh_callback
        
        # Cấu hình phân trang
        self.current_page = 1
        self.items_per_page = 20
        self.total_items = 0
        self.current_data = []
        
        # Biến tạm lưu khách hàng đang sửa
        self.current_customer_id = None
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Thiết lập cấu trúc giao diện phân tầng"""
        # Frame chính chứa tất cả
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 1. Thanh công cụ phía trên
        self.setup_toolbar()
        
        # 2. Container trung tâm (Nơi hoán đổi Table và Form)
        self.content_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True)
        
        self.setup_table()
        self.setup_form()
        
        # 3. Thanh phân trang phía dưới
        self.setup_pagination()

    def setup_toolbar(self):
        """Thanh công cụ với tìm kiếm và các nút chức năng"""
        toolbar = ctk.CTkFrame(self.main_frame, fg_color="#1f1f1f", corner_radius=10)
        toolbar.pack(fill="x", pady=(0, 10))
        
        # Nhóm nút bên trái
        left_btns = ctk.CTkFrame(toolbar, fg_color="transparent")
        left_btns.pack(side="left", padx=10, pady=10)
        
        self.add_btn = ctk.CTkButton(left_btns, text="➕ Thêm khách hàng", command=self.show_add_form,
                                    fg_color="#4a9eff", hover_color="#357ae8", height=35)
        self.add_btn.pack(side="left", padx=5)
        
        ctk.CTkButton(left_btns, text="📊 Excel", command=self.export_to_excel, 
                      fg_color="#00c853", width=80, height=35).pack(side="left", padx=5)
        
        ctk.CTkButton(left_btns, text="📄 PDF", command=self.export_to_pdf, 
                      fg_color="#ff9800", width=80, height=35).pack(side="left", padx=5)

        # Nhóm tìm kiếm bên phải
        search_frame = ctk.CTkFrame(toolbar, fg_color="#2b2b2b", corner_radius=8)
        search_frame.pack(side="right", padx=10)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Tên, SĐT, Mã...", width=250, border_width=0)
        self.search_entry.pack(side="left", padx=10, pady=5)
        self.search_entry.bind("<Return>", lambda e: self.search())
        
        ctk.CTkButton(search_frame, text="Tìm kiếm", command=self.search, width=80, height=30).pack(side="left", padx=5)
        
        ctk.CTkButton(toolbar, text="🔄", command=self.load_data, width=40, height=35, 
                      fg_color="#757575").pack(side="right", padx=5)

    def setup_table(self):
        """Khởi tạo cấu trúc bảng hiển thị dữ liệu"""
        self.table_frame = ctk.CTkScrollableFrame(self.content_container, fg_color="#1f1f1f", corner_radius=10)
        self.table_frame.pack(fill="both", expand=True)
        
        self.headers = ["ID", "Mã KH", "Họ tên", "Số điện thoại", "Email", "Địa chỉ", "Ngày tạo", "Thao tác"]
        self.column_widths = [20, 120, 120, 110, 180, 200, 105, 130]
        
        for i, (header, width) in enumerate(zip(self.headers, self.column_widths)):
            lbl = ctk.CTkLabel(self.table_frame, text=header, font=ctk.CTkFont(size=13, weight="bold"),
                               text_color="#4a9eff", width=width, anchor="w")
            lbl.grid(row=0, column=i, padx=10, pady=12)
            
        self.table_rows = []

    def setup_form(self):
        """Khởi tạo Form nhập liệu"""
        self.form_frame = ctk.CTkFrame(self.content_container, fg_color="#1f1f1f", corner_radius=15)
        
        self.form_title = ctk.CTkLabel(self.form_frame, text="Thông tin khách hàng", font=ctk.CTkFont(size=22, weight="bold"))
        self.form_title.pack(pady=30)

        self.form_entries = {}
        fields = [("Họ tên *", "ho_ten"), ("Số điện thoại *", "so_dien_thoai"), ("Email", "email"), ("Địa chỉ", "dia_chi")]
        
        for label, key in fields:
            row_f = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            row_f.pack(fill="x", pady=10, padx=100)
            
            ctk.CTkLabel(row_f, text=label, width=150, anchor="w", font=ctk.CTkFont(size=14)).pack(side="left")
            entry = ctk.CTkEntry(row_f, width=400, height=40)
            entry.pack(side="left", padx=10)
            self.form_entries[key] = entry

        btn_f = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        btn_f.pack(pady=40)
        
        ctk.CTkButton(btn_f, text="💾 Lưu dữ liệu", command=self.save_customer, 
                      fg_color="#00c853", hover_color="#00a844", width=150, height=45).pack(side="left", padx=15)
        ctk.CTkButton(btn_f, text="❌ Hủy bỏ", command=self.hide_form, 
                      fg_color="#d32f2f", hover_color="#b71c1c", width=150, height=45).pack(side="left", padx=15)

    def show_add_form(self):
        self.current_customer_id = None
        self.form_title.configure(text="➕ THÊM KHÁCH HÀNG MỚI")
        for entry in self.form_entries.values():
            entry.delete(0, 'end')
        
        self.table_frame.pack_forget()
        self.pagination_frame.pack_forget()
        self.form_frame.pack(fill="both", expand=True)

    def show_edit_form(self, customer):
        self.current_customer_id = customer['id']
        self.form_title.configure(text="✏️ CHỈNH SỬA THÔNG TIN")
        
        for key in ['ho_ten', 'so_dien_thoai', 'email', 'dia_chi']:
            self.form_entries[key].delete(0, 'end')
            val = customer.get(key, "")
            self.form_entries[key].insert(0, str(val) if val else "")

        self.table_frame.pack_forget()
        self.pagination_frame.pack_forget()
        self.form_frame.pack(fill="both", expand=True)

    def hide_form(self):
        """Quay lại bảng dữ liệu"""
        self.form_frame.pack_forget()
        self.table_frame.pack(fill="both", expand=True)
        self.pagination_frame.pack(fill="x", pady=10)

    def render_table(self, data_list):
        """Hàm dùng chung để vẽ dữ liệu lên bảng"""
        # Xóa các dòng cũ
        for row in self.table_rows:
            for widget in row:
                widget.destroy()
        self.table_rows.clear()
        
        self.total_items = len(data_list)
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        page_data = data_list[start:end]

        for i, kh in enumerate(page_data, start=1):
            widgets = []
            
            # Xử lý ngày tháng
            date_str = kh['ngay_tao'].strftime("%d/%m/%Y") if isinstance(kh['ngay_tao'], datetime) else str(kh['ngay_tao'])
            
            display_values = [
                kh['id'], kh['ma_kh'], kh['ho_ten'], kh['so_dien_thoai'],
                kh['email'] if kh['email'] else "—",
                kh['dia_chi'] if kh['dia_chi'] else "—",
                date_str
            ]
            
            for col, text in enumerate(display_values):
                l = ctk.CTkLabel(self.table_frame, text=str(text), font=ctk.CTkFont(size=13))
                l.grid(row=i, column=col, padx=10, pady=8, sticky="w")
                widgets.append(l)

            # Nút thao tác
            act_f = ctk.CTkFrame(self.table_frame, fg_color="transparent")
            act_f.grid(row=i, column=7, padx=5, pady=5)
            
            ctk.CTkButton(act_f, text="✏️", width=35, fg_color="#ff9800", 
                         command=lambda k=kh: self.show_edit_form(k)).pack(side="left", padx=2)
            ctk.CTkButton(act_f, text="🗑️", width=35, fg_color="#d32f2f", 
                         command=lambda k=kh: self.delete_customer(k['id'])).pack(side="left", padx=2)
            ctk.CTkButton(act_f, text="🚘", width=35, fg_color="#2196f3", 
                         command=lambda k=kh: self.view_customer_cars(k)).pack(side="left", padx=2)
            
            widgets.append(act_f)
            self.table_rows.append(widgets)
        
        self.update_pagination_info()

    def load_data(self):
        """Tải toàn bộ dữ liệu từ DB"""
        self.current_data = self.controller.get_all()
        self.render_table(self.current_data)

    def search(self):
        """Tìm kiếm dữ liệu"""
        kw = self.search_entry.get().strip()
        if not kw:
            self.load_data()
            return
        
        self.current_data = self.controller.search(kw)
        self.current_page = 1
        self.render_table(self.current_data)
        
        if not self.current_data:
            messagebox.showinfo("Kết quả", "Không tìm thấy khách hàng phù hợp")

    def save_customer(self):
        """Lưu (Add/Update) và cập nhật giao diện"""
        data = {k: v.get().strip() for k, v in self.form_entries.items()}
        
        if not data['ho_ten'] or not data['so_dien_thoai']:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ các trường bắt buộc (*)")
            return

        if self.current_customer_id:
            success = self.controller.update(self.current_customer_id, data['ho_ten'], 
                                             data['so_dien_thoai'], data['email'], data['dia_chi'])
        else:
            success = self.controller.add(data['ho_ten'], data['so_dien_thoai'], 
                                          data['email'], data['dia_chi'])

        if success:
            messagebox.showinfo("Thành công", "Dữ liệu đã được cập nhật")
            self.hide_form()
            self.load_data()
            if self.on_refresh:
                self.on_refresh()
        else:
            messagebox.showerror("Lỗi", "Không thể lưu dữ liệu vào Database")

    def delete_customer(self, customer_id):
        """Xóa khách hàng"""
        if messagebox.askyesno("Xác nhận xóa", "Xóa khách hàng này sẽ xóa tất cả xe liên quan. Tiếp tục?"):
            if self.controller.delete(customer_id):
                messagebox.showinfo("Thành công", "Đã xóa khách hàng khỏi hệ thống")
                self.load_data()
                if self.on_refresh:
                    self.on_refresh()
            else:
                messagebox.showerror("Lỗi", "Xóa thất bại. Vui lòng kiểm tra lại.")

    # ==================== SỬA LỖI METHOD NÀY ====================
    def view_customer_cars(self, customer):
        """Mở cửa sổ danh sách xe của khách hàng"""
        car_win = ctk.CTkToplevel(self.parent)
        car_win.title(f"Xe của khách hàng: {customer['ho_ten']}")
        car_win.geometry("850x500")
        car_win.grab_set()
        car_win.after(100, lambda: car_win.lift())

        # Header
        header_frame = ctk.CTkFrame(car_win, fg_color="#1f1f1f", corner_radius=0)
        header_frame.pack(fill="x")
        
        ctk.CTkLabel(header_frame, text=f"DANH SÁCH XE - {customer['ho_ten'].upper()}", 
                    font=ctk.CTkFont(size=18, weight="bold"), text_color="#4a9eff").pack(pady=15)
        
        # Thông tin khách hàng
        info_frame = ctk.CTkFrame(car_win, fg_color="#2b2b2b", corner_radius=10)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = f"Mã KH: {customer['ma_kh']} | SĐT: {customer['so_dien_thoai']} | Email: {customer['email'] or 'Chưa có'}"
        ctk.CTkLabel(info_frame, text=info_text, font=ctk.CTkFont(size=12), text_color="#888888").pack(pady=10)
        
        # Container cho bảng
        container = ctk.CTkFrame(car_win, fg_color="#1f1f1f", corner_radius=10)
        container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Tạo Treeview
        cols = ("ID", "Biển số", "Hiệu xe", "Model", "Màu sắc", "Năm SX")
        tree = ttk.Treeview(container, columns=cols, show="headings", height=10)
        
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        try:
            c_id = customer['id']
            print(f"DEBUG: Đang tìm xe cho khách hàng ID: {c_id}")
            
            # Gọi method từ controller
            cars = self.controller.get_cars_by_customer(c_id)
            
            print(f"DEBUG: Kết quả trả về: {len(cars) if cars else 0} xe")
            
            if cars and len(cars) > 0:
                for c in cars:
                    tree.insert("", "end", values=(
                        c.get('id', '—'), 
                        c.get('bien_so', '—'), 
                        c.get('hieu_xe', '—'), 
                        c.get('model', '—'), 
                        c.get('mau_sac', '—'), 
                        c.get('nam_sx', '—')
                    ))
                
                # Footer thông tin
                footer_frame = ctk.CTkFrame(car_win, fg_color="transparent")
                footer_frame.pack(fill="x", padx=20, pady=10)
                
                count_label = ctk.CTkLabel(footer_frame, text=f"✅ Tổng số xe: {len(cars)}", 
                                          font=ctk.CTkFont(size=13, weight="bold"), text_color="#00c853")
                count_label.pack(side="left")
            else:
                # Hiển thị thông báo không có xe
                no_cars_frame = ctk.CTkFrame(car_win, fg_color="transparent")
                no_cars_frame.pack(fill="both", expand=True)
                
                ctk.CTkLabel(no_cars_frame, text="🚗", font=ctk.CTkFont(size=64)).pack(pady=30)
                ctk.CTkLabel(no_cars_frame, text=f"Khách hàng {customer['ho_ten']} chưa có xe nào.", 
                            font=ctk.CTkFont(size=16), text_color="#888888").pack()
                ctk.CTkLabel(no_cars_frame, text="Vui lòng thêm xe mới cho khách hàng này từ mục 'Quản lý xe'.", 
                            font=ctk.CTkFont(size=12), text_color="#666666").pack()
                
        except Exception as e:
            print(f"DEBUG Lỗi: {str(e)}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Lỗi", f"Lỗi hiển thị danh sách xe: {str(e)}")
        
        # Nút đóng
        btn_frame = ctk.CTkFrame(car_win, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkButton(btn_frame, text="Đóng", command=car_win.destroy,
                     fg_color="#4a9eff", width=120, height=40,
                     font=ctk.CTkFont(size=13, weight="bold")).pack()

    def setup_pagination(self):
        self.pagination_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.pagination_frame.pack(fill="x", pady=10)
        
        self.page_label = ctk.CTkLabel(self.pagination_frame, text="Trang 1 / 1", font=ctk.CTkFont(size=12))
        self.page_label.pack(side="left", padx=20)
        
        self.next_btn = ctk.CTkButton(self.pagination_frame, text="Sau ▶", command=self.next_page, width=90)
        self.next_btn.pack(side="right", padx=5)
        
        self.prev_btn = ctk.CTkButton(self.pagination_frame, text="◀ Trước", command=self.prev_page, width=90)
        self.prev_btn.pack(side="right", padx=5)

    def update_pagination_info(self):
        total_p = max(1, (self.total_items + self.items_per_page - 1) // self.items_per_page)
        self.page_label.configure(text=f"Đang xem {self.current_page}/{total_p} (Tổng {self.total_items} khách hàng)")
        
        self.prev_btn.configure(state="normal" if self.current_page > 1 else "disabled")
        self.next_btn.configure(state="normal" if self.current_page < total_p else "disabled")

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.render_table(self.current_data)

    def next_page(self):
        total_p = (self.total_items + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_p:
            self.current_page += 1
            self.render_table(self.current_data)

    def export_to_excel(self):
        try:
            from utils.excel_export import ExcelExporter
            filename = f"KhachHang_{datetime.now().strftime('%d%m%Y_%H%M%S')}.xlsx"
            ExcelExporter.export_khach_hang(self.current_data, filename)
            messagebox.showinfo("Thành công", f"Đã xuất file: {filename}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi xuất Excel: {e}")

    def export_to_pdf(self):
        try:
            from utils.pdf_export import PDFExporter
            filename = f"KhachHang_{datetime.now().strftime('%d%m%Y_%H%M%S')}.pdf"
            PDFExporter.export_khach_hang(self.current_data, filename)
            messagebox.showinfo("Thành công", f"Đã xuất file: {filename}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi xuất PDF: {e}")