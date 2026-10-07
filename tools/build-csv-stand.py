"""Готовит стенд для проверки загрузки прайса из «Google Таблицы» (CSV)."""
import csv
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
tmp = Path(sys.argv[2])
tmp.mkdir(parents=True, exist_ok=True)

rows = json.loads((root / "tools" / "prices.json").read_text(encoding="utf-8"))

header = list(rows[0])
header.append("Пикап")          # новый тип авто, добавленный «заказчиком»
body = [list(r) + [""] for r in rows[1:]]

# «заказчик» правит цену и добавляет новую услугу
for r in body:
    if r[2] == "Лёгкая полировка кузова":
        r[3] = 777
body.append(["Полировка и защита ЛКП", "", "Тестовая новая услуга", "", "", "", "", "", 1234, "Добавлено в таблице"])
body.append(["Полировка и защита ЛКП", "", "Услуга по типу авто", "", 990, "", 1990, "", "", ""])

csv_path = tmp / "prices.csv"
with csv_path.open("w", encoding="utf-8", newline="") as fh:
    writer = csv.writer(fh)
    writer.writerow(header)
    writer.writerows(body)

html = (root / "index.html").read_text(encoding="utf-8")
html = html.replace(
    "csvUrl: '',",
    "csvUrl: 'http://127.0.0.1:8765/prices.csv',",
)
(html and (tmp / "test-site.html").write_text(html, encoding="utf-8"))

print("csv:", csv_path, "rows:", len(body) + 1, "cols:", len(header))
print("site:", tmp / "test-site.html")
