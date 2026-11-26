#!/usr/bin/env python3
"""Test of bin/awsq and bin/dbq with fake `aws`, `pass` and clients on the PATH and a fake HOME.

Usage: python3 test_bin.py
"""
import json
import os
import stat
import subprocess
import tempfile

BIN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bin")


def script(folder, name, body):
    path = os.path.join(folder, name)
    open(path, "w").write("#!/usr/bin/env bash\n" + body)
    os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)


with tempfile.TemporaryDirectory() as home:
    fakes = os.path.join(home, "fakes")
    os.makedirs(fakes)
    vault = os.path.join(home, "vault")
    os.makedirs(os.path.join(vault, "devflow", "investigate"))
    os.makedirs(os.path.join(home, ".config", "devflow"))
    json.dump({"vault": vault}, open(os.path.join(home, ".config", "devflow", "config.json"), "w"))
    json.dump({"sso_session": "s", "profiles": {"stg/dev": {"profile": "p-stg", "use_for": "x"}}},
              open(os.path.join(vault, "devflow", "investigate", "aws.json"), "w"))
    script(fakes, "aws", 'if [[ "$*" == *"sts get-caller-identity"* ]]; then exit "${FAKE_SSO:-0}"; fi\n'
                         'if [[ "$*" == *"sso login"* ]]; then echo "something went wrong"; exit 1; fi\n'
                         'echo "aws $*"; exit "${FAKE_EXIT:-0}"\n')
    script(fakes, "pass", 'case "$FAKE_PASS" in\n'
                          '  missing) echo "Error: $2 is not in the password store." >&2; exit 1 ;;\n'
                          '  gpg) echo "gpg: decryption failed: No secret key" >&2; exit 2 ;;\n'
                          '  *) printf "redis://h:6379\\nnotes\\n" ;;\nesac\n')
    script(fakes, "redis-cli", 'echo "redis-cli $*"\n')
    base = {**os.environ, "HOME": home, "PATH": fakes + os.pathsep + os.environ["PATH"], "AWSQ_LOGIN_WAIT": "2",
            "XDG_CACHE_HOME": os.path.join(home, ".cache")}
    run = lambda tool, *args, **env: subprocess.run([os.path.join(BIN, tool), *args], capture_output=True, text=True,
                                                    env={**base, **env}, timeout=30)

    r = run("awsq", "stg", "dev", "s3", "ls")
    assert r.returncode == 0 and "aws --profile p-stg s3 ls" in r.stdout, (r.returncode, r.stdout, r.stderr)
    r = run("awsq", "stg", "dev", "s3", "ls", FAKE_SSO="255")
    assert r.returncode == 75 and "session expired" in r.stderr, (r.returncode, r.stderr)
    r = run("awsq", "status", FAKE_SSO="255")
    assert r.returncode == 75, r.returncode
    r = run("awsq", "stg", "dev", "s3", "bad", FAKE_EXIT="2")
    assert r.returncode == 2 and "expired" not in r.stderr, (r.returncode, r.stderr)
    r = run("awsq", "login", FAKE_SSO="255")
    assert r.returncode == 1 and "could not start the login" in r.stderr and "something went wrong" in r.stderr, (r.returncode, r.stderr)
    r = run("awsq", "prod", "x", "s3", "ls")
    assert r.returncode == 1 and "unknown profile" in r.stderr

    r = run("dbq", "shop", "stg", "cache", "GET", "k")
    assert r.returncode == 0 and r.stdout.strip() == "redis-cli -u redis://h:6379 GET k", (r.stdout, r.stderr)
    r = run("dbq", "shop", "stg", "cache", FAKE_PASS="missing")
    assert r.returncode == 1 and "is not in the pass store" in r.stderr, r.stderr
    r = run("dbq", "shop", "stg", "cache", FAKE_PASS="gpg")
    assert r.returncode == 1 and "could not read" in r.stderr and "decryption failed" in r.stderr and "not in the pass store" not in r.stderr, r.stderr

print("ok: awsq maps profiles, exits 75 only on an expired session, passes aws errors through, reports a failed login; dbq tells a missing entry from a GPG failure")
