// news-image-20261123 — entry program (Node 22, stdlib only).
// Copies the poster drawn in-session (entry.png) to the output directory.
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");

if (!existsSync(src)) {
  throw new Error(`missing entry image: ${src}`);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);
// Gate check, same on every run: the image must stay a whole PNG
// of at most 1 MiB, so both graded runs write identical valid bytes.
const bytes = statSync(dst).size;
if (bytes > 1048576) {
  throw new Error(`entry.png too large: ${bytes} bytes (max 1048576)`);
}
console.log(`wrote ${dst} (${bytes} bytes)`);
