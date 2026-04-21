from model.xe_model import XeModel

class XeController:
    def __init__(self):
        self.model = XeModel()
    
    def get_all(self):
        return self.model.get_all()
    
    def get_by_id(self, id):
        return self.model.get_by_id(id)
    
    def search(self, keyword):
        return self.model.search(keyword)
    
    def add(self, bien_so, hieu_xe, model, mau_sac, nam_sx, id_khach_hang):
        try:
            if not bien_so or not hieu_xe or not id_khach_hang:
                print("Lỗi: Biển số, hiệu xe và ID khách hàng không được để trống")
                return False
            result = self.model.add(bien_so, hieu_xe, model, mau_sac, nam_sx, id_khach_hang)
            print(f"Kết quả thêm xe: {result}")
            return result
        except Exception as e:
            print(f"Lỗi trong controller: {e}")
            return False
    
    def update(self, id, bien_so, hieu_xe, model, mau_sac, nam_sx, id_khach_hang):
        try:
            result = self.model.update(id, bien_so, hieu_xe, model, mau_sac, nam_sx, id_khach_hang)
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