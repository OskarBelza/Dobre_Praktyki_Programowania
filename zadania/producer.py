import sqlite3

DB_NAME = 'tasks_queue.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT,
            status TEXT DEFAULT 'pending'
        )
    ''')
    conn.commit()
    conn.close()

def add_job(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task_name, status) VALUES (?, ?)", (name, 'pending'))
    conn.commit()
    conn.close()
    print(f" [+] Dodano zadanie: {name}")

if __name__ == "__main__":
    init_db()
    # Pętla do wrzucenia 100 zadań na kolejkę
    for i in range(1, 101):
        add_job(f"Rozmowa nr {i}")