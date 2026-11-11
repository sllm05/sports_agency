const fs = require('fs');
const markedCode = fs.readFileSync('scratch/marked.js', 'utf-8');
const win = {};
const fn = new Function('window', markedCode + '; return window.marked;');
const marked = fn(win);

const md = fs.readFileSync('outputs/Michael_Olise_pitch_deck.md', 'utf-8');
const html = marked.parse(md);

const idx = html.indexOf('DataMB 5대 리그 동 포지션 백분위 벤치마크');
console.log('--- OUTPUT ---');
console.log(html.substring(idx - 50, idx + 800));
