/**
 * Resilient stock data service.
 * Supports Tencent Smartbox search, Tencent primary quotes, and Sina fallback quotes.
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
    if (typeof fetch === "function") {
      const res = await fetch(url, options);
      if (!res.ok) throw new Error(`HTTP Status ${res.status}`);
      return res.arrayBuffer();
    }

    if (typeof require !== "function") {
      throw new Error("No fetch implementation available in this runtime");
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
      req.setTimeout(5000, () => {
        req.destroy(new Error("Request timeout"));
      });
    });
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
    try {
      return await this._fetchTencent(normSymbols);
    } catch (primaryError) {
      console.warn(`[Fallback] Tencent quotes failed: ${primaryError.message}. Switching to Sina.`);
      try {
        return await this._fetchSina(normSymbols);
      } catch (secondaryError) {
        console.error("[Fatal] Tencent and Sina quote sources both failed:", secondaryError);
        return [];
      }
    }
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
