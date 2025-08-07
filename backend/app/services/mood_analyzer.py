import re
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
import json

@dataclass
class MoodAnalysis:
    """Result of sophisticated mood analysis for a page"""
    primary_mood: str
    secondary_mood: str
    confidence: float
    detected_elements: Dict[str, int]
    suggested_sound: str
    reasoning: str
    context_phrases: List[str]
    emotional_intensity: float
    atmospheric_density: float

class AdvancedMoodAnalyzer:
    """Massively sophisticated mood analyzer with regex-based phrase recognition and complex decision-making"""
    
    def __init__(self):
        # COMPLEX REGEX PATTERNS for sophisticated phrase matching
        self.REGEX_PATTERNS = {
            "epic_battle": {
                "patterns": [
                    r"\b(epic|heroic|mighty|powerful|tremendous|overwhelming)\s+(battle|struggle|war|conflict|fight)\b",
                    r"\b(battle|war|conflict)\s+(raging|fierce|terrifying|overwhelming|epic)\b",
                    r"\b(heroic|mighty|powerful)\s+(deeds|actions|struggle|effort)\b",
                    r"\b(grand|magnificent|tremendous)\s+(scale|proportions|display|force)\b"
                ],
                "weight": 5,
                "mood": "epic",
                "sound": "ambience/storm"
            },
            "mystical_magic": {
                "patterns": [
                    r"\b(magical|mystical|ethereal|otherworldly)\s+(aura|power|energy|presence|beauty)\b",
                    r"\b(supernatural|divine|sacred)\s+(force|intervention|ground|ritual)\b",
                    r"\b(ancient|wisdom|enchanting)\s+(magic|spell|melody|atmosphere)\b",
                    r"\b(magical|ethereal)\s+(spell|light|realm|transformation)\b"
                ],
                "weight": 4,
                "mood": "mystical",
                "sound": "ambience/atmosphere-sound-effect-239969"
            },
            "romantic_love": {
                "patterns": [
                    r"\b(love|romance|passion)\s+(blooming|growing|burning|intense)\b",
                    r"\b(affection|desire)\s+(shown|deep|warm|strong)\b",
                    r"\b(romantic|beloved)\s+(moment|presence|evening|story)\b",
                    r"\b(heart|kiss)\s+(beating|racing|shared|sweet)\b"
                ],
                "weight": 4,
                "mood": "romantic",
                "sound": "ambience/cabin"
            },
            "dark_evil": {
                "patterns": [
                    r"\b(dark|evil|corruption)\s+(presence|force|spreading|lurking)\b",
                    r"\b(shadow|death|decay)\s+(lurking|approaching|setting|visible)\b",
                    r"\b(rotten|corrupt|malicious)\s+(atmosphere|power|intent|soul)\b",
                    r"\b(sinister|dark)\s+(plot|magic|influence|whisper)\b"
                ],
                "weight": 4,
                "mood": "dark",
                "sound": "ambience/tense_drones"
            },
            "storm_weather": {
                "patterns": [
                    r"\b(storm|tempest)\s+(approaching|raging|wild|fierce)\b",
                    r"\b(thunder|lightning)\s+(crashing|flashing|rolling|strike)\b",
                    r"\b(rain|gale)\s+(pouring|falling|force|strong)\b",
                    r"\b(wind|air)\s+(howling|blowing|whistling|rustling)\b"
                ],
                "weight": 3,
                "mood": "tense",
                "sound": "ambience/stormy_night"
            },
            "mountain_journey": {
                "patterns": [
                    r"\b(mountain|cliff|ridge|summit)\s+(peak|face|line|reached|view)\b",
                    r"\b(alpine|high)\s+(meadow|air|elevation|altitude|forest)\b",
                    r"\b(long|traveling)\s+(journey|far|distance|companion)\b",
                    r"\b(road|path)\s+(ahead|forward|destiny|less traveled)\b"
                ],
                "weight": 3,
                "mood": "journey",
                "sound": "ambience/windy_mountains"
            },
            "peaceful_calm": {
                "patterns": [
                    r"\b(peaceful|tranquil|serene)\s+(silence|atmosphere|setting|beauty)\b",
                    r"\b(gentle|soft)\s+(breeze|whispers|touch|light|rain)\b",
                    r"\b(calm|comfortable)\s+(waters|warmth|mind|meditation)\b",
                    r"\b(cozy|warm)\s+(atmosphere|room|home|embrace)\b"
                ],
                "weight": 3,
                "mood": "peaceful",
                "sound": "ambience/default_ambience"
            },
            "victory_triumph": {
                "patterns": [
                    r"\b(victory|triumph)\s+(achieved|moment|return|march|dance)\b",
                    r"\b(successful|achievement)\s+(completion|mission|earned|unlocked)\b",
                    r"\b(joyous|hope)\s+(celebration|restored|renewed|reunion)\b",
                    r"\b(light|salvation)\s+(breaking|shining|found|granted)\b"
                ],
                "weight": 4,
                "mood": "triumphant",
                "sound": "ambience/default_ambience"
            },
            "mystery_intrigue": {
                "patterns": [
                    r"\b(mystery|enigmatic)\s+(deep|presence|unfolding|solved)\b",
                    r"\b(puzzling|curious)\s+(situation|case|clues|behavior)\b",
                    r"\b(strange|cryptic)\s+(occurrence|message|symbols|atmosphere)\b",
                    r"\b(secret|hidden)\s+(passage|meaning|truth|obscure)\b"
                ],
                "weight": 3,
                "mood": "mysterious",
                "sound": "ambience/atmosphere-sound-effect-239969"
            },
            "danger_peril": {
                "patterns": [
                    r"\b(danger|peril)\s+(lurking|ahead|close|zone)\b",
                    r"\b(threat|hazardous)\s+(growing|real|situation|terrain)\b",
                    r"\b(deadly|fatal|lethal)\s+(force|mistake|weapon|intent)\b",
                    r"\b(treacherous|risky)\s+(path|business|waters|move)\b"
                ],
                "weight": 4,
                "mood": "dangerous",
                "sound": "ambience/tense_drones"
            },
            "desperation_urgency": {
                "patterns": [
                    r"\b(desperate|urgent)\s+(situation|need|measure|plea)\b",
                    r"\b(critical|emergency)\s+(moment|decision|response|time)\b",
                    r"\b(last|final)\s+(chance|attempt|opportunity|stand)\b",
                    r"\b(doomed|hopeless)\s+(fate|cause|effort|struggle)\b"
                ],
                "weight": 4,
                "mood": "desperate",
                "sound": "ambience/tense_drones"
            },
            "ceremony_ritual": {
                "patterns": [
                    r"\b(ceremony|ritual)\s+(begins|performed|complete|grand)\b",
                    r"\b(formal|official)\s+(occasion|ceremony|gathering|event)\b",
                    r"\b(sacred|solemn)\s+(moment|ground|vow|atmosphere)\b",
                    r"\b(dignified|reverent)\s+(presence|ceremony|silence|prayer)\b"
                ],
                "weight": 3,
                "mood": "ceremonial",
                "sound": "ambience/default_ambience"
            }
        }
        
        # CONTEXT-BASED DECISION RULES
        self.CONTEXT_RULES = {
            "geographic_override": {
                "mountains": {
                    "patterns": [r"\b(mountain|peak|cliff|ridge|summit|alpine)\b"],
                    "override_mood": "journey",
                    "override_sound": "ambience/windy_mountains",
                    "weight": 2
                },
                "water": {
                    "patterns": [r"\b(river|stream|lake|water|flowing|crossing)\b"],
                    "override_mood": "peaceful",
                    "override_sound": "ambience/cabin_rain",
                    "weight": 2
                },
                "indoors": {
                    "patterns": [r"\b(inside|room|house|building|chamber|hall)\b"],
                    "override_mood": "peaceful",
                    "override_sound": "ambience/cabin",
                    "weight": 1
                },
                "night": {
                    "patterns": [r"\b(night|dark|evening|dusk|stars|moon)\b"],
                    "override_mood": "mysterious",
                    "override_sound": "ambience/stormy_night",
                    "weight": 2
                }
            },
            "intensity_modifiers": {
                "high_intensity": {
                    "patterns": [r"\b(intense|overwhelming|powerful|strong|deep|profound)\b"],
                    "boost_mood": "epic",
                    "boost_confidence": 0.3
                },
                "low_intensity": {
                    "patterns": [r"\b(gentle|soft|mild|subtle|quiet|calm)\b"],
                    "boost_mood": "peaceful",
                    "boost_confidence": 0.2
                }
            }
        }
        
        # MASSIVE keyword and phrase databases (keeping existing for fallback)
        self.MOOD_CATEGORIES = {
            "peaceful": {
                "keywords": ["peace", "calm", "quiet", "gentle", "soft", "tranquil", "serene", "comfortable", "cozy", "warm"],
                "phrases": [
                    "peaceful silence", "gentle breeze", "soft whispers", "tranquil atmosphere", "calm waters",
                    "serene landscape", "comfortable warmth", "cozy atmosphere", "peaceful moment", "gentle touch",
                    "soft light", "tranquil setting", "calm before", "serene beauty", "peaceful sleep",
                    "gentle rain", "soft music", "tranquil garden", "calm mind", "serene meditation"
                ],
                "sounds": ["ambience/default_ambience", "ambience/cabin", "ambience/atmosphere-sound-effect-239969"],
                "description": "Calm, comfortable, safe atmosphere with gentle elements"
            },
            "tense": {
                "keywords": ["tension", "fear", "anxiety", "worry", "nervous", "cautious", "suspicious", "uneasy", "apprehensive"],
                "phrases": [
                    "building tension", "growing fear", "nervous anticipation", "cautious approach", "suspicious atmosphere",
                    "uneasy feeling", "apprehensive mood", "tense silence", "fearful moment", "anxious waiting",
                    "worried expression", "nervous energy", "cautious movement", "suspicious glance", "uneasy peace",
                    "apprehensive step", "tension mounting", "fear creeping", "anxiety building", "worried thoughts"
                ],
                "sounds": ["ambience/tense_drones", "ambience/footsteps-approaching-316715", "ambience/stormy_night"],
                "description": "Building tension, fear, anxiety with suspenseful elements"
            },
            "epic": {
                "keywords": ["epic", "heroic", "battle", "war", "mighty", "powerful", "grand", "magnificent", "tremendous", "overwhelming"],
                "phrases": [
                    "epic battle", "heroic struggle", "mighty force", "powerful presence", "grand scale",
                    "magnificent display", "tremendous power", "overwhelming force", "epic proportions", "heroic deeds",
                    "mighty warriors", "powerful magic", "grand ceremony", "magnificent victory", "tremendous effort",
                    "overwhelming odds", "epic journey", "heroic sacrifice", "mighty fortress", "powerful enemy"
                ],
                "sounds": ["ambience/storm", "ambience/thunder-city-377703", "ambience/tense_drones"],
                "description": "Large-scale, heroic, powerful events with dramatic impact"
            },
            "mystical": {
                "keywords": ["magical", "mystical", "ethereal", "otherworldly", "enchanting", "supernatural", "divine", "sacred", "ancient", "wisdom"],
                "phrases": [
                    "magical aura", "mystical power", "ethereal beauty", "otherworldly presence", "enchanting melody",
                    "supernatural force", "divine intervention", "sacred ground", "ancient wisdom", "mystical energy",
                    "magical spell", "ethereal light", "otherworldly realm", "enchanting atmosphere", "supernatural being",
                    "divine blessing", "sacred ritual", "ancient magic", "mystical realm", "magical transformation"
                ],
                "sounds": ["ambience/atmosphere-sound-effect-239969", "ambience/default_ambience", "ambience/cabin"],
                "description": "Magical, supernatural, mystical atmosphere with enchanting elements"
            },
            "triumphant": {
                "keywords": ["victory", "triumph", "success", "achievement", "celebration", "joy", "hope", "light", "salvation"],
                "phrases": [
                    "victory achieved", "triumphant moment", "successful completion", "achievement unlocked", "celebration begins",
                    "joyous occasion", "hope restored", "light breaking", "salvation found", "victory march",
                    "triumphant return", "successful mission", "achievement earned", "celebration feast", "joyous reunion",
                    "hope renewed", "light shining", "salvation granted", "victory dance", "triumphant cheer"
                ],
                "sounds": ["ambience/default_ambience", "ambience/cabin", "ambience/atmosphere-sound-effect-239969"],
                "description": "Victory, success, celebration, hope with uplifting elements"
            },
            "dark": {
                "keywords": ["dark", "evil", "corruption", "shadow", "death", "decay", "rotten", "corrupt", "malicious", "sinister"],
                "phrases": [
                    "dark presence", "evil force", "corruption spreading", "shadow lurking", "death approaching",
                    "decay setting", "rotten atmosphere", "corrupt power", "malicious intent", "sinister plot",
                    "dark magic", "evil influence", "corruption deep", "shadow growing", "death looming",
                    "decay visible", "rotten core", "corrupt soul", "malicious grin", "sinister whisper"
                ],
                "sounds": ["ambience/tense_drones", "ambience/stormy_night", "ambience/footsteps-approaching-316715"],
                "description": "Dark, evil, corrupt atmosphere with malevolent elements"
            },
            "journey": {
                "keywords": ["travel", "journey", "road", "path", "walking", "riding", "moving", "adventure", "exploration"],
                "phrases": [
                    "long journey", "traveling far", "road ahead", "path forward", "walking distance",
                    "riding through", "moving forward", "adventure begins", "exploration continues", "journey's end",
                    "travel companion", "road less traveled", "path of destiny", "walking together", "riding into",
                    "moving toward", "adventure awaits", "exploration deep", "journey's start", "traveling light"
                ],
                "sounds": ["ambience/windy_mountains", "ambience/cabin", "ambience/default_ambience"],
                "description": "Travel, movement, adventure with dynamic elements"
            },
            "celebration": {
                "keywords": ["party", "celebration", "festival", "joy", "laughter", "music", "dancing", "feast", "merry"],
                "phrases": [
                    "party atmosphere", "celebration time", "festival spirit", "joyous occasion", "laughter ringing",
                    "music playing", "dancing feet", "feast prepared", "merry mood", "party gathering",
                    "celebration feast", "festival lights", "joyous laughter", "music filling", "dancing crowd",
                    "feast table", "merry company", "party spirit", "celebration song", "festival dance"
                ],
                "sounds": ["ambience/default_ambience", "ambience/cabin", "ambience/atmosphere-sound-effect-239969"],
                "description": "Celebration, party, festive atmosphere with joyous elements"
            },
            "melancholy": {
                "keywords": ["sad", "melancholy", "sorrow", "grief", "lonely", "mourning", "despair", "heartbroken", "weep"],
                "phrases": [
                    "sad moment", "melancholy mood", "sorrow deep", "grief overwhelming", "lonely heart",
                    "mourning period", "despair setting", "heartbroken soul", "weeping softly", "sad reflection",
                    "melancholy thoughts", "sorrow shared", "grief visible", "lonely night", "mourning song",
                    "despair growing", "heartbroken tears", "weeping willow", "sad memories", "melancholy air"
                ],
                "sounds": ["ambience/tense_drones", "ambience/stormy_night", "ambience/cabin"],
                "description": "Sad, sorrowful, melancholic atmosphere with emotional depth"
            },
            "mysterious": {
                "keywords": ["mystery", "enigmatic", "puzzling", "curious", "strange", "cryptic", "obscure", "secret", "hidden"],
                "phrases": [
                    "mystery deep", "enigmatic presence", "puzzling situation", "curious case", "strange occurrence",
                    "cryptic message", "obscure meaning", "secret hidden", "mystery unfolding", "enigmatic smile",
                    "puzzling clues", "curious behavior", "strange atmosphere", "cryptic symbols", "obscure truth",
                    "secret passage", "mystery solved", "enigmatic figure", "puzzling mystery", "curious discovery"
                ],
                "sounds": ["ambience/atmosphere-sound-effect-239969", "ambience/tense_drones", "ambience/cabin"],
                "description": "Mysterious, puzzling, enigmatic atmosphere with intrigue"
            },
            "romantic": {
                "keywords": ["love", "romance", "passion", "affection", "desire", "romantic", "beloved", "heart", "kiss"],
                "phrases": [
                    "love blooming", "romance growing", "passion burning", "affection shown", "desire deep",
                    "romantic moment", "beloved presence", "heart beating", "kiss shared", "love story",
                    "romance begins", "passion intense", "affection warm", "desire strong", "romantic evening",
                    "beloved one", "heart racing", "kiss sweet", "love eternal", "romance perfect"
                ],
                "sounds": ["ambience/cabin", "ambience/default_ambience", "ambience/atmosphere-sound-effect-239969"],
                "description": "Romantic, loving, passionate atmosphere with intimate elements"
            },
            "dangerous": {
                "keywords": ["danger", "peril", "threat", "hazardous", "risky", "deadly", "fatal", "lethal", "treacherous"],
                "phrases": [
                    "danger lurking", "peril ahead", "threat growing", "hazardous situation", "risky move",
                    "deadly force", "fatal mistake", "lethal weapon", "treacherous path", "danger close",
                    "peril deep", "threat real", "hazardous terrain", "risky business", "deadly intent",
                    "fatal error", "lethal dose", "treacherous waters", "danger zone", "peril imminent"
                ],
                "sounds": ["ambience/tense_drones", "ambience/footsteps-approaching-316715", "ambience/stormy_night"],
                "description": "Dangerous, perilous, threatening atmosphere with risk elements"
            },
            "hopeful": {
                "keywords": ["hope", "optimistic", "promising", "bright", "future", "possibility", "potential", "aspiration"],
                "phrases": [
                    "hope rising", "optimistic outlook", "promising future", "bright tomorrow", "future bright",
                    "possibility real", "potential great", "aspiration high", "hope renewed", "optimistic spirit",
                    "promising start", "bright horizon", "future promising", "possibility endless", "potential unlimited",
                    "aspiration achieved", "hope eternal", "optimistic view", "promising signs", "bright future"
                ],
                "sounds": ["ambience/default_ambience", "ambience/cabin", "ambience/atmosphere-sound-effect-239969"],
                "description": "Hopeful, optimistic, promising atmosphere with positive elements"
            },
            "desperate": {
                "keywords": ["desperate", "urgent", "critical", "emergency", "last_chance", "final", "doomed", "hopeless"],
                "phrases": [
                    "desperate situation", "urgent need", "critical moment", "emergency call", "last chance",
                    "final attempt", "doomed fate", "hopeless cause", "desperate measure", "urgent action",
                    "critical decision", "emergency response", "last opportunity", "final stand", "doomed effort",
                    "hopeless struggle", "desperate plea", "urgent request", "critical time", "emergency situation"
                ],
                "sounds": ["ambience/tense_drones", "ambience/storm", "ambience/footsteps-approaching-316715"],
                "description": "Desperate, urgent, critical atmosphere with intense elements"
            },
            "ceremonial": {
                "keywords": ["ceremony", "ritual", "formal", "official", "sacred", "solemn", "dignified", "reverent"],
                "phrases": [
                    "ceremony begins", "ritual performed", "formal occasion", "official ceremony", "sacred moment",
                    "solemn atmosphere", "dignified presence", "reverent silence", "ceremony complete", "ritual sacred",
                    "formal gathering", "official event", "sacred ground", "solemn vow", "dignified ceremony",
                    "reverent prayer", "ceremony grand", "ritual ancient", "formal celebration", "official recognition"
                ],
                "sounds": ["ambience/default_ambience", "ambience/cabin", "ambience/atmosphere-sound-effect-239969"],
                "description": "Ceremonial, ritual, formal atmosphere with dignified elements"
            }
        }
        
        # MASSIVE geographic and environmental phrase databases
        self.GEOGRAPHIC_ELEMENTS = {
            "mountains": {
                "keywords": ["mountain", "peak", "cliff", "ridge", "summit", "alpine", "high", "elevation"],
                "phrases": [
                    "mountain peak", "cliff face", "ridge line", "summit reached", "alpine meadow",
                    "high elevation", "mountain range", "cliff edge", "ridge top", "summit view",
                    "alpine air", "high altitude", "mountain pass", "cliff side", "ridge path",
                    "summit climb", "alpine forest", "high peak", "mountain slope", "cliff base"
                ]
            },
            "water": {
                "keywords": ["river", "stream", "lake", "water", "flowing", "crossing", "ferry", "boat"],
                "phrases": [
                    "river flowing", "stream bubbling", "lake surface", "water clear", "flowing water",
                    "crossing river", "ferry boat", "boat sailing", "river bank", "stream bed",
                    "lake shore", "water deep", "flowing stream", "crossing bridge", "ferry crossing",
                    "boat dock", "river bend", "stream source", "lake bottom", "water surface"
                ]
            },
            "indoors": {
                "keywords": ["inside", "room", "house", "building", "chamber", "hall", "interior"],
                "phrases": [
                    "inside room", "house interior", "building structure", "chamber deep", "hall long",
                    "interior space", "inside walls", "room cozy", "house warm", "building grand",
                    "chamber secret", "hall empty", "interior design", "inside safe", "room quiet",
                    "house home", "building tall", "chamber dark", "hall wide", "interior beautiful"
                ]
            },
            "plains": {
                "keywords": ["plain", "field", "grassland", "meadow", "open", "vast", "wide"],
                "phrases": [
                    "plain vast", "field open", "grassland wide", "meadow green", "open space",
                    "vast landscape", "wide expanse", "plain flat", "field empty", "grassland rolling",
                    "meadow peaceful", "open area", "vast horizon", "wide view", "plain endless",
                    "field golden", "grassland natural", "meadow wild", "open sky", "vast territory"
                ]
            },
            "ruins": {
                "keywords": ["ruin", "ancient", "stone", "echo", "old", "crumbling", "decay"],
                "phrases": [
                    "ruin ancient", "stone old", "echo hollow", "crumbling walls", "decay visible",
                    "ancient ruin", "stone structure", "echo chamber", "old building", "crumbling stone",
                    "decay setting", "ruin forgotten", "ancient stone", "echo sound", "old ruins",
                    "crumbling decay", "stone ancient", "echo empty", "old structure", "decay old"
                ]
            }
        }
        
        # MASSIVE weather and atmospheric phrase databases
        self.WEATHER_ELEMENTS = {
            "storm": {
                "keywords": ["storm", "thunder", "lightning", "rain", "tempest", "gale", "wind", "stormy"],
                "phrases": [
                    "storm approaching", "thunder crashing", "lightning flashing", "rain pouring", "tempest raging",
                    "gale force", "wind howling", "stormy weather", "thunder rolling", "lightning strike",
                    "rain falling", "tempest wild", "gale strong", "wind blowing", "storm dark",
                    "thunder loud", "lightning bright", "rain heavy", "tempest fierce", "gale powerful"
                ]
            },
            "night": {
                "keywords": ["night", "dark", "evening", "dusk", "stars", "moon", "shadow"],
                "phrases": [
                    "night dark", "evening quiet", "dusk falling", "stars shining", "moon bright",
                    "shadow deep", "night silent", "dark sky", "evening calm", "dusk peaceful",
                    "stars twinkling", "moon full", "shadow moving", "night long", "dark night",
                    "evening cool", "dusk beautiful", "stars clear", "moon silver", "shadow cast"
                ]
            },
            "wind": {
                "keywords": ["wind", "breeze", "gust", "blowing", "air"],
                "phrases": [
                    "wind blowing", "breeze gentle", "gust strong", "air moving", "wind howling",
                    "breeze cool", "gust powerful", "air fresh", "wind whistling", "breeze soft",
                    "gust sudden", "air clean", "wind rustling", "breeze warm", "gust fierce",
                    "air still", "wind direction", "breeze light", "gust wild", "air pure"
                ]
            },
            "cold": {
                "keywords": ["cold", "snow", "ice", "frost", "chill", "freezing"],
                "phrases": [
                    "cold air", "snow falling", "ice forming", "frost covering", "chill wind",
                    "freezing temperature", "cold night", "snow white", "ice crystal", "frost pattern",
                    "chill deep", "freezing cold", "cold winter", "snow deep", "ice thick",
                    "frost beautiful", "chill biting", "freezing point", "cold breath", "snow pure"
                ]
            },
            "warm": {
                "keywords": ["warm", "sun", "heat", "hot", "fire", "burning"],
                "phrases": [
                    "warm sun", "heat intense", "hot day", "fire burning", "burning bright",
                    "warm glow", "sun shining", "heat rising", "hot summer", "fire warm",
                    "burning passion", "warm light", "sun bright", "heat strong", "hot weather",
                    "fire crackling", "burning desire", "warm embrace", "sun golden", "heat comfortable"
                ]
            }
        }
        
        # MASSIVE emotional intensity phrase databases
        self.EMOTIONAL_INDICATORS = {
            "high_intensity": {
                "keywords": ["intense", "overwhelming", "powerful", "strong", "deep", "profound"],
                "phrases": [
                    "intense emotion", "overwhelming feeling", "powerful impact", "strong reaction", "deep emotion",
                    "profound experience", "intense moment", "overwhelming force", "powerful presence", "strong feeling",
                    "deep impact", "profound effect", "intense passion", "overwhelming love", "powerful anger",
                    "strong fear", "deep sorrow", "profound joy", "intense hate", "overwhelming grief"
                ]
            },
            "medium_intensity": {
                "keywords": ["moderate", "steady", "consistent", "stable", "balanced", "measured"],
                "phrases": [
                    "moderate emotion", "steady feeling", "consistent mood", "stable emotion", "balanced reaction",
                    "measured response", "moderate intensity", "steady pace", "consistent flow", "stable state",
                    "balanced approach", "measured tone", "moderate passion", "steady love", "consistent anger",
                    "stable fear", "balanced sorrow", "measured joy", "moderate hate", "steady grief"
                ]
            },
            "low_intensity": {
                "keywords": ["gentle", "soft", "mild", "subtle", "quiet", "calm"],
                "phrases": [
                    "gentle emotion", "soft feeling", "mild reaction", "subtle mood", "quiet emotion",
                    "calm response", "gentle intensity", "soft passion", "mild love", "subtle anger",
                    "quiet fear", "calm sorrow", "gentle joy", "soft hate", "mild grief",
                    "subtle emotion", "quiet feeling", "calm reaction", "gentle mood", "soft response"
                ]
            }
        }

    def analyze_page_mood(self, text: str) -> MoodAnalysis:
        """Massively sophisticated mood analysis with regex-based phrase recognition and complex decision-making"""
        if not text:
            return self._create_empty_analysis()
        
        text_lower = text.lower()
        
        # Step 1: Advanced regex-based pattern matching
        regex_analysis = self._analyze_regex_patterns(text_lower)
        
        # Step 2: Context-based decision rules
        context_analysis = self._analyze_context_rules(text_lower)
        
        # Step 3: Fallback to traditional keyword/phrase analysis
        traditional_analysis = self._analyze_traditional_patterns(text_lower)
        
        # Step 4: Complex decision-making combining all analyses
        primary_mood, secondary_mood, suggested_sound = self._make_complex_decisions(
            regex_analysis, context_analysis, traditional_analysis
        )
        
        # Step 5: Calculate confidence with regex weighting
        confidence = self._calculate_regex_confidence(regex_analysis, context_analysis, traditional_analysis)
        
        # Step 6: Generate sophisticated reasoning
        reasoning = self._generate_regex_reasoning(regex_analysis, context_analysis, traditional_analysis)
        
        # Step 7: Extract context phrases using regex
        context_phrases = self._extract_regex_context_phrases(text_lower, regex_analysis)
        
        # Step 8: Calculate emotional and atmospheric density
        emotional_intensity = self._calculate_regex_emotional_intensity(regex_analysis, context_analysis)
        atmospheric_density = self._calculate_regex_atmospheric_density(regex_analysis, context_analysis)
        
        return MoodAnalysis(
            primary_mood=primary_mood,
            secondary_mood=secondary_mood,
            confidence=confidence,
            detected_elements={**regex_analysis, **context_analysis, **traditional_analysis},
            suggested_sound=suggested_sound,
            reasoning=reasoning,
            context_phrases=context_phrases,
            emotional_intensity=emotional_intensity,
            atmospheric_density=atmospheric_density
        )

    def _analyze_regex_patterns(self, text: str) -> Dict[str, int]:
        """Advanced regex-based pattern analysis"""
        results = {}
        
        for pattern_name, pattern_data in self.REGEX_PATTERNS.items():
            score = 0
            matches = []
            
            for pattern in pattern_data["patterns"]:
                matches_found = re.findall(pattern, text, re.IGNORECASE)
                if matches_found:
                    score += len(matches_found) * pattern_data["weight"]
                    matches.extend(matches_found)
            
            if score > 0:
                results[pattern_name] = {
                    "score": score,
                    "mood": pattern_data["mood"],
                    "sound": pattern_data["sound"],
                    "matches": matches
                }
        
        return results

    def _analyze_context_rules(self, text: str) -> Dict[str, any]:
        """Analyze context-based decision rules"""
        results = {}
        
        # Geographic overrides
        for geo_type, geo_data in self.CONTEXT_RULES["geographic_override"].items():
            for pattern in geo_data["patterns"]:
                if re.search(pattern, text, re.IGNORECASE):
                    results[f"geo_{geo_type}"] = {
                        "override_mood": geo_data["override_mood"],
                        "override_sound": geo_data["override_sound"],
                        "weight": geo_data["weight"]
                    }
                    break
        
        # Intensity modifiers
        for intensity_type, intensity_data in self.CONTEXT_RULES["intensity_modifiers"].items():
            for pattern in intensity_data["patterns"]:
                if re.search(pattern, text, re.IGNORECASE):
                    results[f"intensity_{intensity_type}"] = {
                        "boost_mood": intensity_data["boost_mood"],
                        "boost_confidence": intensity_data["boost_confidence"]
                    }
                    break
        
        return results

    def _analyze_traditional_patterns(self, text: str) -> Dict[str, int]:
        """Fallback traditional keyword/phrase analysis"""
        mood_scores = {}
        
        for mood, data in self.MOOD_CATEGORIES.items():
            score = 0
            # Check keywords
            for keyword in data["keywords"]:
                if keyword in text:
                    score += 1
            
            # Check phrases (weighted higher)
            for phrase in data["phrases"]:
                if phrase in text:
                    score += 3  # Phrases worth 3x keywords
            
            if score > 0:
                mood_scores[mood] = score
        
        return mood_scores

    def _make_complex_decisions(self, regex_analysis: Dict, context_analysis: Dict, 
                               traditional_analysis: Dict) -> Tuple[str, str, str]:
        """Complex decision-making combining all analysis methods"""
        
        # Priority 1: Regex patterns (highest priority)
        if regex_analysis:
            # Find the highest scoring regex pattern
            best_regex = max(regex_analysis.items(), key=lambda x: x[1]["score"])
            primary_mood = best_regex[1]["mood"]
            suggested_sound = best_regex[1]["sound"]
            
            # Find secondary mood from other regex patterns
            secondary_mood = "neutral"
            if len(regex_analysis) > 1:
                second_best = sorted(regex_analysis.items(), key=lambda x: x[1]["score"], reverse=True)[1]
                secondary_mood = second_best[1]["mood"]
            
            return primary_mood, secondary_mood, suggested_sound
        
        # Priority 2: Context overrides
        if context_analysis:
            for key, data in context_analysis.items():
                if key.startswith("geo_"):
                    return data["override_mood"], "neutral", data["override_sound"]
        
        # Priority 3: Traditional analysis
        if traditional_analysis:
            sorted_moods = sorted(traditional_analysis.items(), key=lambda x: x[1], reverse=True)
            primary_mood = sorted_moods[0][0]
            secondary_mood = sorted_moods[1][0] if len(sorted_moods) > 1 else "neutral"
            
            # Get sound from mood category
            mood_data = self.MOOD_CATEGORIES.get(primary_mood, self.MOOD_CATEGORIES["peaceful"])
            suggested_sound = mood_data["sounds"][0]
            
            return primary_mood, secondary_mood, suggested_sound
        
        # Default fallback
        return "neutral", "neutral", "ambience/default_ambience"

    def _calculate_regex_confidence(self, regex_analysis: Dict, context_analysis: Dict, 
                                  traditional_analysis: Dict) -> float:
        """Calculate confidence with regex weighting"""
        
        # Regex confidence (highest weight)
        regex_confidence = 0.0
        if regex_analysis:
            total_regex_score = sum(data["score"] for data in regex_analysis.values())
            regex_confidence = min(total_regex_score / 50.0, 1.0)
        
        # Context confidence
        context_confidence = min(len(context_analysis) / 5.0, 1.0)
        
        # Traditional confidence
        traditional_confidence = min(sum(traditional_analysis.values()) / 20.0, 1.0)
        
        # Weighted average with regex priority
        confidence = (
            regex_confidence * 0.6 +
            context_confidence * 0.3 +
            traditional_confidence * 0.1
        )
        
        return min(1.0, confidence)

    def _generate_regex_reasoning(self, regex_analysis: Dict, context_analysis: Dict, 
                                traditional_analysis: Dict) -> str:
        """Generate sophisticated reasoning with regex information"""
        
        reasons = []
        
        # Regex pattern reasoning
        if regex_analysis:
            for pattern_name, data in regex_analysis.items():
                reasons.append(f"Regex pattern '{pattern_name}': {data['mood']} (score: {data['score']})")
        
        # Context reasoning
        if context_analysis:
            for key, data in context_analysis.items():
                if key.startswith("geo_"):
                    reasons.append(f"Geographic override: {data['override_mood']}")
                elif key.startswith("intensity_"):
                    reasons.append(f"Intensity modifier: {data['boost_mood']}")
        
        # Traditional reasoning
        if traditional_analysis:
            top_mood = max(traditional_analysis.items(), key=lambda x: x[1])
            reasons.append(f"Traditional analysis: {top_mood[0]} (score: {top_mood[1]})")
        
        return "; ".join(reasons) if reasons else "No clear patterns detected"

    def _extract_regex_context_phrases(self, text: str, regex_analysis: Dict) -> List[str]:
        """Extract context phrases using regex matches"""
        context_phrases = []
        
        for pattern_name, data in regex_analysis.items():
            if "matches" in data:
                context_phrases.extend(data["matches"][:2])  # Top 2 matches per pattern
        
        return context_phrases[:5]  # Return top 5 phrases

    def _calculate_regex_emotional_intensity(self, regex_analysis: Dict, context_analysis: Dict) -> float:
        """Calculate emotional intensity using regex analysis"""
        
        # Base intensity from regex patterns
        base_intensity = sum(data["score"] for data in regex_analysis.values()) / 100.0 if regex_analysis else 0.5
        
        # Intensity modifiers from context
        for key, data in context_analysis.items():
            if key.startswith("intensity_high_intensity"):
                base_intensity = min(base_intensity * 1.5, 1.0)
            elif key.startswith("intensity_low_intensity"):
                base_intensity = base_intensity * 0.5
        
        return min(1.0, base_intensity)

    def _calculate_regex_atmospheric_density(self, regex_analysis: Dict, context_analysis: Dict) -> float:
        """Calculate atmospheric density using regex analysis"""
        
        # Count geographic and weather patterns
        geo_weather_patterns = sum(1 for key in regex_analysis.keys() 
                                 if any(geo in key for geo in ["mountain", "storm", "water", "night"]))
        
        # Context density
        context_density = len(context_analysis) / 5.0
        
        return min((geo_weather_patterns + context_density) / 2.0, 1.0)

    def _create_empty_analysis(self) -> MoodAnalysis:
        """Create empty analysis for empty text"""
        return MoodAnalysis(
            primary_mood="neutral",
            secondary_mood="neutral",
            confidence=0.0,
            detected_elements={},
            suggested_sound="ambience/default_ambience",
            reasoning="No text provided",
            context_phrases=[],
            emotional_intensity=0.0,
            atmospheric_density=0.0
        )

# Legacy compatibility
class MoodAnalyzer(AdvancedMoodAnalyzer):
    """Legacy wrapper for backward compatibility"""
    pass

def analyze_book_pages(book_content: List[str]) -> List[MoodAnalysis]:
    """Analyze all pages of a book with enhanced mood analysis"""
    analyzer = AdvancedMoodAnalyzer()
    return [analyzer.analyze_page_mood(page) for page in book_content] 