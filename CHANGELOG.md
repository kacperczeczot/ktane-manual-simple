# Dziennik Zmian (Changelog)

Wszystkie istotne zmiany w projekcie są dokumentowane w tym pliku zgodnie ze standardem [Keep a Changelog](https://keepachangelog.com/pl/1.1.0/) oraz [Semantic Versioning](https://semver.org/lang/pl/).

---

## [Unreleased]

### Added
- Dostosowanie repozytorium do standardów DevEx (Single-App).
- Struktura dokumentacji `docs/` z certyfikatem `docs/STANDARDS.md` i rejestrem `docs/adr/`.
- Pliki konfiguracyjne: `.editorconfig`, `.agents/rules/project.md`, `.github/pull_request_template.md`.
- Strona główna podręcznika `public/index.html` z wyborem języka PL/EN.

### Changed
- Reorganizacja struktury do Kanonu Root:
  - `Module*.html`, `pl/`, `css/`, `img/` ➡️ `public/`
  - `pdf/` ➡️ `assets/pdf/`
- Zaktualizowanie generatora `scripts/generate_pl_html.py` do nowych ścieżek `public/` i `assets/`.

---

## [1.0.0] - 2026-08-15

### Added
- Zoptymalizowane moduły podręcznika KTANE (13 modułów).
- Wersja polska podręcznika oraz generator PDF.
