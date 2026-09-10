"""
iheart_identifiers.py — the full categorized iHeartMedia detection list
from more-podcast-intelligence, pulled out into its own module so it's
not buried inside daily_scrape.py.

Use check_iheart(*fields) against any combination of show title/author/
description to flag iHeart-affiliated shows in chart_entries.
"""

PARENT_IDENTIFIERS = [
    "iheartmedia", "iheartradio", "iheartpodcasts",
    "iheart podcasts", "iheart media",
]

OWNED_NETWORKS = [
    "howstuffworks", "big money players", "black effect", "my cultura",
    "will media", "ruby media", "cool zone media", "tenderfoot tv",
    "pushkin industries", "exactly right", "shondaland", "shondaland audio",
    "meateater", "outspoken", "inflection",
]

HOWSTUFFWORKS_SHOWS = [
    "stuff you should know", "stuff you missed in history",
    "stuff they don't want you to know", "stuff mom never told you",
    "stuff to blow your mind", "brainstuff", "sciencestuff", "savor",
]

COOL_ZONE_SHOWS = [
    "behind the bastards", "it could happen here", "internet hate machine",
    "ghost church", "sixteenth minute",
]

TENDERFOOT_SHOWS = [
    "atlanta monster", "monster: dc sniper", "up and vanished",
    "your own backyard", "happy face", "hell and gone", "le monstre",
]

EXACTLY_RIGHT_SHOWS = [
    "my favorite murder", "buried bones", "that's messed up", "small town dicks",
]

BIG_MONEY_PLAYERS_SHOWS = [
    "all the smoke", "club shay shay", "shannon sharpe",
    "literally with rob lowe", "this is important", "fly on the wall",
    "good fortune with ed helms", "i am all in", "fake doctors real friends",
    "dear chelsea", "dear chelsea with chelsea handler",
]

BLACK_EFFECT_SHOWS = [
    "all the smoke", "85 south show", "the 85 south comedy show",
    "earn your leisure", "the black effect", "therapy for black girls",
    "the read", "yo, is this racist", "the lover boys",
    "questlove supreme", "the questlove show",
    "higher learning with van lathan", "say race with dr ibram x kendi",
    "in black america", "codie with an ie",
    "selective ignorance with mandii b", "selective ignorance",
    "laugh and learn", "i didn't know maybe you didn't either", "the trap",
]

MY_CULTURA_SHOWS = [
    "ponle pausa", "lele pons", "this is your life", "latinos who lunch",
    "brown girl self care", "my curious familia", "señora sex ed",
    "bleep with ana navarro", "who made you with eva longoria", "who made you",
    "locatora radio", "latinx files", "fierce",
]

SHONDALAND_SHOWS = [
    "shondaland audio", "katie's crib", "katie couric",
    "tell me with katie couric", "the betches", "betches",
    "you're wrong about", "scandal rewatch podcast", "greys anatomy rewatch",
    "how to save a planet", "bridgerton: the official podcast",
    "inventing anna", "queen charlotte",
]

PUSHKIN_SHOWS = [
    "revisionist history", "revisionist history with malcolm gladwell",
    "malcolm gladwell", "broken record", "broken record with rick rubin",
    "rick rubin", "cautionary tales", "tim harford", "against the rules",
    "michael lewis", "deep background with noah feldman", "the happiness lab",
    "dr laurie santos", "laurie santos", "the moment with brian koppelman",
    "rework", "by the book", "an arm and a leg", "poog", "land of the giants",
    "heavyweight", "not lost", "deep cover",
]

SPORTS_SHOWS = [
    "new heights with jason and travis kelce", "new heights",
    "jason kelce", "travis kelce",
    "the colin cowherd podcast", "colin cowherd",
    "the herd with colin cowherd", "the herd",
    "undisputed", "skip bayless", "shannon sharpe", "club shay shay",
    "the rich eisen show", "rich eisen", "rex chapman show",
    "pat mcafee show", "pat mcafee", "dan patrick show", "dan patrick",
    "mcafee and hawk", "bleacher report podcast", "the volume",
    "the rennae stubbs tennis podcast", "rennae stubbs",
    "women's sports audio network",
]

RADIO_PERSONALITY_SHOWS = [
    "the breakfast club", "charlamagne tha god", "dj envy", "jess hilarious",
    "bobby bones", "the bobby bones show",
    "bobby bones presents the bobbycast", "bobbycast",
    "ryan seacrest", "on air with ryan seacrest",
    "coast to coast am", "george noory",
    "armstrong and getty", "the armstrong and getty show",
    "the morning mash up", "brooke and jeffrey",
    "catch up with brandi cyrus", "brandi cyrus",
    "people every day", "steve harvey morning show",
    "the steve harvey morning show", "elvis duran",
]

NEWS_SHOWS = [
    "the daily dive", "politics war room",
    "the sean hannity podcast", "sean hannity",
    "the glen beck program", "glenn beck",
    "rush limbaugh", "the rush limbaugh show",
    "ben shapiro", "the ben shapiro show",
    "mark levin", "the mark levin show",
    "verdict with ted cruz", "ted cruz",
    "american history tellers", "american scandal",
    "the big picture", "inflection with andrea mitchell",
    "the clay travis and buck sexton show", "2 pros and a cup of joe",
    "breaking points with krystal and saagar",
    "countdown with keith olbermann",
    "next question with katie couric",
]

