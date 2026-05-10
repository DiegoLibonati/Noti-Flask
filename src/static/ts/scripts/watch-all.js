import { spawn } from "child_process";

/**
 * @param {string} command
 * @param {string[]} args
 * @param {string} label
 * @param {((msg: string) => void) | undefined} onOutput
 */
function run(command, args, label, onOutput) {
  const proc = spawn(command, args, { shell: true });

  proc.stdout.on("data", (data) => {
    const msg = data.toString().trim();
    console.log(`[${label}] ${msg}`);
    onOutput?.(msg);
  });

  proc.stderr.on("data", (data) => {
    console.error(`[${label}] ${data.toString().trim()}`);
  });

  proc.on("exit", (code) => {
    console.log(`[${label}] exited with code ${code}`);
  });

  return proc;
}

console.log("[watch] Starting tsc + sass + tsc-alias watchers...");

run(
  "npx",
  [
    "sass",
    "--watch",
    "../scss/main.scss:../css/main.css",
    "--style=compressed",
    "--no-source-map",
  ],
  "sass"
);

run(
  "npx",
  [
    "tsc",
    "-p",
    "tsconfig.app.json",
    "--watch",
    "--preserveWatchOutput",
    "--watchFile",
    "dynamicPriorityPolling",
    "--watchDirectory",
    "fixedPollingInterval",
  ],
  "tsc",
  (msg) => {
    if (msg.includes("Found 0 errors. Watching for file changes.")) {
      console.log(
        "[watch] Compilation done, running tsc-alias + fix-imports..."
      );
      spawn("npx", ["tsc-alias", "-p", "tsconfig.app.json"], {
        shell: true,
      }).on("exit", () => {
        spawn("node", ["scripts/fix-imports.js"], {
          stdio: "inherit",
          shell: true,
        });
      });
    }
  }
);
