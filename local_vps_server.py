#!/usr/bin/env python3
"""
Local VPS Server - tiendung_zzz
Biến máy local hoặc hosting free thành VPS với VNC access
https://tiendung-profile.vercel.app/
"""

import os
import sys
import time
import subprocess
import platform
import threading
import signal
from pathlib import Path

# Cấu hình
VNC_PASSWORD = "tiendung"
VNC_PORT = 5900
NOVNC_PORT = 6080
CLOUDFLARE_TUNNEL = True  # Sử dụng Cloudflare tunnel để public


class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_banner():
    """In banner"""
    banner = f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║           Local VPS Server - tiendung_zzz                 ║
║           https://tiendung-profile.vercel.app/            ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝{Colors.END}
    """
    print(banner)


def print_step(message):
    """In bước thực hiện"""
    print(f"\n{Colors.BOLD}[•]{Colors.END} {message}")
    print("─" * 60)


def print_success(message):
    """In thông báo thành công"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")


def print_error(message):
    """In thông báo lỗi"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")


def print_info(message):
    """In thông tin"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")


def print_warning(message):
    """In cảnh báo"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")


def run_command(cmd, shell=True, check=True, capture_output=False):
    """Chạy command"""
    try:
        if capture_output:
            result = subprocess.run(cmd, shell=shell, check=check, 
                                  capture_output=True, text=True)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, shell=shell, check=check)
            return True
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {cmd}")
        if capture_output and e.stderr:
            print_error(e.stderr)
        return None


def check_os():
    """Kiểm tra hệ điều hành"""
    os_name = platform.system()
    print_step("Kiểm tra hệ điều hành")
    print_info(f"OS: {os_name}")
    print_info(f"Platform: {platform.platform()}")
    
    if os_name == "Windows":
        print_success("Windows detected")
        return "windows"
    elif os_name == "Linux":
        print_success("Linux detected")
        return "linux"
    elif os_name == "Darwin":
        print_success("macOS detected")
        return "macos"
    else:
        print_error(f"Unsupported OS: {os_name}")
        return None


def install_dependencies_windows():
    """Cài đặt dependencies trên Windows"""
    print_step("Cài đặt dependencies cho Windows")
    
    # Check Python
    print_info("Checking Python...")
    python_version = run_command("python --version", capture_output=True)
    if python_version:
        print_success(f"Python: {python_version}")
    
    # Install Python packages
    print_info("Installing Python packages...")
    packages = ["websockify", "novnc"]
    for pkg in packages:
        print_info(f"Installing {pkg}...")
        if run_command(f"pip install {pkg}", check=False):
            print_success(f"{pkg} installed")
    
    # Download TightVNC
    print_info("Checking TightVNC...")
    vnc_path = r"C:\Program Files\TightVNC\tvnserver.exe"
    if not os.path.exists(vnc_path):
        print_warning("TightVNC not found!")
        print_info("Please download and install TightVNC from:")
        print_info("https://www.tightvnc.com/download.php")
        print_info("Or run this PowerShell command as Administrator:")
        print("""
