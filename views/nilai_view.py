import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import *
from controllers.controllers import NilaiController, KrsController

class NilaiView(tk.Frame):
    def __init__(self, parent, main_win):
        super().__init__(parent, bg=BG)
        self.main_win  = main_win
        self.ctrl      = NilaiController()
        self.krs_ctrl  = KrsController()
        self._sel_id_nilai = None
        self._sel_id_krs   = None
        self._build()
        self._load_all()

    def _build(self):
        hdr = tk.Frame(self, bg="#D97706", pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="✏️  Input Nilai Mahasiswa", font=TITLE_F,
                 bg="#D97706", fg=WHITE).pack(padx=20, anchor="w")

        form_f = tk.LabelFrame(self, text="Form Input Nilai",
                               font=LABEL_F, bg=BG, padx=15, pady=10)
        form_f.pack(fill="x", padx=10, pady=8)

        tk.Label(form_f, text="NIM Mahasiswa", font=LABEL_F, bg=BG, width=22, anchor="w").grid(row=0, column=0, sticky="w", pady=4, padx=5)
        nim_frame = tk.Frame(form_f, bg=BG)
        nim_frame.grid(row=0, column=1, pady=4, sticky="w")
        self.entry_nim = tk.Entry(nim_frame, font=LABEL_F, width=25, relief="solid", bd=1)
        self.entry_nim.pack(side="left")
        styled_button(nim_frame, "🔍 Cari KRS", "#D97706", self._load_krs_by_nim, width=10).pack(side="left", padx=5)

        tk.Label(form_f, text="Pilih KRS", font=LABEL_F, bg=BG, width=22, anchor="w").grid(row=1, column=0, sticky="w", pady=4, padx=5)
        self.combo_krs = ttk.Combobox(form_f, width=48, state="readonly")
        self.combo_krs.grid(row=1, column=1, pady=4, sticky="w")
        self._krs_map = {}

        tk.Label(form_f, text="Nilai Angka (0-100)", font=LABEL_F, bg=BG, width=22, anchor="w").grid(row=2, column=0, sticky="w", pady=4, padx=5)
        val_frame = tk.Frame(form_f, bg=BG)
        val_frame.grid(row=2, column=1, pady=4, sticky="w")
        self.entry_nilai = tk.Entry(val_frame, font=LABEL_F, width=10, relief="solid", bd=1)
        self.entry_nilai.pack(side="left")
        self.lbl_konversi = tk.Label(val_frame, text="", font=("Segoe UI", 10, "bold"), bg=BG, fg="#059669")
        self.lbl_konversi.pack(side="left", padx=10)
        self.entry_nilai.bind("<KeyRelease>", self._preview_konversi)

        btn_f = tk.Frame(form_f, bg=BG)
        btn_f.grid(row=3, column=0, columnspan=2, pady=10)
        styled_button(btn_f, "💾 Simpan", "#D97706", self._save).pack(side="left", padx=4)
        styled_button(btn_f, "🗑  Hapus", DANGER,    self._delete).pack(side="left", padx=4)
        styled_button(btn_f, "🔄 Reset",  "#64748B",  self._reset).pack(side="left", padx=4)

        cols   = ("id_nilai","nim","nama","mk","sks","angka","huruf","bobot","mutu")
        heads  = ("ID","NIM","Nama Mahasiswa","Mata Kuliah","SKS","Nilai Angka","Nilai Huruf","Bobot","Mutu")
        widths = (50,100,180,200,60,90,90,70,70)
        self.tree = build_treeview(self, cols, heads, widths)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _load_all(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in self.ctrl.get_all_detail():
            self.tree.insert("", "end", values=r)

    def _load_krs_by_nim(self):
        nim = self.entry_nim.get().strip()
        if not nim: return
        rows = self.krs_ctrl.get_by_nim(nim)
        if not rows:
            messagebox.showwarning("Peringatan", "Tidak ada KRS untuk NIM tersebut!"); return
        self._krs_map = {}
        options = []
        for r in rows:
            # r: id_krs, nim, nama_mhs, prodi, kode_mk, nama_mk, sks, kelas, ruang, hari, jam, nuptk, nama_dosen
            label = f"{r[4]} - {r[5]} ({r[8]}) {r[9]} {str(r[10])[:5]}"
            self._krs_map[label] = r[0]
            options.append(label)
        self.combo_krs["values"] = options
        if options: self.combo_krs.set(options[0])

    def _preview_konversi(self, _):
        try:
            angka = float(self.entry_nilai.get())
            huruf, bobot = self.ctrl.konversi(angka)
            self.lbl_konversi.config(text=f"→ {huruf}  (bobot {bobot:.2f})", fg="#059669")
        except:
            self.lbl_konversi.config(text="")

    def _on_select(self, _):
        sel = self.tree.selection()
        if not sel: return
        v = self.tree.item(sel[0], "values")
        # set nim and load krs
        self.entry_nim.delete(0,"end"); self.entry_nim.insert(0, v[1])
        self.entry_nilai.delete(0,"end"); self.entry_nilai.insert(0, v[5])
        self._sel_id_nilai = v[0]
        self._load_krs_by_nim()

    def _save(self):
        krs_label = self.combo_krs.get()
        id_krs    = self._krs_map.get(krs_label)
        nilai_str = self.entry_nilai.get().strip()
        if not id_krs or not nilai_str:
            messagebox.showwarning("Peringatan","Pilih KRS dan masukkan nilai!"); return
        try:
            float(nilai_str)
            self.ctrl.save(self._sel_id_nilai, id_krs, float(nilai_str))
            toast(self.main_win, "Nilai berhasil disimpan!")
            self._load_all(); self._reset()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _delete(self):
        if not self._sel_id_nilai:
            messagebox.showwarning("Peringatan","Pilih data terlebih dahulu!"); return
        if messagebox.askyesno("Konfirmasi","Hapus nilai ini?"):
            self.ctrl.delete(self._sel_id_nilai)
            toast(self.main_win,"Nilai dihapus!",DANGER)
            self._load_all(); self._reset()

    def _reset(self):
        self.entry_nim.delete(0,"end")
        self.entry_nilai.delete(0,"end")
        self.combo_krs.set("")
        self.combo_krs["values"] = []
        self.lbl_konversi.config(text="")
        self._krs_map = {}
        self._sel_id_nilai = None
        self._sel_id_krs   = None
