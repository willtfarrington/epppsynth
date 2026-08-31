# Canary fixtures — deliberate test fixtures, inert by construction (EP-6)

Every file in this directory is a **deliberate test fixture**. Each exists to make one
leak-prevention scanner fire, so that a scanner which has never failed is not mistaken for a scanner
that works.

Nothing here is real. The strings are **structurally valid and inert**: a token-shaped string with a
documented non-existent prefix, a digit run that names nobody, a placeholder user-profile path whose
account segment is a literal placeholder, an invented citation. No value here resolves, authenticates,
identifies a person, or came from any source.

The scanners exempt **this directory and no other**, by exact path, never by pattern — a
pattern-based exemption is how a real leak later hides. The allowlist has exactly one entry and
`epppsynth/tests/test_publicsafety.py` fails if a second is added; adding one is an `ADR-008`
amendment, not an edit.

**These files are not the acceptance evidence.** EP-6's nine red runs plant *un*-exempted copies
outside this directory, in the working tree only, and remove them again. A public repository's
history is permanent and an unreachable object is not a deleted one, so no red-run canary is ever
pushed. What lives here is the unit-test input; what proved the scanners work is recorded in EP-6's
completion note.

Every file carries a header line declaring itself a fixture. A file here without one is a mistake.
