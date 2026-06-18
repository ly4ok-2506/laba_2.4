import socket
import threading
import os
from task_2 import encrypt

HOST = '0.0.0.0'
PORT = 12345


def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Сервер запущен на {HOST}:{PORT}. Ожидание подключений...")

    while True:
        conn, addr = server.accept()
        print(f"[*] Подключился клиент: {addr}")

        try:
            request = conn.recv(1024).decode('utf-8')
            if request.startswith("UPLOAD"):
                _, filename, content = request.split('|', 2)
                print(f"[+] Получен файл {filename} для конвертации и шифрования")

                encrypted = encrypt(content.encode('utf-8'), 0x4F)

                bin_filename = filename.split('.')[0] + ".bin"
                with open(f"resource/server_{bin_filename}", 'wb') as f:
                    f.write(encrypted)

                conn.sendall(b"SUCCESS: File encrypted and saved on server.")

            elif request.startswith("DOWNLOAD"):
                _, filename = request.split('|')
                filepath = f"resource/server_{filename}"
                if os.path.exists(filepath):
                    with open(filepath, 'rb') as f:
                        conn.sendall(f.read())
                else:
                    conn.sendall(b"ERROR: File not found")
        except Exception as e:
            print(f"[-] Ошибка обработки: {e}")
        finally:
            conn.close()


def run_client():
    print("\n--- Запуск клиента ---")

    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect((HOST, PORT))
    json_data = '{"user": "student", "lab": "2.4"}'
    s1.sendall(f"UPLOAD|test.json|{json_data}".encode('utf-8'))
    response = s1.recv(1024).decode('utf-8')
    print(f"[Клиент] Ответ сервера: {response}")
    s1.close()

    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((HOST, PORT))
    s2.sendall(b"DOWNLOAD|test.bin")
    binary_content = s2.recv(4096)

    with open("resource/downloaded_test.bin", "wb") as f:
        f.write(binary_content)
    print(f"[Клиент] Зашифрованный бинарный файл успешно скачан и сохранен локально!")
    s2.close()


if __name__ == "__main__":
    os.makedirs('resource', exist_ok=True)

    srv_thread = threading.Thread(target=run_server, daemon=True)
    srv_thread.start()

    import time

    time.sleep(1)

    run_client()