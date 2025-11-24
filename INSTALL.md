# Hướng dẫn cài đặt VPS Local (Không cần Python)

## 🚀 Cách 1: Script Bash (Đơn giản nhất)

### Yêu cầu
- Linux hosting với quyền `sudo`
- Kết nối internet

### Cài đặt

```bash
# Tải script
wget https://raw.githubusercontent.com/hahuykhoi/vps-local/master/simple_vps.sh

# Chạy
sudo bash simple_vps.sh
```

Xong! VPS sẽ chạy tại `http://localhost:6080/vnc.html`

---

## 🐳 Cách 2: Docker (Khuyên dùng)

### Yêu cầu
- Docker và Docker Compose đã cài đặt

### Cài đặt Docker (nếu chưa có)

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y docker.io docker-compose

# Khởi động Docker
sudo systemctl start docker
sudo systemctl enable docker
```

### Chạy VPS

```bash
# Clone repo
git clone https://github.com/hahuykhoi/vps-local.git
cd vps-local

# Tạo thư mục data
mkdir -p data

# Tạo disk image
docker run --rm -v $(pwd)/data:/data tianon/qemu qemu-img create -f qcow2 /data/vps.img 10G

# Chạy VPS
sudo docker-compose up -d
```

### Truy cập

- Local: `http://localhost:6080`
- Password: `tiendung`

### Quản lý

```bash
# Xem logs
sudo docker-compose logs -f

# Dừng VPS
sudo docker-compose down

# Khởi động lại
sudo docker-compose restart
```

---

## 🌐 Cách 3: Cài đặt thủ công

### Bước 1: Cài đặt packages

```bash
sudo apt-get update
sudo apt-get install -y qemu-system-x86 novnc websockify wget
```

### Bước 2: Tạo disk image

```bash
qemu-img create -f qcow2 vps.img 10G
```

### Bước 3: Chạy QEMU

```bash
qemu-system-x86_64 \
    -hda vps.img \
    -m 2048 \
    -smp 2 \
    -vnc :0 \
    -usbdevice tablet \
    -net nic -net user \
    -daemonize
```

### Bước 4: Chạy noVNC

```bash
websockify -D --web=/usr/share/novnc/ 6080 localhost:5900
```

### Bước 5: Tạo public URL (tùy chọn)

```bash
# Tải cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
chmod +x cloudflared

# Chạy tunnel
./cloudflared tunnel --url http://localhost:6080
```

---

## 📦 Deploy lên hosting miễn phí

### Railway.app

1. Fork repo này
2. Tạo project mới trên Railway
3. Chọn "Deploy from GitHub"
4. Railway sẽ tự động detect Docker và deploy

### Render.com

1. Fork repo này
2. Tạo "Web Service" mới
3. Chọn "Docker" làm environment
4. Deploy

### DigitalOcean App Platform

1. Fork repo này
2. Tạo App mới
3. Connect GitHub repo
4. Chọn Dockerfile
5. Deploy

---

## ⚠️ Lưu ý

- VPS cần ít nhất 1GB RAM
- Disk image sẽ lưu trong thư mục `data/`
- Lần đầu boot sẽ lâu (cần cài OS)
- Không có persistent storage khi restart container

---

## 🆘 Troubleshooting

### Port 6080 đã được sử dụng

```bash
# Tìm process đang dùng port
sudo lsof -i :6080

# Kill process
sudo kill -9 <PID>
```

### QEMU không chạy

```bash
# Kiểm tra KVM
ls /dev/kvm

# Nếu không có, chạy không có KVM
qemu-system-x86_64 -hda vps.img -m 1024 -vnc :0 -no-kvm
```

### noVNC không kết nối

```bash
# Kiểm tra VNC đang chạy
netstat -tulpn | grep 5900

# Restart websockify
pkill websockify
websockify -D --web=/usr/share/novnc/ 6080 localhost:5900
```

---

## 🔧 Cấu hình nâng cao

### Tăng RAM

Sửa `-m 2048` thành `-m 4096` (4GB)

### Thêm CPU cores

Sửa `-smp 2` thành `-smp 4` (4 cores)

### Thay đổi port

Sửa `6080` thành port khác trong docker-compose.yml hoặc script

---

**Chúc bạn thành công!** 🎉
