import csv
import uuid
import os

def export_to_csv(data, headers):
    csv_dir = ensure_csv_dir()
    filename = f"export-{uuid.uuid4().hex[:4]}.csv"
    file_path = os.path.join(csv_dir, filename)

    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)

    return file_path

def ensure_csv_dir():
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
    csv_dir = os.path.join(parent_dir, "csv")
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
    return csv_dir