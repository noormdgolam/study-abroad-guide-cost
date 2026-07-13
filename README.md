# Study Abroad Guide Cost Comparison

This is a blazing fast, SEO-optimized static website built with a custom Python static site generator. The generated site is fully PWA-ready, AdSense-optimized, and built to handle massive traffic spikes via CDN without any server rendering overhead.

## Architecture

- `_src/`: Contains the raw markdown content, JSON configuration, Jinja2 HTML templates, CSS/JS assets, and the python generator scripts.
- `/`: The root directory contains the compiled, deployment-ready static files.

**Important**: This project uses a root-deployment strategy for cPanel Git Version Control. Do not move the output files to a `dist/` or `public/` directory, as cPanel will serve the repository root directly.

## How to Add New Content

1. Create a new markdown file in `_src/content/articles/` (for blog posts) or `_src/content/pages/` (for static pages).
2. Add the required YAML frontmatter to the top of the file:
   ```yaml
   ---
   title: "Your Article Title"
   slug: "your-article-slug"
   category: "tuition"  # Must match a category ID in _src/data/site.json
   author: "Your Name"
   date: "YYYY-MM-DD"
   key_takeaways:
     - "Point 1"
     - "Point 2"
   ---
   Your markdown content goes here...
   ```
3. Run the generator script to compile the new content into static HTML:
   ```bash
   python _src/generate.py
   ```
4. Commit the new generated files and push to cPanel:
   ```bash
   git add .
   git commit -m "Added new article"
   git push origin main
   ```

## AdSense & Analytics

To enable Google AdSense and Analytics, open `_src/data/site.json` and replace the placeholder IDs:
- `"adsense_client_id": "ca-pub-XXXXXXXXXXXXXXXX"`
- `"ga_measurement_id": "G-XXXXXXXXXX"`

Then re-run `python _src/generate.py`.

The `_src/templates/base.html` and `_src/templates/article.html` files contain pre-configured ad slots for above-the-fold, mid-article, and end-of-article placements.

## Customizing Design

Edit `_src/assets/css/style.css` to update the CSS variables for the color palette, fonts, and spacing.
Edit `_src/templates/` to change the HTML structure.

## Deployment via cPanel

1. In your cPanel dashboard, go to **Git™ Version Control**.
2. Click **Create** and link it to your remote repository (e.g. GitHub/GitLab).
3. Set the repository path to your subdomain's document root (e.g., `public_html/study-abroad-guide-cost`).
4. Every time you push to the `main` branch, cPanel will automatically pull the changes and update the live site instantly. No `.cpanel.yml` file is required because the document root is serving the repository root directly.
