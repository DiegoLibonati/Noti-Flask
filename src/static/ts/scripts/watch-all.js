import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const jsDir = path.resolve(__dirname, "../../js");

console.log("Starting TypeScript + Alias + Fix watchers...");
console.log("JS DIR:", jsDir);

function run(command, args, label, onData) {
  const proc = spawn(command, args, { shell: true });
  proc.stdout.on("data", data => {
    const msg = data.toString();
    console.log(`[${label}] ${msg.trim()}`);
    if (onData) onData(msg);
  });
  proc.stderr.on("data", d => console.error(`[${label} ERROR] ${d}`));
  proc.on("exit", code => console.log(`[${label}] exited with code ${code}`));
  return proc;
}

run(
  "npx",
  [
    "tsc",
    "-p", "tsconfig.app.json",
    "--watch",
    "--preserveWatchOutput",
    "--watchFile", "dynamicPriorityPolling",
    "--watchDirectory", "fixedPollingInterval"
  ],
  "tsc",
  (msg) => {
    if (msg.includes("Found 0 errors. Watching for file changes.")) {
      console.log("[tsc] Compilation complete, running fix-imports...");
      spawn("node", ["scripts/fix-imports.js"], { stdio: "inherit", shell: true });
    }
  }
);

run("npx", ["tsc-alias", "-p", "tsconfig.app.json", "--watch"], "alias");
