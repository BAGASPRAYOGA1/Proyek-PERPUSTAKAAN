import os

# BASE_DIR = folder project saat ini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# DB_DIR = folder database
DB_DIR = os.path.join(BASE_DIR, 'database')

# DB_NAME = nama file database
DB_NAME = 'perpustakaan.db'

# DB_PATH = gabungan folder database dan nama database
DB_PATH = os.path.join(DB_DIR, DB_NAME)

# Buat folder database otomatis jika belum ada
os.makedirs(DB_DIR, exist_ok=True)

