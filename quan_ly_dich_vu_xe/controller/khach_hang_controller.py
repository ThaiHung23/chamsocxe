from model.khach_hang_model import KhachHangModel

class KhachHangController:
    def __init__(self):
        self.model = KhachHangModel()
    
    def get_all(self):
        return self.model.get_all()
    
    def get_by_id(self, id):
        return self.model.get_by_id(id)
    
    def search(self, keyword):
        return self.model.search(keyword)
    
    def add(self, ho_ten, so_dien_thoai, email, dia_chi):
        try:
            if not ho_ten or not so_dien_thoai:
                print("Lỗi: Họ tên và số điện thoại không được để trống")
                return False
            result = self.model.add(ho_ten, so_dien_thoai, email, dia_chi)
            print(f"Kết quả thêm khách hàng: {result}")
            return result
        except Exception as e:
            print(f"Lỗi trong controller: {e}")
            return False
    
    def update(self, id, ho_ten, so_dien_thoai, email, dia_chi):
        try:
            result = self.model.update(id, ho_ten, so_dien_thoai, email, dia_chi)
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