from tkinter import ttk
from tkinter import messagebox
from datetime import date

import database

# Font Segoe UI
FONT_FAMILY = "Segoe UI"


class PengembalianFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.selected_id = None
        self.configure_style()
        self.create_widgets()
        # Tampilkan riwayat pengembalian langsung saat halaman dibuka
        self.load_data()

    def configure_style(self):
        """Konfigurasi style untuk halaman Pengembalian."""
        style = ttk.Style(self)
        style.configure("Kembali.TFrame", background="#f0f4f8")
        style.configure(
            "KembaliHeader.TLabel",
            background="#f0f4f8",
            font=(FONT_FAMILY, 18, "bold"),
            foreground="#2c3e50",
        )
        style.configure(
            "KembaliFormLabel.TLabel",
            background="#f0f4f8",
            font=(FONT_FAMILY, 10),
            foreground="#34495e",
        )
        style.configure(
            "KembaliAction.TButton",
            font=(FONT_FAMILY, 10, "bold"),
            padding=(12, 6),
        )

    def create_widgets(self):
        """Membuat layout halaman Pengembalian Buku."""
        # ===== Header =====
        header = ttk.Label(self, text="Pengembalian Buku", style="KembaliHeader.TLabel")
        header.pack(pady=(20, 15))

        # ===== Container utama =====
        main = ttk.Frame(self, style="Kembali.TFrame")
        main.pack(fill="both", expand=True, padx=30, pady=5)

        main.columnconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)

        # ===== Panel Atas: Cari & Tombol =====
        top_panel = ttk.Frame(main, style="Kembali.TFrame")
        top_panel.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        top_panel.columnconfigure(0, weight=1)

        # Bar pencarian
        search_frame = ttk.Frame(top_panel, style="Kembali.TFrame")
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        search_label = ttk.Label(
            search_frame, text="Cari :", style="KembaliFormLabel.TLabel"
        )
        search_label.pack(side="left", padx=(0, 5))

        self.search_entry = ttk.Entry(search_frame, font=(FONT_FAMILY, 10))
        self.search_entry.pack(side="left", fill="x", expand=True)

        # Tombol aksi
        btn_frame = ttk.Frame(top_panel, style="Kembali.TFrame")
        btn_frame.grid(row=1, column=0, sticky="ew")
        btn_frame.columnconfigure((0, 1, 2, 3), weight=1)

        buttons = [
            ("Cari", "search"),
            ("Kembalikan", "return"),
            ("Refresh", "refresh"),
            ("Bersihkan", "clear"),
        ]

        self.buttons = {}

        for i, (text, key) in enumerate(buttons):
            btn = ttk.Button(
                btn_frame,
                text=text,
                style="KembaliAction.TButton",
                command=lambda k=key: self.on_button_click(k),
            )
            btn.grid(row=0, column=i, padx=3, pady=2, sticky="ew")
            self.buttons[key] = btn

        # ===== Panel Tengah: Treeview =====
        tree_frame = ttk.Frame(main, style="Kembali.TFrame")
        tree_frame.grid(row=1, column=0, sticky="nsew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        columns = (
            "id_pinjam",
            "nama_siswa",
            "kelas",
            "judul_buku",
            "tanggal_pinjam",
            "tanggal_kembali",
            "status",
        )

        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        headings = {
            "id_pinjam": "ID",
            "nama_siswa": "Nama Siswa",
            "kelas": "Kelas",
            "judul_buku": "Buku",
            "tanggal_pinjam": "Tanggal Pinjam",
            "tanggal_kembali": "Tanggal Kembali",
            "status": "Status",
        }

        widths = {
            "id_pinjam": 40,
            "nama_siswa": 180,
            "kelas": 60,
            "judul_buku": 220,
            "tanggal_pinjam": 120,
            "tanggal_kembali": 120,
            "status": 110,
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(
                col,
                width=widths[col],
                anchor="center"
                if col in (
                    "id_pinjam",
                    "kelas",
                    "tanggal_pinjam",
                    "tanggal_kembali",
                    "status",
                )
                else "w",
            )

        self.tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        scroll_y = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        scroll_y.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scroll_y.set)

        scroll_x = ttk.Scrollbar(
            tree_frame, orient="horizontal", command=self.tree.xview
        )
        scroll_x.grid(row=1, column=0, sticky="ew")
        self.tree.configure(xscrollcommand=scroll_x.set)

        # Event saat baris Treeview dipilih
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def on_tree_select(self, event=None):
        """Simpan id_peminjaman dari baris yang dipilih pada Treeview.

        Tidak mengisi form apa pun.
        """
        try:
            selection = self.tree.selection()
            if not selection:
                return

            # Simpan id_peminjaman dari baris yang dipilih (iid = id_pinjam)
            self.selected_id = selection[0]
        except Exception as e:
            print(f"[ERROR] Gagal memilih baris Treeview: {e}")

    def load_data(self):
        """Ambil riwayat peminjaman dan tampilkan pada Treeview.

        Hanya menampilkan transaksi yang masih berstatus 'Dipinjam'.
        Urutkan dari transaksi terbaru.
        """
        try:
            # Pastikan tabel tersedia
            database.create_tables()

            # Ambil data peminjaman (gabung dengan buku & siswa)
            # Hanya tampilkan transaksi yang masih berstatus 'Dipinjam'
            # Urutkan dari transaksi terbaru
            rows = database.fetch_all(
                "SELECT p.id_pinjam, p.id_buku, p.id_siswa, "
                "s.nama AS nama_siswa, s.kelas, "
                "b.judul AS judul_buku, "
                "p.tanggal_pinjam, p.tanggal_kembali, p.status "
                "FROM peminjaman p "
                "LEFT JOIN siswa s ON s.id_siswa = p.id_siswa "
                "LEFT JOIN buku b ON b.id_buku = p.id_buku "
                "WHERE p.status = ? "
                "ORDER BY p.id_pinjam DESC",
                ("Dipinjam",),
            )

            # Hapus isi Treeview lama
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Tampilkan data
            if rows:
                for row in rows:
                    self.tree.insert(
                        "",
                        "end",
                        iid=str(row["id_pinjam"]),
                        values=(
                            row["id_pinjam"],
                            row["nama_siswa"],
                            row["kelas"],
                            row["judul_buku"],
                            row["tanggal_pinjam"],
                            row["tanggal_kembali"],
                            row["status"],
                        ),
                    )
        except Exception as e:
            print(f"[ERROR] Gagal memuat data peminjaman: {e}")

    def kembalikan(self):
        """Proses pengembalian buku untuk transaksi yang dipilih.

        Mengubah status menjadi 'Dikembalikan', menambah stok_tersedia
        buku +1, dan menyimpan tanggal pengembalian (hari ini) dalam satu
        transaksi SQLite.
        """
        conn = None
        try:
            # Pastikan ada transaksi yang dipilih
            if not self.selected_id:
                messagebox.showwarning(
                    "Peringatan",
                    "Silakan pilih baris peminjaman pada tabel terlebih dahulu.",
                )
                return

            id_pinjam = int(self.selected_id)

            # Ambil data peminjaman yang akan dikembalikan
            row = database.fetch_one(
                "SELECT p.id_buku, p.status FROM peminjaman p "
                "WHERE p.id_pinjam = ?",
                (id_pinjam,),
            )
            if not row:
                messagebox.showerror("Error", "Data peminjaman tidak ditemukan.")
                return

            id_buku = row["id_buku"]
            status = row["status"]

            # Validasi: hanya transaksi berstatus 'Dipinjam' yang dapat dikembalikan
            if status != "Dipinjam":
                messagebox.showwarning(
                    "Peringatan",
                    "Transaksi ini bukan berstatus 'Dipinjam'.",
                )
                return

            # Tanggal pengembalian = hari ini
            tanggal_dikembalikan = date.today().strftime("%Y-%m-%d")

            # Buka transaksi SQLite
            conn = database.get_connection()
            if conn is None:
                messagebox.showerror("Error", "Gagal terhubung ke database.")
                return

            cursor = conn.cursor()

            # Ubah status menjadi 'Dikembalikan' dan simpan tanggal pengembalian
            cursor.execute(
                "UPDATE peminjaman SET status = ?, tanggal_dikembalikan = ? "
                "WHERE id_pinjam = ? AND status = 'Dipinjam'",
                ("Dikembalikan", tanggal_dikembalikan, id_pinjam),
            )

            # Tambahkan stok_tersedia buku sebanyak 1
            cursor.execute(
                "UPDATE buku SET stok_tersedia = stok_tersedia + 1 "
                "WHERE id_buku = ?",
                (id_buku,),
            )

            # Commit transaksi
            conn.commit()

            # Refresh Treeview
            self.load_data()

            # Kosongkan pilihan
            self.selected_id = None
            if self.tree.selection():
                self.tree.selection_remove(self.tree.selection())

            # Tampilkan pesan berhasil
            messagebox.showinfo("Sukses", "Buku berhasil dikembalikan.")

        except Exception as e:
            # Rollback jika terjadi kesalahan
            if conn is not None:
                try:
                    conn.rollback()
                except Exception:
                    pass
            print(f"[ERROR] Gagal mengembalikan buku: {e}")
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

        finally:
            if conn is not None:
                conn.close()

    def on_button_click(self, action):
        """Handler tombol."""
        if action == "refresh":
            self.load_data()
        elif action == "clear":
            # Bersihkan kotak pencarian dan muat ulang data
            self.search_entry.delete(0, "end")
            self.load_data()
        elif action == "search":
            self.search_pengembalian()
        elif action == "return":
            self.kembalikan()
        else:
            messagebox.showinfo(
                "Informasi",
                f"Fungsi '{action.capitalize()}' belum tersedia.",
            )

    def search_pengembalian(self):
        """Cari transaksi peminjaman berdasarkan Nama Siswa atau Judul Buku (LIKE).

        Halaman Pengembalian menampilkan transaksi yang masih berstatus 'Dipinjam'.
        """
        try:
            keyword = self.search_entry.get().strip()

            # Jika kotak pencarian kosong, tampilkan seluruh data kembali
            if not keyword:
                self.load_data()
                return

            pattern = f"%{keyword}%"

            # Cari berdasarkan Nama Siswa atau Judul Buku menggunakan LIKE
            rows = database.fetch_all(
                "SELECT p.id_pinjam, p.id_buku, p.id_siswa, "
                "s.nama AS nama_siswa, s.kelas, "
                "b.judul AS judul_buku, "
                "p.tanggal_pinjam, p.tanggal_kembali, p.status "
                "FROM peminjaman p "
                "LEFT JOIN siswa s ON s.id_siswa = p.id_siswa "
                "LEFT JOIN buku b ON b.id_buku = p.id_buku "
                "WHERE (s.nama LIKE ? OR b.judul LIKE ?) "
                "AND p.status = ? "
                "ORDER BY p.id_pinjam DESC",
                (pattern, pattern, "Dipinjam"),
            )

            # Hapus isi Treeview lama
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Tampilkan data hasil pencarian
            if rows:
                for row in rows:
                    self.tree.insert(
                        "",
                        "end",
                        iid=str(row["id_pinjam"]),
                        values=(
                            row["id_pinjam"],
                            row["nama_siswa"],
                            row["kelas"],
                            row["judul_buku"],
                            row["tanggal_pinjam"],
                            row["tanggal_kembali"],
                            row["status"],
                        ),
                    )
            else:
                messagebox.showinfo(
                    "Informasi",
                    f"Tidak ditemukan transaksi dengan kata kunci '{keyword}'.",
                )

        except Exception as e:
            print(f"[ERROR] Gagal mencari pengembalian: {e}")
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
