import socket

HOST = "127.0.0.1"
PORT = 5001


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            data = s.recv(1024)
            if not data:
                print("Соединение потеряно")
                break

            msg = data.decode("utf-8").strip()
            for line in msg.splitlines():
                if line == "MOVE":
                    move = input("Ваш ход (камень/ножницы/бумага или выход): ").strip().lower()
                    s.sendall((move + "\n").encode("utf-8"))
                elif line.startswith("RESULT") or line.startswith("OK") or line.startswith("WAIT") or line.startswith("ERROR"):
                    print(line)
                elif line == "GAMEOVER":
                    print("Игра окончена")
                    return


if __name__ == "__main__":
    main()
