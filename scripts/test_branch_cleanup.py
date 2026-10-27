#!/usr/bin/env python3
"""Exercise the checked-in github-script cleanup with a mocked GitHub API."""
import json
import subprocess
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/cleanup-merged-profile-branches.yml"
REGISTER = ROOT / "orchestration/branch-deletion-register.json"
REPO = "andrecsmenezes/andrecsmenezes"
BRANCH = "fix/profile-registered-branch-guard-20261027-0955"


def workflow_script():
    raw = WORKFLOW.read_text(encoding="utf-8")
    marker = "          script: |\n"
    if raw.count(marker) != 1:
        raise AssertionError("Expected exactly one github-script block")
    return textwrap.dedent(raw.split(marker, 1)[1])


def run_case(branches, prs, register=None, live=None):
    if register is None:
        register = json.loads(REGISTER.read_text(encoding="utf-8"))
    scenario = {"branches": branches, "prs": prs, "register": register,
                "live": live or {}}
    harness = """
const s = JSON.parse(process.argv[1]);
const deleted = [];
const context = { repo: { owner: 'andrecsmenezes', repo: 'andrecsmenezes' }, sha: 'MAIN_SHA' };
const core = { info: () => {} };
const github = {
  rest: {
    repos: {
      listBranches: function listBranches() {},
      getContent: async () => ({ data: {
        type: 'file', encoding: 'base64',
        content: Buffer.from(JSON.stringify(s.register)).toString('base64')
      } }),
      getBranch: async ({ branch }) => {
        if (deleted.includes('heads/' + branch)) {
          const error = new Error('Deleted'); error.status = 404; throw error;
        }
        const inventory = s.branches.find(b => b.name === branch);
        if (!inventory) {
          const error = new Error('Not found'); error.status = 404; throw error;
        }
        return { data: { commit: { sha: s.live[branch] || inventory.commit.sha } } };
      }
    },
    pulls: { list: function listPulls() {} },
    git: { deleteRef: async ({ ref }) => deleted.push(ref) }
  },
  paginate: async (fn) => {
    if (fn === github.rest.repos.listBranches) return s.branches;
    if (fn === github.rest.pulls.list) return s.prs;
    throw new Error('Unexpected pagination target');
  }
};
(async () => {
""" + workflow_script() + """
})().then(() => console.log(JSON.stringify({ deleted }))).catch(error => {
  console.error(String(error));
  process.exitCode = 2;
});
"""
    result = subprocess.run(
        ["node", "-e", harness, json.dumps(scenario)],
        capture_output=True, text=True, check=False, timeout=15
    )
    return result


def branch(name, sha="MATCH"):
    return {"name": name, "protected": False, "commit": {"sha": sha}}


def pr(name, sha="MATCH", state="closed", merged_at="2026-10-27T12:00:00Z"):
    return {"state": state, "merged_at": merged_at,
            "head": {"repo": {"full_name": REPO}, "ref": name, "sha": sha},
            "base": {"ref": "main"}}


class RegisteredDeletionTest(unittest.TestCase):
    def test_registered_exact_merged_only(self):
        branches = [branch("main"), branch("output"), branch(BRANCH),
                    branch("fix/unregistered-completed")]
        result = run_case(branches, [pr(BRANCH),
                          pr("fix/unregistered-completed")])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["deleted"],
                         ["heads/" + BRANCH])

    def test_open_pr_protects_registered_branch(self):
        result = run_case([branch(BRANCH)], [pr(BRANCH), pr(BRANCH, state="open")])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["deleted"], [])

    def test_stale_merge_sha_fails_closed(self):
        result = run_case([branch(BRANCH, "CHANGED")], [pr(BRANCH, "MATCH")])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["deleted"], [])

    def test_changed_live_branch_fails_closed(self):
        result = run_case([branch(BRANCH)], [pr(BRANCH)], live={BRANCH: "CHANGED"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["deleted"], [])

    def test_invalid_owner_blocks_all(self):
        register = json.loads(REGISTER.read_text(encoding="utf-8"))
        register["owner"] = "unknown/other"
        result = run_case([branch(BRANCH)], [pr(BRANCH)], register=register)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid registered deletion policy", result.stderr)

    def test_duplicate_intent_blocks_all(self):
        register = json.loads(REGISTER.read_text(encoding="utf-8"))
        register["deletion_intents"].append(dict(register["deletion_intents"][0]))
        result = run_case([branch(BRANCH)], [pr(BRANCH)], register=register)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Malformed or duplicated", result.stderr)


if __name__ == "__main__":
    unittest.main()
