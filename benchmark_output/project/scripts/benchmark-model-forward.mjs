import fs from "node:fs";
import path from "node:path";
import net from "node:net";
import { fileURLToPath } from "node:url";

const runtime = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../storage/benchmark-design");
const server = net.createServer((client) => {
  let worker;
  try { worker = JSON.parse(fs.readFileSync(path.join(runtime, "gpu/worker-info.json"), "utf8")); }
  catch { return client.destroy(); }
  if (!net.isIPv4(worker.ip) || worker.port !== 18013) return client.destroy();
  const upstream = net.connect(worker.port, worker.ip);
  upstream.on("error", () => client.destroy());
  client.on("error", () => upstream.destroy());
  client.on("close", () => upstream.destroy());
  upstream.on("close", () => client.destroy());
  client.pipe(upstream);
  upstream.pipe(client);
});
server.listen(18013, "127.0.0.1", () => console.log("Checkpoint transport listening on 127.0.0.1:18013"));
const timer = setInterval(() => {
  if (fs.existsSync(path.join(runtime, "gpu/release.json"))) {
    clearInterval(timer);
    server.close();
  }
}, 10000);
