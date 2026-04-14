import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import customtkinter as ctk
from tkinter import messagebox, ttk, StringVar  
from datetime import datetime, timedelta

class ModernHoaDonView:
    def __init__(self, parent, controller, xe_controller, dich_vu_controller):
        self.parent = parent
        self.controller = controller
        self.xe_controller = xe_controller
        self.dich_vu_controller = dich_vu_controller
        self.current_hoa_don_id = None
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Thiết lập giao diện quản lý hóa đơn"""
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)
        
        # Tạo hóa đơn nhanh
        self.setup_create_section()
        
        # Bảng hóa đơn
        self.setup_table()
        
        # Chi tiết hóa đơn
        self.setup_detail_view()
    
    def setup_create_section(self):
        """Khu vực tạo hóa đơn nhanh"""
        create_frame = ctk.CTkFrame(self.main_frame, fg_color="#1f1f1f", corner_radius=10)
        create_frame.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            create_frame,
            text="Tạo hóa đơn mới",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=10)
        
        input_frame = ctk.CTkFrame(create_frame, fg_color="transparent")
        input_frame.pack(pady=10)
        
        ctk.CTkLabel(input_frame, text="ID Xe:", font=ctk.CTkFont(size=14)).pack(side="left", padx=5)
        self.id_xe_entry = ctk.CTkEntry(input_frame, width=150, height=35)
        self.id_xe_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(input_frame, text="Hoặc biển số:", font=ctk.CTkFont(size=14)).pack(side="left", padx=5)
        self.bien_so_entry = ctk.CTkEntry(input_frame, width=150, height=35)
        self.bien_so_entry.pack(side="left", padx=5)
        
        self.find_btn = ctk.CTkButton(
            input_frame,
            text="🔍 Tìm xe",
            command=self.find_car_by_plate,
            fg_color="#2196f3",
            height=35
        )
        self.find_btn.pack(side="left", padx=5)
        
        self.create_btn = ctk.CTkButton(
            create_frame,
            text="➕ Tạo hóa đơn",
            command=self.create_hoa_don,
            fg_color="#4a9eff",
            height=40,
            width=200,
            corner_radius=10
        )
        self.create_btn.pack(pady=10)
    
    def find_car_by_plate(self):
        """Tìm xe theo biển số"""
        bien_so = self.bien_so_entry.get().strip()
        if bien_so:
            cars = self.xe_controller.search(bien_so)
            if cars:
                self.id_xe_entry.delete(0, 'end')
                self.id_xe_entry.insert(0, cars[0]['id'])
                messagebox.showinfo("Thông tin", f"Tìm thấy xe: {cars[0]['bien_so']} - {cars[0]['hieu_xe']}")
            else:
                messagebox.showwarning("Không tìm thấy", "Không tìm thấy xe với biển số này")
    
    def setup_table(self):
        """Bảng danh sách hóa đơn"""
        self.table_frame = ctk.CTkFrame(self.main_frame, fg_color="#1f1f1f", corner_radius=10)
        self.table_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Label
        label = ctk.CTkLabel(
            self.table_frame,
            text="Danh sách hóa đơn",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label.pack(pady=10)
        
        # Treeview
        tree_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Mã HD", "Ngày lập", "Biển số", "Chủ xe", "Tổng tiền", "Trạng thái"),
            show="headings",
            height=10
        )
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Mã HD", text="Mã HD")
        self.tree.heading("Ngày lập", text="Ngày lập")
        self.tree.heading("Biển số", text="Biển số")
        self.tree.heading("Chủ xe", text="Chủ xe")
        self.tree.heading("Tổng tiền", text="Tổng tiền")
        self.tree.heading("Trạng thái", text="Trạng thái")
        
        self.tree.column("ID", width=50)
        self.tree.column("Mã HD", width=120)
        self.tree.column("Ngày lập", width=150)
        self.tree.column("Biển số", width=120)
        self.tree.column("Chủ xe", width=150)
        self.tree.column("Tổng tiền", width=150)
        self.tree.column("Trạng thái", width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<<TreeviewSelect>>", self.on_select_hoa_don)
        
        # Buttons
        btn_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        self.add_service_btn = ctk.CTkButton(
            btn_frame,
            text="➕ Thêm dịch vụ",
            command=self.add_service_to_hoa_don,
            fg_color="#ff9800",
            height=35,
            width=150
        )
        self.add_service_btn.pack(side="left", padx=10)
        
        self.update_status_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 Cập nhật trạng thái",
            command=self.update_status,
            fg_color="#2196f3",
            height=35,
            width=150
        )
        self.update_status_btn.pack(side="left", padx=10)
        
        self.print_btn = ctk.CTkButton(
            btn_frame,
            text="🖨️ In hóa đơn",
            command=self.print_hoa_don,
            fg_color="#00c853",
            height=35,
            width=150
        )
        self.print_btn.pack(side="left", padx=10)
        
        self.delete_btn = ctk.CTkButton(
            btn_frame,
            text="🗑️ Xóa",
            command=self.delete_hoa_don,
            fg_color="#d32f2f",
            height=35,
            width=150
        )
        self.delete_btn.pack(side="left", padx=10)
        
        self.refresh_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 Làm mới",
            command=self.load_data,
            fg_color="#757575",
            height=35,
            width=150
        )
        self.refresh_btn.pack(side="right", padx=10)
    
    def setup_detail_view(self):
        """Khu vực hiển thị chi tiết hóa đơn"""
        self.detail_frame = ctk.CTkFrame(self.main_frame, fg_color="#1f1f1f", corner_radius=10)
        self.detail_frame.pack(fill="x", pady=(0, 20))
        
        label = ctk.CTkLabel(
            self.detail_frame,
            text="Chi tiết hóa đơn",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label.pack(pady=10)
        
        # Frame hiển thị chi tiết
        self.detail_content = ctk.CTkFrame(self.detail_frame, fg_color="transparent")
        self.detail_content.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.detail_info = ctk.CTkLabel(
            self.detail_content,
            text="Chọn một hóa đơn để xem chi tiết",
            font=ctk.CTkFont(size=14),
            text_color="#888888"
        )
        self.detail_info.pack(pady=20)
    
    def load_data(self):
        """Tải danh sách hóa đơn"""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Lấy dữ liệu
        hoa_dons = self.controller.get_all()
        print(f"Đã tải {len(hoa_dons)} hóa đơn")
        
        for hd in hoa_dons:
            status_text = {
                'dang_xu_ly': 'Đang xử lý',
                'hoan_thanh': 'Hoàn thành',
                'da_huy': 'Đã hủy'
            }.get(hd['trang_thai'], hd['trang_thai'])
            
            self.tree.insert("", "end", values=(
                hd['id'],
                hd['ma_hd'],
                hd['ngay_lap'].strftime("%d/%m/%Y %H:%M") if hd['ngay_lap'] else "",
                hd['bien_so'],
                hd['ten_chu_xe'],
                f"{hd['tong_tien']:,.0f} VNĐ",
                status_text
            ), tags=(hd['trang_thai'],))
        
        # Tạo tags cho màu sắc
        self.tree.tag_configure('dang_xu_ly', foreground='#ff9800')
        self.tree.tag_configure('hoan_thanh', foreground='#00c853')
        self.tree.tag_configure('da_huy', foreground='#d32f2f')
    
    def on_select_hoa_don(self, event):
        """Khi chọn một hóa đơn"""
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.current_hoa_don_id = values[0]
            self.show_chi_tiet(self.current_hoa_don_id)
    
    def show_chi_tiet(self, hoa_don_id):
        """Hiển thị chi tiết hóa đơn"""
        # Xóa nội dung cũ
        for widget in self.detail_content.winfo_children():
            widget.destroy()
        
        # Lấy chi tiết
        chi_tiet = self.controller.get_chi_tiet(hoa_don_id)
        print(f"Chi tiết hóa đơn {hoa_don_id}: {len(chi_tiet)} dịch vụ")
        
        if not chi_tiet:
            info_frame = ctk.CTkFrame(self.detail_content, fg_color="transparent")
            info_frame.pack(expand=True, fill="both", pady=40)
            
            info_icon = ctk.CTkLabel(
                info_frame,
                text="📭",
                font=ctk.CTkFont(size=48)
            )
            info_icon.pack()
            
            info = ctk.CTkLabel(
                info_frame,
                text="Chưa có dịch vụ nào trong hóa đơn này",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#888888"
            )
            info.pack(pady=10)
            
            sub_info = ctk.CTkLabel(
                info_frame,
                text="Nhấn nút '➕ Thêm dịch vụ' bên trên để thêm",
                font=ctk.CTkFont(size=13),
                text_color="#666666"
            )
            sub_info.pack()
            
            return
        
        # Tạo frame cho bảng
        table_container = ctk.CTkFrame(self.detail_content, fg_color="#2b2b2b", corner_radius=10)
        table_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tiêu đề bảng
        table_title = ctk.CTkLabel(
            table_container,
            text="📋 DANH SÁCH DỊCH VỤ",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4a9eff"
        )
        table_title.pack(pady=10)
        
        # Tạo bảng chi tiết
        columns = ("STT", "Tên dịch vụ", "Số lượng", "Đơn giá", "Thành tiền")
        tree = ttk.Treeview(table_container, columns=columns, show="headings", height=8)
        
        col_widths = [50, 250, 100, 150, 150]
        for col, width in zip(columns, col_widths):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="center")
        
        # Thêm scrollbar
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        for i, ct in enumerate(chi_tiet, 1):
            tree.insert("", "end", values=(
                i,
                ct['ten_dich_vu'],
                ct['so_luong'],
                f"{ct['don_gia']:,.0f} VNĐ",
                f"{ct['thanh_tien']:,.0f} VNĐ"
            ))
        
        # Tổng tiền
        total = sum(ct['thanh_tien'] for ct in chi_tiet)
        total_frame = ctk.CTkFrame(table_container, fg_color="transparent")
        total_frame.pack(fill="x", pady=10)
        
        total_label = ctk.CTkLabel(
            total_frame,
            text=f"TỔNG CỘNG: {total:,.0f} VNĐ",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ff9800"
        )
        total_label.pack()
    
    def create_hoa_don(self):
        """Tạo hóa đơn mới"""
        id_xe_str = self.id_xe_entry.get().strip()
        bien_so = self.bien_so_entry.get().strip()
        
        print(f"Tạo hóa đơn - ID xe: {id_xe_str}, Biển số: {bien_so}")
        
        if not id_xe_str and not bien_so:
            messagebox.showerror("Lỗi", "Vui lòng nhập ID xe hoặc biển số xe")
            return
        
        # Nếu nhập biển số thì tìm ID xe
        if bien_so and not id_xe_str:
            cars = self.xe_controller.search(bien_so)
            if cars:
                id_xe_str = str(cars[0]['id'])
                print(f"Tìm thấy xe với ID: {id_xe_str}")
            else:
                messagebox.showerror("Lỗi", f"Không tìm thấy xe với biển số: {bien_so}")
                return
        
        try:
            id_xe = int(id_xe_str)
            hoa_don_id = self.controller.create(id_xe)
            print(f"Kết quả tạo hóa đơn: {hoa_don_id}")
            
            if hoa_don_id:
                messagebox.showinfo("Thành công", f"Tạo hóa đơn thành công!\nMã hóa đơn: HD{datetime.now().strftime('%Y%m%d%H%M%S')}")
                self.id_xe_entry.delete(0, 'end')
                self.bien_so_entry.delete(0, 'end')
                self.load_data()
                self.current_hoa_don_id = hoa_don_id
            else:
                messagebox.showerror("Lỗi", "Tạo hóa đơn thất bại\nKiểm tra lại ID xe có tồn tại không")
        except ValueError:
            messagebox.showerror("Lỗi", "ID xe phải là số")
    
    def add_service_to_hoa_don(self):
        """Thêm dịch vụ vào hóa đơn - Phiên bản đơn giản nhất"""
        
        if not self.current_hoa_don_id:
            selected = self.tree.selection()
            if selected:
                values = self.tree.item(selected[0])['values']
                self.current_hoa_don_id = values[0]
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn hóa đơn cần thêm dịch vụ")
                return
        
        # Lấy danh sách dịch vụ
        services = self.dich_vu_controller.get_all()
        
        if not services:
            messagebox.showerror("Lỗi", "Chưa có dịch vụ nào! Vui lòng thêm dịch vụ trước.")
            return
        
        # Tạo dialog đơn giản
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Thêm dịch vụ")
        dialog.geometry("450x400")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.transient(self.parent)
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Main frame
        main_frame = ctk.CTkFrame(dialog, fg_color="#2b2b2b", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Tiêu đề
        title_label = ctk.CTkLabel(
            main_frame,
            text="➕ THÊM DỊCH VỤ",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#4a9eff"
        )
        title_label.pack(pady=(10, 5))
        
        hd_label = ctk.CTkLabel(
            main_frame,
            text=f"Hóa đơn #{self.current_hoa_don_id}",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        hd_label.pack(pady=(0, 15))
        
        # Separator
        separator = ctk.CTkFrame(main_frame, height=2, fg_color="#4a9eff")
        separator.pack(fill="x", padx=10, pady=(0, 15))
        
        # Chọn dịch vụ
        service_label = ctk.CTkLabel(
            main_frame,
            text="Chọn dịch vụ:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        service_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        service_names = [f"{s['ma_dv']} - {s['ten_dich_vu']} - {s['don_gia']:,.0f} VNĐ" for s in services]
        
        service_combo = ctk.CTkComboBox(
            main_frame,
            values=service_names,
            width=380,
            height=40,
            font=ctk.CTkFont(size=13)
        )
        service_combo.pack(padx=20, pady=(0, 15))
        if service_names:
            service_combo.set(service_names[0])
        
        # Số lượng
        qty_label = ctk.CTkLabel(
            main_frame,
            text="Số lượng:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        qty_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        so_luong_entry = ctk.CTkEntry(
            main_frame,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        so_luong_entry.insert(0, "1")
        so_luong_entry.pack(padx=20, pady=(0, 15))
        
        # Thành tiền
        total_label = ctk.CTkLabel(
            main_frame,
            text="Thành tiền: 0 VNĐ",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#00c853"
        )
        total_label.pack(pady=(10, 20))
        
        def update_total(*args):
            try:
                idx = service_combo.current()
                if idx >= 0 and idx < len(services):
                    service = services[idx]
                    so_luong = int(so_luong_entry.get() or 1)
                    thanh_tien = so_luong * service['don_gia']
                    total_label.configure(text=f"Thành tiền: {thanh_tien:,.0f} VNĐ")
            except:
                total_label.configure(text="Thành tiền: 0 VNĐ")
        
        service_combo.bind("<<ComboboxSelected>>", update_total)
        so_luong_entry.bind("<KeyRelease>", update_total)
        update_total()
        
        # ===== BUTTON FRAME =====
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(10, 15))
        
        def add_service():
            idx = service_combo.current()
            if idx < 0:
                messagebox.showerror("Lỗi", "Vui lòng chọn dịch vụ")
                return
            
            try:
                so_luong = int(so_luong_entry.get())
                if so_luong <= 0:
                    messagebox.showerror("Lỗi", "Số lượng phải lớn hơn 0")
                    return
                
                service = services[idx]
                
                result = self.controller.add_service(
                    self.current_hoa_don_id,
                    service['id'],
                    so_luong,
                    service['don_gia']
                )
                
                if result:
                    messagebox.showinfo(
                        "Thành công",
                        f"Đã thêm {so_luong} x {service['ten_dich_vu']}\nThành tiền: {so_luong * service['don_gia']:,.0f} VNĐ"
                    )
                    dialog.destroy()
                    self.load_data()
                    self.show_chi_tiet(self.current_hoa_don_id)
                else:
                    messagebox.showerror("Lỗi", "Thêm dịch vụ thất bại!")
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng không hợp lệ")
        
        # Nút THÊM DỊCH VỤ - Màu xanh, rõ ràng
        add_button = ctk.CTkButton(
            button_frame,
            text="THÊM DỊCH VỤ",
            command=add_service,
            fg_color="#4a9eff",
            hover_color="#357ae8",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        add_button.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        # Nút Hủy
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Hủy",
            command=dialog.destroy,
            fg_color="#757575",
            hover_color="#616161",
            height=45,
            font=ctk.CTkFont(size=14),
            corner_radius=10
        )
        cancel_button.pack(side="left", padx=(10, 0))
    
    def update_status(self):
        """Cập nhật trạng thái hóa đơn"""
        if not self.current_hoa_don_id:
            selected = self.tree.selection()
            if selected:
                values = self.tree.item(selected[0])['values']
                self.current_hoa_don_id = values[0]
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn hóa đơn cần cập nhật")
                return
        
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Cập nhật trạng thái")
        dialog.geometry("350x250")
        dialog.grab_set()
        
        main_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame, 
            text=f"Hóa đơn #{self.current_hoa_don_id}", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        ctk.CTkLabel(main_frame, text="Chọn trạng thái mới:", font=ctk.CTkFont(size=14)).pack(pady=10)
        
        status_var = ctk.StringVar(value="Đang xử lý")
        status_combo = ctk.CTkComboBox(
            main_frame,
            values=["Đang xử lý", "Hoàn thành", "Đã hủy"],
            variable=status_var,
            width=200,
            height=35
        )
        status_combo.pack(pady=10)
        
        status_map = {
            "Đang xử lý": "dang_xu_ly",
            "Hoàn thành": "hoan_thanh",
            "Đã hủy": "da_huy"
        }
        
        def update():
            new_status = status_map[status_var.get()]
            if self.controller.update_status(self.current_hoa_don_id, new_status):
                messagebox.showinfo("Thành công", "Cập nhật trạng thái thành công")
                dialog.destroy()
                self.load_data()
            else:
                messagebox.showerror("Lỗi", "Cập nhật thất bại")
        
        ctk.CTkButton(
            main_frame, 
            text="Cập nhật", 
            command=update, 
            fg_color="#4a9eff", 
            height=35, 
            width=150
        ).pack(pady=20)
    
    def print_hoa_don(self):
        """In hóa đơn PDF"""
        if not self.current_hoa_don_id:
            selected = self.tree.selection()
            if selected:
                values = self.tree.item(selected[0])['values']
                self.current_hoa_don_id = values[0]
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn hóa đơn cần in")
                return
        
        try:
            from utils.pdf_export import PDFExporter
            
            # Lấy thông tin hóa đơn
            hoa_don_info = self.controller.get_by_id(self.current_hoa_don_id)
            chi_tiet = self.controller.get_chi_tiet(self.current_hoa_don_id)
            
            if not chi_tiet:
                messagebox.showwarning("Cảnh báo", "Hóa đơn chưa có dịch vụ nào, không thể in")
                return
            
            filename = f"hoa_don_{hoa_don_info['ma_hd']}_{datetime.now().strftime('%Y%m%d')}.pdf"
            PDFExporter.export_hoa_don(hoa_don_info, chi_tiet, filename)
            messagebox.showinfo("Thành công", f"Đã in hóa đơn: {filename}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"In hóa đơn thất bại: {str(e)}")
    
    def delete_hoa_don(self):
        """Xóa hóa đơn"""
        if not self.current_hoa_don_id:
            selected = self.tree.selection()
            if selected:
                values = self.tree.item(selected[0])['values']
                self.current_hoa_don_id = values[0]
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn hóa đơn cần xóa")
                return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa hóa đơn này?"):
            if self.controller.delete(self.current_hoa_don_id):
                messagebox.showinfo("Thành công", "Xóa hóa đơn thành công")
                self.current_hoa_don_id = None
                self.load_data()
                # Xóa chi tiết
                for widget in self.detail_content.winfo_children():
                    widget.destroy()
                info = ctk.CTkLabel(
                    self.detail_content,
                    text="Chọn một hóa đơn để xem chi tiết",
                    font=ctk.CTkFont(size=14),
                    text_color="#888888"
                )
                info.pack(pady=20)
            else:
                messagebox.showerror("Lỗi", "Xóa hóa đơn thất bại")