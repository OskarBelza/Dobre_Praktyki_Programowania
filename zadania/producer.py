import csv
import uuid
import os

FILE_NAME = 'queue.csv'


def add_job(job_name):
    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['id', 'task_name', 'status'])

        job_id = str(uuid.uuid4())[:8]
        writer.writerow([job_id, job_name, 'pending'])
        print(f" Dodano zadanie: {job_name} (ID: {job_id})")


if __name__ == "__main__":
    add_job("Rozmowa telefoniczna")
