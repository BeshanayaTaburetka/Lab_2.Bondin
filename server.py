import socket
import threading

HOST = "127.0.0.1"
PORT = 5001

CHOICES_RU = {"камень", "ножницы", "бумага"}
# Отображение на английские коды для логики
RU_TO_EN = {
    "камень": "rock",
    "ножницы": "scissors",
    "бумага": "paper",
}


def determine_winner(move1, move2):
    if move1 == move2:
        return 0
    wins_over = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock",
    }
    if wins_over[move1] == move2:
        return 1
    else:
        return 2


def handle_game(player1, player2):
    conn1, addr1 = player1
    conn2, addr2 = player2

    try:
        conn1.sendall("OK Вы Игрок 1. Вводите: камень/ножницы/бумага или выход\n".encode("utf-8"))
        conn2.sendall("OK Вы Игрок 2. Вводите: камень/ножницы/бумага или выход\n".encode("utf-8"))

        while True:
            conn1.sendall("MOVE\n".encode("utf-8"))
            conn2.sendall("MOVE\n".encode("utf-8"))

            move1 = conn1.recv(1024).decode("utf-8").strip().lower()
            move2 = conn2.recv(1024).decode("utf-8").strip().lower()

            if not move1 or not move2:
                break
            if move1 == "выход" or move2 == "выход":
                conn1.sendall("GAMEOVER\n".encode("utf-8"))
                conn2.sendall("GAMEOVER\n".encode("utf-8"))
                break

            if move1 not in CHOICES_RU or move2 not in CHOICES_RU:
                msg = "ERROR Неверный ход. Используйте: камень, ножницы, бумага\n"
                conn1.sendall(msg.encode("utf-8"))
                conn2.sendall(msg.encode("utf-8"))
                continue

            en1 = RU_TO_EN[move1]
            en2 = RU_TO_EN[move2]

            winner = determine_winner(en1, en2)

            if winner == 0:
                msg1 = f"RESULT Ничья: {move1} против {move2}\n"
                msg2 = msg1
            elif winner == 1:
                msg1 = f"RESULT Победа! {move1} бьёт {move2}\n"
                msg2 = f"RESULT Поражение. {move2} проигрывает {move1}\n"
            else:
                msg1 = f"RESULT Поражение. {move1} проигрывает {move2}\n"
                msg2 = f"RESULT Победа! {move2} бьёт {move1}\n"

            conn1.sendall(msg1.encode("utf-8"))
            conn2.sendall(msg2.encode("utf-8"))

    finally:
        conn1.close()
        conn2.close()
        print("Игра завершена")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Сервер запущен на {HOST}:{PORT}")
        print("Ожидание двух игроков...")

        while True:
            conn1, addr1 = s.accept()
            print(f"Подключился первый игрок: {addr1}")
            conn1.sendall("WAIT Ожидание второго игрока...\n".encode("utf-8"))

            conn2, addr2 = s.accept()
            print(f"Подключился второй игрок: {addr2}")

            game_thread = threading.Thread(
                target=handle_game,
                args=((conn1, addr1), (conn2, addr2)),
                daemon=True,
            )
            game_thread.start()


if __name__ == "__main__":
    main()
