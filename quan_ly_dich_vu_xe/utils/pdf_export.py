from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime

class PDFExporter:
    @staticmethod
    def export_hoa_don(hoa_don_info, chi_tiet, filename="hoa_don.pdf"):
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Tiêu đề
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#003366'),
            alignment=1,
            spaceAfter=30
        )
        story.append(Paragraph("HÓA ĐƠN DỊCH VỤ CHĂM SÓC XE", title_style))
        
        # Thông tin hóa đơn
        info_data = [
            ["Mã hóa đơn:", hoa_don_info['ma_hd']],
            ["Ngày lập:", hoa_don_info['ngay_lap'].strftime("%d/%m/%Y %H:%M")],
            ["Biển số xe:", hoa_don_info['bien_so']],
            ["Chủ xe:", hoa_don_info['ten_chu_xe']],
            ["Trạng thái:", hoa_don_info['trang_thai']]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Chi tiết dịch vụ
        detail_data = [["STT", "Tên dịch vụ", "Số lượng", "Đơn giá", "Thành tiền"]]
        for i, ct in enumerate(chi_tiet, 1):
            detail_data.append([
                str(i),
                ct['ten_dich_vu'],
                str(ct['so_luong']),
                f"{ct['don_gia']:,.0f} VNĐ",
                f"{ct['thanh_tien']:,.0f} VNĐ"
            ])
        
        detail_table = Table(detail_data, colWidths=[0.5*inch, 2.5*inch, 1*inch, 1.5*inch, 1.5*inch])
        detail_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(detail_table)
        story.append(Spacer(1, 20))
        
        # Tổng tiền
        total = sum(ct['thanh_tien'] for ct in chi_tiet)
        total_style = ParagraphStyle(
            'TotalStyle',
            parent=styles['Normal'],
            fontSize=14,
            alignment=2,
            textColor=colors.red
        )
        story.append(Paragraph(f"<b>Tổng tiền: {total:,.0f} VNĐ</b>", total_style))
        
        # Chữ ký
        story.append(Spacer(1, 50))
        signature_data = [
            ["Người lập phiếu", "Khách hàng"],
            ["(Ký, ghi rõ họ tên)", "(Ký, ghi rõ họ tên)"]
        ]
        signature_table = Table(signature_data, colWidths=[3*inch, 3*inch])
        signature_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        story.append(signature_table)
        
        doc.build(story)
        return filename