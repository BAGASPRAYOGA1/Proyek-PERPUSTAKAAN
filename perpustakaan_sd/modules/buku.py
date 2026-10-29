from tkinter import ttk
import tkinter as tk
from tkinter import messagebox

import database

# Font Segoe UI
FONT_FAMILY = "Segoe UI"


class BukuFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.selected_id = None
        self.configure_style()
        self.create_widgets()
        # Tampilkan data buku langsung saat halaman dibuka
        self.load_data()

    def configure_style(self):
        """Konfigurasi style untuk halaman Buku."""
        style = ttk.Style(self)
        style.configure("Buku.TFrame", background="#f0f4f8")
        style.configure(
            "BukuHeader.TLabel",
            background="#f0f4f8",
            font=(FONT_FAMILY, 18, "bold"),
            foreground="#2c3e50",
        )
        style.configure(
            "BukuFormLabel.TLabel",
            background="#f0f4f8",
            font=(FONT_FAMILY, 10),
            foreground="#34495e",
        )
        style.configure(
            "BukuAction.TButton",
            font=(FONT_FAMILY, 10, "bold"),
            padding=(12, 6),
        )

    def create_widgets(self):
        """Membuat layout halaman CRUD Buku."""
        # ===== Header =====
        header = ttk.Label(self, text="Manajemen Buku", style="BukuHeader.TLabel")
        header.pack(pady=(20, 15))

        # ===== Container utama =====
        main = ttk.Frame(self, style="Buku.TFrame")
        main.pack(fill="both", expand=True, padx=30, pady=5)

        main.columnconfigure(0, weight=3)
        main.columnconfigure(1, weight=4)
        main.rowconfigure(0, weight=1)

        # ===== Panel Kiri: Form =====
        form_panel = ttk.LabelFrame(main, text=" Form Buku ", style="Buku.TFrame")
        form_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        fields_before = [
            ("Kode Buku", "kode_buku"),
            ("Judul Buku", "judul"),
        ]

        fields_after = [
            ("Kategori", "kategori"),
            ("Penerbit", "penerbit"),
            ("Tahun Terbit", "tahun"),
            ("Rak", "rak"),
            ("Stok Total", "stok_total"),
            ("Stok Tersedia", "stok_tersedia"),
        ]

        self.entries = {}

        row = 0
        for label, key in fields_before:
            lbl = ttk.Label(form_panel, text=label + " :", style="BukuFormLabel.TLabel")
            lbl.grid(row=row, column=0, sticky="w", padx=(15, 10), pady=8)

            ent = ttk.Entry(form_panel, font=(FONT_FAMILY, 10), width=25)
            ent.grid(row=row, column=1, sticky="ew", padx=(0, 15), pady=8)
            self.entries[key] = ent
            row += 1

        # Field Kelas (Combobox)
        lbl_kelas = ttk.Label(form_panel, text="Kelas :", style="BukuFormLabel.TLabel")
        lbl_kelas.grid(row=row, column=0, sticky="w", padx=(15, 10), pady=8)
        self.combo_kelas = ttk.Combobox(
            form_panel,
            values=["1", "2", "3", "4", "5", "6"],
            font=(FONT_FAMILY, 10),
            state="readonly",
            width=22,
        )
        self.combo_kelas.grid(row=row, column=1, sticky="ew", padx=(0, 15), pady=8)
        row += 1

        for label, key in fields_after:
            lbl = ttk.Label(form_panel, text=label + " :", style="BukuFormLabel.TLabel")
            lbl.grid(row=row, column=0, sticky="w", padx=(15, 10), pady=8)

            ent = ttk.Entry(form_panel, font=(FONT_FAMILY, 10), width=25)
            ent.grid(row=row, column=1, sticky="ew", padx=(0, 15), pady=8)
            self.entries[key] = ent
            row += 1

        form_panel.columnconfigure(1, weight=1)

        # ===== Panel Kanan: Cari, Tombol & Treeview =====
        right_panel = ttk.Frame(main, style="Buku.TFrame")
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(2, weight=1)

        # Bar pencarian
        search_frame = ttk.Frame(right_panel, style="Buku.TFrame")
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        search_label = ttk.Label(
            search_frame, text="Cari :", style="BukuFormLabel.TLabel"
        )
        search_label.pack(side="left", padx=(0, 5))

        self.search_entry = ttk.Entry(search_frame, font=(FONT_FAMILY, 10))
        self.search_entry.pack(side="left", fill="x", expand=True)

        # Tombol aksi
        btn_frame = ttk.Frame(right_panel, style="Buku.TFrame")
        btn_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        btn_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        buttons = [
            ("Tambah", "add"),
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
                style="BukuAction.TButton",
                command=lambda k=key: self.on_button_click(k),
            )
            btn.grid(row=0, column=i, padx=3, pady=2, sticky="ew")
            self.buttons[key] = btn

        # Treeview Buku
        tree_frame = ttk.Frame(right_panel, style="Buku.TFrame")
        tree_frame.grid(row=2, column=0, sticky="nsew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        columns = (
            "id_buku",
            "kode_buku",
            "judul",
            "kelas",
            "kategori",
            "penerbit",
            "tahun",
            "rak",
            "stok_total",
            "stok_tersedia",
        )

        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        headings = {
            "id_buku": "ID",
            "kode_buku": "Kode Buku",
            "judul": "Judul",
            "kelas": "Kelas",
            "kategori": "Kategori",
            "penerbit": "Penerbit",
            "tahun": "Tahun",
            "rak": "Rak",
            "stok_total": "Stok Total",
            "stok_tersedia": "Stok Tersedia",
        }

        widths = {
            "id_buku": 40,
            "kode_buku": 100,
            "judul": 200,
            "kelas": 60,
            "kategori": 100,
            "penerbit": 120,
            "tahun": 70,
            "rak": 60,
            "stok_total": 90,
            "stok_tersedia": 100,
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(
                col,
                width=widths[col],
                anchor="center" if col in ("id_buku", "kelas", "tahun", "rak", "stok_total", "stok_tersedia") else "w",
            )

        self.tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scroll_y.set)

        scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        scroll_x.grid(row=1, column=0, sticky="ew")
        self.tree.configure(xscrollcommand=scroll_x.set)

        # Event saat baris Treeview dipilih
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def on_tree_select(self, event=None):
        """Isi seluruh Entry otomatis saat satu baris Treeview dipilih."""
        try:
            selection = self.tree.selection()
            if not selection:
                return

            item = selection[0]
            values = self.tree.item(item, "values")

            if not values:
                return

            # Simpan id_buku dari baris yang dipilih (iid = id_buku)
            self.selected_id = item

