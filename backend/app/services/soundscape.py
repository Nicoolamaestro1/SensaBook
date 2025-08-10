import re
from collections import Counter, defaultdict
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from .book import get_page
from .emotion_analysis import find_trigger_words, AdvancedEmotionAnalyzer

# Enhanced scene sound mappings with sophisticated regex patterns and psychoacoustic metadata
ENHANCED_SCENE_SOUND_MAPPINGS = {
    # Epic and Heroic Scenes
    "epic_battle": {
        "patterns": [
            # Primary battle indicators with enhanced context
            r"\b(epic|heroic|mighty|powerful|tremendous|overwhelming|colossal|massive)\s+(battle|struggle|war|conflict|fight|clash|combat|confrontation)\b",
            # Secondary intensity modifiers with emotional depth
            r"\b(grand|magnificent|tremendous|colossal|massive|monumental)\s+(scale|proportions|display|force|impact|magnitude|presence)\b",
            # Emotional intensity cues for dynamic audio
            r"\b(heart|pulse|adrenaline|spirit|courage)\s+(racing|pounding|surge|rush|explosion|soaring|unleashed)\b",
            # Temporal dynamics for sound evolution
            r"\b(sudden|abrupt|instant|momentary|fleeting|dramatic)\s+(explosion|burst|flash|surge|wave|transformation|revelation)\b",
            # Advanced battle context patterns
            r"\b(warrior|champion|hero|legend)\s+(rises|emerges|unleashes|demonstrates|proves)\b",
            r"\b(ultimate|final|decisive|climactic)\s+(moment|battle|confrontation|showdown|victory)\b"
        ],
        "weight": 5,
        "mood": "epic",
        "carpet": "ambience/storm",
        "psychoacoustic": {
            "frequency_range": "low_mid",      # 200-800Hz for epic feel
            "spatial_width": "wide",           # Full stereo field
            "temporal_dynamics": "crescendo",  # Building intensity
            "emotional_curve": "rising_tension",
            "volume_profile": "dynamic",       # Variable volume for impact
            "reverb_type": "large_outdoor"    # Epic space feeling
        }
    },
    
    # Mystical and Magical Scenes
    "mystical_magic": {
        "patterns": [
            # High-frequency mystical elements for sparkle
            r"\b(sparkle|twinkle|shimmer|glisten|radiate|gleam|scintillate)\s+(light|energy|magic|essence|aura|presence|beauty)\b",
            # Mid-frequency magical presence for warmth
            r"\b(magical|mystical|ethereal|otherworldly|enchanted|supernatural|divine)\s+(presence|power|energy|atmosphere|realm|world|existence)\b",
            # Low-frequency ancient wisdom for depth
            r"\b(ancient|timeless|eternal|primal|primordial|immortal|legendary)\s+(wisdom|knowledge|power|magic|force|presence|essence)\b",
            # Magical transformation patterns
            r"\b(transform|change|shift|alter|convert)\s+(into|from|through|across|beyond)\b",
            # Enchanted atmosphere indicators
            r"\b(enchanted|bewitched|charmed|spellbound|mesmerized)\s+(place|moment|atmosphere|presence|feeling)\b",
            # Mystical energy flow patterns
            r"\b(energy|power|force|essence|spirit)\s+(flowing|streaming|pulsing|radiating|emanating)\b"
        ],
        "weight": 4,
        "mood": "mystical",
        "carpet": "ambience/atmosphere-sound-effect-239969",
        "psychoacoustic": {
            "frequency_range": "high_mid",     # 2-8kHz for mystical sparkle
            "spatial_width": "narrow",         # Focused, intimate
            "temporal_dynamics": "sustained",  # Continuous presence
            "emotional_curve": "contemplative",
            "volume_profile": "gentle",        # Subtle, not overwhelming
            "reverb_type": "mystical_cave"     # Enchanted space feeling
        }
    },
    
    # Romantic and Love Scenes
    "romantic_love": {
        "patterns": [
            # Primary romantic indicators with emotional depth
            r"\b(love|romance|passion|affection|devotion)\s+(blooming|growing|burning|intense|deep|profound|genuine)\b",
            # Secondary emotional states for nuanced audio
            r"\b(affection|desire|longing|yearning)\s+(shown|deep|warm|strong|intense|overwhelming|pure)\b",
            # Romantic atmosphere and setting
            r"\b(romantic|beloved|cherished|precious)\s+(moment|presence|evening|story|memory|experience)\b",
            # Physical and emotional connection
            r"\b(heart|soul|spirit|emotion)\s+(beating|racing|shared|sweet|tender|warm|connected)\b",
            # Intimate interaction patterns
            r"\b(touch|embrace|kiss|hold|clasp)\s+(gentle|tender|passionate|loving|affectionate)\b",
            # Emotional vulnerability and trust
            r"\b(trust|vulnerability|openness|honesty)\s+(shared|expressed|revealed|demonstrated)\b"
        ],
        "weight": 4,
        "mood": "romantic",
        "carpet": "ambience/cabin",
        "psychoacoustic": {
            "frequency_range": "mid",          # 800-2kHz for warmth
            "spatial_width": "intimate",       # Close, personal
            "temporal_dynamics": "gentle",     # Soft, flowing
            "emotional_curve": "warm_embrace",
            "volume_profile": "soft",          # Gentle, not intrusive
            "reverb_type": "intimate_room"     # Close, personal space
        }
    },
    
    # Dark and Evil Scenes
    "dark_evil": {
        "patterns": [
            # Primary dark presence indicators
            r"\b(dark|evil|corruption|malevolence|wickedness)\s+(presence|force|spreading|lurking|growing|manifesting)\b",
            # Secondary shadow and death elements
            r"\b(shadow|death|decay|destruction|annihilation)\s+(lurking|approaching|setting|visible|creeping|advancing)\b",
            # Corrupt and malicious intent
            r"\b(rotten|corrupt|malicious|vicious|cruel|brutal)\s+(atmosphere|power|intent|soul|nature|essence)\b",
            # Sinister and threatening patterns
            r"\b(sinister|dark|threatening|dangerous|hostile)\s+(plot|magic|influence|whisper|presence|intent)\b",
            # Fear and terror indicators
            r"\b(fear|terror|dread|horror|panic)\s+(growing|spreading|overwhelming|paralyzing|consuming)\b",
            # Evil manifestation patterns
            r"\b(evil|darkness|corruption)\s+(rises|emerges|unleashes|reveals|manifests)\b"
        ],
        "weight": 4,
        "mood": "dark",
        "carpet": "ambience/tense_drones",
        "psychoacoustic": {
            "frequency_range": "low",          # 60-200Hz for darkness
            "spatial_width": "surrounding",    # All around, immersive
            "temporal_dynamics": "ominous",    # Slow, threatening
            "emotional_curve": "descending_fear",
            "volume_profile": "creeping",      # Gradually building
            "reverb_type": "deep_cave"         # Dark, oppressive space
        }
    },
    
    # Storm and Weather Scenes
    "storm_weather": {
        "patterns": [
            # Primary storm indicators with intensity
            r"\b(storm|tempest|hurricane|cyclone|typhoon)\s+(approaching|raging|wild|fierce|violent|intense)\b",
            # Secondary thunder and lightning
            r"\b(thunder|lightning|thunderbolt|bolt)\s+(crashing|flashing|rolling|strike|explode|illuminate)\b",
            # Rain and wind patterns
            r"\b(rain|gale|downpour|deluge|torrent)\s+(pouring|falling|force|strong|heavy|relentless)\b",
            r"\b(wind|air|breeze|gust|blast)\s+(howling|blowing|whistling|rustling|roaring|screaming)\b",
            # Atmospheric pressure and tension
            r"\b(pressure|tension|electricity)\s+(building|mounting|intense|palpable|overwhelming)\b",
            # Weather transformation patterns
            r"\b(weather|atmosphere|sky)\s+(changing|transforming|darkening|clearing|settling)\b"
        ],
        "weight": 3,
        "mood": "tense",
        "carpet": "ambience/stormy_night",
        "psychoacoustic": {
            "frequency_range": "full_spectrum", # All frequencies for storm
            "spatial_width": "immersive",       # Full 3D sound field
            "temporal_dynamics": "chaotic",     # Unpredictable, dynamic
            "emotional_curve": "building_tension",
            "volume_profile": "dynamic",        # Variable, storm-like
            "reverb_type": "outdoor_storm"      # Natural storm environment
        }
    },
    
    # Mountain and Journey Scenes
    "mountain_journey": {
        "patterns": [
            # Primary mountain and elevation indicators
            r"\b(mountain|cliff|ridge|summit|peak|crest)\s+(peak|face|line|reached|view|climbed|conquered)\b",
            # Secondary alpine and high-altitude elements
            r"\b(alpine|high|elevated|towering|looming)\s+(meadow|air|elevation|altitude|forest|vista|panorama)\b",
            # Journey and travel patterns
            r"\b(long|traveling|endless|arduous|challenging)\s+(journey|far|distance|companion|quest|adventure)\b",
            # Path and destination indicators
            r"\b(road|path|trail|route|way)\s+(ahead|forward|destiny|less traveled|unknown|mysterious)\b",
            # Altitude and perspective changes
            r"\b(ascend|climb|rise|elevate|reach)\s+(higher|summit|peak|heights|altitude)\b",
            # Mountain atmosphere and conditions
            r"\b(thin|rarefied|crisp|clear|pure)\s+(air|atmosphere|light|view|perspective)\b"
        ],
        "weight": 3,
        "mood": "journey",
        "carpet": "ambience/windy_mountains",
        "psychoacoustic": {
            "frequency_range": "mid_high",     # 1-4kHz for clarity
            "spatial_width": "expansive",      # Wide, open feeling
            "temporal_dynamics": "steady",     # Consistent, reliable
            "emotional_curve": "progressive",
            "volume_profile": "moderate",      # Balanced, not overwhelming
            "reverb_type": "mountain_valley"   # Natural outdoor space
        }
    },
    
    # Peaceful and Calm Scenes
    "peaceful_calm": {
        "patterns": [
            # Primary peaceful indicators
            r"\b(peaceful|tranquil|serene|calm|placid)\s+(silence|atmosphere|setting|beauty|moment|presence)\b",
            # Secondary gentle and soft elements
            r"\b(gentle|soft|mild|subtle|delicate)\s+(breeze|whispers|touch|light|rain|sound|presence)\b",
            # Calm and comfortable states
            r"\b(calm|comfortable|relaxed|at ease|content)\s+(waters|warmth|mind|meditation|state|feeling)\b",
            # Cozy and warm atmosphere
            r"\b(cozy|warm|inviting|welcoming|comforting)\s+(atmosphere|room|home|embrace|feeling|presence)\b",
            # Natural peace indicators
            r"\b(nature|natural|organic)\s+(peace|tranquility|serenity|calm|harmony)\b",
            # Time-based peaceful moments
            r"\b(morning|dawn|sunrise|evening|dusk|twilight)\s+(peace|tranquility|serenity|calm)\b"
        ],
        "weight": 3,
        "mood": "peaceful",
        "carpet": "ambience/default_ambience",
        "psychoacoustic": {
            "frequency_range": "mid_low",     # 400-1kHz for warmth
            "spatial_width": "comfortable",   # Moderate, not overwhelming
            "temporal_dynamics": "gentle",    # Soft, flowing
            "emotional_curve": "stable_peace",
            "volume_profile": "gentle",       # Soft, background level
            "reverb_type": "comfortable_room" # Warm, inviting space
        }
    },
    
    # Victory and Triumph Scenes
    "victory_triumph": {
        "patterns": [
            # Primary victory indicators
            r"\b(victory|triumph|success|achievement|conquest)\s+(achieved|moment|return|march|dance|celebration)\b",
            # Secondary success and completion
            r"\b(successful|achievement|accomplishment|completion)\s+(completion|mission|earned|unlocked|realized|fulfilled)\b",
            # Joyous and hopeful emotions
            r"\b(joyous|hope|joy|happiness|elation)\s+(celebration|restored|renewed|reunion|moment|feeling)\b",
            # Light and salvation themes
            r"\b(light|salvation|redemption|liberation|freedom)\s+(breaking|shining|found|granted|achieved|realized)\b",
            # Heroic achievement patterns
            r"\b(hero|champion|victor|winner|conqueror)\s+(emerges|rises|proves|demonstrates|achieves)\b",
            # Triumphant return and celebration
            r"\b(return|homecoming|arrival|reunion)\s+(triumphant|victorious|successful|celebrated|honored)\b"
        ],
        "weight": 4,
        "mood": "triumphant",
        "carpet": "ambience/default_ambience",
        "psychoacoustic": {
            "frequency_range": "full_spectrum", # All frequencies for celebration
            "spatial_width": "expansive",       # Wide, celebratory
            "temporal_dynamics": "rising",      # Building to climax
            "emotional_curve": "ascending_joy",
            "volume_profile": "building",       # Gradually increasing
            "reverb_type": "celebration_hall"   # Large, celebratory space
        }
    },
    
    # Mystery and Intrigue Scenes
    "mystery_intrigue": {
        "patterns": [
            # Primary mystery indicators
            r"\b(mystery|enigmatic|puzzling|cryptic|obscure)\s+(deep|presence|unfolding|solved|revealed|hidden)\b",
            # Secondary puzzling situations
            r"\b(puzzling|curious|intriguing|fascinating|bewildering)\s+(situation|case|clues|behavior|occurrence|phenomenon)\b",
            # Strange and cryptic elements
            r"\b(strange|cryptic|mysterious|peculiar|odd)\s+(occurrence|message|symbols|atmosphere|behavior|pattern)\b",
            # Secret and hidden information
            r"\b(secret|hidden|concealed|buried|obscured)\s+(passage|meaning|truth|knowledge|information|purpose)\b",
            # Investigation and discovery patterns
            r"\b(investigate|discover|uncover|reveal|expose)\s+(truth|secret|mystery|clue|evidence)\b",
            # Suspense and tension building
            r"\b(suspense|tension|anticipation|expectation)\s+(building|mounting|growing|intense|overwhelming)\b"
        ],
        "weight": 3,
        "mood": "mysterious",
        "carpet": "ambience/atmosphere-sound-effect-239969",
        "psychoacoustic": {
            "frequency_range": "mid",          # 800-2kHz for intrigue
            "spatial_width": "focused",        # Concentrated, mysterious
            "temporal_dynamics": "suspenseful", # Building tension
            "emotional_curve": "building_curiosity",
            "volume_profile": "variable",      # Changing, mysterious
            "reverb_type": "mysterious_space"  # Unknown, hidden space
        }
    },
    
    # Danger and Peril Scenes
    "danger_peril": {
        "patterns": [
            # Primary danger indicators
            r"\b(danger|peril|risk|hazard|threat)\s+(lurking|ahead|close|zone|present|immediate)\b",
            # Secondary threatening situations
            r"\b(threat|hazardous|dangerous|risky|treacherous)\s+(growing|real|situation|terrain|condition|circumstance)\b",
            # Deadly and fatal consequences
            r"\b(deadly|fatal|lethal|mortal|terminal)\s+(force|mistake|weapon|intent|consequence|outcome)\b",
            # Treacherous and risky conditions
            r"\b(treacherous|risky|precarious|unstable|volatile)\s+(path|business|waters|move|situation|ground)\b",
            # Warning and caution indicators
            r"\b(warning|caution|alert|beware|careful)\s+(sign|signal|indication|message|feeling)\b",
            # Immediate threat patterns
            r"\b(immediate|instant|sudden|urgent|critical)\s+(danger|threat|risk|peril|hazard)\b"
        ],
        "weight": 4,
        "mood": "dangerous",
        "carpet": "ambience/tense_drones",
        "psychoacoustic": {
            "frequency_range": "low_mid",      # 200-800Hz for threat
            "spatial_width": "surrounding",    # All around, threatening
            "temporal_dynamics": "urgent",     # Fast, immediate
            "emotional_curve": "rising_fear",
            "volume_profile": "building",      # Increasing threat
            "reverb_type": "dangerous_space"   # Threatening environment
        }
    },
    
    # Desperation and Urgency Scenes
    "desperation_urgency": {
        "patterns": [
            # Primary desperation indicators
            r"\b(desperate|urgent|critical|emergency|pressing)\s+(situation|need|measure|plea|requirement|circumstance)\b",
            # Secondary critical moments
            r"\b(critical|emergency|vital|essential|crucial)\s+(moment|decision|response|time|situation|choice)\b",
            # Last chance scenarios
            r"\b(last|final|ultimate|desperate|hopeless)\s+(chance|attempt|opportunity|stand|effort|hope)\b",
            # Doomed and hopeless situations
            r"\b(doomed|hopeless|futile|vain|pointless)\s+(fate|cause|effort|struggle|attempt|situation)\b",
            # Time pressure indicators
            r"\b(time|moment|second|minute|hour)\s+(running|short|limited|precious|critical|urgent)\b",
            # Panic and chaos patterns
            r"\b(panic|chaos|disorder|confusion|desperation)\s+(ensues|breaks|spreads|grows|overwhelms)\b"
        ],
        "weight": 4,
        "mood": "desperate",
        "carpet": "ambience/tense_drones",
        "psychoacoustic": {
            "frequency_range": "mid_high",     # 1-4kHz for urgency
            "spatial_width": "closing",        # Getting closer, tighter
            "temporal_dynamics": "accelerating", # Getting faster
            "emotional_curve": "rising_panic",
            "volume_profile": "intense",       # High, urgent
            "reverb_type": "claustrophobic"    # Tight, oppressive space
        }
    },
    
    # Ceremony and Ritual Scenes
    "ceremony_ritual": {
        "patterns": [
            # Primary ceremony indicators
            r"\b(ceremony|ritual|ceremonial|formal|official)\s+(begins|performed|complete|grand|solemn|sacred)\b",
            # Secondary formal occasions
            r"\b(formal|official|ceremonial|ritualistic|traditional)\s+(occasion|ceremony|gathering|event|celebration|observance)\b",
            # Sacred and solemn moments
            r"\b(sacred|solemn|holy|divine|reverent)\s+(moment|ground|vow|atmosphere|presence|ceremony)\b",
            # Dignified and reverent atmosphere
            r"\b(dignified|reverent|respectful|honorable|noble)\s+(presence|ceremony|silence|prayer|atmosphere|conduct)\b",
            # Traditional and cultural patterns
            r"\b(traditional|cultural|ancestral|heritage|lineage)\s+(practice|custom|belief|ceremony|ritual)\b",
            # Spiritual and mystical elements
            r"\b(spiritual|mystical|divine|sacred|holy)\s+(connection|presence|energy|force|guidance)\b"
        ],
        "weight": 3,
        "mood": "ceremonial",
        "carpet": "ambience/default_ambience",
        "psychoacoustic": {
            "frequency_range": "mid",          # 800-2kHz for ceremony
            "spatial_width": "reverent",       # Respectful, focused
            "temporal_dynamics": "measured",   # Deliberate, respectful
            "emotional_curve": "stable_reverence",
            "volume_profile": "moderate",      # Balanced, respectful
            "reverb_type": "ceremonial_hall"   # Formal, sacred space
        }
    }
}

