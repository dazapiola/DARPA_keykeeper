import subprocess
import platform

def build_executable():
    subprocess.run(["pyinstaller", "--onefile", "--windowed", "--workpath", "./build", "--distpath", "./output", "../app.py"])

def create_windows_installer():
    subprocess.run(["iscc", "setup.iss"])

def create_macos_dmg():
    subprocess.run(["create-dmg", "dist/tu_programa.app"])

def create_linux_deb():
    subprocess.run(["dpkg-deb", "--build", "myapp"])

if __name__ == "__main__":
    build_executable()
    
    current_os = platform.system()
    
    if current_os == "Windows":
        create_windows_installer()
    elif current_os == "Darwin":
        create_macos_dmg()
    elif current_os == "Linux":
        create_linux_deb()
