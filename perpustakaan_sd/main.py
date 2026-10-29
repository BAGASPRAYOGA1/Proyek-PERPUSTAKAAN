import datetime
import tkinter as tk
from tkinter import font, ttk

import database
from modules.buku import BukuFrame
from modules.dashboard import DashboardFrame
from modules.laporan import LaporanFrame
from modules.peminjaman import PeminjamanFrame
from modules.pengembalian import PengembalianFrame
from modules.rekap_buku import RekapBukuFrame
from modules.siswa import SiswaFrame


def main():
    database.create_tables()

    root = tk.Tk()
    root.title("Sistem Informasi Perpustakaan SD")
    root.geometry("1400x800")
    root.resizable(True, True)
    root.configure(bg="#1d4ed8")  # Latar belakang header biru

    # Font Default
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(family="Segoe UI", size=10)
    root.option_add("*Font", default_font)

    # ==========================================================
    # STYLING GLOBAL & NOTEBOOK TAB (BIRU MODERN)
    # ==========================================================
    style = ttk.Style()
    style.theme_use("default")  # Menggunakan tema default

    # Header Top Bar & Latar Belakang Tab
    style.configure(
        "TNotebook",
        background="#1d4ed8",
        borderwidth=0,
        tabmargins=[15, 10, 15, 0],
    )

    # Tab Normal (Putih / Abu-abu terang)
    style.configure(
        "TNotebook.Tab",
        background="#f1f5f9",
        foreground="#334155",
        font=("Segoe UI", 10, "bold"),
        padding=[16, 8],
        borderwidth=0,
        focusthickness=0,
    )

    # Tab Aktif (Biru Cerah & Teks Putih)
    style.map(
        "TNotebook.Tab",
        background=[("selected", "#2563eb"), ("active", "#eff6ff")],
        foreground=[("selected", "#ffffff"), ("active", "#1d4ed8")],
    )

    # Container Utama
    main_container = tk.Frame(root, bg="#1d4ed8")
    main_container.pack(fill="both", expand=True)

    notebook = ttk.Notebook(main_container, style="TNotebook")
    notebook.pack(fill="both", expand=True)

    # Inisialisasi Frame Modul
    dashboard_frame = DashboardFrame(notebook)
    buku_frame = BukuFrame(notebook)
    siswa_frame = SiswaFrame(notebook)
    peminjaman_frame = PeminjamanFrame(notebook)
    pengembalian_frame = PengembalianFrame(notebook)
    laporan_frame = LaporanFrame(notebook)
    rekap_buku_frame = RekapBukuFrame(notebook)

    # Tambah Tab Navigasi
    notebook.add(dashboard_frame, text="  🏠  Dashboard  ")
    notebook.add(buku_frame, text="  📖  Buku  ")
    notebook.add(siswa_frame, text="  🎓  Siswa  ")
    notebook.add(peminjaman_frame, text="  👨‍💼  Peminjaman  ")
    notebook.add(pengembalian_frame, text="  ↔  Pengembalian  ")
    notebook.add(laporan_frame, text="  📊  Laporan  ")
    notebook.add(rekap_buku_frame, text="  📋  Rekap Buku  ")

    # Footer Bar
    footer = tk.Frame(root, bg="#1e40af", height=30)
    footer.pack(fill="x", side="bottom")

    today_str = datetime.date.today().strftime("%d-%m-%Y")
    lbl_date = tk.Label(
        footer,
        text=f"📅 {today_str}",
        bg="#1e40af",
        fg="#ffffff",
        font=("Segoe UI", 9, "bold"),
    )
    lbl_date.pack(side="left", padx=15, pady=4)

    lbl_user = tk.Label(
        footer,
        text="👤 Administrator",
        bg="#1e40af",
        fg="#ffffff",
        font=("Segoe UI", 9, "bold"),
    )
    lbl_user.pack(side="right", padx=15, pady=4)

    root.mainloop()


if __name__ == "__main__":
    main()