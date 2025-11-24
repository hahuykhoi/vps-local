#!/bin/bash

# VPS Local Setup Script - Không cần Python
# Chạy trực tiếp trên Linux hosting với sudo

echo "=== VPS Local Setup ==="
echo ""

# Kiểm tra quyền sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Vui lòng chạy với sudo: sudo bash setup_vps.sh"
    exit 1
fi

# Cài đặt các package cần thiết
echo "[1/5] Cài đặt dependencies..."
apt-get update -qq
apt-get install -y qemu-system-x86 wget unzip novnc websockify xvfb x11vnc > /dev/null 2>&1

# Tải Windows ISO (hoặc dùng image có sẵn)
echo "[2/5] Chuẩn bị Windows image..."
if [ ! -f "windows.img" ]; then
    echo "Tạo disk image 20GB..."
    qemu-img create -f qcow2 windows.img 20G
fi

# Tải cloudflared
echo "[3/5] Tải Cloudflare Tunnel..."
if [ ! -f "cloudflared" ]; then
    wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
    mv cloudflared-linux-amd64 cloudflared
    chmod +x cloudflared
fi

# Khởi động VNC server
echo "[4/5] Khởi động VNC server..."
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x16 &
sleep 2

# Khởi động QEMU với Windows
echo "[5/5] Khởi động VPS..."
qemu-system-x86_64 \
    -hda windows.img \
    -m 2048 \
    -smp 2 \
    -vnc :0 \
    -usbdevice tablet \
    -net nic -net user \
    -enable-kvm 2>/dev/null &

sleep 3

# Khởi động noVNC
echo "Khởi động noVNC..."
cd /usr/share/novnc
./utils/novnc_proxy --vnc localhost:5900 --listen 6080 &

# Khởi động Cloudflare Tunnel
echo "Tạo public URL..."
./cloudflared tunnel --url http://localhost:6080 > tunnel.log 2>&1 &

sleep 5

# Lấy public URL
echo ""
echo "=== VPS đã sẵn sàng! ==="
echo ""
echo "Local URL: http://localhost:6080/vnc.html"
echo ""

# Đợi và hiển thị Cloudflare URL
for i in {1..10}; do
    if grep -q "https://" tunnel.log; then
        PUBLIC_URL=$(grep -o "https://[a-z0-9-]*\.trycloudflare\.com" tunnel.log | head -1)
        echo "Public URL: $PUBLIC_URL/vnc.html"
        echo ""
        echo "Password: tiendung"
        break
    fi
    sleep 2
done

echo ""
echo "VPS đang chạy... Nhấn Ctrl+C để dừng"
echo ""

# Giữ script chạy
tail -f /dev/null
