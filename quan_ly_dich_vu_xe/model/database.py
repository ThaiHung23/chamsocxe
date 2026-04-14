import mysql.connector
from mysql.connector import Error
import hashlib

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_connection(self):
        """Tạo kết nối mới mỗi lần"""
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='quan_ly_dich_vu_xe',
                user='root',
                password='',
                autocommit=True,
                use_pure=True
            )
            return connection
        except Error as e:
            print(f"Lỗi kết nối database: {e}")
            return None
    
    def execute_query(self, query, params=None, fetch=False):
        """Thực thi query và trả về kết quả"""
        connection = self.get_connection()
        if not connection:
            return None if not fetch else []
        
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
                if query.strip().upper().startswith('INSERT'):
                    return cursor.lastrowid
                else:
                    return cursor.rowcount
        except Error as e:
            print(f"Lỗi thực thi query: {e}")
            print(f"Query: {query}")
            print(f"Params: {params}")
            return None if not fetch else []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def fetch_all(self, query, params=None):
        """Lấy tất cả kết quả"""
        return self.execute_query(query, params, fetch=True) or []
    
    def fetch_one(self, query, params=None):
        """Lấy một kết quả"""
        results = self.fetch_all(query, params)
        return results[0] if results else None
    
    def insert(self, query, params=None):
        """Thực thi INSERT và trả về ID"""
        result = self.execute_query(query, params, fetch=False)
        return result if result and result > 0 else None
    
    def update(self, query, params=None):
        """Thực thi UPDATE và trả về số dòng affected"""
        result = self.execute_query(query, params, fetch=False)
        return result if result is not None else 0
    
    def delete(self, query, params=None):
        """Thực thi DELETE"""
        return self.update(query, params)
    
    @staticmethod
    def hash_password(password):
        """Hash mật khẩu bằng SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()