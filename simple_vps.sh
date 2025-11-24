#!/bin/bash

# Script đơn giản nhất - Chỉ cần sudo
# Không cần Python, chạy trực tiếp VPS

echo "=== Simple VPS Setup ==="

# Cài đặt nhanh
echo "Cài đặt packages..."
sudo apt-get update -qq && sudo apt-get install -y qemu-system-x86 novnc websockify wget -qq

# Tạo disk nếu chưa có
[ ! -f "vps.img" ] && qemu-img create -f qcow2 vps.img 10G

# Tải cloudflared
if [ ! -f "cloudflared" ]; then
    wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
    chmod +x cloudflared
fi

# Chạy QEMU
echo "Khởi động VPS..."
qemu-system-x86_64 -hda vps.img -m 1024 -vnc :0 -daemonize

# Chạy noVNC
echo "Khởi động noVNC..."
websockify -D --web=/usr/share/novnc/ 6080 localhost:5900

# Chạy Cloudflare Tunnel
echo "Tạo public URL..."
./cloudflared tunnel --url http://localhost:6080 > /tmp/tunnel.log 2>&1 &

sleep 5

# Hiển thị URLs
echo ""
echo "✅ VPS đã sẵn sàng!"
echo ""
echo "🌐 Local:  http://localhost:6080/vnc.html"

# Lấy public URL
if [ -f "/tmp/tunnel.log" ]; then
    PUBLIC_URL=$(grep -o "https://[a-z0-9-]*\.trycloudflare\.com" /tmp/tunnel.log | head -1)
    [ ! -z "$PUBLIC_URL" ] && echo "🌍 Public: $PUBLIC_URL/vnc.html"
fi

echo ""
echo "🔑 Password: tiendung"
echo ""
