# Multi-attribute scroll-tracking study (oTree 6)

App folder: `binarychoice/` (the oTree app). `settings.py`, `Procfile` and `requirements.txt` sit one level up, at the repo root, next to this folder.

## Design

| | Rounds | Shown on each swipe card | `condition` |
|---|---|---|---|
| Part 1 | – | rate every trainer from -3 to 3 (appearance only), unchanged from the one-attribute study | – |
| Block 1 | `BLOCK1_LENGTH` | picture (appearance) | 1 |
| Block 2 | `BLOCK2_LENGTH` | picture + discount ("40% off") | 2 |
| Block 3 | `BLOCK3_LENGTH` | picture + discount + star reviews | 3 |

The block order is fixed (as specified). Participants see an instruction page at the start of each block.

### Block lengths (set in `class C`)
The three blocks may have different lengths. The total must not exceed `MAX_ROUNDS` (150; an assertion stops the app from starting if it does).
Recommended defaults: **28 / 42 / 72** (142 rounds, cap 150) or **28 / 28 / 60** (116 rounds, cap 120; then also set `MAX_ROUNDS = 120`).

Balance rules (so every cell has exactly equal counts):
- Block 2 should be a multiple of 2 (two attribute layouts).
- Block 3 should be a multiple of 6 (six attribute layouts).
- Any block that is a multiple of 7 has exactly equal numbers of rating-difference levels (-3..3). Other lengths are balanced to within one round.
- Block 1 has one layout only.

### Why one `page_sequence`
oTree runs the *whole* `page_sequence` once per round, so you cannot list `[Instructions3, PreDecision, Decision, ...]` again for later blocks. There is a single sequence, and `Instructions2/3/4` are switched on by `is_displayed` at the first round of each block (`BLOCK_STARTS`). `Decision` reads `player.condition` to decide what to show.

### Pair generation (Part 1 ratings -> pairs)
- Pairs are built from the participant's own Part 1 ratings, as ordered pairs (left, right).
- Only pairs whose rating *difference* is between -3 and 3 are kept (ratings themselves run -3..3, so 3 against -3 is excluded).
- Within each block, every difficulty level (rating difference -3..3) is used `n // 7` times, and the leftover rounds get random levels.
- A pair of shoes (unordered) is not reused across blocks unless the participant's ratings leave no fresh candidates.
- The order of the pairs is shuffled within a block, never across blocks.
- The shoes shown come from the first 90 shoes per gender (`N_SHOES = 90`) in `MALE_SHOES` / `FEMALE_SHOES`, all rated in Part 1.

## Attributes

### Discount
- Every discount is between `DISCOUNT_MIN` and `DISCOUNT_MAX` (10% to 60%) in steps of `DISCOUNT_STEP` (5). There is no 0% (no information) and no 100% (a free product, which behaves differently from any other price cut).
- The gap between the two cards (left minus right) is planned in round 1 (`discount_diffs`) and is one of `DISCOUNT_DIFFERENCES` = -30, -20, -10, 0, 10, 20, 30 percentage points. Each gap size is used equally often within a block; the lower discount is then drawn at random so that both discounts stay inside the range.
- Agree/conflict balance: among rounds where both the rating difference and the discount gap are non-zero, half the rounds "agree" (the product rated higher also has the higher discount) and half "conflict". The size of the discount gap is unrelated to the size of the rating gap. Where the two ratings are equal, the higher discount is on the left in half of the rounds.
- Blocks 2 and 3 use the same rule, so comparing them isolates the effect of the star reviews.
- Recorded as `thisround_discount1/2` and `thisround_discountdiff` (left minus right). Compare its sign with the sign of `thisround_valuedifference` for agree vs conflict.
- Edit `DISCOUNT_*` in `class C` to change the range or gaps. An assertion checks that the gaps fit inside the range. If the pilot shows people always pick the higher discount at a 30-point gap, narrow `DISCOUNT_DIFFERENCES` to +/-20.

### Star reviews
- Fixed per product, read from `binarychoice/shoe_reviews.csv` (`avg_stars` out of 5, and `n_reviews`). The card shows the stars and, if enabled, the number of reviews: "4.3 / 5 (57 reviews)".
- **Stars only (no number of reviews):** set `show_number_of_reviews=0` in the session config (default 1 = number is shown). Then:
  - the card shows "4.3 / 5" and the star icons only;
  - the Block 3 instruction page drops the phrase about the number of reviews;
  - `thisround_nreviews1/2` are left empty in the data (the number is not recorded because it was not shown), and `nreviews_shown` is 0;
  - the `n_reviews` column in `shoe_reviews.csv` may be left blank (it is still worth filling in for your own records).
- `nreviews_shown` (block 3 only): 1 = number of reviews shown, 0 = stars only. Empty in blocks 1 and 2.
- Real-study check: when the session is created with real reviews, the app refuses to start if any shoe that can be shown has no stars (or, when the number is shown, no number of reviews). The error lists the shoes, so the problem appears before anyone takes part rather than at the first round of block 3.

## Attribute positions (session setting `attribute_order`)
Each card shows its lines top to bottom. The same layout is used on both cards in a round.

