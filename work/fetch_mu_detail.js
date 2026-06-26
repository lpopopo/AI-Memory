const https = require('https');
const { TextDecoder } = require('util');

const syms = 'usMU,usSMH,usQQQ,usSPY';
https.get('https://qt.gtimg.cn/q=' + syms, { timeout: 8000 }, res => {
  const c = [];
  res.on('data', d => c.push(d));
  res.on('end', () => {
    const txt = new TextDecoder('gbk').decode(Buffer.concat(c));
    const lines = txt.split('\n').filter(l => l.includes('~'));
    for (const line of lines) {
      const m = line.match(/v_us(\w+)="([^"]*)"/);
      if (!m) continue;
      const f = m[2].split('~');
      const price = parseFloat(f[3]) || 0;
      const prev  = parseFloat(f[4]) || 0;
      const high  = parseFloat(f[33]) || 0;
      const low   = parseFloat(f[34]) || 0;
      const open  = parseFloat(f[5]) || 0;
      const chg   = prev > 0 ? ((price - prev) / prev * 100) : 0;
      console.log(`${m[1].padEnd(4)} price=${price.toFixed(2)} open=${open.toFixed(2)} high=${high.toFixed(2)} low=${low.toFixed(2)} prev=${prev.toFixed(2)} chg=${chg.toFixed(2)}%`);
    }
  });
}).on('error', e => console.error(e.message));
