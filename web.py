# Импорт встроенной библиотеки для работы веб-сервера
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

# Для начала определим настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """
    Специальный класс, который отвечает за
    обработку входящих запросов от клиентов
    """

    def do_GET(self):
        """Метод для обработки входящих GET-запросов"""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if self.path == "/category.html":
            read_page(self, "category.html")
        elif self.path == "/catalogies.html":
            read_page(self, "catalogies.html")
        elif self.path == "/contacts.html":
            read_page(self, "contacts.html")
        else:
            read_page(self, "main.html")

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        str_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        # Записываем данные с формы contacts
        with open("data.txt", "a", encoding="utf-8") as file_log:
            file_log.write(str_date + " POST " + "Отправлено с формы contacts: " + post_data.decode("utf-8") + "\n")
        # Использую модальное окно, поэтому добавил задержку
        time.sleep(2)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # Выводим страницу contacts
        read_page(self, "contacts.html")


def read_page(self, path):
    with open(path, "r", encoding="utf-8") as file:
        data = file.read()
    self.wfile.write(bytes(data, "utf-8"))


if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрах в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")
