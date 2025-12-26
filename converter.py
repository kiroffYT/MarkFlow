import sys
import os
import json
import re
import markdown
from airium import Airium

def load_themes():
    with open('themes.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def create_html(md_content, theme_data):
    html_body = markdown.markdown(md_content, extensions=[
        'extra', 'sane_lists', 'wikilinks', 'nl2br'
    ])
    
    a = Airium()
    a('<!DOCTYPE html>')
    with a.html(lang="ru"):
        with a.head():
            a.meta(charset="utf-8")
            a.title(_t="Converted Document")
            with a.style():
                a(f"""
                    body {{
                        background-color: {theme_data['bg']};
                        color: {theme_data['text']};
                        font-family: 'Segoe UI', system-ui, sans-serif;
                        line-height: 1.6; padding: 50px;
                        max-width: 900px; margin: 0 auto;
                    }}
                    h1, h2, h3, h4, h5, h6 {{ color: {theme_data['accent']}; }}
                    a, .wikilink {{ 
                        color: {theme_data['accent']}; 
                        text-decoration: none; 
                        border-bottom: 1px solid; 
                    }}
                    hr {{ border: 0; border-top: 2px solid {theme_data['border']}; margin: 40px 0; }}
                    blockquote {{
                        border-left: 5px solid {theme_data['quote_bar']};
                        padding-left: 20px; margin: 20px 0;
                        font-style: italic; opacity: 0.9;
                    }}
                    code {{
                        background: {theme_data['code_bg']};
                        padding: 3px 6px; border-radius: 4px;
                        font-family: monospace;
                    }}
                    pre {{
                        background: {theme_data['code_bg']};
                        padding: 20px; border-radius: 10px;
                        overflow-x: auto;
                    }}
                    table {{
                        border-collapse: collapse; width: 100%; margin: 25px 0;
                    }}
                    th, td {{
                        border: 1px solid {theme_data['border']};
                        padding: 12px; text-align: left;
                    }}
                    th {{ background: {theme_data['table_header']}; }}
                    img {{ max-width: 100%; border-radius: 8px; }}
                    ins {{ text-decoration: underline; }}
                    del {{ opacity: 0.6; }}
                """)
        
        with a.body():
            with a.article():
                a(html_body)

    return str(a)

def main():
    if len(sys.argv) < 4:
        print("Usage: converter.py <input.md> <output.html> <theme_name>")
        return

    input_file, output_file, theme_name = sys.argv[1:4]

    try:
        themes = load_themes()
        theme_data = themes.get(theme_name, list(themes.values())[0])

        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()

        text = re.sub(r'\+\+(.*?)\+\+', r'<ins>\1</ins>', text)

        result = create_html(text, theme_data)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"created, theme: {theme_name}")

    except Exception as e:
        print(f"error: {e}")

if __name__ == "__main__":
    main()