# Advanced psychoacoustic patterns for specialized scenes
ADVANCED_PSYCHOACOUSTIC_PATTERNS = {
    # Tension Building and Release
    "tension_building": {
        "patterns": [
            # Gradual tension indicators
            r"\b(gradually|slowly|steadily|increasingly|progressively)\s+(intense|tense|worried|anxious|concerned|nervous)\b",
            # Subtle warning signs
            r"\b(something|feeling|sense|intuition)\s+(wrong|off|strange|different|concerning|troubling)\b",
            # Time pressure building
            r"\b(time|moment|second|minute)\s+(running|short|limited|precious|critical|urgent|pressing)\b",
            # Atmospheric tension
            r"\b(atmosphere|air|mood|feeling)\s+(thickening|tightening|building|mounting|growing|intensifying)\b",
            # Subtle danger indicators
            r"\b(shadow|presence|feeling)\s+(lurking|creeping|approaching|gathering|converging)\b"
        ],
        "weight": 3,
        "mood": "building_tension",
        "carpet": "ambience/tense_drones",
        "psychoacoustic": {
            "frequency_range": "mid",          # 800-2kHz for tension
            "spatial_width": "narrowing",      # Closing in
            "temporal_dynamics": "accelerating", # Getting faster
            "emotional_curve": "rising_anxiety",
            "volume_profile": "creeping",      # Gradually building
            "reverb_type": "tightening_space"  # Closing environment
        }
    },
    
    # Emotional Vulnerability and Intimacy
    "emotional_vulnerability": {
        "patterns": [
            # Raw emotional states
            r"\b(raw|naked|exposed|vulnerable|fragile)\s+(emotion|feeling|truth|soul|heart|spirit)\b",
            # Intimate revelations
            r"\b(truth|secret|feeling|emotion)\s+(revealed|exposed|shared|confessed|admitted)\b",
            # Emotional breakthrough
            r"\b(breakthrough|realization|epiphany|revelation)\s+(emotional|personal|profound|life-changing)\b",
            # Trust and openness
            r"\b(trust|faith|hope|love)\s+(given|shared|offered|extended|demonstrated)\b",
            # Emotional healing
            r"\b(healing|recovery|renewal|restoration)\s+(emotional|spiritual|personal|inner)\b"
        ],
        "weight": 4,
        "mood": "vulnerable",
        "carpet": "ambience/cabin",
        "psychoacoustic": {
            "frequency_range": "mid_low",     # 400-1kHz for warmth
            "spatial_width": "intimate",      # Very close, personal
            "temporal_dynamics": "gentle",    # Soft, flowing
            "emotional_curve": "gentle_healing",
            "volume_profile": "whisper",      # Very soft, intimate
            "reverb_type": "intimate_space"   # Close, personal environment
        }
    },
    
    # Spatial and Environmental Awareness
    "spatial_context": {
        "open_outdoors": {
            "patterns": [
                r"\b(wide|open|vast|expansive|endless|boundless)\s+(plain|field|meadow|valley|horizon|landscape)\b",
                r"\b(sky|clouds|stars|sun|moon|heavens)\s+(above|overhead|visible|clear|bright|endless)\b",
                r"\b(horizon|distance|far|beyond|across)\s+(stretching|extending|reaching|spreading|expanding)\b"
            ],
            "spatial_audio": {
                "reverb": "large_outdoor",
                "delay": "long",
                "stereo_width": "maximum",
                "depth": "far_field",
                "frequency_response": "natural_outdoor"
            }
        },
        "confined_indoor": {
            "patterns": [
                r"\b(small|tight|confined|cramped|narrow|restricted)\s+(room|chamber|corridor|passage|space|area)\b",
                r"\b(walls|ceiling|floor|boundaries)\s+(close|near|surrounding|enclosing|confining|limiting)\b",
                r"\b(indoors|inside|enclosed|contained|trapped)\s+(space|area|environment|atmosphere|feeling)\b"
            ],
            "spatial_audio": {
                "reverb": "small_room",
                "delay": "short",
                "stereo_width": "narrow",
                "depth": "near_field",
                "frequency_response": "confined_space"
            }
        },
        "natural_landscape": {
            "patterns": [
                r"\b(forest|woods|jungle|grove|thicket)\s+(dense|thick|lush|verdant|wild|natural)\b",
                r"\b(mountain|hill|cliff|ridge|valley)\s+(natural|wild|untamed|pristine|beautiful)\b",
                r"\b(river|stream|lake|pond|water)\s+(flowing|running|moving|living|natural)\b"
            ],
            "spatial_audio": {
                "reverb": "natural_landscape",
                "delay": "medium",
                "stereo_width": "wide",
                "depth": "medium_field",
                "frequency_response": "natural_environment"
            }
        }
    },
    
    # Temporal Dynamics and Sound Evolution
    "temporal_patterns": {
        "sudden_events": {
            "patterns": [
                r"\b(suddenly|abruptly|instantly|immediately|without warning|all at once)\b",
                r"\b(flash|burst|explosion|crash|bang|boom)\s+(of|with|across|through|against)\b",
                r"\b(instant|momentary|fleeting|brief|transient)\s+(change|transformation|revelation|moment)\b"
            ],
            "audio_response": {
                "attack_time": "instant",      # 0-10ms
                "decay_time": "fast",          # 100-500ms
                "sustain_level": "high",       # 80-100%
                "release_time": "medium",      # 1-3s
                "frequency_response": "impact_focused"
            }
        },
        "gradual_changes": {
            "patterns": [
                r"\b(gradually|slowly|steadily|progressively|over time|bit by bit)\b",
                r"\b(build|grow|increase|develop|evolve|transform)\s+(up|into|toward|across|through)\b",
                r"\b(steady|consistent|continuous|ongoing|persistent)\s+(change|growth|development|evolution)\b"
            ],
            "audio_response": {
                "attack_time": "slow",         # 500ms-2s
                "decay_time": "long",          # 2-10s
                "sustain_level": "variable",   # 20-80%
                "release_time": "long",        # 5-15s
                "frequency_response": "evolving_spectrum"
            }
        },
        "rhythmic_patterns": {
            "patterns": [
                r"\b(rhythm|beat|pulse|cadence|tempo)\s+(steady|consistent|regular|reliable|predictable)\b",
                r"\b(heartbeat|pulse|throb|thump|drum)\s+(steady|regular|consistent|reliable|strong)\b",
                r"\b(march|walk|step|stride|pace)\s+(steady|regular|consistent|measured|deliberate)\b"
            ],
            "audio_response": {
                "attack_time": "punchy",       # 50-200ms
                "decay_time": "rhythmic",      # 200ms-1s
                "sustain_level": "consistent", # 60-80%
                "release_time": "short",       # 200-500ms
                "frequency_response": "rhythmic_focus"
            }
        }
    }
}

