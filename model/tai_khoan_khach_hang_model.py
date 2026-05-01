from .database import Database
from datetime import datetime

class TaiKhoanKhachHangModel:
    def __init__(self):
        self.db = Database()
    
    def get_by_username(self, username):
        query = """SELECT tk.*, kh.ho_ten, kh.so_dien_thoai, kh.email, kh.dia_chi 
                   FROM tai_khoan_khach_hang tk
                   JOIN khach_hang kh ON tk.id_khach_hang = kh.id
                   WHERE tk.username = %s AND tk.trang_thai = 1"""
        return self.db.fetch_one(query, (username,))
    
    def login(self, username, password):
        user = self.get_by_username(username)
        if user and user['password'] == password:
            return user
        return None