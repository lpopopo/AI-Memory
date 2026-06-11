#!/usr/bin/env node

const fs = require("node:fs");
const path = require("node:path");
const { execFile } = require("node:child_process");

const MONTHS =
  "January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec";

const SOURCES = [
  {
    name: "AQR Research",
    listUrl: "https://www.aqr.com/Insights/Research",
    allowedHost: "www.aqr.com",
    requiredPath: "/Insights/Research/",
    dimension: "trend_aligned_entry / factor robustness / portfolio construction",
  },
  {
    name: "Citadel Securities Market Insights",
    listUrl: "https://www.citadelsecurities.com/news-and-insights/category/market-insights/",
    allowedHost: "www.citadelsecurities.com",
    requiredPath: "/news-and-insights/",
    excludePathIncludes: ["/category/", "/series/", "/in-the-media/", "/policy-positions/"],
    dimension: "flow_fragility / market structure / macro strategy",
  },
  {
    name: "GMO Research Library",
    listUrl: "https://www.gmo.com/americas/research-library/",
    allowedHost: "www.gmo.com",
    requiredPath: "/americas/research-library/",
    dimension: "AI_quality/capex_cycle / valuation-aware allocation / quality",
  },
  {
    name: "Man Institute Market Views",
    listUrl: "https://www.man.com/maninstitute/market-views",
    allowedHost: "www.man.com",
    requiredPath: "/insights/",
    dimension: "factor_macro_exposure / flow_fragility / AI bottleneck watch",
  },
];

