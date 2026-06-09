# Image generation

How the deck's hero / section images are generated. They're produced with
**Amazon Bedrock** and committed to `../assets/gen/`, so you only need to
re-run this if you want to change or add imagery.

## Why this is unusual (account constraints)

Plain "prompt → image" is **not available** on this account, so we use an
image-guided model instead:

| Option | Status |
| --- | --- |
| Amazon Nova Canvas, Titan Image v2 | `LEGACY`, locked ("unused 30 days"); no toggle (Model access page retired) |
| Stability Core / Ultra / SD3.5 (text-to-image) | not in the account catalog (`invalid model id`) |
| Other regions | denied by an org SCP (Bedrock is pinned to `us-east-1`) |
| **Stability `control-structure`** | ✅ works — **this is what we use** |

`control-structure` takes a **structure image + a text prompt** and re-renders
the structure in the prompt's style. So the workflow is two steps: build a
clean composition, then restyle it.

Notes:
- Model id must be the **inference profile** `us.stability.stable-image-control-structure-v1:0`
  (the bare `stability.*` id rejects on-demand calls).
- `control_strength` ~0.4 lets the prompt's style dominate; ~0.7 preserves the
  input composition more strictly.

## Files

```
image-gen/
  control/control-light.html   structure composition (light bg)  → editorial renders
  control/control-dark.html    structure composition (dark bg)    → blueprint / glow renders
  rasterize.py                 control/*.html → control/*.png (Playwright)
  prompts.json                 every image: control + strength + seed + prompt + negative
  generate.py                  prompts.json → ../assets/gen/<name>.png (Bedrock)
```

## Run it

```bash
# 0. toolchain (flake provides aws + jq + node); for rasterize:
pip install playwright && python -m playwright install chromium

# 1. render the control compositions to PNG
python image-gen/rasterize.py

# 2. generate all images (uses AWS_PROFILE=admin-590183794660, us-east-1)
python image-gen/generate.py

# ...or just one:
python image-gen/generate.py hero/title
```

Override the AWS identity/region with `AWS_PROFILE` / `AWS_REGION` env vars.

## Tuning

Edit `prompts.json` — change a `prompt`, bump `control_strength`, or change the
`seed` for a different take — then re-run `generate.py <name>`. Add an entry
(and reference `../assets/gen/<name>.png` from `slides.md`) to create new art.
To change the underlying composition, edit a `control/*.html` and re-run
`rasterize.py` first.
