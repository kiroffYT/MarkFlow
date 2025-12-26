# MarkFlow - Markdown converter

**MarkFlow** allows you to transform MD files into beautiful, readable HTML pages. The emphasis is on the readability of the resulting page.
## Features

🎨 **More than 30 design themes**
  - Classic (`dark-red`, `yellow`, `light-green`)  
  - Special (`matrix`)

📑 **Expanded Markdown support**
  - Support for Obsidian/Notion style links  
  - Support for tables, quotes, lists and all heading levels  
## Installation

1. Clone the repository (or download the files manually)

```
git clone https://github.com/kiroffYT/MarkFlow.git
cd MarkFlow
```

2. Install dependencies via **pip**

```
pip install markdown airium
```
## Usage

```python
python converter.py "note.md" "converted.html" dark-purple
```

`note.md` - the original Markdown file to be converted  
`converted.html` - the name of the HTML file to be saved  
`dark-purple` - color theme for an HTML page

