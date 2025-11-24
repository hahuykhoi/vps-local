# VPS Manager - tiendung_zzz

> **Created by tiendung_zzz**  
> **Profile**: https://tiendung-profile.vercel.app/

## 🚀 Giới thiệu

VPS Manager là một hệ thống quản lý VPS tự động được phát triển bởi **tiendung_zzz**. Hệ thống cho phép tạo và quản lý VPS Windows thông qua GitHub Actions một cách hoàn toàn tự động.

**3 cách sử dụng:**
1. **Local VPS Server** ⭐ (Mới) - Biến máy local/hosting free thành VPS, không cần GitHub Actions
2. **Python Tool** - Tạo VPS tự động trên GitHub Actions, chỉ trả về link
3. **Website** - Giao diện web đầy đủ với quản lý VPS

## ✨ Tính năng

- 🖥️ **VPS Windows Server** với giao diện đồ họa đầy đủ
- 🌐 **Truy cập qua Web** sử dụng noVNC 
- 🔄 **Tự động khởi động lại** sau 5.5 giờ
- 🛡️ **Bảo mật** với mật khẩu tùy chỉnh
- 📱 **Giao diện hiện đại** và responsive
- ⚡ **Triển khai nhanh chóng** trên Vercel

## 🏗️ Cấu trúc dự án

```
vps-manager/
├── api/
│   ├── create-vps.js      # API tạo VPS
│   ├── vpsuser.js         # API quản lý người dùng
│   └── index.js           # API chính (fallback)
├── public/
│   └── index.html         # Giao diện web chính
├── package.json           # Dependencies
├── vercel.json           # Cấu hình Vercel
├── next.config.js        # Cấu hình Next.js
└── README.md             # Tài liệu này
```

## 🛠️ Cài đặt và triển khai

### Cách 1: Local VPS Server ⭐ (Khuyên dùng - Chạy trên máy local hoặc hosting free)

Biến máy local hoặc hosting free (Render, Railway, Replit...) thành VPS với giao diện đồ họa.

#### Windows - Chạy ngay
```bash
start_vps.bat
```

#### Linux/Mac - Chạy ngay
```bash
chmod +x start_vps.sh
./start_vps.sh
```

#### Hoặc chạy thủ công
```bash
pip install -r requirements_local.txt
python local_vps_server.py
```

**Kết quả:**
- Local: `http://localhost:6080/vnc.html`
- Public: `https://xxxxx.trycloudflare.com/vnc.html` (tự động)
- Password: `tiendung`

**Deploy lên hosting free:**
- Render.com: Push code + file `render.yaml` → Auto deploy
- Railway.app: Push code → Auto deploy
- Docker: `docker-compose up -d`

**Xem hướng dẫn chi tiết:** [LOCAL_VPS_GUIDE.md](LOCAL_VPS_GUIDE.md)

---

### Cách 2: Python Tool (Tạo VPS trên GitHub Actions)

#### Yêu cầu
- Python 3.7+
- GitHub Personal Access Token

#### Cài đặt
```bash
pip install -r requirements.txt
```

#### Sử dụng

**Windows - Cách nhanh nhất:**
```bash
create_vps.bat
```

**Hoặc chạy trực tiếp:**
```bash
python vps_creator.py
```

**Với biến môi trường:**
```bash
# Windows CMD
set GITHUB_TOKEN=ghp_your_token_here
python vps_creator.py

# Windows PowerShell
$env:GITHUB_TOKEN="ghp_your_token_here"
python vps_creator.py
```

Tool sẽ tự động:
1. Tạo repository
2. Cấu hình workflow
3. Khởi động VPS
4. Trả về link truy cập

**Xem hướng dẫn chi tiết:** [PYTHON_TOOL_GUIDE.md](PYTHON_TOOL_GUIDE.md)

---

### Cách 3: Website (Giao diện web với quản lý VPS)

#### 1. Clone dự án
```bash
git clone <repository-url>
cd vps-manager
```

#### 2. Cài đặt dependencies
```bash
npm install
```

#### 3. Cài đặt Vercel CLI (nếu chưa có)
```bash
npm install -g vercel
```

#### 4. Chạy development server
```bash
npm run dev
```

Server sẽ chạy tại: `http://localhost:3000`

**Lưu ý**: 
- Dữ liệu VPS users sẽ được lưu trong thư mục `./data/` (local)
- CORS đã được cấu hình để chấp nhận localhost
- Xem chi tiết trong file `LOCAL_SETUP.md`

