import unicodedata
from typing import List, Tuple, Optional

ALPHABET_CZECH = "ABCDEFGHIJKLMNOPQRSTUVXYZ"  # 25 znakov (bez W)
ALPHABET_ENGLISH = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # 25 znakov (bez J)
SPACE_MARKER = "XMEZERAX"
PADDING_CHARS = ["X", "Q", "Z"]


def remove_diacritics(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(c for c in normalized if not unicodedata.combining(c))


def normalize_by_language(text: str, alphabet: str) -> str:
    """Map characters based on alphabet language"""
    if "W" not in alphabet:
        # Czech alphabet (no W) - map W→V
        text = text.replace("W", "V")
    if "J" not in alphabet:
        # English alphabet (no J) - map J→I
        text = text.replace("J", "I")
    return text


def filter_input(text: str, alphabet: str) -> str:
    text = remove_diacritics(text).upper()
    text = normalize_by_language(text, alphabet)
    result = []
    for char in text:
        if char == " ":
            result.append(SPACE_MARKER)
        elif char in alphabet or char.isdigit():
            result.append(char)
    return "".join(result)


def restore_spaces(text: str) -> str:
    return text.replace(SPACE_MARKER, " ")


def format_five(text: str) -> str:
    text = text.replace(" ", "")
    return " ".join(text[i : i + 5] for i in range(0, len(text), 5))


def create_matrix(key: str, alphabet: str) -> List[List[str]]:
    if len(alphabet) != 25:
        raise ValueError(f"Alphabet must have 25 characters, got {len(alphabet)}")

    key_filtered = filter_input(key, alphabet)
    seen = set()
    matrix_chars = []

    for char in key_filtered:
        if char not in seen and char in alphabet:
            seen.add(char)
            matrix_chars.append(char)

    for char in alphabet:
        if char not in seen:
            matrix_chars.append(char)

    return [matrix_chars[i : i + 5] for i in range(0, 25, 5)]


def find_position(matrix: List[List[str]], char: str) -> Optional[Tuple[int, int]]:
    for i, row in enumerate(matrix):
        for j, c in enumerate(row):
            if c == char:
                return (i, j)
    return None


def get_padding_char(avoid_char: str, alphabet: str) -> str:
    for padding in PADDING_CHARS:
        if padding != avoid_char and padding in alphabet:
            return padding
    for char in alphabet:
        if char != avoid_char:
            return char
    return "X"


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

        if text[i].isdigit():
            if i + 1 < len(text) and text[i + 1].isdigit():
                bigrams.append(text[i] + text[i + 1])
                i += 2
            else:
                bigrams.append(text[i] + text[i])
                i += 1
            continue

        if i == len(text) - 1:
            padding = get_padding_char(text[i], alphabet)
            bigrams.append(text[i] + padding)
            i += 1
        else:
            first = text[i]
            second = text[i + 1]

            if first == second and first in alphabet:
                padding = get_padding_char(first, alphabet)
                bigrams.append(first + padding)
                i += 1
            else:
                bigrams.append(first + second)
                i += 2

    return bigrams


def process_bigram(
    bigram: str, matrix: List[List[str]], alphabet: str, decrypt: bool = False
) -> str:
    if any(c.isdigit() for c in bigram):
        return bigram

    a, b = bigram[0], bigram[1]
    pos_a = find_position(matrix, a)
    pos_b = find_position(matrix, b)

    if pos_a is None or pos_b is None:
        return bigram

    r1, c1 = pos_a
    r2, c2 = pos_b
    shift = -1 if decrypt else 1

    if r1 == r2:
        return matrix[r1][(c1 + shift) % 5] + matrix[r2][(c2 + shift) % 5]
    elif c1 == c2:
        return matrix[(r1 + shift) % 5][c1] + matrix[(r2 + shift) % 5][c2]
    else:
        return matrix[r1][c2] + matrix[r2][c1]


def remove_padding(text: str) -> str:
    """Remove filler X between duplicate letters and trailing X/Q/Z"""
    if not text:
        return text

    result = []
    i = 0
    while i < len(text):
        if i > 0 and i < len(text) - 1:
            if text[i] in PADDING_CHARS and i > 0 and i < len(text) - 1:
                prev_char = result[-1] if result else ""
                next_char = text[i + 1]
                if prev_char == next_char and prev_char.isalpha():
                    i += 1
                    continue
        result.append(text[i])
        i += 1

    text = "".join(result)

    while text and text[-1] in PADDING_CHARS:
        text = text[:-1]

    return text


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
    encrypted_bigrams = [
        process_bigram(bg, matrix, alphabet, decrypt=False) for bg in bigrams
    ]
    ciphertext = "".join(encrypted_bigrams)

    return (ciphertext, filtered, bigrams, matrix)


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

    cipher_clean = ciphertext.replace(" ", "").upper()
    if not cipher_clean:
        raise ValueError("Ciphertext contains no valid characters!")

    matrix = create_matrix(key, alphabet)
    bigrams = [cipher_clean[i : i + 2] for i in range(0, len(cipher_clean), 2)]
    decrypted_bigrams = [
        process_bigram(bg, matrix, alphabet, decrypt=True) for bg in bigrams
    ]
    plaintext = "".join(decrypted_bigrams)
    plaintext = restore_spaces(plaintext)
    plaintext = remove_padding(plaintext)

    return (plaintext, matrix, decrypted_bigrams)


def get_filtered_input(plaintext: str, alphabet: str) -> str:
    return filter_input(plaintext, alphabet)
