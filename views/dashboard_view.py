import tkinter as tk
from tkinter import ttk

class DashboardView(tk.Frame):
    def __init__(self, parent, counts):
        super().__init__(parent, bg="#F8FAFC")
        self._build(counts)

    def _build(self, counts):
        # Title
        title_frame = tk.Frame(self, bg="#2563EB", pady=20)
        title_frame.pack(fill="x")
        tk.Label(title_frame, text="SISTEM INFORMASI AKADEMIK",
                 font=("Segoe UI", 18, "bold"), bg="#2563EB", fg="white").pack()
        tk.Label(title_frame, text="Universitas Muhammadiyah Palu",
                 font=("Segoe UI", 11), bg="#2563EB", fg="#BFDBFE").pack()

        # Cards
        card_frame = tk.Frame(self, bg="#F8FAFC", pady=30)
        card_frame.pack(fill="both", expand=True, padx=30)

        cards = [
            ("👥  Mahasiswa",  counts.get("mahasiswa", 0),  "#2563EB", "#DBEAFE"),
            ("🎓  Dosen",      counts.get("dosen", 0),       "#7C3AED", "#EDE9FE"),
            ("📚  Mata Kuliah", counts.get("matakuliah", 0), "#0891B2", "#CFFAFE"),
            ("📋  Total KRS",  counts.get("krs", 0),         "#059669", "#D1FAE5"),
        ]

        for col, (label, val, color, bg) in enumerate(cards):
            card = tk.Frame(card_frame, bg=bg, padx=25, pady=20,
                            relief="flat", bd=0, cursor="hand2")
            card.grid(row=0, column=col, padx=12, pady=10, sticky="nsew")
            card_frame.columnconfigure(col, weight=1)

            tk.Label(card, text=str(val), font=("Segoe UI", 36, "bold"),
                     bg=bg, fg=color).pack()
            tk.Label(card, text=label, font=("Segoe UI", 11),
                     bg=bg, fg="#374151").pack(pady=(4, 0))

        # Info
        info_frame = tk.Frame(self, bg="#FFFFFF", padx=30, pady=20,
                              relief="flat", bd=1)
        info_frame.pack(fill="x", padx=30, pady=(0, 20))
        tk.Label(info_frame, text="ℹ️  Informasi Sistem",
                 font=("Segoe UI", 11, "bold"), bg="#FFFFFF", fg="#1E293B").pack(anchor="w")
        tk.Label(info_frame,
                 text="Pilih menu di sebelah kiri untuk mengelola data akademik.\n"
                      "Sistem ini mendukung CRUD Mahasiswa, Dosen, Mata Kuliah, KRS, Nilai, serta Laporan KRS dan KHS.",
                 font=("Segoe UI", 10), bg="#FFFFFF", fg="#64748B", justify="left").pack(anchor="w", pady=(5, 0))
