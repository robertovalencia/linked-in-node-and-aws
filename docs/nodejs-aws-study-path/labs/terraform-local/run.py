#!/usr/bin/env python3
"""Run an isolated built-in-provider Terraform lab. No AWS CLI or provider."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("--evidence", type=Path, help="Write command results as JSON; no state or saved plans")
args = parser.parse_args()
source = Path(__file__).resolve().parent
records = []
env = {k: v for k, v in os.environ.items() if not k.startswith(("TF_VAR_", "TF_CLI_ARGS", "AWS_"))}
env.update(TF_IN_AUTOMATION="1", CHECKPOINT_DISABLE="1")
env.pop("TF_DATA_DIR", None)
env.pop("TF_WORKSPACE", None)

def run(*words, expected=0):
    result = subprocess.run(["terraform", *words], cwd=lab, env=env, text=True, capture_output=True)
    records.append({"command": ["terraform", *words], "exit_code": result.returncode,
                    "stdout": result.stdout, "stderr": result.stderr})
    if result.returncode != expected:
        raise RuntimeError(f"{words}: expected {expected}, got {result.returncode}\n{result.stdout}\n{result.stderr}")
    print(f"PASS terraform {' '.join(words)} (exit {result.returncode})")
    return result.stdout

def plan(label, *variables, expected=2):
    run("plan", "-input=false", "-no-color", "-detailed-exitcode", f"-out={label}.tfplan", *variables, expected=expected)
    return json.loads(run("show", "-json", f"{label}.tfplan"))

def actions(document):
    return [r["change"]["actions"] for r in document.get("resource_changes", [])]

if not shutil.which("terraform"):
    raise SystemExit("Terraform >=1.10,<2.0 must already be installed; this lab installs nothing.")

try:
    with tempfile.TemporaryDirectory(prefix="terraform-local-study-") as directory:
        lab = Path(directory)
        shutil.copy2(source / "main.tf", lab / "main.tf")
        shutil.copytree(source / "tests", lab / "tests")
        version = json.loads(run("version", "-json"))["terraform_version"]
        major, minor = map(int, version.split(".")[:2])
        if major != 1 or minor < 10:
            raise RuntimeError(f"Terraform {version} is outside >=1.10,<2.0")
        run("fmt", "-check", "-recursive")
        run("init", "-backend=false", "-input=false", "-no-color")
        run("validate", "-no-color")
        assert actions(plan("first")) == [["create"]]
        run("apply", "-input=false", "-no-color", "first.tfplan")
        first_id = json.loads(run("show", "-json"))["values"]["root_module"]["resources"][0]["values"]["id"]
        plan("idempotent", expected=0)
        assert actions(plan("change", "-var=release=v2")) == [["update"]]
        run("apply", "-input=false", "-no-color", "change.tfplan")
        assert actions(plan("replace", "-var=release=v2", "-var=generation=2")) == [["delete", "create"]]
        run("apply", "-input=false", "-no-color", "replace.tfplan")
        replaced_id = json.loads(run("show", "-json"))["values"]["root_module"]["resources"][0]["values"]["id"]
        assert first_id != replaced_id, "Replacement must generate a different resource identity"
        path = lab / "main.tf"
        text = path.read_text().replace('"terraform_data" "release"', '"terraform_data" "artifact"').replace('terraform_data.release.output', 'terraform_data.artifact.output')
        text += '\nmoved {\n  from = terraform_data.release\n  to   = terraform_data.artifact\n}\n'
        path.write_text(text)
        run("fmt", "-no-color")
        moved = plan("moved", "-var=release=v2", "-var=generation=2")
        assert actions(moved) == [["no-op"]], "Address move must not replace the object"
        assert moved["resource_changes"][0]["previous_address"] == "terraform_data.release"
        run("apply", "-input=false", "-no-color", "moved.tfplan")
        assert json.loads(run("show", "-json"))["values"]["root_module"]["resources"][0]["values"]["id"] == replaced_id
        plan("after-move", "-var=release=v2", "-var=generation=2", expected=0)
        run("test", "-no-color")
        run("destroy", "-auto-approve", "-input=false", "-no-color", "-var=release=v2", "-var=generation=2")
        assert run("state", "list").strip() == ""
        print("PASS all local transitions, three configuration test runs, and empty-state cleanup")
finally:
    if args.evidence:
        args.evidence.parent.mkdir(parents=True, exist_ok=True)
        args.evidence.write_text(json.dumps({"scope": "built-in terraform_data only; no AWS provider or credentials", "records": records}, indent=2) + "\n")
