from model.hoa_don_model import HoaDonModel

class HoaDonController:
    def __init__(self):
        self.model = HoaDonModel()
    
    def get_all(self):
        return self.model.get_all()
    
    def get_by_id(self, id):
        return self.model.get_by_id(id)
    
    def get_chi_tiet(self, id_hoa_don):
        return self.model.get_chi_tiet(id_hoa_don)
    
    def create(self, id_xe):
        try:
            if not id_xe:
                print("Lỗi: ID xe không được để trống")
                return None
            result = self.model.create(id_xe)
            print(f"Kết quả tạo hóa đơn: {result}")
            return result
        except Exception as e:
            print(f"Lỗi trong controller: {e}")
            return None
    
    def add_service(self, id_hoa_don, id_dich_vu, so_luong, don_gia):
        try:
            result = self.model.add_service(id_hoa_don, id_dich_vu, so_luong, don_gia)
            print(f"Kết quả thêm dịch vụ vào hóa đơn: {result}")
            return result
        except Exception as e:
            print(f"Lỗi trong controller: {e}")
            return False
    
    def update_status(self, id, trang_thai):
        try:
            result = self.model.update_status(id, trang_thai)
            return result
        except Exception as e:
            print(f"Lỗi cập nhật trạng thái: {e}")
            return False
    
    def delete(self, id):
        try:
            result = self.model.delete(id)
            return result
        except Exception as e:
            print(f"Lỗi xóa: {e}")
            return False
    
    def thong_ke(self, from_date=None, to_date=None, include_all_status=False):
        """Thống kê doanh thu
        
        Args:
            from_date: Ngày bắt đầu (string YYYY-MM-DD)
            to_date: Ngày kết thúc (string YYYY-MM-DD)
            include_all_status: Nếu True thì thống kê tất cả, False chỉ thống kê hoàn thành
        """
        try:
            result = self.model.get_thong_ke(from_date, to_date, include_all_status)
            print(f"DEBUG thong_ke controller: {len(result) if result else 0} records, include_all={include_all_status}")
            return result if result else []
        except Exception as e:
            print(f"Lỗi trong thong_ke controller: {e}")
            import traceback
            traceback.print_exc()
            return []
        
    def get_by_khach_hang(self, khach_hang_id):
        """Lấy danh sách hóa đơn theo ID khách hàng"""
        try:
            return self.model.get_by_khach_hang(khach_hang_id)
        except Exception as e:
            print(f"Lỗi lấy hóa đơn theo khách hàng: {e}")
            return []