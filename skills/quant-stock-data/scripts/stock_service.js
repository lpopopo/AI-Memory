/**
 * Resilient stock data service.
 * Supports Tencent Smartbox search, Tencent primary quotes, Yahoo fallback quotes,
 * and Sina last-resort fallback quotes.
 */
class StockService {
  static _decodeGbk(buf) {
    try {
      return new TextDecoder("gbk").decode(buf);
    } catch (error) {
      if (typeof Buffer !== "undefined") {
        console.warn("[Decode] GBK TextDecoder is unavailable; Chinese names may be garbled.");
        return Buffer.from(buf).toString("binary");
      }
      throw error;
    }
  }

  static async _requestArrayBuffer(url, options = {}) {
    const errors = [];
    const useNodeClient = typeof require === "function" && typeof window === "undefined";
    if (useNodeClient) {
      try {
        if (typeof process !== "undefined" && process.env.AI_MEMORY_FORCE_NODE_HTTP_FAIL === "1") {
          throw new Error("Forced node:https failure for smoke test");
        }
        return await this._requestArrayBufferWithNode(url, options);
      } catch (error) {
        errors.push(`node:https ${this._compactError(error)}`);
      }

      if (typeof process !== "undefined" && process.platform === "win32") {
        try {
          return await this._requestArrayBufferWithPowerShell(url, options);
        } catch (error) {
          errors.push(`powershell ${this._compactError(error)}`);
        }
      }
    }

    if (typeof fetch === "function") {
      try {
        const res = await fetch(url, options);
        if (!res.ok) throw new Error(`HTTP Status ${res.status}`);
        return res.arrayBuffer();
      } catch (error) {
        errors.push(`fetch ${this._compactError(error)}`);
      }
    }

    throw new Error(errors.length ? errors.join(" | ") : "No fetch implementation available in this runtime");
  }

  static async _requestJson(url, options = {}) {
    const buf = await this._requestArrayBuffer(url, {
      headers: {
        Accept: "application/json,text/plain,*/*",
        "User-Agent": "Mozilla/5.0",
        ...(options.headers || {}),
      },
      timeoutMs: options.timeoutMs || 8000,
    });
    const text = new TextDecoder("utf-8").decode(buf);
    return JSON.parse(text);
  }

  static _toYahooSymbol(symbol) {
    const clean = String(symbol).trim();
    if (/^us/i.test(clean)) return clean.slice(2).toUpperCase();
    return clean.toUpperCase();
  }

  static _isUsSymbol(symbol) {
    return /^us[A-Z.]+$/i.test(String(symbol)) || /^[A-Z.]+$/i.test(String(symbol));
  }

  static _lastNumber(values) {
    if (!Array.isArray(values)) return 0;
    for (let index = values.length - 1; index >= 0; index -= 1) {
      const value = Number.parseFloat(values[index]);
      if (Number.isFinite(value)) return value;
    }
    return 0;
  }

  static _compactError(error) {
    return String(error && error.message ? error.message : error).replace(/\s+/g, " ").slice(0, 240);
  }

  static async _requestArrayBufferWithNode(url, options = {}) {
    if (typeof require !== "function") {
      throw new Error("No Node request implementation available in this runtime");
    }
    const client = url.startsWith("https:") ? require("https") : require("http");
    return new Promise((resolve, reject) => {
      const req = client.get(url, { headers: options.headers || {} }, (res) => {
        if (res.statusCode < 200 || res.statusCode >= 300) {
          res.resume();
          reject(new Error(`HTTP Status ${res.statusCode}`));
          return;
        }

        const chunks = [];
        res.on("data", (chunk) => chunks.push(chunk));
        res.on("end", () => {
          const buffer = Buffer.concat(chunks);
          resolve(buffer.buffer.slice(buffer.byteOffset, buffer.byteOffset + buffer.byteLength));
        });
      });
      req.on("error", reject);
      req.setTimeout(options.timeoutMs || 8000, () => {
        req.destroy(new Error("Request timeout"));
      });
    });
  }

