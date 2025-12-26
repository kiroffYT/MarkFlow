# MarkFlow - Markdown converter

**MarkFlow** allows you to transform MD files into beautiful, readable HTML pages. The emphasis is on the readability of the resulting page.  

![Themes count: 1112](https://img.shields.io/badge/themes%20count-1112-orange)

![Made in Python](https://img.shields.io/badge/made_in-python-blue) ![With Airium library](https://img.shields.io/badge/with_library-airium-green) ![With JSON library](https://img.shields.io/badge/with_library-json-green) ![With Markdown library](https://img.shields.io/badge/with_library-markdown-green)
## Features

🎨 **More than 1000 design themes**
  - Classic (`dark-red`, `yellow`, `light-green`)  
  - Special (`matrix`)
  - HUE-based (`hue-60`, `dark-hue-120`, `light-hue-180`)

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

