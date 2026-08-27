#!/usr/bin/env python3
"""Generate Polish HTML copies of the simplified KTANE manual."""

import re
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PL_DIR = ROOT / "public" / "pl"
DOC_TITLE = "Keep Talking and Nobody Explodes v.1 Uproszczony"
META_DESC = "Podręcznik rozbrajania bomb do gry wideo Keep Talking and Nobody Explodes"


def head(title_suffix: str, section: str = "", page_class: str = "") -> str:
    title = f"KTANE v1 Uproszczony - {title_suffix}"
    extra_page_class = f" {page_class}" if page_class else ""
    return f"""<!DOCTYPE html>
<html class='no-js' lang='pl'><head><meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>
\t<meta charset='utf-8'>
\t<link rel='icon' href='../img/favicon.ico' type='image/png'>
\t<meta http-equiv='X-UA-Compatible' content='IE=edge'>
\t<meta name='description' content='{META_DESC}'>
\t<title>{title}</title>
\t<meta name='viewport' content='initial-scale=1'>
\t<link href='https://fonts.googleapis.com/css?family=Special+Elite' rel='stylesheet' type='text/css'>
\t<link rel='stylesheet' type='text/css' href='../css/normalize.css'>
\t<link rel='stylesheet' type='text/css' href='../css/main.css'>
</head>
<body>
<div class='section'>
\t<div class='page{extra_page_class}'>
\t\t<div class='page-header'>
\t\t\t<span class='page-header-doc-title'>{DOC_TITLE}</span>
\t\t\t<span class='page-header-section-title'>{section or title_suffix}</span>
\t\t</div>
\t\t<div class='page-content'>"""


def foot() -> str:
    return """\t\t</div>
\t</div>
</div>
</body></html>
"""


def page_header_only(section: str) -> str:
    return f"""\t<div class='page page-bg-01'>
\t\t<div class='page-header'>
\t\t\t<span class='page-header-doc-title'>{DOC_TITLE}</span>
\t\t\t<span class='page-header-section-title'>{section}</span>
\t\t</div>
\t\t<div class='page-content'>"""


def fetch_wof_tables() -> tuple[str, str]:
    html = urllib.request.urlopen(
        "https://www.bombmanual.com/pl/web/index.html", timeout=30
    ).read().decode("utf-8")
    start = html.find('class="whos-on-first-step1-table"')
    if start == -1:
        raise RuntimeError("WOF step 1 table not found")
    start = html.rfind("<table", 0, start)
    end = html.find("</table>", start) + len("</table>")
    step1 = html[start:end]
    start2 = html.find('class="whos-on-first-step2-table"')
    start2 = html.rfind("<table", 0, start2)
    end2 = html.find("</table>", start2) + len("</table>")
    step2 = html[start2:end2]
    step1 = step1.replace('img/modules/whosonfirst/eye-icon.png', '../img/eye-icon.png')
    step1 = step1.replace('class="', "class='").replace('"', "'", 1000)
    step2 = step2.replace('class="', "class='").replace("<q>", "'").replace("</q>", "'")
    step2 = re.sub(r"<span>([^<]+)</span>", r"\1", step2)
    step2 = step2.replace('class="', "class='")
    return step1, step2


def module_button() -> str:
    return (
        head("Przycisk", "Przycisk")
        + """
\t\t\t<img src='../img/ButtonComponent.svg' class='diagram'>
\t\t\t<h2>Odnośnie Przycisku</h2>
\t\t\t<p class='flavour-text'>
\t\t\t\tMógłbyś pomyśleć, że przycisk proszący o naciśnięcie to oczywista sprawa. Właśnie takie myślenie doprowadza do eksplozji.
\t\t\t</p>

\t\t\t<p class='appendix-reference'>
\t\t\t\tZobacz Załącznik A odnośnie rozpoznawania wskaźników.<br/>
\t\t\t\tZobacz Załącznik B odnośnie rozpoznawania baterii.
\t\t\t</p><p>
\t\t\t\tPostępuj zgodnie z poniższymi zasadami w podanej kolejności. Wykonaj pierwszą czynność, która ma zastosowanie:
\t\t\t</p>

\t\t\t<ol><li>
\t\t\t\t<span class='color-blue'>Niebieski</span> 'PRZERWIJ' : przytrzymaj
\t\t\t</li><li>
\t\t\t\t'DETONUJ' I (baterie >= 2) : naciśnij i puść
\t\t\t</li><li>
\t\t\t\t<span class='color-white'>Biały</span> I wskaźnik 'CAR' : przytrzymaj
\t\t\t</li><li>
\t\t\t\t(baterie >= 3) I wskaźnik 'FRK' : naciśnij i puść
\t\t\t</li><li>
\t\t\t\t<span class='color-red'>Czerwony</span> 'PRZYTRZYMAJ' : naciśnij i puść
\t\t\t</li><li>
\t\t\t\tw przeciwnym razie : przytrzymaj
\t\t\t</li></ol>

\t\t\t<h3>Puszczanie trzymanego Przycisku</h3>
\t\t\t<p>
\t\t\t\tGdy zaczniesz trzymać wciśnięty przycisk, zaświeci się kolorowy pasek po prawej stronie modułu. Na podstawie jego koloru musisz puścić przycisk, gdy licznik czasu wyświetla podaną cyfrę na dowolnej pozycji:
\t\t\t</p>

\t\t\t<ul><li>
\t\t\t\t<em><span class='color-yellow'>Żółty</span> pasek:</em> puść na 5.
\t\t\t</li><li>
\t\t\t\t<em><span class='color-blue'>Niebieski</span> pasek:</em> puść na 4.
\t\t\t</li><li>
\t\t\t\t<em>W przeciwnym razie:</em> puść na 1.
\t\t\t</li></ul>
"""
        + foot()
    )


