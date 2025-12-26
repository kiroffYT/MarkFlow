import sys
import os
import json
import re
import colorsys
from typing import Dict, Tuple

import markdown
from airium import Airium

DEFAULT_THEME: Dict[str, str] = {
    "bg": "#1e1e1e", "text": "#d4d4d4", "accent": "#3794ff",
    "code_bg": "#2d2d2d", "border": "#454545", "quote_bar": "#3794ff",
    "table_header": "#2d2d2d"
}

def rgb_to_hex(rgb: Tuple[float, float, float]) -> str:
    return '#%02x%02x%02x' % tuple(int(x * 255) for x in rgb)

def generate_dynamic_theme(hue: int, mode: str = "dark") -> Dict[str, str]:
    h_val = (hue % 360) / 360.0
    
    if mode == "light":
        bg_rgb = colorsys.hls_to_rgb(h_val, 0.97, 0.2)
        text_rgb = colorsys.hls_to_rgb(h_val, 0.2, 0.1)
        acc_rgb = colorsys.hls_to_rgb(h_val, 0.4, 0.8)
        cbg_rgb = colorsys.hls_to_rgb(h_val, 0.92, 0.15)
    else:
        bg_rgb = colorsys.hls_to_rgb(h_val, 0.07, 0.15)
        text_rgb = colorsys.hls_to_rgb(h_val, 0.85, 0.1)
        acc_rgb = colorsys.hls_to_rgb(h_val, 0.6, 0.7)
        cbg_rgb = colorsys.hls_to_rgb(h_val, 0.12, 0.2)

    brd_rgb = colorsys.hls_to_rgb(h_val, 0.3, 0.2)
    
    return {
        "bg": rgb_to_hex(bg_rgb),
        "text": rgb_to_hex(text_rgb),
        "accent": rgb_to_hex(acc_rgb),
        "code_bg": rgb_to_hex(cbg_rgb),
        "border": rgb_to_hex(brd_rgb),
        "quote_bar": rgb_to_hex(acc_rgb),
        "table_header": rgb_to_hex(cbg_rgb)
    }

def load_theme(theme_name: str) -> Dict[str, str]:
    if "hue-" in theme_name:
        mode = "light" if "light" in theme_name else "dark"
        digits = re.findall(r'\d+', theme_name)
        hue_val = int(digits[0]) if digits else 0
        return generate_dynamic_theme(hue_val, mode)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'themes.json')
    
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                themes_db = json.load(f)
                if theme_name in themes_db:
                    return themes_db[theme_name]
        except (json.JSONDecodeError, OSError):
            return DEFAULT_THEME
            
    return DEFAULT_THEME

def create_html(md_content: str, theme_data: Dict[str, str]) -> str:
    exts = ['extra', 'sane_lists', 'wikilinks', 'nl2br']
    html_body = markdown.markdown(md_content, extensions=exts)
    
    air = Airium()
    air('<!DOCTYPE html>')
    with air.html(lang="ru"):
        with air.head():
            air.meta(charset="utf-8")
            air.style(_t=f"""
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
        with air.body():
            air(html_body)
    return str(air)

def main() -> None:
    """Точка входа в программу."""
    if len(sys.argv) < 4:
        print("Usage: converter.py <input.md> <output.html> <theme>")
        sys.exit(0)

    input_f, output_f, theme_n = sys.argv[1:4]
    
    if not os.path.exists(input_f):
        print(f"Error: File {input_f} not found.")
        sys.exit(1)

    try:
        with open(input_f, 'r', encoding='utf-8') as f:
            content = f.read()
            # Поддержка подчеркивания
            md_text = re.sub(r'\+\+(.*?)\+\+', r'<ins>\1</ins>', content)
        
        theme_cfg = load_theme(theme_n)
        html_out = create_html(md_text, theme_cfg)
        
        with open(output_f, 'w', encoding='utf-8') as f:
            f.write(html_out)
        print(f"Success! Generated with theme: {theme_n}")

    except (OSError, ValueError, PermissionError) as err:
        print(f"Runtime Error: {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
