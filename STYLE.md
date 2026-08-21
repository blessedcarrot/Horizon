<!-- lint-ignore-file: this file quotes every pattern it bans -->

# Writing standard

Everything a reader sees is governed by this: the site copy, the prompts that
generate the digests, and any string that renders into a published page.

## Why it exists

This radar is a professional asset. Writing that reads as machine-generated
undermines the credibility it exists to build, and the audience it is written
for recognises the patterns immediately.

## Rules

**No em dashes.** Use a comma, a colon, a semicolon, or a full stop.

**No negative-to-positive constructions.** Avoid "not X, but Y", "X, not Y", and
the rhetorical uses of "rather than" and "instead of". State what is true and
drop the contrast.

**No promotional register.** Avoid "crucial", "pivotal", "game-changing",
"landscape", "delve", "unlock", "leverage" as a verb, and "in today's rapidly
evolving".

**No three-item lists for rhythm.** Three items are fine when there are three
things. They are a tell when the third is filler.

**Define a thing by what it does.** This is the same rule as the one above about
negative-to-positive constructions, at the scale of a section. A heading like
"What it does not do", followed by a list of exclusions, describes a shape by
its shadow. Say what the thing is for. A factual negation inside a sentence is
fine ("popularity is not evidence of importance"); building a section out of
negations is the problem.

**Cut qualifiers that defend against doubts the reader does not have.**
"Items genuinely scored below threshold" says no more than "items scored below
threshold".

**Understatement over superlative.** The audience is senior. Claims should be
ones you would defend in a boardroom.

## The three layers

The mistake is checking only the first. All three reach the reader.

1. **Site copy.** `docs/index.md`, `docs/subscribe.md`, `docs/_layouts/*.html`,
   `docs/_commentary/*.md`.
2. **The prompts.** `profiles/*/match.md`, `analysis.md`, `enrichment.md`. The
   model mirrors the register it is given: 25 em dashes across these prompts
   produced 10 in a single published digest. Every `enrichment.md` carries a
   `# Style constraints` section. Keep it when adding a profile.
3. **Code strings.** `scripts/check_run_health.py` renders a health footer into
   every published page. `scripts/notify_telegram.py` writes the notifications.

## The audit

Run before publishing anything, and after adding a profile or a page.

```bash
# 1. Em dashes anywhere a reader can see them
grep -rn "—" docs/ profiles/*/[man]*.md scripts/*.py

# 2. Negative-to-positive constructions
grep -rniE "not (just|only|merely) |, not | rather than | instead of " docs/ profiles/*/[man]*.md

# 3. Promotional register
grep -rniE "crucial|pivotal|game.chang|landscape|delve|unlock|leverag" docs/ profiles/*/[man]*.md

# 4. Sections and headings framed by what something is not
grep -rnE "^#+ .*(not|never|avoid)|<h[1-3][^>]*>[^<]*(not|Not)" docs/*.md

# 5. Every profile still carries the style constraints. Upstream's four
#    profiles (ai-creator, finance-news, tech-blog, tech-news) are expected
#    here: no source routes to them, so their prompts never run.
grep -L "Style constraints" profiles/*/enrichment.md
```

`STYLE.md` matches its own search patterns; exclude it when running the audit. A hit elsewhere is not automatically a fault. A quoted source, or a factual negation
inside a sentence, is fine. The check exists to make each one a decision.

The audit has already earned itself twice. The first run found em dashes in both
scripts and 69 across the inherited documentation pages. The second found a
whole section, "What it does not do", written as three exclusions in a row,
which is the rule about negation appearing at a scale the greps were not looking
for. When something slips through, extend the checks rather than only fixing the
instance.

## One command instead of five

The greps above stay useful for their specificity. For a single pass over a
file, `lint-voice.py` from the Tenure design system applies rules 1 to 3 at
once, strips HTML and CSS before checking so markup cannot raise a false hit,
and reports each finding with its line:

```bash
python3 ~/AI-Proj/design/tenure/lint-voice.py docs/index.md docs/method.md
```

It exits non-zero when anything is found, so a workflow step can gate on it.

Text that quotes a banned pattern in order to teach it is suppressed with
`data-lint="off"` on an HTML element, `<!-- lint-ignore -->` on a Markdown
line, or `<!-- lint-ignore-file -->` near the top of a file that is entirely
examples. Both markers count only when written as a comment, so prose naming
them keeps being checked, and skipped files are listed in the output. That
also answers the note above about this file matching its own patterns.

Rules 4 and 5 stay as greps. A section framed by what something is not, and a
profile missing its style constraints, are shapes a line-by-line check does
not see.

## Checking generated output

Prompts influence output, they do not guarantee it. After a run, read one item
closely:

```bash
grep -c "—" docs/_posts/$(date -u +%Y-%m-%d)-*-summary-en.md
```

If the model still reaches for a banned pattern, make the instruction more
specific in the profile's `enrichment.md`. Accepting the drift is how the
standard erodes.