# Enhanced context-based decision rules with psychoacoustic awareness
CONTEXT_RULES = {
    "geographic_override": {
        "mountains": {
            "patterns": [r"\b(mountain|peak|cliff|ridge|summit|alpine|highland|elevation)\b"],
            "override_mood": "journey",
            "override_sound": "ambience/windy_mountains",
            "weight": 2,
            "psychoacoustic": {
                "frequency_range": "mid_high",     # 1-4kHz for clarity
                "spatial_width": "expansive",      # Wide, open feeling
                "reverb_type": "mountain_valley"   # Natural outdoor space
            }
        },
        "water": {
            "patterns": [r"\b(river|stream|lake|water|flowing|crossing|ocean|sea|pond)\b"],
            "override_mood": "peaceful",
            "override_sound": "ambience/cabin_rain",
            "weight": 2,
            "psychoacoustic": {
                "frequency_range": "high",         # 4-8kHz for water clarity
                "spatial_width": "flowing",        # Dynamic, moving
                "reverb_type": "water_environment" # Natural water space
            }
        },
        "indoors": {
            "patterns": [r"\b(inside|room|house|building|chamber|hall|interior|enclosed)\b"],
            "override_mood": "peaceful",
            "override_sound": "ambience/cabin",
            "weight": 1,
            "psychoacoustic": {
                "frequency_range": "mid",          # 800-2kHz for warmth
                "spatial_width": "contained",      # Limited, focused
                "reverb_type": "indoor_space"      # Enclosed environment
            }
        },
        "night": {
            "patterns": [r"\b(night|dark|evening|dusk|stars|moon|midnight|nighttime)\b"],
            "override_mood": "mysterious",
            "override_sound": "ambience/stormy_night",
            "weight": 2,
            "psychoacoustic": {
                "frequency_range": "low_mid",      # 200-800Hz for mystery
                "spatial_width": "enveloping",     # Surrounding, immersive
                "reverb_type": "night_environment" # Dark, mysterious space
            }
        },
        "forest": {
            "patterns": [r"\b(forest|woods|jungle|grove|thicket|trees|woodland)\b"],
            "override_mood": "mysterious",
            "override_sound": "ambience/atmosphere-sound-effect-239969",
            "weight": 2,
            "psychoacoustic": {
                "frequency_range": "mid_high",     # 1-4kHz for natural clarity
                "spatial_width": "organic",        # Natural, irregular
                "reverb_type": "forest_environment" # Natural woodland space
            }
        }
    },
    "intensity_modifiers": {
        "high_intensity": {
            "patterns": [r"\b(intense|overwhelming|powerful|strong|deep|profound|extreme|maximum)\b"],
            "boost_mood": "epic",
            "boost_confidence": 0.3,
            "psychoacoustic": {
                "volume_boost": 0.4,
                "frequency_boost": "high",
                "spatial_expansion": "wide",
                "temporal_acceleration": "fast"
            }
        },
        "low_intensity": {
            "patterns": [r"\b(gentle|soft|mild|subtle|quiet|calm|delicate|tender)\b"],
            "boost_mood": "peaceful",
            "boost_confidence": 0.2,
            "psychoacoustic": {
                "volume_reduction": 0.3,
                "frequency_focus": "mid",
                "spatial_contraction": "narrow",
                "temporal_slowing": "gentle"
            }
        },
        "building_intensity": {
            "patterns": [r"\b(building|growing|increasing|mounting|escalating|intensifying)\b"],
            "boost_mood": "tense",
            "boost_confidence": 0.25,
            "psychoacoustic": {
                "volume_gradient": "rising",
                "frequency_expansion": "gradual",
                "spatial_growth": "expanding",
                "temporal_acceleration": "progressive"
            }
        }
    },
    "emotional_context": {
        "character_emotion": {
            "joy": {
                "patterns": [r"\b(joy|happiness|elation|delight|pleasure|contentment)\b"],
                "psychoacoustic": {
                    "frequency_range": "bright",      # 2-6kHz for joy
                    "spatial_width": "expansive",     # Open, happy feeling
                    "temporal_dynamics": "lively",    # Energetic, upbeat
                    "volume_profile": "cheerful"      # Bright, positive
                }
            },
            "sadness": {
                "patterns": [r"\b(sadness|sorrow|grief|melancholy|despair|loneliness)\b"],
                "psychoacoustic": {
                    "frequency_range": "dark",        # 100-400Hz for sadness
                    "spatial_width": "contracted",    # Closed, inward
                    "temporal_dynamics": "slow",      # Dragging, heavy
                    "volume_profile": "subdued"       # Quiet, introspective
                }
            },
            "anger": {
                "patterns": [r"\b(anger|rage|fury|wrath|irritation|frustration)\b"],
                "psychoacoustic": {
                    "frequency_range": "aggressive",  # 800-3kHz for anger
                    "spatial_width": "confrontational", # Direct, focused
                    "temporal_dynamics": "explosive", # Sudden, intense
                    "volume_profile": "forceful"      # Strong, aggressive
                }
            },
            "fear": {
                "patterns": [r"\b(fear|terror|dread|horror|panic|anxiety|worry)\b"],
                "psychoacoustic": {
                    "frequency_range": "unsettling",  # 1-5kHz for fear
                    "spatial_width": "surrounding",   # All around, threatening
                    "temporal_dynamics": "erratic",   # Unpredictable, chaotic
                    "volume_profile": "creeping"      # Gradually building
                }
            }
        }
    }
}

