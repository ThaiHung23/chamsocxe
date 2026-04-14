import tkinter as tk
from tkinter import ttk, messagebox

class XeView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.khach_hang_controller = None  # Sẽ được set từ main
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
        list_frame = ttk.LabelFrame(self, text="Danh sách xe")
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Treeview
        columns = ("ID", "Biển số", "Hiệu xe", "Model", "Màu sắc", "Năm SX", "Chủ xe")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
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
        
        xe_list = self.controller.get_all()
        for xe in xe_list:
            self.tree.insert("", "end", values=(
                xe['id'],
                xe['bien_so'],
                xe['hieu_xe'],
                xe['model'],
                xe['mau_sac'],
                xe['nam_sx'],
                xe.get('ten_chu_xe', 'N/A')
            ))
    
    def search(self):
        keyword = self.search_var.get()
        if keyword:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            results = self.controller.search(keyword)
            for xe in results:
                self.tree.insert("", "end", values=(
                    xe['id'],
                    xe['bien_so'],
                    xe['hieu_xe'],
                    xe['model'],
                    xe['mau_sac'],
                    xe['nam_sx'],
                    xe.get('ten_chu_xe', 'N/A')
                ))
    
    def open_add_window(self):
        self.open_form_window("Thêm xe mới")
    
    def open_edit_window(self, event=None):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn xe cần sửa")
            return
        
        xe = self.tree.item(selected[0])['values']
        self.open_form_window("Sửa thông tin xe", xe)
    
    def open_form_window(self, title, data=None):
        window = tk.Toplevel(self)
        window.title(title)
        window.geometry("500x450")
        window.grab_set()
        
        frame = ttk.Frame(window, padding="20")
        frame.pack(fill="both", expand=True)
        
        # Các trường nhập liệu
        fields = {}
        labels = ["Biển số:", "Hiệu xe:", "Model:", "Màu sắc:", "Năm sản xuất:", "ID khách hàng:"]
        
        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky="w", pady=5)
            entry = ttk.Entry(frame, width=40)
            entry.grid(row=i, column=1, pady=5, padx=10)
            fields[label] = entry
            
            if data and i < len(data) - 1:
                entry.insert(0, data[i+1] if i+1 < len(data) else "")
        
        # Combobox chọn khách hàng (có thể thay thế bằng combobox)
        ttk.Label(frame, text="Hoặc chọn từ danh sách:").grid(row=6, column=0, pady=5)
        kh_combo = ttk.Combobox(frame, width=37)
        kh_combo.grid(row=6, column=1, pady=5)
        
        # Load danh sách khách hàng (cần controller khách hàng)
        # Tạm thời bỏ qua phần này, yêu cầu nhập ID thủ công
        
        def save():
            bien_so = fields["Biển số:"].get().strip()
            hieu_xe = fields["Hiệu xe:"].get().strip()
            model = fields["Model:"].get().strip()
            mau_sac = fields["Màu sắc:"].get().strip()
            nam_sx = fields["Năm sản xuất:"].get().strip()
            id_kh = fields["ID khách hàng:"].get().strip()
            
            if not bien_so or not hieu_xe or not id_kh:
                messagebox.showerror("Lỗi", "Biển số, hiệu xe và ID khách hàng không được để trống")
                return
            
            try:
                id_kh = int(id_kh)
                nam_sx = int(nam_sx) if nam_sx else 0
            except ValueError:
                messagebox.showerror("Lỗi", "ID khách hàng và năm sản xuất phải là số")
                return
            
            if data:  # Sửa
                if self.controller.update(data[0], bien_so, hieu_xe, model, mau_sac, nam_sx, id_kh):
                    messagebox.showinfo("Thành công", "Cập nhật xe thành công")
                    self.load_data()
                    window.destroy()
                else:
                    messagebox.showerror("Lỗi", "Cập nhật thất bại")
            else:  # Thêm mới
                if self.controller.add(bien_so, hieu_xe, model, mau_sac, nam_sx, id_kh):
                    messagebox.showinfo("Thành công", "Thêm xe thành công")
                    self.load_data()
                    window.destroy()
                else:
                    messagebox.showerror("Lỗi", "Thêm xe thất bại")
        
        ttk.Button(frame, text="Lưu", command=save).grid(row=7, column=0, columnspan=2, pady=20)
    
    def delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn xe cần xóa")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa xe này?"):
            xe = self.tree.item(selected[0])['values']
            if self.controller.delete(xe[0]):
                messagebox.showinfo("Thành công", "Xóa xe thành công")
                self.load_data()
            else:
                messagebox.showerror("Lỗi", "Xóa xe thất bại")