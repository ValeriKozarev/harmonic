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

def to_camelot(key, mode):
    if key == -1:
        return "Unknown"
    
    return pitch_class_dict[(key, mode)]