# Legacy simple scene mappings (kept for backward compatibility)
SIMPLE_SCENE_MAPPINGS = {
    "eating": {
        "keywords": ["dinner", "supper", "eating", "meal", "restaurant", "food", "dining", "feast"],
        "carpet": "ambience/atmosphere-sound-effect-239969.mp3"
    },
    "hotel": {
        "keywords": ["hotel", "lobby", "room service", "inn", "accommodation", "reception"],
        "carpet": "ambience/atmosphere-sound-effect-239969.mp3"
    },
    "library": {
        "keywords": ["museum", "library", "books", "research", "study", "academic", "scholarly"],
        "carpet": "ambience/default_ambience.mp3"
    },
    "travel": {
        "keywords": ["carriage", "train", "journey", "trip", "traveling", "voyage", "expedition"],
        "carpet": "ambience/footsteps-approaching-316715.mp3"
    },
    "storm": {
        "keywords": ["storm", "thunder", "lightning", "rain", "downpour", "tempest", "gale"],
        "carpet": "ambience/stormy_night.mp3"
    },
    "forest": {
        "keywords": ["forest", "trees", "woods", "grove", "thicket", "wilderness"],
        "carpet": "ambience/windy_mountains.mp3"
    },
    "castle": {
        "keywords": ["castle", "keep", "tower", "gates", "fortress", "palace", "citadel"],
        "carpet": "ambience/tense_drones.mp3"
    },
    "mountains": {
        "keywords": ["mountains", "cliff", "peak", "valley", "summit", "ridge", "alpine"],
        "carpet": "ambience/windy_mountains.mp3"
    },
    "fear": {
        "keywords": ["superstition", "afraid", "creepy", "haunted", "dark", "disaster", "evil", "terrifying"],
        "carpet": "ambience/tense_drones.mp3"
    },
    "indoors": {
        "keywords": ["cabin", "indoors", "inside", "house", "room", "building", "apartment", "home", "wall", "walls", "roof"],
        "carpet": "ambience/cabin.mp3"
    }
}

