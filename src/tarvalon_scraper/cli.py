from tarvalon_scraper.books_scraper import book_scrape
from tarvalon_scraper.chap_list_scraper import list_scrape
from tarvalon_scraper.content_scraper import content_scrape
from tarvalon_scraper.exporter import make_epub
from tarvalon_scraper.book_compiler import scrape_book
from rich.console import Console
from rich.table import Table
from rich.prompt import IntPrompt

from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.align import Align
from rich.rule import Rule

console = Console()



BOOK_URL = "https://library.tarvalon.net/index.php?title=Chapter_Summaries"

BANNER_ART = r"""
 [bold cyan]████████╗ █████╗ ██████╗ ██╗   ██╗ █████╗ ██╗      ██████╗ ███╗   ██╗[/bold cyan]
 [bold bright_blue]╚══██╔══╝██╔══██╗██╔══██╗██║   ██║██╔══██╗██║     ██╔═══██╗████╗  ██║[/bold bright_blue]
    [bold blue]██║   ███████║██████╔╝██║   ██║███████║██║     ██║   ██║██╔██╗ ██║[/bold blue]
    [bold magenta]██║   ██╔══██║██╔══██╗╚██╗ ██╔╝██╔══██║██║     ██║   ██║██║╚██╗██║[/bold magenta]
    [bold bright_magenta]██║   ██║  ██║██║  ██║ ╚████╔╝ ██║  ██║███████╗╚██████╔╝██║ ╚████║[/bold bright_magenta]
    [bold violet]╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝[/bold violet]
"""

def print_header():
    banner = Text.from_markup(BANNER_ART)
    subtitle = Text("✦ TAR VALON ARCHIVES • THE WHEEL OF TIME SCRAPER ✦\n", style="bold yellow")
    badges = Text.from_markup("[bold black on bright_cyan] VERSION 0.1.6 [/bold black on bright_cyan]  [bold white on magenta] LIBRARY SCRAPER [/bold white on magenta]  [bold black on bright_green] ONLINE [/bold black on bright_green]")
    
    header_content = Align.center(
        Text.assemble(banner, "\n", subtitle, badges)
    )
    
    console.print()
    console.print(
        Panel(
            header_content,
            box=box.DOUBLE_EDGE,
            border_style="bright_magenta",
            padding=(1, 2)
        )
    )
    console.print()


def show_menu(items, title):
    table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        box=box.ROUNDED,
        border_style="bright_blue",
        expand=True,
        pad_edge=True
    )

    table.add_column("INDEX", justify="center", style="bold yellow", width=10)
    table.add_column("TITLE / NAME", style="bold white")

    for i, item in enumerate(items):
        idx_badge = f"[bold cyan]❯ [{i:02d}][/bold cyan]"
        table.add_row(idx_badge, item)

    panel = Panel(
        table,
        title=f"[bold bright_yellow]✦ {title.upper()} ✦[/bold bright_yellow]",
        title_align="center",
        subtitle="[dim cyan]Type option index & press Enter[/dim cyan]",
        subtitle_align="center",
        border_style="bold magenta",
        box=box.ROUNDED,
        padding=(1, 2)
    )

    console.print(panel)


def choose_from_dict(data, title):

    names = list(data.keys())

    show_menu(names, title)

    choice = IntPrompt.ask(
        "\n[bold bright_yellow]❯[/bold bright_yellow] [bold bright_white]Select Choice Index[/bold bright_white]",
        choices=[str(i) for i in range(len(names))],
        show_choices=False
    )

    name = names[int(choice)]

    return name, data[name]

def choose_option(options, title):

    show_menu(options, title)

    choice = IntPrompt.ask(
        "\n[bold bright_yellow]❯[/bold bright_yellow] [bold bright_white]Select Option Index[/bold bright_white]",
        choices=[str(i) for i in range(len(options))],
        show_choices=False
    )

    return options[int(choice)]


def scrape_chapter(chapter_name, chapter_url):
    with console.status("[bold cyan]Scraping chapter content from Tar Valon...[/bold cyan]", spinner="dots12"):
        return content_scrape(chapter_url)


def save_file(filename, content):

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    print_header()

    with console.status("[bold cyan]Fetching library catalog from Tar Valon...[/bold cyan]", spinner="dots12"):
        books = book_scrape(BOOK_URL)

    book_name, book_url = choose_from_dict(
        books,
        "Select Target Book"
    )

    console.print(
        Panel(
            f"[bold white]Active Selection:[/bold white] [bold bright_yellow]{book_name}[/bold bright_yellow]",
            border_style="bright_green",
            box=box.ROUNDED,
            expand=False
        )
    )
    console.print()

    mode = choose_option(
        [
            "Single Chapter",
            "Complete Book"
        ],
        "Output Mode"
    )

    if mode == "Single Chapter":
        with console.status("[bold cyan]Fetching chapter list from Tar Valon...[/bold cyan]", spinner="dots12"):
            chapters = list_scrape(book_url)

        chapter_name, chapter_url = choose_from_dict(
            chapters,
            "Select Chapter"
        )

        content = scrape_chapter(
            chapter_name,
            chapter_url
        )

        filename = chapter_name.replace(":", "").replace("/", "-").replace(" ", "_") + ".md"

        save_file(
            filename,
            content
        )

        console.print()
        console.print(
            Panel(
                f"[bold bright_green]✔ CHAPTER SCRAPED SUCCESSFULLY![/bold bright_green]\n\n"
                f"[bold white]Saved to:[/bold white] [bold bright_cyan]{filename}[/bold bright_cyan]",
                title="[bold bright_green]✦ SUCCESS ✦[/bold bright_green]",
                title_align="center",
                border_style="bright_green",
                box=box.ROUNDED,
                expand=False
            )
        )
    else:

        output = choose_option(
            [
                "Markdown (.md)",
                "EPUB (.epub)"
            ],
            "Select Book Format"
        )

        book_content = scrape_book(
            book_name,
            book_url
        )

        md_filename = book_name.replace(" ", "_") + ".md"

        save_file(
            md_filename,
            book_content
        )

        console.print()
        if output == "Markdown (.md)":

            console.print(
                Panel(
                    f"[bold bright_green]✔ COMPLETE BOOK SCRAPED SUCCESSFULLY![/bold bright_green]\n\n"
                    f"[bold white]Saved to:[/bold white] [bold bright_cyan]{md_filename}[/bold bright_cyan]",
                    title="[bold bright_green]✦ SUCCESS ✦[/bold bright_green]",
                    title_align="center",
                    border_style="bright_green",
                    box=box.ROUNDED,
                    expand=False
                )
            )

        else:

            epub_filename = book_name.replace(" ", "_") + ".epub"

            with console.status("[bold cyan]Compiling EPUB book archive...[/bold cyan]", spinner="dots12"):
                make_epub(
                    md_filename,
                    epub_filename,
                    book_name
                )

            console.print(
                Panel(
                    f"[bold bright_green]✔ EPUB GENERATED SUCCESSFULLY![/bold bright_green]\n\n"
                    f"[bold white]Saved to:[/bold white] [bold bright_cyan]{epub_filename}[/bold bright_cyan]",
                    title="[bold bright_green]✦ SUCCESS ✦[/bold bright_green]",
                    title_align="center",
                    border_style="bright_green",
                    box=box.ROUNDED,
                    expand=False
                )
            )


if __name__ == "__main__":
    main()
