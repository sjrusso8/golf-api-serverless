import random
import string

DEFAULT_CHAR_STRING = string.ascii_lowercase + string.digits


def generate_random_string(chars=DEFAULT_CHAR_STRING, size=6):
    return ''.join(random.choice(chars) for _ in range(size))


ROUND_TYPE = [
    ('18', '18 Holes'),
    ('F9', 'Front 9'),
    ('B9', 'Back 9'),
]

SHOT_SHAPE = [
    ('H', 'Hook'),
    ('LD', 'Left Draw'),
    ('L', 'Left'),
    ('LF', 'Left Fade'),
    ('D', 'Draw'),
    ('ST', 'Straight'),
    ('F', 'Fade'),
    ('RD', 'Right Draw'),
    ('R', 'Right'),
    ('RF', 'Right Fade'),
    ('S', 'Slice'),
    ('SK', 'Shank'),
    ('ER', 'Hitting Error'),
]

# SHOT_LIE = [
#     ('TB', "Tee Box"),
#     ('FR', 'Fairway'),
#     ('GR', 'Green'),
#     ('GB', 'Greenside Bunker'),
#     ('FB', 'Fairway Bunker'),
#     ('LR', 'Left Rough'),
#     ('RR', 'Right Rough'),
# ]

# INTENT = [
#     ("HR", "Hit Fairway"),
#     ("HG", "Hit Green"),
#     ("LU", "Lay up"),
#     ("IP", "Back in Play"),
#     ("HO", "Hole Out"),
#     ("CC", "Chip Close"),
#     ("2P", "2 Putt"),
# ]

OUTCOME = [
    ("LO", "Missed Long"),
    ("LT", "Missed Left"),
    ("RT", "Missed Right"),
    ("HT", "Hit"),
    ("SH", "Missed Short"),
    ("SK", "Shank"),
    ("NA", "NA"),
]

PENALTIES = [
    ("S", "Greenside Bunker"),
    ("F", "Fairway Bunker"),
    ("O", "Out of Bounds"),
    ("W", "Water Hazard"),
    ("D", "Drop or Other")
]

GENERIC_CLUBS = [
    ('DR', 'Driver'),
    ('W3', '3 Wood'),
    ('W4', '4 Wood'),
    ('W5', '5 Wood'),
    ('W6', '6 Wood'),
    ('W7', '7 Wood'),
    ('U3', '3 Utility'),
    ('U4', '4 Utility'),
    ('U5', '5 Utility'),
    ('U6', '6 Utility'),
    ('U7', '7 Utility'),
    ('i3', '3 Iron'),
    ('i4', '4 Iron'),
    ('i5', '5 Iron'),
    ('i6', '6 Iron'),
    ('i7', '7 Iron'),
    ('i8', '8 Iron'),
    ('i9', '9 Iron'),
    ('PW', 'Pitching Wedge'),
    ('UW', 'Utility Wedge'),
    ('GW', 'Gap Wedge'),
    ('SW', 'Sand Wedge'),
    ('LW', 'Lop Wedge'),
    ('PT', 'Putter')
]