  static async _requestArrayBufferWithPowerShell(url, options = {}) {
    const { execFileSync } = require("child_process");
    const script = `
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$headers = @{}
$headersJson = @'
${JSON.stringify(options.headers || {})}
'@
if ($headersJson.Trim().Length -gt 0) {
  $parsed = $headersJson | ConvertFrom-Json
  foreach ($prop in $parsed.PSObject.Properties) { $headers[$prop.Name] = [string]$prop.Value }
}
$client = [System.Net.WebClient]::new()
foreach ($key in $headers.Keys) { $client.Headers[$key] = $headers[$key] }
$bytes = $client.DownloadData('${String(url).replace(/'/g, "''")}')
[Convert]::ToBase64String($bytes)
`;
    const output = execFileSync("powershell.exe", ["-NoProfile", "-NonInteractive", "-Command", script], {
      encoding: "utf8",
      maxBuffer: 1024 * 1024 * 8,
      timeout: (options.timeoutMs || 8000) + 3000,
      windowsHide: true,
    }).trim();
    const buffer = Buffer.from(output, "base64");
    return buffer.buffer.slice(buffer.byteOffset, buffer.byteOffset + buffer.byteLength);
  }

  static normalizeSymbol(symbol) {
    const clean = String(symbol).trim().replace(/[\s.]/g, "").toLowerCase();
    if (/^(sh|sz|hk|us)/.test(clean)) return clean;
    if (/^\d{6}$/.test(clean)) {
      return clean.startsWith("6") || clean.startsWith("9") ? `sh${clean}` : `sz${clean}`;
    }
    if (/^\d{1,5}$/.test(clean)) return `hk${clean.padStart(5, "0")}`;
    if (/^[a-z]+$/i.test(clean)) return `us${clean.toUpperCase()}`;
    return clean;
  }

