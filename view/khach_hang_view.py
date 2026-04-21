import tkinter as tk
from tkinter import ttk, messagebox

class KhachHangView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        # Frame tìm kiếm
        search_frame = ttk.LabelFrame(self, text="Tìm kiếm")
        search_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(search_frame, text="Từ khóa:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side="left", padx=5)
        
        ttk.Button(search_frame, text="Tìm kiếm", command=self.search).pack(side="left", padx=5)
        ttk.Button(search_frame, text="Làm mới", command=self.load_data).pack(side="left", padx=5)
        
        # Frame danh sách
        list_frame = ttk.LabelFrame(self, text="Danh sách khách hàng")
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Treeview
        columns = ("ID", "Mã KH", "Họ tên", "Số điện thoại", "Email", "Địa chỉ", "Ngày tạo")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame chức năng
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Thêm mới", command=self.open_add_window).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Sửa", command=self.open_edit_window).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Xóa", command=self.delete).pack(side="left", padx=5)
        
        # Bind double click
        self.tree.bind("<Double-Button-1>", self.open_edit_window)
    
    def load_data(self):
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Lấy dữ liệu từ controller
        khach_hangs = self.controller.get_all()
        for kh in khach_hangs:
            self.tree.insert("", "end", values=(
                kh['id'],
                kh['ma_kh'],
                kh['ho_ten'],
                kh['so_dien_thoai'],
                kh['email'],
                kh['dia_chi'],
                kh['ngay_tao']
            ))
    
    def search(self):
        keyword = self.search_var.get()
        if keyword:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            results = self.controller.search(keyword)
            for kh in results:
                self.tree.insert("", "end", values=(
                    kh['id'],
                    kh['ma_kh'],
                    kh['ho_ten'],
                    kh['so_dien_thoai'],
                    kh['email'],
                    kh['dia_chi'],
                    kh['ngay_tao']
                ))
    
    def open_add_window(self):
        self.open_form_window("Thêm khách hàng mới")
    
    def open_edit_window(self, event=None):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng cần sửa")
            return
        
        khach_hang = self.tree.item(selected[0])['values']
        self.open_form_window("Sửa thông tin khách hàng", khach_hang)
    
    def open_form_window(self, title, data=None):
        window = tk.Toplevel(self)
        window.title(title)
        window.geometry("500x400")
        window.grab_set()
        
        # Frame nhập liệu
        frame = ttk.Frame(window, padding="20")
        frame.pack(fill="both", expand=True)
        
        # Các trường nhập liệu
        fields = {}
        labels = ["Họ tên:", "Số điện thoại:", "Email:", "Địa chỉ:"]
        
        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky="w", pady=5)
            entry = ttk.Entry(frame, width=40)
            entry.grid(row=i, column=1, pady=5, padx=10)
            fields[label] = entry
            
            if data and i < len(data) - 3:  # Bỏ qua id, ma_kh, ngay_tao
                entry.insert(0, data[i+2] if i+2 < len(data) else "")
        
        def save():
            ho_ten = fields["Họ tên:"].get().strip()
            so_dien_thoai = fields["Số điện thoại:"].get().strip()
            email = fields["Email:"].get().strip()
            dia_chi = fields["Địa chỉ:"].get().strip()
            
            if not ho_ten or not so_dien_thoai:
                messagebox.showerror("Lỗi", "Họ tên và số điện thoại không được để trống")
                return
            
            if data:  # Sửa
                if self.controller.update(data[0], ho_ten, so_dien_thoai, email, dia_chi):
                    messagebox.showinfo("Thành công", "Cập nhật khách hàng thành công")
                    self.load_data()
                    window.destroy()
                else:
                    messagebox.showerror("Lỗi", "Cập nhật thất bại")
            else:  # Thêm mới
                if self.controller.add(ho_ten, so_dien_thoai, email, dia_chi):
                    messagebox.showinfo("Thành công", "Thêm khách hàng thành công")
                    self.load_data()
                    window.destroy()
                else:
                    messagebox.showerror("Lỗi", "Thêm khách hàng thất bại")
        
        ttk.Button(frame, text="Lưu", command=save).grid(row=4, column=0, columnspan=2, pady=20)
    
    def delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng cần xóa")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa khách hàng này?"):
            khach_hang = self.tree.item(selected[0])['values']
            if self.controller.delete(khach_hang[0]):
                messagebox.showinfo("Thành công", "Xóa khách hàng thành công")
                self.load_data()
            else:
                messagebox.showerror("Lỗi", "Xóa khách hàng thất bại")