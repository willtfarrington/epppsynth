# A planted over-budget quotation, for EP-5 acceptance 8

`count_quotations` must fail on this file. The quoted span below is thirty words long, five over
the D-74 per-quote budget of twenty-five, and it is attributed so that it also counts toward a
source total.

The sentence inside the quotation marks is invented for this fixture. It is not from any source,
and nothing in this repository is; what is being tested is the counter, not the sentence.

"This invented sentence exists only to be counted, and it runs on for exactly thirty words so that
the counter has something to fail on, which is the entire point." [yalom-existential-psychotherapy-1980, ch. 3]

A short quotation on the same page must still pass, so that the counter is shown to discriminate
rather than merely to complain: "under budget" [yalom-existential-psychotherapy-1980].

And an exemption must be honoured when it states a reason:

<!-- quote-budget-allow: a rule definition, quoted to show the marker works -->
"This second invented sentence is also well over the per-quote budget, and it is exempted by the
marker above, so the counter must record it as exempt and must raise no finding about its length."