def module_wires() -> str:
    return (
        head("Przewody", "Przewody")
        + """
\t\t\t<img src='../img/WireComponent.svg' class='diagram'>
\t\t\t<h2>Odnośnie Przewodów</h2>
\t\t\t<p class='flavour-text'>
\t\t\t\tPrzewody to siła napędowa elektroniki! Nie, chwila, to byłby prąd. Przewody są bardziej jak tętnice. Żyły? No nieważne…
\t\t\t</p>

\t\t\t<ul>
\t\t\t\t<li>Moduł ten może zawierać 3–6 przewodów.</li>
\t\t\t\t<li>Tylko <em>jeden</em> przewód musi zostać przecięty.</li>
\t\t\t\t<li>Przewody numerowane są od góry do dołu.</li>
\t\t\t</ul>

\t\t\t<table>
\t\t\t\t<tr><td>
\t\t\t\t\t<strong><em>3 przewody:</em></strong>
\t\t\t\t\t<ul><li>
\t\t\t\t\t\tjeśli (#<span class='color-red'>czerwonych</span> == 0) : przetnij drugi przewód
\t\t\t\t\t</li><li>
\t\t\t\t\t\tjeśli (#<span class='color-blue'>niebieskich</span> > 1) I (trzeci != <span class='color-white'>biały</span>) : przetnij ostatni <span class='color-blue'>niebieski</span>
\t\t\t\t\t</li><li>
\t\t\t\t\t\tw przeciwnym razie : przetnij trzeci przewód
\t\t\t\t\t</li></ul>
\t\t\t\t</td></tr>

\t\t\t\t<tr><td>
\t\t\t\t\t<strong><em>4 przewody:</em></strong>
\t\t\t\t\t<ul>
\t\t\t\t\t<strong>PYTAJ</strong> 'Czy NS nieparzysty?' 'Ile <span class='color-red'>czerwonych</span>?'
\t\t\t\t\t<li>
\t\t\t\t\t\tjeśli (#<span class='color-red'>czerwonych</span> > 1) I (NS == nieparzysty) : przetnij ostatni <span class='color-red'>czerwony</span>
\t\t\t\t\t</li>
\t\t\t\t\t<strong>PYTAJ</strong> 'Opisz czwarty przewód.'
\t\t\t\t\t<li>
\t\t\t\t\t\tjeśli (#<span class='color-red'>czerwonych</span> == 0) I (czwarty == <span class='color-yellow'>żółty</span>) : przetnij pierwszy przewód
\t\t\t\t\t</li>
\t\t\t\t\t<strong>PYTAJ</strong> 'Ile <span class='color-blue'>niebieskich</span>?'
\t\t\t\t\t<li>
\t\t\t\t\t\tjeśli (#<span class='color-blue'>niebieskich</span> == 1) : przetnij pierwszy przewód
\t\t\t\t\t</li>
\t\t\t\t\t<strong>PYTAJ</strong> 'Ile <span class='color-yellow'>żółtych</span>?'
\t\t\t\t\t<li>
\t\t\t\t\t\tjeśli (#<span class='color-yellow'>żółtych</span> > 1) : przetnij czwarty przewód
\t\t\t\t\t</li><li>
\t\t\t\t\t\tw przeciwnym razie : przetnij drugi przewód
\t\t\t\t\t</li></ul>
\t\t\t\t</td></tr>

\t\t\t\t<tr><td>
\t\t\t\t\t<strong><em>5 przewodów:</em></strong>
\t\t\t\t\t<ul>
\t\t\t\t\t<strong>PYTAJ</strong> 'Czy NS nieparzysty?' 'Opisz 5. przewód.'
\t\t\t\t\t<li>
\t\t\t\t\t\tjeśli (5. == <span class='color-black'>czarny</span>) I (NS == nieparzysty) : przetnij czwarty przewód
\t\t\t\t\t</li>
\t\t\t\t\t<strong>PYTAJ</strong> 'Ile <span class='color-red'>czerwonych</span> / <span class='color-black'>czarnych</span> / <span class='color-yellow'>żółtych</span>?'
\t\t\t\t\t<li>
\t\t\t\t\t\tjeśli (#<span class='color-black'>czarnych</span> == 0) I (#<span class='color-red'>czerwonych</span> != 1) LUB (#<span class='color-yellow'>żółtych</span> < 2) : przetnij drugi przewód
\t\t\t\t\t</li><li>
\t\t\t\t\t\tw przeciwnym razie : przetnij pierwszy przewód
\t\t\t\t\t</li></ul>
\t\t\t\t</td></tr>

\t\t\t\t<tr><td>
\t\t\t\t\t<strong><em>6 przewodów:</em></strong>
\t\t\t\t\t<ul>
\t\t\t\t\t<strong>PYTAJ</strong> 'Czy NS nieparzysty?' 'Ile <span class='color-yellow'>żółtych</span> / <span class='color-red'>czerwonych</span> / <span class='color-white'>białych</span>?'
\t\t\t\t\t<li>
\t\t\t\t\t\tjeśli (#<span class='color-yellow'>żółtych</span> == 0) I (NS == nieparzysty) : przetnij trzeci przewód
\t\t\t\t\t</li><li>
\t\t\t\t\t\tjeśli (#<span class='color-yellow'>żółtych</span> != 1) I (#<span class='color-red'>czerwonych</span> == 0) I (#<span class='color-white'>białych</span> < 2) : przetnij ostatni przewód
\t\t\t\t\t</li><li>
\t\t\t\t\t\tw przeciwnym razie : przetnij czwarty przewód
\t\t\t\t\t</li></ul>
\t\t\t\t</td></tr>
\t\t\t</table>
"""
        + foot()
    )


def module_keypad() -> str:
    labels = {
        "Racket": "Rakieta",
        "E": "E",
        "Copyright": "Copyright",
        "Six": "Sześć",
        "Psi": "Psi",
        "A": "A",
        "W": "W",
        "Paragraph": "Akapit",
        "Smiley": "Uśmiech",
        "Lambda": "Lambda",
        "Back C": "Odwr. C",
        "Q": "Q",
        "B": "B",
        "Not Equals": "Nierówność",
        "Lightning": "Błyskawica",
        "K's": "K-k",
        "Alien": "Kosmita",
        "C": "C",
        "AE": "AE",
        "Empty Star": "Pusta gwiazda",
        "Three": "Trójka",
        "H": "H",
        "Question": "Pytajnik",
        "Dragon": "Smok",
        "N": "N",
        "Filled Star": "Pełna gwiazda",
        "Omega": "Omega",
    }
    en = Path(ROOT / "public" / "ModuleKeypad.html").read_text(encoding="utf-8")
    body = re.search(r"<div class='page-content'>(.*)</div>\s*</div>\s*</div>", en, re.DOTALL).group(1)
    for en_label, pl_label in labels.items():
        body = body.replace(f">{en_label}</p>", f">{pl_label}</p>")
    body = body.replace("On the Subject of Keypads", "Odnośnie Klawiatur")
    body = body.replace(
        "I'm not sure what these symbols are, but I suspect they have something to do with occult.",
        "Nie mam pojęcia co to za symbole, ale podejrzewam że mają coś wspólnego z okultyzmem.",
    )
    body = body.replace(
        "Only one column below has all four of the symbols from the keypad.",
        "Tylko jedna z kolumn poniżej zawiera wszystkie cztery symbole z klawiatury.",
    )
    body = body.replace(
        "Press the four buttons in the order their symbols appear from top to bottom within that column.",
        "Naciśnij cztery przyciski w kolejności, w której symbole znajdują się w tabeli, od góry do dołu.",
    )
    body = body.replace("src='img/", "src='../img/")
    return head("Klawiatury", "Klawiatury") + body + foot()


