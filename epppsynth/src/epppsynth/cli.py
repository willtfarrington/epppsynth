"""Command-line entry point (D-21).

The CLI exists from day one as the cheapest end-to-end smoke test the project
has. It prints the package version and the (contract, registry, template)
version triple; all three are placeholders until EP-17 (contracts) and EP-18
(registry loader) give them real values.
"""

import sys

from epppsynth import __version__

# Placeholders — EP-17 / EP-18 replace these with real, loaded versions.
CONTRACT_VERSION = "none"
REGISTRY_VERSION = "none"
TEMPLATE_VERSION = "none"


def main() -> int:
    print(f"epppsynth {__version__}")
    print(f"contract={CONTRACT_VERSION} registry={REGISTRY_VERSION} template={TEMPLATE_VERSION}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
