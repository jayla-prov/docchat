# Docchat

A command-line chatbot that answers questions about local documents using Groq. It can list files, read text, search files, calculate expressions, and remember the conversation.

## Cat Website

Run from the docchat repository root:

```text
cd test_projects/lab-homepage
chat
chat> /ls .
README.md
cat.jpg
cat1.JPG
cat2.jpeg
cat3.JPG
facts.html
index.html
pictures.html
style.css
submission.toml
chat> Read the HTML files in this folder. What is this website about, and what pages does it have?
```

Actual response excerpt:
> The site’s a lil’ showcase of why the author be lovin’ cats, a stash of cat facts, and a gallery of pictures.

I learned that the website has separate home, facts, and pictures pages.

## Markdown Compiler

Run from the docchat repository root:

```text
cd test_projects/markdown-compiler
chat
chat> /ls .
README.md
example
markdown_compiler
pyproject.toml
requirements.txt
chat> /cat markdown_compiler/util/line_functions.py
```

After the file contents appeared:

```text
chat> Using only the code already shown in our conversation, explain how Markdown headings become HTML. Do not call any tools.
```

Actual response excerpt:
> Checking from the highest level first ensures that a line like `###### Header` won’t be mistaken for a smaller header.

I learned that the compiler counts heading markers from six down to one and creates the matching HTML heading tags.

## eBay Scraper

Run from the docchat repository root:

```text
cd test_projects/ebay-scraper
chat
chat> /ls .
README.md
ebay-dl.py
garden tools.csv
garden tools.json
golf clubs.csv
golf clubs.json
practice-pages
stuffed animal.csv
stuffed animal.json
submission.toml
chat> /cat ebay-dl.py
```

After the file contents appeared:

```text
chat> Using only the code already shown in our conversation, what information does this scraper collect from each eBay listing, and how does it save the results? Do not call any tools.
```

Actual response excerpts:
> If you run it with the `--csv` flag, it writes a CSV file named `<search‑term>.csv`.

> Without `--csv`, it writes a JSON file named `<search‑term>.json`.

I learned that the scraper collects six listing fields and saves the results as JSON or CSV.