def module_simon() -> str:
    return (
        head("Simon mówi", "Simon mówi")
        + """
\t\t\t<img src='../img/SimonComponent.svg' class='diagram'>
\t\t\t<h2>Odnośnie Simon mówi</h2>
\t\t\t<p class='flavour-text'>
\t\t\t\tTo jedna z tych zabawek, którymi bawiłeś się w dzieciństwie, gdzie musiałeś wprowadzić sekwencję w odpowiedniej kolejności. Z tym, że to podróbka, zapewne prosto z bazaru.
\t\t\t</p>

\t\t\t<ol><li>
\t\t\t\tJeden z czterech kolorowych przycisków będzie migał.
\t\t\t</li><li>
\t\t\t\tKorzystając z właściwej tabeli poniżej, naciśnij przycisk o odpowiadającym kolorze.
\t\t\t</li><li>
\t\t\t\tOryginalny przycisk zaświeci się, a po nim kolejny. Powtarzaj tę sekwencję, używając mapowania kolorów.
\t\t\t</li><li>
\t\t\t\tPo każdym wprowadzeniu prawidłowej sekwencji będzie się ona wydłużać, aż do unieszkodliwienia modułu.
\t\t\t</li></ol>

\t\t\t<style>
\t\t\t\t.simon-colors span[class^='color-'] { white-space: nowrap; font-size: 0.85em; }
\t\t\t\t.simon-colors img.simon-diagram { width: 42%; vertical-align: middle; }
\t\t\t</style>
\t\t\t<table class='repeaters-table simon-colors'>
\t\t\t\t<tr>
\t\t\t\t\t<th colspan='1' class='repeaters-spacer'></th>
\t\t\t\t\t<th>Samogłoska w NS</th><th>Brak samogłoski</th>
\t\t\t\t</tr><tr>
\t\t\t\t\t<th>Brak pomyłek</th>
\t\t\t\t\t<td>
\t\t\t\t\t\t<span class='color-blue'>niebieski</span>
\t\t\t\t\t\t</br>
\t\t\t\t\t\t<span class='color-red'>czerwony</span>
\t\t\t\t\t\t<img src='../img/simon/Vowel_0.png' class='simon-diagram'>
\t\t\t\t\t\t<span class='color-yellow'>żółty</span>
\t\t\t\t\t\t</br>
\t\t\t\t\t\t<span class='color-green'>zielony</span>
\t\t\t\t\t</td><td>
\t\t\t\t\t\t<span class='color-blue'>niebieski</span>
\t\t\t\t\t\t</br>
\t\t\t\t\t\t<span class='color-red'>czerwony</span>
\t\t\t\t\t\t<img src='../img/simon/NoVowel_0.png' class='simon-diagram'>
\t\t\t\t\t\t<span class='color-yellow'>żółty</span>
\t\t\t\t\t\t</br>
\t\t\t\t\t\t<span class='color-green'>zielony</span>
\t\t\t\t\t</td>
\t\t\t\t</tr><tr>
\t\t\t\t\t<th>1 pomyłka</th>
\t\t\t\t\t<td>
\t\t\t\t\t\t<span class='color-blue'>niebieski</span>
\t\t\t\t\t\t</br>
\t\t\t\t\t\t<span class='color-red'>czerwony</span>
\t\t\t\t\t\t<img src='../img/simon/Vowel_1.png' class='simon-diagram'>
\t\t\t\t\t\t<span class='color-yellow'>żółty</span>
\t\t\t\t\t\t</br>
\t\t\t\t\t\t<span class='color-green'>zielony</span>
\t\t\t\t\t</td><td>
\t\t\t\t\t\t<span class='color-blue'>niebieski</span>
\t\t\t\t\t\t</br>
\t\t\t\t\t\t<span class='color-red'>czerwony</span>
\t\t\t\t\t\t<img src='../img/simon/NoVowel_1.png' class='simon-diagram'>
\t\t\t\t\t\t<span class='color-yellow'>żółty</span>
\t\t\t\t\t\t</br>
\t\t\t\t\t\t<span class='color-green'>zielony</span>
\t\t\t\t\t</td>
\t\t\t\t</tr><tr>
\t\t\t\t\t<th>2 pomyłki</th>
\t\t\t\t\t<td>
\t\t\t\t\t\t<span class='color-blue'>niebieski</span>
\t\t\t\t\t\t</br>
\t\t\t\t\t\t<span class='color-red'>czerwony</span>
\t\t\t\t\t\t<img src='../img/simon/Vowel_2.png' class='simon-diagram'>
\t\t\t\t\t\t<span class='color-yellow'>żółty</span>
\t\t\t\t\t\t</br>
\t\t\t\t\t\t<span class='color-green'>zielony</span>
\t\t\t\t\t</td><td>
\t\t\t\t\t\t<span class='color-blue'>niebieski</span>
\t\t\t\t\t\t</br>
\t\t\t\t\t\t<span class='color-red'>czerwony</span>
\t\t\t\t\t\t<img src='../img/simon/NoVowel_2.png' class='simon-diagram'>
\t\t\t\t\t\t<span class='color-yellow'>żółty</span>
\t\t\t\t\t\t</br>
\t\t\t\t\t\t<span class='color-green'>zielony</span>
\t\t\t\t\t</td>
\t\t\t\t</tr>
\t\t\t</table>
"""
        + foot()
    )


def module_whos_on_first(step1: str, step2: str) -> str:
    return (
        head("Kto na pierwszym", "Kto na pierwszym")
        + """
\t\t\t<img src='../img/WhosOnFirstComponent.svg' class='diagram'>
\t\t\t<h2>Odnośnie Kto na pierwszym</h2>
\t\t\t<p class='flavour-text'>
\t\t\t\tTo ustrojstwo wygląda jak coś wyjętego żywcem ze skeczów komediowych i mogłoby być zabawne, gdyby nie fakt że jest podłączone do bomby. Nie będę się rozpisywał, bo słowa tylko komplikują sprawy.
\t\t\t</p>

\t\t\t<ol><li>
\t\t\t\tSpójrz na wyświetlacz i użyj kroku 1, by ustalić z którego przycisku <u>odczytać</u> napis.
\t\t\t</li><li>
\t\t\t\tUżywając odczytanego napisu, użyj kroku 2, by ustalić który przycisk <u>wcisnąć</u>.
\t\t\t</li><li>
\t\t\t\tPowtarzaj aż do unieszkodliwienia modułu.
\t\t\t</li></ol>

\t\t\t<h3>Krok 1:</h3>
\t\t\t<p>
\t\t\t\tNa podstawie tekstu na wyświetlaczu, <u>odczytaj</u> napis na konkretnym przycisku i przejdź do kroku 2:
\t\t\t</p>

\t\t\t"""
        + step1
        + """
\t\t</div>
\t</div>
"""
        + page_header_only("Kto na pierwszym")
        + """
\t\t\t<h3>Krok 2:</h3>

\t\t\t<p>
\t\t\t\tUżywając napisu z kroku 1, <u>wciśnij pierwszy przycisk</u>, który pojawia się na liście odpowiadającej napisowi:
\t\t\t</p>

\t\t\t"""
        + step2
        + foot()
    )


