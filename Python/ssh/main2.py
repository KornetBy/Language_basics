import paramiko

def ssh_connect(hostname, port, username, password):
    try:
        # Создаем SSH-клиент
        client = paramiko.SSHClient()
        # Разрешаем подключение к неизвестным хостам
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Подключаемся к серверу
        client.connect(hostname, port=port, username=username, password=password)
        
        print(f"Успешное подключение к {hostname}")

        # Пример выполнения команды
        stdin, stdout, stderr = client.exec_command('ls -l')
        print(stdout.read().decode())  # Вывод результата выполнения команды

    except Exception as e:
        print(f"Ошибка подключения: {e}")
    finally:
        client.close()  # Закрываем соединение

if __name__ == "__main__":
    # Замените значения на ваши данные
    hostname = "178.172.212.135"  # IP-адрес или доменное имя
    port = 22  # Обычно порт SSH 22
    username = "root"  # Ваше имя пользователя
    password = "8?MTua$4Fb@yvn&"  # Ваш пароль

    ssh_connect(hostname, port, username, password)