# Urutan kolom: id_buku, kode_buku, judul, kelas, kategori, penerbit, tahun, rak, stok_total, stok_tersedia
            keys = [
                "kode_buku",
                "judul",
                "kategori",
                "penerbit",
                "tahun",
                "rak",
                "stok_total",
                "stok_tersedia",
            ]

            # Kelas diisi dari index 3 (nilai ke-4)
            self.combo_kelas.set(
                str(values[3]) if values[3] is not None else ""
            )

            # Nilai dimulai dari index 1 (lewati id_buku)
            for i, key in enumerate(keys):
                self.entries[key].delete(0, "end")
                self.entries[key].insert(0, str(values[i + 1]) if values[i + 1] is not None else "")

        except Exception as e:
            print(f"[ERROR] Gagal mengisi form dari Treeview: {e}")

    def load_data(self):
        """Ambil seluruh data buku dari SQLite dan tampilkan pada Treeview."""
        try:
            # Pastikan tabel tersedia
            database.create_tables()

# Ambil seluruh data buku
            rows = database.fetch_all(
                "SELECT id_buku, kode_buku, judul, kelas, kategori, penerbit, "
                "tahun, rak, stok_total, stok_tersedia FROM buku ORDER BY id_buku"
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
                        iid=str(row["id_buku"]),
                        values=(
                            row["id_buku"],
                            row["kode_buku"],
                            row["judul"],
                            row["kelas"],
                            row["kategori"],
                            row["penerbit"],
                            row["tahun"],
                            row["rak"],
                            row["stok_total"],
                            row["stok_tersedia"],
                        ),
                    )

        except Exception as e:
            print(f"[ERROR] Gagal memuat data buku: {e}")

    def search_buku(self):
        """Cari buku berdasarkan Kode Buku atau Judul Buku menggunakan LIKE."""
        try:
            # Pastikan tabel tersedia
            database.create_tables()

            kata = self.search_entry.get().strip()

            # Jika kotak pencarian kosong, tampilkan seluruh data
            if not kata:
                self.load_data()
                return

