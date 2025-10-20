import unicodedata
from typing import List, Tuple, Optional

ALPHABET_CZECH = "ABCDEFGHIJKLMNOPQRSTUVXYZ"  # Without W
ALPHABET_ENGLISH = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Without J
SPACE_MARKER = "XMEZERAX"
PADDING_CHARS = ["X", "Q", "Z"]


# Odstrani diakritiku z textu (napr. c -> c, e -> e)
def remove_diacritics(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    # Pre kazdy znak skontroluje, ci je to diakritika (combining) a ak nie, ponecha ho
    return "".join(c for c in normalized if not unicodedata.combining(c))


# Podla pouziteho abecedy upravi specificke znaky (napr. W->V pre cestinu, J->I pre anglictinu)
def normalize_by_language(text: str, alphabet: str) -> str:
    # Ak v abecede nie je W, nahrad ho za V
    if "W" not in alphabet:
        text = text.replace("W", "V")
    # Ak v abecede nie je J, nahrad ho za I
    if "J" not in alphabet:
        text = text.replace("J", "I")
    return text


# Vyfiltruje vstupny text: ponecha len znaky z abecedy a cislice, medzery nahradi specialnym markerom
def filter_input(text: str, alphabet: str) -> str:
    text = remove_diacritics(text).upper()
    text = normalize_by_language(text, alphabet)
    result = []
    for char in text:
        if char == " ":
            result.append(SPACE_MARKER)
        elif char in alphabet or char.isdigit():
            result.append(char)
        # Vsetky ostatne znaky ignoruje
    return "".join(result)


# Obnovi medzery v texte
def restore_spaces(text: str) -> str:
    return text.replace(SPACE_MARKER, " ")


# Rozdeli text do skupin po 5 znakoch
def format_five(text: str) -> str:
    text = text.replace(" ", "")
    # Rozdeli text na podretazce po 5 znakoch
    return " ".join(text[i : i + 5] for i in range(0, len(text), 5))


# Vytvori 5x5 maticu na zaklade kluca a abecedy
def create_matrix(key: str, alphabet: str) -> List[List[str]]:
    if len(alphabet) != 25:
        raise ValueError(f"Alphabet must have 25 characters, got {len(alphabet)}")
    key_filtered = filter_input(key, alphabet)
    seen = set()
    matrix_chars = []
    # Najprv pridava znaky z kluca, ktore este neboli pouzite
    for char in key_filtered:
        if char not in seen and char in alphabet:
            seen.add(char)
            matrix_chars.append(char)
    # Potom doplni zvysne znaky z abecedy
    for char in alphabet:
        if char not in seen:
            matrix_chars.append(char)
    # Rozdeli zoznam na 5x5 maticu
    return [matrix_chars[i : i + 5] for i in range(0, 25, 5)]


# Najde poziciu znaku v matici
def find_position(matrix: List[List[str]], char: str) -> Optional[Tuple[int, int]]:
    for i, row in enumerate(matrix):
        for j, c in enumerate(row):
            if c == char:
                return (i, j)
    return None


# Vyberie padding znak, ktory sa pouzije na doplnenie bigramu
def get_padding_char(avoid_char: str, alphabet: str) -> str:
    # Najprv skusi padding znaky, ktore nie su rovnake ako avoid_char
    for padding in PADDING_CHARS:
        if padding != avoid_char and padding in alphabet:
            return padding
    # Ak padding znaky nie su vhodne, pouzije prvy iny znak z abecedy
    for char in alphabet:
        if char != avoid_char:
            return char
    return "X"


# Rozdeli text na dvojice znakov, spracuje specialne pripady (medzery, cislice, opakovane znaky)
def prepare_bigrams(text: str, alphabet: str) -> List[str]:
    bigrams = []
    i = 0
    while i < len(text):
        if text[i : i + 8] == SPACE_MARKER:
            bigrams.append("XM")
            bigrams.append("EZ")
            bigrams.append("ER")
            bigrams.append("AX")
            i += 8
            continue
        # Ak je znak cislica, spracujeme ju specialne
        if text[i].isdigit():
            if i + 1 < len(text) and text[i + 1].isdigit():
                bigrams.append(text[i] + text[i + 1])
                i += 2
            else:
                bigrams.append(text[i] + text[i])
                i += 1
            continue
        # Ak je posledny znak, doplnime padding
        if i == len(text) - 1:
            padding = get_padding_char(text[i], alphabet)
            bigrams.append(text[i] + padding)
            i += 1
        else:
            first = text[i]
            second = text[i + 1]
            # Ak su dva rovnake znaky za sebou, vlozime padding
            if first == second and first in alphabet:
                padding = get_padding_char(first, alphabet)
                bigrams.append(first + padding)
                i += 1
            else:
                bigrams.append(first + second)
                i += 2
    return bigrams


# Zasifruje alebo desifruje jeden bigram
def process_bigram(
    bigram: str, matrix: List[List[str]], alphabet: str, decrypt: bool = False
) -> str:
    # Ak je v bigrame cislica, vratime ho bez zmeny
    if any(c.isdigit() for c in bigram):
        return bigram
    a, b = bigram[0], bigram[1]
    pos_a = find_position(matrix, a)
    pos_b = find_position(matrix, b)
    # Ak sa znak nenachadza v matici, vratime povodny bigram
    if pos_a is None or pos_b is None:
        return bigram
    r1, c1 = pos_a
    r2, c2 = pos_b
    shift = (
        -1 if decrypt else 1
    )  # Smer posunu podla toho, ci sifrujeme alebo desifrujeme
    # Ak su znaky v rovnakom riadku, posuvame stlpce
    if r1 == r2:
        return matrix[r1][(c1 + shift) % 5] + matrix[r2][(c2 + shift) % 5]
    # Ak su znaky v rovnakom stlpci, posuvame riadky
    elif c1 == c2:
        return matrix[(r1 + shift) % 5][c1] + matrix[(r2 + shift) % 5][c2]
    # Vymena stlpcov
    else:
        return matrix[r1][c2] + matrix[r2][c1]


# Odstrani padding znaky z desifrovaneho textu, ktore vznikli pocas sifrovania
def remove_padding(text: str) -> str:
    if not text:
        return text
    result = []
    i = 0
    while i < len(text):
        # Ak je padding medzi dvoma rovnakymi pismenami, preskocime ho
        if i > 0 and i < len(text) - 1:
            if text[i] in PADDING_CHARS and i > 0 and i < len(text) - 1:
                prev_char = result[-1] if result else ""
                next_char = text[i + 1]
                # Ak padding je medzi dvoma rovnakymi pismenami, ignorujeme ho
                if prev_char == next_char and prev_char.isalpha():
                    i += 1
                    continue
        result.append(text[i])
        i += 1
    text = "".join(result)
    # Odstrani padding na konci
    while text and text[-1] in PADDING_CHARS:
        text = text[:-1]
    return text


# Pripravi bigramy, zasifruje ich a vrati vysledok
def encrypt(
    plaintext: str, key: str, alphabet: str
) -> Tuple[str, str, List[str], List[List[str]]]:
    if not plaintext or not plaintext.strip():
        raise ValueError("Input text cannot be empty!")
    if not key or not key.strip():
        raise ValueError("Keyword cannot be empty!")
    key_filtered = filter_input(key, alphabet)
    if not any(c in alphabet for c in key_filtered):
        raise ValueError("Keyword must contain at least one valid letter!")
    filtered = filter_input(plaintext, alphabet)
    if not filtered:
        raise ValueError("Input text must contain at least one valid character!")
    matrix = create_matrix(key, alphabet)
    bigrams = prepare_bigrams(filtered, alphabet)
    # Zasifrujeme kazdy bigram samostatne
    encrypted_bigrams = [
        process_bigram(bg, matrix, alphabet, decrypt=False) for bg in bigrams
    ]
    ciphertext = "".join(encrypted_bigrams)
    return (ciphertext, filtered, bigrams, matrix)


# Rozdeli text na bigramy, desifruje ich a odstrani padding
def decrypt(
    ciphertext: str, key: str, alphabet: str
) -> Tuple[str, List[List[str]], List[str]]:
    if not ciphertext or not ciphertext.strip():
        raise ValueError("Ciphertext cannot be empty!")
    if not key or not key.strip():
        raise ValueError("Keyword cannot be empty!")
    key_filtered = filter_input(key, alphabet)
    if not any(c in alphabet for c in key_filtered):
        raise ValueError("Keyword must contain at least one valid letter!")
    # Odstrani medzery a zmeni na velke pismena
    cipher_clean = ciphertext.replace(" ", "").upper()
    if not cipher_clean:
        raise ValueError("Ciphertext contains no valid characters!")
    matrix = create_matrix(key, alphabet)
    # Rozdeli text na bigramy po dvoch znakoch
    bigrams = [cipher_clean[i : i + 2] for i in range(0, len(cipher_clean), 2)]
    decrypted_bigrams = [
        process_bigram(bg, matrix, alphabet, decrypt=True) for bg in bigrams
    ]
    plaintext = "".join(decrypted_bigrams)
    plaintext = restore_spaces(plaintext)
    plaintext = remove_padding(plaintext)
    return (plaintext, matrix, decrypted_bigrams)
