import os
import sys

from tarvalon_scraper.books_scraper import book_scrape
from tarvalon_scraper.chap_list_scraper import list_scrape
from tarvalon_scraper.content_scraper import content_scrape
from tarvalon_scraper.exporter import make_epub
from tarvalon_scraper.book_compiler import scrape_book

from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.rule import Rule
from rich.prompt import IntPrompt
from rich import box


def _detect_unicode_support() -> bool:
    if os.environ.get("TARVALON_ASCII", "0") != "0":
        return False
    if os.environ.get("TARVALON_UNICODE", "0") != "0":
        return True

    encoding = (getattr(sys.stdout, "encoding", None) or "").upper()
    if "UTF" not in encoding:
        return False

    if sys.platform == "win32" and not (
        os.environ.get("WT_SESSION") or os.environ.get("TERM_PROGRAM")
    ):
        return False

    return True


UNICODE_OK = _detect_unicode_support()

BOX_PANEL = box.DOUBLE_EDGE if UNICODE_OK else box.ASCII_DOUBLE_HEAD
BOX_TABLE = box.SIMPLE_HEAVY if UNICODE_OK else box.ASCII2
BOX_SUCCESS = box.ROUNDED if UNICODE_OK else box.ASCII
RULE_CHAR = "─" if UNICODE_OK else "-"

VIOLET = "#8b5cf6"
GOLD = "#facc15"
TEXT = "#f4f4f5"
SUCCESS = "#4ade80"

THEME = Theme(
    {
        "title": f"bold {GOLD}",
        "index": f"bold {VIOLET}",
        "item": TEXT,
        "prompt": f"bold {VIOLET}",
        "success": f"bold {SUCCESS}",
        "border": VIOLET,
    }
)

console = Console(theme=THEME)

BOOK_URL = "https://library.tarvalon.net/index.php?title=Chapter_Summaries"

GRADIENT_START = (139, 92, 246)
GRADIENT_END = (250, 204, 21)


def _card_width():
    return max(56, min(console.size.width - 8, 78))


def _lerp_color(start, end, t):
    return tuple(int(start[i] + (end[i] - start[i]) * t) for i in range(3))


def gradient_text(s, start_rgb=GRADIENT_START, end_rgb=GRADIENT_END):
    text = Text()
    total = max(len(s) - 1, 1)
    for i, ch in enumerate(s):
        r, g, b = _lerp_color(start_rgb, end_rgb, i / total)
        text.append(ch, style=f"bold #{r:02x}{g:02x}{b:02x}")
    return text


def show_banner():
    width = _card_width()
    banner = gradient_text("Tar Valon Library Scraper")

    console.print()
    try:
        console.print(
            Panel(
                Align.center(banner),
                box=BOX_PANEL,
                border_style="border",
                padding=(1, 4),
                width=width,
            ),
            justify="center",
        )
    except UnicodeEncodeError:
        console.print("=" * min(console.size.width, 60))
        console.print(Align.center(Text("Tar Valon Library Scraper", style="title")))
        console.print("=" * min(console.size.width, 60))
    console.print()


def success_panel(message):
    width = _card_width()
    console.print()
    console.print(
        Panel(
            Align.center(Text(message, style="success")),
            box=BOX_SUCCESS,
            border_style="success",
            padding=(1, 6),
            width=width,
        ),
        justify="center",
    )


def build_menu_table(items, title):
    table = Table(
        box=BOX_TABLE,
        border_style="border",
        title=title,
        title_style="title",
        header_style="bold",
        pad_edge=False,
        min_width=40,
    )

    table.add_column("No.", justify="right", style="index", width=4, no_wrap=True)
    table.add_column("Name", style="item")

    for i, item in enumerate(items):
        table.add_row(str(i), item)

    return table


def show_menu(items, title):
    console.print()
    console.print(Rule(style="border", characters=RULE_CHAR))
    console.print()
    table = build_menu_table(items, title)
    console.print(table, justify="center")


def prompt_choice(count):
    return IntPrompt.ask(
        "\n[prompt]Choose[/prompt]",
        choices=[str(i) for i in range(count)],
        show_choices=False,
    )


def choose_from_dict(data, title):
    names = list(data.keys())
    show_menu(names, title)
    choice = prompt_choice(len(names))
    name = names[int(choice)]
    return name, data[name]


def choose_option(options, title):
    show_menu(options, title)
    choice = prompt_choice(len(options))
    return options[int(choice)]


def scrape_chapter(chapter_name, chapter_url):
    return content_scrape(chapter_url)


def save_file(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    show_banner()

    books = book_scrape(BOOK_URL)

    book_name, book_url = choose_from_dict(books, "Choose Book")
    console.print(f"\nSelected: [bold gold1]{book_name}[/bold gold1]\n")

    mode = choose_option(["Single Chapter", "Complete Book"], "Output Type")

    if mode == "Single Chapter":
        chapters = list_scrape(book_url)

        chapter_name, chapter_url = choose_from_dict(chapters, "Choose Chapter")

        content = scrape_chapter(chapter_name, chapter_url)

        filename = chapter_name.replace(" ", "_") + ".md"
        save_file(filename, content)

        success_panel(f"Saved {filename}")

    else:
        output = choose_option(["Markdown (.md)", "EPUB (.epub)"], "Book Format")

        book_content = scrape_book(book_name, book_url)

        md_filename = book_name.replace(" ", "_") + ".md"
        save_file(md_filename, book_content)

        if output == "Markdown (.md)":
            success_panel(f"Saved {md_filename}")
        else:
            epub_filename = book_name.replace(" ", "_") + ".epub"
            make_epub(md_filename, epub_filename, book_name)
            success_panel(f"Saved {epub_filename}")

    console.print()


if __name__ == "__main__":
    main()