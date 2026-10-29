from otree.api import *
import ast
import csv
import os
import random

c = cu

doc = """
Binary choice with scroll tracking, multi-attribute version.
Part 1: rate trainers (appearance only).
Part 2: 90 rounds in three fixed-order blocks of 30 rounds:
  block 1 (rounds  1-30): appearance only
  block 2 (rounds 31-60): appearance + discount
  block 3 (rounds 61-90): appearance + discount + star reviews
"""


class C(BaseConstants):
    # built-in constants
    NAME_IN_URL = 'multiattr_binarychoice'
    PLAYERS_PER_GROUP = None
    BLOCK_LENGTH = 10
    NUM_BLOCKS = 3
    NUM_ROUNDS = BLOCK_LENGTH * NUM_BLOCKS  # 90
    # Discount levels (in %) drawn independently for each product on each trial in blocks 2 and 3.
    # 100 = full discount (free product). Change here if the range should be narrower.
    DISCOUNT_LEVELS = list(range(0, 101, 10))


# ---------------------------------------------------------------------------
# STIMULI
# ---------------------------------------------------------------------------
# Number of shoes per gender in pilot mode (session config pilot = 1)
PILOT_N_SHOES = 20

MALE_SHOES = [15147403, 12100503, 21001440, 12126140, 15133340, 16105627, 11798240, 12000002, 21228230, 15139716, 13149303, 11028927, 16105644, 16105601, 13138103, 12134602, 13149026, 16105699, 16105621, 12126103, 12254302, 12100540, 21001403, 16106103, 16105640, 11798203, 12000041, 16105642, 13149340, 13149041, 13123926, 15153203, 21153118, 13141627, 12000001, 12141001, 13149003, 13107203, 13149027, 13107227, 13123940, 12131399, 13141603, 12126143, 13149018, 12102121, 12105399, 12141003, 12105340, 13107201, 16105602, 13141625, 12000003, 21228208, 12131303, 13107240, 16105683, 12105301, 12100522, 13149040, 12126119, 12100402, 12257527, 13141640, 13123903, 13149099, 15146618, 12126147, 15112718, 15395841, 13149103, 12102103, 12000040, 13110730, 21060740, 12105303, 13110701, 16105608, 15148701, 12237827, 21005915, 13110703, 21010103, 15395740, 12237803, 15111704, 11795703, 13138640, 15101627, 13153740, 12126172, 12887143, 13145640, 21060826, 21073718, 13149032, 13106703, 15111706, 13149069, 12672703, 13100640, 15156141, 13110702, 12141037, 13149072, 21073501, 15148724, 12106926, 12672740, 13149033, 12141074, 15156201, 12887140, 13117908, 11028930]
#['13106703','13120641','13120626','12118603','16105642','12167703','16105601','12126118','12102103','12126140','13115602','13107203','12167727','16105627','12167740','13110701','13120603','12102140','12105303','16106101','13110703','12156040','12118630','12126103','21300503','12102167','21127840','12100403','21310803','21201127','12105340','12344303','12100418','21127803','12167702','21223903','12167718','12102144','12126172','12116803','12126147','12100430','12105301','13110730','13120703','12100540','12102174','12139947','12156027','21233703','12134603','21158040','12192203','12100503','12100440','13118503','12167746','12100427','12141003','12139902','21141240','12141025','12100522','21313803','13100903','21116240','12100469','13107201','16105640','11484401','12134630','12105403','12121025','12118640','15129641','12114503','21233907','12134640','11003201','15133302','11044501','21144303','12227401','12134602','21303008','16105030','16106203','12327127','21303018','12121022','12121041','16105637','16105003','12192218','12100415','16105669','12105331','12599702','15129630','12128127','12103340','12105408','21127801','12192241','21157801','12115340','12103308','12327103','12116002','14532403','15100903']

