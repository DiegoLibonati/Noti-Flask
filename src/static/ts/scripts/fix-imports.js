import { globby } from "globby";
import { readFileSync, writeFileSync } from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const baseDir = path.resolve(__dirname, "../../js");
console.log("[fix-imports] Base dir:", baseDir);

const files = await globby(["**/*.js"], { cwd: baseDir, absolute: true });
console.log("[fix-imports] Found", files.length, ".js files");

let totalModified = 0;

for (const file of files) {
  let content = readFileSync(file, "utf8");
  let updated = content;

  updated = updated.replace(
    /from\s+["'](\.{1,2}\/[^"']+)(?<!\.js)["']/g,
    'from "$1.js"'
  );

  updated = updated.replace(/from\s+["']@src\/([^"']+)["']/g, (_, relPath) => {
    const depth = file.replace(baseDir, "").split("/").length - 2;
    const prefix = depth > 0 ? "../".repeat(depth) : "./";
    return `from "${prefix}${relPath}.js"`;
  });

  if (updated !== content) {
    writeFileSync(file, updated, "utf8");
    console.log(`[fix-imports] Fixed imports in: ${path.relative(process.cwd(), file)}`);
    totalModified++;
  }
}

console.log(`[fix-imports] Completed. Total modified files: ${totalModified}`);
