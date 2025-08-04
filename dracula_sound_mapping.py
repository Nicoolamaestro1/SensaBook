# Dracula Sound Mapping - Focused on Meaningful Atmospheric Sounds
# Book ID: 10 - Dracula by Bram Stoker

# SCENE_SOUND_MAPPINGS - Atmospheric scenes that set the mood
SCENE_SOUND_MAPPINGS = {
    "dracula_castle": {
        "keywords": ["castle", "dracula", "count", "vampire", "tomb", "grave", "coffin", "undead", "blood", "throat"],
        "carpet": "gothic_castle_ambience.mp3"
    },
    "dracula_night": {
        "keywords": ["night", "dark", "darkness", "shadow", "shadows", "moon", "stars", "starry", "evening", "dusk", "twilight", "black", "gloom", "obscure"],
        "carpet": "night_ambience.mp3"
    },
    "dracula_storm": {
        "keywords": ["storm", "thunder", "lightning", "clouds", "dark clouds", "tempest", "gale", "wind", "stormy", "thunderstorm", "tempestuous"],
        "carpet": "storm_ambience.mp3"
    },
    "dracula_forest": {
        "keywords": ["forest", "trees", "woods", "grove", "thicket", "wilderness", "mountain", "mountains", "peak", "peaks", "ridge", "cliff", "rocky", "stone"],
        "carpet": "forest_ambience.mp3"
    },
    "dracula_journey": {
        "keywords": ["ride", "riding", "journey", "travel", "road", "path", "way", "steeds", "horses", "mount", "gallop", "trot", "leagues", "miles", "distance", "traveling", "carriage", "train"],
        "carpet": "travel_ambience.mp3"
    },
    "dracula_water": {
        "keywords": ["water", "river", "sea", "ocean", "ship", "boat", "sailing", "waves", "lapping", "swirling", "creaking", "wood"],
        "carpet": "water_ambience.mp3"
    },
    "dracula_fear": {
        "keywords": ["fear", "afraid", "creepy", "haunted", "disaster", "evil", "terrifying", "horror", "dread", "terror", "panic", "anxiety"],
        "carpet": "tense_drones.mp3"
    },
    "dracula_battle": {
        "keywords": ["battle", "fight", "combat", "weapon", "sword", "knife", "gun", "rifle", "attack", "defend", "struggle", "conflict"],
        "carpet": "battle_ambience.mp3"
    },
    "dracula_wolves": {
        "keywords": ["wolf", "wolves", "howling", "beast", "animal", "wild", "hunt", "prey"],
        "carpet": "wolf_howls.mp3"
    }
}

# WORD_TO_SOUND - Specific sound effects that make sense
WORD_TO_SOUND = {
    # Dracula-specific sounds
    "dracula": "vampire_hiss.mp3",
    "vampire": "vampire_hiss.mp3", 
    "blood": "blood_drip.mp3",
    "throat": "throat_slice.mp3",
    "bite": "vampire_bite.mp3",
    "fangs": "vampire_bite.mp3",
    
    # Atmospheric sounds
    "thunder": "thunder_roll.mp3",
    "lightning": "lightning_crack.mp3",
    "storm": "storm_wind.mp3",
    "wind": "wind_howl.mp3",
    
    # Action sounds
    "footsteps": "footsteps_stone.mp3",
    "door": "door_creak.mp3",
    "knife": "knife_unsheathe.mp3",
    "sword": "sword_clash.mp3",
    "gun": "gunshot.mp3",
    "rifle": "rifle_shot.mp3",
    
    # Animal sounds
    "wolf": "wolf_howl.mp3",
    "wolves": "wolf_pack.mp3",
    "horse": "horse_neigh.mp3",
    "horses": "horses_gallop.mp3",
    
    # Water sounds
    "waves": "waves_crash.mp3",
    "water": "water_flow.mp3",
    "river": "river_current.mp3",
    "ship": "ship_creak.mp3",
    
    # Battle sounds
    "fight": "battle_clash.mp3",
    "battle": "battle_roar.mp3",
    "attack": "sword_strike.mp3",
    
    # Fear/terror sounds
    "scream": "human_scream.mp3",
    "cry": "desperate_cry.mp3",
    "moan": "pain_moan.mp3",
    
    # Castle/creepy sounds
    "castle": "castle_echo.mp3",
    "tomb": "tomb_creak.mp3",
    "coffin": "coffin_open.mp3",
    "grave": "earth_shift.mp3"
}

# Priority order for carpet sounds (higher index = higher priority)
CARPET_PRIORITY = [
    "dracula_fear", "dracula_battle", "dracula_wolves", "dracula_storm", 
    "dracula_castle", "dracula_night", "dracula_forest", "dracula_water", "dracula_journey"
]

# Suggested MP3 files to acquire for Dracula:
SUGGESTED_SOUND_FILES = {
    # Carpet/Ambient Sounds
    "gothic_castle_ambience.mp3": "Dark, echoing castle atmosphere with distant moans",
    "night_ambience.mp3": "Quiet night sounds with occasional owl hoots",
    "storm_ambience.mp3": "Thunder, rain, and wind combined",
    "forest_ambience.mp3": "Rustling leaves, distant animal sounds",
    "travel_ambience.mp3": "Horse hooves, carriage wheels, journey sounds",
    "water_ambience.mp3": "Flowing water, ship creaks, waves",
    "tense_drones.mp3": "Low, ominous background tension",
    "battle_ambience.mp3": "Clashing weapons, shouts, chaos",
    "wolf_howls.mp3": "Distant wolf pack howling",
    
    # Specific Sound Effects
    "vampire_hiss.mp3": "Dracula's menacing hiss",
    "blood_drip.mp3": "Dripping blood sound",
    "throat_slice.mp3": "Sharp cutting sound",
    "vampire_bite.mp3": "Fangs sinking into flesh",
    "thunder_roll.mp3": "Deep thunder rumble",
    "lightning_crack.mp3": "Sharp lightning strike",
    "storm_wind.mp3": "Howling storm wind",
    "wind_howl.mp3": "Eerie wind through trees",
    "footsteps_stone.mp3": "Footsteps on stone floors",
    "door_creak.mp3": "Old door creaking open",
    "knife_unsheathe.mp3": "Knife being drawn",
    "sword_clash.mp3": "Swords clashing together",
    "gunshot.mp3": "Single gunshot",
    "rifle_shot.mp3": "Rifle firing",
    "wolf_howl.mp3": "Single wolf howl",
    "wolf_pack.mp3": "Multiple wolves howling",
    "horse_neigh.mp3": "Horse whinny",
    "horses_gallop.mp3": "Multiple horses running",
    "waves_crash.mp3": "Ocean waves crashing",
    "water_flow.mp3": "Flowing water sound",
    "river_current.mp3": "River water movement",
    "ship_creak.mp3": "Wooden ship creaking",
    "battle_clash.mp3": "Weapons clashing",
    "battle_roar.mp3": "Battle cries and chaos",
    "sword_strike.mp3": "Sword striking",
    "human_scream.mp3": "Human scream of terror",
    "desperate_cry.mp3": "Desperate human cry",
    "pain_moan.mp3": "Pain-filled moan",
    "castle_echo.mp3": "Echoing castle halls",
    "tomb_creak.mp3": "Tomb opening sound",
    "coffin_open.mp3": "Coffin lid opening",
    "earth_shift.mp3": "Earth moving/shifting"
} 