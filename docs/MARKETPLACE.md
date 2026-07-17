# xAI Plugin Marketplace listing

Official catalog: https://github.com/xai-org/plugin-marketplace

## Prerequisites

1. This monorepo is **public** on `CaplifiTechnologies/caplifi-grok-plugins`
2. Each plugin has a valid `.grok-plugin/plugin.json` + `plugin.json` (+ `.claude-plugin/plugin.json`, kept byte-identical — selftest enforces)
3. Remote source pins a **full 40-char commit SHA** — always a **tag's** SHA, never raw HEAD (see `scripts/release.sh`; pinning HEAD chases itself because the pin commit moves HEAD)
4. Keywords/domains are **brand-scoped** (not generic `brand`, `deploy`, `api`)
5. `scripts/check_urls.sh` passes (every homepage/spec URL live, no redirect loops)

## Catalog entries (draft)

Add four entries under `.grok-plugin/marketplace.json` in a fork of the marketplace:

```json
{
  "name": "brandmd",
  "description": "BRAND.md open brand standard for agents: apply core brand under 600 tokens, load deeper files on demand, audit repo conformance, score completeness.",
  "category": "development",
  "source": {
    "source": "url",
    "url": "https://github.com/CaplifiTechnologies/caplifi-grok-plugins.git",
    "sha": "adf47574768b491d8f0c0fb2d120dec18b1444bf",
    "path": "plugins/brandmd"
  },
  "homepage": "https://caplifi.com/build/brandmd/",
  "keywords": ["brandmd", "brand.md", "caplifi brandmd"],
  "domains": ["caplifi.com"]
}
```

Same pattern for `hbi`, `slopmd`, `caplifi-approve` with matching paths and keywords:

| name | keywords | domains | homepage |
|------|----------|---------|----------|
| brandmd | brandmd, brand.md, caplifi brandmd | caplifi.com | https://caplifi.com/build/brandmd/ |
| hbi | hbi, half-baked idea, hbi-standard | eclecticventures.net, caplifi.com | https://eclecticventures.net/hbi/ |
| slopmd | slopmd, slop.md, instigate handoff | eclecticventures.net | https://eclecticventures.net/slopmd/ |
| caplifi-approve | caplifi-approve, headgate.approve, caplifi approve | caplifi.com | https://caplifi.com/approve/ |

Then:

```bash
python3 scripts/generate-plugin-index.py
python3 scripts/validate-catalog.py
# open PR to xai-org/plugin-marketplace
```

## Security note for reviewers

These plugins ship **skills and slash commands only** (HBI also ships a pure-Python local validator). No remote MCP, no postinstall, no secret exfiltration. Agents may call public HTTP URLs the user already uses.