def module_memory() -> str:
    return (
        head("Pamięć", "Pamięć")
        + """
\t\t\t<img src='../img/MemoryComponent.svg' class='diagram'>
\t\t\t<h2>Odnośnie Pamięci</h2>
\t\t\t<p class='flavour-text'>
\t\t\t\tPamięć jest krucha, zresztą jak wszystko inne gdy bomba wybucha, więc skup się!
\t\t\t</p>

\t\t\t<ul><li>
\t\t\t\tNaciśnij prawidłowy przycisk, by przejść do kolejnego etapu. Ukończ wszystkie etapy, by unieszkodliwić moduł.
\t\t\t</li><li>
\t\t\t\tNaciśnięcie niewłaściwego przycisku zresetuje moduł do etapu 1.
\t\t\t</li><li>
\t\t\t\tPrzyciski są numerowane od lewej do prawej.
\t\t\t</li></ul>

\t\t\t<div class='memory-rules'>
\t\t\t\t<h4>Etap 1:</h4>
\t\t\t\t<ul><li>&nbsp;
\t\t\t\t\tWyświetlacz 1 — druga pozycja
\t\t\t\t</li><li>&nbsp;
\t\t\t\t\tWyświetlacz 2 — druga pozycja
\t\t\t\t</li><li>&nbsp;
\t\t\t\t\tWyświetlacz 3 — trzecia pozycja
\t\t\t\t</li><li>&nbsp;
\t\t\t\t\tWyświetlacz 4 — czwarta pozycja
\t\t\t\t</li></ul>

\t\t\t\t<h4>Etap 2:</h4>
\t\t\t\t<ul><li>&nbsp;
\t\t\t\t\tWyświetlacz 1 — etykieta „4”
\t\t\t\t</li><li>&nbsp;
\t\t\t\t\tWyświetlacz 2 — <u>Etap 1</u>: pozycja
\t\t\t\t</li><li>&nbsp;
\t\t\t\t\tWyświetlacz 3 — pierwsza pozycja
\t\t\t\t</li><li>&nbsp;
\t\t\t\t\tWyświetlacz 4 — <u>Etap 1</u>: pozycja
\t\t\t\t</li></ul>

\t\t\t\t<h4>Etap 3:</h4>
\t\t\t\t<ul><li>&nbsp;
\t\t\t\t\tWyświetlacz 1 — <u>Etap 2</u>: etykieta
\t\t\t\t</li><li>&nbsp;
\t\t\t\t\tWyświetlacz 2 — <u>Etap 1</u>: etykieta
\t\t\t\t</li><li>&nbsp;
\t\t\t\t\tWyświetlacz 3 — trzecia pozycja
\t\t\t\t</li><li>&nbsp;
\t\t\t\t\tWyświetlacz 4 — etykieta „4”
\t\t\t\t</li></ul>

\t\t\t\t<h4>Etap 4:</h4>
\t\t\t\t<ul><li>&nbsp;
\t\t\t\t\tWyświetlacz 1 — <u>Etap 1</u>: pozycja
\t\t\t\t</li><li>&nbsp;
\t\t\t\t\tWyświetlacz 2 — pierwsza pozycja
\t\t\t\t</li><li>&nbsp;
\t\t\t\t\tWyświetlacz 3 — <u>Etap 2</u>: pozycja
\t\t\t\t</li><li>&nbsp;
\t\t\t\t\tWyświetlacz 4 — <u>Etap 2</u>: pozycja
\t\t\t\t</li></ul>

\t\t\t\t<h4>Etap 5:</h4>
\t\t\t\t<ul><li>&nbsp;
\t\t\t\t\tWyświetlacz 1 — <u>Etap 1</u>: etykieta
\t\t\t\t</li><li>&nbsp;
\t\t\t\t\tWyświetlacz 2 — <u>Etap 2</u>: etykieta
\t\t\t\t</li><li>&nbsp;
\t\t\t\t\tWyświetlacz 3 — <u>Etap 4</u>: etykieta
\t\t\t\t</li><li>&nbsp;
\t\t\t\t\tWyświetlacz 4 — <u>Etap 3</u>: etykieta
\t\t\t\t</li></ul>
\t\t\t</div>
"""
        + foot()
    )


def module_morse() -> str:
    words = [
        ("bomby", "3.565"),
        ("barka", "3.555"),
        ("broda", "3.535"),
        ("drzwi", "3.505"),
        ("harfa", "3.600"),
        ("indyk", "3.592"),
        ("kakao", "3.522"),
        ("lampa", "3.582"),
        ("obraz", "3.545"),
        ("pojazd", "3.595"),
        ("ponton", "3.552"),
        ("rower", "3.542"),
        ("rzeka", "3.532"),
        ("szafa", "3.572"),
        ("zamek", "3.575"),
        ("arbuz", "3.515"),
    ]
    rows = []
    for i in range(0, len(words), 4):
        chunk = words[i : i + 4]
        row = "<tr>\n"
        for word, freq in chunk:
            row += f"\t\t\t\t\t<th>{word.upper()}\n\t\t\t\t\t<td>{freq}\n\n"
        row += "\t\t\t\t</tr>"
        rows.append(row)
    table = "\n".join(rows)
    return (
        head("Alfabet Morse'a", "Alfabet Morse'a", "morse-code")
        + """
\t\t\t<img src='../img/MorseCodeComponent.svg' class='diagram'>
\t\t\t<h2>Odnośnie Alfabetu Morse'a</h2>
\t\t\t<p class='flavour-text'>
\t\t\t\tStaroświecka forma komunikacji na morzu? I co jeszcze? Plus jest taki że to prawdziwy Alfabet Morse'a, więc możesz się czegoś nauczyć, jeśli się przyłożysz.
\t\t\t</p>

\t\t\t<ul><li>
\t\t\t\tZinterpretuj sygnał w Alfabecie Morse'a, nadawany przez migające światło, który literuje jedno ze słów z tabeli.
\t\t\t</li><li>
\t\t\t\tSygnał jest zapętlony, z długą przerwą między powtórzeniami.
\t\t\t</li><li>
\t\t\t\tPo zidentyfikowaniu słowa ustaw odpowiadającą mu częstotliwość i naciśnij przycisk transmisji (TX).
\t\t\t</li></ul>

\t\t\t<img id='morseCodeChart' src='../img/MorseCodeTree.png'/>
\t\t\t<table>
"""
        + table
        + """
\t\t\t</table>
"""
        + foot()
    )


def module_complicated_wires() -> str:
    return (
        head("Skomplikowane przewody", "Skomplikowane przewody", "complex-wires")
        + """
\t\t\t<img src='../img/ComplexWireComponent.svg' class='diagram'>
\t\t\t<h2>Odnośnie Skomplikowanych przewodów</h2>
\t\t\t<p class='flavour-text'>
\t\t\t\tTe przewody nie są jak inne. Niektóre są w paski! To sprawia, że są zupełnie odmienne. Dobre wieści są takie, że znaleźliśmy zwięzły zestaw instrukcji, mówiących co z nimi zrobić! Może zbyt zwięzłych…
\t\t\t</p>

\t\t\t<ul><li>
\t\t\t\tSpójrz na każdy przewód: nad przewodem znajduje się dioda LED, a pod przewodem miejsce na symbol „★”.
\t\t\t</li><li>
\t\t\t\tDla <b>każdej</b> kombinacji przewód/LED/gwiazdka użyj tabeli poniżej, by zdecydować czy przewód należy przeciąć.
\t\t\t</li><li>
\t\t\t\tKażdy przewód może być w paski w wielu kolorach.
\t\t\t</li></ul>

\t\t\t</br>
\t\t\t<div>
\t\t\t\t<table id='complextable'>
\t\t\t\t\t<tr><th>Kolor<th>-<th>LED<th>★<th>LED + ★

\t\t\t\t\t<tr><th><span class='color-white'>Brak</span>
\t\t\t\t\t\t<td> PRZETNIJ
\t\t\t\t\t\t<td> NIE
\t\t\t\t\t\t<td> PRZETNIJ
\t\t\t\t\t\t<td> Baterie > 1

\t\t\t\t\t<tr><th><span class='color-red'>Czerwony</span>
\t\t\t\t\t\t<td> NS parzysty
\t\t\t\t\t\t<td> Baterie > 1
\t\t\t\t\t\t<td> PRZETNIJ
\t\t\t\t\t\t<td> Baterie > 1

\t\t\t\t\t<tr><th><span class='color-blue'>Niebieski</span>
\t\t\t\t\t\t<td> NS parzysty
\t\t\t\t\t\t<td> Port równoległy
\t\t\t\t\t\t<td> NIE
\t\t\t\t\t\t<td> Port równoległy

\t\t\t\t\t<tr><th><span class='color-red'>Czerwony</span> + <span class='color-blue'>Niebieski</span>
\t\t\t\t\t\t<td> NS parzysty
\t\t\t\t\t\t<td> NS parzysty
\t\t\t\t\t\t<td> Port równoległy
\t\t\t\t\t\t<td> NIE
\t\t\t\t</table>
\t\t\t</div>
\t\t\t</br>

\t\t\t<div style='clear:both;'/>
\t\t\t\t<p class='appendix-reference'>
\t\t\t\t\tZobacz Załącznik B odnośnie rozpoznawania baterii.<br/>
\t\t\t\t\tZobacz Załącznik C odnośnie rozpoznawania portów.
\t\t\t\t</p>
\t\t\t</div>
"""
        + foot()
    )


