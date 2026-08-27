# KTANE — Uproszczony Podręcznik Rozbrajania Bomb

> Zoptymalizowany pod kątem szybkości podejmowania decyzji i czytelności podręcznik dla Ekspertów do gry *Keep Talking and Nobody Explodes*.

---

## 1. Korzystanie z Podręcznika


| Dokument / Sekcja | Opis |
| :--- | :--- |
| [Dokumentacja Projektu (`docs/README.md`)](docs/README.md) | Centralny hub dokumentacji technicznej |
| [Reguły AI Projektu (`.agents/rules/project.md`)](.agents/rules/project.md) | Wytyczne domenowe dla asystentów AI |

---

## 2. Mapa Repozytorium

* 📁 [**`public/`**](public/README.md) — Bezserwerowy interfejs webowy podręcznika (wersja polska `pl/`, wersja angielska, style CSS i diagramy).
* 📁 [**`assets/`**](assets/README.md) — Gotowe pliki PDF do druku fizycznego (`assets/pdf/`).
* 📁 [**`docs/`**](docs/README.md) — Dokumentacja techniczna i rejestr ADR.
* 📁 [**`scripts/`**](scripts/README.md) — Generator wersji polskiej i kompilator PDF (`generate_pl_html.py`).

---

## 3. Uruchomienie i Użycie

### Przeglądanie w przeglądarce:
Otwórz plik `public/index.html` bezpośrednio w przeglądarce.

### Regeneracja wersji polskiej i PDF:
```bash
python3 scripts/generate_pl_html.py
```