function parseArgs(argv) {
  const args = {
    since: null,
    out: path.resolve(process.cwd(), "work", "institutional-research-latest.md"),
    json: null,
    maxItems: 6,
  };
  for (let i = 2; i < argv.length; i += 1) {
    const key = argv[i];
    const value = argv[i + 1];
    if (key === "--since") {
      args.since = new Date(value);
      i += 1;
    } else if (key === "--out") {
      args.out = path.resolve(value);
      i += 1;
    } else if (key === "--json") {
      args.json = path.resolve(value);
      i += 1;
    } else if (key === "--max-items") {
      args.maxItems = Number.parseInt(value, 10);
      i += 1;
    } else if (key === "--help") {
      console.log(`Usage:
  node domains/quant-strategy/tools/institutional-research-checker.js [options]

Options:
  --since <iso-date>       Only mark items newer than this time as post-window verified.
  --out <path>             Markdown report path. Defaults to work/institutional-research-latest.md.
  --json <path>            JSON diagnostics path. Defaults next to --out.
  --max-items <number>     Max candidate detail pages per source. Defaults to 6.
`);
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${key}`);
    }
  }
  if (args.since && Number.isNaN(args.since.getTime())) {
    throw new Error("--since must be an ISO-like date");
  }
  if (!args.json) args.json = args.out.replace(/\.md$/i, ".json");
  return args;
}

function fetchTextWithPowerShell(url, timeoutMs = 30000) {
  const script = `
$ProgressPreference = 'SilentlyContinue'
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$headers = @{
  'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AI-Memory-institutional-research-checker/1.0'
  'Accept' = 'text/markdown,text/html,application/rss+xml,*/*;q=0.8'
}
$r = Invoke-WebRequest -UseBasicParsing -Uri $env:AI_MEMORY_FETCH_URL -TimeoutSec 30 -Headers $headers
if ($r.Content -is [byte[]]) {
  [Text.Encoding]::UTF8.GetString($r.Content)
} else {
  $r.Content
}
`;
  return new Promise((resolve) => {
    execFile(
      "powershell.exe",
      ["-NoProfile", "-NonInteractive", "-Command", script],
      {
        encoding: "utf8",
        timeout: timeoutMs + 5000,
        maxBuffer: 30 * 1024 * 1024,
        env: { ...process.env, AI_MEMORY_FETCH_URL: url },
      },
      (error, stdout, stderr) => {
        if (error) {
          resolve({ ok: false, status: 0, url, text: stdout || "", error: stderr || error.message });
          return;
        }
        resolve({ ok: true, status: 200, url, text: stdout || "" });
      }
    );
  });
}

async function fetchTextWithRetry(url, timeoutMs = 30000, attempts = 3) {
  let last = null;
  for (let attempt = 1; attempt <= attempts; attempt += 1) {
    last = await fetchTextWithPowerShell(url, timeoutMs);
    if (last.ok && last.text && last.text.trim().length > 0) return { ...last, attempts: attempt };
    await new Promise((resolve) => setTimeout(resolve, 1000 * attempt));
  }
  return { ...(last || { ok: false, status: 0, url, text: "", error: "not attempted" }), ok: false, attempts };
}

function jinaUrl(url) {
  const target = url.replace(/^https:\/\//, "http://");
  return `https://r.jina.ai/http://${target.replace(/^http:\/\//, "")}`;
}

function stripMarkdown(raw) {
  return String(raw || "")
    .replace(/!\[[^\]]*]\([^)]+\)/g, "")
    .replace(/\[([^\]]+)]\(([^)]+)(?:\s+"[^"]*")?\)/g, "$1")
    .replace(/\*\*/g, "")
    .replace(/#+/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function normalizeUrl(url) {
  try {
    const parsed = new URL(url.replace(/^http:\/\//, "https://"));
    parsed.hash = "";
    return parsed.toString().replace(/\/$/, "/");
  } catch {
    return null;
  }
}

function isAllowedArticleUrl(url, source) {
  try {
    const parsed = new URL(url);
    if (parsed.hostname !== source.allowedHost) return false;
    if (parsed.search) return false;
    if (!parsed.pathname.startsWith(source.requiredPath)) return false;
    if (source.excludePathIncludes?.some((part) => parsed.pathname.includes(part))) return false;
    if (parsed.pathname.replace(/\/$/, "") === source.requiredPath.replace(/\/$/, "")) return false;
    if (parsed.pathname.split("/").filter(Boolean).length < 2) return false;
    return true;
  } catch {
    return false;
  }
}

function findDate(text) {
  const iso = text.match(/Published Time:\s*([0-9]{4}-[0-9]{2}-[0-9]{2}T[^\s]+)/i);
  if (iso) return new Date(iso[1]);
  const monthDate = text.match(new RegExp(`\\b(${MONTHS})\\s+\\d{1,2},\\s+20\\d{2}\\b`, "i"));
  if (monthDate) return new Date(monthDate[0]);
  return null;
}

function extractCandidates(source, text) {
  const lines = text.split(/\r?\n/);
  const candidates = [];

  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i];
    const re = /\[([^\]]*)]\((https?:\/\/[^)\s]+)(?:\s+"([^"]*)")?\)/g;
    let match;
    while ((match = re.exec(line))) {
      const url = normalizeUrl(match[2]);
      if (!url || !isAllowedArticleUrl(url, source)) continue;
      const titleFromLink = stripMarkdown(match[3] || match[1]);
      const neighborhood = lines.slice(Math.max(0, i - 2), Math.min(lines.length, i + 8)).join("\n");
      const titleFromNextHeading =
        lines
          .slice(i, i + 8)
          .map((candidateLine) => candidateLine.match(/^#+\s+(.+)$/)?.[1])
          .find(Boolean) || "";
      const title = stripMarkdown(titleFromLink || titleFromNextHeading || new URL(url).pathname.split("/").at(-2));
      const listDate = findDate(neighborhood);
      candidates.push({
        title,
        url,
        listDate: listDate ? listDate.toISOString() : null,
        listContext: stripMarkdown(neighborhood).slice(0, 500),
      });
    }
  }

  const seen = new Set();
  return candidates.filter((candidate) => {
    if (seen.has(candidate.url)) return false;
    seen.add(candidate.url);
    return true;
  });
}

function parseDetail(candidate, detailText) {
  const title = stripMarkdown(detailText.match(/^Title:\s*(.+)$/m)?.[1] || candidate.title);
  const published = findDate(detailText);
  const warning = /security verification|CAPTCHA|returned error 403|Forbidden|Just a moment/i.test(detailText);
  const content = stripMarkdown(
    detailText
      .split(/Markdown Content:/i)
      .slice(1)
      .join("\n")
      .replace(/Cookie Manager[\s\S]*?# Market Views/i, "")
  );
  return {
    title,
    url: candidate.url,
    date: published ? published.toISOString() : candidate.listDate,
    dateSource: published ? "detail_page" : candidate.listDate ? "list_page" : "none",
    summary: content.slice(0, 700),
    detailWarning: warning,
  };
}

function classifyItem(item, args) {
  if (!item.date) {
    return {
      verificationStatus: item.detailWarning ? "detail_blocked_no_date" : "date_unverified",
      isPostWindow: false,
      evidence: item.detailWarning ? "低：列表可见但详情页安全校验/403，无法确认发布时间和正文。" : "低：未取得稳定发布日期。",
    };
  }
  const date = new Date(item.date);
  const isPostWindow = args.since ? date > args.since : true;
  if (!item.detailOk) {
    return {
      verificationStatus: isPostWindow ? "post_window_list_only" : "pre_window_or_existing_list_only",
      isPostWindow,
      evidence: "中：官方列表页可见标题/日期，但详情页未读取成功；可记录为候选，不应提炼新框架。",
    };
  }
  return {
    verificationStatus: isPostWindow ? "post_window_verified" : "pre_window_or_existing",
    isPostWindow,
    evidence: item.detailWarning
      ? "中：列表/部分详情可见但详情存在安全校验提示。"
      : "高：官方域名文章页经 Reader 读取，标题和日期可核验。",
  };
}

async function checkSource(source, args) {
  const diagnostics = [];
  const listResult = await fetchTextWithRetry(jinaUrl(source.listUrl), 45000);
  diagnostics.push({
    channel: "jina_list",
    url: listResult.url,
    ok: listResult.ok,
    length: listResult.text.length,
    attempts: listResult.attempts,
    error: listResult.error || null,
  });

  if (!listResult.ok || !listResult.text) {
    return { source: source.name, dimension: source.dimension, items: [], diagnostics, note: "列表页 Reader 读取失败。" };
  }

  const candidates = extractCandidates(source, listResult.text).slice(0, args.maxItems);
  const items = [];
  for (const candidate of candidates) {
    const detail = await fetchTextWithRetry(jinaUrl(candidate.url), 45000, 2);
    diagnostics.push({
      channel: "jina_detail",
      url: detail.url,
      ok: detail.ok,
      length: detail.text.length,
      attempts: detail.attempts,
      error: detail.error || null,
      candidate: candidate.url,
    });
    const parsed = parseDetail(candidate, detail.text || "");
    parsed.detailOk = detail.ok && detail.text && detail.text.trim().length > 0;
    const classification = classifyItem(parsed, args);
    items.push({ ...parsed, ...classification, dimension: source.dimension });
  }

  items.sort((a, b) => {
    if (!a.date && !b.date) return 0;
    if (!a.date) return 1;
    if (!b.date) return -1;
    return new Date(b.date) - new Date(a.date);
  });

  return {
    source: source.name,
    dimension: source.dimension,
    items,
    diagnostics,
    note: candidates.length ? "列表页可读；已读取候选详情页并按日期过滤。" : "列表页可读，但未抽取到官方文章候选。",
  };
}

function formatDate(iso) {
  if (!iso) return "";
  return new Intl.DateTimeFormat("zh-CN", {
    timeZone: "Asia/Shanghai",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(new Date(iso));
}

function renderMarkdown(results, args) {
  const lines = [];
  const now = new Date();
  lines.push("# Institutional Research Check");
  lines.push("");
  lines.push(`Run time: ${now.toISOString()}`);
  if (args.since) lines.push(`Since: ${args.since.toISOString()}`);
  lines.push("");
  lines.push("## Summary");
  lines.push("");
  lines.push("| Source | Post-window verified | Candidates checked | Dimension | Note |");
  lines.push("| --- | ---: | ---: | --- | --- |");
  for (const result of results) {
    const verified = result.items.filter((item) => item.isPostWindow).length;
    lines.push(`| ${result.source} | ${verified} | ${result.items.length} | ${result.dimension} | ${result.note || ""} |`);
  }
  lines.push("");

  for (const result of results) {
    lines.push(`## ${result.source}`);
    lines.push("");
    if (result.items.length) {
      lines.push("| Date | Status | Title | Link | Evidence | Summary |");
      lines.push("| --- | --- | --- | --- | --- | --- |");
      for (const item of result.items) {
        lines.push(
          `| ${formatDate(item.date)} | ${item.verificationStatus} | ${item.title.replace(/\|/g, "/")} | ${item.url} | ${item.evidence} | ${item.summary.replace(/\|/g, "/")} |`
        );
      }
      lines.push("");
    } else {
      lines.push(result.note || "No candidates extracted.");
      lines.push("");
    }
    lines.push("Diagnostics:");
    for (const diagnostic of result.diagnostics) {
      lines.push(
        `- ${diagnostic.channel}: ok=${diagnostic.ok} length=${diagnostic.length} url=${diagnostic.url}${diagnostic.error ? ` error=${diagnostic.error}` : ""}`
      );
    }
    lines.push("");
  }

  lines.push("Not investment advice.");
  lines.push("");
  return lines.join("\n");
}

async function main() {
  const args = parseArgs(process.argv);
  const results = [];
  for (const source of SOURCES) {
    results.push(await checkSource(source, args));
  }
  fs.mkdirSync(path.dirname(args.out), { recursive: true });
  fs.writeFileSync(args.out, renderMarkdown(results, args), "utf8");
  fs.writeFileSync(args.json, JSON.stringify({ args, results }, null, 2), "utf8");
  console.log(`Wrote ${args.out}`);
  console.log(`Wrote ${args.json}`);
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