def module_wire_sequence() -> str:
    return (
        head("Sekwencje przewodów", "Sekwencje przewodów", "wire-sequence")
        + """
\t\t\t<img src='../img/WireSequenceComponent.svg' class='diagram'>
\t\t\t<h2>W temacie Sekwencji Przewodów</h2>
\t\t\t<p class='flavour-text'>
\t\t\t\tCiężko powiedzieć jak działa ten mechanizm. Technologia jest całkiem imponująca, ale na pewno istnieje łatwiejszy sposób na upchnięcie dziewięciu przewodów.
\t\t\t</p>

\t\t\t<ul><li>
\t\t\t\tModuł zawiera kilka paneli z przewodami, ale tylko jeden panel jest widoczny w danej chwili. Przejdź do następnego panelu strzałką w dół, do poprzedniego strzałką w górę.
\t\t\t</li><li>
\t\t\t\tNie przechodź do następnego panelu, dopóki nie jesteś pewien, że przeciąłeś wszystkie wymagane przewody na aktualnym panelu.
\t\t\t</li><li>
\t\t\t\tPrzetnij przewody według tabeli poniżej. Wystąpienia przewodów kumulują się na wszystkich panelach modułu.
\t\t\t</li></ul>
\t\t\t<div style='clear:both'></div>

\t\t\t<table class='red-table'>
\t\t\t\t<tr><th colspan='2' class='header'>Czerwone przewody
\t\t\t\t<tr><th class='first-col'>Wystąpienie<th>Przetnij, jeśli:
\t\t\t\t<tr><td class='first-col'><span class='color-red'>czerwony</span> 1<td class='second-col'>C
\t\t\t\t<tr><td class='first-col'><span class='color-red'>czerwony</span> 2<td class='second-col'>B
\t\t\t\t<tr><td class='first-col'><span class='color-red'>czerwony</span> 3<td class='second-col'>A
\t\t\t\t<tr><td class='first-col'><span class='color-red'>czerwony</span> 4<td class='second-col'>A / C
\t\t\t\t<tr><td class='first-col'><span class='color-red'>czerwony</span> 5<td class='second-col'>B
\t\t\t\t<tr><td class='first-col'><span class='color-red'>czerwony</span> 6<td class='second-col'>A / C
\t\t\t\t<tr><td class='first-col'><span class='color-red'>czerwony</span> 7<td class='second-col'>A / B / C
\t\t\t\t<tr><td class='first-col'><span class='color-red'>czerwony</span> 8<td class='second-col'>A / B
\t\t\t\t<tr><td class='first-col'><span class='color-red'>czerwony</span> 9<td class='second-col'>B

\t\t\t</table><table class='blue-table'>
\t\t\t\t<tr><th colspan='2' class='header'>Niebieskie przewody</th>
\t\t\t\t<tr><th class='first-col'>Wystąpienie<th>Przetnij, jeśli:
\t\t\t\t<tr><td class='first-col'><span class='color-blue'>niebieski</span> 1<td class='second-col'>B
\t\t\t\t<tr><td class='first-col'><span class='color-blue'>niebieski</span> 2<td class='second-col'>A / C
\t\t\t\t<tr><td class='first-col'><span class='color-blue'>niebieski</span> 3<td class='second-col'>B
\t\t\t\t<tr><td class='first-col'><span class='color-blue'>niebieski</span> 4<td class='second-col'>A
\t\t\t\t<tr><td class='first-col'><span class='color-blue'>niebieski</span> 5<td class='second-col'>B
\t\t\t\t<tr><td class='first-col'><span class='color-blue'>niebieski</span> 6<td class='second-col'>B / C
\t\t\t\t<tr><td class='first-col'><span class='color-blue'>niebieski</span> 7<td class='second-col'>C
\t\t\t\t<tr><td class='first-col'><span class='color-blue'>niebieski</span> 8<td class='second-col'>A / C
\t\t\t\t<tr><td class='first-col'><span class='color-blue'>niebieski</span> 9<td class='second-col'>A

\t\t\t</table><table class='black-table'><tr><th colspan='2' class='header'>Czarne przewody</th>
\t\t\t\t<tr><th class='first-col'>Wystąpienie</th><th>Przetnij, jeśli:</th>
\t\t\t\t<tr><td class='first-col'><span class='color-black'>czarny</span> 1<td class='second-col'>A / B / C
\t\t\t\t<tr><td class='first-col'><span class='color-black'>czarny</span> 2<td class='second-col'>A / C
\t\t\t\t<tr><td class='first-col'><span class='color-black'>czarny</span> 3<td class='second-col'>B
\t\t\t\t<tr><td class='first-col'><span class='color-black'>czarny</span> 4<td class='second-col'>A / C
\t\t\t\t<tr><td class='first-col'><span class='color-black'>czarny</span> 5<td class='second-col'>B
\t\t\t\t<tr><td class='first-col'><span class='color-black'>czarny</span> 6<td class='second-col'>B / C
\t\t\t\t<tr><td class='first-col'><span class='color-black'>czarny</span> 7<td class='second-col'>A / B
\t\t\t\t<tr><td class='first-col'><span class='color-black'>czarny</span> 8<td class='second-col'>C
\t\t\t\t<tr><td class='first-col'><span class='color-black'>czarny</span> 9<td class='second-col'>C
\t\t\t</table>
"""
        + foot()
    )


def module_maze() -> str:
    return (
        head("Labirynty", "Labirynty")
        + """
\t\t\t<img src='../img/MazeComponent.svg' class='diagram'>
\t\t\t<h2>Odnośnie Labiryntów</h2>
\t\t\t<p class='flavour-text'>
\t\t\t\tWygląda to na jakiś rodzaj labiryntu, zapewne skradziony z restauracyjnej podkładki pod talerz.
\t\t\t</p>

\t\t\t<ul><li>
\t\t\t\tZnajdź labirynt z pasującymi, okrągłymi znacznikami.
\t\t\t</li><li>
\t\t\t\tRozbrajający musi doprowadzić białe światełko do czerwonego trójkąta, używając przycisków ze strzałkami.
\t\t\t</li><li>
\t\t\t\t<strong>Uwaga:</strong> Nie przecinaj linii widocznych w labiryncie. Te linie są niewidzialne na bombie.
\t\t\t</li><li>
\t\t\t\tDla szybkiego odniesienia unikalne <strong>pozycje wierszy</strong> znaczników okrągłych są oznaczone po lewej stronie każdego labiryntu.
\t\t\t</li></ul>

\t\t\t\t\t\t1-6 <img class='maze' src='../img/maze/maze0.svg'/>
\t\t\t&nbsp;&nbsp;2-5 <img class='maze' src='../img/maze/maze1.svg'/>
\t\t\t&nbsp;&nbsp;4-6 <img class='maze' src='../img/maze/maze2.svg'/>

\t\t\t\t\t\t1-1 <img class='maze' src='../img/maze/maze3.svg'/>
\t\t\t&nbsp;&nbsp;4-5 <img class='maze' src='../img/maze/maze4.svg'/>
\t\t\t&nbsp;&nbsp;3-5 <img class='maze' src='../img/maze/maze5.svg'/>

\t\t\t\t\t\t2-2 <img class='maze' src='../img/maze/maze6.svg'/>
\t\t\t&nbsp;&nbsp;3-4 <img class='maze' src='../img/maze/maze7.svg'/>
\t\t\t&nbsp;&nbsp;1-3 <img class='maze' src='../img/maze/maze8.svg'/>
"""
        + foot()
    )


