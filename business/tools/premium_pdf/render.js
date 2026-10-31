// Chromium PDF renderer for the Hagiazo premium documents.
// usage: node render.js jobs.json
const fs = require("fs"), path = require("path");
const { chromium } = require("/opt/node22/lib/node_modules/playwright");
const { execFileSync } = require("child_process");

const jobs = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const MARGIN = { top: "24mm", bottom: "24mm", left: "22mm", right: "22mm" };

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext();
  for (const j of jobs) {
    const page = await ctx.newPage();
    const tmpdir = path.dirname(j.body);
    const stem = path.basename(j.out, ".pdf").replace(/[^\w]+/g, "_");
    if (j.kind === "doc") {
      await page.goto("file://" + j.cover); await page.evaluate(() => document.fonts.ready);
      const coverPdf = path.join(tmpdir, stem + ".cover.pdf");
      await page.pdf({ path: coverPdf, format: "A4", printBackground: true, margin: { top: 0, bottom: 0, left: 0, right: 0 }, preferCSSPageSize: true });
      await page.goto("file://" + j.body); await page.evaluate(() => document.fonts.ready);
      const bodyPdf = path.join(tmpdir, stem + ".body.pdf");
      await page.pdf({ path: bodyPdf, format: "A4", printBackground: true, margin: MARGIN,
        displayHeaderFooter: true, headerTemplate: j.header, footerTemplate: j.footer });
      fs.mkdirSync(path.dirname(j.out), { recursive: true });
      execFileSync("pdfunite", [coverPdf, bodyPdf, j.out]);
    } else {
      await page.goto("file://" + j.body); await page.evaluate(() => document.fonts.ready);
      fs.mkdirSync(path.dirname(j.out), { recursive: true });
      await page.pdf({ path: j.out, format: "A4", printBackground: true, margin: { top: "16mm", bottom: "16mm", left: "18mm", right: "18mm" } });
    }
    await page.close();
    console.log("✓", j.out);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
