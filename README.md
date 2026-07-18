# Caplifi Agent Plugins

**Stranger-facing** official agent plugins for Grok Build and Claude Code — open standards and contracts from Caplifi Technologies / Eclectic Ventures.

| Plugin | Product | Install path |
|--------|---------|--------------|
| **brandmd** | [BRAND.md](https://caplifi.com/build/brandmd/) open brand standard | `plugins/brandmd` |
| **hbi** | [HBI](https://eclecticventures.net/hbi/) Half-Baked Idea package format | `plugins/hbi` |
| **slopmd** | [SLOP.md](https://eclecticventures.net/slopmd/) agent handoff envelopes + INSTIGATE/HANDOFF | `plugins/slopmd` |
| **caplifi-approve** | [Caplifi Approve](https://caplifi.com/approve/) `headgate.approve.v1` | `plugins/caplifi-approve` |

**Not in this ship (separate gate):** money-rail authorization plugins. Open standards only here.

## What these are

- **Skills** agents load when the job matches  
- **Slash commands** for explicit invoke  
- **No house paths** — no `~/ALMI`, no private Camelot, no local Dashboard ports  
- **Public specs** linked by URL; tools are self-contained  

## Install (Grok Build)

```bash
# From a clone of this repo (path install)
grok plugin install ./plugins/brandmd --trust
grok plugin install ./plugins/hbi --trust
grok plugin install ./plugins/slopmd --trust
grok plugin install ./plugins/caplifi-approve --trust

grok plugin list
grok plugin details brandmd
```

Or after GitHub publish:

```bash
grok plugin install CaplifiTechnologies/caplifi-agent-plugins#plugins/brandmd --trust
```

Marketplace listing (xAI official catalog) is a **separate PR** to `xai-org/plugin-marketplace` — see [docs/MARKETPLACE.md](docs/MARKETPLACE.md).

## Install (Claude Code)

This repo is also a Claude Code plugin marketplace (`.claude-plugin/marketplace.json`):

```
/plugin marketplace add CaplifiTechnologies/caplifi-agent-plugins
/plugin install brandmd@caplifi
/plugin install hbi@caplifi
/plugin install slopmd@caplifi
/plugin install caplifi-approve@caplifi
```

Skills and slash commands are shared between harnesses — `skills/*/SKILL.md` is the single source of truth; the per-harness manifests (`.grok-plugin/`, `.claude-plugin/`) are kept byte-identical by `scripts/selftest.sh`.

**Install doctrine:** no `curl | bash`, no postinstall, no network tools. Pin by tag/SHA, verify checksums on release zips. The same rule Caplifi Approve asks of your agents, applied to our own artifacts.

## License

Apache-2.0 — see [LICENSE](LICENSE). Each open standard has its own stewardship page; this repo packages agent playbooks, not exclusive ownership of the ideas.

## Steward

Caplifi Technologies (Eclectic Ventures Incorporated)  
https://caplifi.com · https://eclecticventures.net
