# CANARY FIXTURE (EP-6, check `badge`) — a README whose badge outruns its evidence

This is the **one innocuous canary** EP-6 pushes, because proving the workflow is wired to the rules
needs a real CI run and this canary carries no secret, no PHI, no local path and no protected text.
The badge below claims a rung whose evidence file does not exist, which is exactly the drift D-59
and D-12 exist to prevent: a badge tied to evidence is only real if the tie is mechanical.

The red run replaces the badge line in the repository's own `README.md` with this one, on a scratch
branch, watches CI fail on `scan: badge`, and reverts.

```
status: skeleton
```

The evidence file that rung maps to is `epppsynth/docs/evidence/skeleton.md`, and it does not exist:
no engine runs end-to-end on fixtures yet.
