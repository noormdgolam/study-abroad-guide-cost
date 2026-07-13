import os
import json
import shutil
from datetime import datetime
from email.utils import format_datetime
import markdown
import frontmatter
from jinja2 import Environment, FileSystemLoader

# Paths
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SRC_DIR, '..'))
TEMPLATES_DIR = os.path.join(SRC_DIR, 'templates')
ASSETS_DIR = os.path.join(SRC_DIR, 'assets')
DATA_DIR = os.path.join(SRC_DIR, 'data')
CONTENT_ARTICLES_DIR = os.path.join(SRC_DIR, 'content', 'articles')
CONTENT_PAGES_DIR = os.path.join(SRC_DIR, 'content', 'pages')

# Setup Jinja2
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# Markdown parser with extensions
md = markdown.Markdown(extensions=['toc', 'tables', 'fenced_code', 'meta'])

# Load Site Config
with open(os.path.join(DATA_DIR, 'site.json'), 'r', encoding='utf-8') as f:
    site_config = json.load(f)

def parse_markdown_files(directory, content_type='article'):
    items = []
    if not os.path.exists(directory): return items
    
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                
                # Convert markdown to html
                md.reset()
                html_content = md.convert(post.content)
                toc = md.toc if hasattr(md, 'toc') else ''
                
                item = {
                    'title': post.get('title', ''),
                    'slug': post.get('slug', filename[:-3]),
                    'date': post.get('date', datetime.now().strftime('%Y-%m-%d')),
                    'author': post.get('author', site_config['author']),
                    'category': post.get('category', ''),
                    'is_pillar': post.get('is_pillar', False),
                    'key_takeaways': post.get('key_takeaways', []),
                    'content': html_content,
                    'toc': toc,
                    'type': content_type,
                    'excerpt': post.get('excerpt', post.content[:150] + '...'),
                    'url': f"/{post.get('slug', filename[:-3])}/" if content_type == 'article' else f"/{post.get('slug', filename[:-3])}/"
                }
                # Handle root pages like about, contact, etc.
                if content_type == 'page':
                    item['url'] = f"/{item['slug']}/"
                items.append(item)
    
    # Sort items by date descending
    items.sort(key=lambda x: x['date'], reverse=True)
    return items

def build_site():
    print("Starting build...")
    
    # Parse content
    articles = parse_markdown_files(CONTENT_ARTICLES_DIR, 'article')
    pages = parse_markdown_files(CONTENT_PAGES_DIR, 'page')
    
    # Group articles by category
    categories_dict = {cat['id']: {'name': cat['name'], 'articles': []} for cat in site_config.get('categories', [])}
    for article in articles:
        cat_id = article.get('category')
        if cat_id in categories_dict:
            categories_dict[cat_id]['articles'].append(article)
            
    # Copy Assets
    print("Copying assets...")
    dest_assets = os.path.join(ROOT_DIR, 'assets')
    if os.path.exists(dest_assets):
        shutil.rmtree(dest_assets)
    if os.path.exists(ASSETS_DIR):
        shutil.copytree(ASSETS_DIR, dest_assets)
        
    # Also copy sw.js and manifest.json to root if they exist in assets
    for file in ['sw.js', 'manifest.json', 'robots.txt']:
        src_file = os.path.join(ASSETS_DIR, file)
        if os.path.exists(src_file):
            shutil.copy2(src_file, os.path.join(ROOT_DIR, file))

    # Helper function to write HTML
    def write_html(path_parts, html):
        target_dir = os.path.join(ROOT_DIR, *path_parts[:-1])
        os.makedirs(target_dir, exist_ok=True)
        target_file = os.path.join(target_dir, path_parts[-1])
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(html)

    # 1. Render Homepage
    print("Rendering homepage...")
    template = env.get_template('index.html')
    html = template.render(site=site_config, articles=articles[:10], categories=categories_dict)
    write_html(['index.html'], html)

    # 2. Render Articles
    print(f"Rendering {len(articles)} articles...")
    template = env.get_template('article.html')
    for article in articles:
        # Get related articles from the same category
        related = [a for a in articles if a['category'] == article['category'] and a['slug'] != article['slug']][:3]
        html = template.render(site=site_config, article=article, related_articles=related)
        write_html([article['slug'], 'index.html'], html)
        
    # 3. Render Pages
    print(f"Rendering {len(pages)} pages...")
    template = env.get_template('page.html')
    for page in pages:
        html = template.render(site=site_config, page=page)
        write_html([page['slug'], 'index.html'], html)

    # 4. Render Search Results Page
    print("Rendering search page...")
    template = env.get_template('search.html')
    html = template.render(site=site_config)
    write_html(['search', 'index.html'], html)

    # 5. Generate Search Index (JSON)
    print("Generating search index...")
    search_index = []
    for a in articles:
        search_index.append({
            'title': a['title'],
            'url': a['url'],
            'excerpt': a['excerpt'],
            'category': a['category']
        })
    with open(os.path.join(ROOT_DIR, 'search_index.json'), 'w', encoding='utf-8') as f:
        json.dump(search_index, f)

    # 6. Generate Sitemap
    print("Generating sitemap.xml...")
    urls = [{'loc': f"{site_config['url']}/", 'lastmod': datetime.now().strftime('%Y-%m-%d'), 'priority': '1.0'}]
    for a in articles:
        urls.append({'loc': f"{site_config['url']}{a['url']}", 'lastmod': a['date'], 'priority': '0.8'})
    for p in pages:
        urls.append({'loc': f"{site_config['url']}{p['url']}", 'lastmod': datetime.now().strftime('%Y-%m-%d'), 'priority': '0.5'})
    
    sitemap_template = env.get_template('sitemap.xml')
    sitemap_xml = sitemap_template.render(urls=urls)
    write_html(['sitemap.xml'], sitemap_xml)

    # 7. Generate RSS
    print("Generating rss.xml...")
    rss_template = env.get_template('rss.xml')
    # Use rfc-822 format for RSS dates
    for a in articles:
        dt = datetime.strptime(a['date'], '%Y-%m-%d')
        a['pubDate'] = format_datetime(dt)
    
    rss_xml = rss_template.render(site=site_config, articles=articles[:50], lastBuildDate=format_datetime(datetime.now()))
    write_html(['rss.xml'], rss_xml)

    print("Build complete!")

if __name__ == '__main__':
    build_site()
