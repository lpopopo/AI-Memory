#!/usr/bin/env node

const fs = require("node:fs");
const path = require("node:path");
const { execFile } = require("node:child_process");

const TWITTER_EPOCH_MS = 1288834974657n;

const DEFAULT_X_ACCOUNTS = [
  {
    handle: "nvidia",
    label: "@nvidia",
    relatedHandles: ["nvidia", "nvidianewsroom", "NVIDIAAIInfra"],
    dimension: "AI 算力/推理/产品路线",
  },
  {
    handle: "elonmusk",
    label: "@elonmusk",
    relatedHandles: ["elonmusk"],
    dimension: "xAI/Tesla/SpaceX/AI 基建",
  },
  {
    handle: "realDonaldTrump",
    label: "@realDonaldTrump",
    relatedHandles: ["realDonaldTrump"],
    dimension: "政策/关税/地缘风险",
  },
];

const DEFAULT_XHS_ACCOUNTS = [
  {
    label: "美研芒格君",
    url: "https://www.xiaohongshu.com/user/profile/632ea1e700000000230381cb",
    dimension: "AI 产业链线索",
  },
];

function parseArgs(argv) {
  const args = {
    since: null,
    out: path.resolve(process.cwd(), "work", "realtime-public-source-latest.md"),
    json: null,
    maxPosts: 5,
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
    } else if (key === "--max-posts") {
      args.maxPosts = Number.parseInt(value, 10);
      i += 1;
    } else if (key === "--help") {
      printHelp();
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${key}`);
    }
  }

  if (args.since && Number.isNaN(args.since.getTime())) {
    throw new Error("--since must be an ISO-like date, for example 2026-06-03T12:30:34.033Z");
  }

  if (!args.json) {
    args.json = args.out.replace(/\.md$/i, ".json");
  }

  return args;
}

function printHelp() {
  console.log(`Usage:
  node domains/quant-strategy/tools/realtime-public-source-checker.js [options]

Options:
  --since <iso-date>       Only report posts newer than this time.
  --out <path>             Markdown report path. Defaults to work/realtime-public-source-latest.md.
  --json <path>            JSON diagnostics path. Defaults next to --out.
  --max-posts <number>     Max X posts per account. Defaults to 8.
`);
}

function normalizeHandle(handle) {
  return String(handle || "").replace(/^@/, "").toLowerCase();
}

function xPostCreatedAtFromId(id) {
  const value = BigInt(id);
  const ms = (value >> 22n) + TWITTER_EPOCH_MS;
  return new Date(Number(ms));
}

async function fetchText(url, options = {}) {
  if (/^https:\/\/r\.jina\.ai\//i.test(url)) {
    return fetchTextWithPowerShell(url, options);
  }

  const timeoutMs = options.timeoutMs || 15000;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, {
      signal: controller.signal,
      headers: {
        "user-agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 AI-Memory-public-source-checker/1.0",
        accept: "text/markdown,text/html,application/rss+xml,*/*;q=0.8",
        ...(options.headers || {}),
      },
    });
    const text = await response.text();
    return { ok: response.ok, status: response.status, url, text };
  } catch (error) {
    const fallback = await fetchTextWithPowerShell(url, options);
    if (fallback.ok || fallback.text) return fallback;
    return { ok: false, status: 0, url, text: "", error: `${error.message}; ${fallback.error || ""}` };
  } finally {
    clearTimeout(timer);
  }
}

function fetchTextWithPowerShell(url, options = {}) {
  const timeoutMs = options.timeoutMs || 20000;
  const script = `
$ProgressPreference = 'SilentlyContinue'
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$headers = @{
  'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AI-Memory-public-source-checker/1.0'
  'Accept' = 'text/markdown,text/html,application/rss+xml,*/*;q=0.8'
}
$r = Invoke-WebRequest -UseBasicParsing -Uri $env:AI_MEMORY_FETCH_URL -TimeoutSec 20 -Headers $headers
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
        maxBuffer: 20 * 1024 * 1024,
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

async function fetchViaJina(url) {
  const target = url.replace(/^https:\/\//, "http://");
  return fetchText(`https://r.jina.ai/http://${target.replace(/^http:\/\//, "")}`);
}

function unique(values) {
  return [...new Set(values)];
}

function extractStatusIds(text, allowedHandles = []) {
  const handles = allowedHandles.map(normalizeHandle);
  const ids = [];
  const re = /https?:\/\/(?:www\.)?(?:x|twitter)\.com\/([^/\s)]+)\/status\/(\d{12,25})/gi;
  let match;
  while ((match = re.exec(text))) {
    const handle = normalizeHandle(match[1]);
    if (handles.length === 0 || handles.includes(handle)) {
      ids.push(match[2]);
    }
  }
  return unique(ids);
}

function stripMarkdown(raw) {
  return raw
    .replace(/!\[[^\]]*]\([^)]+\)/g, "")
    .replace(/\[([^\]]+)]\(([^)]+)\)/g, "$1")
    .replace(/https?:\/\/t\.co\/\S+/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function decodeHtml(raw) {
  return String(raw || "")
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&nbsp;/g, " ");
}

