from .database import Database
from datetime import datetime


class DatLichModel:
    def __init__(self):
        self.db = Database()

    # ------------------------------------------------------------------ #
    #  Truy vấn                                                            #
    # ------------------------------------------------------------------ #

    def get_all(self):
        query = """
            SELECT dl.*,
                   kh.ho_ten  AS ten_khach_hang,
                   kh.so_dien_thoai,
                   xe.bien_so AS bien_so_xe,
                   xe.hieu_xe
            FROM dat_lich dl
            LEFT JOIN khach_hang kh ON dl.id_khach_hang = kh.id
            LEFT JOIN xe          xe ON dl.id_xe         = xe.id
            ORDER BY dl.ngay_hen DESC, dl.gio_hen DESC
        """
        return self.db.fetch_all(query)

    def get_by_id(self, id):
        query = """
            SELECT dl.*,
                   kh.ho_ten  AS ten_khach_hang,
                   kh.so_dien_thoai,
                   xe.bien_so AS bien_so_xe,
                   xe.hieu_xe
            FROM dat_lich dl
            LEFT JOIN khach_hang kh ON dl.id_khach_hang = kh.id
            LEFT JOIN xe          xe ON dl.id_xe         = xe.id
            WHERE dl.id = %s
        """
        return self.db.fetch_one(query, (id,))

    def get_by_ngay(self, ngay):
        """Lấy lịch theo ngày (ngay dạng 'YYYY-MM-DD')"""
        query = """
            SELECT dl.*,
                   kh.ho_ten  AS ten_khach_hang,
                   kh.so_dien_thoai,
                   xe.bien_so AS bien_so_xe,
                   xe.hieu_xe
            FROM dat_lich dl
            LEFT JOIN khach_hang kh ON dl.id_khach_hang = kh.id
            LEFT JOIN xe          xe ON dl.id_xe         = xe.id
            WHERE dl.ngay_hen = %s
            ORDER BY dl.gio_hen
        """
        return self.db.fetch_all(query, (ngay,))

    def get_by_thang(self, nam, thang):
        query = """
            SELECT dl.*,
                   kh.ho_ten  AS ten_khach_hang,
                   kh.so_dien_thoai,
                   xe.bien_so AS bien_so_xe,
                   xe.hieu_xe
            FROM dat_lich dl
            LEFT JOIN khach_hang kh ON dl.id_khach_hang = kh.id
            LEFT JOIN xe          xe ON dl.id_xe         = xe.id
            WHERE YEAR(dl.ngay_hen) = %s AND MONTH(dl.ngay_hen) = %s
            ORDER BY dl.ngay_hen, dl.gio_hen
        """
        return self.db.fetch_all(query, (nam, thang))

    def search(self, keyword):
        query = """
            SELECT dl.*,
                   kh.ho_ten  AS ten_khach_hang,
                   kh.so_dien_thoai,
                   xe.bien_so AS bien_so_xe,
                   xe.hieu_xe
            FROM dat_lich dl
            LEFT JOIN khach_hang kh ON dl.id_khach_hang = kh.id
            LEFT JOIN xe          xe ON dl.id_xe         = xe.id
            WHERE kh.ho_ten       LIKE %s
               OR kh.so_dien_thoai LIKE %s
               OR xe.bien_so       LIKE %s
               OR dl.ma_lich       LIKE %s
            ORDER BY dl.ngay_hen DESC, dl.gio_hen DESC
        """
        kw = f"%{keyword}%"
        return self.db.fetch_all(query, (kw, kw, kw, kw))

    def get_chi_tiet(self, id_dat_lich):
        query = """
            SELECT cdl.*, dv.ten_dich_vu, dv.don_gia, dv.thoi_gian_du_kien
            FROM chi_tiet_dat_lich cdl
            JOIN dich_vu dv ON cdl.id_dich_vu = dv.id
            WHERE cdl.id_dat_lich = %s
        """
        return self.db.fetch_all(query, (id_dat_lich,))

    def get_total(self):
        result = self.db.fetch_one("SELECT COUNT(*) AS total FROM dat_lich")
        return result['total'] if result else 0

    def get_total_hom_nay(self):
        result = self.db.fetch_one(
            "SELECT COUNT(*) AS total FROM dat_lich WHERE ngay_hen = CURDATE()"
        )
        return result['total'] if result else 0

    # ------------------------------------------------------------------ #
    #  Thêm / Sửa / Xóa                                                   #
    # ------------------------------------------------------------------ #

    def _gen_ma_lich(self):
        ma = f"DL{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return ma

    def add(self, id_khach_hang, id_xe, ngay_hen, gio_hen, ghi_chu, danh_sach_dich_vu=None):
        """
        danh_sach_dich_vu: list of dict {'id_dich_vu': int, 'so_luong': int, 'ghi_chu': str}
        """
        ma_lich = self._gen_ma_lich()
        query = """
            INSERT INTO dat_lich (ma_lich, id_khach_hang, id_xe, ngay_hen, gio_hen, ghi_chu, trang_thai)
            VALUES (%s, %s, %s, %s, %s, %s, 'cho_xac_nhan')
        """
        new_id = self.db.insert(query, (ma_lich, id_khach_hang, id_xe, ngay_hen, gio_hen, ghi_chu))
        if new_id and danh_sach_dich_vu:
            self._add_chi_tiet(new_id, danh_sach_dich_vu)
        return new_id is not None

    def _add_chi_tiet(self, id_dat_lich, danh_sach_dich_vu):
        for item in danh_sach_dich_vu:
            query = """
                INSERT INTO chi_tiet_dat_lich (id_dat_lich, id_dich_vu, so_luong, ghi_chu)
                VALUES (%s, %s, %s, %s)
            """
            self.db.insert(query, (
                id_dat_lich,
                item.get('id_dich_vu'),
                item.get('so_luong', 1),
                item.get('ghi_chu', '')
            ))

    def update(self, id, id_khach_hang, id_xe, ngay_hen, gio_hen, ghi_chu, trang_thai, danh_sach_dich_vu=None):
        query = """
            UPDATE dat_lich
            SET id_khach_hang = %s, id_xe = %s, ngay_hen = %s,
                gio_hen = %s, ghi_chu = %s, trang_thai = %s
            WHERE id = %s
        """
        affected = self.db.update(query, (id_khach_hang, id_xe, ngay_hen, gio_hen, ghi_chu, trang_thai, id))
        if affected > 0 and danh_sach_dich_vu is not None:
            # Xóa chi tiết cũ rồi thêm lại
            self.db.delete("DELETE FROM chi_tiet_dat_lich WHERE id_dat_lich = %s", (id,))
            self._add_chi_tiet(id, danh_sach_dich_vu)
        return affected > 0

    def update_trang_thai(self, id, trang_thai):
        query = "UPDATE dat_lich SET trang_thai = %s WHERE id = %s"
        affected = self.db.update(query, (trang_thai, id))
        return affected > 0

    def delete(self, id):
        query = "DELETE FROM dat_lich WHERE id = %s"
        affected = self.db.delete(query, (id,))
        return affected > 0

 

    def get_by_khach_hang(self, khach_hang_id):
        """Lấy danh sách lịch hẹn theo ID khách hàng"""
        query = """
            SELECT dl.*,
                kh.ho_ten AS ten_khach_hang,
                kh.so_dien_thoai,
                xe.bien_so AS bien_so_xe,
                xe.hieu_xe,
                (SELECT GROUP_CONCAT(dv.ten_dich_vu SEPARATOR ', ') 
                    FROM chi_tiet_dat_lich cdl 
                    JOIN dich_vu dv ON cdl.id_dich_vu = dv.id 
                    WHERE cdl.id_dat_lich = dl.id) AS ten_dich_vu
            FROM dat_lich dl
            LEFT JOIN khach_hang kh ON dl.id_khach_hang = kh.id
            LEFT JOIN xe xe ON dl.id_xe = xe.id
            WHERE dl.id_khach_hang = %s
            ORDER BY dl.ngay_hen DESC, dl.gio_hen DESC
        """
        return self.db.fetch_all(query, (khach_hang_id,))