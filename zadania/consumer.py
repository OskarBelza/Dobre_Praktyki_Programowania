import csv
import time
import os

FILE_NAME = 'queue.csv'
TEMP_FILE = 'queue_temp.csv'


def process_jobs():
    print(f"[*] Konsument uruchomiony. Czekam na zadania...")

    while True:
        job_to_do = None
        rows = []

        if not os.path.exists(FILE_NAME):
            time.sleep(5)
            continue

        # KROK 1: Odczyt i próba rezerwacji zadania
        with open(FILE_NAME, mode='r', newline='', encoding='utf-8') as file:
            reader = list(csv.reader(file))
            if not reader: continue

            headers = reader[0]
            for row in reader[1:]:
                if row[2] == 'pending' and job_to_do is None:
                    row[2] = 'in_progress'
                    job_to_do = row
                rows.append(row)

        # KROK 2: Zapisanie zmian do pliku (rezerwacja)
        if job_to_do:
            with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(rows)

            # KROK 3: Wykonanie pracy
            print(f"[!] Pobrano zadanie {job_to_do[0]}: {job_to_do[1]}. Praca potrwa 30s...")
            time.sleep(30)

            # KROK 4: Zmiana statusu na 'done'
            final_rows = []
            with open(FILE_NAME, mode='r', newline='', encoding='utf-8') as file:
                reader = list(csv.reader(file))
                headers = reader[0]
                for row in reader[1:]:
                    if row[0] == job_to_do[0]:
                        row[2] = 'done'
                    final_rows.append(row)

            with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(final_rows)

            print(f"[V] Zakończono zadanie {job_to_do[0]}.")
        else:
            time.sleep(5)


if __name__ == "__main__":
    process_jobs()
