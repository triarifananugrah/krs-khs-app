import tkinter as tk
from tkinter import ttk, messagebox

# ── Warna & font global ─────────────────────────────────────
BG      = "#F8FAFC"
PRIMARY = "#2563EB"
SIDEBAR = "#1E293B"
SUCCESS = "#22C55E"
DANGER  = "#EF4444"
WHITE   = "#FFFFFF"
LABEL_F = ("Segoe UI", 10)
TITLE_F = ("Segoe UI", 13, "bold")

def styled_button(parent, text, color, command, width=12):
    b = tk.Button(parent, text=text, bg=color, fg=WHITE,
                  font=("Segoe UI", 9, "bold"), relief="flat",
                  activebackground=color, activeforeground=WHITE,
                  cursor="hand2", width=width, pady=5,
                  command=command)
    b.bind("<Enter>", lambda e: b.config(bg=_darken(color)))
    b.bind("<Leave>", lambda e: b.config(bg=color))
    return b

def _darken(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = (max(0, int(h[i:i+2], 16) - 30) for i in (0, 2, 4))
    return f"#{r:02x}{g:02x}{b:02x}"

def build_treeview(parent, columns, headings, widths):
    frame = tk.Frame(parent, bg=BG)
    frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview.Heading",
                    font=("Segoe UI", 9, "bold"),
                    background=PRIMARY, foreground=WHITE)
    style.configure("Custom.Treeview",
                    font=("Segoe UI", 9), rowheight=26,
                    background=WHITE, fieldbackground=WHITE)
    style.map("Custom.Treeview", background=[("selected", PRIMARY)])

    vsb = ttk.Scrollbar(frame, orient="vertical")
    hsb = ttk.Scrollbar(frame, orient="horizontal")
    tree = ttk.Treeview(frame, columns=columns, show="headings",
                        style="Custom.Treeview",
                        yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.config(command=tree.yview)
    hsb.config(command=tree.xview)

    for col, head, w in zip(columns, headings, widths):
        tree.heading(col, text=head,
                     command=lambda c=col, t=tree: sort_tree(t, c, False))
        tree.column(col, width=w, minwidth=40)

    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)
    return tree

def sort_tree(tree, col, reverse):
    data = [(tree.set(k, col), k) for k in tree.get_children("")]
    try:
        data.sort(key=lambda t: float(t[0]), reverse=reverse)
    except ValueError:
        data.sort(reverse=reverse)
    for idx, (_, k) in enumerate(data):
        tree.move(k, "", idx)
    tree.heading(col, command=lambda: sort_tree(tree, col, not reverse))

def search_bar(parent, on_search):
    frame = tk.Frame(parent, bg=BG)
    frame.pack(fill="x", padx=10, pady=5)
    tk.Label(frame, text="🔍 Cari:", font=LABEL_F, bg=BG).pack(side="left")
    entry = tk.Entry(frame, font=LABEL_F, width=30, relief="solid", bd=1)
    entry.pack(side="left", padx=5)
    entry.bind("<KeyRelease>", lambda e: on_search(entry.get()))
    return entry

def toast(root, message, color=SUCCESS):
    t = tk.Toplevel(root)
    t.overrideredirect(True)
    t.attributes("-topmost", True)
    t.configure(bg=color)
    tk.Label(t, text=f"  {message}  ", bg=color, fg=WHITE,
             font=("Segoe UI", 10, "bold"), pady=10, padx=15).pack()
    # position bottom right
    root.update_idletasks()
    w, h = 350, 45
    x = root.winfo_x() + root.winfo_width() - w - 20
    y = root.winfo_y() + root.winfo_height() - h - 20
    t.geometry(f"{w}x{h}+{x}+{y}")
    t.after(2500, t.destroy)
