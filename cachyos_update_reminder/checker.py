from dataclasses import dataclass
import subprocess


@dataclass
class Update:
    name: str
    old_version: str
    new_version: str


def parse_updates(output: str) -> list[Update]:
    """Parse the output of checkupdates."""
    updates = []

    for line in output.splitlines():
        line = line.strip()

        if not line:
            continue

        parts = line.split()

        if len(parts) != 4 or parts[2] != "->":
            continue

        name = parts[0]
        old_version = parts[1]
        new_version = parts[3]

        updates.append(
            Update(
                name=name,
                old_version=old_version,
                new_version=new_version,
            )
        )

    return updates

def check_updates() -> list[Update]:
    """Run checkupdates and return available updates."""
    result = subprocess.run(
        ["checkupdates"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode not in (0, 2):
        raise RuntimeError(
            f"checkupdates failed with exit code {result.returncode}"
        )

    return parse_updates(result.stdout)