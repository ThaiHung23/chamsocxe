import tkinter as tk
from tkinter import ttk, messagebox

class DichVuView(ttk.Frame):
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
        list_frame = ttk.LabelFrame(self, text="Danh sách dịch vụ")
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Treeview
        columns = ("ID", "Mã DV", "Tên dịch vụ", "Đơn giá", "Thời gian (phút)", "Mô tả")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Đơn giá":
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
        
        ttk.Button(btn_frame, text="Thêm mới", command=self.open_add_window).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Sửa", command=self.open_edit_window).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Xóa", command=self.delete).pack(side="left", padx=5)
        
        self.tree.bind("<Double-Button-1>", self.open_edit_window)
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        dich_vus = self.controller.get_all()
        for dv in dich_vus:
            self.tree.insert("", "end", values=(
                dv['id'],
                dv['ma_dv'],
                dv['ten_dich_vu'],
                f"{dv['don_gia']:,.0f} VNĐ",
                dv['thoi_gian_du_kien'],
                dv['mo_ta']
            ))
    
    def search(self):
        keyword = self.search_var.get()
        if keyword:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            results = self.controller.search(keyword)
            for dv in results:
                self.tree.insert("", "end", values=(
                    dv['id'],
                    dv['ma_dv'],
                    dv['ten_dich_vu'],
                    f"{dv['don_gia']:,.0f} VNĐ",
                    dv['thoi_gian_du_kien'],
                    dv['mo_ta']
                ))
    
    def open_add_window(self):
        self.open_form_window("Thêm dịch vụ mới")
    
    def open_edit_window(self, event=None):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dịch vụ cần sửa")
            return
        
        dich_vu = self.tree.item(selected[0])['values']
        self.open_form_window("Sửa thông tin dịch vụ", dich_vu)
    
    def open_form_window(self, title, data=None):
        window = tk.Toplevel(self)
        window.title(title)
        window.geometry("500x450")
        window.grab_set()
        
        frame = ttk.Frame(window, padding="20")
        frame.pack(fill="both", expand=True)
        
        # Các trường nhập liệu
        fields = {}
        labels = ["Mã dịch vụ:", "Tên dịch vụ:", "Đơn giá:", "Thời gian (phút):", "Mô tả:"]
        
        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky="w", pady=5)
            entry = ttk.Entry(frame, width=40)
            entry.grid(row=i, column=1, pady=5, padx=10)
            fields[label] = entry
            
            if data and i < len(data) - 1:
                value = data[i+1] if i+1 < len(data) else ""
                if i == 2:  # Đơn giá - loại bỏ "VNĐ"
                    value = value.replace(" VNĐ", "").replace(",", "")
                entry.insert(0, value)
        
        def save():
            ma_dv = fields["Mã dịch vụ:"].get().strip()
            ten_dv = fields["Tên dịch vụ:"].get().strip()
            don_gia = fields["Đơn giá:"].get().strip()
            thoi_gian = fields["Thời gian (phút):"].get().strip()
            mo_ta = fields["Mô tả:"].get().strip()
            
            if not ma_dv or not ten_dv or not don_gia:
                messagebox.showerror("Lỗi", "Mã DV, tên DV và đơn giá không được để trống")
                return
            
            try:
                don_gia = float(don_gia)
                thoi_gian = int(thoi_gian) if thoi_gian else 0
            except ValueError:
                messagebox.showerror("Lỗi", "Đơn giá và thời gian phải là số")
                return
            
            if data:  # Sửa
                if self.controller.update(data[0], ma_dv, ten_dv, don_gia, thoi_gian, mo_ta):
                    messagebox.showinfo("Thành công", "Cập nhật dịch vụ thành công")
                    self.load_data()
                    window.destroy()
                else:
                    messagebox.showerror("Lỗi", "Cập nhật thất bại")
            else:  # Thêm mới
                if self.controller.add(ma_dv, ten_dv, don_gia, thoi_gian, mo_ta):
                    messagebox.showinfo("Thành công", "Thêm dịch vụ thành công")
                    self.load_data()
                    window.destroy()
                else:
                    messagebox.showerror("Lỗi", "Thêm dịch vụ thất bại")
        
        ttk.Button(frame, text="Lưu", command=save).grid(row=5, column=0, columnspan=2, pady=20)
    
    def delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dịch vụ cần xóa")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa dịch vụ này?"):
            dich_vu = self.tree.item(selected[0])['values']
            if self.controller.delete(dich_vu[0]):
                messagebox.showinfo("Thành công", "Xóa dịch vụ thành công")
                self.load_data()
            else:
                messagebox.showerror("Lỗi", "Xóa dịch vụ thất bại")