# Psychoacoustic helper functions for advanced audio processing
def check_frequency_conflict(sound1_metadata: Dict, sound2_metadata: Dict) -> Dict:
    """
    Check for frequency conflicts between two sounds to prevent masking.
    
    Args:
        sound1_metadata: Psychoacoustic metadata for first sound
        sound2_metadata: Psychoacoustic metadata for second sound
        
    Returns:
        Dictionary with conflict analysis and recommendations
    """
    # Frequency range mapping
    frequency_ranges = {
        "low": (60, 200),
        "low_mid": (200, 800),
        "mid": (800, 2000),
        "mid_high": (2000, 4000),
        "high": (4000, 8000),
        "high_mid": (2000, 8000),
        "full_spectrum": (60, 8000),
        "bright": (2000, 6000),
        "dark": (100, 400),
        "aggressive": (800, 3000),
        "unsettling": (1000, 5000),
        "natural_outdoor": (200, 4000),
        "confined_space": (400, 2000),
        "natural_environment": (200, 3000),
        "impact_focused": (100, 2000),
        "evolving_spectrum": (200, 6000),
        "rhythmic_focus": (400, 1500)
    }
    
    def get_freq_range(metadata):
        freq_key = metadata.get("frequency_range", "mid")
        return frequency_ranges.get(freq_key, (800, 2000))
    
    freq1_start, freq1_end = get_freq_range(sound1_metadata)
    freq2_start, freq2_end = get_freq_range(sound2_metadata)
    
    # Check for overlap
    overlap_start = max(freq1_start, freq2_start)
    overlap_end = min(freq1_end, freq2_end)
    overlap = max(0, overlap_end - overlap_start)
    
    # Calculate conflict severity
    total_range1 = freq1_end - freq1_start
    total_range2 = freq2_end - freq2_start
    overlap_percentage = overlap / min(total_range1, total_range2) if min(total_range1, total_range2) > 0 else 0
    
    # Conflict analysis
    if overlap_percentage > 0.7:
        severity = "high"
        recommendation = "avoid_combination"
    elif overlap_percentage > 0.4:
        severity = "medium"
        recommendation = "reduce_volume"
    elif overlap_percentage > 0.2:
        severity = "low"
        recommendation = "monitor_balance"
    else:
        severity = "none"
        recommendation = "safe_combination"
    
    return {
        "conflict_detected": severity != "none",
        "severity": severity,
        "overlap_percentage": overlap_percentage,
        "overlap_range": (overlap_start, overlap_end),
        "recommendation": recommendation,
        "frequency1": (freq1_start, freq1_end),
        "frequency2": (freq2_start, freq2_end)
    }

def calculate_spatial_position(scene_context: List[str], psychoacoustic_data: Dict) -> Dict:
    """
    Calculate optimal spatial audio positioning based on scene context.
    
    Args:
        scene_context: List of detected scene types
        psychoacoustic_data: Psychoacoustic metadata from scene detection
        
    Returns:
        Dictionary with spatial audio parameters
    """
    # Default spatial settings
    spatial_config = {
        "width": "moderate",
        "depth": "medium_field",
        "height": "neutral",
        "reverb_type": "default",
        "delay": "medium",
        "stereo_width": "normal"
    }
    
    # Spatial width mapping
    width_mapping = {
        "wide": "maximum",
        "expansive": "wide",
        "narrowing": "narrowing",
        "intimate": "narrow",
        "surrounding": "full_surround",
        "closing": "contracting",
        "comfortable": "moderate",
        "reverent": "focused",
        "immersive": "full_3d",
        "organic": "natural_irregular"
    }
    
    # Depth mapping
    depth_mapping = {
        "far_field": "far",
        "near_field": "near",
        "medium_field": "medium",
        "full_3d": "immersive"
    }
    
    # Reverb type mapping
    reverb_mapping = {
        "large_outdoor": "large_outdoor",
        "mystical_cave": "mystical_cave",
        "intimate_room": "intimate_room",
        "deep_cave": "deep_cave",
        "outdoor_storm": "outdoor_storm",
        "mountain_valley": "mountain_valley",
        "comfortable_room": "comfortable_room",
        "celebration_hall": "celebration_hall",
        "mysterious_space": "mysterious_space",
        "dangerous_space": "dangerous_space",
        "claustrophobic": "claustrophobic",
        "ceremonial_hall": "ceremonial_hall",
        "water_environment": "water_environment",
        "indoor_space": "indoor_space",
        "night_environment": "night_environment",
        "forest_environment": "forest_environment"
    }
    
    # Apply psychoacoustic spatial settings
    if psychoacoustic_data:
        spatial_width = psychoacoustic_data.get("spatial_width", "moderate")
        reverb_type = psychoacoustic_data.get("reverb_type", "default")
        
        if spatial_width in width_mapping:
            spatial_config["width"] = width_mapping[spatial_width]
            spatial_config["stereo_width"] = width_mapping[spatial_width]
        
        if reverb_type in reverb_mapping:
            spatial_config["reverb_type"] = reverb_mapping[reverb_type]
    
    # Context-based overrides
    for scene in scene_context:
        if "open_outdoors" in scene or "mountain" in scene:
            spatial_config.update({
                "width": "maximum",
                "depth": "far_field",
                "stereo_width": "full"
            })
        elif "confined" in scene or "indoor" in scene:
            spatial_config.update({
                "width": "narrow",
                "depth": "near_field",
                "stereo_width": "narrow"
            })
        elif "forest" in scene or "natural" in scene:
            spatial_config.update({
                "width": "wide",
                "depth": "medium_field",
                "stereo_width": "natural"
            })
    
    return spatial_config

