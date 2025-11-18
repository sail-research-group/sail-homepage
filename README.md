# Lab Website (Jekyll + GitHub Pages)

This is a minimal, **GitHub Pages–compatible** Jekyll site for a research group/lab. 
It uses only plugins whitelisted by GitHub Pages (via the `github-pages` gem).

## Quick start (no local Ruby needed)
1. Create a **new GitHub repository** (public is easiest for Pages).
2. Upload/commit these files to the repo (or drag-and-drop the ZIP contents).
3. Go to **Settings → Pages** and choose:
   - Build from: **GitHub Actions** (recommended) *or* **Deploy from a branch**
   - Branch: `main` (root)  
   GitHub will publish at `https://<your-username>.github.io/<repo-name>/`.
4. Edit content directly on GitHub (Markdown files) or via PRs from students.

### Optional: Custom domain
- Add your domain under **Settings → Pages** (e.g., `lab.yourdomain.org`).
- Create a `CNAME` record in your DNS pointing to `<user>.github.io` or the project URL GitHub provides.

## Local preview (optional)
If you want to run the site locally:
```bash
# Install Ruby (3.x recommended) and Bundler, then:
bundle install
bundle exec jekyll serve
# Visit http://127.0.0.1:4000
```

## Content you’ll likely edit
- `index.md` – landing page
- `people.md` – generated from `_data/members.yml`
- `publications.md` – generated from `_data/publications.yml`
- `projects.md` – generated from `_data/projects.yml` (optional)
- `blog.md` + files in `_posts/` for news/updates
- `_data/` YAML files for structured content
- `assets/img/` for photos and logos
- `_config.yml` for site name, social links, Google Analytics ID, etc.

## Collaboration workflow
- Give students **Write** (or use forks/PRs).
- Protect `main` (Settings → Branches): require PR + 1 review.
- Students edit Markdown/YAML and open PRs; you review/merge.

## License
MIT (see `LICENSE`).
