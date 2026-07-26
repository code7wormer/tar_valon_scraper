from books_scraper import book_scrape
from chap_list_scraper import list_scrape
from content_scraper import content_scrape

from rich.console import Console
from rich.table import Table
from rich.prompt import IntPrompt
from rich.progress import track


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
        "Select",
        choices=[str(i) for i in range(1, len(names) + 1)]
    )

    selected_name = names[int(choice) - 1]

    return selected_name, data[selected_name]


def save_markdown(filename, text):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)


def main():

    console.print("[bold green]Tar Valon Library Scraper[/bold green]\n")

    # Get books
    books = book_scrape(BOOK_URL)

    book_name, book_url = choose_from_dict(
        books,
        "Choose Book"
    )

    console.print(
        f"\n[cyan]Selected:[/cyan] {book_name}\n"
    )


    # Get chapters
    chapters = list_scrape(book_url)

    chapter_name, chapter_url = choose_from_dict(
        chapters,
        "Choose Chapter"
    )

    console.print(
        f"\n[cyan]Scraping:[/cyan] {chapter_name}\n"
    )


    # Scrape chapter
    content = content_scrape(chapter_url)


    # Save
    filename = chapter_name.replace(" ", "_") + ".md"

    save_markdown(
        filename,
        content
    )

    console.print(
        f"[bold green]Saved:[/bold green] {filename}"
    )


if __name__ == "__main__":
    main()