# Cari berdasarkan Kode Buku atau Judul Buku (case-insensitive)
            rows = database.fetch_all(
                "SELECT id_buku, kode_buku, judul, kelas, kategori, penerbit, "
                "tahun, rak, stok_total, stok_tersedia FROM buku "
                "WHERE kode_buku LIKE ? OR judul LIKE ? ORDER BY id_buku",
                (f"%{kata}%", f"%{kata}%"),
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
                        iid=str(row["id_buku"]),
                        values=(
                            row["id_buku"],
                            row["kode_buku"],
                            row["judul"],
                            row["kelas"],
                            row["kategori"],
                            row["penerbit"],
                            row["tahun"],
                            row["rak"],
                            row["stok_total"],
                            row["stok_tersedia"],
                        ),
                    )
            else:
                print(f"[INFO] Pencarian '{kata}' tidak menemukan data.")

        except Exception as e:
            print(f"[ERROR] Gagal mencari buku: {e}")

    def on_button_click(self, action):
        """Handler tombol."""
        if action == "refresh":
            self.load_data()
        elif action == "add":
            self.add_buku()
        elif action == "edit":
            self.edit_buku()
        elif action == "delete":
            self.delete_buku()
        elif action == "search":
            self.search_buku()
        elif action == "clear":
            self.clear_form()
        else:
            print(f"[INFO] Tombol '{action}' ditekan. Fungsi belum tersedia.")

    def add_buku(self):
        """Tambah data buku baru ke SQLite dengan validasi."""
        try:
            # Ambil nilai dari form
            kode_buku = self.entries["kode_buku"].get().strip()
            judul = self.entries["judul"].get().strip()
            kelas = self.combo_kelas.get().strip()
            kategori = self.entries["kategori"].get().strip()
            penerbit = self.entries["penerbit"].get().strip()
            tahun = self.entries["tahun"].get().strip()
            rak = self.entries["rak"].get().strip()
            stok_total = self.entries["stok_total"].get().strip()
            stok_tersedia = self.entries["stok_tersedia"].get().strip()

            # Validasi: semua field wajib diisi
            fields = {
                "Kode Buku": kode_buku,
                "Judul Buku": judul,
                "Kelas": kelas,
                "Kategori": kategori,
                "Penerbit": penerbit,
                "Tahun Terbit": tahun,
                "Rak": rak,
                "Stok Total": stok_total,
                "Stok Tersedia": stok_tersedia,
            }

            empty = [name for name, value in fields.items() if not value]
            if empty:
                messagebox.showwarning(
                    "Peringatan",
                    f"Field berikut wajib diisi:\n- " + "\n- ".join(empty),
                )
                return

            # Validasi: stok harus angka dan tidak boleh negatif
            try:
                stok_total_int = int(stok_total)
                stok_tersedia_int = int(stok_tersedia)
            except ValueError:
                messagebox.showwarning(
                    "Peringatan",
                    "Stok Total dan Stok Tersedia harus berupa angka.",
                )
                return

            if stok_total_int < 0 or stok_tersedia_int < 0:
                messagebox.showwarning(
                    "Peringatan",
                    "Stok tidak boleh negatif.",
                )
                return

            # Validasi: kode buku unik
            existing = database.fetch_one(
                "SELECT id_buku FROM buku WHERE kode_buku = ?",
                (kode_buku,),
            )
            if existing:
                messagebox.showwarning(
                    "Peringatan",
                    f"Kode Buku '{kode_buku}' sudah digunakan.",
                )
                return

            # Simpan ke SQLite
            result = database.execute_query(
                "INSERT INTO buku (kode_buku, judul, kelas, kategori, penerbit, tahun, rak, stok_total, stok_tersedia) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    kode_buku,
                    judul,
                    kelas,
                    kategori,
                    penerbit,
                    tahun,
                    rak,
                    stok_total_int,
                    stok_tersedia_int,
                ),
            )

            if result is None:
                messagebox.showerror(
                    "Error",
                    "Gagal menyimpan data buku ke database.",
                )
                return

            # Refresh Treeview
            self.load_data()

            # Kosongkan form
            self.clear_form()

            # Tampilkan MessageBox berhasil
            messagebox.showinfo("Sukses", f"Buku '{judul}' berhasil ditambahkan.")

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
            print(f"[ERROR] Gagal menambah buku: {e}")

    def clear_form(self):
        """Kosongkan semua field pada form."""
        try:
            for entry in self.entries.values():
                entry.delete(0, "end")
            self.combo_kelas.set("")
            self.selected_id = None
        except Exception as e:
            print(f"[ERROR] Gagal membersihkan form: {e}")

    def delete_buku(self):
        """Hapus data buku berdasarkan id_buku dengan konfirmasi Yes/No."""
        try:
            # Pastikan ada baris yang dipilih
            if not self.selected_id:
                messagebox.showwarning(
                    "Peringatan",
                    "Silakan pilih baris buku pada tabel terlebih dahulu.",
                )
                return

            # Ambil informasi buku yang akan dihapus
            row = database.fetch_one(
                "SELECT kode_buku, judul FROM buku WHERE id_buku = ?",
                (self.selected_id,),
            )
            if not row:
                messagebox.showwarning(
                    "Peringatan",
                    "Data buku tidak ditemukan.",
                )
                return

            kode_buku = row["kode_buku"]
            judul = row["judul"]

            # Konfirmasi Yes/No
            konfirmasi = messagebox.askyesno(
                "Konfirmasi Hapus",
                f"Apakah Anda yakin ingin menghapus buku:\n\n"
                f"Kode Buku : {kode_buku}\n"
                f"Judul     : {judul}\n\n"
                f"Tindakan ini tidak dapat dibatalkan.",
            )
            if not konfirmasi:
                return

            # Hapus data berdasarkan id_buku
            result = database.execute_query(
                "DELETE FROM buku WHERE id_buku = ?",
                (self.selected_id,),
            )

            if result is None:
                messagebox.showerror(
                    "Error",
                    "Gagal menghapus data buku dari database.",
                )
                return

            # Refresh Treeview
            self.load_data()

            # Kosongkan form
            self.clear_form()

            # Tampilkan MessageBox berhasil
            messagebox.showinfo("Sukses", f"Buku '{judul}' berhasil dihapus.")

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
            print(f"[ERROR] Gagal menghapus buku: {e}")

    def edit_buku(self):
        """Update data buku berdasarkan id_buku."""
        try:
            # Pastikan ada baris yang dipilih
            if not self.selected_id:
                messagebox.showwarning(
                    "Peringatan",
                    "Silakan pilih baris buku pada tabel terlebih dahulu.",
                )
                return

