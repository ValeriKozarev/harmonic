### This module contains the logic for translating between keys/Camelot notation as well as ranking songs by harmonic compatibility.

pitch_class_dict = {
    # key is a tuple of key integer and mode (0 for minor, 1 for major)
    (0, 0): "5A",
    (0, 1): "8B",
    (1, 0): "12A",
    (1, 1): "3B",
    (2, 0): "7A",
    (2, 1): "10B",
    (3, 0): "2A",
    (3, 1): "5B",
    (4, 0): "9A",
    (4, 1): "12B",
    (5, 0): "4A",
    (5, 1): "7B",
    (6, 0): "10A",
    (6, 1): "1B",
    (7, 0): "6A",
    (7, 1): "9B",
    (8, 0): "11A",
    (8, 1): "2B",
    (9, 0): "1A",
    (9, 1): "4B",
    (10, 0): "8A",
    (10, 1): "11B",
    (11, 0): "3A",
    (11, 1): "6B",
}

# convert key to Camelot notation
def to_camelot(key, mode):
    if key == -1:
        return "Unknown"
    
    return pitch_class_dict[(key, mode)]

# find the distance between two keys on the Camelot wheel for ranking and comparison
def calc_camelot_dist(key1, key2):
    key1_num, key1_mode = int(key1[:-1]), key1[-1]
    key2_num, key2_mode = int(key2[:-1]), key2[-1]

    diff = abs(key1_num - key2_num) % 12

    # note: naive approach to start, we'll bump the distance by 1 if the mode doesn't match though I think there is more nuance here...
    mode_diff = 1 if key1_mode != key2_mode else 0

    distance = min(diff, 12 - diff) + mode_diff

    return distance

# given a list of tracks and some criteria (BPM and Camelot key) to match against, return them in ranked order in terms of best match
def rank_tracks(tracks, target_bpm, target_key):
    results = []

    for track in tracks:
        bpm_dist = abs(track["bpm"] - target_bpm)
        key_dist = calc_camelot_dist(track["camelot_key"], target_key)

        # TODO: it would be nice to make this more granular in the future

        if (bpm_dist <= 5 and key_dist <= 2):
            tier = "Perfect Match"
        elif (bpm_dist <= 10 and key_dist <= 3):
            tier = "Workable"
        elif (10 < bpm_dist <= 15 and key_dist <= 4):
            tier = "Ok"
        else:
            continue # bad matches don't even get included in the final results array

        results.append({**track, "tier": tier, "score": (key_dist, bpm_dist)}) # slightly giving the edge to key being more important here

    tier_order = {
        "Perfect Match": 0,
        "Workable": 1,
        "Ok": 2
    }
    return sorted(results, key=lambda t: (tier_order[t["tier"]], t["score"][0], t["score"][1])) # sort by tier first, then key distance, then bpm distance
