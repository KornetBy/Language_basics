import tkinter as tk
from tkinter import messagebox
import paramiko
import socket
import threading
import subprocess
import os
import re
import socks

BROWSER = "https://test0323.belta.by/ru"

class SSHTunnelApp:
    def __init__(self, master):
        self.master = master
        self.master.title("SSH Tunnel Setup")
        self.master.geometry("400x300")  # Установите размеры окна
        
        # Значения по умолчанию
        self.default_host = "178.172.212.135"  # Замените на ваш IP-адрес
        self.default_username = "root"  # Замените на имя пользователя
        self.default_password = "8?MTua$4Fb@yvn&"  # Замените на пароль (не рекомендуется для реального использования)

        self.label_host = tk.Label(master, text="Host IP:")
        self.label_host.pack(pady=5)

        self.entry_host = tk.Entry(master)
        self.entry_host.insert(0, self.default_host)
        self.entry_host.pack(pady=5)

        self.label_username = tk.Label(master, text="Username:")
        self.label_username.pack(pady=5)

        self.entry_username = tk.Entry(master)
        self.entry_username.insert(0, self.default_username)
        self.entry_username.pack(pady=5)

        self.label_password = tk.Label(master, text="Password:")
        self.label_password.pack(pady=5)

        self.entry_password = tk.Entry(master, show='*')
        self.entry_password.insert(0, self.default_password)
        self.entry_password.pack(pady=5)

        self.button_connect = tk.Button(master, text="Connect", command=self.connect)
        self.button_connect.pack(pady=10)

        self.status_label = tk.Label(master, text="")
        self.status_label.pack(pady=5)

    def connect(self):
        host = self.entry_host.get()
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Проверка корректности IP-адреса
        if not self.validate_ip(host):
            messagebox.showerror("Input Error", "Invalid IP address.")
            return

        self.status_label.config(text="Connecting...")
        threading.Thread(target=self.establish_ssh_tunnel, args=(host, username, password)).start()

    def validate_ip(self, ip):
        # Используем регулярное выражение для проверки IP-адреса
        pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        return bool(pattern.match(ip))

    def establish_ssh_tunnel(self, host, username, password):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=username, password=password)
            
            # Установить SOCKS-прокси
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
            socket.socket = socks.socksocket
            
            self.status_label.config(text="Connected! SOCKS proxy is running on localhost:1080.")
            print("SOCKS proxy is running on localhost:1080.")

            self.open_browser(BROWSER)
            
            # Блокировка, чтобы держать SSH-соединение открытым
            while True:
                pass  # Это будет держать соединение открытым. Вы можете добавить логику для обработки клиентских соединений.

        except paramiko.AuthenticationException:
            self.master.after(0, self.show_auth_error)  # Обновление UI с помощью after
        except paramiko.SSHException as e:
            self.master.after(0, lambda: messagebox.showerror("SSH Error", str(e)))
            self.status_label.config(text="SSH connection error.")
        except Exception as e:
            self.master.after(0, lambda: messagebox.showerror("Connection Error", str(e)))
            self.status_label.config(text="Connection failed.")

    def show_auth_error(self):
        messagebox.showerror("Authentication Error", "Invalid username or password.")
        self.status_label.config(text="Authentication failed.")

    def open_browser(self, url):
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(chrome_path):
            subprocess.Popen([chrome_path, url])
        else:
            messagebox.showerror("Browser Error", "Google Chrome не найден!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SSHTunnelApp(root)
    root.mainloop()