FEMALE_SHOES = [27419401, 27638735, 27434101, 21001315, 21600103, 27656407, 27198530, 27372703, 21025170, 21061403, 27400306, 21107306, 27656440, 27434103, 27419403, 27434182, 27400001, 27306676, 27307003, 27752137, 21000830, 27656403, 27400003, 21001215, 21025131, 27434140, 27656441, 27111302, 27209840, 27652203, 27638734, 27301903, 27198531, 27306630, 21061406, 21001334, 27410903, 27652240, 27652141, 27458001, 21040803, 21505203, 21084273, 21104208, 27638732, 21061420, 21001703, 27410901, 21153203, 27316903, 21107303, 21484635, 27400301, 21001307, 27400330, 21061470, 27306603, 27752107, 21025103, 21025127, 21001203, 27656415, 27434170, 27209832, 27306601, 27410932, 27111308, 21001340, 21025105, 27752101, 21000806, 27434131, 21084203, 27306621, 21025003, 21061119, 21000804, 27400309, 21025027, 27415927, 27752103, 27417603, 27209833, 21084206, 21061003, 21001099, 27106742, 27112103, 27234801, 21153231, 21001608, 21025102, 27306602, 27234803, 21025022, 27458332, 27106740, 27112101, 27434132, 27434177, 27142503, 27333540, 27198501, 21104227, 27234840, 27372203, 21001319, 21072403, 27401667, 21025120, 21104203, 27106703, 27647240]

#['27316903','27403330','27403303','27116503','21523003','27415901','27116540','27116501','27434132','27458003','21523007','27434101','27401667','21611503','27315203','27410901','27400303','27304603','27410902','27403340','27417640','27415927','27313803','27400340','27400301','21410803','21408340','21610503','27314003','27400335','27306543','21610524','27400370','27417603','27405642','27417641','27419403','27434131','27128303','21482506','27116525','27116544','27314025','21411406','27419401','27300712','27047602','27016940','27419427','27419440','27402441','27116040','14615701','27403840','27159840','21473907','27423569','27315227','27402430','21410806','27074327','27405640','27012903','27401603','27315103','27428801','27405636','27401601','27401636','27405027','21414906','27458306','27304307','27405630','27033018','27121002','27435032','21415407','27456831','21411403','27116572','21622203','27116569','27151640','27400330','21408324','27313830','27458001','27410931','27400337','27405631','21473901','21411430','21414903','27428803','27116571','27411030','27116519','27401607','27417642','27400367','27400203','21611524','27306303','27124640','21601002','27423501','27415903','21414942','27314006','27409141']

def shoe_list(gender, pilot):
    shoes = list(MALE_SHOES if gender == 'male' else FEMALE_SHOES)
    if pilot == 1:
        shoes = shoes[:PILOT_N_SHOES]
    return [int(s) for s in shoes]

# ---------------------------------------------------------------------------
# STAR REVIEWS
# ---------------------------------------------------------------------------
# Real review data goes in shoe_reviews.csv (same folder as this file) with columns
#   product_id, gender, avg_stars, n_reviews, source_url
# Rows with a blank avg_stars or n_reviews are ignored.
REVIEWS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shoe_reviews.csv')
_reviews_cache = None


