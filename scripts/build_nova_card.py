"""Builds the Nova product card (assets/nova-card.svg).

Usage: python scripts/build_nova_card.py assets/nova-card.svg
Same green theme as the hero; the icon is a 128 px copy of icon.png from the Nova
repository, module icons are from Lucide (ISC license).
"""
import sys

NOVA_ICON = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAMAAAD04JH5AAAA5FBMVEUAAAACDA0DHB0CExMFXFwIuLgF19cGy8sIjY4DJCQGc3QE8fIA//4Hv8AFNzgF5uYA+/sGg4QF09MGu7sC+/wA/PsE6OgEMzQD9fUFVFQJaGgGfH0Gp6gFTEwEKysGiosC7/AGwsIIXV0GpKUD3N0GnZ4GamsE3t4F2NkD8vIFREQGk5QId3kH6OgCDxAJo6QIhoYF19gF+/sD7e4EOjsItLUGsrMGq6wE4eIGY2ME7u8C9vgFf4AG3N0E3uAD6+wGn6AIfH0IdXYEHyAI3NwJj5ADJygD8/MGqKcE6uoD9PUIwMGODVadAAADwUlEQVR42u2Ze1PaQBTF81BePcoVEkEUMFJAtNa2+ChUa9/P7/99Omc3QSIwQ6vJTmf29xeSsPfkZu/ds6vjWCwWi8VisVgsFovFYvn/cD3faPyNzUKxVDYXv/IMALaMKdiuAhBByZSAHWgBNUPzwK0DCETC3YYZAY1dIAxEpLlnRkBLPT8g2Dcj4IATQAk4MBLfK+j4CFA0MgvbTQoQCqh2TAjosgIP64IgaLYNxHcjhEDt6BCBoGJAAIsQ6JWfU0DfgIBBwCnQciMKiNz8BRwAoVQbTh8IMcx/PfKOGbjuOhW+idFJ7gJUEWJHfQghg8U7/E4ny/bAIhQ+eKcKAU4Xwr8onlWjVmZz42WEIEDNcxy/yGZcfxDJP2ePRPNVVgIau5BAVx+XBLz20tdbb6B4llWLGigvcsSP+2zG44vUZfcSMVcZvYRrDv5WLQF7XBC1lhmdt3H84DCbFJSPOfqlejq2REE3dX0isQDBdSYp2GPtxT7Er6lUp6731AwcUUA2s6DELjSK3/sVo6WMqVfgVxHvyiYFfkQBiQ3p8kFTxrTdpIBuucDbxhl0yYspizBpPhP6knfzxrSr3kDbuVF+KQPDVmEXmoWkHMFNOkFAwXPKtyyQ6eNS4C7iX/PB3icrINel1HNe3FHgB7V1oWnr+UsGWTO8/7EeLTLmW5+1GG5QwnljWoFIIBOW6y2TM1oyRP3jeitVCcsR4NPsplN+c29M3StG1V3qFVay1o7SG674dYDpffMdxHMuhm0wjBPUGa4UcOutIeDzagFb9yk8GfGrmTE9krk/d1YK+PJ5nRR8XfXzs7myKyuZM2Pah4QYb8c5jFaN8PURkzCq9+YbrBsxJYkx9Wp8A1GSoG+lZSNsrTsJl5bhQhH16YwTY9r+zjnY/bsRHkmF2+TEmHa5TuW8V9LbRG1MZ20wT2hMJV4bGndcJz7kGp/GVBJjWmGXemCQsucHy0Ab07k2mCM0poEypuX3FHCZ915xT1gHzPuGUEDu23VuE3Tt9x+sEznhq+53tdAG80MbU0+5QSNntzSm8nNbL36/DBwZTTj33m24Jtqg4mLK9ehm+w5hgF7+8WlMJcD1vjo9bhkQ4NZZh8Ni2h3mySkgYYj7PWveDFj/JDR0dq6NKZvAOPc2qCgPEwFmjs4d3QFYi6dPMNq/0NcJMPb/G31iCjHSBhX6UEKMtEFFp6pTMDElwFdd0FAbVJwDYYhNI21QcXIGYLphLL7jtDePf+e9H0jjeubyb7FYLBaLxWKxWCwWi+Vp+ANIlGQTPpPpVQAAAABJRU5ErkJggg=="
MODULES = [
    ('<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" /> <path d="M16 3.128a4 4 0 0 1 0 7.744" /> <path d="M22 21v-2a4 4 0 0 0-3-3.87" /> <circle cx="9" cy="7" r="4" />', "Customers", "Customers and suppliers"),
    ('<path d="M12 12h.01" /> <path d="M16 6V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2" /> <path d="M22 13a18.15 18.15 0 0 1-20 0" /> <rect width="20" height="14" x="2" y="6" rx="2" />', "Staff", "Timesheets, leave, overtime"),
    ('<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1" /> <path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4" />', "Finance", "Income, expenses, receivables"),
    ('<path d="M21 10.656V19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h12.344" /> <path d="m9 11 3 3L22 4" />', "Tasks", "Projects and assignments"),
    ('<path d="m6 14 1.5-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.54 6a2 2 0 0 1-1.95 1.5H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3.9a2 2 0 0 1 1.69.9l.81 1.2a2 2 0 0 0 1.67.9H18a2 2 0 0 1 2 2v2" />', "Files", "Attachments linked to records"),
    ('<path d="m2.05 2.05 1.099-.028a1 1 0 0 1 1.008.815l2.69 14.347A1 1 0 0 0 7.83 18H18" /> <path d="M4.563 5h16.435a1 1 0 0 1 .981 1.204l-1.026 6.226A2 2 0 0 1 18.962 14H6.25" /> <circle cx="18" cy="20" r="2" /> <circle cx="8" cy="20" r="2" />', "Sales & Stock", "POS, product catalog, stock"),
]
W, H = 1000, 300
out = []
o = out.append
o(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Nova — Steer your workflow.">')
o('''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#04201a"/><stop offset="1" stop-color="#0a3a2f"/></linearGradient>
<pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><rect width="20" height="20" fill="none" stroke="#7FD3B2" stroke-opacity=".05"/></pattern>
<clipPath id="ic"><rect x="40" y="36" width="64" height="64" rx="14"/></clipPath>
<style>
.t{font-family:ui-monospace,'JetBrains Mono','Fira Code',Menlo,Consolas,monospace}
.in{animation:f .7s ease-out both}
@keyframes f{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
</style></defs>''')
o(f'<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/><rect width="{W}" height="{H}" rx="18" fill="url(#grid)"/>')
# left: identity
o('<g class="in">')
o('<image x="40" y="36" width="64" height="64" clip-path="url(#ic)" href="' + NOVA_ICON + '" xlink:href="' + NOVA_ICON + '"/>')
o('<rect x="40" y="36" width="64" height="64" rx="14" fill="none" stroke="#45BB92" stroke-opacity=".5"/>')
o('<text x="124" y="66" class="t" font-size="13" fill="#7FD3B2" letter-spacing="2">PRODUCT</text>')
o('<text x="124" y="98" class="t" font-size="36" font-weight="700" fill="#ffffff">Nova</text>')
o('<text x="40" y="146" class="t" font-size="19" font-style="italic" fill="#7FD3B2">"Steer your workflow."</text>')
for i, line in enumerate(["A CRM for small and medium-sized businesses.", "Every business process in a single app.", "Works without an account, even offline."]):
    o(f'<text x="40" y="{180 + i * 24}" class="t" font-size="15" fill="#c9eee0">{line}</text>')
label = "Early access · novaişletme.com.tr"
width = 44 + len(label) * 8.4
o(f'<rect x="40" y="252" width="{width:.1f}" height="32" rx="16" fill="#0b3d31" stroke="#45BB92" stroke-opacity=".6"/>')
o('<circle cx="58" cy="268" r="4.5" fill="#7FD3B2"><animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>')
o(f'<text x="72" y="273" class="t" font-size="14" fill="#c9eee0">{label.replace("&", "&amp;")}</text>')
o('</g>')
# right: modules
for i, (icon, name, desc) in enumerate(MODULES):
    y = 46 + i * 40
    o(f'<g class="in" style="animation-delay:{.15 + i * .08:.2f}s">')
    o(f'<g transform="translate(936 {y}) scale(.9)" fill="none" stroke="#7FD3B2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{icon}</g>')
    o(f'<text x="922" y="{y + 16}" text-anchor="end" class="t" font-size="16" font-weight="700" fill="#ffffff">{name.replace("&", "&amp;")}</text>')
    o('</g>')
o('</svg>')
open(sys.argv[1], "w").write("\n".join(out))
