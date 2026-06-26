const https = require('https');
const { TextDecoder } = require('util');

// Focus: candidates showing relative strength today (beat the market)
// plus key reference tickers for context
const targets = {
  // Clear outperformers today (positive or < -1% vs QQQ -1.54%)
  'NOW':  'usNOW',
  'PLTR': 'usPLTR',
  'APP':  'usAPP',
  'ADBE': 'usADBE',
  'QCOM': 'usQCOM',
  // Reference basket
  'QQQ':  'usQQQ',
  'SMH':  'usSMH',
  'SPY':  'usSPY',
};

function fetchKline(symbol) {
  // Tencent daily K-line: us prefix maps to 'us' category
  const cat = symbol.startsWith('us') ? 'us' : 'hk';
  const url = `https://data.gtimg.cn/flashdata/${cat}/latest/daily/${symbol}.js`;
  return new Promise((resolve) => {
    https.get(url, { timeout: 8000 }, (res) => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        try {
          const buf = Buffer.concat(chunks);
          const text = new TextDecoder('gbk').decode(buf);
          // Format: YYMMDD open high low close volume
          const lines = text.split('\\n').map(l => l.trim()).filter(l => /^\d{6}/.test(l));
          const bars = lines.map(l => {
            const p = l.split(' ');
            return { date: '20' + p[0], close: parseFloat(p[4]) };
          }).filter(b => b.close > 0);
          resolve({ symbol, bars });
        } catch(e) {
          resolve({ symbol, bars: [], error: e.message });
        }
      });
    }).on('error', e => resolve({ symbol, bars: [], error: e.message }));
  });
}

async function main() {
  const entries = Object.entries(targets);
  const all = await Promise.all(entries.map(([name, sym]) => fetchKline(sym).then(r => ({ name, ...r }))));

  const results = [];
  for (const r of all) {
    if (r.bars.length < 10) {
      results.push({ ticker: r.name, bars: r.bars.length, error: r.error || 'too few bars' });
      continue;
    }
    const bars = r.bars.slice(-90); // last 90 trading days
    const last  = bars[bars.length - 1].close;
    const first = bars[0].close;
    const mid   = bars[Math.floor(bars.length / 2)].close;
    const rs90  = ((last - first) / first * 100).toFixed(2);
    const rs45  = ((last - mid) / mid * 100).toFixed(2);
    // 20-day high/low
    const recent20 = bars.slice(-20);
    const h20 = Math.max(...recent20.map(b => b.close));
    const l20 = Math.min(...recent20.map(b => b.close));
    const pctFromH = ((last - h20) / h20 * 100).toFixed(2);
    results.push({
      ticker: r.name,
      lastClose: last.toFixed(2),
      rs90d: rs90 + '%',
      rs45d: rs45 + '%',
      pctFromH20: pctFromH + '%',
      h20: h20.toFixed(2),
      l20: l20.toFixed(2),
      barCount: bars.length
    });
  }

  results.sort((a, b) => parseFloat(b.rs90d) - parseFloat(a.rs90d));
  console.log('\n=== 90-Day Relative Strength Table ===');
  console.table(results);
}

main();
