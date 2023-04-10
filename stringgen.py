import random
from chunk_formats import formats, fonts
import numpy as np


_start = 0x0c00
_all_chars = set(list(range(103)))

_consonants = [*range(21, 41), *range(42, 49), *range(50, 52), *range(53, 58)]

_vowels = [*range(5, 13), *range(14, 17), *range(18, 21), *(96,)]

_vowel_diacs = [1, 2, 3, *range(62, 69), *range(70, 73), *range(74, 78)]

_depr = [0, 4, 12, 13, 17, 41, 49, 52, 58, 59, 60, 61, 69, 73, 78, 79, 80, 81, 82, 83, 84, 87, 88, 89, 90, 91, 92, 93,
         94, 95, 97, 100, 101, 102, 103, 104, 105, 106, 107]

_pruned = _all_chars.difference(_depr)

_puncs = [c for c in "\"#$%&'()*+-/<=>@[\\]^`{|}~-_~"]
_breaks = [c for c in ",:;"]

_eng_chars = "abcdefghijklmnopqrstuvwxyz"
_eng_chars = list(_eng_chars + _eng_chars.upper())

_digs = list("0123456789")


def _prob(p):
    return random.random() <= p


def _p_dist(u, s, l):
    u, s = u / l, s / l
    ps = np.linspace(0, 1, l)
    ps = 1 / (s * np.sqrt(2 * np.pi)) * np.exp(-(ps - u) ** 2 / (2 * s ** 2))
    ps = ps / np.sum(ps)
    return ps


def letter(first=False):
    if _prob(0.05):
        return "".join(random.choice(_puncs))

    if first:
        if _prob(0.5):
            return "".join(chr(_start + random.choice(_vowels)))

    ltr = [chr(_start + random.choice(_consonants))]

    cons = None
    if _prob(0.2):
        ltr.append(chr(_start + 77))

        cons = random.choice(_consonants)
        ltr.append(chr(_start + cons))

        if _prob(0.01):
            ltr.append(chr(_start + 77))

            cons2 = random.choice(_consonants)
            ltr.append(chr(_start + cons2))

    if _prob(0.9):
        if cons is not None and cons == 57:
            ltr.append(chr(_start + random.choice(_vowel_diacs + [85])))
        else:
            ltr.append(chr(_start + random.choice(_vowel_diacs)))

    return "".join(ltr)


_w_L = 50
_w_ps = _p_dist(4, 1, _w_L)


def word(ln=None):
    if _prob(0.02):
        return "".join([random.choice(_digs) for _ in range(random.randint(1, 10))]) \
            if _prob(0.2) \
            else "".join(np.random.choice(_eng_chars, size=random.randint(1, 10)))

    w = [letter(first=True)]
    ln = np.random.choice(range(1, _w_L + 1), p=_w_ps) if ln is None else ln
    for _ in range(ln):
        w.append(letter())

    w = "".join(w)
    for c, replacement in zip(('&', '<', '>'), ("&amp;", "&lt;", "&gt;")):
        w = w.replace(c, replacement)
    return "".join(w)


_s_L = 100
_s_ps = _p_dist(15.5, 5.5, _s_L)


def sentence(ln=None):
    s = []
    ln = np.random.choice(range(1, _s_L + 1), p=_s_ps) if ln is None else ln
    for _ in range(ln - 1):
        s.append(word())
        if _prob(0.3):
            s[-1] += (random.choice(_breaks))

    s.append(word())
    s[-1] += (str(np.random.choice(list(".?!"), p=[0.5, 0.25, 0.25])) * np.random.choice(range(1, 4), p=[0.4, 0.4, 0.2]))
    return s


_p_L = 15
_p_ps = _p_dist(6, 5, _p_L)


def paragraph(ln=None):
    ln = np.random.choice(range(1, _p_L + 1), p=_p_ps) if ln is None else ln
    p = [sentence() for _ in range(ln)]

    return p


def word_xml(text, bold=False, italics=False, underline=False, strikethrough=False):
    w = formats['word']['body']
    for choice, replacement in zip((bold, italics, underline, strikethrough), formats['word']['params'].keys()):
        if choice:
            w = w.replace(replacement, formats['word']['params'][replacement])
        else:
            w = w.replace(replacement, "")
    w = w.replace("text_here", text)

    return w


def paragraph_xml(p, style="Normal",  f_size=30, f_name="Gautami"):
    body = ""

    run = ""
    for s in p:
        for w in s:
            b, i, u, s = _prob(0.03), _prob(0.03), _prob(0.01), _prob(0.01)
            if not (b or i or u or s):
                run += w + " "
            else:
                if run:
                    body += word_xml(run + " ", False, False, False, False)
                    run = ""
                body += word_xml(w + " ", bold=b, italics=i, underline=u, strikethrough=s)

    body = formats['paragraph']['body'].replace("word_here", body)

    for kwarg, replacement in zip((style, f_name, f_size), ('paragraph_style', 'font_name', 'font_size')):
        body = body.replace(replacement, str(kwarg))

    return body


def header_footer_xml(horf="h", w1=None, w2=None, w3=None):
    horf = "header" if horf == "h" else "footer"
    body = ""
    for w in w1, w2, w3:
        if w is not None:
            b, i, u, s = _prob(0.03), _prob(0.03), _prob(0.01), _prob(0.01)
            body += word_xml(w, bold=b, italics=i, underline=u, strikethrough=s)
        body += formats[horf]['tab']

    body = formats[horf]['body'].replace(f"{horf}_here", body)

    for key in formats[horf]['params'].keys():
        body = body.replace(key, str(random.choice(formats[horf]['params'][key])))

    return body


def docgen():
    body = ""
    run = []

    for _ in range(random.randint(1, 4)):
        if _prob(0.2):
            p = [[word() + " " for _ in range(random.randint(1, 10))]]
            body += paragraph_xml(
                p,
                style="Heading",
                f_size=random.randint(30, 45),
                f_name=random.choice(fonts))
            run.append(p)

        p = paragraph()
        body += paragraph_xml(p, style="Normal", f_size=random.randint(30, 40), f_name=random.choice(fonts))

        run.append(p)

        if _prob(0.2):
            body += paragraph_xml([[("*" + random.randint(1, 5) * " ") * random.randint(2, 7)]], style="Heading", f_size=random.randint(30, 55), f_name=random.choice(fonts))

        body += paragraph_xml([["\n" * random.randint(1, 3)]], f_name=random.choice(fonts))

        for key in formats['paragraph']['params'].keys():
            body = body.replace(key, str(random.choice(formats['paragraph']['params'][key])))

    body = formats['document']['body'].replace("paragraphs_here", body)
    for key in formats['document']['params'].keys():
        body = body.replace(key, str(random.choice(formats['document']['params'][key])))

    return body, run


def header_footer_gen(horf):
    ws = [word() if _prob(0.5) else str(random.randint(1, 1000)) if _prob(0.33) else None for _ in range(3)]

    if horf == "h":
        return header_footer_xml("h", *ws)
    else:
        return header_footer_xml("f", *ws)


