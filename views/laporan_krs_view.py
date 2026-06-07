import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, sys, os
from views.base_view import *
from controllers.controllers import KrsController
from reports.pdf_generator import cetak_krs

class LaporanKrsView(tk.Frame):
    def __init__(self, parent, main_win):
        super().__init__(parent, bg=BG)
        self.main_win = main_win
        self.ctrl = KrsController()
        self._nim = None
        self._nama = ""
        self._prodi = ""
        self._rows = []
        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg="#2563EB", pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📄  Laporan KRS Mahasiswa", font=TITLE_F,
                 bg="#2563EB", fg=WHITE).pack(padx=20, anchor="w")

        # Search frame
        sf = tk.LabelFrame(self, text="Cari KRS Mahasiswa", font=LABEL_F, bg=BG, padx=15, pady=10)
        sf.pack(fill="x", padx=10, pady=8)
        tk.Label(sf, text="NIM Mahasiswa:", font=LABEL_F, bg=BG).grid(row=0, column=0, sticky="w", padx=5)
        self.entry_nim = tk.Entry(sf, font=LABEL_F, width=25, relief="solid", bd=1)
        self.entry_nim.grid(row=0, column=1, padx=5)
        styled_button(sf, "🔍 Tampilkan", PRIMARY, self._show).grid(row=0, column=2, padx=10)
        styled_button(sf, "📥 Export PDF", "#059669", self._export_pdf).grid(row=0, column=3, padx=5)

        # Info
        self.lbl_info = tk.Label(self, text="", font=("Segoe UI", 11, "bold"), bg=BG, fg=PRIMARY)
        self.lbl_info.pack(pady=(5,0))

        # Treeview
        cols   = ("no","kode","nama_mk","sks","kelas","ruang","hari","jam","dosen")
        heads  = ("No","Kode MK","Nama Mata Kuliah","SKS","Kelas","Ruang","Hari","Jam","Dosen Pengampu")
        widths = (40,90,220,60,60,70,90,70,200)
        self.tree = build_treeview(self, cols, heads, widths)

        # Total SKS
        bot = tk.Frame(self, bg=BG)
        bot.pack(fill="x", padx=10, pady=5)
        self.lbl_total = tk.Label(bot, text="", font=("Segoe UI", 11, "bold"), bg=BG, fg=PRIMARY)
        self.lbl_total.pack(anchor="e")

    def _show(self):
        nim = self.entry_nim.get().strip()
        if not nim:
            messagebox.showwarning("Peringatan","Masukkan NIM terlebih dahulu!"); return
        self._rows = self.ctrl.get_by_nim(nim)
        if not self._rows:
            messagebox.showinfo("Info","Tidak ada KRS untuk NIM tersebut."); return
        # r: id_krs, nim, nama_mhs, prodi, kode_mk, nama_mk, sks, kelas, ruang, hari, jam, nuptk, nama_dosen
        self._nim   = nim
        self._nama  = self._rows[0][2]
        self._prodi = self._rows[0][3]
        self.lbl_info.config(text=f"Mahasiswa: {self._nama}  |  Prodi: {self._prodi}  |  NIM: {nim}")
        for i in self.tree.get_children(): self.tree.delete(i)
        total_sks = 0
        for no, r in enumerate(self._rows, 1):
            self.tree.insert("", "end", values=(no, r[4], r[5], r[6], r[7], r[8], r[9], str(r[10])[:5], r[12]))
            total_sks += r[6]
        self.lbl_total.config(text=f"Total SKS: {total_sks}")

    def _export_pdf(self):
        if not self._rows:
            messagebox.showwarning("Peringatan","Tampilkan data KRS terlebih dahulu!"); return
        try:
            path = cetak_krs(self._nim, self._nama, self._prodi, self._rows)
            toast(self.main_win, f"PDF tersimpan: {os.path.basename(path)}", "#059669")
            if sys.platform == "win32": os.startfile(path)
            elif sys.platform == "darwin": subprocess.call(["open", path])
            else: subprocess.call(["xdg-open", path])
        except Exception as e:
            messagebox.showerror("Error PDF", str(e))
