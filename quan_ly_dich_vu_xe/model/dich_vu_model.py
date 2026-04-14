from .database import Database

class DichVuModel:
    def __init__(self):
        self.db = Database()
    
    def get_all(self):
        query = "SELECT * FROM dich_vu ORDER BY id DESC"
        return self.db.fetch_all(query)
    
    def get_by_id(self, id):
        query = "SELECT * FROM dich_vu WHERE id = %s"
        return self.db.fetch_one(query, (id,))
    
    def add(self, ma_dv, ten_dich_vu, don_gia, thoi_gian_du_kien, mo_ta):
        query = """INSERT INTO dich_vu (ma_dv, ten_dich_vu, don_gia, thoi_gian_du_kien, mo_ta) 
                   VALUES (%s, %s, %s, %s, %s)"""
        result = self.db.insert(query, (ma_dv, ten_dich_vu, don_gia, thoi_gian_du_kien, mo_ta))
        return result is not None
    
    def update(self, id, ma_dv, ten_dich_vu, don_gia, thoi_gian_du_kien, mo_ta):
        query = """UPDATE dich_vu 
                   SET ma_dv = %s, ten_dich_vu = %s, don_gia = %s, 
                       thoi_gian_du_kien = %s, mo_ta = %s 
                   WHERE id = %s"""
        affected = self.db.update(query, (ma_dv, ten_dich_vu, don_gia, thoi_gian_du_kien, mo_ta, id))
        return affected > 0
    
    def delete(self, id):
        query = "DELETE FROM dich_vu WHERE id = %s"
        affected = self.db.delete(query, (id,))
        return affected > 0
    
    def search(self, keyword):
        query = """SELECT * FROM dich_vu 
                   WHERE ten_dich_vu LIKE %s 
                   OR ma_dv LIKE %s
                   ORDER BY id DESC"""
        keyword = f"%{keyword}%"
        return self.db.fetch_all(query, (keyword, keyword))