import { DurableObject } from "cloudflare:workers";
import template from "./hero-template.js";

// A single counter instance; requests are processed one at a time, so concurrent visits are never lost.
export class VisitCounter extends DurableObject {
  async increment() {
    const count = ((await this.ctx.storage.get("count")) ?? 0) + 1;
    await this.ctx.storage.put("count", count);
    return count;
  }
}

function counterBadge(count) {
  const label = `${count.toLocaleString("en-US")} views`;
  const width = 44 + label.length * 8.4;
  const x = 1000 - 24 - width;
  return `<g class="in d3">
<rect x="${x}" y="20" width="${width}" height="32" rx="16" fill="#0b3d31" stroke="#45BB92" stroke-opacity=".6"/>
<circle cx="${x + 18}" cy="36" r="4.5" fill="#7FD3B2"><animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>
<text x="${x + 32}" y="41" class="t" font-size="14" fill="#c9eee0">${label}</text>
</g>`;
}

const HEADERS = {
  "content-type": "image/svg+xml; charset=utf-8",
  // Keep GitHub's image proxy (camo) from caching, so it fetches again on every visit.
  "cache-control": "no-cache, no-store, must-revalidate, max-age=0",
};

export default {
  async fetch(request, env) {
    const { pathname } = new URL(request.url);
    if (pathname !== "/hero.svg") {
      return Response.redirect("https://github.com/moosyroot", 302);
    }
    if (request.method !== "GET") {
      return new Response(null, { headers: HEADERS });
    }

    let badge = "";
    try {
      const counter = env.COUNTER.get(env.COUNTER.idFromName("moosyroot-profile"));
      badge = counterBadge(await counter.increment());
    } catch (error) {
      // Even if the counter fails, Mr. Moosy should still show up.
      console.error("failed to increment counter", error);
    }
    return new Response(template.replace("<!--COUNTER-->", badge), { headers: HEADERS });
  },
};
