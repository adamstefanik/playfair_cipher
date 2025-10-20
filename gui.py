import tkinter as tk
from tkinter import messagebox, ttk

# Oprava DPI scalingu na Windows pre ostrejsie zobrazenie
try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)  # Windows 8.1+
except:
    try:
        from ctypes import windll

        windll.user32.SetProcessDPIAware()  # Windows Vista+
    except:
        pass

from playfaircypher import (
    encrypt,
    decrypt,
    format_five,
    create_matrix,
    find_position,
    ALPHABET_CZECH,
    ALPHABET_ENGLISH,
)

# Farby a fonty pre tmavu temu
DARK_BG = "#222026"
LIGHT_TXT = "#08AC2C"
DARK_ENTRY = "#222026"
BUTTON_BG = "#2b2b2b"
HIGHLIGHT_BG = "#08AC2C"
HIGHLIGHT_FG = "#2b2b2b"
FONT = ("Consolas", 11)
LABEL_FONT = ("Consolas", 12, "bold")
BUTTON_FONT = ("Consolas", 12, "bold")


class PlayfairCipherGUI:
    def __init__(self, root):
        # Inicializacia hlavneho okna a nastavenie temy
        self.root = root
        self.root.title("Playfair Cipher")
        self.root.geometry("650x550")
        self.root.resizable(False, False)
        self.root.configure(bg=DARK_BG)
        self.current_alphabet = ALPHABET_CZECH
        self.alphabet_var = tk.StringVar(value="CZECH")
        self.setup_ui()

    def setup_ui(self):
        # Vytvorenie hlavneho framu a rozdelenie na lavy a pravy panel
        main_frame = tk.Frame(self.root, bg=DARK_BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.setup_left_panel(main_frame)
        self.setup_right_panel(main_frame)

    def setup_left_panel(self, parent):
        # Lavy panel: vstup, vystup, buttony
        left_frame = tk.Frame(parent, bg=DARK_BG)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 10))

        tk.Label(
            left_frame, text="INPUT", bg=DARK_BG, fg=LIGHT_TXT, font=LABEL_FONT
        ).pack(anchor=tk.W, pady=(0, 5))
        self.input_text = tk.Text(
            left_frame,
            height=5,
            width=30,
            bg=DARK_ENTRY,
            fg=LIGHT_TXT,
            insertbackground=LIGHT_TXT,
            font=FONT,
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=LIGHT_TXT,
            highlightcolor=LIGHT_TXT,
        )
        self.input_text.pack(fill=tk.BOTH, expand=False, padx=(3, 0), pady=(0, 10))

        tk.Label(
            left_frame,
            text="Filtered Encryption Text",
            bg=DARK_BG,
            fg=LIGHT_TXT,
            font=LABEL_FONT,
        ).pack(anchor=tk.W, pady=(0, 5))
        self.filtered_encrypt_text = tk.Text(
            left_frame,
            height=3,
            width=30,
            bg=DARK_ENTRY,
            fg=LIGHT_TXT,
            state=tk.DISABLED,
            font=FONT,
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=LIGHT_TXT,
            highlightcolor=LIGHT_TXT,
        )
        self.filtered_encrypt_text.pack(
            fill=tk.BOTH, expand=False, padx=(3, 0), pady=(0, 10)
        )

        tk.Label(
            left_frame,
            text="Filtered Decryption Text",
            bg=DARK_BG,
            fg=LIGHT_TXT,
            font=LABEL_FONT,
        ).pack(anchor=tk.W, pady=(0, 5))
        self.filtered_decrypt_text = tk.Text(
            left_frame,
            height=3,
            width=30,
            bg=DARK_ENTRY,
            fg=LIGHT_TXT,
            state=tk.DISABLED,
            font=FONT,
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=LIGHT_TXT,
            highlightcolor=LIGHT_TXT,
        )
        self.filtered_decrypt_text.pack(
            fill=tk.BOTH, expand=False, padx=(3, 0), pady=(0, 10)
        )

        tk.Label(
            left_frame,
            text="OUTPUT",
            bg=DARK_BG,
            fg=LIGHT_TXT,
            font=LABEL_FONT,
        ).pack(anchor=tk.W, pady=(0, 5))
        self.output_text = tk.Text(
            left_frame,
            height=4,
            width=30,
            bg=DARK_ENTRY,
            fg=LIGHT_TXT,
            state=tk.DISABLED,
            font=FONT,
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=LIGHT_TXT,
            highlightcolor=LIGHT_TXT,
        )
        self.output_text.pack(fill=tk.BOTH, expand=False, padx=(3, 0), pady=(0, 10))

        self.setup_buttons(left_frame)

    def setup_buttons(self, parent):
        # Button styling
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Custom.TButton",
            background=BUTTON_BG,
            foreground=LIGHT_TXT,
            font=BUTTON_FONT,
            borderwidth=1,
            focuscolor="none",
            relief="flat",
            highlightthickness=1,
            highlightbackground=LIGHT_TXT,
            highlightcolor=LIGHT_TXT,
        )
        style.map(
            "Custom.TButton",
            background=[("active", "#5a5a5a"), ("pressed", "#5a5a5a")],
            foreground=[("active", LIGHT_TXT)],
            relief=[("pressed", "sunken")],
        )

        button_frame = tk.Frame(parent, bg=DARK_BG)
        button_frame.pack(fill=tk.X, pady=(10, 10))

        # Tlacidlo na sifrovanie
        self.encrypt_btn = ttk.Button(
            button_frame,
            text="ENCRYPT",
            style="Custom.TButton",
            command=self.do_encrypt,
            cursor="hand2",
        )
        self.encrypt_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))

        # Tlacidlo na desifrovanie
        self.decrypt_btn = ttk.Button(
            button_frame,
            text="DECRYPT",
            style="Custom.TButton",
            command=self.do_decrypt,
            cursor="hand2",
        )
        self.decrypt_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

    def setup_right_panel(self, parent):
        # Pravy panel: vyber abecedy, zobrazenie abecedy, kluc, matica
        right_frame = tk.Frame(parent, bg=DARK_BG, width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 10))
        right_frame.pack_propagate(False)

        tk.Label(
            right_frame, text="Alphabet", bg=DARK_BG, fg=LIGHT_TXT, font=LABEL_FONT
        ).pack(
            anchor=tk.W,
        )

        self.setup_alphabet_selection(right_frame)

        # Zobrazenie aktualnej abecedy
        self.alphabet_display = tk.Entry(
            right_frame,
            bg=DARK_ENTRY,
            fg=LIGHT_TXT,
            font=FONT,
            width=27,
            state="readonly",
            readonlybackground=DARK_ENTRY,
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=LIGHT_TXT,
            highlightcolor=LIGHT_TXT,
        )
        self.alphabet_display.pack(anchor=tk.W, padx=(3, 0), pady=(0, 5))

        # Zobrazenie mapovania znakov
        self.mapping_display = tk.Label(
            right_frame,
            text="",
            bg=DARK_BG,
            fg=LIGHT_TXT,
            font=("Consolas", 11, "bold"),
        )
        self.mapping_display.pack(anchor=tk.W, pady=(0, 15))

        self.setup_keyword_entry(right_frame)
        self.setup_matrix(right_frame)

        self.update_alphabet_info()

    def setup_alphabet_selection(self, parent):
        # Vyber medzi ceskou a anglickou abecedou
        radio_frame = tk.Frame(parent, bg=DARK_BG)
        radio_frame.pack(anchor=tk.W, pady=(0, 5))

        tk.Radiobutton(
            radio_frame,
            text="CZECH",
            variable=self.alphabet_var,
            value="CZECH",
            bg=DARK_BG,
            fg=LIGHT_TXT,
            selectcolor=BUTTON_BG,
            font=("Consolas", 10),
            command=self.change_alphabet,
            activebackground=DARK_BG,
            activeforeground=LIGHT_TXT,
            padx=-5,
        ).pack(side=tk.LEFT, padx=(0, 25))
        tk.Radiobutton(
            radio_frame,
            text="ENGLISH",
            variable=self.alphabet_var,
            value="ENGLISH",
            bg=DARK_BG,
            fg=LIGHT_TXT,
            selectcolor=BUTTON_BG,
            font=("Consolas", 10),
            command=self.change_alphabet,
            activebackground=DARK_BG,
            activeforeground=LIGHT_TXT,
        ).pack(side=tk.LEFT, padx=(25, 0))

    def setup_keyword_entry(self, parent):
        # Policko pre zadanie kluca
        tk.Label(
            parent, text="Keyword", bg=DARK_BG, fg=LIGHT_TXT, font=LABEL_FONT
        ).pack(anchor=tk.W, pady=(15, 5))
        self.keyword_entry = tk.Entry(
            parent,
            bg=DARK_ENTRY,
            fg=LIGHT_TXT,
            insertbackground=LIGHT_TXT,
            font=FONT,
            width=27,
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=LIGHT_TXT,
            highlightcolor=LIGHT_TXT,
        )
        self.keyword_entry.pack(anchor=tk.W, padx=(3, 0), pady=(0, 15))

        # Realtime matrix update
        self.keyword_entry.bind("<KeyRelease>", self.update_matrix_realtime)

    def setup_matrix(self, parent):
        # Vytvorenie 5x5 matice
        tk.Label(parent, text="Matrix", bg=DARK_BG, fg=LIGHT_TXT, font=LABEL_FONT).pack(
            anchor=tk.W, pady=(0, 5)
        )
        matrix_frame = tk.Frame(parent, bg=DARK_BG)
        matrix_frame.pack(pady=(0, 15))

        self.matrix_labels = []
        for i in range(5):
            row = []
            for j in range(5):
                label = tk.Label(
                    matrix_frame,
                    text="?",
                    bg=BUTTON_BG,
                    fg=LIGHT_TXT,
                    font=("Consolas", 14, "bold"),
                    width=3,
                    height=1,
                    relief=tk.FLAT,
                )
                label.grid(row=i, column=j, padx=2, pady=2)
                row.append(label)
            self.matrix_labels.append(row)

    def change_alphabet(self):
        choice = self.alphabet_var.get()
        if choice == "CZECH":
            self.current_alphabet = ALPHABET_CZECH
        elif choice == "ENGLISH":
            self.current_alphabet = ALPHABET_ENGLISH

        self.update_alphabet_info()

    def update_alphabet_info(self):

        choice = self.alphabet_var.get()

        if choice == "CZECH":
            alphabet_text = "ABCDEFGHIJKLMNOPQRSTUVXYZ"
            mapping_text = "W → V"
        elif choice == "ENGLISH":
            alphabet_text = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
            mapping_text = "J → I"
        else:
            alphabet_text = ""
            mapping_text = ""

        # Odomkne entry widget, vymaze stary text a vlozi novu abecedu
        self.alphabet_display.config(state="normal")
        self.alphabet_display.delete(0, tk.END)
        self.alphabet_display.insert(0, alphabet_text)
        self.alphabet_display.config(state="readonly")

        # Nastavi popis mapovania cz/en
        self.mapping_display.config(text=mapping_text)

    def update_matrix_realtime(self, event=None):
        # Aktualizuje maticu v realnom case pri pisani kluca
        try:
            key = self.keyword_entry.get().strip()
            if not key:
                return

            matrix = create_matrix(key, self.current_alphabet)
            self.update_matrix(matrix)
        except Exception as e:
            pass

    def update_matrix(self, matrix, highlight_positions=None):
        # Aktualizuje zobrazenie matice a popripade zvyrazni pouzite pismena
        for i in range(5):
            for j in range(5):
                char = matrix[i][j] if i < len(matrix) and j < len(matrix[i]) else "?"

                # Ak je pozicia v highlight_positions, zvyrazni ju
                if highlight_positions and (i, j) in highlight_positions:
                    self.matrix_labels[i][j].config(
                        text=char, bg=HIGHLIGHT_BG, fg=HIGHLIGHT_FG
                    )
                else:
                    self.matrix_labels[i][j].config(
                        text=char, bg=BUTTON_BG, fg=LIGHT_TXT
                    )

    def get_used_positions(self, bigrams, matrix):
        # Vrati vsetky pozicie v matici, ktore sa pouzili v bigramoch
        positions = set()
        for bigram in bigrams:
            if len(bigram) == 2:
                for char in bigram:
                    if char.isalpha():  # Preskoc cislice
                        pos = find_position(matrix, char)
                        if pos:
                            positions.add(pos)
        return positions

    def set_text(self, widget, text):
        # Bezpecne nastavi text do widgetu
        widget.config(state=tk.NORMAL)
        widget.delete(1.0, tk.END)
        widget.insert(1.0, text)
        widget.config(state=tk.DISABLED)

    def do_encrypt(self):
        # Ziska vstup, kluc, zasifruje, zobrazi vysledky a zvyrazni pouzite pismena
        try:
            plaintext = self.input_text.get(1.0, tk.END).strip()
            key = self.keyword_entry.get().strip()

            if not key:
                messagebox.showwarning("Error", "Please enter a keyword!")
                return

            ciphertext, filtered, bigrams, matrix = encrypt(
                plaintext, key, self.current_alphabet
            )

            self.set_text(self.filtered_encrypt_text, " ".join(bigrams))
            self.set_text(self.output_text, format_five(ciphertext))

            # Zvyrazni pouzite pismena v matici
            used_positions = self.get_used_positions(bigrams, matrix)
            self.update_matrix(matrix, used_positions)

            self.set_text(self.filtered_decrypt_text, "")
        except Exception as e:
            messagebox.showerror("Encryption Error", str(e))

    def do_decrypt(self):
        # Ziska vstup, kluc, desifruje, zobrazi vysledky a zvyrazni pouzite pismena
        try:
            ciphertext = self.input_text.get(1.0, tk.END).strip()
            key = self.keyword_entry.get().strip()

            if not key:
                messagebox.showwarning("Error", "Please enter a keyword!")
                return

            plaintext, matrix, decrypted_bigrams = decrypt(
                ciphertext, key, self.current_alphabet
            )

            self.set_text(self.filtered_decrypt_text, " ".join(decrypted_bigrams))

            self.set_text(self.output_text, plaintext)

            # Zvyrazni pouzite pismena v matici
            used_positions = self.get_used_positions(decrypted_bigrams, matrix)
            self.update_matrix(matrix, used_positions)

            self.set_text(self.filtered_encrypt_text, "")
        except Exception as e:
            messagebox.showerror("Decryption Error", str(e))