### Triển khai lên Vercel (Production)
1. Push code lên GitHub repository
2. Kết nối repository với Vercel
3. Deploy tự động sẽ được kích hoạt
4. Domain sẽ có dạng: `https://your-project.vercel.app`

### 5. Cấu hình domain tùy chỉnh
- Trong Vercel Dashboard, vào Settings > Domains
- Thêm domain tùy chỉnh của bạn
- Cấu hình DNS records theo hướng dẫn

## 📋 Yêu cầu

### GitHub Token
- Cần có **Personal Access Token** từ GitHub
- Token phải có quyền:
  - `repo` (full repository access)
  - `workflow` (workflow permissions)
  - `write:packages` (nếu cần)

### Tạo GitHub Token
1. Vào GitHub Settings > Developer settings > Personal access tokens
2. Generate new token (classic)
3. Chọn scopes cần thiết
4. Copy token và sử dụng trong ứng dụng

## 🔧 API Endpoints

### POST `/api/create-vps`
Tạo VPS mới

**Body:**
```json
{
  "github_token": "ghp_xxxxxxxxxxxxxxxxxxxx"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "VPS creation initiated successfully",
  "repository": "user/vps-project-xxxxx",
  "workflow_status": "triggered"
}
```

### GET `/api/vpsuser`
Lấy danh sách VPS đang hoạt động

**Response:**
```json
{
  "status": "success",
  "total": 2,
  "users": [
    {
      "token": "ghp_1234567***",
      "link": "https://xxxxx.trycloudflare.com/vnc.html"
    }
  ]
}
```

### POST `/api/vpsuser`
Lưu hoặc lấy thông tin VPS user

## 🎯 Cách sử dụng

1. **Truy cập website**: Domain đã deploy hoặc localhost
2. **Nhập GitHub Token**: Token phải có đủ quyền
3. **Nhấn "Tạo VPS"**: Hệ thống sẽ tự động:
   - Tạo repository mới trên GitHub
   - Thiết lập workflow
   - Khởi động VPS Windows
   - Trả về link truy cập
4. **Truy cập VPS**: Mở link trong tab mới, mật khẩu: `tiendung`

## 🔐 Bảo mật

- Tất cả repository được tạo ở chế độ **private**
- GitHub Token chỉ được sử dụng server-side
- CORS được cấu hình cho phép domain của bạn
- Mật khẩu VNC mặc định: `tiendung`

## ⚠️ Lưu ý quan trọng

- **GitHub Actions limits**: GitHub có giới hạn về thời gian chạy workflow
- **VPS lifetime**: VPS sẽ tự động tắt sau ~5.5 giờ và khởi động lại
- **Storage**: Không có persistent storage, dữ liệu sẽ mất khi restart
- **Performance**: Phù hợp cho testing, development, không dùng production

## 🛠️ Customization

### Thay đổi mật khẩu VNC
Sửa trong file `api/create-vps.js`:
```powershell
VALUE_OF_PASSWORD=your-new-password
```

### Thay đổi thời gian chạy
Sửa biến `$totalMinutes` trong workflow:
```powershell
$totalMinutes = 330  # 5.5 giờ
```

### Thêm software
Thêm các lệnh cài đặt trong phần workflow setup.

## 🎨 Giao diện

- **Framework**: Pure HTML/CSS/JavaScript
- **Design**: Modern gradient design với glassmorphism
- **Icons**: Font Awesome 6
- **Fonts**: Inter (Google Fonts)
- **Responsive**: Hỗ trợ mobile và desktop

## 📝 Changelog

### Version 1.0.0
- ✅ Giao diện web hoàn chỉnh
- ✅ API tạo VPS tự động
- ✅ Quản lý danh sách VPS
- ✅ Auto-restart workflow
- ✅ Cloudflare Tunnel integration
- ✅ Vercel deployment ready

## 👨‍💻 Tác giả

**tiendung_zzz**
- Profile: https://tiendung-profile.vercel.app/

## 📄 License

MIT License - Tự do sử dụng và chỉnh sửa

## 🆘 Hỗ trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra GitHub Token có đủ quyền
2. Xem logs trong GitHub Actions
3. Đảm bảo repository không bị rate limit

---

*Developed with ❤️ by tiendung_zzz | https://tiendung-profile.vercel.app/*
"# vps-local" 
