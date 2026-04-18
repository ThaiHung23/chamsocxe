import customtkinter as ctk
from tkinter import messagebox, ttk, StringVar
from datetime import datetime

class ModernHoaDonView:
    def __init__(self, parent, controller, xe_controller, dich_vu_controller):
        self.parent = parent
        self.controller = controller
        self.xe_controller = xe_controller
        self.dich_vu_controller = dich_vu_controller
        self.current_hoa_don_id = None
        
        # --- Cấu hình kích thước chuẩn cho UI ---
        self.BTN_HEIGHT = 45
        self.BTN_WIDTH = 170
        self.ENTRY_HEIGHT = 40
        self.FONT_BOLD = ctk.CTkFont(size=13, weight="bold")
        self.TITLE_FONT = ctk.CTkFont(size=18, weight="bold")
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Khung sườn chính của giao diện quản lý hóa đơn"""
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 1. Phần Nhập liệu & Tạo hóa đơn
        self.setup_create_section()
        
        # 2. Phần Danh sách hóa đơn
        self.setup_table_section()
        
        # 3. Phần Chi tiết dịch vụ
        self.setup_detail_section()
    
    def setup_create_section(self):
        """Khu vực tìm xe và tạo hóa đơn mới"""
        create_frame = ctk.CTkFrame(self.main_frame, fg_color="#1f1f1f", corner_radius=12)
        create_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(create_frame, text="TẠO HÓA ĐƠN MỚI", font=self.TITLE_FONT, text_color="#4a9eff").pack(pady=15)
        
        input_frame = ctk.CTkFrame(create_frame, fg_color="transparent")
        input_frame.pack(pady=10)
        
        # Nhập ID Xe
        ctk.CTkLabel(input_frame, text="ID Xe:", font=self.FONT_BOLD).pack(side="left", padx=10)
        self.id_xe_entry = ctk.CTkEntry(input_frame, width=100, height=self.ENTRY_HEIGHT)
        self.id_xe_entry.pack(side="left", padx=5)
        
        # Nhập Biển số
        ctk.CTkLabel(input_frame, text="Hoặc Biển số:", font=self.FONT_BOLD).pack(side="left", padx=10)
        self.bien_so_entry = ctk.CTkEntry(input_frame, width=180, height=self.ENTRY_HEIGHT, placeholder_text="Ví dụ: 30A-12345")
        self.bien_so_entry.pack(side="left", padx=5)
        self.bien_so_entry.bind("<Return>", lambda e: self.find_car_by_plate())
        
        # Nút Tìm xe
        self.find_btn = ctk.CTkButton(input_frame, text="🔍 Tìm", command=self.find_car_by_plate,
                                     fg_color="#2196f3", height=self.ENTRY_HEIGHT, width=80, font=self.FONT_BOLD)
        self.find_btn.pack(side="left", padx=10)
        
        # Nút Tạo hóa đơn chính
        self.create_btn = ctk.CTkButton(create_frame, text="➕ TẠO HÓA ĐƠN MỚI", command=self.create_hoa_don,
                                       fg_color="#00c853", hover_color="#00a344", 
                                       height=55, width=300, font=ctk.CTkFont(size=15, weight="bold"))
        self.create_btn.pack(pady=(10, 20))
    
    def setup_table_section(self):
        """Bảng hiển thị danh sách hóa đơn"""
        self.table_frame = ctk.CTkFrame(self.main_frame, fg_color="#1f1f1f", corner_radius=12)
        self.table_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        ctk.CTkLabel(self.table_frame, text="DANH SÁCH HÓA ĐƠN", font=self.FONT_BOLD).pack(pady=10)
        
        # Container cho Treeview và Scrollbar
        tree_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        columns = ("ID", "Mã HD", "Ngày lập", "Biển số", "Chủ xe", "Tổng tiền", "Trạng thái")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)
        self.tree.column("ID", width=50)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<<TreeviewSelect>>", self.on_select_hoa_don)
        
        # --- Thanh Toolbar ---
        btn_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=15, padx=15)
        
        self.add_service_btn = ctk.CTkButton(btn_frame, text="➕ Thêm dịch vụ", command=self.add_service_to_hoa_don,
                                            fg_color="#ff9800", height=self.BTN_HEIGHT, width=self.BTN_WIDTH, font=self.FONT_BOLD)
        self.add_service_btn.pack(side="left", padx=5)
        
        self.update_status_btn = ctk.CTkButton(btn_frame, text="🔄 Trạng thái", command=self.update_status,
                                              fg_color="#2196f3", height=self.BTN_HEIGHT, width=self.BTN_WIDTH, font=self.FONT_BOLD)
        self.update_status_btn.pack(side="left", padx=5)
        
        self.print_btn = ctk.CTkButton(btn_frame, text="🖨️ In hóa đơn", command=self.print_hoa_don,
                                      fg_color="#00c853", height=self.BTN_HEIGHT, width=self.BTN_WIDTH, font=self.FONT_BOLD)
        self.print_btn.pack(side="left", padx=5)
        
        self.delete_btn = ctk.CTkButton(btn_frame, text="🗑️ Xóa", command=self.delete_hoa_don,
                                       fg_color="#d32f2f", height=self.BTN_HEIGHT, width=100, font=self.FONT_BOLD)
        self.delete_btn.pack(side="left", padx=5)
        
        # Nút Làm mới bên phải
        self.refresh_btn = ctk.CTkButton(btn_frame, text="🔄 Làm mới", command=self.load_data,
                                        fg_color="#757575", height=self.BTN_HEIGHT, width=120, font=self.FONT_BOLD)
        self.refresh_btn.pack(side="right", padx=5)

    def setup_detail_section(self):
        """Khu vực hiển thị danh sách dịch vụ chi tiết bên dưới"""
        self.detail_frame = ctk.CTkFrame(self.main_frame, fg_color="#1f1f1f", corner_radius=12)
        self.detail_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        self.detail_content = ctk.CTkFrame(self.detail_frame, fg_color="transparent")
        self.detail_content.pack(fill="both", expand=True, padx=15, pady=10)
        
        self.detail_info = ctk.CTkLabel(self.detail_content, text="Chọn một hóa đơn từ bảng để xem chi tiết", text_color="#888888")
        self.detail_info.pack(pady=15)

    # --- HÀM XỬ LÝ LOGIC ---

    def load_data(self):
        """Cập nhật lại dữ liệu cho bảng danh sách hóa đơn"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        hoa_dons = self.controller.get_all()
        for hd in hoa_dons:
            status_text = {
                'dang_xu_ly': 'Đang xử lý',
                'hoan_thanh': 'Hoàn thành',
                'da_huy': 'Đã hủy'
            }.get(hd['trang_thai'], hd['trang_thai'])
            
            # Xử lý ngày tháng an toàn
            ngay_lap = hd['ngay_lap']
            if isinstance(ngay_lap, str):
                try:
                    ngay_lap = datetime.strptime(ngay_lap, "%Y-%m-%d %H:%M:%S")
                except:
                    ngay_lap = datetime.now()
            
            self.tree.insert("", "end", values=(
                hd['id'], 
                hd['ma_hd'], 
                ngay_lap.strftime("%d/%m/%Y %H:%M") if hasattr(ngay_lap, 'strftime') else str(ngay_lap),
                hd['bien_so'], 
                hd['ten_chu_xe'], 
                f"{hd['tong_tien']:,.0f} VNĐ", 
                status_text
            ))

    def find_car_by_plate(self):
        """Tìm xe theo biển số"""
        plate = self.bien_so_entry.get().strip()
        if plate:
            cars = self.xe_controller.search(plate)
            if cars:
                self.id_xe_entry.delete(0, 'end')
                self.id_xe_entry.insert(0, str(cars[0]['id']))
                messagebox.showinfo("Tìm thấy", f"Xe: {cars[0]['hieu_xe']} - {cars[0]['bien_so']}\nChủ xe: {cars[0].get('ten_chu_xe', 'N/A')}")
            else:
                messagebox.showwarning("Không tìm thấy", f"Không tìm thấy xe với biển số: {plate}")

    def create_hoa_don(self):
        """Logic tạo hóa đơn mới từ ID xe"""
        try:
            id_xe_str = self.id_xe_entry.get().strip()
            if not id_xe_str:
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập ID xe hoặc tìm xe theo biển số")
                return
            
            id_xe = int(id_xe_str)
            result = self.controller.create(id_xe)
            
            if result:
                messagebox.showinfo("Thành công", "Đã tạo hóa đơn mới thành công!")
                self.id_xe_entry.delete(0, 'end')
                self.bien_so_entry.delete(0, 'end')
                self.load_data()
            else:
                messagebox.showerror("Lỗi", "Không thể tạo hóa đơn. Kiểm tra lại ID xe.")
        except ValueError:
            messagebox.showerror("Lỗi", "ID xe phải là một con số")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi: {str(e)}")

    def on_select_hoa_don(self, event):
        """Sự kiện khi click vào một dòng trên bảng"""
        selected = self.tree.selection()
        if selected:
            self.current_hoa_don_id = self.tree.item(selected[0])['values'][0]
            self.show_chi_tiet(self.current_hoa_don_id)

    def show_chi_tiet(self, hoa_don_id):
        """Hiển thị các dịch vụ đã sử dụng trong hóa đơn được chọn"""
        # Xóa nội dung cũ
        for widget in self.detail_content.winfo_children():
            widget.destroy()
        
        chi_tiet = self.controller.get_chi_tiet(hoa_don_id)
        
        if not chi_tiet or len(chi_tiet) == 0:
            ctk.CTkLabel(self.detail_content, text="📋 Hóa đơn này hiện chưa có dịch vụ nào", 
                        font=ctk.CTkFont(size=14), text_color="#888888").pack(pady=20)
            return
        
        # Tiêu đề
        header_frame = ctk.CTkFrame(self.detail_content, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(header_frame, text="📝 CHI TIẾT DỊCH VỤ", 
                    font=ctk.CTkFont(size=14, weight="bold"), text_color="#4a9eff").pack(side="left")
        
        # Tổng tiền
        tong_tien = sum(ct['thanh_tien'] for ct in chi_tiet)
        ctk.CTkLabel(header_frame, text=f"Tổng: {tong_tien:,.0f} VNĐ", 
                    font=ctk.CTkFont(size=14, weight="bold"), text_color="#00c853").pack(side="right")
        
        # Bảng chi tiết
        cols = ("Tên dịch vụ", "Số lượng", "Đơn giá", "Thành tiền")
        tree_dt = ttk.Treeview(self.detail_content, columns=cols, show="headings", height=6)
        
        for c in cols:
            tree_dt.heading(c, text=c)
            tree_dt.column(c, anchor="center", width=150)
        
        for ct in chi_tiet:
            tree_dt.insert("", "end", values=(
                ct['ten_dich_vu'], 
                ct['so_luong'], 
                f"{ct['don_gia']:,.0f} VNĐ", 
                f"{ct['thanh_tien']:,.0f} VNĐ"
            ))
        
        tree_dt.pack(fill="both", expand=True)

    def add_service_to_hoa_don(self):
        """Mở cửa sổ (Popup) thêm dịch vụ"""
        if not self.current_hoa_don_id:
            messagebox.showwarning("Lưu ý", "Vui lòng chọn 1 hóa đơn từ danh sách!")
            return

        services = self.dich_vu_controller.get_all()
        if not services:
            messagebox.showwarning("Lưu ý", "Chưa có dịch vụ nào trong hệ thống. Vui lòng thêm dịch vụ trước.")
            return
            
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Thêm Dịch Vụ Vào Hóa Đơn")
        dialog.geometry("500x500")
        dialog.grab_set()
        dialog.after(100, lambda: dialog.lift())

        main_pop = ctk.CTkFrame(dialog, fg_color="#1e1e1e", corner_radius=15)
        main_pop.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_pop, text="THÊM DỊCH VỤ", font=self.TITLE_FONT).pack(pady=20)
        
        # ComboBox chọn dịch vụ
        ctk.CTkLabel(main_pop, text="Chọn loại dịch vụ:", font=self.FONT_BOLD).pack(anchor="w", padx=40)
        service_names = [f"{s['ten_dich_vu']} - {s['don_gia']:,.0f} VNĐ" for s in services]
        combo = ctk.CTkComboBox(main_pop, values=service_names, width=380, height=45)
        combo.pack(pady=10)

        # Nhập số lượng
        ctk.CTkLabel(main_pop, text="Nhập số lượng:", font=self.FONT_BOLD).pack(anchor="w", padx=40)
        qty_entry = ctk.CTkEntry(main_pop, width=120, height=45, justify="center")
        qty_entry.insert(0, "1")
        qty_entry.pack(pady=10)

        # Nút xác nhận
        btn = ctk.CTkButton(main_pop, text="XÁC NHẬN & LƯU", height=55, width=280, 
                            font=self.FONT_BOLD, fg_color="#00c853", hover_color="#00a344",
                            command=lambda: self.confirm_add_service(dialog, services, combo, qty_entry))
        btn.pack(pady=30)

    def confirm_add_service(self, dialog, services, combo, qty_entry):
        """Xử lý lưu vào Database và cập nhật giao diện"""
        try:
            qty = int(qty_entry.get())
            if qty <= 0:
                messagebox.showerror("Lỗi", "Số lượng phải lớn hơn 0")
                return
                
            selected_text = combo.get()
            if not selected_text:
                messagebox.showerror("Lỗi", "Vui lòng chọn dịch vụ")
                return
            
            # Tìm ID dịch vụ từ tên đã chọn
            service_selected = None
            for s in services:
                if s['ten_dich_vu'] in selected_text:
                    service_selected = s
                    break

            if service_selected and self.current_hoa_don_id:
                # Gọi Controller lưu dữ liệu
                success = self.controller.add_service(
                    self.current_hoa_don_id, 
                    service_selected['id'], 
                    qty, 
                    service_selected['don_gia']
                )
                
                if success:
                    dialog.destroy()
                    messagebox.showinfo("Thành công", "Dịch vụ đã được thêm vào hóa đơn!")
                    
                    # Cập nhật giao diện
                    self.load_data()
                    self.show_chi_tiet(self.current_hoa_don_id)
                else:
                    messagebox.showerror("Lỗi", "Hệ thống không thể lưu dịch vụ này.")
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy dịch vụ đã chọn")
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng phải là một con số nguyên dương")

    def update_status(self):
        """Cập nhật trạng thái xử lý hóa đơn"""
        if not self.current_hoa_don_id:
            messagebox.showwarning("Lưu ý", "Vui lòng chọn hóa đơn cần cập nhật trạng thái")
            return
        
        # Lấy thông tin hóa đơn hiện tại
        hoa_don_info = None
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            if values[0] == self.current_hoa_don_id:
                hoa_don_info = values
                break
        
        # Tạo dialog chọn trạng thái
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Cập nhật trạng thái hóa đơn")
        dialog.geometry("450x400")
        dialog.grab_set()
        dialog.after(100, lambda: dialog.lift())
        
        main_frame = ctk.CTkFrame(dialog, fg_color="#1f1f1f", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="CẬP NHẬT TRẠNG THÁI", 
                    font=self.TITLE_FONT, text_color="#4a9eff").pack(pady=15)
        
        # Hiển thị thông tin hóa đơn
        if hoa_don_info:
            info_text = f"Mã HD: {hoa_don_info[1]}\nTrạng thái hiện tại: {hoa_don_info[6]}"
            ctk.CTkLabel(main_frame, text=info_text, font=ctk.CTkFont(size=12), 
                        text_color="#888888").pack(pady=10)
        
        ctk.CTkLabel(main_frame, text="Chọn trạng thái mới:", font=self.FONT_BOLD).pack(pady=10)
        
        status_var = ctk.StringVar(value="dang_xu_ly")
        
        status_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        status_frame.pack(pady=10)
        
        statuses = [
            ("🟡 Đang xử lý", "dang_xu_ly"),
            ("🟢 Hoàn thành", "hoan_thanh"),
            ("🔴 Đã hủy", "da_huy")
        ]
        
        for text, value in statuses:
            radio = ctk.CTkRadioButton(status_frame, text=text, variable=status_var, 
                                      value=value, font=ctk.CTkFont(size=13))
            radio.pack(anchor="w", pady=5)
        
        def confirm_update():
            new_status = status_var.get()
            if self.controller.update_status(self.current_hoa_don_id, new_status):
                messagebox.showinfo("Thành công", f"Đã cập nhật trạng thái thành '{new_status}'")
                dialog.destroy()
                self.load_data()
                # Giữ nguyên selection và refresh chi tiết
                if self.current_hoa_don_id:
                    self.show_chi_tiet(self.current_hoa_don_id)
            else:
                messagebox.showerror("Lỗi", "Cập nhật trạng thái thất bại")
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(btn_frame, text="Cập nhật", command=confirm_update,
                     fg_color="#4a9eff", height=40, width=120, font=self.FONT_BOLD).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Hủy", command=dialog.destroy,
                     fg_color="#757575", height=40, width=100).pack(side="left", padx=10)

    def print_hoa_don(self):
        """Xuất/In hóa đơn ra PDF"""
        if not self.current_hoa_don_id:
            messagebox.showwarning("Lưu ý", "Vui lòng chọn hóa đơn cần in")
            return
        
        try:
            # Lấy thông tin hóa đơn
            hoa_don = self.controller.get_by_id(self.current_hoa_don_id)
            chi_tiet = self.controller.get_chi_tiet(self.current_hoa_don_id)
            
            if not hoa_don:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin hóa đơn")
                return
            
            if not chi_tiet or len(chi_tiet) == 0:
                if not messagebox.askyesno("Xác nhận", "Hóa đơn chưa có dịch vụ nào. Bạn vẫn muốn in?"):
                    return
            
            # Import và xuất PDF
            from utils.pdf_export import PDFExporter
            
            filename = f"hoa_don_{hoa_don['ma_hd']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            PDFExporter.export_hoa_don(hoa_don, chi_tiet, filename)
            
            messagebox.showinfo("Thành công", f"Đã xuất hóa đơn thành công!\nFile: {filename}")
            
        except ImportError:
            messagebox.showerror("Lỗi", "Chưa cài đặt thư viện reportlab.\nVui lòng chạy: pip install reportlab")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Xuất PDF thất bại: {str(e)}")

    def delete_hoa_don(self):
        """Xóa hóa đơn vĩnh viễn"""
        if not self.current_hoa_don_id:
            messagebox.showwarning("Lưu ý", "Vui lòng chọn hóa đơn cần xóa")
            return
        
        # Lấy thông tin hóa đơn để hiển thị xác nhận
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            ma_hd = values[1]
        else:
            ma_hd = str(self.current_hoa_don_id)
        
        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa hóa đơn {ma_hd}?\nHành động này không thể hoàn tác!"):
            if self.controller.delete(self.current_hoa_don_id):
                messagebox.showinfo("Thành công", "Đã xóa hóa đơn")
                self.current_hoa_don_id = None
                self.load_data()
                # Xóa nội dung chi tiết
                for widget in self.detail_content.winfo_children():
                    widget.destroy()
                ctk.CTkLabel(self.detail_content, text="Chọn một hóa đơn từ bảng để xem chi tiết", 
                           text_color="#888888").pack(pady=15)
            else:
                messagebox.showerror("Lỗi", "Xóa hóa đơn thất bại.\nCó thể hóa đơn đang được tham chiếu ở nơi khác.")