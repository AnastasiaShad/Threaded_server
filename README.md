## Лабораторная работа "Многопоточный сервер" по Практикуму по программированию
### Задания для самостоятельного выполнения

1.Модифицировать простой эхо-сервер таким образом, чтобы при подключении клиента создавался новый поток, в котором происходило взаимодействие с ним.

![image](https://user-images.githubusercontent.com/70855182/139716579-7016ebe3-2f87-4063-8013-b9f53639f76c.png)

![image](https://user-images.githubusercontent.com/70855182/139716980-ef889ecf-a09b-4999-8430-72783afa86b3.png)

2.Реализовать простой чат сервер на базе сервера аутентификации. Сервер должен обеспечивать подключение многих пользователей одновременно, отслеживание имен пользователей, поддерживать историю сообщений и пересылку сообщений от каждого пользователя всем остальным.

![image](https://user-images.githubusercontent.com/70855182/139723335-0cc6db8a-3333-477b-a4a5-b89e58372d91.png)

![image](https://user-images.githubusercontent.com/70855182/139717107-9d8366f3-4dc5-46a8-b716-83f07cadc130.png)

![image](https://user-images.githubusercontent.com/70855182/139717057-39d21bcc-a31c-4c6d-8c17-49c87a5b5863.png)

клиент_2 повторно подключился и увидел предыдущие сообщения:

![image](https://user-images.githubusercontent.com/70855182/139717307-7f3f5938-6ad5-4345-85e2-4bd6ec2cc7ea.png)

![image](https://user-images.githubusercontent.com/70855182/139717510-46ad0c38-8b85-46f6-b37b-0625ef372661.png)

![image](https://user-images.githubusercontent.com/70855182/139722226-ee845bb7-00a7-47d1-99d4-6f3cb248ce6f.png)

![image](https://user-images.githubusercontent.com/70855182/139722331-df28f636-8a21-49bd-932a-8cb97c4b819b.png)


3.Реализовать сервер с управляющим потоком. При создании сервера прослушивание портов происходит в отдельном потоке, а главный поток программы в это время способен принимать команды от пользователя. Необходимо реализовать следующие команды:

![image](https://user-images.githubusercontent.com/70855182/139717714-4d3d3acb-faa6-4859-88ed-8035e071dab0.png)

  Отключение сервера (завершение программы);
  
  ![image](https://user-images.githubusercontent.com/70855182/139719366-d5605d25-a3a7-46e8-9346-86fa4ca0109d.png)
  ____
  Пауза (остановка прослушивание порта);
  
 ![image](https://user-images.githubusercontent.com/70855182/139717942-fd2d210a-22d6-485a-81ee-4d7bd38b0e12.png)
 
 Клиент в это время ожидает повторное подключение
  ____
  Показ логов;
  
  ![image](https://user-images.githubusercontent.com/70855182/139718181-30bda99d-6d57-4884-88df-bb8f70ffb119.png)

  ____
  Очистка логов;
  
  ![image](https://user-images.githubusercontent.com/70855182/139718427-da4e9935-9f2f-48e8-91c9-482046a517d9.png)
  
  ![image](https://user-images.githubusercontent.com/70855182/139720826-4b3e1ce6-5c13-4154-8e37-ae906a0239e7.png)

  ____
  Очистка файла идентификации.
  
  ![image](https://user-images.githubusercontent.com/70855182/139718849-7c922faf-b39f-4b77-ba81-0890efef8fa6.png)
  
  Т.к теперь файл идентификации пуст, то клиента вновь просят зарегистрироваться в системе
  
  ![image](https://user-images.githubusercontent.com/70855182/139720226-d697d095-404a-4e6b-8e1e-747d53a5f06f.png)

