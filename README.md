# Tar Valon Scraper

![Build](https://img.shields.io/badge/build-0.2.0-blue)
[![PyPI](https://img.shields.io/pypi/v/tarvalon-scraper)](https://pypi.org/project/tarvalon-scraper/)
[![AUR](https://img.shields.io/aur/version/tarvalon-scraper)](https://aur.archlinux.org/packages/tarvalon-scraper)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**All your Wheel of Time summaries, in one place.**

Scraper for the Tar Valon Library — a comprehensive fan resource for Robert Jordan's *The Wheel of Time* — that pulls chapter summaries and compiles them into clean, offline-ready Markdown or EPUB files.

[Homepage](https://github.com/code7wormer/tar_valon_scraper) · [PyPI](https://pypi.org/project/tarvalon-scraper/)

<p align="center">
<img width="1342" height="740" alt="menu_prtsc" src="https://github.com/user-attachments/assets/2f4b7f90-bd3a-4ff8-911a-6515a632810b" />
</p>
## Features

- Book selection
- Chapter scraping
- Concurrent downloads
- Markdown export
- EPUB export

## Tech Stack

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) — HTML parsing
- [ebooklib](https://github.com/aerkalov/ebooklib) — EPUB generation
- [rich](https://github.com/Textualize/rich) — CLI output and progress bars

## Installation

### From PyPI

```bash
pip install tarvalon-scraper
```

### From the AUR

```bash
yay -S tarvalon-scraper
```

## Usage

```bash
tarvalon
```

## License

MIT
