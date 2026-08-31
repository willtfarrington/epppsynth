# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""Rights: the per-source record, the licence boundary, and the checks over both.

Four rules live here, each as a library function with its own tests, so that
EP-6 wires proven code into CI rather than inventing checks under time pressure:

* `check_source_refs` — every concept's `source_id` resolves to a rights record.
* `check_no_verbatim_from_nonredistributable` — the D-10 rule.
* `count_quotations` — the D-74 budget: 25 words per quote, 150 per source.
* `licence_coverage` — every tracked file maps to exactly one licence.

`render_rights_md` generates `epppsynth/docs/rights.md`, and refuses to when the
D-10 rule is broken.

Submodules are imported lazily (PEP 562). Three of them are run as
`python -m epppsynth.rights.<name>`, and eagerly importing them here would mean
`runpy` re-executing an already-imported module — which Python warns about, and
which is exactly the kind of noise that trains a reader to skip warnings.
"""

from __future__ import annotations

import importlib

__all__ = [
    "Citation",
    "ConceptProvenance",
    "Finding",
    "Quotation",
    "QuotationReport",
    "RightsError",
    "Source",
    "SourceRegistry",
    "check_locators",
    "check_no_verbatim_from_nonredistributable",
    "check_source_refs",
    "count_quotations",
    "licence_coverage",
    "load_concepts",
    "load_sources",
    "render_rights_md",
]

_EXPORTS: dict[str, str] = {
    "Citation": "model",
    "ConceptProvenance": "model",
    "Finding": "model",
    "RightsError": "model",
    "Source": "model",
    "SourceRegistry": "model",
    "Quotation": "quotes",
    "QuotationReport": "quotes",
    "check_locators": "check",
    "check_no_verbatim_from_nonredistributable": "check",
    "check_source_refs": "check",
    "count_quotations": "quotes",
    "licence_coverage": "coverage",
    "load_concepts": "check",
    "load_sources": "load",
    "render_rights_md": "render",
}


def __getattr__(name: str) -> object:
    module = _EXPORTS.get(name)
    if module is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return getattr(importlib.import_module(f".{module}", __name__), name)


def __dir__() -> list[str]:
    return list(__all__)
