import json
import requests
from parsel import Selector


def join_texts(texts: list[str]):
    return " ".join(text.strip() for text in texts if text.strip())


def parse_page(sel: Selector):
    data = dict()
    for h in sel.css("article"):
        article = h.css("div.dre-item__text")
        href = article.css("a::attr(href)").get("").strip()
        if not href:
            continue
        data[href] = {
            "title_lg": join_texts(
                article.css("div.dre-item__alt-title--lg ::text").getall()
            ),
            "title_md": join_texts(
                article.css("div.dre-item__alt-title--md ::text").getall()
            ),
            "title_sm": join_texts(
                article.css("div.dre-item__alt-title--sm ::text").getall()
            ),
            "pretitle": article.css("div.dre-item__pretitle::text").get("").strip(),
        }
    return data


def main():
    """main function"""

    html = requests.get("https://www.eb.dk").text
    sel = Selector(text=html)
    output = parse_page(sel)

    with open("eb.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
