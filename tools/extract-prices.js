// Извлекает встроенный прайс-лист из index.html и сохраняет его как JSON,
// чтобы шаблон Google Таблицы и сайт гарантированно совпадали.
const fs = require('fs');
const path = require('path');

const root = process.argv[2];
const out = process.argv[3];
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');

const match = html.match(/const DEFAULT_PRICE_ROWS = (\[[\s\S]*?\n\s*\]);/);
if (!match) throw new Error('DEFAULT_PRICE_ROWS не найден');
const literal = match[1];
// eslint-disable-next-line no-eval
const rows = eval(literal);

if (!Array.isArray(rows) || rows.length < 2) throw new Error('массив пуст');
fs.writeFileSync(out, JSON.stringify(rows, null, 1), 'utf8');
console.log('rows:', rows.length, 'cols:', rows[0].length);
console.log('sheets data written to', out);
