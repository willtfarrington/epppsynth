# Source material — local only, not tracked

This directory holds the primary texts the project synthesizes from. Those
works are under copyright, so **nothing in here is committed to the
repository** — everything except this README is excluded by `.gitignore`.

To work with the project locally, place your own legally obtained copies here,
one directory per work:

```
source material/
  <title> - <author>/
    <title> - <author>.epub      # your own copy
    markdown/                    # generated, also untracked
```

The markdown under each work is derived text and is likewise local only.

The conversion pipeline that produces that markdown lives in
[`tools/epub_to_md_pipeline.py`](../tools/epub_to_md_pipeline.py) and *is*
tracked — the code is ours, only the texts it operates on are not.
