import tkinter as tk
from tkinter import ttk, messagebox

class HoaDonView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.dich_vu_controller = None
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        # Frame tạo hóa đơn
        create_frame = ttk.LabelFrame(self, text="Tạo hóa đơn mới")
        create_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(create_frame, text="ID Xe:").grid(row=0, column=0, padx=5, pady=5)
        self.id_xe_entry = ttk.Entry(create_frame, width=20)
        self.id_xe_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(create_frame, text="Tạo hóa đơn", command=self.create_hoa_don).grid(row=0, column=2, padx=10, pady=5)
        
        # Frame danh sách hóa đơn
        list_frame = ttk.LabelFrame(self, text="Danh sách hóa đơn")
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Treeview
        columns = ("ID", "Mã HD", "Ngày lập", "Biển số", "Chủ xe", "Tổng tiền", "Trạng thái")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Tổng tiền":
                self.tree.column(col, width=150)
            else:
                self.tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame chức năng
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Thêm dịch vụ", command=self.add_service).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cập nhật trạng thái", command=self.update_status).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Xem chi tiết", command=self.view_detail).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Xóa", command=self.delete).pack(side="left", padx=5)
        
        self.tree.bind("<Double-Button-1>", self.view_detail)
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        hoa_dons = self.controller.get_all()
        for hd in hoa_dons:
            status_text = {
                'dang_xu_ly': 'Đang xử lý',
                'hoan_thanh': 'Hoàn thành',
                'da_huy': 'Đã hủy'
            }.get(hd['trang_thai'], hd['trang_thai'])
            
            self.tree.insert("", "end", values=(
                hd['id'],
                hd['ma_hd'],
                hd['ngay_lap'],
                hd['bien_so'],
                hd['ten_chu_xe'],
                f"{hd['tong_tien']:,.0f} VNĐ",
                status_text
            ))
    
    def create_hoa_don(self):
        id_xe = self.id_xe_entry.get().strip()
        if not id_xe:
            messagebox.showerror("Lỗi", "Vui lòng nhập ID xe")
            return
        
        try:
            id_xe = int(id_xe)
            if self.controller.create(id_xe):
                messagebox.showinfo("Thành công", "Tạo hóa đơn thành công")
                self.load_data()
                self.id_xe_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Lỗi", "Tạo hóa đơn thất bại")
        except ValueError:
            messagebox.showerror("Lỗi", "ID xe phải là số")
    
    def add_service(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hóa đơn cần thêm dịch vụ")
            return
        
        hoa_don = self.tree.item(selected[0])['values']
        self.open_service_window(hoa_don[0])
    
    def open_service_window(self, id_hoa_don):
        window = tk.Toplevel(self)
        window.title("Thêm dịch vụ vào hóa đơn")
        window.geometry("500x300")
        window.grab_set()
        
        frame = ttk.Frame(window, padding="20")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="ID Dịch vụ:").grid(row=0, column=0, pady=5)
        id_dv_entry = ttk.Entry(frame, width=30)
        id_dv_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Số lượng:").grid(row=1, column=0, pady=5)
        so_luong_entry = ttk.Entry(frame, width=30)
        so_luong_entry.grid(row=1, column=1, pady=5)
        so_luong_entry.insert(0, "1")
        
        def add():
            try:
                id_dv = int(id_dv_entry.get())
                so_luong = int(so_luong_entry.get())
                
                # Lấy thông tin dịch vụ
                if self.dich_vu_controller:
                    dich_vu = self.dich_vu_controller.get_by_id(id_dv)
                    if dich_vu:
                        don_gia = dich_vu['don_gia']
                        if self.controller.add_service(id_hoa_don, id_dv, so_luong, don_gia):
                            messagebox.showinfo("Thành công", "Thêm dịch vụ thành công")
                            window.destroy()
                            self.load_data()
                        else:
                            messagebox.showerror("Lỗi", "Thêm dịch vụ thất bại")
                    else:
                        messagebox.showerror("Lỗi", "Không tìm thấy dịch vụ")
                else:
                    messagebox.showerror("Lỗi", "Chưa kết nối với controller dịch vụ")
            except ValueError:
                messagebox.showerror("Lỗi", "ID và số lượng phải là số")
        
        ttk.Button(frame, text="Thêm", command=add).grid(row=2, column=0, columnspan=2, pady=20)
    
    def update_status(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hóa đơn cần cập nhật")
            return
        
        hoa_don = self.tree.item(selected[0])['values']
        
        window = tk.Toplevel(self)
        window.title("Cập nhật trạng thái")
        window.geometry("300x150")
        window.grab_set()
        
        frame = ttk.Frame(window, padding="20")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Chọn trạng thái:").pack(pady=5)
        status_var = tk.StringVar()
        status_combo = ttk.Combobox(frame, textvariable=status_var, values=["dang_xu_ly", "hoan_thanh", "da_huy"], width=20)
        status_combo.pack(pady=5)
        
        def update():
            if self.controller.update_status(hoa_don[0], status_var.get()):
                messagebox.showinfo("Thành công", "Cập nhật trạng thái thành công")
                self.load_data()
                window.destroy()
            else:
                messagebox.showerror("Lỗi", "Cập nhật thất bại")
        
        ttk.Button(frame, text="Cập nhật", command=update).pack(pady=10)
    
    def view_detail(self, event=None):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hóa đơn cần xem")
            return
        
        hoa_don = self.tree.item(selected[0])['values']
        
        window = tk.Toplevel(self)
        window.title(f"Chi tiết hóa đơn {hoa_don[1]}")
        window.geometry("600x400")
        
        # Hiển thị thông tin hóa đơn
        info_frame = ttk.LabelFrame(window, text="Thông tin hóa đơn", padding="10")
        info_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(info_frame, text=f"Mã HD: {hoa_don[1]}").grid(row=0, column=0, sticky="w")
        ttk.Label(info_frame, text=f"Ngày: {hoa_don[2]}").grid(row=0, column=1, sticky="w")
        ttk.Label(info_frame, text=f"Biển số: {hoa_don[3]}").grid(row=1, column=0, sticky="w")
        ttk.Label(info_frame, text=f"Chủ xe: {hoa_don[4]}").grid(row=1, column=1, sticky="w")
        ttk.Label(info_frame, text=f"Tổng tiền: {hoa_don[5]}").grid(row=2, column=0, sticky="w")
        ttk.Label(info_frame, text=f"Trạng thái: {hoa_don[6]}").grid(row=2, column=1, sticky="w")
        
        # Danh sách dịch vụ
        service_frame = ttk.LabelFrame(window, text="Danh sách dịch vụ", padding="10")
        service_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("ID", "Tên dịch vụ", "Số lượng", "Đơn giá", "Thành tiền")
        service_tree = ttk.Treeview(service_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            service_tree.heading(col, text=col)
            service_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(service_frame, orient="vertical", command=service_tree.yview)
        service_tree.configure(yscrollcommand=scrollbar.set)
        
        service_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load chi tiết
        chi_tiet = self.controller.get_chi_tiet(hoa_don[0])
        for ct in chi_tiet:
            service_tree.insert("", "end", values=(
                ct['id_dich_vu'],
                ct['ten_dich_vu'],
                ct['so_luong'],
                f"{ct['don_gia']:,.0f} VNĐ",
                f"{ct['thanh_tien']:,.0f} VNĐ"
            ))
    
    def delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hóa đơn cần xóa")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa hóa đơn này?"):
            hoa_don = self.tree.item(selected[0])['values']
            if self.controller.delete(hoa_don[0]):
                messagebox.showinfo("Thành công", "Xóa hóa đơn thành công")
                self.load_data()
            else:
                messagebox.showerror("Lỗi", "Xóa hóa đơn thất bại")