def module_password() -> str:
    words = [
        "alarm", "apacz", "arena", "babka", "cecha", "ekipa", "fajka", "farma",
        "głowa", "hańba", "larwa", "laska", "macka", "obiad", "palec", "palma",
        "pegaz", "robak", "scena", "skrót", "smoła", "smycz", "tafla", "teren",
        "toast", "torba", "trasa", "twarz", "walka", "wełna", "wnęka", "zakaz",
        "zwiad", "znicz", "żniwa",
    ]
    cols = 5
    rows = []
    for i in range(0, len(words), cols):
        chunk = words[i : i + cols]
        row = "<tr>" + "".join(f"<td>{w}</td>" for w in chunk)
        if len(chunk) < cols:
            row += "<td></td>" * (cols - len(chunk))
        row += "</tr>"
        rows.append(row)
    table = "\n".join(rows)
    return (
        head("Hasła", "Hasła")
        + """
\t\t\t<img src='../img/PasswordComponent.svg' class='diagram'>
\t\t\t<h2>Odnośnie Haseł</h2>
\t\t\t<p class='flavour-text'>
\t\t\t\tNa szczęście to hasło zdaje się nie spełniać rządowych wymogów bezpieczeństwa: 22 znaki, małe i wielkie litery, numery w losowej kolejności, bez palindromów dłuższych niż 3 znaki.
\t\t\t</p>

\t\t\t<ul><li>
\t\t\t\tPrzyciski nad i pod każdą literą pozwolą przejrzeć możliwości dla tej pozycji.
\t\t\t</li><li>
\t\t\t\tTylko jedna kombinacja dostępnych liter będzie pasować do hasła poniżej.
\t\t\t</li><li>
\t\t\t\tNaciśnij przycisk zatwierdzający po ustawieniu prawidłowego hasła.
\t\t\t</li></ul>

\t\t\t<table class='password-table'>
"""
        + table
        + """
\t\t\t</table>
"""
        + foot()
    )


def module_needy_misc() -> str:
    return (
        head("Moduły irytki", "Sekcja 2: Moduły irytki", "section-title")
        + """
\t\t\t<div class='vertical-spacer-small'></div>
\t\t\t<img src='../img/NeedyComponent.svg' class='diagram' />
\t\t\t<div class='new-block-formatting-context'>
\t\t\t\t<h1>Sekcja 2: Moduły irytki</h1>
\t\t\t\t<p>
\t\t\t\t\tModuły irytki nie mogą zostać unieszkodliwione i stanowią powracające zagrożenie.
\t\t\t\t</p><p>
\t\t\t\t\tModuły irytki można rozpoznać po małym 2&#8209;cyfrowym liczniku na środku górnej części modułu. Interakcja z bombą może spowodować ich aktywację. Po aktywowaniu wymagają regularnej uwagi, by zapobiec pomyłce, gdy ich licznik dobiegnie końca.
\t\t\t\t</p><p>
\t\t\t\t\tPozostań czujny: moduły irytki mogą aktywować się ponownie w każdej chwili.
\t\t\t\t</p>
\t\t\t</div>

\t\t\t<div class='vertical-spacer-smaller'></div>

\t\t\t<img src='../img/NeedyVentComponent.svg' class='diagram' />
\t\t\t<h2>Odnośnie Wietrzenia gazu</h2>
\t\t\t<p class='flavour-text'>
\t\t\t\tHakowanie to ciężka robota! Cóż, zazwyczaj tak jest. Do tego zadania wystarczy pijący ptak, wciskający na okrągło ten sam przycisk.
\t\t\t</p>
\t\t\t<ul><li>
\t\t\t\tOdpowiedz na zapytania komputera, naciskając „T” dla „Tak” lub „N” dla „Nie”.
\t\t\t</li></ul>

\t\t\t<div class='vertical-spacer-smaller'></div>

\t\t\t<img src='../img/NeedyDischargeComponent.svg' class='diagram' />
\t\t\t<h2>Odnośnie Rozładowywania kondensatora</h2>
\t\t\t<p class='flavour-text'>
\t\t\t\tObstawiam, że to ustrojstwo ma po prostu przyciągnąć twoją uwagę, bo w przeciwnym razie to straszna fuszerka.
\t\t\t</p>
\t\t\t<ul><li>
\t\t\t\tRozładuj kondensator zanim zostanie przeciążony, przytrzymując jego dźwignię.
\t\t\t</li></ul>
"""
        + foot()
    )


def module_needy_knob() -> str:
    return (
        head("Gałki", "Gałki")
        + """
\t\t\t<img src='../img/NeedyKnobComponent.svg' class='diagram'>
\t\t\t<h2>Odnośnie Gałek</h2>
\t\t\t<p class='flavour-text'>
\t\t\t\tNiepotrzebnie skomplikowany i nieskończenie domagający się uwagi. Wyobraź sobie co by się stało, gdyby to ustrojstwo było używane do stworzenia czegoś innego niż diaboliczne łamigłówki.
\t\t\t</p>

\t\t\t<ul><li>
\t\t\t\tGałka może być ustawiona w jednym z czterech położeń.
\t\t\t</li><li>
\t\t\t\tGałka musi być we właściwym położeniu, gdy licznik czasu modułu dojdzie do zera.
\t\t\t</li><li>
\t\t\t\tWłaściwe położenie można określić na podstawie konfiguracji dwunastu włączonych/wyłączonych diod LED.
\t\t\t</li><li>
\t\t\t\tPołożenia gałki odnoszą się do napisu „GÓRA”, który może zmieniać pozycję.
\t\t\t</li></ul>

\t\t\t<h3>Konfiguracje diod LED</h3>

\t\t\t<h4>Położenie prawe:</h4>
\t\t\t<table style='display: inline-table'>
\t\t\t\t<tr><td>.<td>.<td>.<td>X<td>.<td>.
\t\t\t\t<tr><td>.<td>.<td>.<td>.<td>.<td>.
\t\t\t</table>

\t\t\t<h4>Położenie lewe:</h4>
\t\t\t<table style='display: inline-table'>
\t\t\t\t<tr><td> <td> <td> <td> <td>X<td>
\t\t\t\t<tr><td>.<td>.<td>.<td>.<td>.<td>.
\t\t\t</table>

\t\t\t<h4>Położenie górne:</h4>
\t\t\t<table style='display: inline-table'>
\t\t\t\t<tr><td>.<td>.<td>.<td>.<td>X<td>X
\t\t\t\t<tr><td>.<td>.<td>.<td>.<td>.<td>.
\t\t\t</table>
\t\t\t<table style='display: inline-table'>
\t\t\t\t<tr><td>.<td>.<td>.<td>.<td>.<td>.
\t\t\t\t<tr><td>.<td>.<td>.<td>.<td>X<td>X
\t\t\t</table>

\t\t\t<h4>Położenie dolne:</h4>
\t\t\tJeśli żadna z powyższych konfiguracji nie pasuje, ustaw gałkę w położeniu dolnym.

\t\t\t<h5>Legenda tabeli:</h5>
\t\t\t<table style='display: inline-table'>
\t\t\t\t<tr><td>X<td> Dioda musi być włączona
\t\t\t\t<tr><td> <td> Dioda musi być wyłączona
\t\t\t\t<tr><td>.<td> Dioda może być ignorowana
\t\t\t</table>
"""
        + foot()
    )


