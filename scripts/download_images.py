import csv
import os
import requests
from urllib.parse import urlparse
from datetime import datetime
import time

DATA_DIR = "data/originals"
CSV_PATH = "data/metadata.csv"
ERROR_LOG = "data/download_errors.log"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.dirname(ERROR_LOG), exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    "Referer": "https://www.pinterest.com/"
}

def log_error(msg: str):
    ts = datetime.utcnow().isoformat() + "Z"
    with open(ERROR_LOG, "a", encoding="utf-8") as f:
        f.write(f"{ts} {msg}\n")

def safe_filename_from_uri(uri: str, fallback_id: str):
    try:
        parsed = urlparse(uri)
        name = os.path.basename(parsed.path)
        if not name:
            return f"asset-{fallback_id}.jpg"
        return name.split("?")[0]
    except Exception:
        return f"asset-{fallback_id}.jpg"

def download_with_retries(uri: str, headers: dict, retries: int = 3, timeout: int = 20):
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(uri, headers=headers, timeout=timeout)
            r.raise_for_status()
            return r.content
        except Exception as e:
            last_exc = e
            time.sleep(0.5 * attempt)
    raise last_exc

def download_row(row: dict):
    uri = (row.get('uri') or "").strip()
    if not uri:
        row['notes'] = "no_uri"
        return row

    try:
        content = download_with_retries(uri, HEADERS, retries=3, timeout=20)
        filename = row.get('filename') or safe_filename_from_uri(uri, row.get('id', 'unknown'))
        path = os.path.join(DATA_DIR, filename)
        with open(path, "wb") as f:
            f.write(content)
        row['filename'] = filename
        row['downloadedAt'] = datetime.utcnow().isoformat() + "Z"
        print("Downloaded", filename)
    except Exception as e:
        err_msg = f"download_error: {type(e).__name__}: {e}"
        row['notes'] = err_msg
        print("Failed", uri, err_msg)
        log_error(f"Failed {uri} -> {err_msg}")
    return row

def read_csv(path: str):
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    return rows, reader.fieldnames if 'reader' in locals() else None

def write_csv(path: str, rows: list):
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main():
    if not os.path.exists(CSV_PATH):
        print("metadata.csv nenalezen:", CSV_PATH)
        return

    rows, _ = read_csv(CSV_PATH)
    if not rows:
        print("metadata.csv je prázdný.")
        return

    updated = []
    for r in rows:
        updated.append(download_row(r))

    write_csv(CSV_PATH, updated)
    print("Hotovo. Zkontroluj složku data/originals a data/download_errors.log pokud jsou chyby.")

if __name__ == "__main__":
    main()
