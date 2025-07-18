import feedparser
import argparse
from rich.console import Console
from rich.table import Table
from deep_translator import GoogleTranslator

RSS_FEEDS = {
    # 🇬🇧 United Kingdom
    "bbc": ("BBC News (UK, Center)", "http://feeds.bbci.co.uk/news/rss.xml"),
    "telegraph": ("The Telegraph (UK, Right)", "https://www.telegraph.co.uk/rss.xml"),
    "daily_mail": ("Daily Mail (UK, Right)", "https://www.dailymail.co.uk/articles.rss"),
    "independent": ("The Independent (UK, Center)", "https://www.independent.co.uk/news/uk/rss"),
    "guardian": ("The Guardian (UK, Left)", "https://www.theguardian.com/world/rss"),
    "new_statesman": ("New Statesman (UK, Left)", "https://www.newstatesman.com/feed"),

    # 🇺🇸 United States
    "nyt": ("New York Times (US, Center-Left)", "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"),
    "fox": ("Fox News (US, Right)", "http://feeds.foxnews.com/foxnews/latest"),
    "breitbart": ("Breitbart (US, Right)", "http://feeds.feedburner.com/breitbart"),
    "npr": ("NPR (US, Center)", "https://www.npr.org/rss/rss.php?id=1001"),
    "wash_ex": ("Washington Examiner (US, Right)", "https://www.washingtonexaminer.com/rss"),
    "national_review": ("National Review (US, Right)", "https://www.nationalreview.com/feed/"),
    "mother_jones": ("Mother Jones (US, Left)", "https://www.motherjones.com/feed/"),
    "the_intercept": ("The Intercept (US, Left)", "https://theintercept.com/feed/?rss"),
    "msnbc": ("MSNBC (US, Left)", "https://www.msnbc.com/feeds/latest"),

    # 🇮🇹 Italy
    "ansa": ("ANSA (Italy, Center)", "https://www.ansa.it/sito/ansait_rss.xml"),
    "corriere": ("Corriere della Sera (Italy, Center-Right)", "https://xml2.corriereobjects.it/rss/homepage.xml"),
    "repubblica": ("La Repubblica (Italy, Center-Left)", "https://www.repubblica.it/rss/homepage/rss2.0.xml"),
    "la_stampa": ("La Stampa (Italy, Center)", "https://www.lastampa.it/rss/homepage.xml"),
    "tgcom24": ("TGCom24 (Italy, Center-Right)", "https://www.tgcom24.mediaset.it/rss/homepage.xml"),

    # 🇩🇪 Germany
    "dw": ("Deutsche Welle (Germany, Center)", "https://rss.dw.com/rdf/rss-en-all"),
    "faz": ("Frankfurter Allgemeine Zeitung - FAZ (Germany, Center)", "https://www.faz.net/rss/aktuell/"),

    # 🇫🇷 France
    "france24": ("France 24 (France, Center)", "https://www.france24.com/en/rss"),
    "le_monde": ("Le Monde (France, Center)", "https://www.lemonde.fr/rss/une.xml"),

    # 🇵🇱 Poland
    "tvn24": ("TVN24 (Poland, Center)", "https://tvn24.pl/najnowsze.xml"),
    "gazeta": ("Gazeta Wyborcza (Poland, Center-Left)", "https://wyborcza.pl/pub/rss/gazetawyborcza.xml"),

    # 🇭🇺 Hungary
    "hungary_today": ("Hungary Today (Hungary, Pro-Government)", "https://hungarytoday.hu/feed/"),

    # 🇨🇳 China (state-aligned)
    "xinhuanet": ("Xinhua News (China, State Media)", "http://www.xinhuanet.com/english/rss/worldrss.xml"),

    # 🇯🇵 Japan
    "japan_times": ("The Japan Times (Japan, Center)", "https://www.japantimes.co.jp/feed/"),
    "nhk": ("NHK World News (Japan, Center)", "https://www3.nhk.or.jp/rss/news/cat0.xml"),

    # 🇧🇷 Brazil
    "folha": ("Folha de S. Paulo (Brazil, Center-Left)", "https://feeds.folha.uol.com.br/emcimadahora/rss091.xml"),
    "globo": ("Globo (Brazil, Center)", "https://g1.globo.com/dynamo/rss2.xml"),

    # 🇦🇷 Argentina
    "clarin": ("Clarín (Argentina, Center-Right)", "https://www.clarin.com/rss/lo-ultimo/")
}

def translate_text(text, lang):
    try:
        return GoogleTranslator(source='auto', target=lang).translate(text)
    except Exception:
        return text  # fallback to original if translation fails

def get_headlines_from_feeds(selected_sources, count, lang=None):
    console = Console()
    for key in selected_sources:
        if key not in RSS_FEEDS:
            console.print(f"[red]Unknown source '{key}' skipped.[/red]")
            continue

        name, url = RSS_FEEDS[key]
        feed = feedparser.parse(url)

        table = Table(title=f"{name} - Top {count} Headlines ({lang or 'original'})")
        table.add_column("No.", justify="right")
        table.add_column("Title", style="bold cyan")
        table.add_column("Summary", style="white")
        table.add_column("Published", style="dim")

        for i, entry in enumerate(feed.entries[:count], 1):
            title = entry.get('title', 'N/A')
            summary = entry.get('summary', entry.get('description', 'No summary available'))[:300]

            if lang:
                title = translate_text(title, lang)
                summary = translate_text(summary, lang)

            published = entry.get('published', 'N/A')
            table.add_row(str(i), title, summary, published)
            table.add_row("", "", "", "")  # Empty row as separator

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

    parser.add_argument(
    "--lang", "-l", default=None,
    help="Translate results into specified language (e.g., 'it', 'es', 'fr')"
    )

    args = parser.parse_args()

    get_headlines_from_feeds(args.source, args.count, args.lang)
