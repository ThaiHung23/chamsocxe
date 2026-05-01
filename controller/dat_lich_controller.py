from model.dat_lich_model import DatLichModel


class DatLichController:
    def __init__(self):
        self.model = DatLichModel()

    def get_all(self):
        return self.model.get_all()

    def get_by_id(self, id):
        return self.model.get_by_id(id)

    def get_by_ngay(self, ngay):
        return self.model.get_by_ngay(ngay)

    def get_by_thang(self, nam, thang):
        return self.model.get_by_thang(nam, thang)

    def search(self, keyword):
        return self.model.search(keyword)

    def get_chi_tiet(self, id_dat_lich):
        return self.model.get_chi_tiet(id_dat_lich)

    def get_total(self):
        return self.model.get_total()

    def get_total_hom_nay(self):
        return self.model.get_total_hom_nay()

    def add(self, id_khach_hang, id_xe, ngay_hen, gio_hen, ghi_chu='', danh_sach_dich_vu=None):
        try:
            if not id_khach_hang or not ngay_hen or not gio_hen:
                return False, "Vui lòng điền đầy đủ thông tin bắt buộc."
            result = self.model.add(id_khach_hang, id_xe, ngay_hen, gio_hen, ghi_chu, danh_sach_dich_vu)
            if result:
                return True, "Đặt lịch thành công!"
            return False, "Không thể thêm lịch hẹn."
        except Exception as e:
            print(f"Lỗi thêm lịch: {e}")
            return False, str(e)

    def update(self, id, id_khach_hang, id_xe, ngay_hen, gio_hen, ghi_chu, trang_thai, danh_sach_dich_vu=None):
        try:
            result = self.model.update(id, id_khach_hang, id_xe, ngay_hen, gio_hen, ghi_chu, trang_thai, danh_sach_dich_vu)
            if result:
                return True, "Cập nhật lịch hẹn thành công!"
            return False, "Không tìm thấy lịch hẹn cần cập nhật."
        except Exception as e:
            print(f"Lỗi cập nhật lịch: {e}")
            return False, str(e)

    def update_trang_thai(self, id, trang_thai):
        try:
            result = self.model.update_trang_thai(id, trang_thai)
            return result
        except Exception as e:
            print(f"Lỗi cập nhật trạng thái: {e}")
            return False

    def delete(self, id):
        try:
            result = self.model.delete(id)
            return result
        except Exception as e:
            print(f"Lỗi xóa lịch: {e}")
            return False

    def get_by_khach_hang(self, khach_hang_id):
        """Lấy danh sách lịch hẹn theo ID khách hàng"""
        try:
            return self.model.get_by_khach_hang(khach_hang_id)
        except Exception as e:
            print(f"Lỗi lấy lịch theo khách hàng: {e}")
            return []