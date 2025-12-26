import sys
import os
import json
import re
import colorsys
from typing import Dict, Any, Tuple

import markdown
from airium import Airium

DEFAULT_THEME: Dict[str, str] = {
    "bg": "#1e1e1e", "text": "#d4d4d4", "accent": "#3794ff",
    "code_bg": "#2d2d2d", "border": "#454545", "quote_bar": "#3794ff",
    "table_header": "#2d2d2d"
}

def hex_to_rgb(hex_str: str) -> Tuple[float, float, float]:
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4)) # type: ignore

def rgb_to_hex(rgb: Tuple[float, float, float]) -> str:
    return '#%02x%02x%02x' % tuple(int(x * 255) for x in rgb)

def generate_dynamic_theme(hue: int, mode: str = "dark") -> Dict[str, str]:
    h = (hue % 360) / 360.0
    
    if mode == "light":
        bg = colorsys.hls_to_rgb(h, 0.97, 0.2)
        text = colorsys.hls_to_rgb(h, 0.2, 0.1)
        accent = colorsys.hls_to_rgb(h, 0.4, 0.8)
        code_bg = colorsys.hls_to_rgb(h, 0.92, 0.15)
    else: # dark
        bg = colorsys.hls_to_rgb(h, 0.07, 0.15)
        text = colorsys.hls_to_rgb(h, 0.85, 0.1)
        accent = colorsys.hls_to_rgb(h, 0.6, 0.7)
        code_bg = colorsys.hls_to_rgb(h, 0.12, 0.2)

    border = colorsys.hls_to_rgb(h, 0.3, 0.2)
    
    return {
        "bg": rgb_to_hex(bg),
        "text": rgb_to_hex(text),
        "accent": rgb_to_hex(accent),
        "code_bg": rgb_to_hex(code_bg),
        "border": rgb_to_hex(border),
        "quote_bar": rgb_to_hex(accent),
        "table_header": rgb_to_hex(code_bg)
    }

def load_theme(theme_name: str) -> Dict[str, str]:
    if "hue-" in theme_name:
        mode = "light" if "light" in theme_name else "dark"
        try:
            hue_val = int(re.findall(r'\d+', theme_name)[0])
            return generate_dynamic_theme(hue_val, mode)
        except (IndexError, ValueError):
            return DEFAULT_THEME

    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'themes.json')
    
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                themes = json.load(f)
                if theme_name in themes:
                    return themes[theme_name]
        except (json.JSONDecodeError, IOError):
            pass
            
    return DEFAULT_THEME

def create_html(md_content: str, theme_data: Dict[str, str]) -> str:
    html_body = markdown.markdown(md_content, extensions=['extra', 'sane_lists', 'wikilinks', 'nl2br'])
    a = Airium()
    a('<!DOCTYPE html>')
    with a.html(lang="ru"):
        with a.head():
            a.meta(charset="utf-8")
            a.style(_t=f"""
                body {{ background: {theme_data['bg']}; color: {theme_data['text']}; font-family: sans-serif; padding: 40px; max-width: 800px; margin: auto; line-height: 1.6; }}
                h1, h2, h3, h4, h5, h6 {{ color: {theme_data['accent']}; }}
                a, .wikilink {{ color: {theme_data['accent']}; text-decoration: none; border-bottom: 1px solid; }}
                code {{ background: {theme_data['code_bg']}; padding: 2px 5px; border-radius: 4px; font-family: monospace; }}
                pre {{ background: {theme_data['code_bg']}; padding: 15px; border-radius: 8px; overflow-x: auto; }}
                blockquote {{ border-left: 5px solid {theme_data['quote_bar']}; padding-left: 20px; font-style: italic; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid {theme_data['border']}; padding: 8px; }}
                th {{ background: {theme_data['table_header']}; }}
                hr {{ border: 0; border-top: 2px solid {theme_data['border']}; margin: 20px 0; }}
                img {{ max-width: 100%; }}
            """)
        with a.body():
            a(html_body)
    return str(a)

def main() -> None:
    if len(sys.argv) < 4:
        print("Usage: converter.py <input.md> <output.html> <theme>")
        return

    input_f, output_f, theme_n = sys.argv[1:4]
    
    try:
        with open(input_f, 'r', encoding='utf-8') as f:
            md_text = re.sub(r'\+\+(.*?)\+\+', r'<ins>\1</ins>', f.read())
        
        theme_data = load_theme(theme_n)
        final_html = create_html(md_text, theme_data)
        
        with open(output_f, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Done! Style: {theme_n}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
