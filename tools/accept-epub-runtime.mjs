#!/usr/bin/env node
// Open the actual archived Javanese EPUB in epub.js and exercise representative reflow.

import crypto from "node:crypto";
import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

function parseArgs(argv) {
  const result = {};
  for (let i = 0; i < argv.length; i += 2) {
    if (!argv[i]?.startsWith("--") || argv[i + 1] === undefined) throw new Error("Arguments must be --name value pairs");
    result[argv[i].slice(2)] = argv[i + 1];
  }
  for (const key of ["epub", "audit", "output", "epub-js", "jszip", "puppeteer"] ) {
    if (!result[key]) throw new Error(`Missing --${key}`);
  }
  return result;
}

const args = parseArgs(process.argv.slice(2));
const epubPath = path.resolve(args.epub);
const auditPath = path.resolve(args.audit);
const outputPath = path.resolve(args.output);
const screenshotDir = path.join(path.dirname(outputPath), "runtime-screenshots");
const epubJsPath = path.resolve(args["epub-js"]);
const jsZipPath = path.resolve(args.jszip);
const puppeteerPath = path.resolve(args.puppeteer);
const require = createRequire(import.meta.url);
const puppeteer = require(puppeteerPath);

function sha256(payload) {
  return crypto.createHash("sha256").update(payload).digest("hex");
}

const epubBytes = fs.readFileSync(epubPath);
const audit = JSON.parse(fs.readFileSync(auditPath, "utf8"));
if (audit.status !== "PASS") throw new Error("Independent audit must pass before runtime acceptance");
if (sha256(epubBytes) !== audit.artifact.sha256) throw new Error("EPUB digest drift before runtime acceptance");
fs.mkdirSync(screenshotDir, { recursive: true });

const harness = `<!doctype html><html lang="jv-Latn-ID"><head><meta charset="utf-8"/>
<title>OpenLogic Javanese EPUB runtime harness</title><style>html,body{margin:0}#area{width:320px;height:900px;overflow:hidden}</style></head>
<body><main><div id="area"></div></main><script src="/jszip.min.js"></script><script src="/epub.min.js"></script></body></html>`;
const serverRequests = [];
const server = http.createServer((request, response) => {
  const url = new URL(request.url || "/", "http://127.0.0.1");
  serverRequests.push({ method: request.method || "GET", path: url.pathname });
  const resources = {
    "/harness.html": { type: "text/html; charset=utf-8", body: Buffer.from(harness) },
    "/jszip.min.js": { type: "text/javascript; charset=utf-8", body: fs.readFileSync(jsZipPath) },
    "/epub.min.js": { type: "text/javascript; charset=utf-8", body: fs.readFileSync(epubJsPath) },
    "/book.epub": { type: "application/epub+zip", body: epubBytes },
    "/favicon.ico": { type: "image/x-icon", body: Buffer.alloc(0) },
  };
  const resource = resources[url.pathname];
  if (!resource) {
    response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    response.end("not found");
    return;
  }
  response.writeHead(200, {
    "Content-Type": resource.type,
    "Content-Length": resource.body.length,
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff",
  });
  if (request.method === "HEAD") response.end();
  else response.end(resource.body);
});
await new Promise((resolve, reject) => {
  server.once("error", reject);
  server.listen(0, "127.0.0.1", resolve);
});
const address = server.address();
if (!address || typeof address === "string") throw new Error("Failed to bind loopback server");
const origin = `http://127.0.0.1:${address.port}`;