def map_emotion_to_audio(emotion: str, intensity: float, psychoacoustic_data: Dict = None) -> Dict:
    """
    Map emotional intensity to audio parameters for dynamic soundscapes.
    
    Args:
        emotion: Detected emotional state
        intensity: Emotional intensity (0.0 to 1.0)
        psychoacoustic_data: Additional psychoacoustic metadata
        
    Returns:
        Dictionary with audio parameter recommendations
    """
    # Base audio parameters
    audio_params = {
        "volume": max(0.2, min(1.0, intensity * 0.8 + 0.2)),  # 20-100%
        "reverb": "medium",
        "stereo_width": "normal",
        "frequency_boost": "none",
        "temporal_dynamics": "normal"
    }
    
    # Emotion-specific mappings
    emotion_mappings = {
        "epic": {
            "volume": min(1.0, intensity * 0.9 + 0.3),  # 30-120%
            "reverb": "large",
            "stereo_width": "wide",
            "frequency_boost": "full_spectrum",
            "temporal_dynamics": "dynamic"
        },
        "mystical": {
            "volume": max(0.3, intensity * 0.6 + 0.3),  # 30-90%
            "reverb": "mystical",
            "stereo_width": "focused",
            "frequency_boost": "high_mid",
            "temporal_dynamics": "sustained"
        },
        "romantic": {
            "volume": max(0.4, intensity * 0.5 + 0.4),  # 40-90%
            "reverb": "intimate",
            "stereo_width": "narrow",
            "frequency_boost": "mid",
            "temporal_dynamics": "gentle"
        },
        "dark": {
            "volume": max(0.3, intensity * 0.7 + 0.3),  # 30-100%
            "reverb": "deep",
            "stereo_width": "surrounding",
            "frequency_boost": "low",
            "temporal_dynamics": "ominous"
        },
        "tense": {
            "volume": max(0.5, intensity * 0.8 + 0.5),  # 50-130%
            "reverb": "tight",
            "stereo_width": "narrowing",
            "frequency_boost": "mid_high",
            "temporal_dynamics": "accelerating"
        },
        "peaceful": {
            "volume": max(0.2, intensity * 0.4 + 0.2),  # 20-60%
            "reverb": "comfortable",
            "stereo_width": "moderate",
            "frequency_boost": "mid_low",
            "temporal_dynamics": "gentle"
        },
        "triumphant": {
            "volume": max(0.6, intensity * 0.9 + 0.6),  # 60-150%
            "reverb": "celebration",
            "stereo_width": "expansive",
            "frequency_boost": "full_spectrum",
            "temporal_dynamics": "rising"
        },
        "mysterious": {
            "volume": max(0.3, intensity * 0.6 + 0.3),  # 30-90%
            "reverb": "mysterious",
            "stereo_width": "focused",
            "frequency_boost": "mid",
            "temporal_dynamics": "suspenseful"
        },
        "dangerous": {
            "volume": max(0.4, intensity * 0.8 + 0.4),  # 40-120%
            "reverb": "threatening",
            "stereo_width": "surrounding",
            "frequency_boost": "low_mid",
            "temporal_dynamics": "urgent"
        },
        "desperate": {
            "volume": max(0.6, intensity * 0.9 + 0.6),  # 60-150%
            "reverb": "claustrophobic",
            "stereo_width": "closing",
            "frequency_boost": "mid_high",
            "temporal_dynamics": "accelerating"
        },
        "ceremonial": {
            "volume": max(0.4, intensity * 0.6 + 0.4),  # 40-100%
            "reverb": "formal",
            "stereo_width": "reverent",
            "frequency_boost": "mid",
            "temporal_dynamics": "measured"
        }
    }
    
    # Apply emotion-specific mapping
    if emotion in emotion_mappings:
        emotion_params = emotion_mappings[emotion]
        for key, value in emotion_params.items():
            if key == "volume":
                audio_params[key] = value
            else:
                audio_params[key] = value
    
    # Apply psychoacoustic overrides if available
    if psychoacoustic_data:
        if "volume_profile" in psychoacoustic_data:
            profile = psychoacoustic_data["volume_profile"]
            if profile == "dynamic":
                audio_params["volume"] *= (0.8 + intensity * 0.4)  # Dynamic variation
            elif profile == "creeping":
                audio_params["volume"] *= (0.6 + intensity * 0.6)  # Gradual build
            elif profile == "building":
                audio_params["volume"] *= (0.7 + intensity * 0.5)  # Progressive increase
        
        if "temporal_dynamics" in psychoacoustic_data:
            audio_params["temporal_dynamics"] = psychoacoustic_data["temporal_dynamics"]
    
    # Ensure volume stays within safe bounds
    audio_params["volume"] = max(0.1, min(1.5, audio_params["volume"]))
    
    return audio_params

def optimize_soundscape_frequency_balance(detected_scenes: List[Dict]) -> Dict:
    """
    Optimize frequency balance across multiple detected scenes to prevent masking.
    
    Args:
        detected_scenes: List of detected scenes with psychoacoustic metadata
        
    Returns:
        Dictionary with frequency optimization recommendations
    """
    if not detected_scenes:
        return {"optimization": "none_needed", "recommendations": []}
    
    # Analyze frequency distribution
    frequency_analysis = {
        "low": 0,
        "low_mid": 0,
        "mid": 0,
        "mid_high": 0,
        "high": 0,
        "full_spectrum": 0
    }
    
    scene_frequencies = []
    
    for scene in detected_scenes:
        if "psychoacoustic" in scene and "frequency_range" in scene["psychoacoustic"]:
            freq_range = scene["psychoacoustic"]["frequency_range"]
            frequency_analysis[freq_range] = frequency_analysis.get(freq_range, 0) + 1
            scene_frequencies.append({
                "scene": scene.get("type", "unknown"),
                "frequency": freq_range,
                "weight": scene.get("weight", 1)
            })
    
    # Identify potential conflicts
    conflicts = []
    recommendations = []
    
    # Check for frequency crowding
    for freq_range, count in frequency_analysis.items():
        if count > 2 and freq_range != "full_spectrum":
            conflicts.append(f"Frequency crowding in {freq_range} range ({count} scenes)")
            recommendations.append(f"Consider reducing {freq_range} frequency scenes or adjust volumes")
    
    # Check for missing frequency ranges
    missing_ranges = [freq for freq, count in frequency_analysis.items() if count == 0]
    if missing_ranges:
        recommendations.append(f"Consider adding scenes with {', '.join(missing_ranges)} frequencies for balance")
    
    # Full spectrum dominance check
    if frequency_analysis["full_spectrum"] > 1:
        conflicts.append("Multiple full-spectrum scenes may cause frequency masking")
        recommendations.append("Limit full-spectrum scenes or adjust individual frequency components")
    
    # Generate optimization strategy
    if conflicts:
        optimization = "frequency_conflicts_detected"
    elif len([f for f in frequency_analysis.values() if f > 0]) < 3:
        optimization = "frequency_imbalance"
    else:
        optimization = "well_balanced"
    
    return {
        "optimization": optimization,
        "frequency_distribution": frequency_analysis,
        "conflicts": conflicts,
        "recommendations": recommendations,
        "scene_frequencies": scene_frequencies
    }