def readme_pl() -> str:
    return """# Uproszczony podręcznik rozbrajania bomb KTANE

Udoskonalona wersja oryginalnego podręcznika rozbrajania bomb do gry „Keep Talking and Nobody Explodes”,
z lepszą czytelnością i łatwością użycia. To nie jest inteligentny podręcznik ani inne narzędzie wspomagające
rozbrajanie — to po prostu bardziej przejrzysta wersja oryginalnego dokumentu.

Zaleca się zastąpienie odpowiednich stron oryginalnego podręcznika ich uproszczonymi odpowiednikami.

## Moduły

### Przewody
Uproszczona logika decyzyjna i bardziej zwięzłe kroki.

Kolory przewodów są oznaczone kolorem w tekście.

### Przycisk
Znacznie uproszczona logika decyzyjna, co skraca czas podejmowania decyzji.

Kolory przycisków są oznaczone kolorem w tekście.

### Klawiatury
Dodano etykiety tekstowe pod symbolami, by usunąć niejednoznaczność.

### Simon mówi
Transformacje przedstawione jako czytelne diagramy zamiast tekstu.

### Kto na pierwszym
Uporządkowano elementy obu kroków alfabetycznie.

Usunięto zbędne warianty słów z kroku 2.

### Pamięć
Bardziej zwięzłe kroki.

### Alfabet Morse'a
Wykres kodu Morse'a zastąpiono równoważnym drzewem binarnym.

Rozwiązania posortowano alfabetycznie zamiast według częstotliwości.

### Skomplikowane przewody
Diagram Venna zastąpiono zwięzłą tabelą 4×4.

Kolory przewodów są oznaczone kolorem w tekście.

### Sekwencje przewodów
Bardziej zwięzła tabela.

Kolory przewodów są oznaczone kolorem w tekście.

### Labirynty
Oznaczono każdy labirynt unikalną parą numerów kolumn dla kółek.

### Hasła
Hasła w tabeli alfabetycznej (uproszczona wersja polskiej listy haseł).

## Moduły irytki
Wietrzenie gazu i rozładowywanie kondensatora zebrane na jednej stronie.

### Gałki
Znacznie uproszczona logika — w niektórych przypadkach istotna jest tylko jedna pozycja LED.
"""


def build_wof_step1_manual() -> str:
    """Build WOF step 1 from official Polish manual structure."""
    eye = "<img src='../img/eye-icon.png' alt='Spójrz na' style='height: 1em;'/>"
    empty = "<td></td>"
    br = "<td><br></td>"

    def cell(display: str, data_row: int, col: int) -> str:
        grid = [[br, br] for _ in range(3)]
        grid[data_row][col] = f"<td class='whos-on-first-look-at'>{eye}</td>"
        rows_html = "".join(f"<tr>{''.join(grid[r])}</tr>" for r in range(3))
        return (
            f"<td><table><tr><th class='whos-on-first-look-at-display' colspan='2'>{display}</th></tr>"
            f"{rows_html}</table></td>"
        )

    mapping = {
        "TAK": (1, 0),
        "BUT": (0, 1),
        "WYŚWIETLACZ": (2, 1),
        "OKEJ": (0, 1),
        "JA?": (2, 1),
        "NIC": (1, 0),
        "": (1, 0),
        "PUSTY": (1, 1),
        "NIE": (2, 1),
        "MIEĆ": (1, 0),
        "MIEDŹ": (2, 1),
        "MOŻE": (1, 1),
        "MORZE": (1, 1),
        "LUD": (2, 0),
        "LÓD": (2, 0),
        "LUT": (2, 1),
        "BUK": (1, 1),
        "BÓG": (2, 1),
        "BUG": (1, 1),
        "KOLAŻ": (1, 1),
        "KOLARZ": (0, 0),
        "RĄB": (2, 1),
        "ROMB": (2, 0),
        "JAK": (1, 1),
        "JAK?": (1, 0),
        "JA": (2, 1),
        "KOD": (2, 1),
        "KOT": (2, 1),
    }
    layout = [
        ["TAK", "BUT", "WYŚWIETLACZ", "OKEJ", "JA?", "NIC"],
        ["", "PUSTY", "NIE", "MIEĆ", "MIEDŹ", "MOŻE"],
        ["MORZE", "LUD", "LÓD", "LUT", "BUK", "BÓG"],
        ["BUG", "KOLAŻ", "KOLARZ", "RĄB", "ROMB", "JAK"],
        ["", "JAK?", "JA", "KOD", "KOT", ""],
    ]
    rows = []
    for row_idx, row_words in enumerate(layout):
        row_cells = []
        for col_idx, word in enumerate(row_words):
            if not word:
                # Pusty wyświetlacz (nie mylić z PUSTY na przycisku)
                if row_idx == 1 and col_idx == 0:
                    r, c = mapping[""]
                    row_cells.append(cell("", r, c))
                else:
                    row_cells.append("<td></td>")
                continue
            r, c = mapping[word]
            row_cells.append(cell(word, r, c))
        rows.append("<tr>" + "".join(row_cells) + "</tr>")
    return "<table class='whos-on-first-step1-table'>" + "".join(rows) + "</table>"


def trim_wof_step2_list(key: str, word_list: str) -> str:
    """Keep only words up to and including the row key (simplified manual)."""
    words = [w.strip() for w in word_list.split(",")]
    for i, word in enumerate(words):
        if word == key:
            return ", ".join(words[: i + 1])
    return word_list


