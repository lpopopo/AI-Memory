const https = require('https');
const { TextDecoder } = require('util');

const tickers = ['TSLA','NOK','RKLB','RDW','MRVL','AXTI','ORCL','INTC','SNDK','WDC','STX'];
const sym = tickers.map(t => 'us' + t).join(',');

https.get('https://qt.gtimg.cn/q=' + sym, { timeout: 8000 }, res => {
  const c = [];
  res.on('data', d => c.push(d));
  res.on('end', () => {
    const txt = new TextDecoder('gbk').decode(Buffer.concat(c));
    const lines = txt.split('\n').filter(l => l.includes('~'));
    const out = [];
    for (const line of lines) {
      const m = line.match(/v_us(\w+)="([^"]*)"/);
      if (!m) continue;
      const f = m[2].split('~');
      const price = parseFloat(f[3]) || 0;
      const prev  = parseFloat(f[4]) || 0;
      const chg   = prev > 0 ? ((price - prev) / prev * 100) : parseFloat(f[32]);
      out.push({ ticker: m[1], price: price.toFixed(2), chg: chg.toFixed(2) + '%', prev: prev.toFixed(2) });
    }
    out.sort((a, b) => parseFloat(b.chg) - parseFloat(a.chg));
    console.log(JSON.stringify(out, null, 2));
  });
}).on('error', e => console.error(e.message));