HEALTH_SHOWS = [
    "on purpose with jay shetty", "on purpose", "jay shetty",
    "iweigh with jameela jamil", "jameela jamil",
    "therapy for black girls", "the dr john delony show", "john delony",
    "a healthier mind", "the psychology of your 20s", "psychology of your 20s",
    "feel better live more", "ten percent happier",
    "ten percent happier with dan harris",
    "unlocking us with brene brown", "brene brown", "brené brown",
]

TRUE_CRIME_SHOWS = [
    "crime junkie", "dr death", "dr. death", "dirty john",
    "over my dead body", "blood ties", "even the rich",
    "betrayal", "betrayal podcast", "your own backyard",
    "scam goddess", "the cold", "something was wrong",
    "fighting conviction", "the piketon massacre", "atlanta monster",
    "dead eyes", "freeway phantom",
    "wrongful conviction", "wrongful conviction with jason flom", "jason flom",
    "redhanded", "disgraceland", "smokescreen", "school of humans",
    "american shadows", "the secret world of roald dahl",
    "love trapped", "doubt", "mind games",
]

COMEDY_SHOWS = [
    "las culturistas", "las culturistas with matt rogers and bowen yang",
    "matt rogers", "bowen yang",
    "fly on the wall", "fly on the wall with dana carvey",
    "dana carvey", "david spade",
    "this is important", "workaholics",
    "adam devine", "anders holm", "blake anderson",
    "smartless", "thanks dad", "ego nwodim",
    "good one a podcast about jokes", "good one",
    "conan o'brien needs a friend", "conan obrien needs a friend",
    "conan needs a friend", "handsome rambler",
    "the ron burgundy podcast", "snafu with ed helms",
    "here's the thing with alec baldwin", "boysober", "ok storytime",
]

CULTURE_SHOWS = [
    "bookmarked by reese's book club", "bookmarked", "reese witherspoon",
    "the michelle obama podcast", "michelle obama",
    "oprah's supersoul", "oprah",
    "getting curious with jonathan van ness", "jonathan van ness", "jvn",
    "ologies with alie ward", "ologies",
    "no stupid questions", "freakonomics radio", "freakonomics", "stephen dubner",
    "stuff you should know", "a way with words", "wait wait don't tell me",
    "drink champs", "red table talk", "two ts in a pod", "pod meets world",
    "brown ambition", "good game with sarah spain",
    "latino usa", "radio ambulante", "american history hotline", "hungry for history",
    "the official yellowstone podcast", "no grip", "earn your leisure",
]

NETFLIX_PARTNERSHIP_SHOWS = [
    "my favorite murder", "the breakfast club",
    "bobby bones presents the bobbycast",
    "behind the bastards", "the psychology of your 20s",
    "dear chelsea", "this is important", "las culturistas",
    "new heights", "fly on the wall", "literally with rob lowe",
    "the questlove show", "earn your leisure", "smartless",
]

BLOOMBERG_SHOWS = [
    "odd lots", "masters in business", "bloomberg surveillance",
    "bloomberg businessweek", "trillions", "bloomberg crypto",
    "zero", "money stuff the podcast", "foundering",
    "the david rubenstein show",
]

MEATEATER_SHOWS = [
    "meateater podcast", "the meateater podcast", "steven rinella", "rinella",
    "wired to hunt", "out alive", "hunting collective", "hunting with style",
    "bear grease", "cal of the wild", "in pursuit", "meateater kids",
]

IHEARTMEDIA_HOSTS = [
    "charlamagne tha god", "dj envy", "jess hilarious", "bobby bones",
    "colin cowherd", "jay shetty", "karen kilgariff", "georgia hardstark",
    "robert evans", "payne lindsey", "donald albright",
    "malcolm gladwell", "josh clark", "chuck bryant",
    "christian johnson", "will pearson",
    "katie couric", "jameela jamil", "chelsea handler",
    "rob lowe", "ed helms", "dana carvey",
    "matt rogers", "bowen yang", "shonda rhimes", "questlove",
    "jason kelce", "travis kelce", "rich eisen",
    "ana navarro", "eva longoria", "ego nwodim",
    "brene brown", "brené brown", "reese witherspoon",
]

IHEART_IDENTIFIERS = list(set(
    PARENT_IDENTIFIERS + OWNED_NETWORKS + HOWSTUFFWORKS_SHOWS +
    COOL_ZONE_SHOWS + TENDERFOOT_SHOWS + EXACTLY_RIGHT_SHOWS +
    BIG_MONEY_PLAYERS_SHOWS + BLACK_EFFECT_SHOWS + MY_CULTURA_SHOWS +
    SHONDALAND_SHOWS + PUSHKIN_SHOWS + SPORTS_SHOWS +
    RADIO_PERSONALITY_SHOWS + NEWS_SHOWS + HEALTH_SHOWS +
    TRUE_CRIME_SHOWS + COMEDY_SHOWS + CULTURE_SHOWS +
    NETFLIX_PARTNERSHIP_SHOWS + BLOOMBERG_SHOWS + MEATEATER_SHOWS +
    IHEARTMEDIA_HOSTS
))


def is_iheart(text: str) -> bool:
    if not text:
        return False
    lower = text.lower()
    return any(kw in lower for kw in IHEART_IDENTIFIERS)


def check_iheart(*fields) -> bool:
    return any(is_iheart(f) for f in fields)