def build_wof_step2_from_md() -> str:
    rows = [
        ("GOTÓW", "TAK, OKEJ, HAH, ŚRODEK, LEWY, NADUŚ, PRAWY, PUSTY, GOTÓW, NIE, PIERWSZY, ŹLE, NIC, CZEKAJ"),
        ("PIERWSZY", "LEWY, OKEJ, TAK, ŚRODEK, NIE, PRAWY, NIC, ŹLE, CZEKAJ, GOTÓW, PUSTY, HAH, NADUŚ, PIERWSZY"),
        ("NIE", "PUSTY, ŹLE, CZEKAJ, PIERWSZY, HAH, GOTÓW, PRAWY, TAK, NIC, LEWY, NADUŚ, OKEJ, NIE, ŚRODEK"),
        ("PUSTY", "CZEKAJ, PRAWY, OKEJ, ŚRODEK, PUSTY, NADUŚ, GOTÓW, NIC, NIE, HAH, LEWY, ŹLE, TAK, PIERWSZY"),
        ("NIC", "ŹLE, PRAWY, OKEJ, ŚRODEK, TAK, PUSTY, NIE, NADUŚ, LEWY, HAH, CZEKAJ, PIERWSZY, NIC, GOTÓW"),
        ("TAK", "OKEJ, PRAWY, ŹLE, ŚRODEK, PIERWSZY, HAH, NADUŚ, GOTÓW, NIC, TAK, LEWY, PUSTY, NIE, CZEKAJ"),
        ("HAH", "ŹLE, HAH, LEWY, NIC, GOTÓW, PUSTY, ŚRODEK, NIE, OKEJ, PIERWSZY, CZEKAJ, TAK, NADUŚ, PRAWY"),
        ("ŹLE", "GOTÓW, NIC, LEWY, HAH, OKEJ, TAK, PRAWY, NIE, NADUŚ, PUSTY, ŹLE, ŚRODEK, CZEKAJ, PIERWSZY"),
        ("LEWY", "PRAWY, LEWY, PIERWSZY, NIE, ŚRODEK, TAK, PUSTY, HAH, ŹLE, CZEKAJ, NADUŚ, GOTÓW, OKEJ, NIC"),
        ("PRAWY", "TAK, NIC, GOTÓW, NADUŚ, NIE, CZEKAJ, HAH, PRAWY, ŚRODEK, LEWY, ŹLE, PUSTY, OKEJ, PIERWSZY"),
        ("ŚRODEK", "PUSTY, GOTÓW, OKEJ, HAH, NIC, NADUŚ, NIE, CZEKAJ, LEWY, ŚRODEK, PRAWY, PIERWSZY, ŹLE, TAK"),
        ("OKEJ", "ŚRODEK, NIE, PIERWSZY, TAK, ŹLE, NIC, CZEKAJ, OKEJ, LEWY, GOTÓW, PUSTY, NADUŚ, HAH, PRAWY"),
        ("CZEKAJ", "ŹLE, NIE, PUSTY, OKEJ, TAK, LEWY, PIERWSZY, NADUŚ, HAH, CZEKAJ, NIC, GOTÓW, PRAWY, ŚRODEK"),
        ("NADUŚ", "PRAWY, ŚRODEK, TAK, GOTÓW, NADUŚ, OKEJ, NIC, ŹLE, PUSTY, LEWY, PIERWSZY, HAH, NIE, CZEKAJ"),
        ("BUK", "DALEJ, BÓG, BUG, BUT, NASTĘPNY, LUT, LÓD, TRZYMAJ, CO?, BUK, HAHA, KTÓRY?, DOBRZE, LUD"),
        ("BÓG", "BUG, NASTĘPNY, KTÓRY?, LUT, CO?, DOBRZE, HAHA, TRZYMAJ, BUK, LUD, BUT, DALEJ, LÓD, BÓG"),
        ("BUG", "HAHA, BÓG, LUT, BUG, NASTĘPNY, LÓD, DALEJ, LUD, BUT, BUK, CO?, TRZYMAJ, KTÓRY?, DOBRZE"),
        ("BUT", "BUK, BUT, LÓD, NASTĘPNY, HAHA, BÓG, LUD, BUG, CO?, LUT, DALEJ, DOBRZE, KTÓRY?, TRZYMAJ"),
        ("LÓD", "DOBRZE, LUD, LÓD, LUT, CO?, DALEJ, BUG, TRZYMAJ, BUT, KTÓRY?, NASTĘPNY, HAHA, BÓG, BUK"),
        ("LUD", "LUT, DALEJ, NASTĘPNY, CO?, BUT, LÓD, HAHA, DOBRZE, LUD, BUK, KTÓRY?, TRZYMAJ, BÓG, BUG"),
        ("LUT", "LUT, BUG, BÓG, BUK, DOBRZE, TRZYMAJ, HAHA, NASTĘPNY, DALEJ, KTÓRY?, BUT, LÓD, LUD, CO?"),
        ("HAHA", "LÓD, LUD, BÓG, BUT, NASTĘPNY, HAHA, DOBRZE, BUK, LUT, KTÓRY?, BUG, DALEJ, TRZYMAJ, CO?"),
        ("CO?", "BUK, TRZYMAJ, BUT, BUG, LUD, DOBRZE, HAHA, KTÓRY?, BÓG, LUT, LÓD, NASTĘPNY, CO?, DALEJ"),
        ("DOBRZE", "DALEJ, LUT, NASTĘPNY, CO?, BUG, LÓD, BUT, TRZYMAJ, KTÓRY?, BUK, LUD, BÓG, HAHA, DOBRZE"),
        ("NASTĘPNY", "CO?, LUT, HAHA, BUG, TRZYMAJ, DALEJ, NASTĘPNY, KTÓRY?, DOBRZE, BÓG, LÓD, BUT, LUD, BUK"),
        ("TRZYMAJ", "BÓG, LUD, DOBRZE, HAHA, BUK, LÓD, DALEJ, CO?, BUT, NASTĘPNY, TRZYMAJ, LUT, BUG, KTÓRY?"),
        ("DALEJ", "BÓG, DOBRZE, KTÓRY?, BUT, BUK, TRZYMAJ, LUT, LÓD, DALEJ, LUD, CO?, NASTĘPNY, BUG, HAHA"),
        ("KTÓRY?", "BUT, NASTĘPNY, LUD, LÓD, TRZYMAJ, DOBRZE, HAHA, CO?, LUT, BUK, KTÓRY?, DALEJ, BÓG, BUG"),
    ]
    body = []
    for key, vals in rows:
        trimmed = trim_wof_step2_list(key, vals)
        body.append(
            f"\t\t\t\t<tr>\n\t\t\t\t\t<th>'{key}':</th>\n"
            f"\t\t\t\t\t<td>{trimmed}</td>\n\t\t\t\t</tr>"
        )
    return "<table class='whos-on-first-step2-table'>\n" + "\n".join(body) + "\n\t\t\t</table>"


def write_combined_index_and_pdf() -> None:
    modules = sorted(PL_DIR.glob("Module*.html"))
    parts = []
    for path in modules:
        content = path.read_text(encoding="utf-8")
        body = content.split("<body>", 1)[1].rsplit("</body>", 1)[0]
        parts.append(body)

    index = PL_DIR / "index.html"
    index.write_text(
        f"""<!DOCTYPE html>
<html lang='pl'><head><meta charset='utf-8'>
<link href='https://fonts.googleapis.com/css?family=Special+Elite' rel='stylesheet'>
<link rel='stylesheet' href='../css/normalize.css'>
<link rel='stylesheet' href='../css/main.css'>
<style>@media print {{ .page {{ page-break-after: always; }} }}</style>
</head><body>{''.join(parts)}</body></html>""",
        encoding="utf-8",
    )
    print(f"Wrote {index}")

    try:
        from playwright.sync_api import sync_playwright

        import shutil
        pdf_path = PL_DIR / "KTANE-v1-Uproszczony-pl.pdf"
        assets_pdf = ROOT / "assets" / "pdf" / "KTANE-v1-Uproszczony-pl.pdf"
        assets_pdf.parent.mkdir(parents=True, exist_ok=True)
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(index.resolve().as_uri(), wait_until="networkidle")
            page.pdf(path=str(pdf_path), format="Letter", print_background=True)
            browser.close()
        shutil.copy2(pdf_path, assets_pdf)
        print(f"Wrote {pdf_path} and {assets_pdf}")
    except ImportError:
        print("Skipping PDF (install playwright to generate KTANE-v1-Uproszczony-pl.pdf)")


def main() -> None:
    PL_DIR.mkdir(exist_ok=True)
    step1 = build_wof_step1_manual()
    step2 = build_wof_step2_from_md()

    files = {
        "ModuleButton.html": module_button(),
        "ModuleWires.html": module_wires(),
        "ModuleKeypad.html": module_keypad(),
        "ModuleSimon.html": module_simon(),
        "ModuleWhosOnFirst.html": module_whos_on_first(step1, step2),
        "ModuleMemory.html": module_memory(),
        "ModuleMorseCode.html": module_morse(),
        "ModuleComplicatedWires.html": module_complicated_wires(),
        "ModuleWireSequence.html": module_wire_sequence(),
        "ModuleMaze.html": module_maze(),
        "ModulePassword.html": module_password(),
        "ModuleNeedyMisc.html": module_needy_misc(),
        "ModuleNeedyKnob.html": module_needy_knob(),
        "README.md": readme_pl(),
    }
    for name, content in files.items():
        path = PL_DIR / name
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {path}")

    write_combined_index_and_pdf()


if __name__ == "__main__":
    main()
