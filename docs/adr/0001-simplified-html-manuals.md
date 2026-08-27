[Strona główna](../../README.md) > [Dokumentacja](../README.md) > [ADR](README.md) > [ADR 0001](0001-simplified-html-manuals.md)

---

# ADR 0001: Uproszczony Format Modułów HTML i Generator Wersji PL

* **Status:** Zaakceptowany
* **Data:** 2026-08-15
* **Autorzy:** Kacper Czeczot

---

## Kontekst
Oryginalny podręcznik do gry *Keep Talking and Nobody Explodes* zawiera wiele rozwlekłych opisów tekstowych, które podczas rozgrywki na czas spowalniają komunikację między Saperem a Ekspertem.

## Decyzja
1. **Moduły HTML w `public/`:** Każdy moduł posiada zoptymalizowaną stronę HTML z tabelami decyzyjnymi, diagramami i skróconą logiką.
2. **Automatyczny generator wersji polskiej (`scripts/generate_pl_html.py`):** Skrypt parsuje moduły i generuje wersję polską w `public/pl/` oraz kompiluje dokument do PDF.
3. **Pliki PDF w `assets/pdf/`:** Gotowe materiały do druku.

## Konsekwencje
### Pozytywne:
- Radykalne skrócenie czasu podejmowania decyzji przy rozbrajaniu bomb.
- Pełna dwujęzyczność (PL/EN) i możliwość wydruku fizycznego.
