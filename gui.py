"""
Playfair Cipher GUI using Tkinter
"""

import tkinter as tk
from tkinter import messagebox
from playfaircypher import (
    encrypt,
    decrypt,
    format_five,
    ALPHABET_CZECH,
    ALPHABET_ENGLISH,
)

DARK_BG = "#2b2b2b"
LIGHT_TXT = "#9e74d4"
DARK_ENTRY = "#3c3c3c"
BUTTON_BG = "#4a4a4a"
FONT = ("Arial", 11)
LABEL_FONT = ("Arial", 11, "bold")
BUTTON_FONT = ("Arial", 12, "bold")


class PlayfairCipherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("< Playfair Cipher >")
        self.root.geometry("550x500")
        self.root.resizable(False, False)
        self.root.configure(bg=DARK_BG)
        self.current_alphabet = ALPHABET_CZECH
        self.alphabet_var = tk.StringVar(value="CZECH")
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg=DARK_BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.setup_left_panel(main_frame)
        self.setup_right_panel(main_frame)

    def setup_left_panel(self, parent):
        left_frame = tk.Frame(parent, bg=DARK_BG)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 10))

        tk.Label(
            left_frame, text="ENTER TEXT", bg=DARK_BG, fg=LIGHT_TXT, font=LABEL_FONT
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
        )
        self.input_text.pack(fill=tk.BOTH, expand=False, pady=(0, 10))

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
        )
        self.filtered_encrypt_text.pack(fill=tk.BOTH, expand=False, pady=(0, 10))

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
        )
        self.filtered_decrypt_text.pack(fill=tk.BOTH, expand=False, pady=(0, 10))

        tk.Label(
            left_frame,
            text="Encrypted / Decrypted Text",
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
        )
        self.output_text.pack(fill=tk.BOTH, expand=False, pady=(0, 10))

        self.setup_buttons(left_frame)

    def setup_buttons(self, parent):
        button_frame = tk.Frame(parent, bg=DARK_BG)
        button_frame.pack(fill=tk.X, pady=(10, 10))

        self.encrypt_btn = tk.Button(
            button_frame,
            text="ENCRYPT",
            bg=BUTTON_BG,
            fg=LIGHT_TXT,
            font=BUTTON_FONT,
            command=self.do_encrypt,
            cursor="hand2",
            activebackground="#5a5a5a",
            activeforeground=LIGHT_TXT,
        )
        self.encrypt_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.decrypt_btn = tk.Button(
            button_frame,
            text="DECRYPT",
            bg=BUTTON_BG,
            fg=LIGHT_TXT,
            font=BUTTON_FONT,
            command=self.do_decrypt,
            cursor="hand2",
            activebackground="#5a5a5a",
            activeforeground=LIGHT_TXT,
        )
        self.decrypt_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

    def setup_right_panel(self, parent):
        right_frame = tk.Frame(parent, bg=DARK_BG, width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_frame.pack_propagate(False)

        tk.Label(
            right_frame, text="Alphabet", bg=DARK_BG, fg=LIGHT_TXT, font=LABEL_FONT
        ).pack(anchor=tk.W, pady=(0, 10))

        self.setup_alphabet_selection(right_frame)
        self.setup_keyword_entry(right_frame)
        self.setup_matrix(right_frame)

    def setup_alphabet_selection(self, parent):
        radio_frame = tk.Frame(parent, bg=DARK_BG)
        radio_frame.pack(anchor=tk.W, pady=(0, 15))

        tk.Radiobutton(
            radio_frame,
            text="CZECH",
            variable=self.alphabet_var,
            value="CZECH",
            bg=DARK_BG,
            fg=LIGHT_TXT,
            selectcolor=BUTTON_BG,
            font=("Arial", 10),
            command=self.change_alphabet,
            activebackground=DARK_BG,
            activeforeground=LIGHT_TXT,
        ).pack(side=tk.LEFT, padx=(0, 30))
        tk.Radiobutton(
            radio_frame,
            text="ENGLISH",
            variable=self.alphabet_var,
            value="ENGLISH",
            bg=DARK_BG,
            fg=LIGHT_TXT,
            selectcolor=BUTTON_BG,
            font=("Arial", 10),
            command=self.change_alphabet,
            activebackground=DARK_BG,
            activeforeground=LIGHT_TXT,
        ).pack(side=tk.LEFT)

    def setup_keyword_entry(self, parent):
        tk.Label(
            parent, text="Keyword", bg=DARK_BG, fg=LIGHT_TXT, font=LABEL_FONT
        ).pack(anchor=tk.W, pady=(0, 5))
        self.keyword_entry = tk.Entry(
            parent,
            bg=DARK_ENTRY,
            fg=LIGHT_TXT,
            insertbackground=LIGHT_TXT,
            font=FONT,
            width=21,
        )
        self.keyword_entry.pack(anchor=tk.W, pady=(0, 15))

    def setup_matrix(self, parent):
        tk.Label(parent, text="Matrix", bg=DARK_BG, fg=LIGHT_TXT, font=LABEL_FONT).pack(
            anchor=tk.W, pady=(0, 5)
        )
        matrix_frame = tk.Frame(parent, bg=DARK_BG)
        matrix_frame.pack(anchor=tk.W, pady=(0, 15))

        self.matrix_labels = []
        for i in range(5):
            row = []
            for j in range(5):
                label = tk.Label(
                    matrix_frame,
                    text="?",
                    bg=BUTTON_BG,
                    fg=LIGHT_TXT,
                    font=("Arial", 14, "bold"),
                    width=3,
                    height=1,
                    relief=tk.RIDGE,
                    borderwidth=2,
                )
                label.grid(row=i, column=j, padx=1, pady=2)
                row.append(label)
            self.matrix_labels.append(row)

    def change_alphabet(self):
        choice = self.alphabet_var.get()
        if choice == "CZECH":
            self.current_alphabet = ALPHABET_CZECH
        elif choice == "ENGLISH":
            self.current_alphabet = ALPHABET_ENGLISH

    def update_matrix(self, matrix):
        for i in range(5):
            for j in range(5):
                char = matrix[i][j] if i < len(matrix) and j < len(matrix[i]) else "?"
                self.matrix_labels[i][j].config(text=char)

    def set_text(self, widget, text):
        widget.config(state=tk.NORMAL)
        widget.delete(1.0, tk.END)
        widget.insert(1.0, text)
        widget.config(state=tk.DISABLED)

    def do_encrypt(self):
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
            self.update_matrix(matrix)
            self.set_text(self.filtered_decrypt_text, "")
        except Exception as e:
            messagebox.showerror("Encryption Error", str(e))

    def do_decrypt(self):
        try:
            ciphertext = self.input_text.get(1.0, tk.END).strip()
            key = self.keyword_entry.get().strip()

            if not key:
                messagebox.showwarning("Error", "Please enter a keyword!")
                return

            plaintext, matrix = decrypt(ciphertext, key, self.current_alphabet)

            self.set_text(self.filtered_decrypt_text, plaintext)
            self.set_text(self.output_text, plaintext)
            self.update_matrix(matrix)
            self.set_text(self.filtered_encrypt_text, "")
        except Exception as e:
            messagebox.showerror("Decryption Error", str(e))
