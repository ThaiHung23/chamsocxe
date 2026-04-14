from model.dich_vu_model import DichVuModel

class DichVuController:
    def __init__(self):
        self.model = DichVuModel()
    
    def get_all(self):
        return self.model.get_all()
    
    def get_by_id(self, id):
        return self.model.get_by_id(id)
    
    def search(self, keyword):
        return self.model.search(keyword)
    
    def add(self, ma_dv, ten_dich_vu, don_gia, thoi_gian_du_kien, mo_ta):
        try:
            if not ma_dv or not ten_dich_vu or not don_gia:
                print("Lỗi: Mã DV, tên DV và đơn giá không được để trống")
                return False
            result = self.model.add(ma_dv, ten_dich_vu, don_gia, thoi_gian_du_kien, mo_ta)
            print(f"Kết quả thêm dịch vụ: {result}")
            return result
        except Exception as e:
            print(f"Lỗi trong controller: {e}")
            return False
    
    def update(self, id, ma_dv, ten_dich_vu, don_gia, thoi_gian_du_kien, mo_ta):
        try:
            result = self.model.update(id, ma_dv, ten_dich_vu, don_gia, thoi_gian_du_kien, mo_ta)
            return result
        except Exception as e:
            print(f"Lỗi cập nhật: {e}")
            return False
    
    def delete(self, id):
        try:
            result = self.model.delete(id)
            return result
        except Exception as e:
            print(f"Lỗi xóa: {e}")
            return False