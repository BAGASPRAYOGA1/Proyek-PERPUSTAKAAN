from tkinter import ttk
import tkinter as tk
from tkinter import messagebox

import database

# Font Segoe UI
FONT_FAMILY = "Segoe UI"


class SiswaFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.selected_id = None
        self.configure_style()
        self.create_widgets()
        # Tampilkan data siswa langsung saat halaman dibuka
        self.load_data()

    def configure_style(self):
        """Konfigurasi style untuk halaman Siswa."""
        style = ttk.Style(self)
        style.configure("Siswa.TFrame", background="#f0f4f8")
        style.configure(
            "SiswaHeader.TLabel",
            background="#f0f4f8",
            font=(FONT_FAMILY, 18, "bold"),
            foreground="#2c3e50",
        )
        style.configure(
            "SiswaFormLabel.TLabel",
            background="#f0f4f8",
            font=(FONT_FAMILY, 10),
            foreground="#34495e",
        )
        style.configure(
            "SiswaAction.TButton",
            font=(FONT_FAMILY, 10, "bold"),
            padding=(12, 6),
        )

    def create_widgets(self):
        """Membuat layout halaman Master Siswa."""
        # ===== Header =====
        header = ttk.Label(self, text="Master Siswa", style="SiswaHeader.TLabel")
        header.pack(pady=(20, 15))

        # ===== Container utama =====
        main = ttk.Frame(self, style="Siswa.TFrame")
        main.pack(fill="both", expand=True, padx=30, pady=5)

        main.columnconfigure(0, weight=2)
        main.columnconfigure(1, weight=5)
        main.rowconfigure(0, weight=1)

        # ===== Panel Kiri: Form =====
        form_panel = ttk.LabelFrame(main, text=" Form Siswa ", style="Siswa.TFrame")
        form_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        # Field NISN
        lbl_nisn = ttk.Label(form_panel, text="NISN :", style="SiswaFormLabel.TLabel")
        lbl_nisn.grid(row=0, column=0, sticky="w", padx=(15, 10), pady=8)
        self.entry_nisn = ttk.Entry(form_panel, font=(FONT_FAMILY, 10), width=25)
        self.entry_nisn.grid(row=0, column=1, sticky="ew", padx=(0, 15), pady=8)

        # Field Nama Siswa
        lbl_nama = ttk.Label(form_panel, text="Nama Siswa :", style="SiswaFormLabel.TLabel")
        lbl_nama.grid(row=1, column=0, sticky="w", padx=(15, 10), pady=8)
        self.entry_nama = ttk.Entry(form_panel, font=(FONT_FAMILY, 10), width=25)
        self.entry_nama.grid(row=1, column=1, sticky="ew", padx=(0, 15), pady=8)

        # Field Kelas (Combobox)
        lbl_kelas = ttk.Label(form_panel, text="Kelas :", style="SiswaFormLabel.TLabel")
        lbl_kelas.grid(row=2, column=0, sticky="w", padx=(15, 10), pady=8)
        self.combo_kelas = ttk.Combobox(
            form_panel,
            values=["1", "2", "3", "4", "5", "6"],
            font=(FONT_FAMILY, 10),
            state="readonly",
            width=22,
        )
        self.combo_kelas.grid(row=2, column=1, sticky="ew", padx=(0, 15), pady=8)

        # Field Jenis Kelamin (Combobox)
        lbl_jk = ttk.Label(form_panel, text="Jenis Kelamin :", style="SiswaFormLabel.TLabel")
        lbl_jk.grid(row=3, column=0, sticky="w", padx=(15, 10), pady=8)
        self.combo_jk = ttk.Combobox(
            form_panel,
            values=["Laki-laki", "Perempuan"],
            font=(FONT_FAMILY, 10),
            state="readonly",
            width=22,
        )
        self.combo_jk.grid(row=3, column=1, sticky="ew", padx=(0, 15), pady=8)

        # Field Alamat
        lbl_alamat = ttk.Label(form_panel, text="Alamat :", style="SiswaFormLabel.TLabel")
        lbl_alamat.grid(row=4, column=0, sticky="nw", padx=(15, 10), pady=8)
        self.text_alamat = tk.Text(
            form_panel,
            font=(FONT_FAMILY, 10),
            width=25,
            height=4,
            wrap="word",
        )
        self.text_alamat.grid(row=4, column=1, sticky="ew", padx=(0, 15), pady=8)

        form_panel.columnconfigure(1, weight=1)

        # ===== Panel Kanan: Cari, Tombol & Treeview =====
        right_panel = ttk.Frame(main, style="Siswa.TFrame")
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(2, weight=1)

        # Bar pencarian
        search_frame = ttk.Frame(right_panel, style="Siswa.TFrame")
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        search_label = ttk.Label(
            search_frame, text="Cari :", style="SiswaFormLabel.TLabel"
        )
        search_label.pack(side="left", padx=(0, 5))

        self.search_entry = ttk.Entry(search_frame, font=(FONT_FAMILY, 10))
        self.search_entry.pack(side="left", fill="x", expand=True)

        # Tombol aksi
        btn_frame = ttk.Frame(right_panel, style="Siswa.TFrame")
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
                style="SiswaAction.TButton",
                command=lambda k=key: self.on_button_click(k),
            )
            btn.grid(row=0, column=i, padx=3, pady=2, sticky="ew")
            self.buttons[key] = btn

        # Treeview Siswa
        tree_frame = ttk.Frame(right_panel, style="Siswa.TFrame")
        tree_frame.grid(row=2, column=0, sticky="nsew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        columns = (
            "id_siswa",
            "nisn",
            "nama",
            "kelas",
            "jenis_kelamin",
            "alamat",
        )

        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        headings = {
            "id_siswa": "ID",
            "nisn": "NISN",
            "nama": "Nama",
            "kelas": "Kelas",
            "jenis_kelamin": "Jenis Kelamin",
            "alamat": "Alamat",
        }

        widths = {
            "id_siswa": 40,
            "nisn": 120,
            "nama": 200,
            "kelas": 70,
            "jenis_kelamin": 120,
            "alamat": 250,
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(
                col,
                width=widths[col],
                anchor="center" if col in ("id_siswa", "nisn", "kelas", "jenis_kelamin") else "w",
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
        """Isi seluruh form otomatis saat satu baris Treeview dipilih."""
        try:
            selection = self.tree.selection()
            if not selection:
                return

            item = selection[0]
            values = self.tree.item(item, "values")

            if not values:
                return

            # Simpan id_siswa dari baris yang dipilih (iid = id_siswa)
            self.selected_id = item

            # Isi form sesuai urutan kolom:
            # id_siswa, nisn, nama, kelas, jenis_kelamin, alamat
            self.entry_nisn.delete(0, "end")
            self.entry_nisn.insert(0, str(values[1]) if values[1] is not None else "")

            self.entry_nama.delete(0, "end")
            self.entry_nama.insert(0, str(values[2]) if values[2] is not None else "")

            self.combo_kelas.set(str(values[3]) if values[3] is not None else "")

            self.combo_jk.set(str(values[4]) if values[4] is not None else "")

            self.text_alamat.delete("1.0", "end")
            if values[5] is not None:
                self.text_alamat.insert("1.0", str(values[5]))

        except Exception as e:
            print(f"[ERROR] Gagal mengisi form dari Treeview: {e}")

    def load_data(self):
        """Ambil seluruh data siswa dari SQLite dan tampilkan pada Treeview."""
        try:
            # Pastikan tabel tersedia
            database.create_tables()

            # Ambil seluruh data siswa
            rows = database.fetch_all(
                "SELECT id_siswa, nisn, nama, kelas, jenis_kelamin, alamat "
                "FROM siswa ORDER BY id_siswa"
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
                        iid=str(row["id_siswa"]),
                        values=(
                            row["id_siswa"],
                            row["nisn"],
                            row["nama"],
                            row["kelas"],
                            row["jenis_kelamin"],
                            row["alamat"],
                        ),
                    )

        except Exception as e:
            print(f"[ERROR] Gagal memuat data siswa: {e}")

    def clear_form(self):
        """Kosongkan semua field pada form dan hilangkan pilihan pada Treeview."""
        try:
            self.entry_nisn.delete(0, "end")
            self.entry_nama.delete(0, "end")
            self.combo_kelas.set("")
            self.combo_jk.set("")
            self.text_alamat.delete("1.0", "end")
            self.selected_id = None
            # Hilangkan pilihan pada Treeview
            if self.tree.selection():
                self.tree.selection_remove(self.tree.selection())
        except Exception as e:
            print(f"[ERROR] Gagal membersihkan form: {e}")

    def add_siswa(self):
        """Tambah data siswa baru ke SQLite dengan validasi."""
        try:
            # Ambil nilai dari form
            nisn = self.entry_nisn.get().strip()
            nama = self.entry_nama.get().strip()
            kelas = self.combo_kelas.get().strip()
            jenis_kelamin = self.combo_jk.get().strip()
            alamat = self.text_alamat.get("1.0", "end").strip()

            # Validasi: semua field wajib diisi
            fields = {
                "NISN": nisn,
                "Nama Siswa": nama,
                "Kelas": kelas,
                "Jenis Kelamin": jenis_kelamin,
                "Alamat": alamat,
            }

            empty = [name for name, value in fields.items() if not value]
            if empty:
                messagebox.showwarning(
                    "Peringatan",
                    f"Field berikut wajib diisi:\n- " + "\n- ".join(empty),
                )
                return

            # Validasi: Nama tidak boleh kosong (sudah terwakili di atas, tapi tetap dicek eksplisit)
            if not nama:
                messagebox.showwarning(
                    "Peringatan",
                    "Nama Siswa tidak boleh kosong.",
                )
                return

            # Validasi: NISN tidak boleh sama
            existing = database.fetch_one(
                "SELECT id_siswa FROM siswa WHERE nisn = ?",
                (nisn,),
            )
            if existing:
                messagebox.showwarning(
                    "Peringatan",
                    f"NISN '{nisn}' sudah digunakan.",
                )
                return

            # Simpan ke SQLite
            result = database.execute_query(
                "INSERT INTO siswa (nisn, nama, jenis_kelamin, kelas, alamat) "
                "VALUES (?, ?, ?, ?, ?)",
                (nisn, nama, jenis_kelamin, kelas, alamat),
            )

            if result is None:
                messagebox.showerror(
                    "Error",
                    "Gagal menyimpan data siswa ke database.",
                )
                return

            # Refresh Treeview
            self.load_data()

            # Kosongkan form
            self.clear_form()

            # Tampilkan MessageBox berhasil
            messagebox.showinfo("Sukses", f"Siswa '{nama}' berhasil ditambahkan.")

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
            print(f"[ERROR] Gagal menambah siswa: {e}")

    def edit_siswa(self):
        """Update data siswa berdasarkan id_siswa."""
        try:
            # Pastikan ada baris yang dipilih
            if not self.selected_id:
                messagebox.showwarning(
                    "Peringatan",
                    "Silakan pilih baris siswa pada tabel terlebih dahulu.",
                )
                return

            # Ambil nilai dari form
            nisn = self.entry_nisn.get().strip()
            nama = self.entry_nama.get().strip()
            kelas = self.combo_kelas.get().strip()
            jenis_kelamin = self.combo_jk.get().strip()
            alamat = self.text_alamat.get("1.0", "end").strip()

            # Validasi: semua field wajib diisi
            fields = {
                "NISN": nisn,
                "Nama Siswa": nama,
                "Kelas": kelas,
                "Jenis Kelamin": jenis_kelamin,
                "Alamat": alamat,
            }

            empty = [name for name, value in fields.items() if not value]
            if empty:
                messagebox.showwarning(
                    "Peringatan",
                    f"Field berikut wajib diisi:\n- " + "\n- ".join(empty),
                )
                return

            # Validasi: Nama tidak boleh kosong
            if not nama:
                messagebox.showwarning(
                    "Peringatan",
                    "Nama Siswa tidak boleh kosong.",
                )
                return

            # Validasi: NISN tidak boleh sama (kecuali untuk record yang sedang diedit)
            existing = database.fetch_one(
                "SELECT id_siswa FROM siswa WHERE nisn = ? AND id_siswa != ?",
                (nisn, self.selected_id),
            )
            if existing:
                messagebox.showwarning(
                    "Peringatan",
                    f"NISN '{nisn}' sudah digunakan.",
                )
                return

            # Update berdasarkan id_siswa
            result = database.execute_query(
                "UPDATE siswa SET nisn = ?, nama = ?, jenis_kelamin = ?, kelas = ?, alamat = ? "
                "WHERE id_siswa = ?",
                (nisn, nama, jenis_kelamin, kelas, alamat, self.selected_id),
            )

            if result is None:
                messagebox.showerror(
                    "Error",
                    "Gagal mengupdate data siswa ke database.",
                )
                return

            # Refresh Treeview
            self.load_data()

            # Kosongkan form
            self.clear_form()

            # Tampilkan MessageBox berhasil
            messagebox.showinfo("Sukses", f"Siswa '{nama}' berhasil diperbarui.")

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
            print(f"[ERROR] Gagal mengedit siswa: {e}")

    def delete_siswa(self):
        """Hapus data siswa berdasarkan id_siswa dengan konfirmasi Yes/No."""
        try:
            # Pastikan ada baris yang dipilih
            if not self.selected_id:
                messagebox.showwarning(
                    "Peringatan",
                    "Silakan pilih baris siswa pada tabel terlebih dahulu.",
                )
                return

            # Ambil informasi siswa yang akan dihapus
            row = database.fetch_one(
                "SELECT nisn, nama FROM siswa WHERE id_siswa = ?",
                (self.selected_id,),
            )
            if not row:
                messagebox.showwarning(
                    "Peringatan",
                    "Data siswa tidak ditemukan.",
                )
                return

            nisn = row["nisn"]
            nama = row["nama"]

            # Konfirmasi Yes/No
            konfirmasi = messagebox.askyesno(
                "Konfirmasi Hapus",
                f"Apakah Anda yakin ingin menghapus siswa:\n\n"
                f"NISN : {nisn}\n"
                f"Nama : {nama}\n\n"
                f"Tindakan ini tidak dapat dibatalkan.",
            )
            if not konfirmasi:
                return

            # Hapus data berdasarkan id_siswa
            result = database.execute_query(
                "DELETE FROM siswa WHERE id_siswa = ?",
                (self.selected_id,),
            )

            if result is None:
                messagebox.showerror(
                    "Error",
                    "Gagal menghapus data siswa dari database.",
                )
                return

            # Refresh Treeview
            self.load_data()

            # Kosongkan form
            self.clear_form()

            # Tampilkan MessageBox berhasil
            messagebox.showinfo("Sukses", f"Siswa '{nama}' berhasil dihapus.")

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
            print(f"[ERROR] Gagal menghapus siswa: {e}")

    def search_siswa(self):
        """Cari siswa berdasarkan NISN atau Nama (LIKE)."""
        try:
            keyword = self.search_entry.get().strip()

            # Jika kotak pencarian kosong, tampilkan seluruh data
            if not keyword:
                self.load_data()
                return

            # Cari berdasarkan NISN atau Nama menggunakan LIKE
            pattern = f"%{keyword}%"
            rows = database.fetch_all(
                "SELECT id_siswa, nisn, nama, kelas, jenis_kelamin, alamat "
                "FROM siswa WHERE nisn LIKE ? OR nama LIKE ? "
                "ORDER BY id_siswa",
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
                        iid=str(row["id_siswa"]),
                        values=(
                            row["id_siswa"],
                            row["nisn"],
                            row["nama"],
                            row["kelas"],
                            row["jenis_kelamin"],
                            row["alamat"],
                        ),
                    )
            else:
                messagebox.showinfo(
                    "Informasi",
                    f"Tidak ditemukan siswa dengan kata kunci '{keyword}'.",
                )

        except Exception as e:
            print(f"[ERROR] Gagal mencari siswa: {e}")

    def on_button_click(self, action):
        """Handler tombol."""
        if action == "refresh":
            self.load_data()
        elif action == "add":
            self.add_siswa()
        elif action == "edit":
            self.edit_siswa()
        elif action == "delete":
            self.delete_siswa()
        elif action == "search":
            self.search_siswa()
        elif action == "clear":
            self.clear_form()
        else:
            print(f"[INFO] Tombol '{action}' ditekan. Fungsi belum tersedia.")
