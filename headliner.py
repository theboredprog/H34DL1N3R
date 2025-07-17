import feedparser
import argparse
from rich.console import Console
from rich.table import Table

RSS_FEEDS = {
    # UK
    "bbc": ("BBC News (UK)", "http://feeds.bbci.co.uk/news/rss.xml"),

    # USA - Left, Center, Right spectrum
    "nyt": ("New York Times (US, Center-Left)", "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"),
    "fox": ("Fox News (US, Right)", "http://feeds.foxnews.com/foxnews/latest"),
    "breitbart": ("Breitbart (US, Right)", "http://feeds.feedburner.com/breitbart"),
    "npr": ("NPR (US, Center)", "https://www.npr.org/rss/rss.php?id=1001"),

    # Italy - Various leanings
    "ansa": ("ANSA (Italy, Center)", "https://www.ansa.it/sito/ansait_rss.xml"),
    "corriere": ("Corriere della Sera (Italy, Center-Right)", "https://xml2.corriereobjects.it/rss/homepage.xml"),
    "repubblica": ("La Repubblica (Italy, Center-Left)", "https://www.repubblica.it/rss/homepage/rss2.0.xml"),
    "la_stampa": ("La Stampa (Italy, Center)", "https://www.lastampa.it/rss/homepage.xml"),
    "tgcom24": ("TGCom24 (Italy, Center-Right)", "https://www.tgcom24.mediaset.it/rss/homepage.xml"),
}

def get_headlines_from_feeds(selected_sources, count):
    console = Console()
    for key in selected_sources:
        if key not in RSS_FEEDS:
            console.print(f"[red]Unknown source '{key}' skipped.[/red]")
            continue

        name, url = RSS_FEEDS[key]
        feed = feedparser.parse(url)

        table = Table(title=f"{name} - Top {count} Headlines")
        table.add_column("No.", justify="right")
        table.add_column("Title", style="bold cyan")
        table.add_column("Published", style="dim")
        table.add_column("Link", style="blue underline")

        for i, entry in enumerate(feed.entries[:count], 1):
            published = entry.get('published', 'N/A')
            table.add_row(str(i), entry.title, published, entry.link)

        console.print(table)
        console.print("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="News headline scraper.")
    parser.add_argument(
        "--source", "-s", nargs="+", default=list(RSS_FEEDS.keys()),
        help="Specify news source keys to scrape (default: all). "
             "Available: " + ", ".join(RSS_FEEDS.keys())
    )
    parser.add_argument(
        "--count", "-c", type=int, default=5,
        help="Number of headlines to fetch per source (default: 5)"
    )
    args = parser.parse_args()
    get_headlines_from_feeds(args.source, args.count)
