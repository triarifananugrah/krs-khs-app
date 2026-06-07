import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import *
from controllers.controllers import DosenController

class DosenView(tk.Frame):
    def __init__(self, parent, main_win):
        super().__init__(parent, bg=BG)
        self.main_win = main_win
        self.ctrl = DosenController()
        self._selected_nuptk = None
        self._build()
        self._load()

    def _build(self):
        hdr = tk.Frame(self, bg="#7C3AED", pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🎓  Data Dosen", font=TITLE_F,
                 bg="#7C3AED", fg=WHITE).pack(padx=20, anchor="w")

        form_frame = tk.LabelFrame(self, text="Form Input Data Dosen",
                                   font=LABEL_F, bg=BG, padx=15, pady=10)
        form_frame.pack(fill="x", padx=10, pady=8)

        fields = [
            ("NUPTK", "nuptk"), ("Nama Dosen", "nama"), ("Alamat", "alamat"),
        ]
        self.entries = {}
        for r, (lbl, key) in enumerate(fields):
            tk.Label(form_frame, text=lbl, font=LABEL_F, bg=BG, width=22, anchor="w").grid(row=r, column=0, sticky="w", pady=4, padx=5)
            e = tk.Entry(form_frame, font=LABEL_F, width=35, relief="solid", bd=1)
            e.grid(row=r, column=1, pady=4)
            self.entries[key] = e

        tk.Label(form_frame, text="Pendidikan Terakhir", font=LABEL_F, bg=BG, width=22, anchor="w").grid(row=3, column=0, sticky="w", pady=4, padx=5)
        self.combo_pend = ttk.Combobox(form_frame, values=["S2", "S3"], width=33, state="readonly")
        self.combo_pend.grid(row=3, column=1, pady=4, sticky="w")
        self.combo_pend.set("S2")

        tk.Label(form_frame, text="Jabatan Fungsional", font=LABEL_F, bg=BG, width=22, anchor="w").grid(row=4, column=0, sticky="w", pady=4, padx=5)
        self.combo_jab = ttk.Combobox(form_frame, values=["Asisten Ahli","Lektor","Lektor Kepala","Guru Besar"], width=33, state="readonly")
        self.combo_jab.grid(row=4, column=1, pady=4, sticky="w")
        self.combo_jab.set("Lektor")

        tk.Label(form_frame, text="Jenis Kelamin", font=LABEL_F, bg=BG, width=22, anchor="w").grid(row=5, column=0, sticky="w", pady=4, padx=5)
        self.combo_jk = ttk.Combobox(form_frame, values=["L", "P"], width=33, state="readonly")
        self.combo_jk.grid(row=5, column=1, pady=4, sticky="w")
        self.combo_jk.set("L")

        btn_f = tk.Frame(form_frame, bg=BG)
        btn_f.grid(row=6, column=0, columnspan=2, pady=10)
        styled_button(btn_f, "💾 Simpan",  "#7C3AED", self._save).pack(side="left", padx=4)
        styled_button(btn_f, "🗑  Hapus",  DANGER,    self._delete).pack(side="left", padx=4)
        styled_button(btn_f, "🔄 Reset",   "#64748B",  self._reset).pack(side="left", padx=4)

        search_bar(self, self._search)
        cols   = ("nuptk","nama","pend","jabatan","jk","alamat")
        heads  = ("NUPTK","Nama Dosen","Pendidikan","Jabatan","JK","Alamat")
        widths = (140, 200, 80, 150, 40, 200)
        self.tree = build_treeview(self, cols, heads, widths)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _load(self, rows=None):
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in (rows or self.ctrl.get_all()):
            self.tree.insert("", "end", values=r)

    def _search(self, kw):
        self._load(self.ctrl.search(kw))

    def _on_select(self, _):
        sel = self.tree.selection()
        if not sel: return
        v = self.tree.item(sel[0], "values")
        self.entries["nuptk"].delete(0,"end"); self.entries["nuptk"].insert(0, v[0])
        self.entries["nama"].delete(0,"end");  self.entries["nama"].insert(0, v[1])
        self.entries["alamat"].delete(0,"end"); self.entries["alamat"].insert(0, v[5])
        self.combo_pend.set(v[2])
        self.combo_jab.set(v[3])
        self.combo_jk.set(v[4])
        self._selected_nuptk = v[0]

    def _save(self):
        nuptk = self.entries["nuptk"].get().strip()
        nama  = self.entries["nama"].get().strip()
        if not nuptk or not nama:
            messagebox.showwarning("Peringatan","NUPTK dan Nama wajib diisi!"); return
        try:
            self.ctrl.save(nuptk, nama, self.combo_pend.get(),
                           self.combo_jab.get(), self.combo_jk.get(),
                           self.entries["alamat"].get().strip())
            toast(self.main_win, "Data dosen berhasil disimpan!")
            self._load(); self._reset()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _delete(self):
        if not self._selected_nuptk:
            messagebox.showwarning("Peringatan","Pilih data terlebih dahulu!"); return
        if messagebox.askyesno("Konfirmasi", "Hapus dosen ini?"):
            self.ctrl.delete(self._selected_nuptk)
            toast(self.main_win, "Data berhasil dihapus!", DANGER)
            self._load(); self._reset()

    def _reset(self):
        for e in self.entries.values(): e.delete(0,"end")
        self.combo_pend.set("S2"); self.combo_jab.set("Lektor"); self.combo_jk.set("L")
        self._selected_nuptk = None
