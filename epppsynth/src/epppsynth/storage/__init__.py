# SPDX-FileCopyrightText: 2026 W. Taylor Farrington
# SPDX-License-Identifier: Apache-2.0
"""Storage roots, the reserve floor, the project ceiling and a read-only inventory (EP-7).

Nothing in this project may download a model, build an index or write a
benchmark packet until something refuses to do so when the machine cannot
afford it. This package is that refusal, and nothing more:

``limits``     the constants, the two space guards and the ceiling guard
``layout``     the two root trees, ``models.lock.json`` and ``METADATA.json``
``inventory``  a strictly read-only walk over four model caches
``verify``     revision, format and hash verification of a weight

**No module in this package deletes, moves or renames anything.** That is not a
convention, it is an assertion: ``tests/test_storage.py`` parses every module in
this directory and fails on a call to ``os.remove``, ``os.unlink``,
``Path.unlink``, ``Path.rmdir``, ``shutil.rmtree``, ``shutil.move`` or a
Recycle-Bin helper. The seven rules a future purge tool would have to satisfy
are written down in ``docs/adr/ADR-007-cache-purge-safety-rules.md``; no
implementation of them exists, deliberately (D-71).
"""
