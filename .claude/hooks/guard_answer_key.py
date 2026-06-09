#!/usr/bin/env python3
"""Guard hook: block Claude from reading *.answers.json answer keys
unless a matching approval token exists in approvals/.

Wired as a PreToolUse hook (see .claude/settings.json). It inspects the
tool call Claude is about to make. If the call would READ a file matching
`*.answers.json`, it is denied unless `approvals/<address>.approved` exists.

Creating a new answer key (Write/create) is always allowed — only reads of
EXISTING answer-key files are gated. The point is to keep the tutor honest:
it can author a quiz + key, but cannot peek at a stored key to grade or
reveal answers unless the human explicitly approves.

Claude Code passes the hook a JSON event on stdin and reads the hook's
JSON decision on stdout. We deny by emitting
{"hookSpecificOutput": {"permissionDecision": "deny", ...}}.
Exit code 0 with a deny decision blocks the call.
"""
import json
import os
import re
import sys

ANSWERS_RE = re.compile(r"(?P<address>\d[\dA-Za-z]*\.\d+)\.answers\.json$")

# Tools that read file content. Adjust if your toolset differs.
READ_TOOLS = {"Read", "view"}
# Tools that can sneak a read via a shell. We scan their command strings.
SHELL_TOOLS = {"Bash", "bash_tool"}

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APPROVALS_DIR = os.path.join(REPO_ROOT, "approvals")


def approved(address: str) -> bool:
    token = os.path.join(APPROVALS_DIR, f"{address}.approved")
    return os.path.exists(token)


def deny(reason: str):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def allow():
    # Emitting nothing / an empty object lets the call proceed normally.
    print(json.dumps({}))
    sys.exit(0)


def main():
    try:
        event = json.load(sys.stdin)
    except Exception:
        # If we can't parse the event, fail open (don't break the session),
        # but this should not normally happen.
        allow()
        return

    tool = event.get("tool_name") or event.get("toolName") or ""
    tool_input = event.get("tool_input") or event.get("toolInput") or {}

    # 1) Direct file-reading tools.
    if tool in READ_TOOLS:
        path = str(tool_input.get("path") or tool_input.get("file_path") or "")
        m = ANSWERS_RE.search(path)
        if m and not approved(m.group("address")):
            deny(
                f"Reading the answer key for lesson {m.group('address')} is "
                f"blocked. Ask the user to approve by creating "
                f"approvals/{m.group('address')}.approved, then retry."
            )

    # 2) Shell commands that might read an answer key (cat, grep, python, etc.)
    if tool in SHELL_TOOLS:
        cmd = str(tool_input.get("command") or "")
        for m in ANSWERS_RE.finditer(cmd):
            if not approved(m.group("address")):
                deny(
                    f"That command appears to read the answer key for lesson "
                    f"{m.group('address')} via the shell, which is blocked. "
                    f"Ask the user to approve "
                    f"(approvals/{m.group('address')}.approved) and retry."
                )
        # Also catch a glob-y read of all answer keys.
        if "answers.json" in cmd and ("cat" in cmd or "less" in cmd
                                      or "head" in cmd or "tail" in cmd
                                      or "grep" in cmd or "open" in cmd):
            deny(
                "That command appears to read answer-key files in bulk, which "
                "is blocked. Answer keys require per-lesson approval tokens in "
                "approvals/."
            )

    allow()


if __name__ == "__main__":
    main()