Invoke-WebRequest -Uri "https://www.tightvnc.com/download/2.8.63/tightvnc-2.8.63-gpl-setup-64bit.msi" -OutFile "tightvnc-setup.msi"
Start-Process msiexec.exe -Wait -ArgumentList '/i tightvnc-setup.msi /quiet /norestart ADDLOCAL="Server" SERVER_REGISTER_AS_SERVICE=1 SET_PASSWORD=1 VALUE_OF_PASSWORD=tiendung'
        """)
        return False
    else:
        print_success("TightVNC found")
    
    # Download Cloudflared
    print_info("Checking Cloudflared...")
    if not os.path.exists("cloudflared.exe"):
        print_info("Downloading Cloudflared...")
        if run_command('powershell -Command "Invoke-WebRequest -Uri https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe -OutFile cloudflared.exe"', check=False):
            print_success("Cloudflared downloaded")
    else:
        print_success("Cloudflared found")
    
    return True


def install_dependencies_linux():
    """Cài đặt dependencies trên Linux"""
    print_step("Cài đặt dependencies cho Linux")
    
    # Detect package manager
    if os.path.exists("/usr/bin/apt"):
        pkg_manager = "apt"
    elif os.path.exists("/usr/bin/yum"):
        pkg_manager = "yum"
    elif os.path.exists("/usr/bin/pacman"):
        pkg_manager = "pacman"
    else:
        print_error("Unknown package manager")
        return False
    
    print_info(f"Package manager: {pkg_manager}")
    
    # Install packages
    packages = {
        "apt": ["x11vnc", "xvfb", "fluxbox", "python3-pip"],
        "yum": ["x11vnc", "xorg-x11-server-Xvfb", "fluxbox", "python3-pip"],
        "pacman": ["x11vnc", "xorg-server-xvfb", "fluxbox", "python-pip"]
    }
    
    print_info("Installing system packages...")
    pkg_list = " ".join(packages.get(pkg_manager, []))
    
    if pkg_manager == "apt":
        run_command("sudo apt update", check=False)
        run_command(f"sudo apt install -y {pkg_list}", check=False)
    elif pkg_manager == "yum":
        run_command(f"sudo yum install -y {pkg_list}", check=False)
    elif pkg_manager == "pacman":
        run_command(f"sudo pacman -S --noconfirm {pkg_list}", check=False)
    
    # Install Python packages
    print_info("Installing Python packages...")
    run_command("pip3 install websockify novnc", check=False)
    
    # Download Cloudflared
    print_info("Downloading Cloudflared...")
    if not os.path.exists("cloudflared"):
        arch = platform.machine()
        if arch == "x86_64":
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
        elif arch == "aarch64":
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64"
        else:
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386"
        
        run_command(f"wget -O cloudflared {url}", check=False)
        run_command("chmod +x cloudflared", check=False)
        print_success("Cloudflared downloaded")
    
    return True


def start_vnc_windows():
    """Khởi động VNC trên Windows"""
    print_step("Khởi động VNC Server (Windows)")
    
    vnc_path = r"C:\Program Files\TightVNC\tvnserver.exe"
    
    # Stop existing VNC
    print_info("Stopping existing VNC processes...")
    run_command("taskkill /F /IM tvnserver.exe", check=False)
    time.sleep(2)
    
    # Start VNC
    print_info("Starting TightVNC server...")
    cmd = f'"{vnc_path}" -run -controlservice -start'
    
    # Start in background
    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(5)
    
    print_success("VNC server started on port 5900")
    return True


def start_vnc_linux():
    """Khởi động VNC trên Linux"""
    print_step("Khởi động VNC Server (Linux)")
    
    # Kill existing processes
    print_info("Stopping existing processes...")
    run_command("pkill -9 Xvfb", check=False)
    run_command("pkill -9 x11vnc", check=False)
    run_command("pkill -9 fluxbox", check=False)
    time.sleep(2)
    
    # Start Xvfb (Virtual display)
    print_info("Starting virtual display (Xvfb)...")
    subprocess.Popen(
        ["Xvfb", ":99", "-screen", "0", "1920x1080x24"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(2)
    
    # Set DISPLAY
    os.environ["DISPLAY"] = ":99"
    
    # Start window manager
    print_info("Starting window manager (Fluxbox)...")
    subprocess.Popen(
        ["fluxbox"],
        env={"DISPLAY": ":99"},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(2)
    
    # Start x11vnc
    print_info("Starting x11vnc server...")
    subprocess.Popen(
        ["x11vnc", "-display", ":99", "-forever", "-shared", "-passwd", VNC_PASSWORD],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(3)
    
    print_success("VNC server started on port 5900")
    return True


def start_websockify():
    """Khởi động websockify (noVNC)"""
    print_step("Khởi động noVNC (websockify)")
    
    # Find noVNC path
    try:
        import novnc
        novnc_path = os.path.dirname(novnc.__file__)
        print_info(f"noVNC path: {novnc_path}")
    except:
        print_warning("noVNC module not found, using current directory")
        novnc_path = "."
    
    # Start websockify
    print_info(f"Starting websockify on port {NOVNC_PORT}...")
    
    cmd = f"websockify --web {novnc_path} {NOVNC_PORT} localhost:{VNC_PORT}"
    
    subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(3)
    
    print_success(f"noVNC started on http://localhost:{NOVNC_PORT}")
    return True


def start_cloudflare_tunnel():
    """Khởi động Cloudflare tunnel"""
    print_step("Khởi động Cloudflare Tunnel")
    
    cloudflared_cmd = "./cloudflared" if platform.system() != "Windows" else "cloudflared.exe"
    
    if not os.path.exists(cloudflared_cmd.replace("./", "")):
        print_error("Cloudflared not found!")
        return None
    
    print_info("Starting Cloudflare tunnel...")
    
    # Start cloudflared and capture output
    process = subprocess.Popen(
        [cloudflared_cmd, "tunnel", "--url", f"http://localhost:{NOVNC_PORT}", "--no-autoupdate"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # Wait for URL
    print_info("Waiting for tunnel URL...")
    tunnel_url = None
    
    for i in range(60):  # Wait max 60 seconds
        line = process.stdout.readline()
        if line:
            print(f"  {line.strip()}")
            if "trycloudflare.com" in line:
                # Extract URL
                import re
                match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
                if match:
                    tunnel_url = match.group(0)
                    break
        time.sleep(1)
    
    if tunnel_url:
        print_success(f"Tunnel URL: {tunnel_url}")
        return tunnel_url
    else:
        print_error("Failed to get tunnel URL")
        return None


def main():
    """Main function"""
    print_banner()
    
    # Check OS
    os_type = check_os()
    if not os_type:
        sys.exit(1)
    
    # Install dependencies
    if os_type == "windows":
        if not install_dependencies_windows():
            print_error("Failed to install dependencies")
            print_info("Please install TightVNC manually and run again")
            sys.exit(1)
    elif os_type == "linux":
        if not install_dependencies_linux():
            print_error("Failed to install dependencies")
            sys.exit(1)
    else:
        print_error("macOS not fully supported yet")
        sys.exit(1)
    
    # Start VNC
    if os_type == "windows":
        if not start_vnc_windows():
            print_error("Failed to start VNC")
            sys.exit(1)
    elif os_type == "linux":
        if not start_vnc_linux():
            print_error("Failed to start VNC")
            sys.exit(1)
    
    # Start websockify
    if not start_websockify():
        print_error("Failed to start websockify")
        sys.exit(1)
    
    # Start Cloudflare tunnel
    tunnel_url = None
    if CLOUDFLARE_TUNNEL:
        tunnel_url = start_cloudflare_tunnel()
    
    # Print results
    print("\n" + "=" * 60)
    print_success("VPS SERVER STARTED!")
    print("=" * 60)
    print()
    
    print(f"{Colors.BOLD}📍 Local Access:{Colors.END}")
    print(f"   http://localhost:{NOVNC_PORT}/vnc.html")
    print()
    
    if tunnel_url:
        print(f"{Colors.BOLD}🌐 Public Access (Cloudflare Tunnel):{Colors.END}")
        print(f"   {tunnel_url}/vnc.html")
        print()
    
    print(f"{Colors.BOLD}🔑 VNC Password:{Colors.END} {VNC_PASSWORD}")
    print()
    print(f"{Colors.BOLD}👨‍💻 Created by:{Colors.END} tiendung_zzz")
    print(f"   https://tiendung-profile.vercel.app/")
    print()
    print(f"{Colors.BOLD}💡 Tips:{Colors.END}")
    print("   - Mở link trong trình duyệt")
    print("   - Click 'Connect' và nhập password")
    print("   - Press Ctrl+C to stop server")
    print()
    print("=" * 60)
    
    # Keep running
    try:
        print_info("Server is running... Press Ctrl+C to stop")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print()
        print_info("Stopping server...")
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
