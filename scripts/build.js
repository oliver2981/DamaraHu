/**
 * Build script: reads content/*.txt and generates js/i18n-data.js
 * Usage: node scripts/build.js
 */
const fs = require("fs");
const path = require("path");

const CONTENT_DIR = path.join(__dirname, "..", "content");
const OUTPUT = path.join(__dirname, "..", "js", "i18n-data.js");

function parseContentFile(filePath) {
  const data = { zh: {}, en: {} };
  const lines = fs.readFileSync(filePath, "utf-8").split("\n");
  for (const line of lines) {
    // Skip comments and blank lines
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;

    // Match: key.zh = value  OR  key.en = value
    const m = trimmed.match(/^(.+?)\.(zh|en)\s*=\s*(.*)$/);
    if (m) {
      const key = m[1].trim();
      const lang = m[2];
      const value = m[3];
      if (value) {
        data[lang][key] = value;
      }
    }
  }
  return data;
}

// Read all txt files
const files = fs.readdirSync(CONTENT_DIR).filter(f => f.endsWith(".txt"));
const zh = {};
const en = {};

for (const file of files) {
  const fileData = parseContentFile(path.join(CONTENT_DIR, file));
  Object.assign(zh, fileData.zh);
  Object.assign(en, fileData.en);
}

// Generate i18n-data.js
const output = [
  "// AUTO-GENERATED from content/*.txt — DO NOT EDIT DIRECTLY",
  "// To change content, edit the .txt files in content/ then run: node scripts/build.js",
  "const I18N = {",
  "  zh: {",
];
for (const key of Object.keys(zh).sort()) {
  output.push(`    '${key}': '${zh[key].replace(/'/g, "\\'")}',`);
}
output.push("  },");
output.push("");
output.push("  en: {");
for (const key of Object.keys(en).sort()) {
  output.push(`    '${key}': '${en[key].replace(/'/g, "\\'")}',`);
}
output.push("  }");
output.push("};");

fs.writeFileSync(OUTPUT, output.join("\n"), "utf-8");

console.log(`Generated ${OUTPUT}`);
console.log(`  zh: ${Object.keys(zh).length} keys`);
console.log(`  en: ${Object.keys(en).length} keys`);
