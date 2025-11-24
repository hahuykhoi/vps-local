# VPS Local Server

> Biến máy local hoặc hosting free thành VPS với giao diện đồ họa đầy đủ
> > **Created by tiendung_zzz**  
> **Profile**: https://tiendung-profile.vercel.app/

## 🚀 Giới thiệu

VPS Local Server cho phép bạn chạy một VPS Windows với giao diện đồ họa trên máy local hoặc hosting miễn phí (Render, Railway, Replit...). Truy cập qua trình duyệt web với noVNC.

## ✨ Tính năng

- 🖥️ **VPS Windows** với giao diện đồ họa đầy đủ
- 🌐 **Truy cập qua Web** sử dụng noVNC
- 🔒 **Cloudflare Tunnel** tự động tạo link public
- 🛡️ **Bảo mật** với mật khẩu
- ⚡ **Dễ dàng triển khai** trên nhiều nền tảng

## � ️ Cài đặt

### Yêu cầu
- Python 3.7+
- Windows (hoặc Linux/Mac với QEMU)

### Cài đặt dependencies

```bash
pip install flask requests
```

## 🎯 Sử dụng

### Chạy trên máy local

```bash
python local_vps_server.py
```

### Truy cập VPS

Sau khi chạy, bạn sẽ nhận được:
- **Local URL**: `http://localhost:6080/vnc.html`
- **Public URL**: `https://xxxxx.trycloudflare.com/vnc.html` (tự động tạo)
- **Password**: `tiendung`

## 🌐 Deploy lên hosting miễn phí

### Render.com

1. Fork repository này
2. Tạo Web Service mới trên Render
3. Chọn repository vừa fork
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `python local_vps_server.py`

### Railway.app

1. Fork repository này
2. Tạo project mới trên Railway
3. Connect repository
4. Deploy tự động

### Replit

1. Import repository
2. Chạy `python local_vps_server.py`
3. Replit sẽ tự động expose port

## 🔧 Cấu hình

### Thay đổi mật khẩu

Sửa trong file `local_vps_server.py`:

```python
password = "your-new-password"
```

### Thay đổi port

```python
port = 6080  # Thay đổi port mong muốn
```

## ⚠️ Lưu ý

- VPS chạy trên QEMU, hiệu năng phụ thuộc vào máy host
- Không có persistent storage, dữ liệu sẽ mất khi restart
- Phù hợp cho testing, development, không dùng production
- Cloudflare Tunnel có thể bị giới hạn băng thông

## 🛡️ Bảo mật

- Luôn đổi mật khẩu mặc định
- Không chia sẻ link public với người lạ
- Sử dụng HTTPS khi truy cập từ xa

## 📝 Cấu trúc project

```
vps-local/
├── local_vps_server.py    # Server chính
├── readme.md              # Tài liệu này
└── requirements.txt       # Dependencies (nếu có)
```

## 🆘 Troubleshooting

### Không kết nối được VPS
- Kiểm tra firewall
- Đảm bảo port 6080 không bị chiếm dụng
- Xem logs trong terminal

### Cloudflare Tunnel không hoạt động
- Kiểm tra kết nối internet
- Thử restart server
- Cloudflare có thể tạm thời block

## 📄 License

MIT License - Tự do sử dụng và chỉnh sửa

---

*Developed with Tiendung*
