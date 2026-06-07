import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import *
from controllers.controllers import MatakuliahController

class MatakuliahView(tk.Frame):
    def __init__(self, parent, main_win):
        super().__init__(parent, bg=BG)
        self.main_win = main_win
        self.ctrl = MatakuliahController()
        self._selected_kode = None
        self._build()
        self._load()

    def _build(self):
        hdr = tk.Frame(self, bg="#0891B2", pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📚  Data Mata Kuliah", font=TITLE_F,
                 bg="#0891B2", fg=WHITE).pack(padx=20, anchor="w")

        form_f = tk.LabelFrame(self, text="Form Input Mata Kuliah",
                               font=LABEL_F, bg=BG, padx=15, pady=10)
        form_f.pack(fill="x", padx=10, pady=8)

        fields = [("Kode MK","kode"), ("Nama Mata Kuliah","nama"), ("SKS","sks")]
        self.entries = {}
        for r, (lbl, key) in enumerate(fields):
            tk.Label(form_f, text=lbl, font=LABEL_F, bg=BG, width=22, anchor="w").grid(row=r, column=0, sticky="w", pady=4, padx=5)
            e = tk.Entry(form_f, font=LABEL_F, width=35, relief="solid", bd=1)
            e.grid(row=r, column=1, pady=4)
            self.entries[key] = e

        tk.Label(form_f, text="Semester", font=LABEL_F, bg=BG, width=22, anchor="w").grid(row=3, column=0, sticky="w", pady=4, padx=5)
        self.combo_sem = ttk.Combobox(form_f,
            values=["I","II","III","IV","V","VI","VII","VIII"],
            width=33, state="readonly")
        self.combo_sem.grid(row=3, column=1, pady=4, sticky="w")
        self.combo_sem.set("I")

        btn_f = tk.Frame(form_f, bg=BG)
        btn_f.grid(row=4, column=0, columnspan=2, pady=10)
        styled_button(btn_f, "💾 Simpan", "#0891B2", self._save).pack(side="left", padx=4)
        styled_button(btn_f, "🗑  Hapus", DANGER,    self._delete).pack(side="left", padx=4)
        styled_button(btn_f, "🔄 Reset",  "#64748B",  self._reset).pack(side="left", padx=4)

        search_bar(self, self._search)
        self.tree = build_treeview(self,
            ("kode","nama","sks","semester"),
            ("Kode MK","Nama Mata Kuliah","SKS","Semester"),
            (100, 300, 60, 80))
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _load(self, rows=None):
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in (rows or self.ctrl.get_all()):
            self.tree.insert("", "end", values=r)

    def _search(self, kw): self._load(self.ctrl.search(kw))

    def _on_select(self, _):
        sel = self.tree.selection()
        if not sel: return
        v = self.tree.item(sel[0], "values")
        self.entries["kode"].delete(0,"end"); self.entries["kode"].insert(0, v[0])
        self.entries["nama"].delete(0,"end"); self.entries["nama"].insert(0, v[1])
        self.entries["sks"].delete(0,"end");  self.entries["sks"].insert(0, v[2])
        self.combo_sem.set(v[3])
        self._selected_kode = v[0]

    def _save(self):
        kode = self.entries["kode"].get().strip()
        nama = self.entries["nama"].get().strip()
        sks  = self.entries["sks"].get().strip()
        if not kode or not nama or not sks:
            messagebox.showwarning("Peringatan","Semua field wajib diisi!"); return
        try:
            self.ctrl.save(kode, nama, int(sks), self.combo_sem.get())
            toast(self.main_win, "Mata kuliah berhasil disimpan!")
            self._load(); self._reset()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _delete(self):
        if not self._selected_kode:
            messagebox.showwarning("Peringatan","Pilih data terlebih dahulu!"); return
        if messagebox.askyesno("Konfirmasi","Hapus mata kuliah ini?"):
            self.ctrl.delete(self._selected_kode)
            toast(self.main_win, "Data berhasil dihapus!", DANGER)
            self._load(); self._reset()

    def _reset(self):
        for e in self.entries.values(): e.delete(0,"end")
        self.combo_sem.set("I")
        self._selected_kode = None
