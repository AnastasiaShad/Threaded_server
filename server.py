import os, socket, getpass, csv, threading, datetime
from random import randint
import random
class Server():



    log_inf = {1: 'Сервер начал работу', 2: 'Порт слушает', 3: 'Соединение установлено', 4: 'Получение данных',
               5: 'Клиент был отсоединен',
               6: 'Сервер был отключен', 7: 'Смена порта', 8: 'Новый клиент', 9: 'Сообщение',
               10: 'Пауза', 11: 'Показ логов', 12: 'Очистка файла идентификации', 13:'Очистка логов', 14:'Идентификация', 15:'История сообщений', 16: 'Отображение команд',
               17: 'Отправка данных',
               18: 'Ввод пароля', 19:'Пользователь подключается'}
    # значения по-умолчанию
    HOST = '127.0.0.1'
    PORT = 64444
    commands = ['shutdown', 'listen to', 'quit', 'stop port',
                'show log', 'clear log', 'clear ind', 'help']
    all_help_commands = ['listen to - прослушивание порта', 'quit - отключение сервера',
                         'shutdown - отключение клиентов',
                         'stop port - Пауза (остановка прослушивание порта)',
                         'show log-Показ логов',
                         'clear log-Очистка логов',
                         'clear ind - Очистка файла идентификации',
                         'help - все команды']
    listen_ = True
    # создание уникального ключа для пользователей

    key = ''.join([random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(random.randint(1, 10))])
    # хранение потоков, имен пользователей
    thread_list = []
    usern_ames = []

    history = 'history.txt'
    file_logg = 'log.txt'


    def __init__(self, open_port, host):
        self.open_port = open_port
        self.host = host

    # смена порта
    def change_port(self, port):
        self.open_port = port

    # запись лог файла
    @staticmethod
    def log_text(cod):
        with open(Server.file_logg, 'a') as file:
            if type(cod) == int:
                file.write(str(datetime.datetime.now()) + '\t' + Server.log_inf[cod]  +'\n')


    @staticmethod
    def vernam(k, m):
        k = k*(len(m)//len(k)) + k[-(len(m) % len(k)):]
        return ''.join(map(chr, [i ^ x for i, x in zip(map(ord, m), map(ord, k))]))

    @staticmethod
    def check(port_user):
        try:
            port_user = int(port_user) if port_user != '' else Server.PORT
            port_user = port_user if 1 < port_user < 65537 else Server.PORT
            return port_user
        except:
            return False
    # основная часть
    @staticmethod
    def main_program():
        ClientUser.create_user_file()
        user_port = getpass.getpass(prompt="Введите порт: ", stream=None)
        user_port = Server.check(user_port)
        if user_port == False:
            while user_port == False:
                print('Неверный ввод порта')
                user_port = getpass.getpass(prompt="Введите порт (Enter -- по-умолчанию): ", stream=None)
                user_port = Server.check(user_port)
                if user_port != False:
                    break
        a = Server(user_port, Server.HOST)
        a.running_func()

    @staticmethod
    def listening_inf(sock):
        while True:
            if Server.listen_:
                try:
                    conn, addr = sock.accept()
                except:
                    break
                # поток пользователя когда получаем данные
                thread = UserClientThread(len(Server.thread_list), conn, addr)
                Server.thread_list.append(thread)
                thread.start()
            else:
                continue

    def running_func(self):
        Server.log_text(1)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            while True:
                try:
                    # привязка хоста и порта
                    s.bind((self.host, self.open_port))
                    break
                except:
                    self.change_port(self.open_port+1)
                    Server.log_text(7)
            s.listen(5)
            # поток
            thread = threading.Thread(target=Server.listening_inf, args=(s,))
            Server.thread_list.append(thread)
            thread.start()
            Server.log_text(2)
            print(f'Слушает порт: {self.open_port}')
            while True:
                command = input('Введите команду (help - список команд): ')
                if command == 'shutdown':
                    for n, c in Server.usern_ames:
                        Server.log_text(5)
                        c.close()
                    Server.log_text(6)
                    raise SystemExit
                elif command == "quit":
                    Server.log_text(6)
                    raise SystemExit
                elif command == 'help':
                    print(', '.join(Server.all_help_commands))
                elif command == 'listen to':
                    Server.listen_ = True
                    Server.log_text(2)
                    print(f'Слушает порт: {self.open_port}')
                elif command == 'stop port':
                    Server.listen_ = False
                    Server.log_text(10)
                    print(f'stop port {self.open_port}')
                elif command == 'clear ind':
                    Server.log_text(12)
                    print('Очистка файла идентификации')
                    ClientUser.user_list.clear()
                    with open(ClientUser.all_for_users, 'w', encoding='utf-8') as ss:
                        pass
                elif command == 'clear log':
                    print('Очистка логов')
                    with open(Server.file_logg, 'w') as ss:
                        pass
                elif command == 'show log':
                    print('Логи: ')
                    Server.log_text(11)
                    with open(Server.file_logg, 'r') as ss:
                        text = ss.read()
                        print(text)
                elif command != '':
                    print('Такой команды нет')

# класс для пользователя
class ClientUser():
    all_for_users = 'all_for_users.csv'
    user_list = []

    # создание файла для хранения данных о пользователях
    @staticmethod
    def create_user_file():
        if ClientUser.all_for_users in os.listdir(os.getcwd()):
            with open(ClientUser.all_for_users, encoding='utf-8') as s:
                reader = csv.reader(s, delimiter=';')
                ClientUser.user_list = [row for row in reader]
        else:
            a = open(ClientUser.all_for_users, 'w')
            a.close()

    # добавляем данные о пользователе
    @staticmethod
    def write_data_user():
        with open(ClientUser.all_for_users, 'w', encoding='utf-8') as s:
            writer = csv.writer(s, delimiter=';')
            writer.writerows(ClientUser.user_list)

    # создаем уникальный Id
    @staticmethod
    def user_ind():

        return ''.join([str(randint(1, 2000)) for i in range(40)])

# поток пользователя
class UserClientThread(threading.Thread):
    def __init__(self, name, connector, addr):
        threading.Thread.__init__(self)
        self.name = name
        self.conn = connector
        self.clientaddr = addr

    def run(self):
        name = UserClientThread.identify_user(self.conn)
        Server.usern_ames.append((name, self.conn))
        Server.log_text(14)
        self.history_mess()
        Server.log_text(15)
        while True:
            text = UserClientThread.s_recv(self.conn)
            if not text or text == 'exit':
                Server.log_text(5)
                break
            UserClientThread.s_send(text, name)

    @staticmethod
    def add_new_user(sock):
        sock.send('name'.encode('utf-8'))
        name = sock.recv(1024).decode('utf-8')
        sock.send(f'password,{name}'.encode('utf-8'))
        answer = sock.recv(1024).decode('utf-8')
        key = Server.key
        password = Server.vernam(key, answer)
        user_ind = ClientUser.user_ind()
        sock.send(f'Приветствую пользователя,{name},{user_ind}'.encode('utf-8'))
        ClientUser.user_list.append([name, password, user_ind, key])
        ClientUser.write_data_user()
        Server.log_text(8)
        return name

    @staticmethod
    def identify_user(sock):
        if len(ClientUser.user_list) == 0:
            return UserClientThread.add_new_user(sock)
        else:
            # for row in ClientUser.user_list:
            #     if row[2] == user_ind:
                    # sock.send(f'Приветствую пользователя,{row[0]}'.encode('utf-8'))
            # sock.send('name'.encode('utf-8'))
            # name = sock.recv(1024).decode('utf-8')
            for i, row in enumerate(ClientUser.user_list):
                sock.send('user_ind'.encode('utf-8'))
                user_ind = sock.recv(1024).decode('utf-8')
                try:
                    if row[2] == user_ind:
                        sock.send('name'.encode('utf-8'))
                        name = sock.recv(1024).decode('utf-8')
                        while row[0] != name:
                            sock.send('name'.encode('utf-8'))
                            name = sock.recv(1024).decode('utf-8')
                        while True:

                            sock.send(f'check,{row[0]}'.encode('utf-8'))
                            passwd = sock.recv(1024).decode('utf-8')
                            data = Server.vernam(row[3], passwd)
                            Server.log_text(19)
                            if data == row[1]:
                                # user_ind = ClientUser.user_ind()
                                sock.send(f'Приветствую пользователя,{name},{user_ind}'.encode('utf-8'))
                                # ClientUser.user_list[i].pop()

                                # ClientUser.user_list[i].append(user_ind)
                                Server.log_text(19)
                                ClientUser.write_data_user()
                                return name
                except:
                    continue
            else:
                sock.send('name'.encode('utf-8'))
                name = sock.recv(1024).decode('utf-8')
                sock.send(f'password,{name}'.encode('utf-8'))
                answer = sock.recv(1024).decode('utf-8')
                key = Server.key
                password = Server.vernam(key, answer)
                user_ind = ClientUser.user_ind()
                sock.send(f'Приветствую пользователя,{name},{user_ind}'.encode('utf-8'))
                ClientUser.user_list.append([name, password, user_ind, key])
                ClientUser.write_data_user()
                Server.log_text(8)
                return name

    # отпрака данных
    @staticmethod
    def s_send(mess, name):
        for name_us, conn in Server.usern_ames:
            try:
                if name_us != name:
                    conn.send(f'{name}:{mess}'.encode('utf-8'))
            except:
                continue
        with open(Server.history, 'a') as a:
            a.write(f'{name}:{mess}\n')

    # получение данных
    @staticmethod
    def s_recv(conn):
        try:
            text = conn.recv(1024)
            return text.decode('utf-8')
        except:
            pass
    # история диалога
    def history_mess(self):
        if Server.history in os.listdir(os.getcwd()):
            with open(Server.history, 'r') as ss:
                file_his = ss.read()
                if len(file_his) == 0:
                    self.conn.send('no data'.encode('utf-8'))
                else:
                    self.conn.send(f'{file_his}'.encode('utf-8'))
        else:
            file_his = open(Server.history, 'w')
            self.conn.send('no data'.encode('utf-8'))
            file_his.close()


if __name__ == '__main__':
    Server.main_program()
