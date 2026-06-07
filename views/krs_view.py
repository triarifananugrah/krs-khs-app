import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import *
from controllers.controllers import KrsController, MatakuliahController, DosenController
from controllers.mahasiswa_controller import MahasiswaController

class KrsView(tk.Frame):
    def __init__(self, parent, main_win):
        super().__init__(parent, bg=BG)
        self.main_win = main_win
        self.ctrl     = KrsController()
        self.mhs_ctrl = MahasiswaController()
        self.mk_ctrl  = MatakuliahController()
        self.dsn_ctrl = DosenController()
        self._selected_id = None
        self._mk_map  = {}   # display -> kode_mk
        self._dsn_map = {}   # display -> nuptk
        self._build()
        self._load()

    def _build(self):
        hdr = tk.Frame(self, bg="#059669", pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📋  Input KRS", font=TITLE_F,
                 bg="#059669", fg=WHITE).pack(padx=20, anchor="w")

        form_f = tk.LabelFrame(self, text="Form Input KRS",
                               font=LABEL_F, bg=BG, padx=15, pady=10)
        form_f.pack(fill="x", padx=10, pady=8)

        # Left column
        left = tk.Frame(form_f, bg=BG); left.grid(row=0, column=0, padx=(0,20), sticky="n")
        right = tk.Frame(form_f, bg=BG); right.grid(row=0, column=1, sticky="n")

        tk.Label(left, text="NIM Mahasiswa", font=LABEL_F, bg=BG, width=22, anchor="w").grid(row=0, column=0, sticky="w", pady=4)
        self.entry_nim = tk.Entry(left, font=LABEL_F, width=30, relief="solid", bd=1)
        self.entry_nim.grid(row=0, column=1, pady=4, padx=5)

        tk.Label(left, text="Mata Kuliah", font=LABEL_F, bg=BG, width=22, anchor="w").grid(row=1, column=0, sticky="w", pady=4)
        self.combo_mk = ttk.Combobox(left, width=28, state="readonly")
        self.combo_mk.grid(row=1, column=1, pady=4, padx=5, sticky="w")

        tk.Label(left, text="Dosen Pengampu", font=LABEL_F, bg=BG, width=22, anchor="w").grid(row=2, column=0, sticky="w", pady=4)
        self.combo_dsn = ttk.Combobox(left, width=28, state="readonly")
        self.combo_dsn.grid(row=2, column=1, pady=4, padx=5, sticky="w")

        tk.Label(left, text="Hari", font=LABEL_F, bg=BG, width=22, anchor="w").grid(row=3, column=0, sticky="w", pady=4)
        self.combo_hari = ttk.Combobox(left, values=["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu"], width=28, state="readonly")
        self.combo_hari.grid(row=3, column=1, pady=4, padx=5, sticky="w")
        self.combo_hari.set("Senin")

        tk.Label(right, text="Kelas", font=LABEL_F, bg=BG, width=22, anchor="w").grid(row=0, column=0, sticky="w", pady=4)
        self.entry_kelas = tk.Entry(right, font=LABEL_F, width=30, relief="solid", bd=1)
        self.entry_kelas.grid(row=0, column=1, pady=4, padx=5)

        tk.Label(right, text="Ruang", font=LABEL_F, bg=BG, width=22, anchor="w").grid(row=1, column=0, sticky="w", pady=4)
        self.entry_ruang = tk.Entry(right, font=LABEL_F, width=30, relief="solid", bd=1)
        self.entry_ruang.grid(row=1, column=1, pady=4, padx=5)

        tk.Label(right, text="Jam (HH:MM)", font=LABEL_F, bg=BG, width=22, anchor="w").grid(row=2, column=0, sticky="w", pady=4)
        self.entry_jam = tk.Entry(right, font=LABEL_F, width=30, relief="solid", bd=1)
        self.entry_jam.grid(row=2, column=1, pady=4, padx=5)

        btn_f = tk.Frame(form_f, bg=BG)
        btn_f.grid(row=1, column=0, columnspan=2, pady=10)
        styled_button(btn_f, "💾 Simpan", "#059669", self._save).pack(side="left", padx=4)
        styled_button(btn_f, "🗑  Hapus", DANGER,    self._delete).pack(side="left", padx=4)
        styled_button(btn_f, "🔄 Reset",  "#64748B",  self._reset).pack(side="left", padx=4)

        search_bar(self, self._search)
        cols   = ("id","nim","nama","kode_mk","nama_mk","sks","kelas","ruang","hari","jam","dosen")
        heads  = ("ID","NIM","Nama Mahasiswa","Kode MK","Mata Kuliah","SKS","Kelas","Ruang","Hari","Jam","Dosen")
        widths = (40,100,170,80,200,50,60,70,80,70,180)
        self.tree = build_treeview(self, cols, heads, widths)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self._refresh_combos()

    def _refresh_combos(self):
        mk_opts = self.mk_ctrl.get_options()
        self._mk_map = {f"{r[0]} - {r[1]}": r[0] for r in mk_opts}
        self.combo_mk["values"] = list(self._mk_map.keys())

        dsn_opts = self.dsn_ctrl.get_options()
        self._dsn_map = {f"{r[1]}": r[0] for r in dsn_opts}
        self.combo_dsn["values"] = list(self._dsn_map.keys())

    def _load(self, rows=None):
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in (rows or self.ctrl.get_all()):
            self.tree.insert("", "end", values=(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],str(r[9])[:5],r[10]))

    def _search(self, kw): self._load(self.ctrl.search(kw))

    def _on_select(self, _):
        sel = self.tree.selection()
        if not sel: return
        v = self.tree.item(sel[0], "values")
        self.entry_nim.delete(0,"end");   self.entry_nim.insert(0, v[1])
        self.entry_kelas.delete(0,"end"); self.entry_kelas.insert(0, v[6])
        self.entry_ruang.delete(0,"end"); self.entry_ruang.insert(0, v[7])
        self.entry_jam.delete(0,"end");   self.entry_jam.insert(0, v[9])
        self.combo_hari.set(v[8])
        # Set MK combo
        mk_key = next((k for k, val in self._mk_map.items() if val == v[3]), "")
        self.combo_mk.set(mk_key)
        dsn_key = next((k for k in self._dsn_map if k == v[10]), "")
        self.combo_dsn.set(dsn_key)
        self._selected_id = v[0]

    def _save(self):
        nim   = self.entry_nim.get().strip()
        mk    = self._mk_map.get(self.combo_mk.get())
        nuptk = self._dsn_map.get(self.combo_dsn.get())
        hari  = self.combo_hari.get()
        jam   = self.entry_jam.get().strip()
        kelas = self.entry_kelas.get().strip()
        ruang = self.entry_ruang.get().strip()
        if not nim or not mk or not nuptk or not jam:
            messagebox.showwarning("Peringatan","NIM, Mata Kuliah, Dosen, dan Jam wajib diisi!"); return
        try:
            self.ctrl.save(self._selected_id, nim, mk, kelas, ruang, hari, jam, nuptk)
            toast(self.main_win, "KRS berhasil disimpan!")
            self._load(); self._reset()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _delete(self):
        if not self._selected_id:
            messagebox.showwarning("Peringatan","Pilih data terlebih dahulu!"); return
        if messagebox.askyesno("Konfirmasi","Hapus data KRS ini?"):
            self.ctrl.delete(self._selected_id)
            toast(self.main_win, "Data KRS dihapus!", DANGER)
            self._load(); self._reset()

    def _reset(self):
        self.entry_nim.delete(0,"end")
        self.entry_kelas.delete(0,"end")
        self.entry_ruang.delete(0,"end")
        self.entry_jam.delete(0,"end")
        self.combo_hari.set("Senin")
        self.combo_mk.set("")
        self.combo_dsn.set("")
        self._selected_id = None
