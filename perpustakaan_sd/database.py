import sqlite3
from config import DB_PATH


def get_connection():
    """Membuat dan mengembalikan koneksi ke database SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except sqlite3.Error as e:
        print(f"[ERROR] Gagal terhubung ke database: {e}")
        return None


def create_tables():
    """Membuat tabel-tabel yang dibutuhkan jika belum ada."""
    conn = get_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS buku (
                id_buku INTEGER PRIMARY KEY AUTOINCREMENT,
                kode_buku TEXT UNIQUE,
                judul TEXT,
                kelas INTEGER NOT NULL DEFAULT 1,
                kategori TEXT,
                penerbit TEXT,
                tahun TEXT,
                rak TEXT,
                stok_total INTEGER,
                stok_tersedia INTEGER
            )
        """)

        # Migrasi otomatis: pastikan kolom `kelas` ada pada tabel `buku`
        # Jika database lama (tanpa kolom kelas), tambahkan kolom tanpa menghapus data.
        columns = [row[1] for row in cursor.execute("PRAGMA table_info(buku)").fetchall()]
        if "kelas" not in columns:
            cursor.execute("ALTER TABLE buku ADD COLUMN kelas INTEGER DEFAULT 1")
            print("[INFO] Kolom 'kelas' berhasil ditambahkan pada tabel buku.")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS siswa (
                id_siswa INTEGER PRIMARY KEY AUTOINCREMENT,
                nisn TEXT UNIQUE,
                nama TEXT,
                jenis_kelamin TEXT,
                kelas TEXT,
                alamat TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS peminjaman (
                id_pinjam INTEGER PRIMARY KEY AUTOINCREMENT,
                id_buku INTEGER,
                id_siswa INTEGER,
                tanggal_pinjam TEXT,
                tanggal_kembali TEXT,
                tanggal_dikembalikan TEXT,
                status TEXT,
                FOREIGN KEY (id_buku) REFERENCES buku(id_buku),
                FOREIGN KEY (id_siswa) REFERENCES siswa(id_siswa)
            )
        """)

        conn.commit()
        print("[INFO] Tabel berhasil dibuat/dipastikan tersedia.")
        return True

    except sqlite3.Error as e:
        print(f"[ERROR] Gagal membuat tabel: {e}")
        return False

    finally:
        conn.close()


def execute_query(query, params=()):
    """Menjalankan query INSERT/UPDATE/DELETE dan mengembalikan rowcount atau None jika gagal."""
    conn = get_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount

    except sqlite3.Error as e:
        print(f"[ERROR] Gagal menjalankan query: {e}")
        return None

    finally:
        conn.close()


def fetch_all(query, params=()):
    """Mengambil semua baris hasil query dan mengembalikan list atau None jika gagal."""
    conn = get_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    except sqlite3.Error as e:
        print(f"[ERROR] Gagal mengambil data: {e}")
        return None

    finally:
        conn.close()


def fetch_one(query, params=()):
    """Mengambil satu baris hasil query dan mengembalikan dict atau None jika gagal/tidak ada."""
    conn = get_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None

    except sqlite3.Error as e:
        print(f"[ERROR] Gagal mengambil data: {e}")
        return None

    finally:
        conn.close()


# Panggil create_tables() saat file dijalankan
if __name__ == "__main__":
    create_tables()

