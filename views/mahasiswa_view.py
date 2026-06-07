import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import *
from controllers.mahasiswa_controller import MahasiswaController

class MahasiswaView(tk.Frame):
    def __init__(self, parent, main_win):
        super().__init__(parent, bg=BG)
        self.main_win = main_win
        self.ctrl = MahasiswaController()
        self._selected_nim = None
        self._build()
        self._load()

    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=PRIMARY, pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="👥  Data Mahasiswa", font=TITLE_F,
                 bg=PRIMARY, fg=WHITE).pack(padx=20, anchor="w")

        # Form
        form_frame = tk.LabelFrame(self, text="Form Input Data Mahasiswa",
                                   font=LABEL_F, bg=BG, padx=15, pady=10)
        form_frame.pack(fill="x", padx=10, pady=8)

        fields_left = [
            ("NIM", "nim"), ("Nama Mahasiswa", "nama"),
            ("Program Studi", "prodi"), ("Tempat Lahir", "tempat"),
            ("Tanggal Lahir (YYYY-MM-DD)", "tgl"),
        ]
        fields_right = [
            ("Alamat", "alamat"), ("Desa/Kelurahan", "desa"),
            ("Kecamatan", "kec"), ("Kabupaten/Kota", "kab"),
            ("Provinsi", "prov"),
        ]

        self.entries = {}
        left_col = tk.Frame(form_frame, bg=BG)
        left_col.grid(row=0, column=0, padx=(0,20), sticky="n")
        right_col = tk.Frame(form_frame, bg=BG)
        right_col.grid(row=0, column=1, sticky="n")

        for r, (label, key) in enumerate(fields_left):
            tk.Label(left_col, text=label, font=LABEL_F, bg=BG,
                     anchor="w", width=28).grid(row=r, column=0, sticky="w", pady=3)
            e = tk.Entry(left_col, font=LABEL_F, width=30, relief="solid", bd=1)
            e.grid(row=r, column=1, pady=3, padx=5)
            self.entries[key] = e

        for r, (label, key) in enumerate(fields_right):
            tk.Label(right_col, text=label, font=LABEL_F, bg=BG,
                     anchor="w", width=28).grid(row=r, column=0, sticky="w", pady=3)
            e = tk.Entry(right_col, font=LABEL_F, width=30, relief="solid", bd=1)
            e.grid(row=r, column=1, pady=3, padx=5)
            self.entries[key] = e

        # JK Combobox
        tk.Label(left_col, text="Jenis Kelamin", font=LABEL_F, bg=BG,
                 anchor="w", width=28).grid(row=5, column=0, sticky="w", pady=3)
        self.combo_jk = ttk.Combobox(left_col, values=["L", "P"], width=28, state="readonly")
        self.combo_jk.grid(row=5, column=1, pady=3, padx=5, sticky="w")
        self.combo_jk.set("L")

        # Buttons
        btn_frame = tk.Frame(form_frame, bg=BG)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        styled_button(btn_frame, "💾 Simpan",  PRIMARY, self._save).pack(side="left", padx=4)
        styled_button(btn_frame, "✏️  Ubah",   "#0891B2", self._save).pack(side="left", padx=4)
        styled_button(btn_frame, "🗑  Hapus",  DANGER,   self._delete).pack(side="left", padx=4)
        styled_button(btn_frame, "🔄 Reset",   "#64748B", self._reset).pack(side="left", padx=4)

        # Search + Treeview
        search_bar(self, self._search)
        cols   = ("nim","nama","prodi","jk","tempat","tgl","alamat","desa","kec","kab","prov")
        heads  = ("NIM","Nama Mahasiswa","Prodi","JK","Tempat Lahir","Tgl Lahir","Alamat","Desa/Kel","Kecamatan","Kab/Kota","Provinsi")
        widths = (100, 180, 130, 40, 120, 100, 150, 120, 110, 130, 120)
        self.tree = build_treeview(self, cols, heads, widths)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _load(self, rows=None):
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in (rows or self.ctrl.get_all()):
            tgl = str(r[5]) if r[5] else ""
            self.tree.insert("", "end", values=(r[0],r[1],r[2],r[3],r[4],tgl,r[6],r[7],r[8],r[9],r[10]))

    def _search(self, kw):
        self._load(self.ctrl.search(kw))

    def _on_select(self, _):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0], "values")
        keys = ["nim","nama","prodi","tempat","tgl","alamat","desa","kec","kab","prov"]
        indices = [0,1,2,4,5,6,7,8,9,10]
        for key, idx in zip(keys, indices):
            self.entries[key].delete(0,"end")
            self.entries[key].insert(0, vals[idx])
        self.combo_jk.set(vals[3])
        self._selected_nim = vals[0]

    def _get_vals(self):
        return (
            self.entries["nim"].get().strip(),
            self.entries["nama"].get().strip(),
            self.entries["prodi"].get().strip(),
            self.combo_jk.get(),
            self.entries["tempat"].get().strip(),
            self.entries["tgl"].get().strip() or None,
            self.entries["alamat"].get().strip(),
            self.entries["desa"].get().strip(),
            self.entries["kec"].get().strip(),
            self.entries["kab"].get().strip(),
            self.entries["prov"].get().strip(),
        )

    def _save(self):
        vals = self._get_vals()
        if not vals[0] or not vals[1]:
            messagebox.showwarning("Peringatan", "NIM dan Nama wajib diisi!")
            return
        try:
            op = self.ctrl.save(*vals)
            msg = "Data berhasil disimpan!" if op == "insert" else "Data berhasil diperbarui!"
            toast(self.main_win, msg)
            self._load()
            self._reset()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _delete(self):
        if not self._selected_nim:
            messagebox.showwarning("Peringatan", "Pilih data terlebih dahulu!")
            return
        if messagebox.askyesno("Konfirmasi", f"Hapus mahasiswa {self._selected_nim}?"):
            self.ctrl.delete(self._selected_nim)
            toast(self.main_win, "Data berhasil dihapus!", DANGER)
            self._load()
            self._reset()

    def _reset(self):
        for e in self.entries.values():
            e.delete(0, "end")
        self.combo_jk.set("L")
        self._selected_nim = None
