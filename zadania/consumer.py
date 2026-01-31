import sqlite3
import time

DB_NAME = 'tasks_queue.db'


def consume():
    print("[*] Consumer uruchomiony. Sprawdzanie zadań co 5s...")

    while True:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # KROK 1: Spróbuj znaleźć i zarezerwować zadanie (atomic update)
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute("SELECT id, task_name FROM tasks WHERE status = 'pending' LIMIT 1")
        row = cursor.fetchone()

        if row:
            task_id = row['id']
            task_name = row['task_name']

            cursor.execute("UPDATE tasks SET status = 'in_progress' WHERE id = ?", (task_id,))
            conn.commit()
            conn.close()

            # KROK 2: Wykonanie pracy (30 sekund)
            print(f"[!] Konsumuję zadanie ID {task_id}: {task_name}. Praca zajmie 30s...")
            time.sleep(30)

            # KROK 3: Zmiana statusu na done
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET status = 'done' WHERE id = ?", (task_id,))
            conn.commit()
            conn.close()
            print(f"[V] Zadanie ID {task_id} zakończone.")

        else:
            conn.rollback()
            conn.close()
            time.sleep(5)


if __name__ == "__main__":
    consume()
