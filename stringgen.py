import random
from chunk_formats import formats, fonts
import numpy as np


_start = 0x0c00
_all_chars = set(list(range(103)))

_consonants = [*range(21, 41), *range(42, 49), *range(50, 52), *range(53, 58)]
_consonants = [_start + c for c in _consonants]

_vowels = [*range(5, 13), *range(14, 17), *range(18, 21), *(96,)]
_vowels = [_start + c for c in _vowels]

_vowel_diacs = [1, 2, 3, *range(62, 69), *range(70, 73), *range(74, 77)]
_vowel_diacs = [_start + c for c in _vowel_diacs]

# _depr = [0, 4, 12, 13, 17, 41, 49, 52, 58, 59, 60, 61, 69, 73, 78, 79, 80, 81, 82, 83, 84, 87, 88, 89, 90, 91, 92, 93,
#          94, 95, 97, 100, 101, 102, 103, 104, 105, 106, 107]

# _pruned = _all_chars.difference(_depr)

_puncs = list("\"#$%&'()*+-/<=>@[\\]^`{|}~-_~")
_breaks = list(",:;")

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


def letter(first=False, last=False):
    if _prob(0.05):
        return random.choice(_puncs)

    if first:
        if _prob(0.5):
            return str(chr(random.choice(_vowels)))

    ltr = [chr(random.choice(_consonants))]

    if _prob(0.2):
        cons_diacs = []

        cons = random.choice(_consonants)
        cons_diacs.append(chr(cons))

        if _prob(0.2):
            cons2 = random.choice(_consonants)
            cons_diacs.append(chr(cons2))

        cons_diacs.sort()
        for cd in cons_diacs:
            ltr.extend([chr(_start + 77), cd])

    if last and _prob(0.1):
        ltr.append(chr(_start + 77))

    elif _prob(0.9):
        ltr.append(chr(random.choice(_vowel_diacs)))

    return "".join(ltr)


_w_L = 50
_w_ps = _p_dist(4, 1, _w_L)


def word(ln=None):
    if _prob(0.02):
        return "".join([random.choice(_digs) for _ in range(random.randint(1, 10))]) \
            if _prob(0.2) \
            else "".join(np.random.choice(_eng_chars, size=random.randint(1, 10)))

    ln = np.random.choice(range(1, _w_L + 1), p=_w_ps) if ln is None else ln
    w = [letter(first=True)] + [letter() for _ in range(ln-2)] + [letter(last=True)]

    return "".join(w)


_s_L = 100
_s_ps = _p_dist(15.5, 5.5, _s_L)


def sentence(wn=None):
    s = []
    wn = np.random.choice(range(1, _s_L + 1), p=_s_ps) if wn is None else wn
    for _ in range(wn - 1):
        s.append(word())
        if _prob(0.2):
            s[-1] += (random.choice(_breaks))
    s.append(word() + str(np.random.choice(list(".?!"), p=[0.5, 0.25, 0.25])) * np.random.choice(range(1, 4), p=[0.4, 0.4, 0.2]))
    return s


_p_L = 15
_p_ps = _p_dist(6, 5, _p_L)


def paragraph(sn=None):
    sn = np.random.choice(range(1, _p_L + 1), p=_p_ps) if sn is None else sn
    p = [sentence() for _ in range(sn)]

    return p


def word_xml(text, bold=False, italics=False, underline=False, strikethrough=False):
    for c, replacement in zip(('&', '<', '>'), ("&amp;", "&lt;", "&gt;")):
        text = text.replace(c, replacement)

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
            b, i, u, s = _prob(0.005), _prob(0.03), _prob(0.001), _prob(0.0005)
            if not (b or i or u or s):
                run += w + " "
            else:
                if run:
                    body += word_xml(run + " ", False, False, False, False)
                    run = ""
                body += word_xml(w + " ", bold=b, italics=i, underline=u, strikethrough=s)
    if run:
        body += word_xml(run + " ", False, False, False, False)

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


def header_footer_gen(horf):
    ws = [word() if _prob(0.5) else str(random.randint(1, 1000)) if _prob(0.33) else None for _ in range(3)]

    if horf == "h":
        return header_footer_xml("h", *ws)
    else:
        return header_footer_xml("f", *ws)


n_newlines = _p_dist(1, 3, 15)
def docgen():
    body = ""
    run = []

    for _ in range(random.randint(1, 4)):
        if _prob(0.2):
            p = [sentence(random.randint(1, 10))]
            body += paragraph_xml([]) * np.random.choice(range(15), p=n_newlines)
            body += paragraph_xml(p, style="Heading", f_size=random.randint(35, 45), f_name=random.choice(fonts))
            run.append(p)

        p = paragraph()
        body += paragraph_xml([]) * random.randint(0, 3)
        body += paragraph_xml(p, style="Normal", f_size=random.randint(30, 40), f_name=random.choice(fonts))
        run.append(p)

        for key in formats['paragraph']['params'].keys():
            body = body.replace(key, str(random.choice(formats['paragraph']['params'][key])))

    body = formats['document']['body'].replace("paragraphs_here", body)
    for key in formats['document']['params'].keys():
        body = body.replace(key, str(random.choice(formats['document']['params'][key])))

    return body, run


