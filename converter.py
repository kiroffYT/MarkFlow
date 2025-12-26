import sys
import os
import json
import re
from typing import Dict, Any

import markdown
from airium import Airium

DEFAULT_THEME: Dict[str, str] = {
    "bg": "#002b36",
    "text": "#839496",
    "accent": "#2aa198",
    "code_bg": "#073642",
    "border": "#586e75",
    "quote_bar": "#2aa198",
    "table_header": "#073642"
}

def load_themes() -> Dict[str, Any]:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'themes.json')
    
    if not os.path.exists(json_path):
        return {"default": DEFAULT_THEME}
        
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data: Dict[str, Any] = json.load(f)
            return data
    except (json.JSONDecodeError, IOError, PermissionError):
        return {"default": DEFAULT_THEME}

def create_html(md_content: str, theme_data: Dict[str, str]) -> str:
    html_body = markdown.markdown(md_content, extensions=[
        'extra', 'sane_lists', 'wikilinks', 'nl2br'
    ])
    
    a = Airium()
    a('<!DOCTYPE html>')
    with a.html(lang="ru"):
        with a.head():
            a.meta(charset="utf-8")
            a.title(_t="MarkFlow Document")
            with a.style():
                a(f"""
                    body {{
                        background-color: {theme_data.get('bg', '#fff')};
                        color: {theme_data.get('text', '#000')};
                        font-family: 'Segoe UI', system-ui, sans-serif;
                        line-height: 1.6; padding: 50px;
                        max-width: 900px; margin: 0 auto;
                    }}
                    h1, h2, h3, h4, h5, h6 {{ color: {theme_data.get('accent', 'blue')}; }}
                    a, .wikilink {{ 
                        color: {theme_data.get('accent', 'blue')}; 
                        text-decoration: none; border-bottom: 1px solid; 
                    }}
                    hr {{ border: 0; border-top: 2px solid {theme_data.get('border', '#ccc')}; margin: 40px 0; }}
                    blockquote {{
                        border-left: 5px solid {theme_data.get('quote_bar', 'grey')};
                        padding-left: 20px; margin: 20px 0;
                        font-style: italic; opacity: 0.9;
                    }}
                    code {{
                        background: {theme_data.get('code_bg', '#eee')};
                        padding: 3px 6px; border-radius: 4px; font-family: monospace;
                    }}
                    pre {{
                        background: {theme_data.get('code_bg', '#eee')};
                        padding: 20px; border-radius: 10px; overflow-x: auto;
                    }}
                    table {{ border-collapse: collapse; width: 100%; margin: 25px 0; }}
                    th, td {{
                        border: 1px solid {theme_data.get('border', '#ccc')};
                        padding: 12px; text-align: left;
                    }}
                    th {{ background: {theme_data.get('table_header', '#ddd')}; }}
                    img {{ max-width: 100%; border-radius: 8px; }}
                """)
        
        with a.body():
            with a.article():
                a(html_body)

    return str(a)

def main() -> None:
    if len(sys.argv) < 4:
        print("Usage: converter.py <input.md> <output.html> <theme_name>")
        return

    input_file, output_file, theme_name = sys.argv[1:4]

    try:
        themes = load_themes()
        theme_data = themes.get(theme_name, next(iter(themes.values()), DEFAULT_THEME))

        if not os.path.exists(input_file):
            print(f"Error: {input_file} not found.")
            return

        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()

        text = re.sub(r'\+\+(.*?)\+\+', r'<ins>\1</ins>', text)

        result = create_html(text, theme_data)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
            
        print(f"Success! Theme: {theme_name}")

    except (IOError, OSError) as e:
        print(f"File system error: {e}")
    except RuntimeError as e:
        print(f"Runtime error: {e}")

if __name__ == "__main__":
    main()
