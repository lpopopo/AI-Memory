const https = require('https');

// Fetch 90-day historical closes from Yahoo Finance for a list of tickers
const tickers = [
  'NOW', 'PLTR', 'APP', 'ADBE', 'QCOM',
  'CRDO', 'ALAB', 'COHR', 'CIEN', 'MXL',
  'MU', 'AVGO', 'AMD', 'ANET',
  'VRT', 'ETN', 'TER', 'SMCI',
  'QQQ', 'SMH', 'SPY'
];

function fetchYahoo(ticker) {
  // range=6mo, interval=1d gives ~125 bars
  const url = `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?range=6mo&interval=1d`;
  return new Promise((resolve) => {
    const req = https.get(url, {
      timeout: 10000,
      headers: { 'User-Agent': 'Mozilla/5.0' }
    }, (res) => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        try {
          const json = JSON.parse(Buffer.concat(chunks).toString());
          const meta = json.chart.result[0].meta;
          const closes = json.chart.result[0].indicators.quote[0].close;
          const timestamps = json.chart.result[0].timestamp;
          const bars = closes
            .map((c, i) => ({ date: new Date(timestamps[i] * 1000).toISOString().slice(0, 10), close: c }))
            .filter(b => b.close != null);
          resolve({ ticker, bars });
        } catch(e) {
          resolve({ ticker, bars: [], error: e.message });
        }
      });
    });
    req.on('error', e => resolve({ ticker, bars: [], error: e.message }));
    req.on('timeout', () => { req.destroy(); resolve({ ticker, bars: [], error: 'timeout' }); });
  });
}

async function main() {
  // Stagger requests to avoid rate-limit
  const results = [];
  for (const t of tickers) {
    const r = await fetchYahoo(t);
    await new Promise(res => setTimeout(res, 200));
    if (r.bars.length < 20) {
      results.push({ ticker: t, error: r.error || 'too few bars', rs90d: null, rs45d: null });
      continue;
    }
    // Last 90 calendar days = approx 63 trading days; use last 63 bars
    const bars = r.bars.slice(-63);
    const last  = bars[bars.length - 1].close;
    const first = bars[0].close;
    const mid   = bars[Math.floor(bars.length / 2)].close;
    const rs90  = ((last - first) / first * 100);
    const rs45  = ((last - mid) / mid * 100);
    // 20-bar high
    const recent20 = bars.slice(-20);
    const h20 = Math.max(...recent20.map(b => b.close));
    const pctFromH = ((last - h20) / h20 * 100);
    results.push({
      ticker: t,
      lastClose: last.toFixed(2),
      rs90d: rs90.toFixed(1) + '%',
      rs45d: rs45.toFixed(1) + '%',
      pctFromH20: pctFromH.toFixed(1) + '%',
      rs90raw: rs90,
      bars: bars.length
    });
  }

  // Sort by 90d RS descending
  results.sort((a, b) => (b.rs90raw || -999) - (a.rs90raw || -999));

  console.log('\n=== 90-Day Relative Strength Ranking ===');
  for (const r of results) {
    if (r.error) {
      console.log(`  ${r.ticker.padEnd(6)} ERROR: ${r.error}`);
    } else {
      const bar = r.rs90raw >= 0 ? '▲' : '▼';
      console.log(`  ${r.ticker.padEnd(6)} last=${r.lastClose.padStart(8)}  RS90d=${r.rs90d.padStart(8)}  RS45d=${r.rs45d.padStart(8)}  fromH20=${r.pctFromH20.padStart(7)}  ${bar}`);
    }
  }
}

main();
