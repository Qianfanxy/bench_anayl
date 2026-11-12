import http from "node:http";
import { createHash } from "node:crypto";
import { pathToFileURL } from "node:url";

// Transport compatibility only: the direct runner still owns the agent
// loop, MCP tools, trace recording, conversion and quality checks.
export function createResponsesAdapter({ upstream = "https://tokenhub.sensetime.com", fetchImpl = fetch,
  modelId = "gpt-6-astra/azure_L/sfl", log = console.log } = {}) {
  const origin = new URL(upstream);
  if (origin.username || origin.password || origin.search || origin.hash) throw new Error("Invalid upstream");
  const outputs = new Map();
  const key = (calls) => createHash("sha256").update(JSON.stringify(calls)).digest("hex");
  const callsOf = (items) => items.filter((item) => item.type === "function_call").map((item) =>
    ({ id: item.call_id, name: item.name, arguments: item.arguments }));
  const chatCalls = (calls) => calls.map((call) =>
    ({ id: call.id, name: call.function.name, arguments: call.function.arguments }));
  const content = (value, assistant = false) => {
    if (typeof value === "string") return [{ type: assistant ? "output_text" : "input_text", text: value }];
    return (value || []).map((part) => {
      if (part.type === "text") return { type: assistant ? "output_text" : "input_text", text: part.text };
      if (part.type === "image_url" && !assistant) return { type: "input_image", image_url: part.image_url.url,
        ...(part.image_url.detail ? { detail: part.image_url.detail } : {}) };
      throw new Error(`Unsupported content type: ${part.type}`);
    });
  };
  function toResponses(body) {
    if (body.model !== modelId || body.stream) throw new Error("Only the configured non-streaming model is supported");
    const input = [];
    for (const message of body.messages || []) {
      if (message.role === "tool") {
        input.push({ type: "function_call_output", call_id: message.tool_call_id, output: message.content });
      } else if (message.role === "assistant" && message.tool_calls?.length) {
        const cached = outputs.get(key(chatCalls(message.tool_calls)));
        if (cached) {
          // Replay the exact output, including encrypted reasoning, for tool continuations.
          input.push(...cached);
        } else {
          if (message.content) input.push({ role: "assistant", content: content(message.content, true) });
          for (const call of message.tool_calls) input.push({ type: "function_call", call_id: call.id,
            name: call.function.name, arguments: call.function.arguments });
        }
      } else {
        input.push({ role: message.role, content: content(message.content, message.role === "assistant") });
      }
    }
    const request = { model: body.model, input, store: false, include: ["reasoning.encrypted_content"],
      reasoning: { effort: body.reasoning_effort && body.reasoning_effort !== "none" ? body.reasoning_effort : "low" } };
    if (body.max_tokens !== undefined) request.max_output_tokens = body.max_tokens;
    if (body.max_completion_tokens !== undefined) request.max_output_tokens = body.max_completion_tokens;
    if (body.tools) request.tools = body.tools.map((tool) => {
      if (tool.type !== "function") throw new Error("Unsupported tool type");
      return { type: "function", ...tool.function, strict: tool.function.strict ?? false };
    });
    if (body.tool_choice !== undefined) request.tool_choice = typeof body.tool_choice === "string"
      ? body.tool_choice : { type: "function", name: body.tool_choice.function.name };
    if (body.parallel_tool_calls !== undefined) request.parallel_tool_calls = body.parallel_tool_calls;
    for (const name of ["temperature", "top_p", "metadata"]) if (body[name] !== undefined) request[name] = body[name];
    return request;
  }
  function toChat(response) {
    if (!Array.isArray(response.output)) throw new Error("Upstream response has no output array");
    if (response.status === "failed" || response.error) throw new Error("Upstream response failed");
    const calls = callsOf(response.output);
    if (calls.length) outputs.set(key(calls), response.output);
    // The eval has bounded agent turns. Evict whole outputs, never individual reasoning items.
    while (outputs.size > 2000) outputs.delete(outputs.keys().next().value);
    const text = response.output.filter((item) => item.type === "message")
      .flatMap((item) => item.content || []).filter((part) => part.type === "output_text").map((part) => part.text).join("");
    const toolCalls = calls.map((call) => ({ id: call.id, type: "function", function: { name: call.name, arguments: call.arguments } }));
    const usage = response.usage;
    return { id: response.id, object: "chat.completion", created: response.created_at, model: response.model,
      choices: [{ index: 0, message: { role: "assistant", content: text || null,
        ...(toolCalls.length ? { tool_calls: toolCalls } : {}) },
      finish_reason: response.status === "incomplete" ? "length" : toolCalls.length ? "tool_calls" : "stop" }],
      ...(usage ? { usage: { prompt_tokens: usage.input_tokens, completion_tokens: usage.output_tokens,
        total_tokens: usage.total_tokens, prompt_tokens_details: usage.input_tokens_details,
        completion_tokens_details: usage.output_tokens_details } } : {}) };
  }
  const server = http.createServer(async (req, res) => {
    const send = (status, value) => { res.writeHead(status, { "content-type": "application/json" }); res.end(JSON.stringify(value)); };
    const abort = new AbortController();
    const timeout = setTimeout(() => abort.abort(), 1200000);
    res.on("close", () => { if (!res.writableEnded) abort.abort(); });
    try {
      if (!req.headers.authorization) return send(401, { error: { message: "Authorization required" } });
      if (req.method === "GET" && req.url === "/v1/models") {
        const response = await fetchImpl(new URL("/v1/models", origin), {
          headers: { authorization: req.headers.authorization }, signal: abort.signal });
        return send(response.status, await response.json());
      }
      if (req.method !== "POST" || req.url !== "/v1/chat/completions") return send(404, { error: { message: "Unknown route" } });
      const chunks = []; let size = 0;
      for await (const chunk of req) {
        size += chunk.length;
        if (size > 64 * 1024 * 1024) return send(413, { error: { message: "Request too large" } });
        chunks.push(chunk);
      }
      let request;
      try { request = toResponses(JSON.parse(Buffer.concat(chunks).toString("utf8"))); }
      catch (error) { return send(400, { error: { message: error.message } }); }
      const response = await fetchImpl(new URL("/v1/responses", origin), { method: "POST",
        headers: { authorization: req.headers.authorization, "content-type": "application/json" },
        body: JSON.stringify(request), signal: abort.signal });
      const value = await response.json();
      log(JSON.stringify({ at: new Date().toISOString(), status: response.status, id: value.id,
        output_types: value.output?.map((item) => item.type), usage: value.usage }));
      if (!response.ok) return send(response.status, value);
      send(200, toChat(value));
    } catch (error) {
      log(JSON.stringify({ at: new Date().toISOString(), error: error.name }));
      if (!res.headersSent) send(502, { error: { message: "Responses transport failed", type: error.name } });
      else res.destroy();
    } finally { clearTimeout(timeout); }
  });
  server.requestTimeout = 1200000;
  return { server, toResponses, toChat };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const { server } = createResponsesAdapter();
  server.listen(18185, "127.0.0.1", () => console.log("Responses transport adapter listening on 127.0.0.1:18185"));
}
