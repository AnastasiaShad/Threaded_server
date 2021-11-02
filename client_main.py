import socket, getpass, threading, re, os

# значени хоста и порта по-умолчанию
HOST = '127.0.0.1'
# PORT = 63333
PORT = 64444
file_ind = 'ind_data.txt'


# проверяем данные ip, port
def check_inf(ip, port):
    try:
        ip = ip.group() if ip else HOST
        port = int(port) if port != '' else PORT
        port = port if -1 < port < 65537 else PORT
        return ip, port
    except:
        print("Что-то не так с данными")
        return False, False
# получаем данные ip, port
def inf_user():
    ip = re.search(r'^\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}$', getpass.getpass(prompt='Введите ip для подключения: '))
    # ip = ip.group() if ip else HOST
    port = getpass.getpass(prompt="Введите порт для подключения: ", stream=None)
    ip, port = check_inf(ip, port)
    if ip != False or port != False:
        return ip, port
    else:
        while ip == False or port == False:
            ip = re.search(r'^\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}$',
                           getpass.getpass(prompt='Введите ip для подключения: '))
            port = getpass.getpass(prompt='Введите порт для подключения: ')
            ip, port = check_inf(ip, port)
            if ip != False and port != False:
                break
    return ip, port

# получаем данные
def s_recv(conn):
    while True:
        try:
            msg = conn.recv(1024).decode('utf-8')
            print(msg)
        except:
            print('Отключение')
            break



# считываем данные с файла где хранятся индификатор пользователя
def up_ind():
    if file_ind in os.listdir(os.getcwd()):
        with open(file_ind, 'r', encoding ='utf-8') as ss:
            id_u = ss.read()
            return id_u if id_u else 'no user_ind'
    else:
        a = open(file_ind, 'w')
        a.close()
        return 'no user_ind'

# файл для хранения данных о идентификации пользователя
def ind_file(dta):
    # file_ind = 'ind_data'+str(dta)+'.txt'
    with open(file_ind, 'w', encoding ='utf-8') as file:
        file.write(dta)
max = 100000
def main_func():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        ip, port = inf_user()
        try_connect = 0
        log = False
        # если не получается подключить несолько раз, то клиент просто отключается
        try:
            while try_connect < 5 and not log:
                if not log:
                    # пытаемся подсоединиться
                    try:
                        s.connect((ip, port))
                        print('Соединение успешно было установлено')
                        log = True
                    except:
                        print('Соединение не установлено, повторная попытка')
                        try_connect += 1

        except:
            print('Сервер недоступен, было сделано 5 попыток')
            exit()
        while True:
            ms = s.recv(1024).decode('utf-8')
            if 'name' in ms:
                s.send(input('Введите имя: ').encode('utf-8'))
            elif 'password' in ms:
                name = ms.split(',')[1]
                s.send(input(f'Введите пароль, {name}: ').encode('utf-8'))
            elif 'check' in ms:
                    s.send(input(f'Введите пароль пользователя {ms.split(",")[1]}: ').encode())

            elif 'user_ind' in ms:
                tk = up_ind()
                s.send(tk.encode('utf-8'))

            else:
                # имя пользователя: сообщения пользователя
                name = ms.split(',')[1]
                data_msg = ms.split(',')[2] if len(ms.split(',')) > 2 else False
                if data_msg:
                    ind_file(data_msg)
                break
        print('exit - выйти')
        data = s.recv(max).decode('utf-8')

        if data == 'no data':
            pass
        else:
            data = ''.join([i.lstrip() for i in re.split(rf'{name}[:]', data)])[:-1]
            print(data)
        # создание потока
        potok = threading.Thread(target=s_recv, args=(s,))
        potok.start()
        while True:
            text = str(input())
            if not text or text == 'exit':
                break
            s.send(text.encode('utf-8'))



# запуск основной функции
if __name__ == '__main__':
    main_func()
