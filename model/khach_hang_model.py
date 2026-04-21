from .database import Database
from datetime import datetime

class KhachHangModel:
    def __init__(self):
        self.db = Database()
    
    def get_all(self):
        query = "SELECT * FROM khach_hang ORDER BY id DESC"
        return self.db.fetch_all(query)
    
    def get_by_id(self, id):
        query = "SELECT * FROM khach_hang WHERE id = %s"
        return self.db.fetch_one(query, (id,))
    
    def search(self, keyword):
        query = """SELECT * FROM khach_hang 
                   WHERE ho_ten LIKE %s 
                   OR so_dien_thoai LIKE %s 
                   OR ma_kh LIKE %s
                   ORDER BY id DESC"""
        keyword = f"%{keyword}%"
        return self.db.fetch_all(query, (keyword, keyword, keyword))
    
    def add(self, ho_ten, so_dien_thoai, email, dia_chi):
        # Tạo mã khách hàng tự động
        ma_kh = f"KH{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        query = """INSERT INTO khach_hang (ma_kh, ho_ten, so_dien_thoai, email, dia_chi, ngay_tao) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        
        result = self.db.insert(query, (ma_kh, ho_ten, so_dien_thoai, email, dia_chi, datetime.now()))
        return result is not None
    
    def update(self, id, ho_ten, so_dien_thoai, email, dia_chi):
        query = """UPDATE khach_hang 
                   SET ho_ten = %s, so_dien_thoai = %s, email = %s, dia_chi = %s 
                   WHERE id = %s"""
        affected = self.db.update(query, (ho_ten, so_dien_thoai, email, dia_chi, id))
        return affected > 0
    
    def delete(self, id):
        query = "DELETE FROM khach_hang WHERE id = %s"
        affected = self.db.delete(query, (id,))
        return affected > 0
    
    def get_total(self):
        query = "SELECT COUNT(*) as total FROM khach_hang"
        result = self.db.fetch_one(query)
        return result['total'] if result else 0
    
    def get_cars_by_customer(self, customer_id):
        """Lấy danh sách xe theo ID khách hàng"""
        try:
            query = """SELECT x.*, kh.ho_ten as ten_chu_xe 
                       FROM xe x
                       LEFT JOIN khach_hang kh ON x.id_khach_hang = kh.id
                       WHERE x.id_khach_hang = %s
                       ORDER BY x.id DESC"""
            result = self.db.fetch_all(query, (customer_id,))
            print(f"DEBUG: Tìm thấy {len(result) if result else 0} xe cho KH ID {customer_id}")
            return result if result else []
        except Exception as e:
            print(f"Lỗi truy vấn xe theo khách hàng: {e}")
            return []