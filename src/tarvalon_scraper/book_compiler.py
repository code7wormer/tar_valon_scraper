from tarvalon_scraper.chap_list_scraper import list_scrape
from tarvalon_scraper.content_scraper import content_scrape
from rich.console import Console
from rich.progress import track

from concurrent.futures import ThreadPoolExecutor, as_completed
console = Console()
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
