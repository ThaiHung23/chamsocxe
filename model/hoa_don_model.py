from .database import Database
from datetime import datetime

class HoaDonModel:
    def __init__(self):
        self.db = Database()
    
    def get_all(self):
        query = """SELECT hd.*, xe.bien_so, kh.ho_ten as ten_chu_xe 
                   FROM hoa_don hd
                   LEFT JOIN xe ON hd.id_xe = xe.id
                   LEFT JOIN khach_hang kh ON xe.id_khach_hang = kh.id
                   ORDER BY hd.id DESC"""
        return self.db.fetch_all(query)
    
    def get_by_id(self, id):
        query = """SELECT hd.*, xe.bien_so, kh.ho_ten as ten_chu_xe 
                   FROM hoa_don hd
                   LEFT JOIN xe ON hd.id_xe = xe.id
                   LEFT JOIN khach_hang kh ON xe.id_khach_hang = kh.id
                   WHERE hd.id = %s"""
        return self.db.fetch_one(query, (id,))
    
    def get_chi_tiet(self, id_hoa_don):
        query = """SELECT ct.*, dv.ten_dich_vu, dv.don_gia as gia_goc
                   FROM chi_tiet_hoa_don ct
                   JOIN dich_vu dv ON ct.id_dich_vu = dv.id
                   WHERE ct.id_hoa_don = %s"""
        return self.db.fetch_all(query, (id_hoa_don,))
    
    def create(self, id_xe):
        # Kiểm tra xe tồn tại
        check_query = "SELECT id FROM xe WHERE id = %s"
        xe = self.db.fetch_one(check_query, (id_xe,))
        if not xe:
            print(f"Không tìm thấy xe với ID: {id_xe}")
            return None
        
        # Tạo mã hóa đơn tự động
        ma_hd = f"HD{datetime.now().strftime('%Y%m%d%H%M%S')}"
        query = "INSERT INTO hoa_don (ma_hd, id_xe, ngay_lap, trang_thai) VALUES (%s, %s, %s, 'dang_xu_ly')"
        result = self.db.insert(query, (ma_hd, id_xe, datetime.now()))
        print(f"Tạo hóa đơn: ID={result}, Mã={ma_hd}")
        return result
    
    def add_service(self, id_hoa_don, id_dich_vu, so_luong, don_gia):
        try:
            # Kiểm tra hóa đơn tồn tại
            check_hd = self.get_by_id(id_hoa_don)
            if not check_hd:
                print(f"Không tìm thấy hóa đơn với ID: {id_hoa_don}")
                return False
            
            # Kiểm tra dịch vụ tồn tại
            check_dv_query = "SELECT id FROM dich_vu WHERE id = %s"
            dv = self.db.fetch_one(check_dv_query, (id_dich_vu,))
            if not dv:
                print(f"Không tìm thấy dịch vụ với ID: {id_dich_vu}")
                return False
            
            # Tính thành tiền
            thanh_tien = so_luong * don_gia
            
            # Thêm chi tiết hóa đơn
            query = """INSERT INTO chi_tiet_hoa_don (id_hoa_don, id_dich_vu, so_luong, don_gia, thanh_tien) 
                       VALUES (%s, %s, %s, %s, %s)"""
            result = self.db.insert(query, (id_hoa_don, id_dich_vu, so_luong, don_gia, thanh_tien))
            
            if result:
                print(f"Đã thêm dịch vụ vào hóa đơn {id_hoa_don}, kết quả: {result}")
                # Cập nhật tổng tiền hóa đơn
                self.update_total(id_hoa_don)
                return True
            return False
        except Exception as e:
            print(f"Lỗi khi thêm dịch vụ: {e}")
            return False
    
    def update_total(self, id_hoa_don):
        query = """UPDATE hoa_don 
                   SET tong_tien = (SELECT COALESCE(SUM(thanh_tien), 0) FROM chi_tiet_hoa_don WHERE id_hoa_don = %s)
                   WHERE id = %s"""
        self.db.update(query, (id_hoa_don, id_hoa_don))
        print(f"Đã cập nhật tổng tiền cho hóa đơn {id_hoa_don}")
    
    def update_status(self, id, trang_thai):
        query = "UPDATE hoa_don SET trang_thai = %s WHERE id = %s"
        affected = self.db.update(query, (trang_thai, id))
        return affected > 0
    
    def delete(self, id):
        query = "DELETE FROM hoa_don WHERE id = %s"
        affected = self.db.delete(query, (id,))
        return affected > 0
    
    def get_thong_ke(self, from_date=None, to_date=None, include_all_status=False):
        """Lấy thống kê doanh thu
        
        Args:
            from_date: Ngày bắt đầu (format: YYYY-MM-DD)
            to_date: Ngày kết thúc (format: YYYY-MM-DD)
            include_all_status: Nếu True thì lấy tất cả, False chỉ lấy hoàn thành
        """
        try:
            print(f"DEBUG get_thong_ke: from={from_date}, to={to_date}, include_all={include_all_status}")
            
            if from_date and to_date:
                if include_all_status:
                    # Lấy tất cả hóa đơn (kể cả chưa hoàn thành)
                    query = """SELECT DATE(ngay_lap) as ngay, 
                                      COUNT(*) as so_luong, 
                                      COALESCE(SUM(tong_tien), 0) as doanh_thu 
                               FROM hoa_don 
                               WHERE DATE(ngay_lap) BETWEEN %s AND %s
                               GROUP BY DATE(ngay_lap)
                               ORDER BY ngay DESC"""
                    result = self.db.fetch_all(query, (from_date, to_date))
                    print(f"DEBUG get_thong_ke (all): tìm thấy {len(result) if result else 0} ngày có dữ liệu")
                    return result if result else []
                else:
                    # Chỉ lấy hóa đơn hoàn thành
                    query = """SELECT DATE(ngay_lap) as ngay, 
                                      COUNT(*) as so_luong, 
                                      COALESCE(SUM(tong_tien), 0) as doanh_thu 
                               FROM hoa_don 
                               WHERE trang_thai = 'hoan_thanh' 
                               AND DATE(ngay_lap) BETWEEN %s AND %s
                               GROUP BY DATE(ngay_lap)
                               ORDER BY ngay DESC"""
                    result = self.db.fetch_all(query, (from_date, to_date))
                    print(f"DEBUG get_thong_ke (completed): tìm thấy {len(result) if result else 0} ngày có dữ liệu")
                    return result if result else []
            else:
                # Không có ngày, lấy 30 ngày gần nhất
                if include_all_status:
                    query = """SELECT DATE(ngay_lap) as ngay, 
                                      COUNT(*) as so_luong, 
                                      COALESCE(SUM(tong_tien), 0) as doanh_thu 
                               FROM hoa_don 
                               GROUP BY DATE(ngay_lap)
                               ORDER BY ngay DESC
                               LIMIT 30"""
                    result = self.db.fetch_all(query)
                    return result if result else []
                else:
                    query = """SELECT DATE(ngay_lap) as ngay, 
                                      COUNT(*) as so_luong, 
                                      COALESCE(SUM(tong_tien), 0) as doanh_thu 
                               FROM hoa_don 
                               WHERE trang_thai = 'hoan_thanh'
                               GROUP BY DATE(ngay_lap)
                               ORDER BY ngay DESC
                               LIMIT 30"""
                    result = self.db.fetch_all(query)
                    return result if result else []
        except Exception as e:
            print(f"Lỗi trong get_thong_ke: {e}")
            import traceback
            traceback.print_exc()
            return []