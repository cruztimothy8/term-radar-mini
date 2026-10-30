import requests
import re
from collections import Counter
from datetime import datetime, timedelta

SOURCES = {
    'github': 'https://github.com/trending?since=daily',
    'x': 'https://nitter.net/search?f=tweets&q=AI+model&since=2025-01-01',
    'sitemap': 'https://huggingface.co/sitemap.xml'
}

HEADERS = {'User-Agent': 'Mozilla/5.0'}

KEYWORDS = ['model', 'agent', 'mcp', 'api', 'llm', 'tool', 'dataset']

def fetch_text(url: str) -> str:
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f'Error fetching {url}: {e}')
        return ''

def extract_terms(text: str) -> list:
    # Crude extraction: find capitalized words or hyphenated terms near keywords
    terms = re.findall(r'\b[A-Z][a-z]*[-A-Za-z]*\b', text)
    filtered = []
    for term in terms:
        if len(term) > 2 and any(kw in term.lower() for kw in KEYWORDS):
            filtered.append(term)
    return filtered

def main():
    all_terms = []
    for name, url in SOURCES.items():
        text = fetch_text(url)
        terms = extract_terms(text)
        print(f'{name}: {len(terms)} potential terms')
        all_terms.extend(terms)
    
    # Count frequency as proxy for trending
    counter = Counter(all_terms)
    top = counter.most_common(10)
    
    print('\nTop 10 Terms Today:')
    for term, count in top:
        print(f'{term}: {count}')
    
    # Generate simple report file
    with open('radar_report.txt', 'w') as f:
        f.write(f'AI Term Radar - {datetime.now().date()}\n')
        f.write('='*30 + '\n')
        for term, count in top:
            f.write(f'{term}: {count} occurrences\n')
    print('Report saved to radar_report.txt')

if __name__ == '__main__':
    main()