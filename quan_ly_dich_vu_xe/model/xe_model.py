from .database import Database

class XeModel:
    def __init__(self):
        self.db = Database()
    
    def get_all(self):
        query = """SELECT xe.*, khach_hang.ho_ten as ten_chu_xe 
                   FROM xe 
                   LEFT JOIN khach_hang ON xe.id_khach_hang = khach_hang.id 
                   ORDER BY xe.id DESC"""
        return self.db.fetch_all(query)
    
    def get_by_khach_hang(self, id_khach_hang):
        query = "SELECT * FROM xe WHERE id_khach_hang = %s"
        return self.db.fetch_all(query, (id_khach_hang,))
    
    def get_by_id(self, id):
        query = """SELECT xe.*, khach_hang.ho_ten as ten_chu_xe 
                   FROM xe 
                   LEFT JOIN khach_hang ON xe.id_khach_hang = khach_hang.id 
                   WHERE xe.id = %s"""
        return self.db.fetch_one(query, (id,))
    
    def add(self, bien_so, hieu_xe, model, mau_sac, nam_sx, id_khach_hang):
        query = """INSERT INTO xe (bien_so, hieu_xe, model, mau_sac, nam_sx, id_khach_hang) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        result = self.db.insert(query, (bien_so.upper(), hieu_xe, model, mau_sac, nam_sx, id_khach_hang))
        return result is not None
    
    def update(self, id, bien_so, hieu_xe, model, mau_sac, nam_sx, id_khach_hang):
        query = """UPDATE xe 
                   SET bien_so = %s, hieu_xe = %s, model = %s, 
                       mau_sac = %s, nam_sx = %s, id_khach_hang = %s 
                   WHERE id = %s"""
        affected = self.db.update(query, (bien_so.upper(), hieu_xe, model, mau_sac, nam_sx, id_khach_hang, id))
        return affected > 0
    
    def delete(self, id):
        query = "DELETE FROM xe WHERE id = %s"
        affected = self.db.delete(query, (id,))
        return affected > 0
    
    def search(self, keyword):
        query = """SELECT xe.*, khach_hang.ho_ten as ten_chu_xe 
                   FROM xe 
                   LEFT JOIN khach_hang ON xe.id_khach_hang = khach_hang.id 
                   WHERE xe.bien_so LIKE %s 
                   OR xe.hieu_xe LIKE %s 
                   OR khach_hang.ho_ten LIKE %s
                   ORDER BY xe.id DESC"""
        keyword = f"%{keyword}%"
        return self.db.fetch_all(query, (keyword, keyword, keyword))