from books_scraper import book_scrape
from chap_list_scraper import list_scrape
from content_scraper import content_scrape

from rich.console import Console
from rich.table import Table
from rich.prompt import IntPrompt
from rich.progress import track

from concurrent.futures import ThreadPoolExecutor, as_completed


console = Console()

BOOK_URL = "https://library.tarvalon.net/index.php?title=Chapter_Summaries"


def show_menu(items, title):
    table = Table(title=title)

    table.add_column("No.", justify="center")
    table.add_column("Name")

    for i, item in enumerate(items, start=1):
        table.add_row(str(i), item)

    console.print(table)


def choose_from_dict(data, title):
    names = list(data.keys())

    show_menu(names, title)

    choice = IntPrompt.ask(
        "Choose",
        choices=[str(i) for i in range(1, len(names) + 1)]
    )

    name = names[int(choice) - 1]

    return name, data[name]


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


def save_file(filename, content):

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


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



    book_content = scrape_book(
        book_name,
        book_url
    )


    filename = book_name.replace(" ", "_") + ".md"

    save_file(
        filename,
        book_content
    )


    console.print(
        f"\n[bold green]Saved {filename}[/bold green]"
    )


if __name__ == "__main__":
    main()