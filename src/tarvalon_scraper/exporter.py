from ebooklib import epub
import markdown

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
