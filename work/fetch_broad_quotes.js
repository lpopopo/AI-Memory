const https = require('https');
const { TextDecoder } = require('util');

const tickers = [
  'CRDO','ALAB','LITE','COHR','CIEN','MXL',
  'MU','SNDK','STX',
  'SMCI','TTMI',
  'ORCL','NOW','PLTR',
  'TER',
  'VRT','ETN',
  'ANET','CSCO',
  'AVGO','AMD','INTC','QCOM',
  'APP','ADBE',
  'GLW','DRAM'
];

const symbols = tickers.map(t => 'us' + t).join(',');
const url = 'https://qt.gtimg.cn/q=' + symbols;

const req = https.get(url, { timeout: 10000 }, (res) => {
  const chunks = [];
  res.on('data', c => chunks.push(c));
  res.on('end', () => {
    try {
      const buf = Buffer.concat(chunks);
      const text = new TextDecoder('gbk').decode(buf);
      const lines = text.split('\n').filter(l => l.includes('~'));
      const results = [];
      for (const line of lines) {
        const m = line.match(/v_us(\w+)="([^"]*)"/);
        if (!m) continue;
        const ticker = m[1];
        const fields = m[2].split('~');
        const price = parseFloat(fields[3]) || 0;
        const prev  = parseFloat(fields[4]) || 0;
        const chg   = prev > 0 ? ((price - prev) / prev * 100) : parseFloat(fields[32]);
        results.push({
          ticker,
          price: price.toFixed(2),
          chgPct: chg.toFixed(2),
          prev: prev.toFixed(2)
        });
      }
      results.sort((a, b) => parseFloat(b.chgPct) - parseFloat(a.chgPct));
      console.log(JSON.stringify(results, null, 2));
    } catch(e) {
      console.error('parse error', e.message);
    }
  });
});
req.on('error', e => console.error('req error', e.message));
