# Design System — Vellum (2d_world)

The single source of truth for every visual decision in `vellum-monograph.html`.
Read this before writing any markup or styling.

The design is a printed natural-history monograph: laid paper, plate figures with ruled captions,
a display serif for headings and a text serif for body. Nothing here should look like a web app.

---

## Colour Tokens

Defined in `:root` in `vellum-monograph.html`. These eight are the entire palette.

    --paper:  #E4E8E1;   /* page ground — a cool grey-green laid paper */
    --plate:  #EFF2EC;   /* figure ground — lighter than the page, so plates sit forward */
    --ink:    #1B2621;   /* body text, plate linework */
    --ink2:   #55635A;   /* deks, captions, data labels, plate annotations — secondary voice */
    --rule:   #C0CABB;   /* every hairline: borders, dividers, caption rules */
    --teal:   #2E6E62;   /* the one accent — key terms, blockquote rule, hover, emphasis in plates */
    --ox:     #7A2E3A;   /* oxblood — reserved for danger, predation, and hard limits in plates */
    --gold:   #9A7B2E;   /* reserved for Kell, sunlight, and photosynthesis */

**Semantic rules — these are not interchangeable swatches:**
- `--teal` marks *what the reader should notice*. Never use it for decoration.
- `--ox` means *this kills something, or nothing can pass it*. Never use it for general emphasis.
- `--gold` means *light from Kell*. It appears in the plates where sunlight is the subject and
  nowhere else.

There is no error colour, no success colour, and no state palette. This is a document; nothing
succeeds or fails in it. Do not add them "for completeness".

---

## Typography

- **Display:** Fraunces — headings, plate labels, data keys, blockquotes, masthead
  (weights 300, 500, 700)
- **Body:** Spectral — running text, deks, captions, plate annotations
  (weights 300, 400, 600; italic 400)
- Both from Google Fonts. Fallback stack: `Georgia, serif`. Do not add a third family.

### Scale — provisional, see DECISION-004

These sizes exist as hardcoded values, not tokens. **This is the complete permitted set.** Adding a
fifteenth size requires approval — do not invent one to solve a one-off layout problem.

| Size | Used by |
|------|---------|
| `clamp(40px, 8vw, 76px)` | `h1` — frontispiece title only |
| `clamp(26px, 4.4vw, 38px)` | `h2` — slide titles |
| `21px` | `blockquote` |
| `19px` | `h3`, `.dek` |
| `17px` | body (16px below 620px) |
| `15.5px` | `.toc button` |
| `15px` | `.mast .t` |
| `14.5px` | `.data div` |
| `14px` | `nav.bar button` |
| `13.5px` | `figcaption` |
| `13px` | `.mast .n`, `figcaption b`, `.data dt`, `nav.bar .pos` |
| `12.5px` | `text.lab` in plates |
| `12px` | `.toc .pl`, `text` in plates |

Line heights: `1.72` body, `1.55` captions, `1.42` blockquote, `1.3` h3, `1.14` h2, `1.02` h1.
Letter spacing is negative on display headings only: `-.02em` h1, `-.012em` h2, `+.01em` masthead.

### Measure

    --measure: 64ch;   /* paragraphs, lists, data tables, the TOC */

Narrower measures are deliberate and fixed: `52ch` deks, `46ch` blockquotes, `22ch` h2.
Body text never runs wider than `--measure`. The page itself is capped at `920px`.

---

## Spacing

Not tokenised — see DECISION-004. The values in use, and what they mean:

- Page gutter `28px`; bottom padding `140px` (clears the fixed navigation bar)
- Paragraph and list bottom margin `16px`; list item `7px`
- Section heading `h3`: `30px` above, `6px` below
- Figure block: `26px` above and below; internal padding `16px 16px 10px`
- Dek below its heading: `26px`
- Blockquote: `28px` above and below
- Masthead: `20px` above, `14px` below, `16px` gap
- Slide top padding `34px`

---

## Border Radius

`2px` on figures and buttons. Nothing else has a radius. There are no rounded cards, no pills.
The reference is a printed plate with a hairline rule, not a UI surface.

## Shadows

**There are none, and none may be added.** Depth here comes from the `--plate` / `--paper`
value step and a `1px --rule` hairline. A drop shadow would imply a third dimension, in a document
whose entire subject is a world that does not have one.

---

## Plate (SVG) Classes

Every plate uses this fixed set. Do not add ad-hoc `style` attributes to SVG elements.

| Class | Meaning |
|-------|---------|
| `.ink` | Primary linework — stroke 1.3, round caps and joins |
| `.ink-t` | Secondary/construction line — stroke 0.7 at 55% opacity |
| `.tealS` | Stroke marking the thing the caption is about — 1.3 |
| `.oxS` | Stroke marking danger, predation, or an impassable limit — 1.4 |
| `.inkF` | Solid ink fill |
| `.softF` | Ink fill at 9% — masses, ground, water body |
| `.tealF` | Teal fill at 16% — highlighted region or band |
| `.goldF` | Gold fill — Kell, sunlight, photosynthetic surface |
| `text` | Plate annotation — Spectral 12px, `--ink2` |
| `text.lab` | Plate label — Fraunces 12.5px, `--ink` |

**Known deviation:** these classes hardcode hex values (`stroke:#1B2621`) instead of referencing
the tokens (`stroke:var(--ink)`), because they were written as a self-contained plate stylesheet.
The values are identical to the tokens today. This is the one place raw hex is currently tolerated —
it is a defect, not a licence. Do not extend it: a new plate class must use `var(--token)`, and a
change to a token value must be mirrored here until this is fixed.

---

## Component Rules

### Slide

    <section class="slide" data-t="The system of Kell">
      <h2>The system of Kell</h2>
      <p class="dek">A star that nothing can leave.</p>
      ...
    </section>

Correct: one `h2`, one `.dek` immediately after it, then content.
Wrong: a slide without `data-t` — it breaks the TOC, the masthead, and the position counter.
Wrong: adding a slide past the 18th without extending the `roman` array in the navigator.

### Figure

    <figure>
      <svg viewBox="0 0 900 340" ...>...</svg>
      <figcaption><b>Plate IV.</b> The three constraints. ...</figcaption>
    </figure>

Every figure has a caption. Every caption opens with `<b>Plate N.</b>` in sequence — the numbering
is continuous across the whole document and never restarts. SVG is `width:100%; height:auto`, so
always set a `viewBox` and never a fixed pixel width.

### Data table

    <div class="data">
      <div><span class="k">Day</span><span class="v">19.4 hours</span></div>
    </div>

For specification facts only — measurements, ranges, counts. Not for prose. Collapses to stacked
rows below 620px.

### Blockquote

Reserved for a single sentence that states a law of the plane. One per slide at most. If it needs
two sentences, it is prose, not a pull quote.

### Key term

`<em class="term">` — teal italic, for a term at its first definition. Once per term, ever.

---

## What Is Forbidden

- No hardcoded hex outside the `:root` block — except the documented plate-class deviation above,
  which may not be extended
- No font size outside the fourteen listed in the scale table
- No third font family
- No shadows, no gradients, no rounded corners beyond the `2px` on figures and buttons
- No inline `style` attributes
- No utility-class framework and no arbitrary values — there is no framework here and none is coming
- No image files. Every illustration is inline SVG
- No emoji, no icon font, no icon library
- No colour used for decoration rather than meaning