const browser = await puppeteer.launch({
  headless: true,
  executablePath: puppeteer.executablePath(),
  args: ["--disable-speech-api", "--no-sandbox"],
});
const page = await browser.newPage();
await page.setViewport({ width: 320, height: 900, deviceScaleFactor: 1 });
const externalRequests = [];
const requestFailures = [];
const pageErrors = [];
const consoleErrors = [];
const browserDiagnostics = [];
const expectedBrowserDiagnostics = [
  /^Permissions policy violation: unload is not allowed in this document\.$/,
];
await page.setRequestInterception(true);
page.on("request", (request) => {
  const url = request.url();
  if (url.startsWith(origin + "/") || url.startsWith("blob:") || url.startsWith("data:") || url === "about:blank") request.continue();
  else {
    externalRequests.push(url);
    request.abort("blockedbyclient");
  }
});
page.on("requestfailed", (request) => requestFailures.push({ url: request.url(), error: request.failure()?.errorText || "unknown" }));
page.on("pageerror", (error) => pageErrors.push(String(error)));
page.on("console", (message) => {
  if (message.type() !== "error") return;
  const diagnostic = message.text();
  if (expectedBrowserDiagnostics.some((pattern) => pattern.test(diagnostic))) browserDiagnostics.push(diagnostic);
  else consoleErrors.push(diagnostic);
});
await page.evaluateOnNewDocument(() => {
  window.__jvSpeechCalls = [];
  Object.defineProperty(window, "speechSynthesis", {
    configurable: true,
    value: {
      getVoices: () => [],
      speak: (utterance) => window.__jvSpeechCalls.push(String(utterance?.text || "")),
      cancel: () => {}, pause: () => {}, resume: () => {}, addEventListener: () => {}, removeEventListener: () => {},
    },
  });
});