# Ambil nilai dari form
            kode_buku = self.entries["kode_buku"].get().strip()
            judul = self.entries["judul"].get().strip()
            kelas = self.combo_kelas.get().strip()
            kategori = self.entries["kategori"].get().strip()
            penerbit = self.entries["penerbit"].get().strip()
            tahun = self.entries["tahun"].get().strip()
            rak = self.entries["rak"].get().strip()
            stok_total = self.entries["stok_total"].get().strip()
            stok_tersedia = self.entries["stok_tersedia"].get().strip()

            # Validasi: semua field wajib diisi
            fields = {
                "Kode Buku": kode_buku,
                "Judul Buku": judul,
                "Kelas": kelas,
                "Kategori": kategori,
                "Penerbit": penerbit,
                "Tahun Terbit": tahun,
                "Rak": rak,
                "Stok Total": stok_total,
                "Stok Tersedia": stok_tersedia,
            }

            empty = [name for name, value in fields.items() if not value]
            if empty:
                messagebox.showwarning(
                    "Peringatan",
                    f"Field berikut wajib diisi:\n- " + "\n- ".join(empty),
                )
                return

            # Validasi: stok harus angka dan tidak boleh negatif
            try:
                stok_total_int = int(stok_total)
                stok_tersedia_int = int(stok_tersedia)
            except ValueError:
                messagebox.showwarning(
                    "Peringatan",
                    "Stok Total dan Stok Tersedia harus berupa angka.",
                )
                return

            if stok_total_int < 0 or stok_tersedia_int < 0:
                messagebox.showwarning(
                    "Peringatan",
                    "Stok tidak boleh negatif.",
                )
                return

            # Validasi: kode buku unik (kecuali untuk record yang sedang diedit)
            existing = database.fetch_one(
                "SELECT id_buku FROM buku WHERE kode_buku = ? AND id_buku != ?",
                (kode_buku, self.selected_id),
            )
            if existing:
                messagebox.showwarning(
                    "Peringatan",
                    f"Kode Buku '{kode_buku}' sudah digunakan.",
                )
                return

# Update berdasarkan id_buku
            result = database.execute_query(
                "UPDATE buku SET kode_buku = ?, judul = ?, kelas = ?, kategori = ?, penerbit = ?, "
                "tahun = ?, rak = ?, stok_total = ?, stok_tersedia = ? WHERE id_buku = ?",
                (
                    kode_buku,
                    judul,
                    kelas,
                    kategori,
                    penerbit,
                    tahun,
                    rak,
                    stok_total_int,
                    stok_tersedia_int,
                    self.selected_id,
                ),
            )

            if result is None:
                messagebox.showerror(
                    "Error",
                    "Gagal mengupdate data buku ke database.",
                )
                return

            # Refresh Treeview
            self.load_data()

            # Kosongkan form
            self.clear_form()

            # Tampilkan MessageBox berhasil
            messagebox.showinfo("Sukses", f"Buku '{judul}' berhasil diperbarui.")

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
            print(f"[ERROR] Gagal mengedit buku: {e}")