def enhanced_scene_detection(text: str) -> Tuple[List[str], Dict[str, int], Dict[str, List[int]], Dict[str, any]]:
    """
    Enhanced scene detection with psychoacoustic analysis and advanced pattern recognition.
    
    Args:
        text: Text content to analyze
        
    Returns:
        Tuple of (detected_scenes, scene_counts, scene_positions, mood_analysis)
    """
    if not text:
        return [], {}, {}, {}
    
    detected_scenes = []
    scene_counts = {}
    scene_positions = {}
    mood_analysis = {
        "primary_mood": "neutral",
        "secondary_moods": [],
        "emotional_intensity": 0.0,
        "psychoacoustic_profile": {},
        "frequency_balance": {},
        "spatial_recommendations": {},
        "temporal_dynamics": {},
        "scene_complexity": 0
    }
    
    # Combine all pattern sources for comprehensive detection
    all_patterns = {}
    
    # Add enhanced scene patterns
    for scene_type, scene_data in ENHANCED_SCENE_SOUND_MAPPINGS.items():
        all_patterns[scene_type] = {
            "patterns": scene_data["patterns"],
            "weight": scene_data["weight"],
            "mood": scene_data["mood"],
            "psychoacoustic": scene_data.get("psychoacoustic", {}),
            "source": "enhanced_scenes"
        }
    
    # Add advanced psychoacoustic patterns
    for pattern_type, pattern_data in ADVANCED_PSYCHOACOUSTIC_PATTERNS.items():
        if isinstance(pattern_data, dict) and "patterns" in pattern_data:
            all_patterns[f"advanced_{pattern_type}"] = {
                "patterns": pattern_data["patterns"],
                "weight": pattern_data.get("weight", 2),
                "mood": pattern_data.get("mood", "neutral"),
                "psychoacoustic": pattern_data.get("psychoacoustic", {}),
                "source": "advanced_patterns"
            }
    
    # Add spatial context patterns
    for spatial_type, spatial_data in ADVANCED_PSYCHOACOUSTIC_PATTERNS.get("spatial_context", {}).items():
        if isinstance(spatial_data, dict) and "patterns" in spatial_data:
            all_patterns[f"spatial_{spatial_type}"] = {
                "patterns": spatial_data["patterns"],
                "weight": 2,
                "mood": "environmental",
                "psychoacoustic": spatial_data.get("spatial_audio", {}),
                "source": "spatial_context"
            }
    
    # Add temporal pattern analysis
    for temporal_type, temporal_data in ADVANCED_PSYCHOACOUSTIC_PATTERNS.get("temporal_patterns", {}).items():
        if isinstance(temporal_data, dict) and "patterns" in temporal_data:
            all_patterns[f"temporal_{temporal_type}"] = {
                "patterns": temporal_data["patterns"],
                "weight": 1,
                "mood": "dynamic",
                "psychoacoustic": temporal_data.get("audio_response", {}),
                "source": "temporal_patterns"
            }
    
    # Scene detection with enhanced analysis
    for scene_type, scene_data in all_patterns.items():
        patterns = scene_data["patterns"]
        weight = scene_data["weight"]
        mood = scene_data["mood"]
        psychoacoustic = scene_data["psychoacoustic"]
        source = scene_data["source"]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                start_pos = match.start()
                end_pos = match.end()
                matched_text = match.group()
                
                # Add to detected scenes
                detected_scenes.append({
                    "type": scene_type,
                    "text": matched_text,
                    "position": start_pos,
                    "weight": weight,
                    "mood": mood,
                    "psychoacoustic": psychoacoustic,
                    "source": source,
                    "confidence": 0.8 + (weight * 0.1)  # Base confidence + weight bonus
                })
                
                # Update counts
                scene_counts[scene_type] = scene_counts.get(scene_type, 0) + 1
                
                # Update positions
                if scene_type not in scene_positions:
                    scene_positions[scene_type] = []
                scene_positions[scene_type].append(start_pos)
    
    # Apply context rules for overrides and enhancements
    context_enhanced_scenes = apply_context_rules(detected_scenes, text)
    
    # Analyze emotional progression and mood complexity
    emotion_analyzer = AdvancedEmotionAnalyzer()
    emotional_progression = emotion_analyzer.analyze_emotional_progression(text)
    
    # Convert dataclass to dictionary for further processing
    mood_analysis = {
        "emotional_progression": {
            "segments": emotional_progression.segments,
            "progression_patterns": emotional_progression.progression_patterns,
            "arc_metrics": emotional_progression.arc_metrics,
            "overall_trend": emotional_progression.overall_trend
        }
    }
    
    # Generate psychoacoustic profile
    psychoacoustic_profile = generate_psychoacoustic_profile(detected_scenes)
    mood_analysis["psychoacoustic_profile"] = psychoacoustic_profile
    
    # Analyze frequency balance
    frequency_balance = optimize_soundscape_frequency_balance(detected_scenes)
    mood_analysis["frequency_balance"] = frequency_balance
    
    # Generate spatial recommendations
    spatial_recommendations = calculate_spatial_position(
        [scene["type"] for scene in detected_scenes],
        psychoacoustic_profile
    )
    mood_analysis["spatial_recommendations"] = spatial_recommendations
    
    # Analyze temporal dynamics
    temporal_dynamics = analyze_temporal_dynamics(detected_scenes, text)
    mood_analysis["temporal_dynamics"] = temporal_dynamics
    
    # Calculate scene complexity
    mood_analysis["scene_complexity"] = len(detected_scenes) + len(set(scene["mood"] for scene in detected_scenes))
    
    return detected_scenes, scene_counts, scene_positions, mood_analysis

def apply_context_rules(detected_scenes: List[Dict], text: str) -> List[Dict]:
    """
    Apply context rules to enhance scene detection with geographic and emotional overrides.
    
    Args:
        detected_scenes: List of detected scenes
        text: Original text content
        
    Returns:
        Enhanced list of scenes with context rules applied
    """
    enhanced_scenes = detected_scenes.copy()
    
    # Apply geographic overrides
    for geo_type, geo_data in CONTEXT_RULES["geographic_override"].items():
        patterns = geo_data["patterns"]
        override_mood = geo_data["override_mood"]
        override_sound = geo_data["override_sound"]
        weight = geo_data["weight"]
        psychoacoustic = geo_data.get("psychoacoustic", {})
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Check if this geographic context is already detected
                existing_geo = any(
                    scene["type"] == f"spatial_{geo_type}" 
                    for scene in enhanced_scenes
                )
                
                if not existing_geo:
                    enhanced_scenes.append({
                        "type": f"spatial_{geo_type}",
                        "text": match.group(),
                        "position": match.start(),
                        "weight": weight,
                        "mood": override_mood,
                        "psychoacoustic": psychoacoustic,
                        "source": "geographic_override",
                        "confidence": 0.9,
                        "override_sound": override_sound
                    })
    
    # Apply intensity modifiers
    for intensity_type, intensity_data in CONTEXT_RULES["intensity_modifiers"].items():
        patterns = intensity_data["patterns"]
        boost_mood = intensity_data["boost_mood"]
        boost_confidence = intensity_data["boost_confidence"]
        psychoacoustic = intensity_data.get("psychoacoustic", {})
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Find existing scenes to boost
                for scene in enhanced_scenes:
                    if scene["mood"] == boost_mood:
                        scene["confidence"] = min(1.0, scene["confidence"] + boost_confidence)
                        if psychoacoustic:
                            scene["psychoacoustic"].update(psychoacoustic)
    
    # Apply emotional context
    for emotion_type, emotion_data in CONTEXT_RULES["emotional_context"]["character_emotion"].items():
        patterns = emotion_data["patterns"]
        psychoacoustic = emotion_data["psychoacoustic"]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                enhanced_scenes.append({
                    "type": f"emotion_{emotion_type}",
                    "text": match.group(),
                    "position": match.start(),
                    "weight": 3,
                    "mood": emotion_type,
                    "psychoacoustic": psychoacoustic,
                    "source": "emotional_context",
                    "confidence": 0.85
                })
    
    return enhanced_scenes

