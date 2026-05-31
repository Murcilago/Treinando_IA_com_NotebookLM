#!/usr/bin/env python3
"""
crawler.py — Consolida documentação multi-página em um único HTML auto-contido.

Uso:
    python tools/crawler.py <url> [--depth N] [--output FILE] [--delay S] [--allow-external] [--no-images]

Exemplos:
    python tools/crawler.py https://docs.delta.io/latest/index.html --depth 1
    python tools/crawler.py https://spark.apache.org/docs/latest/sql-programming-guide.html --depth 0
"""

import argparse
import base64
import time
from collections import deque
from urllib.parse import urljoin, urlparse, urldefrag

import requests
from bs4 import BeautifulSoup

# Seletores para área de conteúdo principal, em ordem de prioridade
CONTENT_SELECTORS = [
    'main',
    'article',
    '[role="main"]',
    '#content',
    '.content',
    '.documentation',
    '.doc-content',
    '.markdown-body',
    'body',
]

# Tags de navegação/UI que não são conteúdo
STRIP_TAGS = ['nav', 'footer', 'header', 'script', 'style', 'aside', 'form', 'iframe']


def fetch(url, session, timeout=10):
    try:
        r = session.get(url, timeout=timeout)
        r.raise_for_status()
        return r
    except Exception as e:
        print(f"  [erro] {url} — {e}")
        return None


def embed_images(content_tag, base_url, session):
    """Substitui src de imagens por base64 embutido. Fallback: texto com URL."""
    for img in content_tag.find_all('img'):
        src = img.get('src', '').strip()
        if not src or src.startswith('data:'):
            continue
        abs_src = urljoin(base_url, src)
        try:
            r = session.get(abs_src, timeout=5)
            if r.status_code == 200:
                ct = r.headers.get('content-type', 'image/png').split(';')[0]
                b64 = base64.b64encode(r.content).decode()
                img['src'] = f"data:{ct};base64,{b64}"
        except Exception:
            alt = img.get('alt', '')
            label = f"[Imagem: {alt} — {abs_src}]" if alt else f"[Imagem: {abs_src}]"
            img.replace_with(label)


def extract_content(soup, page_url, session, with_images):
    content = None
    for sel in CONTENT_SELECTORS:
        content = soup.select_one(sel)
        if content:
            break
    if not content:
        return ''

    for tag in content.find_all(STRIP_TAGS):
        tag.decompose()

    if with_images:
        embed_images(content, page_url, session)

    # Converte links relativos em absolutos
    for a in content.find_all('a', href=True):
        a['href'] = urljoin(page_url, a['href'])

    return str(content)


def crawl(start_url, max_depth, delay, same_domain, with_images, session):
    visited = set()
    pages = []
    queue = deque([(start_url, 0)])
    base_domain = urlparse(start_url).netloc

    while queue:
        url, depth = queue.popleft()
        url, _ = urldefrag(url)

        if url in visited:
            continue
        visited.add(url)

        print(f"  [depth {depth}] {url}")
        resp = fetch(url, session)
        if not resp:
            continue

        soup = BeautifulSoup(resp.text, 'html.parser')
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else url

        content = extract_content(soup, url, session, with_images)
        pages.append({'url': url, 'title': title, 'content': content, 'depth': depth})

        if depth < max_depth:
            for a in soup.find_all('a', href=True):
                href = urljoin(url, a['href'])
                href, _ = urldefrag(href)
                parsed = urlparse(href)
                if parsed.scheme not in ('http', 'https'):
                    continue
                if same_domain and parsed.netloc != base_domain:
                    continue
                if href not in visited:
                    queue.append((href, depth + 1))

        time.sleep(delay)

    return pages


