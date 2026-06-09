#!/usr/bin/env python3
"""Generate the deck's hero/background images via Amazon Bedrock.

Text-to-image is unavailable on this account (Nova Canvas / Titan are LEGACY
and locked; Stability Core/Ultra/SD3 aren't in the catalog; an org SCP pins
Bedrock to us-east-1). The one working generative path is Stability
**control-structure**, which restyles a structure image per a text prompt.

Pipeline:
    control/*.html  --rasterize.py-->  control/*.png  --(this)-->  ../assets/gen/<name>.png

Prereqs:
    - AWS creds for a profile that can call Bedrock in us-east-1
      (this repo uses profile `admin-590183794660`; override with AWS_PROFILE).
    - aws CLI v2 + jq on PATH (provided by the nix flake devShell).
    - control PNGs present (run rasterize.py first).

Usage:
    python image-gen/generate.py            # generate every image in prompts.json
    python image-gen/generate.py hero/title # generate only matching name(s)

Env overrides: AWS_PROFILE (default admin-590183794660), AWS_REGION (default
from prompts.json, i.e. us-east-1).
"""
import base64, json, os, subprocess, sys, tempfile, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SPEC = json.loads((HERE / "prompts.json").read_text())
OUT_ROOT = ROOT / "assets" / "gen"
PROFILE = os.environ.get("AWS_PROFILE", "admin-590183794660")
REGION = os.environ.get("AWS_REGION", SPEC.get("region", "us-east-1"))


def invoke(model, body_path, out_path):
    """Call bedrock-runtime invoke-model via the aws CLI."""
    cmd = [
        "aws", "bedrock-runtime", "invoke-model",
        "--model-id", model,
        "--body", f"fileb://{body_path}",
        "--cli-binary-format", "raw-in-base64-out",
        "--region", REGION, "--profile", PROFILE,
        out_path,
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


def b64_of(path):
    return base64.b64encode(pathlib.Path(path).read_bytes()).decode()


def main():
    only = set(sys.argv[1:])
    model = SPEC["model"]
    negs = SPEC["negatives"]
    todo = [i for i in SPEC["images"] if not only or i["name"] in only]
    if not todo:
        print("nothing matched; names are:",
              ", ".join(i["name"] for i in SPEC["images"])); return

    for item in todo:
        control_png = HERE / "control" / f"{item['control']}.png"
        if not control_png.exists():
            print(f"SKIP {item['name']}: missing {control_png.name} "
                  f"(run rasterize.py)"); continue

        req = {
            "prompt": item["prompt"],
            "image": b64_of(control_png),
            "control_strength": item["control_strength"],
            "output_format": "png",
            "negative_prompt": negs[item["negative"]],
            "seed": item["seed"],
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as bf:
            json.dump(req, bf); body_path = bf.name
        resp_path = tempfile.mktemp(suffix=".json")

        r = invoke(model, body_path, resp_path)
        os.unlink(body_path)
        if r.returncode != 0:
            print(f"ERR  {item['name']}: {r.stderr.strip().splitlines()[-1] if r.stderr else r.returncode}")
            continue

        data = json.loads(pathlib.Path(resp_path).read_text())
        os.unlink(resp_path)
        out = OUT_ROOT / f"{item['name']}.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(base64.b64decode(data["images"][0]))
        print(f"OK   {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
