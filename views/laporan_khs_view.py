import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, sys, os
from views.base_view import *
from controllers.controllers import NilaiController
from reports.pdf_generator import cetak_khs

class LaporanKhsView(tk.Frame):
    def __init__(self, parent, main_win):
        super().__init__(parent, bg=BG)
        self.main_win = main_win
        self.ctrl = NilaiController()
        self._nim = None
        self._nama = ""
        self._prodi = ""
        self._rows = []
        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg="#7C3AED", pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🏆  Laporan KHS Mahasiswa", font=TITLE_F,
                 bg="#7C3AED", fg=WHITE).pack(padx=20, anchor="w")

        sf = tk.LabelFrame(self, text="Cari KHS Mahasiswa", font=LABEL_F, bg=BG, padx=15, pady=10)
        sf.pack(fill="x", padx=10, pady=8)
        tk.Label(sf, text="NIM Mahasiswa:", font=LABEL_F, bg=BG).grid(row=0, column=0, sticky="w", padx=5)
        self.entry_nim = tk.Entry(sf, font=LABEL_F, width=25, relief="solid", bd=1)
        self.entry_nim.grid(row=0, column=1, padx=5)
        styled_button(sf, "🔍 Tampilkan", "#7C3AED", self._show).grid(row=0, column=2, padx=10)
        styled_button(sf, "📥 Export PDF", "#059669", self._export_pdf).grid(row=0, column=3, padx=5)

        self.lbl_info = tk.Label(self, text="", font=("Segoe UI", 11, "bold"), bg=BG, fg="#7C3AED")
        self.lbl_info.pack(pady=(5,0))

        cols   = ("no","kode","nama_mk","sks","angka","huruf","bobot","mutu")
        heads  = ("No","Kode MK","Nama Mata Kuliah","SKS","Nilai Angka","Nilai Huruf","Bobot","Mutu")
        widths = (40,90,250,60,100,100,80,80)
        self.tree = build_treeview(self, cols, heads, widths)

        # Summary
        bot = tk.Frame(self, bg="#EFF6FF", relief="flat", bd=1)
        bot.pack(fill="x", padx=10, pady=8)
        self.lbl_sks   = tk.Label(bot, text="Total SKS  : -", font=("Segoe UI", 10, "bold"), bg="#EFF6FF", fg=PRIMARY)
        self.lbl_mutu  = tk.Label(bot, text="Total Mutu : -", font=("Segoe UI", 10, "bold"), bg="#EFF6FF", fg=PRIMARY)
        self.lbl_ip    = tk.Label(bot, text="IP Semester: -", font=("Segoe UI", 14, "bold"), bg="#EFF6FF", fg="#2563EB")
        self.lbl_sks.pack(side="left",  padx=20, pady=10)
        self.lbl_mutu.pack(side="left", padx=20)
        self.lbl_ip.pack(side="right",  padx=30)

    def _show(self):
        nim = self.entry_nim.get().strip()
        if not nim:
            messagebox.showwarning("Peringatan","Masukkan NIM!"); return
        self._rows = self.ctrl.get_by_nim(nim)
        if not self._rows:
            messagebox.showinfo("Info","Tidak ada data nilai untuk NIM tersebut."); return
        # r: id_nilai, id_krs, nim, nama_mhs, prodi, kode_mk, nama_mk, sks, nilai_angka, nilai_huruf, bobot, mutu
        self._nim   = nim
        self._nama  = self._rows[0][3]
        self._prodi = self._rows[0][4]
        self.lbl_info.config(text=f"Mahasiswa: {self._nama}  |  Prodi: {self._prodi}  |  NIM: {nim}")

        for i in self.tree.get_children(): self.tree.delete(i)
        for no, r in enumerate(self._rows, 1):
            self.tree.insert("", "end", values=(no, r[5], r[6], r[7], f"{r[8]:.2f}", r[9], f"{r[10]:.2f}", f"{r[11]:.2f}"))

        total_sks, total_mutu, ip = self.ctrl.hitung_ip(self._rows)
        self.lbl_sks.config(text=f"Total SKS  : {total_sks}")
        self.lbl_mutu.config(text=f"Total Mutu : {total_mutu:.2f}")

        ip_color = "#059669" if ip >= 3.0 else ("#D97706" if ip >= 2.0 else DANGER)
        self.lbl_ip.config(text=f"IP Semester : {ip:.2f}", fg=ip_color)

    def _export_pdf(self):
        if not self._rows:
            messagebox.showwarning("Peringatan","Tampilkan data KHS terlebih dahulu!"); return
        try:
            total_sks, total_mutu, ip = self.ctrl.hitung_ip(self._rows)
            path = cetak_khs(self._nim, self._nama, self._prodi, self._rows,
                             total_sks, total_mutu, ip)
            toast(self.main_win, f"PDF tersimpan: {os.path.basename(path)}", "#059669")
            if sys.platform == "win32": os.startfile(path)
            elif sys.platform == "darwin": subprocess.call(["open", path])
            else: subprocess.call(["xdg-open", path])
        except Exception as e:
            messagebox.showerror("Error PDF", str(e))
