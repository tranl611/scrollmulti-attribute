# Multi-attribute scroll-tracking study (oTree)

## Design

| | Rounds | Shown on each swipe card | `condition` |
|---|---|---|---|
| Part 1 | – | rate every trainer from -3 to 3 (appearance only), unchanged | – |
| Block 1 | 1-30 | picture (appearance) | 1 |
| Block 2 | 31-60 | picture + discount ("40% off") | 2 |
| Block 3 | 61-90 | picture + discount + star reviews | 3 |

Block order is fixed (as specified). Participants see an instruction page at the start of each block.

### Why one `page_sequence`
oTree runs the *whole* `page_sequence` once per round, so you cannot list `[Instructions3, PreDecision, Decision, ...]` again for rounds 31-60. Instead there is a single sequence, and `Instructions2/3/4` are switched on by `is_displayed` at rounds 1, 31 and 61. `Decision` reads `player.condition` to decide what to show.

### Pair generation (Part 1 ratings -> 90 pairs)
- 30 pairs per block; within each block the rating difference (-3..3) is spread evenly (4 per level + 2 random levels), so all blocks have the same difficulty profile.
- Unordered pairs are not reused across blocks (unless the participant's ratings leave no fresh candidates).
- Pair order is shuffled within a block, never across blocks.

### Attributes
- **Discount**: drawn independently for each product and trial from `C.DISCOUNT_LEVELS` (0, 10, ..., 100 %), independent of the participant's rating. Edit the list in `C` to narrow the range.
- **Star reviews**: fixed per product, read from `shoe_reviews.csv` (average stars out of 5 + number of reviews).

## Things you still need to provide

1. **Review data**: fill `shoe_reviews.csv` (scaffold has all 222 product IDs; columns `avg_stars`, `n_reviews`, optional `source_url`). Rows left blank are ignored, and a missing product raises a clear error. Ask your professor which retailer/source and collection date; if it is scraped from SportsDirect itself, check the site's terms first. Products with no reviews will need to be dropped from `MALE_SHOES`/`FEMALE_SHOES` or handled by a rule.
2. **Settings**: add to `SESSION_CONFIGS` in `settings.py`:

```python
dict(
    name='multiattr_binarychoice',
    app_sequence=['multiattr_binarychoice'],
    num_demo_participants=1,
    pilot=1,                      # 1 = 20 shoes per gender, response-curve page shown
    use_placeholder_reviews=1,    # PILOT ONLY: fake but deterministic reviews; use 0 for real data
    prolificurl='https://app.prolific.com/submissions/complete?cc=XXXX',
)
```

3. **Unchanged files** from the one-attribute app: `MobileCheck.html`, `Information.html`, `Instructions.html`, `Preference.html`, `PreDecision.html`, `ResponseCurve.html`, `Results.html`, and the static image.
4. **CSS**: the swipe-card styles (`container3`, `element3`, `fitting-image2`, "hidden until first scroll") are assumed to live in your global template as before. The discount/stars lines sit *inside* `#choicetext1/2`, so they stay hidden until the first scroll like the images. Check on a real phone that the cards are tall enough for the extra lines.

## New data columns
`condition`, `thisround_discount1/2`, `thisround_stars1/2`, `thisround_nreviews1/2`, `reviews_placeholder` (1 = fake pilot reviews). Columns not shown in a block are empty. All process-tracing columns (`psiL/R`, `dwelltimeL/R`, `switchesLR/RL`, ...) are computed exactly as before. Dwell is per product (left vs right card), not per attribute.

## Decisions to confirm
- "Rating" in block 1 is read as the product's appearance (the picture); the participant's own Part 1 rating is not shown.
- Block 2/3 instructions tell people to use *all* information shown (block 1 said style only). Wording is in `Instructions3.html` / `Instructions4.html`.
- A 100 % discount means a free product and may dominate choices; a pilot will show whether to cap the range.
- Fixed block order confounds adding attributes with time/fatigue/learning.
- Pilot mode now uses 20 shoes for *both* genders (the old code truncated only the men's list, to 10).

## Carried over from the old code (not changed, so metrics stay comparable)
In `Decision.before_next_page`: (1) the crossing test `if (j>0) and (...) or (...)` evaluates its second clause at j=0 because of operator precedence; (2) the `x[-1] < 150` / `x[-1] >= 150` branches append `[x[0], y[0]]` where `[x[-1], y[-1]]` looks intended. Both affect `psiL/psiR` slightly; worth a look before data collection.

## Testing done
App imports under oTree 6.0.15; 90 pairs per participant checked for uniform, skewed, all-equal and 20-shoe pilot ratings (even difficulty profile per block, no repeated pairs); attributes per block; review loader. Not tested: rendering in a browser/phone.