function parseStatusMarkdown(id, text) {
  const titleMatch = text.match(/^Title:\s*([\s\S]*?)\s+on X:\s*"([\s\S]*?)"\s*\/ X/m);
  const authorName = titleMatch ? stripMarkdown(titleMatch[1]) : null;
  let titleText = titleMatch ? stripMarkdown(titleMatch[2]) : null;

  const handleMatch = text.match(/\[@([A-Za-z0-9_]+)]\((?:https?:\/\/)?x\.com\/\1\)/i);
  const linkedHandleMatch = text.match(/\]\((?:https?:\/\/)?x\.com\/([A-Za-z0-9_]+)\)/i);
  const authorHandle = handleMatch
    ? handleMatch[1]
    : linkedHandleMatch
      ? linkedHandleMatch[1]
      : null;

  const postSection = text.split(/## Post|# Conversation|## Conversation/).slice(1).join("\n");
  if (!titleText && postSection) {
    titleText = stripMarkdown(
      postSection
        .split(/\[\d[\d.,]*[KM]? Views]|\[\d[\d.,]*[KM]?M? Views]|## New to X\?|## Trending now/)[0]
        .replace(/\[Log in][\s\S]*?\[Sign up][^\n]*/i, "")
    );
  }

  return {
    id,
    authorName,
    authorHandle,
    text: titleText || "",
    url: `https://x.com/i/status/${id}`,
    createdAt: xPostCreatedAtFromId(id).toISOString(),
    createdAtSource: "twitter_snowflake_id",
  };
}

function classifyPost(post, account) {
  const related = account.relatedHandles.map(normalizeHandle);
  const postHandle = normalizeHandle(post.authorHandle);
  if (postHandle === normalizeHandle(account.handle)) {
    return {
      status: "verified_account_post",
      evidence: "高：Jina Reader 读取 status 详情；发布时间由 X snowflake ID 推算；作者匹配目标账号。",
    };
  }
  if (related.includes(postHandle)) {
    return {
      status: "verified_related_official_post",
      evidence: "中到高：来自目标账号时间线中的相关官方账号；发布时间由 X snowflake ID 推算；需在策略中标注不是目标账号原创。",
    };
  }
  return {
    status: "visible_related_or_repost",
    evidence: "中：来自目标账号公开时间线可见内容，但作者不是目标账号或配置的相关官方账号。",
  };
}

async function checkXAccount(account, args) {
  const diagnostics = [];
  const profileUrl = `https://x.com/${account.handle}`;
  const profile = await fetchViaJina(profileUrl);
  diagnostics.push({
    channel: "jina_profile",
    url: profile.url,
    ok: profile.ok,
    status: profile.status,
    length: profile.text.length,
    error: profile.error || null,
  });

  if (!profile.ok || !profile.text) {
    return {
      source: account.label,
      type: "x",
      dimension: account.dimension,
      profileUrl,
      posts: [],
      diagnostics,
      note: "Jina Reader 未能读取账号页。",
    };
  }

  const statusIds = extractStatusIds(profile.text, account.relatedHandles).slice(0, args.maxPosts);
  const posts = [];
  for (const id of statusIds) {
    const detail = await fetchViaJina(`https://x.com/i/status/${id}`);
    diagnostics.push({
      channel: "jina_status",
      id,
      url: detail.url,
      ok: detail.ok,
      status: detail.status,
      length: detail.text.length,
      error: detail.error || null,
    });
    if (!detail.ok || !detail.text) continue;
    const post = parseStatusMarkdown(id, detail.text);
    const classification = classifyPost(post, account);
    if (args.since && new Date(post.createdAt) <= args.since) continue;
    posts.push({
      ...post,
      account: account.label,
      sourceStatus: classification.status,
      dimension: account.dimension,
      evidence: classification.evidence,
    });
  }

  posts.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

  return {
    source: account.label,
    type: "x",
    dimension: account.dimension,
    profileUrl,
    posts: posts.slice(0, args.maxPosts),
    diagnostics,
    note: statusIds.length
      ? "账号页可读；已按 status 详情和 snowflake 时间筛选。"
      : "账号页可读，但没有抽取到可校验 status 链接；可能是 X 返回置顶/历史推荐或无链接摘要。",
  };
}

function xiaohongshuStatusFromText(text) {
  if (/登录即可查看/.test(text) || /TA 还没有发布任何内容/.test(text)) {
    return {
      status: "login_or_public_grid_unavailable",
      note: "公开 Reader 通道只暴露账号元信息或登录提示，未暴露可采信笔记列表。",
      evidence: "低",
    };
  }

  const noteLinks = unique(
    [...text.matchAll(/https?:\/\/(?:www\.)?xiaohongshu\.com\/(?:explore|discovery\/item)\/[A-Za-z0-9]+/gi)].map(
      (match) => match[0]
    )
  );
  if (noteLinks.length === 0) {
    return {
      status: "public_profile_metadata_only",
      note: "公开 Reader 通道只暴露账号元信息，没有稳定笔记 URL、发布时间或正文。",
      evidence: "低",
    };
  }

  const noteTitleCandidates = unique(
    text
      .split(/\r?\n/)
      .map((line) => stripMarkdown(line))
      .filter((line) => line.length >= 6 && !/用户协议|隐私政策|登录|关注|粉丝|获赞|ICP备|营业执照|URL Source|Markdown Content|小红书号|IP属地|收藏内容不可见/.test(line))
  ).slice(0, 12);

  return {
    status: noteTitleCandidates.length ? "visible_titles_unverified_time" : "no_visible_notes",
    note: noteTitleCandidates.length
      ? "公开通道暴露疑似标题，但没有稳定发布时间和正文。"
      : "公开通道未暴露笔记列表。",
    evidence: noteTitleCandidates.length ? "低到中" : "低",
    titles: noteTitleCandidates,
  };
}

async function checkXiaohongshuAccount(account) {
  const diagnostics = [];
  const rawProfile = await fetchText(account.url, {
    timeoutMs: 30000,
    headers: { "accept-language": "zh-CN,zh;q=0.9,en;q=0.8" },
  });
  diagnostics.push({
    channel: "raw_profile_html",
    url: rawProfile.url,
    ok: rawProfile.ok,
    status: rawProfile.status,
    length: rawProfile.text.length,
    error: rawProfile.error || null,
  });

  const rawTitles = extractXiaohongshuSsrTitles(rawProfile.text || "");
  const result = await fetchViaJina(account.url);
  diagnostics.push({
    channel: "jina_profile",
    url: result.url,
    ok: result.ok,
    status: result.status,
    length: result.text.length,
    error: result.error || null,
  });

  const status =
    rawTitles.length > 0
      ? {
          status: "visible_titles_raw_html_unverified_time",
          note:
            "原始公开 HTML/SSR 暴露可见笔记标题，但没有稳定单条笔记 URL、发布时间或正文；可用于主题温度和候选池，不可当作完整事实正文。",
          evidence: "低到中",
          titles: rawTitles.slice(0, 20),
        }
      : xiaohongshuStatusFromText(result.text || "");
  return {
    source: account.label,
    type: "xiaohongshu",
    dimension: account.dimension,
    profileUrl: account.url,
    posts: [],
    ...status,
    diagnostics,
  };
}

function extractXiaohongshuSsrTitles(html) {
  if (!html) return [];
  const items = [];
  const noteItemRe = /<section class="note-item"[\s\S]*?<\/section>/g;
  let match;
  while ((match = noteItemRe.exec(html))) {
    const block = match[0];
    const titleMatch = block.match(/class="title"[\s\S]*?<span[^>]*>([\s\S]*?)<\/span>/);
    if (!titleMatch) continue;
    const title = decodeHtml(titleMatch[1].replace(/<[^>]+>/g, "")).replace(/\s+/g, " ").trim();
    if (!title) continue;
    const pinned = block.includes("置顶") || block.includes("\\u7f6e\\u9876");
    items.push(`${pinned ? "[置顶] " : ""}${title}`);
  }

  const directTitles = [...html.matchAll(/<a[^>]+class="title"[\s\S]*?<span[^>]*>([\s\S]*?)<\/span>/g)].map((m) =>
    decodeHtml(m[1].replace(/<[^>]+>/g, "")).replace(/\s+/g, " ").trim()
  );

  return unique([...items, ...directTitles]).filter(
    (title) =>
      title.length >= 4 &&
      !/用户协议|隐私政策|小红书号|IP属地|登录即可|收藏内容不可见|你的生活兴趣社区/.test(title)
  );
}

function formatBeijing(iso) {
  return new Intl.DateTimeFormat("zh-CN", {
    timeZone: "Asia/Shanghai",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(new Date(iso));
}

function renderMarkdown(results, args) {
  const now = new Date();
  const lines = [];
  lines.push("# Realtime Public Source Check");
  lines.push("");
  lines.push(`Run time: ${now.toISOString()} (${formatBeijing(now.toISOString())} Beijing)`);
  if (args.since) {
    lines.push(`Since: ${args.since.toISOString()} (${formatBeijing(args.since.toISOString())} Beijing)`);
  }
  lines.push("");
  lines.push("## Summary");
  lines.push("");
  lines.push("| Source | Status | New verified items | Dimension | Evidence | Note |");
  lines.push("| --- | --- | ---: | --- | --- | --- |");
  for (const result of results) {
    const count = result.posts ? result.posts.length : 0;
    const status = count > 0 ? "可读取" : result.status || "未取得可采信新内容";
    const evidence = count > 0 ? "中到高" : result.evidence || "低";
    lines.push(
      `| ${result.source} | ${status} | ${count} | ${result.dimension} | ${evidence} | ${result.note || ""} |`
    );
  }
  lines.push("");

  for (const result of results) {
    lines.push(`## ${result.source}`);
    lines.push("");
    if (result.posts && result.posts.length) {
      lines.push("| Beijing time | Author | Type | Link | Content summary | Evidence |");
      lines.push("| --- | --- | --- | --- | --- | --- |");
      for (const post of result.posts) {
        const author = post.authorHandle ? `@${post.authorHandle}` : post.authorName || "";
        lines.push(
          `| ${formatBeijing(post.createdAt)} | ${author} | ${post.sourceStatus} | ${post.url} | ${post.text.replace(/\|/g, "/")} | ${post.evidence} |`
        );
      }
      lines.push("");
    } else if (result.titles && result.titles.length) {
      lines.push("Visible title candidates without reliable time/body:");
      for (const title of result.titles) lines.push(`- ${title}`);
      lines.push("");
    } else {
      lines.push(`${result.note || "No verified public items were extracted."}`);
      lines.push("");
    }

    lines.push("Diagnostics:");
    for (const diagnostic of result.diagnostics || []) {
      const idPart = diagnostic.id ? ` id=${diagnostic.id}` : "";
      const errorPart = diagnostic.error ? ` error=${diagnostic.error}` : "";
      lines.push(
        `- ${diagnostic.channel}${idPart}: ok=${diagnostic.ok} status=${diagnostic.status} length=${diagnostic.length}${errorPart}`
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

  for (const account of DEFAULT_X_ACCOUNTS) {
    results.push(await checkXAccount(account, args));
  }
  for (const account of DEFAULT_XHS_ACCOUNTS) {
    results.push(await checkXiaohongshuAccount(account, args));
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