def generate_psychoacoustic_profile(detected_scenes: List[Dict]) -> Dict:
    """
    Generate comprehensive psychoacoustic profile from detected scenes.
    
    Args:
        detected_scenes: List of detected scenes with psychoacoustic metadata
        
    Returns:
        Comprehensive psychoacoustic profile
    """
    if not detected_scenes:
        return {"profile": "neutral", "recommendations": []}
    
    # Collect all psychoacoustic data
    frequency_ranges = []
    spatial_widths = []
    temporal_dynamics = []
    emotional_curves = []
    volume_profiles = []
    reverb_types = []
    
    for scene in detected_scenes:
        if "psychoacoustic" in scene:
            psycho = scene["psychoacoustic"]
            
            if "frequency_range" in psycho:
                frequency_ranges.append(psycho["frequency_range"])
            if "spatial_width" in psycho:
                spatial_widths.append(psycho["spatial_width"])
            if "temporal_dynamics" in psycho:
                temporal_dynamics.append(psycho["temporal_dynamics"])
            if "emotional_curve" in psycho:
                emotional_curves.append(psycho["emotional_curve"])
            if "volume_profile" in psycho:
                volume_profiles.append(psycho["volume_profile"])
            if "reverb_type" in psycho:
                reverb_types.append(psycho["reverb_type"])
    
    # Analyze dominant characteristics
    def get_dominant(characteristics):
        if not characteristics:
            return "neutral"
        return max(set(characteristics), key=characteristics.count)
    
    profile = {
        "dominant_frequency": get_dominant(frequency_ranges),
        "dominant_spatial": get_dominant(spatial_widths),
        "dominant_temporal": get_dominant(temporal_dynamics),
        "dominant_emotional": get_dominant(emotional_curves),
        "dominant_volume": get_dominant(volume_profiles),
        "dominant_reverb": get_dominant(reverb_types),
        "complexity": len(set(frequency_ranges + spatial_widths + temporal_dynamics))
    }
    
    # Generate recommendations
    recommendations = []
    
    # Frequency balance recommendations
    if len(set(frequency_ranges)) < 3:
        recommendations.append("Consider adding frequency diversity for better audio balance")
    
    # Spatial variety recommendations
    if len(set(spatial_widths)) < 2:
        recommendations.append("Add spatial variety for more immersive experience")
    
    # Temporal dynamics recommendations
    if len(set(temporal_dynamics)) < 2:
        recommendations.append("Include temporal variety for dynamic soundscapes")
    
    profile["recommendations"] = recommendations
    
    return profile

def analyze_temporal_dynamics(detected_scenes: List[Dict], text: str) -> Dict:
    """
    Analyze temporal dynamics and sound evolution patterns.
    
    Args:
        detected_scenes: List of detected scenes
        text: Original text content
        
    Returns:
        Temporal dynamics analysis
    """
    temporal_analysis = {
        "overall_pacing": "steady",
        "dynamic_changes": [],
        "rhythmic_elements": [],
        "temporal_recommendations": []
    }
    
    # Count temporal pattern types
    temporal_counts = {}
    for scene in detected_scenes:
        if "temporal_" in scene["type"]:
            temp_type = scene["type"].replace("temporal_", "")
            temporal_counts[temp_type] = temporal_counts.get(temp_type, 0) + 1
    
    # Analyze overall pacing
    if temporal_counts.get("sudden_events", 0) > 2:
        temporal_analysis["overall_pacing"] = "dynamic"
    elif temporal_counts.get("gradual_changes", 0) > 2:
        temporal_analysis["overall_pacing"] = "evolving"
    elif temporal_counts.get("rhythmic_patterns", 0) > 2:
        temporal_analysis["overall_pacing"] = "rhythmic"
    
    # Identify dynamic changes
    for scene in detected_scenes:
        if "temporal_" in scene["type"]:
            temporal_analysis["dynamic_changes"].append({
                "type": scene["type"],
                "position": scene["position"],
                "text": scene["text"],
                "dynamics": scene.get("psychoacoustic", {})
            })
    
    # Generate temporal recommendations
    if temporal_counts.get("sudden_events", 0) > 3:
        temporal_analysis["temporal_recommendations"].append(
            "High number of sudden events - consider spacing for better impact"
        )
    
    if temporal_counts.get("gradual_changes", 0) == 0:
        temporal_analysis["temporal_recommendations"].append(
            "No gradual changes detected - consider adding for smoother transitions"
        )
    
    return temporal_analysis

def detect_triggered_sounds(text: str) -> List[Dict]:
    """
    Detect specific words that should trigger sound effects.
    """
    # Use the emotion analysis for trigger word detection
    return find_trigger_words(text)

def get_contextual_summary(text: str) -> str:
    """Generate a contextual summary of the text for debugging."""
    if not text:
        return "Empty text"
    
    # Get enhanced scene detection
    sorted_scenes, scene_counts, scene_positions, mood_analysis = enhanced_scene_detection(text)
    
    summary_parts = []
    
    if sorted_scenes:
        scene_info = [f"{scene}({scene_counts[scene]})" for scene in sorted_scenes[:3]]
        summary_parts.append(f"Scenes: {', '.join(scene_info)}")
    
    # Add trigger word info
    trigger_words = detect_triggered_sounds(text)
    if trigger_words:
        trigger_words_list = [tw["word"] for tw in trigger_words]
        summary_parts.append(f"Triggers: {', '.join(trigger_words_list)}")
    
    return "; ".join(summary_parts) if summary_parts else "No scenes or triggers detected"

def get_ambient_soundscape(book_id: int, chapter_number: int, page_number: int, db: Session) -> Dict:
    """
    Returns a structured soundscape dict for a specific book page.
    Uses enhanced scene detection with sophisticated regex patterns and context rules.
    """
    from app.models.book import Book
    
    # Get the book and page
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return {"error": "Book not found"}
    
    book_page = get_page(book_id=book_id, chapter_number=chapter_number, page_number=page_number, db=db)
    if not book_page:
        return {"error": "Book page not found"}

    # Use enhanced scene detection
    sorted_scenes, scene_counts, scene_positions, mood_analysis = enhanced_scene_detection(book_page.content)
    
    # Get trigger words
    trigger_words = detect_triggered_sounds(book_page.content)
    
    # Generate context summary
    context_summary = get_contextual_summary(book_page.content)
    
    # Determine primary mood and sound
    primary_mood = "neutral"
    primary_sound = "ambience/default_ambience"
    confidence = 0.5
    
    if mood_analysis:
        # Get the highest confidence scene
        best_scene = sorted_scenes[0]
        primary_mood = mood_analysis[best_scene]["mood"]
        primary_sound = mood_analysis[best_scene]["sound"]
        confidence = mood_analysis[best_scene]["confidence"]
    
    # Get carpet tracks (primary and secondary)
    carpet_tracks = []
    if primary_sound:
        carpet_tracks.append(primary_sound)
    
    # Add secondary sound if available
    if len(sorted_scenes) > 1:
        secondary_scene = sorted_scenes[1]
        secondary_sound = mood_analysis[secondary_scene]["sound"]
        if secondary_sound != primary_sound:
            carpet_tracks.append(secondary_sound)

    return {
        "book_id": book_id,
        "chapter_id": chapter_number,
        "page_id": page_number,
        "summary": context_summary,
        "detected_scenes": sorted_scenes,
        "scene_keyword_counts": scene_counts,
        "scene_keyword_positions": scene_positions,
        "carpet_tracks": carpet_tracks,
        "triggered_sounds": trigger_words,
        "trigger_positions": _extract_trigger_positions(trigger_words, book_page.content),
        "mood": primary_mood,
        "intensity": confidence,
        "atmosphere": primary_mood,
        "confidence": confidence,
        "reasoning": f"Primary mood: {primary_mood} (confidence: {confidence:.2f})",
        "mood_analysis": mood_analysis
    }

def _extract_trigger_positions(trigger_words: List[Dict], text: str) -> Dict[str, List[Dict]]:
    """
    Extract and organize trigger word positions for frontend synchronization.
    
    Args:
        trigger_words: List of trigger word dictionaries from emotion_analysis
        text: The full text content
        
    Returns:
        Dictionary with trigger word positions organized by type
    """
    if not trigger_words:
        return {}
    
    # Group triggers by type for better organization
    positions_by_type = {}
    
    for trigger in trigger_words:
        trigger_type = trigger.get("type", "unknown")
        
        if trigger_type not in positions_by_type:
            positions_by_type[trigger_type] = []
        
        # Create position info for frontend
        position_info = {
            "word": trigger["word"],
            "sound": trigger["sound"],
            "character_position": trigger["position"],
            "word_position": trigger["word_position"],
            "word_count": trigger["word_count"],
            "timing": trigger["timing"],
            "context": trigger.get("context", ""),
            "pattern_name": trigger.get("pattern_name", ""),
            "folder_path": trigger.get("folder_path", "")
        }
        
        positions_by_type[trigger_type].append(position_info)
    
    # Sort each type by word position for reading order
    for trigger_type in positions_by_type:
        positions_by_type[trigger_type].sort(key=lambda x: x["word_position"])
    
    return positions_by_type
