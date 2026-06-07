"""
Aplikasi KRS dan KHS Mahasiswa
Universitas Muhammadiyah Palu
Dosen: Nursalim, S.Kom., M.Kom.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import tkinter as tk
from tkinter import messagebox

from config.db_config import test_connection, get_connection
from views.dashboard_view    import DashboardView
from views.mahasiswa_view    import MahasiswaView
from views.dosen_view        import DosenView
from views.matakuliah_view   import MatakuliahView
from views.krs_view          import KrsView
from views.nilai_view        import NilaiView
from views.laporan_krs_view  import LaporanKrsView
from views.laporan_khs_view  import LaporanKhsView
from controllers.mahasiswa_controller import MahasiswaController
from controllers.controllers import DosenController, MatakuliahController, KrsController

SIDEBAR_BG = "#1E293B"
SIDEBAR_HOVER = "#2D3F55"
ACTIVE_BG = "#2563EB"
WHITE = "#FFFFFF"
GRAY = "#94A3B8"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Informasi Akademik — Universitas Muhammadiyah Palu")
        self.geometry("1200x700")
        self.minsize(900, 600)
        self.configure(bg="#F8FAFC")

        if not test_connection():
            messagebox.showerror(
                "Koneksi Gagal",
                "Tidak dapat terhubung ke database MySQL.\n\n"
                "Pastikan:\n"
                "1. MySQL / XAMPP / Laragon sudah berjalan\n"
                "2. Database 'dbakademik' sudah dibuat\n"
                "3. Konfigurasi di config/db_config.py sudah benar"
            )
            self.destroy()
            return

        self._active_btn = None
        self._build_layout()
        self._show("dashboard")

    def _build_layout(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=SIDEBAR_BG, width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo / Brand
        brand = tk.Frame(self.sidebar, bg="#0F172A", pady=18)
        brand.pack(fill="x")
        tk.Label(brand, text="🎓", font=("Segoe UI", 20), bg="#0F172A", fg=WHITE).pack()
        tk.Label(brand, text="SIA Akademik", font=("Segoe UI", 11, "bold"),
                 bg="#0F172A", fg=WHITE).pack()
        tk.Label(brand, text="UM Palu", font=("Segoe UI", 8),
                 bg="#0F172A", fg=GRAY).pack()

        # Menu items
        self.nav_buttons = {}
        menus = [
            ("dashboard",    "🏠  Dashboard"),
            ("mahasiswa",    "👥  Mahasiswa"),
            ("dosen",        "🎓  Dosen"),
            ("matakuliah",   "📚  Mata Kuliah"),
            ("krs",          "📋  Input KRS"),
            ("nilai",        "✏️   Input Nilai"),
            ("laporan_krs",  "📄  Laporan KRS"),
            ("laporan_khs",  "🏆  Laporan KHS"),
        ]

        # Separator label
        tk.Label(self.sidebar, text="MENU UTAMA", font=("Segoe UI", 7, "bold"),
                 bg=SIDEBAR_BG, fg=GRAY).pack(anchor="w", padx=15, pady=(12, 2))

        for key, label in menus:
            btn = tk.Button(
                self.sidebar, text=label,
                font=("Segoe UI", 10), anchor="w",
                bg=SIDEBAR_BG, fg=WHITE, bd=0,
                activebackground=ACTIVE_BG, activeforeground=WHITE,
                cursor="hand2", padx=15, pady=10,
                command=lambda k=key: self._show(k)
            )
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=SIDEBAR_HOVER) if b != self._active_btn else None)
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=ACTIVE_BG if b == self._active_btn else SIDEBAR_BG))
            self.nav_buttons[key] = btn

        # Logout
        tk.Frame(self.sidebar, bg=SIDEBAR_BG).pack(fill="y", expand=True)
        tk.Button(self.sidebar, text="🚪  Keluar", font=("Segoe UI", 10),
                  anchor="w", bg="#EF4444", fg=WHITE, bd=0,
                  activebackground="#DC2626", activeforeground=WHITE,
                  cursor="hand2", padx=15, pady=10,
                  command=self._quit).pack(fill="x")

        # Main content area
        self.content = tk.Frame(self, bg="#F8FAFC")
        self.content.pack(side="left", fill="both", expand=True)

    def _show(self, page):
        # Update active button
        if self._active_btn:
            self._active_btn.config(bg=SIDEBAR_BG)
        btn = self.nav_buttons.get(page)
        if btn:
            btn.config(bg=ACTIVE_BG)
            self._active_btn = btn

        # Clear content
        for w in self.content.winfo_children():
            w.destroy()

        # Render page
        if page == "dashboard":
            counts = {
                "mahasiswa":  MahasiswaController().count(),
                "dosen":      DosenController().count(),
                "matakuliah": MatakuliahController().count(),
                "krs":        KrsController().count(),
            }
            DashboardView(self.content, counts).pack(fill="both", expand=True)
        elif page == "mahasiswa":
            MahasiswaView(self.content, self).pack(fill="both", expand=True)
        elif page == "dosen":
            DosenView(self.content, self).pack(fill="both", expand=True)
        elif page == "matakuliah":
            MatakuliahView(self.content, self).pack(fill="both", expand=True)
        elif page == "krs":
            KrsView(self.content, self).pack(fill="both", expand=True)
        elif page == "nilai":
            NilaiView(self.content, self).pack(fill="both", expand=True)
        elif page == "laporan_krs":
            LaporanKrsView(self.content, self).pack(fill="both", expand=True)
        elif page == "laporan_khs":
            LaporanKhsView(self.content, self).pack(fill="both", expand=True)

    def _quit(self):
        if messagebox.askyesno("Keluar", "Yakin ingin keluar dari aplikasi?"):
            self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
