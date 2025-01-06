# Здание 1: Wget на минималках
**Студент: Ву Хоанг Ань**

**Группа: 932101**

# Задание:
Используя примитивы многозадачности и синхронизации реализовать скачивание файла по http с выводом количества уже принятых байтов каждую секунду.

Для реализации рекомендуется использовать http.client.

Программа получает в качестве аргумента командной строки URL файла и скачивает его в текущую папку сохраняя исходное имя. Каждую секунду по таймеру выводится размер принятых данных.

Решение должно быть в виде одного (крайне желательно) файла и работать как консольная утилита.

Базовый язык - Python

# Объяснение

1. Импорт библиотек

```
import http.client  # Используется для отправки HTTP/HTTPS-запросов
import sys  # Используется для получения аргументов командной строки
import os  # Используется для работы с именами файлов
import time  # Используется для отслеживания времени и приостановки работы потоков
from urllib.parse import urlparse  # Используется для разбора URL на компоненты (схема, домен, путь)
import threading  # Используется для создания потоков и синхронизации потоков
```
2. Функция для загрузки файла с предоставленного URL-адреса

```
def download(url):
```
**Разбор URL**

```
# разбивает URL на компоненты: scheme (http, https), netloc (доменное имя), path (путь).
parsed_url = urlparse(url)
# Если отсутствует scheme или netloc, программа выводит ошибку о некорректном URL.
if not parsed_url.scheme or not parsed_url.netloc:
    print("Invalid URL. Must start with http:// or https://")
    return
```
**Определение имени файла**
```
filename = os.path.basename(parsed_url.path) if parsed_url.path else "downloaded_file"
```
**Установка HTTP/HTTPS-соединение**
```
conn_class = http.client.HTTPSConnection if parsed_url.scheme == "https" else http.client.HTTPConnection
path = parsed_url.path if parsed_url.path else '/'
headers = {"User-Agent": "Mozilla/5.0"}    #имитировать запрос от браузера
```
3. Отправьте HTTP-запрос GET
```
conn = conn_class(parsed_url.netloc)    #Устанавливается соединение с доменом 
conn.request("GET", path, headers=headers)    #Отправляется HTTP-запрос GET по указанному пути path
response = conn.getresponse()    #получает ответ от сервера
```
**Проверка статуса ответа**
```
if response.status != 200:
    print(f"Failed to download file. Status: {response.status}")
    return
```
4. Записать загруженные данные в файл
```
# Открывается файл для записи данных в бинарном формате (wb — write binary)
# with гарантирует закрытие файла после завершения загрузки или при возникновении ошибки.
with open(filename, 'wb') as file:
    print(f"Downloading '{filename}'...")
```
5. Создание потока для вывода информации о загрузке
```
lock = threading.Lock()
#создаёт блокировку, чтобы избежать конфликтов при одновременном доступе к переменной byte_counter из разных потоков
def report_progress():    #выполняется в отдельном потоке
    while True:
        time.sleep(1)    #выводит отчёт раз в секунду
        with lock:
            print(f"Downloaded {byte_counter} bytes")
            if finished[0]:    #становится True, поток завершает работу.
                break
finished = [False]
threading.Thread(target=report_progress, daemon=True).start()
```
6. Чтение данных и запись в файл
```
while True:
    buffer = response.read(10000)    #читает по 10 КБ данных с сервера
    #Если данные закончились (buffer пуст), программа выходит из цикла.
    if not buffer:
        break
    with lock:    #используется для защиты данных 
        file.write(buffer)    #записи данных в файл
        byte_counter += len(buffer)    #обновлении переменной byte_counter
```
7. Обработка ошибок и закрытие соединения
```
with lock:
    finished[0] = True    #отправляет сигнал для остановки потока report_progress.
print(f"Finished downloading '{filename}'. Total size: {byte_counter} bytes.")    # размер файла
```
8. Обработка ошибок и закрытие соединения
```
#Если при загрузке произошла ошибка (потеря соединения, ошибка записи…),выводит сообщение об ошибке
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()    #закрывает соединение HTTP/HTTPS для освобождения ресурсов.
```
9. Программы
```
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lab1.py <URL>")
        sys.exit(1)
    url = sys.argv[1]
    download(url)
```
# Пример 
```
python lab1.py https://www.soundhelix.com/examples/mp3/SoundHelix-Song-12.mp3
```
**Результат**
```
Downloading 'SoundHelix-Song-12.mp3'...
Downloaded 1650000 bytes
Downloaded 5460000 bytes
Downloaded 7960000 bytes
Finished downloading 'SoundHelix-Song-12.mp3'. Total size: 12328191 bytes.
```
# Итог

Загрузка файла с указанного URL и отображение количества загруженных байт каждую секунду.

•	Потоки (threading.Thread) для вывода прогресса загрузки.

•	Синхронизация потоков (threading.Lock) для предотвращения конфликтов данных.

•	Использование http.client для выполнения HTTP/HTTPS-запросов

