from tarvalon_scraper.books_scraper import book_scrape
from tarvalon_scraper.chap_list_scraper import list_scrape
from tarvalon_scraper.content_scraper import content_scrape

from rich.console import Console
from rich.table import Table
from rich.prompt import IntPrompt
from rich.progress import track

from concurrent.futures import ThreadPoolExecutor, as_completed

from ebooklib import epub
import markdown

console = Console()

BOOK_URL = "https://library.tarvalon.net/index.php?title=Chapter_Summaries"


def show_menu(items, title):
    table = Table(title=title)

    table.add_column("No.", justify="center")
    table.add_column("Name")

    for i, item in enumerate(items):
        table.add_row(str(i), item)

    console.print(table)


def choose_from_dict(data, title):

    names = list(data.keys())

    show_menu(names, title)

    choice = IntPrompt.ask(
        "Choose",
        choices=[str(i) for i in range(len(names))]
    )

    name = names[int(choice)]

    return name, data[name]

def choose_option(options, title):

    show_menu(options, title)

    choice = IntPrompt.ask(
        "Choose",
        choices=[str(i) for i in range(len(options))]
    )

    return options[int(choice)]


def scrape_book(book_name, book_url):

    chapters = list_scrape(book_url)

    console.print(
        f"\n[cyan]{len(chapters)} chapters found[/cyan]\n"
    )

    results = {}

    with ThreadPoolExecutor(max_workers=5) as executor:

        futures = {
            executor.submit(content_scrape, url): chapter_name
            for chapter_name, url in chapters.items()
        }

        for future in track(
            as_completed(futures),
            total=len(futures),
            description="Scraping chapters..."
        ):

            chapter_name = futures[future]

            try:
                results[chapter_name] = future.result()

            except Exception as e:
                console.print(
                    f"[red]Failed {chapter_name}: {e}[/red]"
                )


    book_text = f"# {book_name}\n\n"

    for chapter_name in chapters:
        if chapter_name in results:
            book_text += results[chapter_name]
            book_text += "\n\n---\n\n"

    return book_text


def scrape_chapter(chapter_name, chapter_url):
    return content_scrape(chapter_url)


def save_file(filename, content):

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
def make_epub(md_file, epub_file, title):

    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_content = markdown.markdown(
        md_content,
        extensions=["extra"]
    )

    book = epub.EpubBook()

    book.set_title(title)
    book.set_language("en")
    book.add_author("Robert Jordan")

    chapter = epub.EpubHtml(
        title=title,
        file_name="chapter.xhtml",
        lang="en"
    )

    chapter.content = html_content

    book.add_item(chapter)

    book.toc = (
        epub.Link(
            "chapter.xhtml",
            title,
            "chapter"
        ),
    )

    book.spine = [
        "nav",
        chapter
    ]

    book.add_item(
        epub.EpubNcx()
    )

    book.add_item(
        epub.EpubNav()
    )

    epub.write_epub(
        epub_file,
        book
    )


def main():

    console.print(
        "[bold cyan]Tar Valon Library Scraper[/bold cyan]\n"
    )

    books = book_scrape(BOOK_URL)

    book_name, book_url = choose_from_dict(
        books,
        "Choose Book"
    )

    console.print(
        f"\nSelected: [yellow]{book_name}[/yellow]\n"
    )


    mode = choose_option(
        [
            "Single Chapter",
            "Complete Book"
        ],
        "Output Type"
    )

    if mode == "Single Chapter":

        chapters = list_scrape(book_url)

        chapter_name, chapter_url = choose_from_dict(
            chapters,
            "Choose Chapter"
        )

        content = scrape_chapter(
            chapter_name,
            chapter_url
        )

        filename = chapter_name.replace(" ", "_") + ".md"

        save_file(
            filename,
            content
        )

        console.print(
            f"[green]Saved {filename}[/green]"
        )
    else:

        output = choose_option(
            [
                "Markdown (.md)",
                "EPUB (.epub)"
            ],
            "Book Format"
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


        if output == "Markdown (.md)":

            console.print(
                f"[green]Saved {md_filename}[/green]"
            )


        else:

            epub_filename = book_name.replace(" ", "_") + ".epub"

            make_epub(
                md_filename,
                epub_filename,
                book_name
            )

            console.print(
                f"[green]Saved {epub_filename}[/green]"
            )


if __name__ == "__main__":
    main()