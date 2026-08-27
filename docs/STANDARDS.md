[Strona główna](../README.md) > [Dokumentacja](README.md) > [Standardy](STANDARDS.md)

---

# Standardy Inżynieryjne Projektu: KTANE Manual

Projekt jest dostosowany do modelu architektonicznego **Single-App** ([`template-single-app`](https://github.com/kacperczeczot/template-single-app)) i przestrzega reguł zdefiniowanych w centralnej Konstytucji **[`devex-standards`](https://github.com/kacperczeczot/devex-standards)**.

---

## 1. Zgodność ze Standardami Zewnętrznymi

| Standard | Implementacja w Projekcie | Oficjalna Specyfikacja |
| :--- | :--- | :--- |
| **Conventional Commits** | Commity w języku angielskim (`feat:`, `fix:`, `docs:`, `refactor:`) | [conventionalcommits.org](https://www.conventionalcommits.org/pl/v1.0.0/) |
| **Semantic Versioning** | SemVer (`MAJOR.MINOR.PATCH`) | [semver.org](https://semver.org/lang/pl/) |
| **Keep a Changelog** | [`CHANGELOG.md`](../CHANGELOG.md) wg specyfikacji 1.1.0 | [keepachangelog.com](https://keepachangelog.com/pl/1.1.0/) |
| **ADR** | Rejestr Decyzji w [`docs/adr/`](adr/README.md) | [adr.github.io](https://adr.github.io/) |
| **EditorConfig** | [`.editorconfig`](../.editorconfig) w root dla spójności IDE | [editorconfig.org](https://editorconfig.org/) |

---

## 2. Bramki Jakościowe i Weryfikacja

- **Kompilacja i generowanie wersji PL/PDF:** `python3 scripts/generate_pl_html.py` (weryfikuje spójność 13 modułów i tworzy PDF).
- **Integralność odnośników:** Poprawność ścieżek do stylów `public/css/` i grafik `public/img/`.

---

## 3. Źródło Prawdy (SSOT)
👉 **[devex-standards / Architecture Rules](https://github.com/kacperczeczot/devex-standards/blob/main/docs/architecture/RULES.md)**
👉 **[devex-standards / Tooling Rules](https://github.com/kacperczeczot/devex-standards/blob/main/docs/tooling/RULES.md)**
