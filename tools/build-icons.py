"""Генерирует favicon-набор из brand/logo-source.jpg.

Логотип лежит на белом фоне, поэтому иконки делаются на белой плитке:
чёрный контур треугольника пропадал бы на тёмной панели вкладок,
а белая плитка читается одинаково в любой теме браузера.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

root = Path(sys.argv[1])
src = root / "brand" / "logo-source.jpg"
out_dir = root

# ------------------------------------------------------------------ подготовка
img = Image.open(src).convert("RGB")
arr = np.asarray(img).astype(int)
mask = ~np.all(arr > 240, axis=2)          # фон = почти белый
ys, xs = np.where(mask)
logo = img.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
print(f"логотип вырезан: {logo.width}x{logo.height}")

# квадратный мастер с полем 6% от большей стороны
side = max(logo.width, logo.height)
margin = round(side * 0.06)
canvas_side = side + margin * 2
master = Image.new("RGB", (canvas_side, canvas_side), "white")
master.paste(logo, ((canvas_side - logo.width) // 2, (canvas_side - logo.height) // 2))
print(f"мастер: {canvas_side}x{canvas_side} (запас {margin}px)")


def render(size):
    """Плитка нужного размера. Для мелких иконок — лёгкая резкость,
    иначе буквы CGP сливаются в кашу."""
    tile = master.resize((size, size), Image.LANCZOS)
    if size <= 48:
        tile = tile.filter(ImageFilter.UnsharpMask(radius=0.6, percent=70, threshold=0))
    return tile


# ------------------------------------------------------------------ генерация
png_targets = {
    "favicon-16x16.png": 16,
    "favicon-32x32.png": 32,
    "favicon-48x48.png": 48,
    "apple-touch-icon.png": 180,
    "icon-192.png": 192,
    "icon-512.png": 512,
}
for name, size in png_targets.items():
    tile = render(size)
    tile.save(out_dir / name, "PNG", optimize=True)
    print(f"  {name:<24} {size}x{size}")

# многокелейный ICO: 16 / 32 / 48
render(256).save(out_dir / "favicon.ico", "ICO", sizes=[(16, 16), (32, 32), (48, 48)])
print(f"  {'favicon.ico':<24} 16/32/48")

# мастер-файл для будущих перегенераций
master.save(root / "brand" / "logo-master.png", "PNG", optimize=True)
print(f"  brand/logo-master.png     {canvas_side}x{canvas_side}")