| `attribute_order` | Behaviour |
|---|---|
| `'fixed'` (default) | picture, discount, stars from top to bottom in every round |
| `'block'` | random layout per participant and block; the same in all rounds of a block |
| `'trial'` | a new layout in every round of blocks 2 and 3 |

- The picture takes part in the randomisation (it can appear below the discount or the stars). Block 1 has only the picture.
- The layouts are not drawn independently each round: a balanced list is built in round 1 (`attr_orders`), so each layout is used equally often within a block (block 2: two layouts, block 3: six), in random order.
- Recorded: `attr_order` (e.g. `stars>picture>discount`, top to bottom), `pos_picture`, `pos_discount`, `pos_stars` (1 = topmost line; empty when the attribute is not shown in that block).
- Only what is drawn inside each card changes. Card geometry (300 px cards, 150 px midpoint) and all tracking code are unchanged. `dwelltimeL/R` and the switches are per card, not per attribute: they say how long each product was in view, not how long each line was looked at.

## Session configs (`settings.py` at the repo root)
All use `app_sequence=['binarychoice']`.

| Config | Shoes | Reviews | Notes |
|---|---|---|---|
| `multiattr_pilot` | 20 per gender | fake, deterministic (`use_placeholder_reviews=1`) | response-curve page shown |
| `multiattr_randompos` | 20 per gender | fake | demo with `attribute_order='trial'` |
| `multiattr_study` | 90 per gender | real, from `shoe_reviews.csv` | `pilot=0`; set `prolificurl`; set `attribute_order`; optional `show_number_of_reviews=0` |

Add `show_number_of_reviews=0` to any config to show the stars only.

## Shoe pictures
Pictures are loaded from the supervisor's host (`users.aalto.fi/.../shoepictures2026/men/` or `.../women/`), as `<product_id>_h.jpg`, chosen by the participant's gender. `check_images.py` still points at the old SportsDirect URL and is not needed for the new host.

## Things you still need to provide
1. **Review data**: fill `shoe_reviews.csv` (180 rows: first 90 male + first 90 female IDs; columns `avg_stars`, `n_reviews`, optional `source_url`). Use a real UK retailer, note the source and the collection date, and check the site's terms. Products with no reviews should be dropped from the lists or handled by a rule. Needed only for `multiattr_study`.
2. **`prolificurl`** in the study config.
3. **Final block lengths** (`BLOCK1/2/3_LENGTH`) and `MAX_ROUNDS`, agreed with your supervisor.
4. **`SECRET_KEY`** in `settings.py`: move it to an environment variable before deploying.
5. **Shared files at the repo root** (from the one-attribute project): `_static/my_folder/portraitmode.png` (used by `Information.html`), `_static/styles.css` (all swipe-card styles) and `_templates/global/Page.html`, which must contain `<link rel="stylesheet" href="{% static 'styles.css' %}">` inside `global_styles`. Without it none of the card styling or the hide-until-scroll rules apply.
6. **Card height**: `styles.css` fixes cards at 250 px high, which would clip the extra lines. `Decision.html` overrides this (same taller card in all three blocks, content centred). Check on a real phone that the A/B buttons are still visible.

## New data columns
`condition`, `thisround_discount1/2`, `thisround_discountdiff`, `thisround_stars1/2`, `thisround_nreviews1/2`, `nreviews_shown`, `reviews_placeholder` (1 = fake pilot reviews), `attr_order`, `pos_picture`, `pos_discount`, `pos_stars`, plus round-1 plans `attr_orders` and `discount_diffs`. Columns not shown in a block are empty. All process-tracing columns (`psiL/R`, `dwelltimeL/R`, `switchesLR/RL`, ...) are computed exactly as before.

`ismobile_touchstart` is set by a script when the first touch is detected on the first page, and is 0 by default in all other rounds: use round 1 only.

## Decisions to confirm with the supervisor
- "Rating" in block 1 is read as appearance (the picture); the participant's own Part 1 rating is not shown next to the pictures.
- Block 2/3 instructions tell people to use *all* the information shown (block 1 said style only). Wording is in `Instructions3.html` / `Instructions4.html`.
- Whether the number of reviews is shown with the stars (`show_number_of_reviews`). It changes how informative the stars are: 4.8 stars from 3 reviews and from 300 reviews look the same without the number.
- Fixed attribute positions confound an attribute with where it is shown; randomising them lets you estimate position effects. Per block or per trial is a design decision.
- Fixed block order confounds adding attributes with time, fatigue and learning.

## Carried over from the old code (not changed, so metrics stay comparable)
In `Decision.before_next_page`: (1) the crossing test `if (j>0) and (...) or (...)` evaluates its second clause at j=0 because of operator precedence; (2) the `x[-1] < 150` / `x[-1] >= 150` branches append `[x[0], y[0]]` where `[x[-1], y[-1]]` looks intended. Both affect `psiL/psiR` slightly; worth a look before data collection.

## Testing done
Bot runs under oTree 6.0.15 (`otree test <config> 2`) for pilot and study configs, with and without the review count: pairs, difficulty levels, attribute layouts, discount range, steps and gaps, agree/conflict balance, recorded versus drawn layout, and whether the count appears on the page (`tests.py` in the app folder). The reviews check was tested with a blank `n_reviews` column (accepted when the count is not shown, refused when it is). Not tested: rendering on a real phone.
