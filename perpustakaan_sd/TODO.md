# TODO: Tambah kolom `kelas` pada tabel `buku` & update CRUD Buku

## Langkah

- [x] Buat rencana & dapatkan persetujuan user
- [ ] 1. Edit `database.py`:
      - Tambah `kelas INTEGER NOT NULL` pada CREATE TABLE buku (setelah judul)
      - Tambah migrasi otomatis: cek PRAGMA table_info(buku), jika kolom `kelas` tidak ada maka `ALTER TABLE buku ADD COLUMN kelas INTEGER DEFAULT 1`
      - Tidak pernah recreate / hapus data
- [ ] 2. Edit `modules/buku.py`:
      - Tambah Combobox Kelas (values 1-6) pada form
      - Jadikan Kelas wajib diisi pada add & edit
      - Masukkan Kelas sebagai kolom Treeview
      - Update semua INSERT, UPDATE, SELECT, SEARCH, dan mapping Treeview
- [ ] 3. Verifikasi:
      - Aplikasi berjalan tanpa error
      - CRUD Buku tetap berfungsi
      - Migrasi database hanya sekali & tidak gagal jika kolom sudah ada
- [ ] 4. (Berikutnya) Implementasi filter kelas pada `modules/peminjaman.py` (belum dikerjakan sekarang)