  static async searchStocks(query) {
    const url = `https://smartbox.gtimg.cn/s3/?v=2&q=${encodeURIComponent(query)}&t=all`;
    try {
      const buf = await this._requestArrayBuffer(url);
      const text = this._decodeGbk(buf);
      const match = text.match(/v_hint="([^"]+)"/);
      if (!match) return [];

      return match[1]
        .split("^")
        .filter(Boolean)
        .map((item) => {
          const fields = item.split("~");
          return {
            symbol: `${fields[0]}${fields[1]}`,
            name: fields[2],
            pinyin: fields[3],
            market: fields[0].toUpperCase(),
            type: fields[4],
          };
        });
    } catch (error) {
      console.error(`Fuzzy search failed for '${query}':`, error);
      return [];
    }
  }

  static async fetchQuotes(symbols) {
    const normSymbols = symbols.map((symbol) => this.normalizeSymbol(symbol));
    const errors = [];
    try {
      const results = await this._fetchTencent(normSymbols);
      if (results.length > 0) return results;
      errors.push("Tencent returned no usable rows");
    } catch (primaryError) {
      errors.push(`Tencent failed: ${this._compactError(primaryError)}`);
    }

    const usSymbols = normSymbols.filter((symbol) => this._isUsSymbol(symbol));
    if (usSymbols.length > 0) {
      try {
        const results = await this._fetchYahoo(usSymbols);
        if (results.length > 0) {
          if (errors.length > 0) console.warn(`[Fallback] ${errors.join(" | ")}. Used Yahoo chart.`);
          return results;
        }
        errors.push("Yahoo returned no usable rows");
      } catch (secondaryError) {
        errors.push(`Yahoo failed: ${this._compactError(secondaryError)}`);
      }
    }

    try {
      const results = await this._fetchSina(normSymbols);
      if (results.length > 0) {
        console.warn(`[Fallback] ${errors.join(" | ")}. Used Sina.`);
        return results;
      }
      errors.push("Sina returned no usable rows");
    } catch (lastError) {
      errors.push(`Sina failed: ${this._compactError(lastError)}`);
    }

    console.error(`[Fatal] quote sources failed: ${errors.join(" | ")}`);
    return [];
  }

  static async _fetchTencent(symbols) {
    const url = `https://qt.gtimg.cn/q=${symbols.join(",")}`;
    const buf = await this._requestArrayBuffer(url);
    const text = this._decodeGbk(buf);
    const lines = text.split("\n");
    const results = [];

    for (const sym of symbols) {
      const line = lines.find((item) => item.includes(`v_${sym}=`));
      if (!line) continue;

      const content = line.substring(line.indexOf('="') + 2, line.lastIndexOf('"'));
      const fields = content.split("~");
      if (fields.length < 35) continue;

      results.push({
        symbol: sym.toUpperCase(),
        name: fields[1],
        price: Number.parseFloat(fields[3]) || 0,
        yesterdayClose: Number.parseFloat(fields[4]) || 0,
        open: Number.parseFloat(fields[5]) || 0,
        changePercent: Number.parseFloat(fields[32]) || 0,
        high: Number.parseFloat(fields[33]) || 0,
        low: Number.parseFloat(fields[34]) || 0,
        volume: Number.parseInt(fields[6], 10) || 0,
        source: "Tencent (Primary)",
      });
    }

    return results;
  }

  static async _fetchYahoo(symbols) {
    const results = [];

    for (const sym of symbols) {
      const ticker = this._toYahooSymbol(sym);
      const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(ticker)}?range=1d&interval=1m`;
      const data = await this._requestJson(url);
      const chart = data && data.chart;
      const item = chart && chart.result && chart.result[0];
      if (!item || !item.meta) continue;

      const meta = item.meta;
      const quote = item.indicators && item.indicators.quote && item.indicators.quote[0] ? item.indicators.quote[0] : {};
      const price = Number.parseFloat(meta.regularMarketPrice) || this._lastNumber(item.indicators && item.indicators.quote && item.indicators.quote[0] && item.indicators.quote[0].close);
      const previousClose = Number.parseFloat(meta.previousClose || meta.chartPreviousClose) || 0;
      const changePercent = previousClose > 0 ? ((price - previousClose) / previousClose) * 100 : 0;

      results.push({
        symbol: `US${ticker}`,
        name: meta.shortName || ticker,
        price,
        yesterdayClose: previousClose,
        open: this._lastNumber(quote.open),
        changePercent,
        high: this._lastNumber(quote.high),
        low: this._lastNumber(quote.low),
        volume: Math.trunc(this._lastNumber(quote.volume)),
        source: "Yahoo Chart (Fallback)",
      });
    }

    return results.filter((item) => Number.isFinite(item.price) && item.price > 0);
  }

  static async _fetchSina(symbols) {
    const url = `https://hq.sinajs.cn/list=${symbols.join(",")}`;
    const buf = await this._requestArrayBuffer(url, {
      headers: {
        Referer: "https://finance.sina.com.cn/",
      },
    });
    const text = this._decodeGbk(buf);
    const lines = text.split("\n");
    const results = [];

    for (const sym of symbols) {
      const line = lines.find((item) => item.includes(`hq_str_${sym}=`));
      if (!line) continue;

      const content = line.substring(line.indexOf('="') + 2, line.lastIndexOf('"'));
      const fields = content.split(",");
      if (fields.length < 10) continue;

      const price = Number.parseFloat(fields[3]) || 0;
      const yesterdayClose = Number.parseFloat(fields[2]) || 0;
      const changePercent = yesterdayClose > 0 ? ((price - yesterdayClose) / yesterdayClose) * 100 : 0;

      results.push({
        symbol: sym.toUpperCase(),
        name: fields[0],
        price,
        yesterdayClose,
        open: Number.parseFloat(fields[1]) || 0,
        changePercent,
        high: Number.parseFloat(fields[4]) || 0,
        low: Number.parseFloat(fields[5]) || 0,
        volume: Math.trunc((Number.parseInt(fields[8], 10) || 0) / 100),
        source: "Sina (Secondary)",
      });
    }

    return results;
  }
}

if (typeof module !== "undefined") {
  module.exports = { StockService };
}