const representatives = [
  "text/title.xhtml",
  "text/olp-0008.xhtml",
  "text/olp-0017.xhtml",
  "text/olp-0018.xhtml",
  "text/olp-0024.xhtml",
  "text/bibliography.xhtml",
];
let runtime;
try {
  await page.goto(origin + "/harness.html", { waitUntil: "load", timeout: 60000 });
  runtime = await page.evaluate(async ({ representatives }) => {
    const book = ePub("/book.epub", { openAs: "epub" });
    await book.ready;
    const [navigation, metadata] = await Promise.all([book.loaded.navigation, book.loaded.metadata]);
    const packageText = await book.archive.getText("/" + book.container.packagePath);
    const spine = book.spine.spineItems;
    const countToc = (items) => items.reduce((total, item) => total + (item.href ? 1 : 0) + countToc(item.subitems || []), 0);
    const counts = {
      spine_items: spine.length,
      unique_spine_hrefs: new Set(spine.map((section) => section.href)).size,
      toc_link_items: countToc(navigation.toc || []),
      xhtml_documents_loaded: 0,
      mathml_roots: 0,
      images: 0,
      scripts: 0,
      empty_titles: 0,
      wrong_language_documents: 0,
      empty_body_documents: 0,
      math_namespace_errors: 0,
      math_alttext_missing: 0,
      math_unrendered_commands: 0,
      image_alt_missing: 0,
    };
    const sectionFindings = [];
    for (const section of spine) {
      try {
        await section.load(book.load.bind(book));
        const doc = section.document;
        const title = (doc.querySelector("title")?.textContent || "").trim();
        const lang = doc.documentElement.getAttribute("lang") || doc.documentElement.getAttribute("xml:lang") || "";
        const maths = Array.from(doc.getElementsByTagNameNS("http://www.w3.org/1998/Math/MathML", "math"));
        const images = Array.from(doc.querySelectorAll("img"));
        counts.xhtml_documents_loaded += 1;
        counts.mathml_roots += maths.length;
        counts.images += images.length;
        counts.scripts += doc.querySelectorAll("script").length;
        counts.empty_titles += title ? 0 : 1;
        counts.wrong_language_documents += lang === "jv-Latn-ID" ? 0 : 1;
        counts.empty_body_documents += (doc.body?.textContent || "").trim() ? 0 : 1;
        counts.math_namespace_errors += Array.from(doc.getElementsByTagName("math")).filter((node) => node.namespaceURI !== "http://www.w3.org/1998/Math/MathML").length;
        counts.math_alttext_missing += maths.filter((node) => !(node.getAttribute("alttext") || "").trim()).length;
        counts.math_unrendered_commands += maths.flatMap((node) => Array.from(node.querySelectorAll("mi"))).filter((node) => (node.textContent || "").startsWith("\\")).length;
        counts.image_alt_missing += images.filter((node) => !(node.getAttribute("alt") || "").trim()).length;
      } catch (error) {
        sectionFindings.push({ href: section.href, error: String(error) });
      } finally {
        section.unload();
      }
    }
    const rendition = book.renderTo("area", {
      width: 320, height: 900, flow: "scrolled-doc", manager: "default", allowScriptedContent: false,
    });
    const rendered = [];
    for (const href of representatives) {
      const row = { href, failures: [] };
      try {
        await rendition.display(href);
        await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
        const contents = rendition.getContents();
        const doc = contents[0]?.document;
        if (!doc) throw new Error("Rendition did not expose a document");
        const mainTextCharacters = (doc.querySelector("main")?.textContent || doc.body?.textContent || "").trim().length;
        const baselineOverflow = doc.documentElement.scrollWidth > doc.documentElement.clientWidth + 1;
        const style = doc.createElement("style");
        style.textContent = "body,body *{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}p{margin-block-end:2em!important}";
        doc.head.appendChild(style);
        await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
        const spacedOverflow = doc.documentElement.scrollWidth > doc.documentElement.clientWidth + 1;
        style.textContent = "html{font-size:200%!important}";
        await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
        const scaledOverflow = doc.documentElement.scrollWidth > doc.documentElement.clientWidth + 1;
        if (mainTextCharacters < 80) row.failures.push("insufficient-readable-content");
        if (doc.querySelectorAll("script").length) row.failures.push("scripted-content-present");
        if (baselineOverflow) row.failures.push("320px-global-horizontal-overflow");
        if (spacedOverflow) row.failures.push("text-spacing-global-horizontal-overflow");
        if (scaledOverflow) row.failures.push("200-percent-global-horizontal-overflow");
        row.title = (doc.querySelector("title")?.textContent || "").trim();
        row.main_text_characters = mainTextCharacters;
        row.mathml_roots = doc.getElementsByTagNameNS("http://www.w3.org/1998/Math/MathML", "math").length;
        row.images = doc.querySelectorAll("img").length;
        row.baseline_global_horizontal_overflow = baselineOverflow;
        row.text_spacing_global_horizontal_overflow = spacedOverflow;
        row.two_hundred_percent_global_horizontal_overflow = scaledOverflow;
      } catch (error) {
        row.failures.push("render-error");
        row.error = String(error);
      }
      rendered.push(row);
    }
    rendition.destroy();
    book.destroy();
    return {
      engine: {
        name: "epub.js", version: "0.3.93", archived_epub_opened: true,
        native_mathml_element_supported: typeof MathMLElement !== "undefined" && document.createElementNS("http://www.w3.org/1998/Math/MathML", "math") instanceof MathMLElement,
      },
      metadata: { title: metadata.title, language: metadata.language, layout: metadata.layout, identifier: metadata.identifier, description: metadata.description },
      package_guards: {
        upstream_revision_present: packageText.includes("9620cc73f9c8e0ad003c514a5d3748f29611c4c0"),
        bounded_scope_present: packageText.includes("24 saka 722"),
        machine_authorship_present: packageText.includes("OpenAI Codex"),
      },
      counts, section_findings: sectionFindings, representative_renders: rendered,
      speech_calls: window.__jvSpeechCalls.length,
    };
  }, { representatives });

  for (const representative of representatives) {
    await page.evaluate(async (href) => {
      const book = ePub("/book.epub", { openAs: "epub" });
      await book.ready;
      const area = document.querySelector("#area");
      area.innerHTML = "";
      area.style.width = "320px";
      area.style.height = "900px";
      const rendition = book.renderTo(area, { width: 320, height: 900, flow: "scrolled-doc", manager: "default", allowScriptedContent: false });
      await rendition.display(href);
      await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
      window.__screenshotBook = book;
      window.__screenshotRendition = rendition;
    }, representative);
    const filename = representative.replace(/[^A-Za-z0-9]+/g, "-").replace(/^-|-$/g, "") + ".png";
    await page.screenshot({ path: path.join(screenshotDir, filename), clip: { x: 0, y: 0, width: 320, height: 900 } });
    await page.evaluate(() => {
      window.__screenshotRendition?.destroy();
      window.__screenshotBook?.destroy();
      document.querySelector("#area").innerHTML = "";
    });
  }
} finally {
  await page.close();
  await browser.close();
  await new Promise((resolve) => server.close(resolve));
}

