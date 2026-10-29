from datetime import date
import tkinter as tk
from tkinter import ttk

import database

FONT_FAMILY = "Segoe UI"


class DashboardFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.value_labels = {}
        self.configure_style()

        database.create_tables()
        self.create_widgets()
        self.refresh_data()
        self.bind_tab_refresh()

    def bind_tab_refresh(self):
        try:
            notebook = self.master
            if notebook is not None and hasattr(notebook, "bind"):
                notebook.bind(
                    "<<NotebookTabChanged>>", self.on_tab_changed, add="+"
                )
        except Exception as e:
            print(f"[ERROR] Gagal mengikat event tab: {e}")

    def on_tab_changed(self, event=None):
        try:
            notebook = self.master
            if notebook is None or not hasattr(notebook, "select"):
                return
            selected = notebook.select()
            if selected and str(selected) == str(self):
                self.refresh_data()
        except Exception as e:
            print(f"[ERROR] Gagal memproses perubahan tab: {e}")

    def configure_style(self):
        style = ttk.Style(self)
        style.configure("Dashboard.TFrame", background="#f8fafc")

        # Style Card Container
        style.configure(
            "Card.TFrame",
            background="#ffffff",
            relief="solid",
            borderwidth=1,
            bordercolor="#e2e8f0",
        )

        # Style Text Card
        style.configure(
            "CardTitle.TLabel",
            background="#ffffff",
            font=(FONT_FAMILY, 10, "bold"),
            foreground="#64748b",
        )
        style.configure(
            "CardValue.TLabel",
            background="#ffffff",
            font=(FONT_FAMILY, 24, "bold"),
            foreground="#0f172a",
        )
        style.configure(
            "CardSub.TLabel",
            background="#ffffff",
            font=(FONT_FAMILY, 9),
            foreground="#94a3b8",
        )

        # Header Styles
        style.configure(
            "HeaderTitle.TLabel",
            background="#f8fafc",
            font=(FONT_FAMILY, 20, "bold"),
            foreground="#1e293b",
        )
        style.configure(
            "HeaderSub.TLabel",
            background="#f8fafc",
            font=(FONT_FAMILY, 10, "italic"),
            foreground="#64748b",
        )

        # Section Labels
        style.configure(
            "Aktivitas.TLabel",
            background="#ffffff",
            font=(FONT_FAMILY, 11, "bold"),
            foreground="#1d4ed8",
        )
        style.configure(
            "Peringatan.TLabel",
            background="#ffffff",
            font=(FONT_FAMILY, 11, "bold"),
            foreground="#ef4444",
        )

        # Treeview Styles
        style.configure(
            "Custom.Treeview",
            rowheight=32,
            font=(FONT_FAMILY, 9),
            background="#ffffff",
            fieldbackground="#ffffff",
            borderwidth=0,
        )
        style.configure(
            "Custom.Treeview.Heading",
            font=(FONT_FAMILY, 9, "bold"),
            background="#f8fafc",
            foreground="#334155",
            relief="flat",
        )

    def create_widgets(self):
        # Frame Utaman dengan Background Terang
        self.main_container = ttk.Frame(self, style="Dashboard.TFrame")
        self.main_container.pack(fill="both", expand=True, padx=30, pady=20)

        # Header Title & Subtitle
        header_frame = ttk.Frame(self.main_container, style="Dashboard.TFrame")
        header_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(
            header_frame,
            text="Dashboard Perpustakaan",
            style="HeaderTitle.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            header_frame,
            text="Ringkasan informasi perpustakaan secara real-time",
            style="HeaderSub.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        # Grid 4 Kartu Stat (1 baris)
        cards_frame = ttk.Frame(self.main_container, style="Dashboard.TFrame")
        cards_frame.pack(fill="x", pady=(0, 20))

        cards_data = [
            (
                "total_buku",
                "Total Buku",
                "Judul Buku",
                "📘",
                "#e0f2fe",
                "#0284c7",
            ),
            (
                "total_siswa",
                "Total Siswa",
                "Siswa Terdaftar",
                "👥",
                "#dcfce7",
                "#16a34a",
            ),
            (
                "buku_dipinjam",
                "Sedang Dipinjam",
                "Buku Dipinjam",
                "📖",
                "#fef3c7",
                "#d97706",
            ),
            (
                "buku_dikembalikan",
                "Sudah Dikembalikan",
                "Buku Dikembalikan",
                "✔",
                "#d1fae5",
                "#059669",
            ),
        ]

        for i, (key, title, sub, icon, bg_color, fg_color) in enumerate(
            cards_data
        ):
            cards_frame.columnconfigure(i, weight=1)
            self.create_stat_card(
                cards_frame, i, key, title, sub, icon, bg_color, fg_color
            )

        # Panel Bawah (2 Kolom: Aktivitas & Peringatan)
        bottom_frame = ttk.Frame(self.main_container, style="Dashboard.TFrame")
        bottom_frame.pack(fill="both", expand=True)
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)

        self.create_aktivitas_section(bottom_frame)
        self.create_peringatan_section(bottom_frame)

    def create_stat_card(
        self, parent, col, key, title, sub_text, icon, bg_color, fg_color
    ):
        card = tk.Frame(
            parent,
            bg="#ffffff",
            highlightbackground="#e2e8f0",
            highlightthickness=1,
            bd=0,
        )
        card.grid(row=0, column=col, padx=(0 if col == 0 else 10, 0), sticky="nsew")

        # Icon Box (Kiri)
        icon_box = tk.Label(
            card,
            text=icon,
            font=(FONT_FAMILY, 20),
            bg=bg_color,
            fg=fg_color,
            width=3,
            height=2,
        )
        icon_box.pack(side="left", padx=15, pady=15)

        # Text Box (Kanan)
        info_frame = tk.Frame(card, bg="#ffffff")
        info_frame.pack(side="left", fill="both", expand=True, pady=12)

        tk.Label(
            info_frame,
            text=title,
            font=(FONT_FAMILY, 9, "bold"),
            fg="#64748b",
            bg="#ffffff",
            anchor="w",
        ).pack(fill="x")

        val_label = tk.Label(
            info_frame,
            text="0",
            font=(FONT_FAMILY, 20, "bold"),
            fg="#0f172a",
            bg="#ffffff",
            anchor="w",
        )
        val_label.pack(fill="x")
        self.value_labels[key] = val_label

        tk.Label(
            info_frame,
            text=sub_text,
            font=(FONT_FAMILY, 8),
            fg="#94a3b8",
            bg="#ffffff",
            anchor="w",
        ).pack(fill="x")

    def create_aktivitas_section(self, parent):
        card = tk.Frame(
            parent,
            bg="#ffffff",
            highlightbackground="#e2e8f0",
            highlightthickness=1,
        )
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Header Section
        header = tk.Frame(card, bg="#ffffff")
        header.pack(fill="x", padx=15, pady=12)
        ttk.Label(
            header,
            text="📑  Aktivitas Terbaru",
            style="Aktivitas.TLabel",
        ).pack(anchor="w")

        # Treeview
        tree_frame = ttk.Frame(card)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        columns = ("nama_siswa", "judul_buku", "aktivitas", "tanggal")
        self.aktivitas_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            height=7,
        )

        headings = {
            "nama_siswa": "Nama Siswa",
            "judul_buku": "Buku",
            "aktivitas": "Aktivitas",
            "tanggal": "Tanggal",
        }
        widths = {
            "nama_siswa": 140,
            "judul_buku": 180,
            "aktivitas": 100,
            "tanggal": 130,
        }

        for col in columns:
            self.aktivitas_tree.heading(col, text=headings[col])
            self.aktivitas_tree.column(
                col,
                width=widths[col],
                anchor="center" if col in ("aktivitas", "tanggal") else "w",
            )

        self.aktivitas_tree.pack(fill="both", expand=True)

        # Config Tag Warna Teks untuk Aktivitas
        self.aktivitas_tree.tag_configure(
            "Peminjaman", foreground="#16a34a", font=(FONT_FAMILY, 9, "bold")
        )
        self.aktivitas_tree.tag_configure(
            "Pengembalian", foreground="#2563eb", font=(FONT_FAMILY, 9, "bold")
        )

    def create_peringatan_section(self, parent):
        card = tk.Frame(
            parent,
            bg="#ffffff",
            highlightbackground="#e2e8f0",
            highlightthickness=1,
        )
        card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        # Header Section
        header = tk.Frame(card, bg="#ffffff")
        header.pack(fill="x", padx=15, pady=12)
        ttk.Label(
            header, text="🔔  Peringatan", style="Peringatan.TLabel"
        ).pack(anchor="w")

        # Treeview
        tree_frame = ttk.Frame(card)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        columns = ("nama_siswa", "judul_buku", "terlambat")
        self.peringatan_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            height=7,
        )

        headings = {
            "nama_siswa": "Nama Siswa",
            "judul_buku": "Buku",
            "terlambat": "Terlambat (hari)",
        }
        widths = {"nama_siswa": 140, "judul_buku": 200, "terlambat": 110}

        for col in columns:
            self.peringatan_tree.heading(col, text=headings[col])
            self.peringatan_tree.column(
                col,
                width=widths[col],
                anchor="center" if col == "terlambat" else "w",
            )

        self.peringatan_tree.pack(fill="both", expand=True)
        self.peringatan_tree.tag_configure(
            "TerlambatTag", foreground="#dc2626", font=(FONT_FAMILY, 9, "bold")
        )

    def load_aktivitas(self):
        try:
            rows = database.fetch_all(
                "SELECT s.nama AS nama_siswa, b.judul AS judul_buku, "
                "p.tanggal_pinjam AS tanggal, 'Peminjaman' AS aktivitas "
                "FROM peminjaman p "
                "JOIN siswa s ON s.id_siswa = p.id_siswa "
                "JOIN buku b ON b.id_buku = p.id_buku "
                "UNION ALL "
                "SELECT s.nama AS nama_siswa, b.judul AS judul_buku, "
                "p.tanggal_dikembalikan AS tanggal, 'Pengembalian' AS aktivitas "
                "FROM peminjaman p "
                "JOIN siswa s ON s.id_siswa = p.id_siswa "
                "JOIN buku b ON b.id_buku = p.id_buku "
                "WHERE p.tanggal_dikembalikan IS NOT NULL "
                "ORDER BY tanggal DESC LIMIT 10"
            )

            for item in self.aktivitas_tree.get_children():
                self.aktivitas_tree.delete(item)

            if rows:
                for row in rows:
                    act = row["aktivitas"]
                    self.aktivitas_tree.insert(
                        "",
                        "end",
                        values=(
                            row["nama_siswa"],
                            row["judul_buku"],
                            act,
                            row["tanggal"],
                        ),
                        tags=(act,),
                    )
        except Exception as e:
            print(f"[ERROR] Gagal memuat Aktivitas Terbaru: {e}")

    def load_peringatan(self):
        try:
            today = date.today().strftime("%Y-%m-%d")
            rows = database.fetch_all(
                "SELECT s.nama AS nama_siswa, b.judul AS judul_buku, "
                "CAST(julianday(?) - julianday(p.tanggal_kembali) AS INTEGER) AS terlambat "
                "FROM peminjaman p "
                "JOIN siswa s ON s.id_siswa = p.id_siswa "
                "JOIN buku b ON b.id_buku = p.id_buku "
                "WHERE p.status = 'Dipinjam' AND p.tanggal_kembali < ? "
                "ORDER BY terlambat DESC LIMIT 10",
                (today, today),
            )

            for item in self.peringatan_tree.get_children():
                self.peringatan_tree.delete(item)

            if rows:
                for row in rows:
                    self.peringatan_tree.insert(
                        "",
                        "end",
                        values=(
                            row["nama_siswa"],
                            row["judul_buku"],
                            row["terlambat"],
                        ),
                        tags=("TerlambatTag",),
                    )
        except Exception as e:
            print(f"[ERROR] Gagal memuat Peringatan: {e}")

    def refresh_data(self):
        try:
            # 1. Total Buku
            r = database.fetch_one("SELECT COUNT(*) AS total FROM buku")
            self.value_labels["total_buku"].config(text=str(r["total"] if r else 0))

            # 2. Total Siswa
            r = database.fetch_one("SELECT COUNT(*) AS total FROM siswa")
            self.value_labels["total_siswa"].config(text=str(r["total"] if r else 0))

            # 3. Sedang Dipinjam
            r = database.fetch_one(
                "SELECT COUNT(*) AS total FROM peminjaman WHERE status = 'Dipinjam'"
            )
            self.value_labels["buku_dipinjam"].config(
                text=str(r["total"] if r else 0)
            )

            # 4. Sudah Dikembalikan
            r = database.fetch_one(
                "SELECT COUNT(*) AS total FROM peminjaman WHERE status = 'Dikembalikan'"
            )
            self.value_labels["buku_dikembalikan"].config(
                text=str(r["total"] if r else 0)
            )

            self.load_aktivitas()
            self.load_peringatan()
        except Exception as e:
            print(f"[ERROR] Gagal memuat data dashboard: {e}")