def generate_html(pages, output_path):
    toc_items = '\n'.join(
        f'    <li><a href="#page-{i}">{p["title"]}</a>'
        f' <span class="src-url">— {p["url"]}</span></li>'
        for i, p in enumerate(pages)
    )

    sections = '\n'.join(f'''
<section id="page-{i}">
  <div class="page-header">
    <h2>{p["title"]}</h2>
    <p class="src-url">Fonte: <a href="{p["url"]}">{p["url"]}</a></p>
  </div>
  {p["content"]}
  <p class="back"><a href="#toc">↑ voltar ao índice</a></p>
  <hr>
</section>'''
    for i, p in enumerate(pages))

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Documentação Consolidada</title>
<style>
  body        {{ font-family: system-ui, sans-serif; max-width: 960px; margin: 0 auto; padding: 1.5rem; color: #222; line-height: 1.6; }}
  img         {{ max-width: 100%; height: auto; display: block; margin: 0.75rem 0; }}
  pre         {{ background: #f5f5f5; padding: 1rem; overflow-x: auto; border-radius: 4px; font-size: 0.88em; }}
  code        {{ background: #f5f5f5; padding: 0.15em 0.35em; border-radius: 3px; font-size: 0.9em; }}
  .page-header{{ background: #f0f4ff; padding: 1rem 1.25rem; border-left: 4px solid #3b6fd4; margin-bottom: 1.5rem; }}
  .page-header h2 {{ margin: 0 0 0.25rem; }}
  .src-url    {{ font-size: 0.8em; color: #777; margin: 0; }}
  .back       {{ font-size: 0.8em; text-align: right; margin-top: 1rem; }}
  hr          {{ border: none; border-top: 2px solid #eee; margin: 2.5rem 0; }}
  #toc        {{ background: #fafafa; padding: 1.5rem; border: 1px solid #ddd; border-radius: 6px; margin-bottom: 2rem; }}
  #toc h1     {{ margin-top: 0; }}
  #toc ol     {{ padding-left: 1.5rem; margin: 0; }}
  #toc li     {{ margin: 0.4rem 0; }}
</style>
</head>
<body>

<nav id="toc">
  <h1>Índice — {len(pages)} página(s) capturada(s)</h1>
  <ol>
{toc_items}
  </ol>
</nav>

{sections}

</body>
</html>"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    size_kb = len(html.encode('utf-8')) // 1024
    print(f"\nArquivo gerado : {output_path}")
    print(f"Páginas        : {len(pages)}")
    print(f"Tamanho        : {size_kb} KB")
    if size_kb > 10_000:
        print("Aviso          : arquivo grande (>10 MB). Considere --no-images ou menor profundidade.")
    print("\nDica: para gerar PDF, abra no Chrome → Ctrl+P → Salvar como PDF → sem margens.")


def main():
    parser = argparse.ArgumentParser(
        description='Consolida documentação multi-página em um único HTML auto-contido.'
    )
    parser.add_argument('url',
                        help='URL de partida')
    parser.add_argument('--depth', type=int, default=1,
                        help='Profundidade máxima de links (padrão: 1)')
    parser.add_argument('--delay', type=float, default=0.5,
                        help='Intervalo entre requisições em segundos (padrão: 0.5)')
    parser.add_argument('--output', default='docs_consolidado.html',
                        help='Arquivo de saída (padrão: docs_consolidado.html)')
    parser.add_argument('--allow-external', action='store_true',
                        help='Seguir links para outros domínios')
    parser.add_argument('--no-images', action='store_true',
                        help='Não embutir imagens (arquivo menor, sem conteúdo visual)')
    args = parser.parse_args()

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (compatible; doc-consolidator/1.0; educational use)'
    })

    print(f"URL inicial  : {args.url}")
    print(f"Profundidade : {args.depth}")
    print(f"Delay        : {args.delay}s")
    print(f"Imagens      : {'não' if args.no_images else 'sim (base64)'}")
    print(f"Domínio      : {'livre' if args.allow_external else 'restrito ao domínio de origem'}\n")

    pages = crawl(
        start_url=args.url,
        max_depth=args.depth,
        delay=args.delay,
        same_domain=not args.allow_external,
        with_images=not args.no_images,
        session=session,
    )

    if not pages:
        print("Nenhuma página capturada.")
        return

    generate_html(pages, args.output)


if __name__ == '__main__':
    main()
