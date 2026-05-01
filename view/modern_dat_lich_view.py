import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime, date
import calendar


# Màu trạng thái
TRANG_THAI_COLORS = {
    'cho_xac_nhan':    ('#f59e0b', '⏳'),
    'da_xac_nhan':     ('#3b82f6', '✅'),
    'dang_thuc_hien':  ('#8b5cf6', '🔧'),
    'hoan_thanh':      ('#22c55e', '🏁'),
    'da_huy':          ('#ef4444', '❌'),
}

TRANG_THAI_LABELS = {
    'cho_xac_nhan':   'Chờ xác nhận',
    'da_xac_nhan':    'Đã xác nhận',
    'dang_thuc_hien': 'Đang thực hiện',
    'hoan_thanh':     'Hoàn thành',
    'da_huy':         'Đã hủy',
}

GIO_HEN = [f"{h:02d}:{m:02d}" for h in range(7, 19) for m in (0, 30)]


class ModernDatLichView:
    def __init__(self, parent, controller, khach_hang_controller, xe_controller, dich_vu_controller, on_refresh_callback=None):
        self.parent = parent
        self.controller = controller
        self.kh_ctrl = khach_hang_controller
        self.xe_ctrl = xe_controller
        self.dv_ctrl = dich_vu_controller
        self.on_refresh = on_refresh_callback

        self.current_page = 1
        self.items_per_page = 20
        self.total_items = 0
        self.current_data = []

        self.current_id = None          # ID lịch hẹn đang sửa
        self.selected_dich_vu = []      # [{id_dich_vu, ten, so_luong}]

        self.setup_ui()
        self.load_data()

    # ================================================================== #
    #  CẤU TRÚC CHÍNH                                                      #
    # ================================================================== #

    def setup_ui(self):
        self.main_frame = ctk.CTkFrame(self.parent, fg_color='transparent')
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.setup_toolbar()

        self.content_container = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        self.content_container.pack(fill='both', expand=True)

        self.setup_table()
        self.setup_form()
        self.setup_pagination()

    # ================================================================== #
    #  TOOLBAR                                                             #
    # ================================================================== #

    def setup_toolbar(self):
        toolbar = ctk.CTkFrame(self.main_frame, fg_color='#1f1f1f', corner_radius=10)
        toolbar.pack(fill='x', pady=(0, 10))

        left = ctk.CTkFrame(toolbar, fg_color='transparent')
        left.pack(side='left', padx=10, pady=10)

        ctk.CTkButton(left, text='➕ Đặt lịch mới', command=self.show_add_form,
                      fg_color='#4a9eff', hover_color='#357ae8', height=35).pack(side='left', padx=5)

        # Lọc theo ngày hôm nay
        ctk.CTkButton(left, text='📅 Hôm nay', command=self.filter_hom_nay,
                      fg_color='#00c853', hover_color='#00a045', height=35, width=100).pack(side='left', padx=5)

        ctk.CTkButton(left, text='🔄 Tất cả', command=self.load_data,
                      fg_color='#757575', hover_color='#616161', height=35, width=90).pack(side='left', padx=5)

        # Tìm kiếm
        search_frame = ctk.CTkFrame(toolbar, fg_color='#2b2b2b', corner_radius=8)
        search_frame.pack(side='right', padx=10)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text='Tên, SĐT, Biển số, Mã lịch...', width=260, border_width=0)
        self.search_entry.pack(side='left', padx=10, pady=5)
        self.search_entry.bind('<Return>', lambda e: self.search())

        ctk.CTkButton(search_frame, text='Tìm', command=self.search, width=70, height=30).pack(side='left', padx=5)

    # ================================================================== #
    #  BẢNG DỮ LIỆU                                                        #
    # ================================================================== #

    def setup_table(self):
        self.table_frame = ctk.CTkScrollableFrame(self.content_container, fg_color='#1f1f1f', corner_radius=10)
        self.table_frame.pack(fill='both', expand=True)

        self.headers = ['ID', 'Mã lịch', 'Khách hàng', 'SĐT', 'Xe', 'Ngày hẹn', 'Giờ hẹn', 'Trạng thái', 'Thao tác']
        self.col_widths = [35, 130, 150, 110, 100, 95, 80, 130, 160]

        self.header_frame = ctk.CTkFrame(self.table_frame, fg_color='#161625', corner_radius=8)
        self.header_frame.pack(fill='x', padx=5, pady=(5, 0))

        for i, (h, w) in enumerate(zip(self.headers, self.col_widths)):
            ctk.CTkLabel(self.header_frame, text=h, font=ctk.CTkFont(size=12, weight='bold'),
                         text_color='#4a9eff', width=w, anchor='center').grid(row=0, column=i, padx=3, pady=8)

    def load_data(self):
        self.current_data = self.controller.get_all()
        self._render_table()

    def filter_hom_nay(self):
        ngay = date.today().strftime('%Y-%m-%d')
        self.current_data = self.controller.get_by_ngay(ngay)
        self._render_table()

    def search(self):
        kw = self.search_entry.get().strip()
        if kw:
            self.current_data = self.controller.search(kw)
        else:
            self.current_data = self.controller.get_all()
        self.current_page = 1
        self._render_table()

    def _render_table(self):
        # Xóa hàng cũ (giữ header)
        for widget in self.table_frame.winfo_children():
            if widget != self.header_frame:
                widget.destroy()

        self.total_items = len(self.current_data)
        start = (self.current_page - 1) * self.items_per_page
        page_data = self.current_data[start: start + self.items_per_page]

        if not page_data:
            ctk.CTkLabel(self.table_frame, text='Không có dữ liệu', text_color='#888888',
                         font=ctk.CTkFont(size=14)).pack(pady=30)
            self._update_pagination()
            return

        for i, row in enumerate(page_data):
            bg = '#1a1a2e' if i % 2 == 0 else '#1f1f1f'
            row_frame = ctk.CTkFrame(self.table_frame, fg_color=bg, corner_radius=6)
            row_frame.pack(fill='x', padx=5, pady=1)

            trang_thai = row.get('trang_thai', 'cho_xac_nhan')
            color, icon = TRANG_THAI_COLORS.get(trang_thai, ('#888', '❓'))
            label_tt = f"{icon} {TRANG_THAI_LABELS.get(trang_thai, trang_thai)}"

            bien_so = row.get('bien_so_xe') or ''
            hieu_xe = row.get('hieu_xe') or ''
            xe_info = f"{bien_so} {hieu_xe}".strip() or '---'

            ngay_str = str(row.get('ngay_hen', ''))
            gio_str  = str(row.get('gio_hen', ''))[:5]

            values = [
                str(row['id']),
                row.get('ma_lich', ''),
                row.get('ten_khach_hang', ''),
                row.get('so_dien_thoai', ''),
                xe_info,
                ngay_str,
                gio_str,
            ]

            for j, (val, w) in enumerate(zip(values, self.col_widths)):
                ctk.CTkLabel(row_frame, text=val, width=w, anchor='center',
                             font=ctk.CTkFont(size=12), text_color='#e0e0e0').grid(row=0, column=j, padx=3, pady=6)

            # Trạng thái có màu
            ctk.CTkLabel(row_frame, text=label_tt, width=self.col_widths[7],
                         font=ctk.CTkFont(size=11, weight='bold'), text_color=color,
                         anchor='center').grid(row=0, column=7, padx=3, pady=6)

            # Nút thao tác
            btn_frame = ctk.CTkFrame(row_frame, fg_color='transparent', width=self.col_widths[8])
            btn_frame.grid(row=0, column=8, padx=3, pady=4)

            ctk.CTkButton(btn_frame, text='✏️', width=32, height=28,
                          fg_color='#4a9eff', hover_color='#357ae8',
                          command=lambda r=row: self.show_edit_form(r)).pack(side='left', padx=2)

            ctk.CTkButton(btn_frame, text='📋', width=32, height=28,
                          fg_color='#8b5cf6', hover_color='#7c3aed',
                          command=lambda r=row: self.show_chi_tiet(r)).pack(side='left', padx=2)

            ctk.CTkButton(btn_frame, text='🗑️', width=32, height=28,
                          fg_color='#ef4444', hover_color='#dc2626',
                          command=lambda rid=row['id']: self.delete_lich(rid)).pack(side='left', padx=2)

        self._update_pagination()

    # ================================================================== #
    #  PHÂN TRANG                                                          #
    # ================================================================== #

    def setup_pagination(self):
        self.pagination_frame = ctk.CTkFrame(self.main_frame, fg_color='#1f1f1f', corner_radius=8)
        self.pagination_frame.pack(fill='x', pady=(5, 0))
        self.pagination_info = ctk.CTkLabel(self.pagination_frame, text='', font=ctk.CTkFont(size=12))
        self.pagination_info.pack(side='left', padx=15, pady=8)
        self.pagination_btns = ctk.CTkFrame(self.pagination_frame, fg_color='transparent')
        self.pagination_btns.pack(side='right', padx=15)

    def _update_pagination(self):
        total_pages = max(1, -(-self.total_items // self.items_per_page))
        self.pagination_info.configure(
            text=f'Tổng: {self.total_items} lịch hẹn  |  Trang {self.current_page}/{total_pages}')

        for w in self.pagination_btns.winfo_children():
            w.destroy()

        if self.current_page > 1:
            ctk.CTkButton(self.pagination_btns, text='◀', width=35, height=30,
                          command=lambda: self._go_page(self.current_page - 1)).pack(side='left', padx=2)
        for p in range(max(1, self.current_page - 2), min(total_pages + 1, self.current_page + 3)):
            fg = '#4a9eff' if p == self.current_page else '#3a3a3a'
            ctk.CTkButton(self.pagination_btns, text=str(p), width=35, height=30,
                          fg_color=fg, command=lambda pp=p: self._go_page(pp)).pack(side='left', padx=2)
        if self.current_page < total_pages:
            ctk.CTkButton(self.pagination_btns, text='▶', width=35, height=30,
                          command=lambda: self._go_page(self.current_page + 1)).pack(side='left', padx=2)

    def _go_page(self, p):
        self.current_page = p
        self._render_table()

    # ================================================================== #
    #  FORM THÊM / SỬA                                                    #
    # ================================================================== #

    def setup_form(self):
        self.form_frame = ctk.CTkFrame(self.content_container, fg_color='#1a1a2e', corner_radius=12)
        # Không pack ngay – chỉ hiện khi cần

    def show_add_form(self):
        self.current_id = None
        self.selected_dich_vu = []
        self._open_form_window('Đặt lịch hẹn mới')

    def show_edit_form(self, row):
        self.current_id = row['id']
        self.selected_dich_vu = []
        # Nạp chi tiết dịch vụ đang có
        chi_tiet = self.controller.get_chi_tiet(row['id'])
        for ct in chi_tiet:
            self.selected_dich_vu.append({
                'id_dich_vu': ct['id_dich_vu'],
                'ten': ct['ten_dich_vu'],
                'so_luong': ct.get('so_luong', 1),
            })
        self._open_form_window('Chỉnh sửa lịch hẹn', row)

    def _open_form_window(self, title, row=None):
        """Cửa sổ popup nhập liệu"""
        win = ctk.CTkToplevel(self.parent)
        win.title(title)
        win.geometry('740x680')
        win.grab_set()
        win.focus_force()

        # --- Tiêu đề ---
        ctk.CTkLabel(win, text=title, font=ctk.CTkFont(size=18, weight='bold'),
                     text_color='#4a9eff').pack(pady=(20, 10))

        scroll = ctk.CTkScrollableFrame(win, fg_color='transparent')
        scroll.scroll_y = True
        scroll.pack(fill='both', expand=True, padx=25)

        def lbl(parent, text):
            ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=13),
                         text_color='#a0a0a0', anchor='w').pack(fill='x', pady=(8, 2))

        # --- Khách hàng ---
        lbl(scroll, '* Khách hàng')
        kh_list = self.kh_ctrl.get_all()
        kh_options = [f"{k['id']} - {k['ho_ten']} ({k['so_dien_thoai']})" for k in kh_list]

        kh_var = ctk.StringVar()
        kh_combo = ctk.CTkComboBox(
            scroll,
            values=kh_options,
            variable=kh_var,
            width=680,
            height=36,
            state="readonly"
        )
        kh_combo.pack(fill='x')


        # --- Xe ---
        lbl(scroll, 'Xe (tùy chọn)')
        xe_var = ctk.StringVar(value='-- Vui lòng chọn khách hàng trước --')

        xe_combo = ctk.CTkComboBox(
            scroll,
            values=['-- Vui lòng chọn khách hàng trước --'],
            variable=xe_var,
            width=680,
            height=36,
            state="readonly"
        )
        xe_combo.pack(fill='x')


        def on_kh_change(choice=None):
            """Load xe theo khách hàng"""
            val = kh_var.get()

            if not val or ' - ' not in val:
                xe_combo.configure(values=['-- Vui lòng chọn khách hàng trước --'])
                xe_var.set('-- Vui lòng chọn khách hàng trước --')
                return

            try:
                kh_id = int(val.split(' - ')[0])
                print("DEBUG KH ID:", kh_id)

                # ⚠️ FIX CỨNG: chống lỗi controller
                try:
                    xe_list = self.xe_ctrl.get_by_khach_hang(kh_id)
                except Exception as e:
                    print("Lỗi controller:", e)
                    xe_list = []

                print("DEBUG XE LIST:", xe_list)

                if not xe_list:
                    xe_combo.configure(values=['-- Khách hàng chưa có xe --'])
                    xe_var.set('-- Khách hàng chưa có xe --')
                    return

                opts = ['-- Chưa chọn xe --']
                for x in xe_list:
                    xe_id = x.get('id')
                    bien_so = x.get('bien_so', '')
                    hieu_xe = x.get('hieu_xe', '')
                    opts.append(f"{xe_id} - {bien_so} ({hieu_xe})")

                xe_combo.configure(values=opts)
                xe_var.set(opts[0])

            except Exception as e:
                print("Lỗi load xe:", e)
                xe_combo.configure(values=['-- Lỗi tải xe --'])
                xe_var.set('-- Lỗi tải xe --')


        # ✅ CHỈ DÙNG 1 CÁI → KHÔNG DÙNG trace_add NỮA
        kh_combo.configure(command=on_kh_change)

        # --- Ngày & giờ ---
        dt_row = ctk.CTkFrame(scroll, fg_color='transparent')
        dt_row.pack(fill='x', pady=4)

        ctk.CTkLabel(dt_row, text='* Ngày hẹn', font=ctk.CTkFont(size=13),
                     text_color='#a0a0a0', width=100, anchor='w').pack(side='left')
        ngay_entry = ctk.CTkEntry(dt_row, placeholder_text='YYYY-MM-DD', width=180, height=36)
        ngay_entry.pack(side='left', padx=(0, 30))

        ctk.CTkLabel(dt_row, text='* Giờ hẹn', font=ctk.CTkFont(size=13),
                     text_color='#a0a0a0', width=80, anchor='w').pack(side='left')
        gio_var = ctk.StringVar(value='08:00')
        gio_combo = ctk.CTkComboBox(dt_row, values=GIO_HEN, variable=gio_var, width=120, height=36)
        gio_combo.pack(side='left')

        # --- Ghi chú ---
        lbl(scroll, 'Ghi chú')
        ghi_chu_entry = ctk.CTkTextbox(scroll, height=70, fg_color='#2b2b2b')
        ghi_chu_entry.pack(fill='x')

        # --- Dịch vụ ---
        lbl(scroll, 'Dịch vụ đăng ký')
        dv_container = ctk.CTkFrame(scroll, fg_color='#1f1f2e', corner_radius=8)
        dv_container.pack(fill='x', pady=4)

        dv_list = self.dv_ctrl.get_all()
        dv_options = [f"{d['id']} - {d['ten_dich_vu']}" for d in dv_list]
        dv_chon_var = ctk.StringVar(value=dv_options[0] if dv_options else '')

        dv_pick_row = ctk.CTkFrame(dv_container, fg_color='transparent')
        dv_pick_row.pack(fill='x', padx=10, pady=8)

        dv_combo = ctk.CTkComboBox(dv_pick_row, values=dv_options, variable=dv_chon_var, width=460, height=34)
        dv_combo.pack(side='left', padx=(0, 10))

        sl_var = ctk.StringVar(value='1')
        ctk.CTkLabel(dv_pick_row, text='SL:', width=25, anchor='w').pack(side='left')
        sl_entry = ctk.CTkEntry(dv_pick_row, textvariable=sl_var, width=55, height=34)
        sl_entry.pack(side='left', padx=(0, 8))

        # Danh sách dịch vụ đã chọn
        dv_list_frame = ctk.CTkScrollableFrame(dv_container, height=90, fg_color='#161625')
        dv_list_frame.pack(fill='x', padx=10, pady=(0, 8))

        def refresh_dv_list():
            for w in dv_list_frame.winfo_children():
                w.destroy()
            for idx, item in enumerate(self.selected_dich_vu):
                r = ctk.CTkFrame(dv_list_frame, fg_color='#1a1a2e', corner_radius=6)
                r.pack(fill='x', pady=2)
                ctk.CTkLabel(r, text=f"• {item['ten']}  x{item['so_luong']}",
                             text_color='#e0e0e0', anchor='w').pack(side='left', padx=10)
                ctk.CTkButton(r, text='✕', width=28, height=24, fg_color='#ef4444',
                              command=lambda i=idx: remove_dv(i)).pack(side='right', padx=5)

        def add_dv():
            val = dv_chon_var.get()
            if not val or ' - ' not in val:
                return
            dv_id = int(val.split(' - ')[0])
            ten = val.split(' - ', 1)[1]
            try:
                sl = int(sl_var.get())
            except ValueError:
                sl = 1
            # Kiểm tra trùng
            for item in self.selected_dich_vu:
                if item['id_dich_vu'] == dv_id:
                    item['so_luong'] += sl
                    refresh_dv_list()
                    return
            self.selected_dich_vu.append({'id_dich_vu': dv_id, 'ten': ten, 'so_luong': sl})
            refresh_dv_list()

        def remove_dv(idx):
            self.selected_dich_vu.pop(idx)
            refresh_dv_list()

        ctk.CTkButton(dv_pick_row, text='+ Thêm', width=80, height=34,
                      fg_color='#22c55e', command=add_dv).pack(side='left')

        # --- Trạng thái (chỉ khi sửa) ---
        tt_var = ctk.StringVar(value='cho_xac_nhan')
        if row:
            lbl(scroll, 'Trạng thái')
            tt_options = list(TRANG_THAI_LABELS.values())
            tt_keys    = list(TRANG_THAI_LABELS.keys())
            tt_display = ctk.StringVar(value=TRANG_THAI_LABELS.get(row.get('trang_thai', 'cho_xac_nhan'), ''))
            tt_combo = ctk.CTkComboBox(scroll, values=tt_options, variable=tt_display, width=300, height=36)
            tt_combo.pack(anchor='w')

            def get_tt_key():
                display = tt_display.get()
                for k, v in TRANG_THAI_LABELS.items():
                    if v == display:
                        return k
                return 'cho_xac_nhan'

        # --- Nạp dữ liệu sẵn nếu là form sửa ---
        if row:
            # Khách hàng
            for opt in kh_options:
                if opt.startswith(str(row.get('id_khach_hang', '')) + ' - '):
                    kh_var.set(opt)
                    break
            on_kh_change()  # Cập nhật xe theo KH
            # Xe
            if row.get('id_xe'):
                xe_data = self.xe_ctrl.get_by_id(row['id_xe']) if row.get('id_xe') else None
                if xe_data:
                    for opt in xe_combo.cget('values'):
                        if opt.startswith(str(row['id_xe']) + ' - '):
                            xe_var.set(opt)
                            break
            # Ngày & giờ
            ngay_entry.insert(0, str(row.get('ngay_hen', '')))
            gio_val = str(row.get('gio_hen', '08:00:00'))[:5]
            gio_var.set(gio_val)
            # Ghi chú
            ghi_chu_entry.insert('1.0', row.get('ghi_chu', '') or '')
            # Dịch vụ
            refresh_dv_list()

        refresh_dv_list()

        # --- Nút lưu ---
        btn_row = ctk.CTkFrame(win, fg_color='transparent')
        btn_row.pack(pady=15)

        def save():
            kh_val = kh_var.get()
            if not kh_val or ' - ' not in kh_val:
                messagebox.showwarning('Thiếu thông tin', 'Vui lòng chọn khách hàng!', parent=win)
                return
            kh_id = int(kh_val.split(' - ')[0])

            xe_val = xe_var.get()
            xe_id = None
            if xe_val and xe_val != '-- Chưa chọn --' and ' - ' in xe_val:
                xe_id = int(xe_val.split(' - ')[0])

            ngay = ngay_entry.get().strip()
            gio  = gio_var.get().strip()
            if not ngay:
                messagebox.showwarning('Thiếu thông tin', 'Vui lòng nhập ngày hẹn!', parent=win)
                return
            # Validate ngày
            try:
                datetime.strptime(ngay, '%Y-%m-%d')
            except ValueError:
                messagebox.showwarning('Sai định dạng', 'Ngày hẹn phải có dạng YYYY-MM-DD', parent=win)
                return

            ghi_chu = ghi_chu_entry.get('1.0', 'end').strip()

            dv_save = [{'id_dich_vu': d['id_dich_vu'], 'so_luong': d['so_luong'], 'ghi_chu': ''}
                       for d in self.selected_dich_vu]

            if self.current_id:
                trang_thai = get_tt_key()
                ok, msg = self.controller.update(
                    self.current_id, kh_id, xe_id, ngay, gio, ghi_chu, trang_thai, dv_save)
            else:
                ok, msg = self.controller.add(kh_id, xe_id, ngay, gio, ghi_chu, dv_save)

            if ok:
                messagebox.showinfo('Thành công', msg, parent=win)
                win.destroy()
                self.load_data()
                if self.on_refresh:
                    self.on_refresh()
            else:
                messagebox.showerror('Lỗi', msg, parent=win)

        ctk.CTkButton(btn_row, text='💾 Lưu lịch hẹn', command=save,
                      fg_color='#4a9eff', hover_color='#357ae8',
                      width=180, height=40, font=ctk.CTkFont(size=14)).pack(side='left', padx=10)
        ctk.CTkButton(btn_row, text='❌ Hủy', command=win.destroy,
                      fg_color='#757575', hover_color='#616161',
                      width=120, height=40, font=ctk.CTkFont(size=14)).pack(side='left', padx=10)

    # ================================================================== #
    #  CHI TIẾT LỊCH HẸN                                                  #
    # ================================================================== #

    def show_chi_tiet(self, row):
        win = ctk.CTkToplevel(self.parent)
        win.title(f"Chi tiết lịch hẹn - {row.get('ma_lich', '')}")
        win.geometry('500x480')
        win.grab_set()
        win.focus_force()

        ctk.CTkLabel(win, text='📋 Chi tiết lịch hẹn', font=ctk.CTkFont(size=16, weight='bold'),
                     text_color='#4a9eff').pack(pady=(15, 5))

        info_frame = ctk.CTkFrame(win, fg_color='#1f1f2e', corner_radius=10)
        info_frame.pack(fill='x', padx=20, pady=5)

        def info_row(label, value, color='#e0e0e0'):
            r = ctk.CTkFrame(info_frame, fg_color='transparent')
            r.pack(fill='x', padx=15, pady=3)
            ctk.CTkLabel(r, text=label, width=140, anchor='w', text_color='#888888',
                         font=ctk.CTkFont(size=12)).pack(side='left')
            ctk.CTkLabel(r, text=str(value), anchor='w', text_color=color,
                         font=ctk.CTkFont(size=12)).pack(side='left')

        trang_thai = row.get('trang_thai', '')
        color_tt, _ = TRANG_THAI_COLORS.get(trang_thai, ('#888', ''))

        info_row('Mã lịch:', row.get('ma_lich', ''))
        info_row('Khách hàng:', row.get('ten_khach_hang', ''))
        info_row('Số điện thoại:', row.get('so_dien_thoai', ''))
        bien_so = row.get('bien_so_xe') or '---'
        hieu_xe = row.get('hieu_xe') or ''
        info_row('Xe:', f"{bien_so} {hieu_xe}".strip())
        info_row('Ngày hẹn:', str(row.get('ngay_hen', '')))
        info_row('Giờ hẹn:', str(row.get('gio_hen', ''))[:5])
        info_row('Trạng thái:', TRANG_THAI_LABELS.get(trang_thai, trang_thai), color_tt)
        info_row('Ghi chú:', row.get('ghi_chu', '') or '')

        # Chi tiết dịch vụ
        ctk.CTkLabel(win, text='Dịch vụ đăng ký:', font=ctk.CTkFont(size=13, weight='bold'),
                     text_color='#a0a0a0').pack(anchor='w', padx=22, pady=(10, 2))

        dv_frame = ctk.CTkScrollableFrame(win, fg_color='#161625', corner_radius=8, height=110)
        dv_frame.pack(fill='x', padx=20)

        chi_tiet = self.controller.get_chi_tiet(row['id'])
        if chi_tiet:
            for ct in chi_tiet:
                r = ctk.CTkFrame(dv_frame, fg_color='transparent')
                r.pack(fill='x', padx=5, pady=2)
                ctk.CTkLabel(r, text=f"• {ct['ten_dich_vu']}", anchor='w',
                             text_color='#e0e0e0').pack(side='left')
                ctk.CTkLabel(r, text=f"x{ct.get('so_luong', 1)}", anchor='w',
                             text_color='#4a9eff', width=40).pack(side='left', padx=10)
                gia = ct.get('don_gia', 0)
                ctk.CTkLabel(r, text=f"{int(gia):,}đ", anchor='e',
                             text_color='#f59e0b').pack(side='right', padx=10)
        else:
            ctk.CTkLabel(dv_frame, text='Chưa có dịch vụ', text_color='#888888').pack(pady=10)

        # Nút đổi trạng thái nhanh
        ctk.CTkLabel(win, text='Cập nhật trạng thái nhanh:', font=ctk.CTkFont(size=12),
                     text_color='#a0a0a0').pack(anchor='w', padx=22, pady=(12, 4))

        tt_btn_row = ctk.CTkFrame(win, fg_color='transparent')
        tt_btn_row.pack(padx=20, anchor='w')

        for key, label in TRANG_THAI_LABELS.items():
            color, _ = TRANG_THAI_COLORS[key]
            ctk.CTkButton(tt_btn_row, text=label, width=105, height=30,
                          fg_color=color, hover_color=color,
                          font=ctk.CTkFont(size=11),
                          command=lambda k=key: self._quick_update_tt(row['id'], k, win)
                          ).pack(side='left', padx=3)

        ctk.CTkButton(win, text='Đóng', command=win.destroy,
                      width=120, height=36, fg_color='#757575').pack(pady=12)

    def _quick_update_tt(self, id, trang_thai, win):
        ok = self.controller.update_trang_thai(id, trang_thai)
        if ok:
            messagebox.showinfo('Thành công', f"Đã cập nhật: {TRANG_THAI_LABELS[trang_thai]}", parent=win)
            win.destroy()
            self.load_data()
        else:
            messagebox.showerror('Lỗi', 'Không thể cập nhật trạng thái.', parent=win)

    # ================================================================== #
    #  XÓA                                                                 #
    # ================================================================== #

    def delete_lich(self, id):
        if not messagebox.askyesno('Xác nhận', 'Bạn có chắc muốn xóa lịch hẹn này?'):
            return
        ok = self.controller.delete(id)
        if ok:
            messagebox.showinfo('Thành công', 'Đã xóa lịch hẹn.')
            self.load_data()
            if self.on_refresh:
                self.on_refresh()
        else:
            messagebox.showerror('Lỗi', 'Không thể xóa lịch hẹn.')
