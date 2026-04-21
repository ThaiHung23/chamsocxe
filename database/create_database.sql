-- Tạo database
CREATE DATABASE IF NOT EXISTS quan_ly_dich_vu_xe;
USE quan_ly_dich_vu_xe;

-- Bảng khách hàng
CREATE TABLE IF NOT EXISTS khach_hang (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ma_kh VARCHAR(20) UNIQUE,
    ho_ten VARCHAR(100) NOT NULL,
    so_dien_thoai VARCHAR(15) NOT NULL UNIQUE,
    email VARCHAR(100),
    dia_chi TEXT,
    ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Bảng xe
CREATE TABLE IF NOT EXISTS xe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bien_so VARCHAR(20) UNIQUE NOT NULL,
    hieu_xe VARCHAR(50) NOT NULL,
    model VARCHAR(50),
    mau_sac VARCHAR(30),
    nam_sx INT,
    id_khach_hang INT,
    FOREIGN KEY (id_khach_hang) REFERENCES khach_hang(id) ON DELETE CASCADE
);

-- Bảng dịch vụ
CREATE TABLE IF NOT EXISTS dich_vu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ma_dv VARCHAR(20) UNIQUE,
    ten_dich_vu VARCHAR(100) NOT NULL,
    don_gia DECIMAL(12,2) NOT NULL,
    thoi_gian_du_kien INT COMMENT 'Thời gian dự kiến (phút)',
    mo_ta TEXT
);

-- Bảng hóa đơn
CREATE TABLE IF NOT EXISTS hoa_don (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ma_hd VARCHAR(20) UNIQUE,
    ngay_lap DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_xe INT,
    tong_tien DECIMAL(12,2) DEFAULT 0,
    trang_thai ENUM('dang_xu_ly','hoan_thanh','da_huy') DEFAULT 'dang_xu_ly',
    ghi_chu TEXT,
    FOREIGN KEY (id_xe) REFERENCES xe(id)
);

-- Bảng chi tiết hóa đơn
CREATE TABLE IF NOT EXISTS chi_tiet_hoa_don (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_hoa_don INT,
    id_dich_vu INT,
    so_luong INT DEFAULT 1,
    don_gia DECIMAL(12,2),
    thanh_tien DECIMAL(12,2),
    FOREIGN KEY (id_hoa_don) REFERENCES hoa_don(id) ON DELETE CASCADE,
    FOREIGN KEY (id_dich_vu) REFERENCES dich_vu(id)
);

-- Bảng người dùng (cho đăng nhập)
CREATE TABLE IF NOT EXISTS nguoi_dung (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    ho_ten VARCHAR(100),
    vai_tro ENUM('admin','nhan_vien') DEFAULT 'nhan_vien',
    trang_thai BOOLEAN DEFAULT TRUE
);

-- Thêm dữ liệu mẫu
INSERT INTO dich_vu (ma_dv, ten_dich_vu, don_gia, thoi_gian_du_kien) VALUES
('DV001', 'Rửa xe', 50000, 30),
('DV002', 'Thay nhớt', 200000, 45),
('DV003', 'Cân chỉnh động cơ', 500000, 120),
('DV004', 'Vệ sinh nội thất', 150000, 60),
('DV005', 'Đánh bóng sơn', 300000, 90);

-- Thêm tài khoản mặc định
INSERT INTO nguoi_dung (username, password, ho_ten, vai_tro) VALUES
('admin', '123456', 'Quản trị viên', 'admin'),
('nhanvien1', '123456', 'Nguyễn Văn A', 'nhan_vien');