def load_reviews():
    """Returns {product_id: (avg_stars, n_reviews)}; empty dict if the file is missing/unfilled."""
    global _reviews_cache
    if _reviews_cache is None:
        data = {}
        if os.path.exists(REVIEWS_FILE):
            with open(REVIEWS_FILE, newline='', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    try:
                        data[int(row['product_id'])] = (float(row['avg_stars']), int(float(row['n_reviews'])))
                    except (ValueError, KeyError, TypeError):
                        continue
        _reviews_cache = data
    return _reviews_cache


def placeholder_review(product_id):
    """PILOT ONLY: deterministic fake review for a product (same for every participant/round)."""
    r = random.Random(product_id)
    return round(r.uniform(2.5, 5.0), 1), r.randint(3, 250)


def get_review(product_id, use_placeholder):
    if use_placeholder:
        return placeholder_review(product_id)
    reviews = load_reviews()
    if product_id not in reviews:
        raise RuntimeError(
            f'No review data for product {product_id}. Fill in shoe_reviews.csv for all products, '
            f'or set use_placeholder_reviews=1 in the session config (pilot only).'
        )
    return reviews[product_id]


# ---------------------------------------------------------------------------
# DESIGN LOGIC (pure functions, no oTree objects)
# ---------------------------------------------------------------------------
def condition_of_round(round_number):
    """1 = appearance only, 2 = + discount, 3 = + discount + star reviews."""
    return (round_number - 1) // C.BLOCK_LENGTH + 1


def build_pairs(shoeorder, shoeratings, block_length=C.BLOCK_LENGTH, num_blocks=C.NUM_BLOCKS, rng=random):
    """
    Returns block_length*num_blocks pairs [shoeA, shoeB], ordered block by block.
    Within each block the rating differences (A - B, from the participant's own Part 1 ratings)
    are spread evenly over -3..3 (4 pairs per level + 2 extra levels drawn at random when
    block_length = 30), so every block has the same difficulty profile.
    Unordered pairs are not reused across blocks unless there are no fresh candidates left.
    The order of pairs is shuffled within a block, never across blocks.
    """
    rating = dict(zip(shoeorder, shoeratings))
    levels_all = list(range(-3, 4))
    bydiff = {d: [] for d in levels_all}
    for a in shoeorder:
        for b in shoeorder:
            if a != b:
                d = rating[a] - rating[b]
                if -3 <= d <= 3:
                    bydiff[d].append((a, b))
    available = [d for d in levels_all if bydiff[d]]

    used = set()
    pairs = []
    for _ in range(num_blocks):
        n_even = block_length // len(levels_all)
        levels = levels_all * n_even
        levels += rng.sample(levels_all, block_length - len(levels))
        block_pairs = []
        for d in levels:
            if not bydiff[d]:  # this participant has no pair with this difference
                d = rng.choice(available)
            fresh = [p for p in bydiff[d] if frozenset(p) not in used]
            pair = rng.choice(fresh if fresh else bydiff[d])
            used.add(frozenset(pair))
            block_pairs.append(list(pair))
        rng.shuffle(block_pairs)
        pairs += block_pairs
    return pairs


def draw_attributes(pair, condition, use_placeholder, rng=random):
    """
    Extra attributes shown for the two products of this round.
    Discounts are drawn independently for each product and trial (independent of the rating).
    Reviews are fixed per product (real data, or deterministic placeholder in pilot).
    """
    out = {}
    if condition >= 2:
        out['discount1'] = rng.choice(C.DISCOUNT_LEVELS)
        out['discount2'] = rng.choice(C.DISCOUNT_LEVELS)
    if condition >= 3:
        out['stars1'], out['nreviews1'] = get_review(pair[0], use_placeholder)
        out['stars2'], out['nreviews2'] = get_review(pair[1], use_placeholder)
    return out


# ---------------------------------------------------------------------------
# MODELS
# ---------------------------------------------------------------------------
class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    prolificcode = models.StringField()
    gender = models.StringField(choices=[['male', "men's trainers"], ['female', "women's trainers"]], label='<p>I would like to see ...</p>', widget=widgets.RadioSelect)
    shoeorder = models.StringField()
    shoeratings = models.StringField()
    shoepairs = models.StringField()
    thisround_shoepair = models.StringField()
    choice = models.IntegerField()
    lastdwell = models.IntegerField()
    dectime_end = models.FloatField()
    dectime = models.FloatField()
    scrolltime = models.FloatField()
    time_startscrolling = models.FloatField()
    time_endscrolling = models.FloatField()
    x = models.StringField()
    y = models.StringField()
    psiL = models.FloatField()
    psiR = models.FloatField()
    thisround_shoe1rating = models.IntegerField()
    thisround_shoe2rating = models.IntegerField()
    thisround_valuedifference = models.IntegerField()
    ismobile_touchstart = models.IntegerField(blank=True, initial=0)
    screenwidth = models.StringField(blank=True, initial='')
    screenheight = models.StringField(blank=True, initial='')
    dwelltimeL = models.FloatField()
    dwelltimeR = models.FloatField()
    switchesLR = models.IntegerField()
    switchesRL = models.IntegerField()
    xdist = models.FloatField()
    # --- new in the multi-attribute version ---
    condition = models.IntegerField()  # 1 = appearance, 2 = + discount, 3 = + discount + reviews
    thisround_discount1 = models.IntegerField()  # % off, left product (blank when not shown)
    thisround_discount2 = models.IntegerField()  # % off, right product
    thisround_stars1 = models.FloatField()  # average star rating, left product
    thisround_stars2 = models.FloatField()
    thisround_nreviews1 = models.IntegerField()  # number of reviews, left product
    thisround_nreviews2 = models.IntegerField()
    reviews_placeholder = models.IntegerField()  # 1 = fake pilot reviews were shown


# ---------------------------------------------------------------------------
# PAGES
# ---------------------------------------------------------------------------
class MobileCheck(Page):
    form_model = 'player'
    form_fields = ['ismobile_touchstart', 'screenwidth', 'screenheight']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        return dict(pilot=session.config['pilot'])


class Information(Page):
    form_model = 'player'
    form_fields = ['prolificcode']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Instructions(Page):
    form_model = 'player'
    form_fields = ['gender']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        session = player.session
        # Randomise the order of shoes
        shoes = shoe_list(player.gender, session.config['pilot'])
        random.shuffle(shoes)
        player.shoeorder = str(shoes)


class Preference(Page):
    form_model = 'player'
    form_fields = ['shoeratings']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        shoeorder = ast.literal_eval(player.shoeorder)

        divs = ''
        for i in range(len(shoeorder)):
            divs += '<span id=\"shoe' + str(i) + 'rating\" hidden></span>'

        return dict(divs=divs, shoeorder=shoeorder)

    @staticmethod
    def js_vars(player: Player):
        shoeorder = ast.literal_eval(player.shoeorder)

        player1 = player.in_round(1)

        if player1.gender == 'male': url = 'https://users.aalto.fi/ileppane/shoepictures2026/men/'
        else: url = 'https://users.aalto.fi/ileppane/shoepictures2026/women/'

        imagelist = [url + str(x) + '_h.jpg' for x in shoeorder]
      
        #imagelist = ["https://www.sportsdirect.com/images/products/" + str(x) + "_h.jpg" for x in shoeorder]
        #imagelist = ["https://users.aalto.fi/~ileppane/shoepictures2026/" + str(x) + "_h.jpg" for x in shoeorder] 

        return dict(numberofshoes=len(shoeorder), shoeorder=shoeorder, imagelist=imagelist)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Here the 90 pairs (3 blocks x 30) are created from the participant's own ratings
        shoeorder = ast.literal_eval(player.shoeorder)
        shoeratings = ast.literal_eval(player.shoeratings)
        player.shoepairs = str(build_pairs(shoeorder, shoeratings))
        # the pair for each round can now be found in player.in_round(1).shoepairs


class Instructions2(Page):
    """Start of Part 2 / block 1 (appearance only)."""

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Instructions3(Page):
    """Start of block 2 (appearance + discount)."""

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.BLOCK_LENGTH + 1


class Instructions4(Page):
    """Start of block 3 (appearance + discount + star reviews)."""

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2 * C.BLOCK_LENGTH + 1


class PreDecision(Page):
    form_model = 'player'
    timeout_seconds = 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        session = player.session

        # Determine the pair of shoes for this round and calculate their ratings and valuedifference
        shoepairs = ast.literal_eval(player.in_round(1).shoepairs)
        thisround_shoepair = shoepairs[player.round_number - 1]
        shoeorder = ast.literal_eval(player.in_round(1).shoeorder)
        shoeratings = ast.literal_eval(player.in_round(1).shoeratings)  # ratings = subjective preferences given by player

        player.thisround_shoepair = str(thisround_shoepair)
        player.thisround_shoe1rating = int(shoeratings[shoeorder.index(thisround_shoepair[0])])
        player.thisround_shoe2rating = int(shoeratings[shoeorder.index(thisround_shoepair[1])])
        player.thisround_valuedifference = player.thisround_shoe1rating - player.thisround_shoe2rating

        # Block / condition and the extra attributes shown in this round
        use_placeholder = bool(session.config.get('use_placeholder_reviews', 0))
        player.condition = condition_of_round(player.round_number)
        attrs = draw_attributes(thisround_shoepair, player.condition, use_placeholder)
        player.thisround_discount1 = attrs.get('discount1')
        player.thisround_discount2 = attrs.get('discount2')
        player.thisround_stars1 = attrs.get('stars1')
        player.thisround_stars2 = attrs.get('stars2')
        player.thisround_nreviews1 = attrs.get('nreviews1')
        player.thisround_nreviews2 = attrs.get('nreviews2')
        player.reviews_placeholder = int(use_placeholder and player.condition >= 3)


class Decision(Page):
    form_model = 'player'
    form_fields = ['choice', 'dectime_end', 'x', 'y', 'time_startscrolling', 'time_endscrolling', 'lastdwell']

    @staticmethod
    def vars_for_template(player: Player):
        shoepair = ast.literal_eval(player.thisround_shoepair)
        player1 = player.in_round(1)

        if player1.gender == 'male':
          url = 'https://users.aalto.fi/ileppane/shoepictures2026/men/'
        else:
          url = 'https://users.aalto.fi/ileppane/shoepictures2026/women/'

        return dict(
            #shoeimage1='https://www.sportsdirect.com/images/products/' + str(shoepair[0]) + '_h.jpg',
            #shoeimage2='https://www.sportsdirect.com/images/products/' + str(shoepair[1]) + '_h.jpg',
            #shoeimage1='https://users.aalto.fi/ileppane/shoepictures2026/men/' + str(shoepair[0]) + '_h.jpg',
            #shoeimage2='https://users.aalto.fi/ileppane/shoepictures2026/women/' + str(shoepair[1]) + '_h.jpg',
            shoeimage1=url + str(shoepair[0]) + '_h.jpg',
            shoeimage2=url + str(shoepair[1]) + '_h.jpg',
            beginning=player.round_number <= 3,
            show_discount=player.condition >= 2,
            show_reviews=player.condition >= 3,
            # these are empty (None) in blocks where the attribute is not shown, hence field_maybe_none
            discount1=player.field_maybe_none('thisround_discount1'),
            discount2=player.field_maybe_none('thisround_discount2'),
            stars1=player.field_maybe_none('thisround_stars1'),
            stars2=player.field_maybe_none('thisround_stars2'),
            nreviews1=player.field_maybe_none('thisround_nreviews1'),
            nreviews2=player.field_maybe_none('thisround_nreviews2'),
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(choice1='Product A', choice2='Product B')

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # NOTE: everything below is kept identical to the one-attribute study so that the
        # process-tracing metrics are comparable across studies.

        # dectime ends when the button is clicked
        player.dectime = round((player.dectime_end - player.time_startscrolling) / 1000, 3)

        # scrolltime ends when the last x coordinate is recorded
        player.scrolltime = round((player.time_endscrolling - player.time_startscrolling) / 1000, 3)

        ### CALCULATING THE PROCESS TRACING METRICS psiL and psiR
        ##
        x = ast.literal_eval(player.x)
        y = ast.literal_eval(player.y)

        # the below line removes the first element(s) from x; reason: x always has more points than y
        # this is because the divs are initially blank and show only after scrolling about 3px, but
        # y starts recording only after divs are shown
        x = x[(len(x) - len(y)):len(x)]

        # total distance travelled in x-direction
        player.xdist = sum(abs(x[i + 1] - x[i]) for i in range(len(x) - 1))

        # append the points to make a curve; the right/left "dwell" starts when x crosses 150 and ends when it crosses 150 again
        xyright = []
        xyleft = []
        for j in range(len(x)):
            if (j > 0) and (x[j - 1] <= 150 and x[j] > 150) or (x[j - 1] >= 150 and x[j] < 150): xyright.append([150, y[j]])
            if (j > 0) and (x[j - 1] <= 150 and x[j] > 150) or (x[j - 1] >= 150 and x[j] < 150): xyleft.append([150, y[j]])
            if x[j] >= 150: xyright.append([x[j], y[j]])
            if x[j] < 150: xyleft.append([x[j], y[j]])

        # add the vertical midpoint line on both
        xyright.append([150, y[-1]])
        xyright.append([150, y[0]])
        xyleft.append([150, y[-1]])
        xyleft.append([150, y[0]])

        # add the horizontal lines
        if x[0] < 150: xyleft.append([x[0], y[0]])
        if x[0] >= 150: xyright.append([x[0], y[0]])
        if x[-1] < 150: xyleft.append([x[0], y[0]])
        if x[-1] >= 150: xyright.append([x[0], y[0]])

        # calculate psiR using xyright
        l = len(xyright)
        s = 0.0
        for i in range(l):
            j = (i + 1) % l  # keep index in [0,l)
            s += (xyright[j][0] - xyright[i][0]) * (xyright[j][1] + xyright[i][1])

        psiR = -0.5 * s

        # calculate psiL using xyleft
        l = len(xyleft)
        s = 0.0
        for i in range(l):
            j = (i + 1) % l  # keep index in [0,l)
            s += (xyleft[j][0] - xyleft[i][0]) * (xyleft[j][1] + xyleft[i][1])

        psiL = -0.5 * s

        player.psiL = abs(psiL)
        player.psiR = abs(psiR)

        ### CALCULATING PROCESS TRACING METRICS dwelltimeL, dwelltimeR and switchesLR, switchesRL
        ##
        dwelltimeleft = 0
        dwelltimeright = 0
        lr = 0
        rl = 0
        for i in range(1, len(y)):
            # dwelltimes
            if x[i] < 150:
                dwelltimeleft += y[i] - y[i - 1]
            if x[i] >= 150:
                dwelltimeright += y[i] - y[i - 1]
            # switches
            if i == 1:  # first switch added separately because stimuli become visible only after a bit of scrolling
                if x[i] > 150: lr += 1
                if x[i] < 150: rl += 1
            if x[i - 1] >= 150 and x[i] < 150:  # going from right to left
                rl += 1
            if x[i - 1] <= 150 and x[i] > 150:  # going from left to right
                lr += 1

        player.dwelltimeR = round(.001 * dwelltimeright, 3)
        player.dwelltimeL = round(.001 * dwelltimeleft, 3)
        player.switchesLR = lr
        player.switchesRL = rl


class ResponseCurve(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        # display in pilot only for the first 3 rounds and the first round of blocks 2 and 3
        first_of_block = player.round_number in (C.BLOCK_LENGTH + 1, 2 * C.BLOCK_LENGTH + 1)
        return session.config['pilot'] == 1 and (player.round_number <= 3 or first_of_block)

    @staticmethod
    def vars_for_template(player: Player):
        x = ast.literal_eval(player.x)
        y = ast.literal_eval(player.y)

        return dict(x=x, y=y)

    @staticmethod
    def js_vars(player: Player):
        x = ast.literal_eval(player.x)
        y = ast.literal_eval(player.y)

        return dict(x=x, y=y)


class Results(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        return dict(
            prolificurl=session.config['prolificurl']
        )


# One sequence for all 90 rounds: oTree runs the whole sequence once per round,
# so the block-specific instruction pages are switched on by round number (is_displayed above).
page_sequence = [MobileCheck, Information, Instructions, Preference,
                 Instructions2, Instructions3, Instructions4,
                 PreDecision, Decision, ResponseCurve, Results]
