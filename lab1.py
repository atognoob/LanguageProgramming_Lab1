# Импорт необходимых библиотек
import http.client
import sys
import os
import time
from urllib.parse import urlparse
import threading

# Функция для загрузки файла с предоставленного URL-адреса
def download(url):
    # Разбор URL
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        print("Invalid URL. Must start with http:// or https://")
        return

    # Определение имени файла
    filename = os.path.basename(parsed_url.path) if parsed_url.path else "downloaded_file"

    # Установка HTTP/HTTPS-соединение.
    byte_counter = 0
    conn_class = http.client.HTTPSConnection if parsed_url.scheme == "https" else http.client.HTTPConnection
    path = parsed_url.path if parsed_url.path else '/'
    headers = {"User-Agent": "Mozilla/5.0"}

    # Отправьте HTTP-запрос GET
    conn = conn_class(parsed_url.netloc)
    conn.request("GET", path, headers=headers)
    response = conn.getresponse()

    # Проверить статус ответа
    if response.status != 200:
        print(f"Failed to download file. Status: {response.status}")
        return

    # Записать загруженные данные в файл
    with open(filename, 'wb') as file:
        print(f"Downloading '{filename}'...")

        # Создание потока для вывода информации о загрузке
        lock = threading.Lock()
        def report_progress():
            while True:
                time.sleep(1)
                with lock:
                    print(f"Downloaded {byte_counter} bytes")
                    if finished[0]:
                        break

        finished = [False]
        threading.Thread(target=report_progress, daemon=True).start()

        try:
            #Чтение данных и запись в файл
            while True:
                buffer = response.read(10000)
                if not buffer:
                    break
                with lock:
                    file.write(buffer)
                    byte_counter += len(buffer)

            # Завершение загрузки
            with lock:
                finished[0] = True

            print(f"Finished downloading '{filename}'. Total size: {byte_counter} bytes.")

        # Обработка ошибок и закрытие соединения
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lab11.py <URL>")
        sys.exit(1)
    url = sys.argv[1]
    download(url)