const failures = [];
function expect(condition, label) { if (!condition) failures.push(label); }
expect(runtime.engine.archived_epub_opened, "archived-epub-not-opened");
expect(runtime.engine.native_mathml_element_supported, "native-mathml-elements-unavailable");
expect(runtime.metadata.title === "OpenLogic: Himpunan, Relasi, lan Fungsi", "metadata-title-mismatch");
expect(runtime.metadata.language === "jv-Latn-ID", "metadata-language-mismatch");
expect(runtime.metadata.layout === "reflowable", "metadata-layout-mismatch");
expect(runtime.package_guards.upstream_revision_present, "upstream-provenance-missing");
expect(runtime.package_guards.bounded_scope_present, "bounded-scope-missing");
expect(runtime.package_guards.machine_authorship_present, "machine-authorship-missing");
expect(runtime.counts.spine_items === audit.metrics.spine_documents, "spine-count-mismatch");
expect(runtime.counts.unique_spine_hrefs === runtime.counts.spine_items, "spine-hrefs-not-unique");
expect(runtime.counts.xhtml_documents_loaded === audit.metrics.spine_documents, "spine-load-count-mismatch");
expect(runtime.counts.mathml_roots === audit.metrics.mathml_roots_checked, "mathml-count-mismatch");
expect(runtime.counts.images === audit.metrics.images_checked, "image-count-mismatch");
expect(runtime.counts.scripts === 0, "scripts-present");
expect(runtime.counts.empty_titles === 0, "empty-title");
expect(runtime.counts.wrong_language_documents === 0, "wrong-language-document");
expect(runtime.counts.empty_body_documents === 0, "empty-body-document");
expect(runtime.counts.math_namespace_errors === 0, "mathml-namespace-error");
expect(runtime.counts.math_alttext_missing === 0, "mathml-alttext-missing");
expect(runtime.counts.math_unrendered_commands === 0, "mathml-unrendered-command");
expect(runtime.counts.image_alt_missing === 0, "image-alt-missing");
expect(runtime.section_findings.length === 0, "spine-load-failure");
expect(runtime.representative_renders.every((row) => row.failures.length === 0), "representative-render-failure");
expect(runtime.speech_calls === 0, "unexpected-speech-call");
expect(externalRequests.length === 0, "external-network-request");
expect(requestFailures.length === 0, "request-failure");
expect(pageErrors.length === 0, "browser-page-error");
expect(consoleErrors.length === 0, "browser-console-error");

const screenshots = fs.readdirSync(screenshotDir).filter((name) => name.endsWith(".png")).sort().map((name) => {
  const bytes = fs.readFileSync(path.join(screenshotDir, name));
  return { name, bytes: bytes.length, sha256: sha256(bytes) };
});
const result = {
  schema: "openlogic-jv-epub-runtime-acceptance/1",
  status: failures.length ? "FAIL" : "PASS",
  artifact: { path: path.basename(epubPath), bytes: epubBytes.length, sha256: sha256(epubBytes) },
  viewport_css_pixels: { width: 320, height: 900 },
  probes: { baseline_reflow: true, text_spacing: true, magnification_200_percent: true, transport: "ephemeral loopback only", external_requests_blocked: true, speech_synthesis_stubbed: true },
  runtime,
  external_request_attempts: externalRequests,
  request_failures: requestFailures,
  page_errors: pageErrors,
  console_errors: consoleErrors,
  expected_browser_diagnostics: browserDiagnostics,
  screenshots,
  failures,
  runner: { path: "tools/accept-epub-runtime.mjs", sha256: sha256(fs.readFileSync(fileURLToPath(import.meta.url))) },
};
fs.writeFileSync(outputPath, JSON.stringify(result, null, 2) + "\n");
process.stdout.write(JSON.stringify(result, null, 2) + "\n");
process.exitCode = failures.length ? 1 : 0;
