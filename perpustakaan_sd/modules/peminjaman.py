from tkinter import ttk
from tkinter import messagebox
from datetime import date, timedelta

import database

# Font Segoe UI
FONT_FAMILY = "Segoe UI"


class PeminjamanFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.selected_id = None
        self.configure_style()
        self.create_widgets()
        # Tampilkan riwayat peminjaman langsung saat halaman dibuka
        self.load_data()

    def configure_style(self):
        """Konfigurasi style untuk halaman Peminjaman."""
        style = ttk.Style(self)
        style.configure("Pinjam.TFrame", background="#f0f4f8")
        style.configure(
            "PinjamHeader.TLabel",
            background="#f0f4f8",
            font=(FONT_FAMILY, 18, "bold"),
            foreground="#2c3e50",
        )
        style.configure(
            "PinjamFormLabel.TLabel",
            background="#f0f4f8",
            font=(FONT_FAMILY, 10),
            foreground="#34495e",
        )
        style.configure(
            "PinjamAction.TButton",
            font=(FONT_FAMILY, 10, "bold"),
            padding=(12, 6),
        )

    def create_widgets(self):
        """Membuat layout halaman Peminjaman."""
        # ===== Header =====
        header = ttk.Label(self, text="Peminjaman Buku", style="PinjamHeader.TLabel")
        header.pack(pady=(20, 15))

        # ===== Container utama =====
        main = ttk.Frame(self, style="Pinjam.TFrame")
        main.pack(fill="both", expand=True, padx=30, pady=5)

        main.columnconfigure(0, weight=2)
        main.columnconfigure(1, weight=5)
        main.rowconfigure(0, weight=1)

        # ===== Panel Kiri: Form =====
        form_panel = ttk.LabelFrame(
            main, text=" Form Peminjaman ", style="Pinjam.TFrame"
        )
        form_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        # Field Kelas (Combobox)
        lbl_kelas = ttk.Label(
            form_panel, text="Kelas :", style="PinjamFormLabel.TLabel"
        )
        lbl_kelas.grid(row=0, column=0, sticky="w", padx=(15, 10), pady=8)
        self.combo_kelas = ttk.Combobox(
            form_panel,
            values=["1", "2", "3", "4", "5", "6"],
            font=(FONT_FAMILY, 10),
            state="readonly",
            width=22,
        )
        self.combo_kelas.grid(row=0, column=1, sticky="ew", padx=(0, 15), pady=8)
        self.combo_kelas.bind("<<ComboboxSelected>>", self.on_kelas_select)

        # Field Nama Siswa (Combobox)
        lbl_siswa = ttk.Label(
            form_panel, text="Nama Siswa :", style="PinjamFormLabel.TLabel"
        )
        lbl_siswa.grid(row=1, column=0, sticky="w", padx=(15, 10), pady=8)
        self.combo_siswa = ttk.Combobox(
            form_panel,
            font=(FONT_FAMILY, 10),
            state="readonly",
            width=22,
        )
        self.combo_siswa.grid(row=1, column=1, sticky="ew", padx=(0, 15), pady=8)

        # Field Buku (Combobox)
        lbl_buku = ttk.Label(
            form_panel, text="Buku :", style="PinjamFormLabel.TLabel"
        )
        lbl_buku.grid(row=2, column=0, sticky="w", padx=(15, 10), pady=8)
        self.combo_buku = ttk.Combobox(
            form_panel,
            font=(FONT_FAMILY, 10),
            state="readonly",
            width=22,
        )
        self.combo_buku.grid(row=2, column=1, sticky="ew", padx=(0, 15), pady=8)

        # Field Tanggal Pinjam (otomatis hari ini)
        lbl_tgl_pinjam = ttk.Label(
            form_panel, text="Tanggal Pinjam :", style="PinjamFormLabel.TLabel"
        )
        lbl_tgl_pinjam.grid(row=3, column=0, sticky="w", padx=(15, 10), pady=8)
        self.entry_tgl_pinjam = ttk.Entry(
            form_panel,
            font=(FONT_FAMILY, 10),
            width=22,
            state="readonly",
        )
        self.entry_tgl_pinjam.grid(row=3, column=1, sticky="ew", padx=(0, 15), pady=8)

        # Field Tanggal Kembali (otomatis +7 hari, dapat diedit)
        lbl_tgl_kembali = ttk.Label(
            form_panel, text="Tanggal Kembali :", style="PinjamFormLabel.TLabel"
        )
        lbl_tgl_kembali.grid(row=4, column=0, sticky="w", padx=(15, 10), pady=8)
        self.entry_tgl_kembali = ttk.Entry(
            form_panel,
            font=(FONT_FAMILY, 10),
            width=22,
            state="normal",
        )
        self.entry_tgl_kembali.grid(row=4, column=1, sticky="ew", padx=(0, 15), pady=8)

        # Isi tanggal otomatis (hari ini & +7 hari)
        self.set_auto_dates()

        form_panel.columnconfigure(1, weight=1)

        # ===== Panel Kanan: Cari, Tombol & Treeview =====
        right_panel = ttk.Frame(main, style="Pinjam.TFrame")
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(2, weight=1)

        # Bar pencarian
        search_frame = ttk.Frame(right_panel, style="Pinjam.TFrame")
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        search_label = ttk.Label(
            search_frame, text="Cari :", style="PinjamFormLabel.TLabel"
        )
        search_label.pack(side="left", padx=(0, 5))

        self.search_entry = ttk.Entry(search_frame, font=(FONT_FAMILY, 10))
        self.search_entry.pack(side="left", fill="x", expand=True)

        # Tombol aksi
        btn_frame = ttk.Frame(right_panel, style="Pinjam.TFrame")
        btn_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        btn_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        buttons = [
            ("Simpan", "save"),
            ("Edit", "edit"),
            ("Hapus", "delete"),
            ("Cari", "search"),
            ("Refresh", "refresh"),
            ("Bersihkan", "clear"),
        ]

        self.buttons = {}

        for i, (text, key) in enumerate(buttons):
            btn = ttk.Button(
                btn_frame,
                text=text,
                style="PinjamAction.TButton",
                command=lambda k=key: self.on_button_click(k),
            )
            btn.grid(row=0, column=i, padx=3, pady=2, sticky="ew")
            self.buttons[key] = btn

        # Treeview Peminjaman
        tree_frame = ttk.Frame(right_panel, style="Pinjam.TFrame")
        tree_frame.grid(row=2, column=0, sticky="nsew")
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

        # Kosongkan pilihan buku karena kelas belum dipilih saat halaman dibuka
        # dan pastikan Nama Siswa juga kosong
        self.siswa_map = {}
        self.buku_map = {}
        self.combo_siswa.set("")
        self.combo_siswa["values"] = []
        self.combo_buku.set("")
        self.combo_buku["values"] = []

    def set_auto_dates(self):
        """Isi Tanggal Pinjam (hari ini) dan Tanggal Kembali (+7 hari) otomatis."""
        try:
            today = date.today()
            kembali = today + timedelta(days=7)

            self.entry_tgl_pinjam.configure(state="normal")
            self.entry_tgl_pinjam.delete(0, "end")
            self.entry_tgl_pinjam.insert(0, today.strftime("%Y-%m-%d"))
            self.entry_tgl_pinjam.configure(state="readonly")

            self.entry_tgl_kembali.configure(state="normal")
            self.entry_tgl_kembali.delete(0, "end")
            self.entry_tgl_kembali.insert(0, kembali.strftime("%Y-%m-%d"))
        except Exception as e:
            print(f"[ERROR] Gagal mengisi tanggal otomatis: {e}")

    def on_kelas_select(self, event=None):
        """Filter combobox Nama Siswa dan Buku berdasarkan kelas yang dipilih."""
        try:
            kelas = self.combo_kelas.get().strip()
            self.combo_siswa.set("")
            self.siswa_map = {}

            if not kelas:
                self.combo_siswa["values"] = []
                # Kosongkan combobox Buku karena kelas belum dipilih
                self.load_buku_options("")
                return

            # Ambil seluruh siswa dari kelas yang dipilih (parameterized query)
            rows = database.fetch_all(
                "SELECT id_siswa, nisn, nama, kelas FROM siswa "
                "WHERE kelas = ? ORDER BY nama",
                (kelas,),
            )

            values = []
            if rows:
                for row in rows:
                    label = f"{row['nama']} ({row['nisn']})"
                    self.siswa_map[label] = row["id_siswa"]
                    values.append(label)
            self.combo_siswa["values"] = values

            # Muat buku hanya dari kelas yang dipilih (stok > 0)
            self.load_buku_options(kelas)
        except Exception as e:
            print(f"[ERROR] Gagal memfilter siswa: {e}")

    def load_buku_options(self, kelas=None):
        """Muat buku yang tersedia (stok > 0) untuk combobox Buku.

        Hanya buku dari kelas yang dipilih yang dimuat. Jika kelas belum
        dipilih, combobox Buku dikosongkan.
        """
        try:
            # Bersihkan pilihan dan peta buku
            self.combo_buku.set("")
            self.buku_map = {}

            # Jika kelas belum dipilih, combobox Buku harus kosong
            if not kelas:
                self.combo_buku["values"] = []
                return

            # Ambil seluruh buku dari kelas yang dipilih dengan stok tersedia > 0
            rows = database.fetch_all(
                "SELECT id_buku, kode_buku, judul, stok_tersedia FROM buku "
                "WHERE kelas = ? AND stok_tersedia > 0 ORDER BY judul",
                (kelas,),
            )

            # Format tampilan: "Judul (Kode)"
            self.buku_map = {}
            values = []
            if rows:
                for row in rows:
                    label = f"{row['judul']} ({row['kode_buku']})"
                    self.buku_map[label] = row["id_buku"]
                    values.append(label)
            self.combo_buku["values"] = values
        except Exception as e:
            print(f"[ERROR] Gagal memuat pilihan buku: {e}")

    def on_tree_select(self, event=None):
        """Isi seluruh form otomatis saat satu baris Treeview dipilih."""
        try:
            selection = self.tree.selection()
            if not selection:
                return

            values = self.tree.item(selection[0], "values")
            if not values:
                return

            # Simpan id_pinjam dari baris yang dipilih (iid = id_pinjam)
            self.selected_id = selection[0]

            # Urutan kolom:
            # id_pinjam, nama_siswa, kelas, judul_buku,
            # tanggal_pinjam, tanggal_kembali, status
            kelas = values[2]
            nama_siswa = values[1]
            judul_buku = values[3]
            tanggal_pinjam = values[4]
            tanggal_kembali = values[5]

            # Set Kelas
            self.combo_kelas.set(str(kelas) if kelas is not None else "")

            # Muat pilihan siswa & buku sesuai kelas yang terpilih
            self.on_kelas_select()

            # Isi Nama Siswa (cocokkan label "Nama (NISN)")
            self.combo_siswa.set("")
            if nama_siswa is not None:
                for label in self.combo_siswa["values"]:
                    if label.startswith(str(nama_siswa)):
                        self.combo_siswa.set(label)
                        break

            # Isi Buku (cocokkan label "Judul (Kode)")
            self.combo_buku.set("")
            if judul_buku is not None:
                for label in self.combo_buku["values"]:
                    if label.startswith(str(judul_buku)):
                        self.combo_buku.set(label)
                        break

            # Isi Tanggal Pinjam
            self.entry_tgl_pinjam.configure(state="normal")
            self.entry_tgl_pinjam.delete(0, "end")
            self.entry_tgl_pinjam.insert(
                0, str(tanggal_pinjam) if tanggal_pinjam is not None else ""
            )
            self.entry_tgl_pinjam.configure(state="readonly")

            # Isi Tanggal Kembali (tetap dapat diedit)
            self.entry_tgl_kembali.configure(state="normal")
            self.entry_tgl_kembali.delete(0, "end")
            self.entry_tgl_kembali.insert(
                0, str(tanggal_kembali) if tanggal_kembali is not None else ""
            )
        except Exception as e:
            print(f"[ERROR] Gagal mengisi form dari Treeview: {e}")

    def simpan_peminjaman(self):
        """Simpan transaksi peminjaman ke tabel peminjaman.

        Transaksi peminjaman dan pengurangan stok dilakukan dalam satu
        transaksi SQLite (commit/rollback) agar stok selalu konsisten.
        """
        conn = None
        try:
            kelas = self.combo_kelas.get().strip()
            siswa_label = self.combo_siswa.get().strip()
            buku_label = self.combo_buku.get().strip()

            # Validasi: Kelas wajib dipilih
            if not kelas:
                messagebox.showwarning("Peringatan", "Kelas wajib dipilih.")
                return

            # Validasi: Nama Siswa wajib dipilih
            if not siswa_label:
                messagebox.showwarning("Peringatan", "Nama Siswa wajib dipilih.")
                return

            # Validasi: Buku wajib dipilih
            if not buku_label:
                messagebox.showwarning("Peringatan", "Buku wajib dipilih.")
                return

            # Ambil id_siswa berdasarkan nama siswa yang dipilih
            id_siswa = self.siswa_map.get(siswa_label)
            if id_siswa is None:
                messagebox.showwarning("Peringatan", "Nama siswa tidak ditemukan.")
                return

            # Ambil id_buku berdasarkan buku pada kelas yang dipilih
            id_buku = self.buku_map.get(buku_label)
            if id_buku is None:
                messagebox.showwarning("Peringatan", "Buku tidak ditemukan.")
                return

            # Periksa stok_tersedia
            row = database.fetch_one(
                "SELECT stok_tersedia FROM buku WHERE id_buku = ?",
                (id_buku,),
            )
            if not row:
                messagebox.showerror("Error", "Data buku tidak ditemukan.")
                return

            stok = row["stok_tersedia"]
            if stok is None or stok <= 0:
                messagebox.showwarning("Peringatan", "Stok buku habis.")
                return

            # Ambil tanggal pinjam dan tanggal kembali dari form
            tanggal_pinjam = self.entry_tgl_pinjam.get().strip()
            tanggal_kembali = self.entry_tgl_kembali.get().strip()

            # Buka transaksi SQLite
            conn = database.get_connection()
            if conn is None:
                messagebox.showerror("Error", "Gagal terhubung ke database.")
                return

            cursor = conn.cursor()

            # Simpan transaksi ke tabel peminjaman
            cursor.execute(
                "INSERT INTO peminjaman (id_buku, id_siswa, tanggal_pinjam, "
                "tanggal_kembali, status) VALUES (?, ?, ?, ?, ?)",
                (id_buku, id_siswa, tanggal_pinjam, tanggal_kembali, "Dipinjam"),
            )

            # Kurangi stok_tersedia sebanyak 1
            cursor.execute(
                "UPDATE buku SET stok_tersedia = stok_tersedia - 1 "
                "WHERE id_buku = ? AND stok_tersedia > 0",
                (id_buku,),
            )

            # Commit transaksi
            conn.commit()

            # Refresh Treeview
            self.load_data()

            # Bersihkan form
            self.clear_form()

            # Tampilkan pesan berhasil
            messagebox.showinfo("Sukses", "Peminjaman berhasil disimpan.")

        except Exception as e:
            # Rollback jika terjadi kesalahan
            if conn is not None:
                try:
                    conn.rollback()
                except Exception:
                    pass
            print(f"[ERROR] Gagal menyimpan peminjaman: {e}")
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

        finally:
            if conn is not None:
                conn.close()

    def edit_peminjaman(self):
        """Edit transaksi peminjaman.

        Yang boleh diubah: tanggal kembali. Jika buku atau siswa diubah,
        stok lama dan stok baru disesuaikan otomatis. Seluruh operasi
        dilakukan dalam satu transaksi SQLite.
        """
        conn = None
        try:
            # Pastikan ada baris yang dipilih
            if not self.selected_id:
                messagebox.showwarning(
                    "Peringatan",
                    "Silakan pilih baris peminjaman pada tabel terlebih dahulu.",
                )
                return

            id_pinjam = int(self.selected_id)

            # Ambil nilai dari form
            siswa_label = self.combo_siswa.get().strip()
            buku_label = self.combo_buku.get().strip()
            tanggal_kembali = self.entry_tgl_kembali.get().strip()

            # Validasi: Nama Siswa wajib dipilih
            if not siswa_label:
                messagebox.showwarning("Peringatan", "Nama Siswa wajib dipilih.")
                return

            # Validasi: Buku wajib dipilih
            if not buku_label:
                messagebox.showwarning("Peringatan", "Buku wajib dipilih.")
                return

            # Validasi: Tanggal Kembali wajib diisi
            if not tanggal_kembali:
                messagebox.showwarning("Peringatan", "Tanggal Kembali wajib diisi.")
                return

            # Ambil id_siswa dan id_buku baru dari pilihan form
            id_siswa_baru = self.siswa_map.get(siswa_label)
            if id_siswa_baru is None:
                messagebox.showwarning("Peringatan", "Nama siswa tidak ditemukan.")
                return

            id_buku_baru = self.buku_map.get(buku_label)
            if id_buku_baru is None:
                messagebox.showwarning("Peringatan", "Buku tidak ditemukan.")
                return

            # Ambil data peminjaman lama
            old = database.fetch_one(
                "SELECT id_buku, id_siswa, status FROM peminjaman "
                "WHERE id_pinjam = ?",
                (id_pinjam,),
            )
            if not old:
                messagebox.showerror("Error", "Data peminjaman tidak ditemukan.")
                return

            old_id_buku = old["id_buku"]
            old_id_siswa = old["id_siswa"]

            # Buka transaksi SQLite
            conn = database.get_connection()
            if conn is None:
                messagebox.showerror("Error", "Gagal terhubung ke database.")
                return

            cursor = conn.cursor()

            # Jika buku diubah, sesuaikan stok lama dan baru
            if old_id_buku != id_buku_baru:
                # Pastikan stok buku baru tersedia
                row = cursor.execute(
                    "SELECT stok_tersedia FROM buku WHERE id_buku = ?",
                    (id_buku_baru,),
                ).fetchone()
                if not row:
                    raise ValueError("Buku baru tidak ditemukan.")
                stok = row["stok_tersedia"]
                if stok is None or stok <= 0:
                    raise ValueError("Stok buku baru habis.")

                # Kembalikan stok buku lama +1
                cursor.execute(
                    "UPDATE buku SET stok_tersedia = stok_tersedia + 1 "
                    "WHERE id_buku = ?",
                    (old_id_buku,),
                )
                # Kurangi stok buku baru -1
                cursor.execute(
                    "UPDATE buku SET stok_tersedia = stok_tersedia - 1 "
                    "WHERE id_buku = ? AND stok_tersedia > 0",
                    (id_buku_baru,),
                )

            # Update data peminjaman (id_buku, id_siswa, tanggal_kembali)
            cursor.execute(
                "UPDATE peminjaman SET id_buku = ?, id_siswa = ?, "
                "tanggal_kembali = ? WHERE id_pinjam = ?",
                (id_buku_baru, id_siswa_baru, tanggal_kembali, id_pinjam),
            )

            # Commit transaksi
            conn.commit()

            # Refresh Treeview
            self.load_data()

            # Bersihkan form
            self.clear_form()

            # Tampilkan pesan berhasil
            messagebox.showinfo("Sukses", "Peminjaman berhasil diperbarui.")

        except Exception as e:
            # Rollback jika terjadi kesalahan
            if conn is not None:
                try:
                    conn.rollback()
                except Exception:
                    pass
            print(f"[ERROR] Gagal mengedit peminjaman: {e}")
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

        finally:
            if conn is not None:
                conn.close()

    def delete_peminjaman(self):
        """Hapus transaksi peminjaman.

        Saat transaksi dihapus, stok buku dikembalikan +1. Seluruh operasi
        dilakukan dalam satu transaksi SQLite dengan konfirmasi Yes/No.
        """
        conn = None
        try:
            # Pastikan ada baris yang dipilih
            if not self.selected_id:
                messagebox.showwarning(
                    "Peringatan",
                    "Silakan pilih baris peminjaman pada tabel terlebih dahulu.",
                )
                return

            id_pinjam = int(self.selected_id)

            # Ambil informasi transaksi yang akan dihapus
            row = database.fetch_one(
                "SELECT p.id_buku, s.nama AS nama_siswa, b.judul AS judul_buku "
                "FROM peminjaman p "
                "LEFT JOIN siswa s ON s.id_siswa = p.id_siswa "
                "LEFT JOIN buku b ON b.id_buku = p.id_buku "
                "WHERE p.id_pinjam = ?",
                (id_pinjam,),
            )
            if not row:
                messagebox.showwarning(
                    "Peringatan",
                    "Data peminjaman tidak ditemukan.",
                )
                return

            id_buku = row["id_buku"]
            nama_siswa = row["nama_siswa"]
            judul_buku = row["judul_buku"]

            # Konfirmasi Yes/No
            konfirmasi = messagebox.askyesno(
                "Konfirmasi Hapus",
                f"Apakah Anda yakin ingin menghapus transaksi peminjaman?\n\n"
                f"Nama Siswa : {nama_siswa}\n"
                f"Buku       : {judul_buku}\n\n"
                f"Stok buku akan dikembalikan (+1).\n"
                f"Tindakan ini tidak dapat dibatalkan.",
            )
            if not konfirmasi:
                return

            # Buka transaksi SQLite
            conn = database.get_connection()
            if conn is None:
                messagebox.showerror("Error", "Gagal terhubung ke database.")
                return

            cursor = conn.cursor()

            # Kembalikan stok buku +1
            cursor.execute(
                "UPDATE buku SET stok_tersedia = stok_tersedia + 1 "
                "WHERE id_buku = ?",
                (id_buku,),
            )

            # Hapus transaksi peminjaman
            cursor.execute(
                "DELETE FROM peminjaman WHERE id_pinjam = ?",
                (id_pinjam,),
            )

            # Commit transaksi
            conn.commit()

            # Refresh Treeview
            self.load_data()

            # Bersihkan form
            self.clear_form()

            # Tampilkan pesan berhasil
            messagebox.showinfo("Sukses", "Transaksi peminjaman berhasil dihapus.")

        except Exception as e:
            # Rollback jika terjadi kesalahan
            if conn is not None:
                try:
                    conn.rollback()
                except Exception:
                    pass
            print(f"[ERROR] Gagal menghapus peminjaman: {e}")
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

        finally:
            if conn is not None:
                conn.close()

    def search_peminjaman(self):
        """Cari transaksi peminjaman berdasarkan Nama Siswa atau Judul Buku (LIKE)."""
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
                "WHERE s.nama LIKE ? OR b.judul LIKE ? "
                "ORDER BY p.id_pinjam DESC",
                (pattern, pattern),
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
            print(f"[ERROR] Gagal mencari peminjaman: {e}")
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    def load_data(self):
        """Ambil riwayat peminjaman dan tampilkan pada Treeview."""
        try:
            # Pastikan tabel tersedia
            database.create_tables()

            # Ambil data peminjaman (gabung dengan buku & siswa)
            rows = database.fetch_all(
                "SELECT p.id_pinjam, p.id_buku, p.id_siswa, "
                "s.nama AS nama_siswa, s.kelas, "
                "b.judul AS judul_buku, "
                "p.tanggal_pinjam, p.tanggal_kembali, p.status "
                "FROM peminjaman p "
                "LEFT JOIN siswa s ON s.id_siswa = p.id_siswa "
                "LEFT JOIN buku b ON b.id_buku = p.id_buku "
                "ORDER BY p.id_pinjam DESC"
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

    def clear_form(self):
        """Kosongkan form dan reset tanggal otomatis."""
        try:
            self.combo_kelas.set("")
            self.combo_siswa.set("")
            self.combo_buku.set("")
            self.combo_siswa["values"] = []
            self.siswa_map = {}
            self.load_buku_options("")
            self.set_auto_dates()
            self.selected_id = None
            if self.tree.selection():
                self.tree.selection_remove(self.tree.selection())
        except Exception as e:
            print(f"[ERROR] Gagal membersihkan form: {e}")

    def on_button_click(self, action):
        """Handler tombol."""
        if action == "save":
            self.simpan_peminjaman()
        elif action == "edit":
            self.edit_peminjaman()
        elif action == "delete":
            self.delete_peminjaman()
        elif action == "search":
            self.search_peminjaman()
        elif action == "refresh":
            self.load_data()
            # Muat ulang buku sesuai kelas yang terpilih (atau kosong)
            self.load_buku_options(self.combo_kelas.get().strip())
        elif action == "clear":
            self.clear_form()
        else:
            messagebox.showinfo(
                "Informasi",
                f"Fungsi '{action.capitalize()}' belum tersedia.",
            )
