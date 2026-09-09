#!/usr/bin/env python3
"""Check this SDK against the published OpenAPI spec.

This package is hand-written, so nothing regenerates when the API moves and
nothing else notices. Two kinds of drift matter and both have bitten:

  1. An operation exists in the spec and no method calls it. The three number
     import endpoints sat unimplemented for months this way.
  2. A method exists but does not accept a parameter the spec marks required.
     `carrier` went required on search and purchase and this SDK kept sending
     requests without it.

Absences that are deliberate go in DELIBERATE with a reason, so an unexplained
gap is the only thing that fails.

Usage: python scripts/check_spec.py [--spec URL_OR_PATH]
"""

from __future__ import annotations

import argparse
import inspect
import re
import sys
import urllib.request

import yaml

from omnidimension import Client

SPEC_URL = "https://docs.omnidim.io/openapi.yaml"

# Operations this SDK does not implement on purpose. Anything not listed here
# and not implemented fails the check.
DELIBERATE = {
    "createSession": "browser-side; the @omnidim-ai/client web SDK owns it",
    "listSimulations": "simulations are undocumented and unstable",
    "createSimulation": "simulations are undocumented and unstable",
    "getSimulation": "simulations are undocumented and unstable",
    "updateSimulation": "simulations are undocumented and unstable",
    "deleteSimulation": "simulations are undocumented and unstable",
    "startSimulation": "simulations are undocumented and unstable",
    "stopSimulation": "simulations are undocumented and unstable",
    "enhancePrompt": "authoring helper, not a runtime call",
}

RESOURCES = ("agent", "bulk_call", "call", "knowledge_base", "phone_number",
             "providers", "reseller", "simulation", "integrations")

CALL = re.compile(r'self\.client\.(get|post|put|patch|delete)\(\s*f?["\']([^"\']*)["\']')
DICT_KEY = re.compile(r'["\']([a-zA-Z_][a-zA-Z0-9_]*)["\']\s*:')
ITEM_SET = re.compile(r'\[["\']([a-zA-Z_][a-zA-Z0-9_]*)["\']\]\s*=')


def load_spec(source: str) -> dict:
    if source.startswith(("http://", "https://")):
        with urllib.request.urlopen(source) as response:  # noqa: S310 - fixed docs URL
            return yaml.safe_load(response.read())
    with open(source, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def normalise(verb: str, path: str) -> str:
    """A route key that matches whether the parameter is written {id} in the
    spec or f"{agent_id}" in a method body."""
    return f"{verb.upper()} " + re.sub(r"\{[^}]*\}", "*", path.strip("/"))


def spec_routes(spec: dict) -> dict[str, dict]:
    out = {}
    for path, item in spec.get("paths", {}).items():
        for verb, op in item.items():
            if not isinstance(op, dict) or not op.get("operationId"):
                continue
            body = (op.get("requestBody", {}).get("content", {})
                      .get("application/json", {}).get("schema", {}) or {})
            # Path parameters are substituted into the URL, so the argument
            # name is the author's choice and a mismatch means nothing. Body
            # and query fields go on the wire under their own names, so those
            # are the ones a method has to actually send.
            out[op["operationId"]] = {
                "route": normalise(verb, path),
                "required": set(body.get("required") or []) | {
                    p["name"] for p in op.get("parameters", [])
                    if p.get("required") and p.get("in") == "query"
                },
            }
    return out


def sdk_methods() -> dict[str, tuple[str, set[str]]]:
    """route -> (dotted name, accepted argument names)."""
    client = Client("x" * 12)
    found = {}
    for resource in RESOURCES:
        obj = getattr(client, resource, None)
        if obj is None:
            continue
        for name, fn in inspect.getmembers(obj, inspect.ismethod):
            if name.startswith("_"):
                continue
            try:
                source = inspect.getsource(fn)
            except (OSError, TypeError):
                continue
            match = CALL.search(source)
            if not match:
                continue
            found.setdefault(normalise(match.group(1), match.group(2)),
                             (f"{resource}.{name}", sent_keys(fn, source)))
    return found


def sent_keys(fn, source: str) -> set[str] | None:
    """The field names this method actually puts in the request.

    Not its argument names: `create(file_data, filename)` sends a key called
    `file`, and comparing argument names would call that drift. None means the
    method takes **kwargs and can therefore send anything.
    """
    if any(p.kind is inspect.Parameter.VAR_KEYWORD
           for p in inspect.signature(fn).parameters.values()):
        return None
    return set(DICT_KEY.findall(source)) | set(ITEM_SET.findall(source))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", default=SPEC_URL)
    options = parser.parse_args()

    ops = spec_routes(load_spec(options.spec))
    methods = sdk_methods()

    missing, unaccepted = [], []
    for op_id, info in sorted(ops.items()):
        hit = methods.get(info["route"])
        if not hit:
            if op_id not in DELIBERATE:
                missing.append(f"{op_id} ({info['route']})")
            continue
        name, sends = hit
        if sends is None:
            continue
        for field in sorted(info["required"] - sends):
            unaccepted.append(f"{name} never sends {field!r}, required by {op_id}")

    for line in missing:
        print(f"drift: no method for {line}", file=sys.stderr)
    for line in unaccepted:
        print(f"drift: {line}", file=sys.stderr)

    print(f"{len(ops)} operations, {len(ops) - len(missing) - len(DELIBERATE)} implemented, "
          f"{len(DELIBERATE)} deliberate, {len(missing)} unexplained")

    if missing or unaccepted:
        print("add the method, or add the operation to DELIBERATE with a reason",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
