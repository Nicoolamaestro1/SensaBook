import re
from typing import Dict, List, Tuple, Optional
from collections import Counter, defaultdict
from dataclasses import dataclass
from enum import Enum
import json

class EmotionType(Enum):
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    NEUTRAL = "neutral"

class ThemeType(Enum):
    ADVENTURE = "adventure"
    ROMANCE = "romance"
    MYSTERY = "mystery"
    HORROR = "horror"
    FANTASY = "fantasy"
    DRAMA = "drama"
    COMEDY = "comedy"
    ACTION = "action"

@dataclass
class EmotionResult:
    primary_emotion: EmotionType
    emotion_scores: Dict[str, float]
    intensity: float  # 0.0 to 1.0
    confidence: float
    keywords: List[str]
    context: str

@dataclass
class ThemeResult:
    primary_theme: ThemeType
    theme_scores: Dict[str, float]
    sub_themes: List[str]
    setting_elements: List[str]
    atmosphere: str

class AdvancedEmotionAnalyzer:
    def __init__(self):
        # Emotion keywords and their weights
        self.emotion_keywords = {
            EmotionType.JOY: {
                "happy": 0.8, "joy": 0.9, "excited": 0.7, "delighted": 0.8,
                "cheerful": 0.7, "elated": 0.9, "thrilled": 0.8, "ecstatic": 0.9,
                "smile": 0.6, "laugh": 0.7, "celebrate": 0.8, "victory": 0.7,
                "wonderful": 0.7, "amazing": 0.6, "fantastic": 0.7, "brilliant": 0.6
            },
            EmotionType.SADNESS: {
                "sad": 0.8, "depressed": 0.9, "melancholy": 0.8, "grief": 0.9,
                "sorrow": 0.8, "tears": 0.7, "mourning": 0.8, "despair": 0.9,
                "lonely": 0.7, "heartbroken": 0.9, "weep": 0.7, "sorrowful": 0.8,
                "miserable": 0.8, "hopeless": 0.9, "gloomy": 0.7, "dejected": 0.8
            },
            EmotionType.ANGER: {
                "angry": 0.8, "furious": 0.9, "rage": 0.9, "irritated": 0.6,
                "enraged": 0.9, "outraged": 0.8, "fuming": 0.8, "livid": 0.9,
                "hostile": 0.8, "aggressive": 0.7, "violent": 0.8, "wrath": 0.9,
                "furious": 0.9, "incensed": 0.8, "irate": 0.8, "mad": 0.7
            },
            EmotionType.FEAR: {
                "afraid": 0.8, "terrified": 0.9, "scared": 0.7, "horrified": 0.9,
                "panic": 0.9, "dread": 0.8, "anxious": 0.6, "nervous": 0.5,
                "frightened": 0.7, "petrified": 0.9, "alarmed": 0.7, "distressed": 0.6,
                "terrifying": 0.9, "fearful": 0.7, "apprehensive": 0.6, "worried": 0.5
            },
            EmotionType.SURPRISE: {
                "surprised": 0.7, "shocked": 0.8, "amazed": 0.7, "astonished": 0.8,
                "stunned": 0.8, "bewildered": 0.6, "startled": 0.7, "astounded": 0.8,
                "incredible": 0.6, "unexpected": 0.7, "suddenly": 0.5, "abruptly": 0.5,
                "unbelievable": 0.7, "remarkable": 0.6, "extraordinary": 0.6
            },
            EmotionType.DISGUST: {
                "disgusted": 0.8, "revolted": 0.9, "repulsed": 0.8, "sickened": 0.8,
                "nauseated": 0.8, "appalled": 0.7, "horrified": 0.8, "contempt": 0.7,
                "loathing": 0.9, "abhorrent": 0.8, "vile": 0.8, "repugnant": 0.8,
                "revolting": 0.8, "disgusting": 0.8, "nauseating": 0.8
            }
        }
        
        # Theme keywords and patterns
        self.theme_keywords = {
            ThemeType.ADVENTURE: ["quest", "journey", "explore", "discover", "treasure", "map", "expedition", "adventure", "travel"],
            ThemeType.ROMANCE: ["love", "heart", "kiss", "romance", "passion", "affection", "desire", "romantic", "beloved"],
            ThemeType.MYSTERY: ["mystery", "clue", "investigate", "detective", "secret", "puzzle", "enigma", "suspense", "mysterious"],
            ThemeType.HORROR: ["horror", "terrifying", "nightmare", "haunted", "ghost", "demonic", "evil", "scary", "frightening"],
            ThemeType.FANTASY: ["magic", "wizard", "spell", "dragon", "fantasy", "enchanted", "mythical", "magical", "sorcery"],
            ThemeType.DRAMA: ["conflict", "tension", "drama", "struggle", "betrayal", "tragedy", "dramatic", "emotional"],
            ThemeType.COMEDY: ["funny", "humor", "joke", "laugh", "comedy", "amusing", "hilarious", "comical", "witty"],
            ThemeType.ACTION: ["fight", "battle", "combat", "action", "thrilling", "intense", "explosive", "warrior", "hero"]
        }
        
        # Setting and atmosphere keywords
        self.setting_keywords = {
            "indoor": ["room", "house", "building", "chamber", "hall", "kitchen", "library", "office", "bedroom"],
            "outdoor": ["forest", "mountain", "beach", "field", "garden", "park", "street", "meadow", "valley"],
            "urban": ["city", "town", "street", "building", "alley", "market", "square", "urban", "metropolitan"],
            "rural": ["village", "farm", "countryside", "meadow", "pasture", "orchard", "rural", "rustic"],
            "night": ["night", "dark", "moonlight", "stars", "midnight", "evening", "darkness", "shadow"],
            "day": ["day", "sunlight", "morning", "afternoon", "bright", "sunny", "dawn", "noon"],
            "weather": ["rain", "storm", "wind", "snow", "fog", "mist", "thunder", "lightning", "cloudy"]
        }

    def analyze_emotion(self, text: str) -> EmotionResult:
        """Analyze the emotional content of text."""
        if not text:
            return EmotionResult(
                primary_emotion=EmotionType.NEUTRAL,
                emotion_scores={},
                intensity=0.0,
                confidence=0.0,
                keywords=[],
                context=""
            )
        
        # Normalize text
        text = text.lower()
        words = re.findall(r'\b\w+\b', text)
        
        # Calculate emotion scores
        emotion_scores = defaultdict(float)
        found_keywords = []
        
        for emotion_type, keywords in self.emotion_keywords.items():
            for keyword, weight in keywords.items():
                if keyword in text:
                    emotion_scores[emotion_type.value] += weight
                    found_keywords.append(keyword)
        
        # Determine primary emotion
        if emotion_scores:
            primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])
            primary_emotion_type = EmotionType(primary_emotion[0])
            intensity = min(primary_emotion[1] / 3.0, 1.0)  # Normalize to 0-1
            confidence = min(len(found_keywords) / 10.0, 1.0)
        else:
            primary_emotion_type = EmotionType.NEUTRAL
            intensity = 0.0
            confidence = 0.0
        
        # Extract context (first sentence)
        context = text.split('.')[0] if '.' in text else text[:100]
        
        return EmotionResult(
            primary_emotion=primary_emotion_type,
            emotion_scores=dict(emotion_scores),
            intensity=intensity,
            confidence=confidence,
            keywords=found_keywords,
            context=context
        )

    def analyze_theme(self, text: str) -> ThemeResult:
        """Analyze the thematic content of text."""
        if not text:
            return ThemeResult(
                primary_theme=ThemeType.DRAMA,
                theme_scores={},
                sub_themes=[],
                setting_elements=[],
                atmosphere="neutral"
            )
        
        text = text.lower()
        theme_scores = defaultdict(float)
        setting_elements = []
        atmosphere_elements = []
        
        # Calculate theme scores
        for theme_type, keywords in self.theme_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    theme_scores[theme_type.value] += 1.0
        
        # Determine primary theme
        if theme_scores:
            primary_theme = max(theme_scores.items(), key=lambda x: x[1])
            primary_theme_type = ThemeType(primary_theme[0])
        else:
            primary_theme_type = ThemeType.DRAMA
        
        # Detect setting elements
        for setting_type, keywords in self.setting_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    setting_elements.append(f"{setting_type}:{keyword}")
        
        # Determine atmosphere based on emotion and setting
        atmosphere = self._determine_atmosphere(text)
        
        return ThemeResult(
            primary_theme=primary_theme_type,
            theme_scores=dict(theme_scores),
            sub_themes=list(theme_scores.keys()),
            setting_elements=setting_elements,
            atmosphere=atmosphere
        )

    def _determine_atmosphere(self, text: str) -> str:
        """Determine the overall atmosphere of the text."""
        atmosphere_indicators = {
            "dark": ["dark", "shadow", "night", "black", "gloomy", "dim", "murky"],
            "bright": ["bright", "light", "sunny", "clear", "illuminated", "radiant", "luminous"],
            "tense": ["tense", "nervous", "anxious", "worried", "stressful", "strained", "strained"],
            "peaceful": ["calm", "peaceful", "tranquil", "serene", "quiet", "gentle", "soothing"],
            "energetic": ["energetic", "lively", "vibrant", "dynamic", "active", "spirited", "enthusiastic"],
            "mysterious": ["mysterious", "enigmatic", "puzzling", "curious", "strange", "cryptic", "obscure"]
        }
        
        text = text.lower()
        atmosphere_scores = defaultdict(int)
        
        for atmosphere, keywords in atmosphere_indicators.items():
            for keyword in keywords:
                if keyword in text:
                    atmosphere_scores[atmosphere] += 1
        
        if atmosphere_scores:
            return max(atmosphere_scores.items(), key=lambda x: x[1])[0]
        return "neutral"

    def generate_soundscape_recommendations(self, emotion_result: EmotionResult, theme_result: ThemeResult) -> Dict:
        """Generate soundscape recommendations based on emotion and theme analysis."""
        recommendations = {
            "primary_soundscape": self._map_emotion_to_soundscape(emotion_result.primary_emotion),
            "secondary_soundscape": self._map_theme_to_soundscape(theme_result.primary_theme),
            "intensity": emotion_result.intensity,
            "atmosphere": theme_result.atmosphere,
            "recommended_volume": self._calculate_volume(emotion_result.intensity),
            "sound_effects": self._get_sound_effects(emotion_result, theme_result)
        }
        
        return recommendations

    def _map_emotion_to_soundscape(self, emotion: EmotionType) -> str:
        """Map emotion to appropriate soundscape."""
        emotion_soundscapes = {
            EmotionType.JOY: "bright_ambience.mp3",
            EmotionType.SADNESS: "melancholy_drones.mp3",
            EmotionType.ANGER: "tense_rhythms.mp3",
            EmotionType.FEAR: "dark_ambience.mp3",
            EmotionType.SURPRISE: "sudden_impact.mp3",
            EmotionType.DISGUST: "unsettling_tones.mp3",
            EmotionType.NEUTRAL: "default_ambience.mp3"
        }
        return emotion_soundscapes.get(emotion, "default_ambience.mp3")

    def _map_theme_to_soundscape(self, theme: ThemeType) -> str:
        """Map theme to appropriate soundscape."""
        theme_soundscapes = {
            ThemeType.ADVENTURE: "epic_journey.mp3",
            ThemeType.ROMANCE: "romantic_melody.mp3",
            ThemeType.MYSTERY: "mysterious_ambience.mp3",
            ThemeType.HORROR: "horror_ambience.mp3",
            ThemeType.FANTASY: "magical_realms.mp3",
            ThemeType.DRAMA: "dramatic_tension.mp3",
            ThemeType.COMEDY: "light_hearted.mp3",
            ThemeType.ACTION: "action_rhythms.mp3"
        }
        return theme_soundscapes.get(theme, "default_ambience.mp3")

    def _calculate_volume(self, intensity: float) -> float:
        """Calculate recommended volume based on emotion intensity."""
        base_volume = 0.5
        intensity_multiplier = 0.3
        return min(base_volume + (intensity * intensity_multiplier), 1.0)

    def _get_sound_effects(self, emotion_result: EmotionResult, theme_result: ThemeResult) -> List[str]:
        """Get recommended sound effects based on analysis."""
        effects = []
        
        # Add emotion-based effects
        if emotion_result.primary_emotion == EmotionType.FEAR:
            effects.extend(["heartbeat.mp3", "distant_scream.mp3"])
        elif emotion_result.primary_emotion == EmotionType.SURPRISE:
            effects.append("sudden_impact.mp3")
        elif emotion_result.primary_emotion == EmotionType.JOY:
            effects.append("bright_chimes.mp3")
        
        # Add theme-based effects
        if theme_result.primary_theme == ThemeType.ACTION:
            effects.extend(["sword_clash.mp3", "footsteps.mp3"])
        elif theme_result.primary_theme == ThemeType.FANTASY:
            effects.append("magic_spell.mp3")
        
        return effects

# Global analyzer instance
emotion_analyzer = AdvancedEmotionAnalyzer()

# COMPREHENSIVE REGEX-BASED TRIGGER SYSTEM
TRIGGER_PATTERNS = {
    # WEATHER & ATMOSPHERIC SOUNDS
    "wind_sounds": {
        "patterns": [
            r"\b(wind|breeze|gust|gale|zephyr|blast|whirlwind|cyclone|hurricane|typhoon)\b",
            r"\b(wind|breeze)\s+(howling|whistling|whispering|moaning|sighing|rustling|swirling|roaring|screaming|wailing)\b",
            r"\b(howling|whistling|whispering|moaning|sighing|rustling|swirling|roaring|screaming|wailing)\s+(wind|breeze)\b",
            r"\b(leaves?|trees?|branches?)\s+(rustling|swaying|dancing|trembling|quivering|shaking)\b",
            r"\b(rustling|swaying|dancing|trembling|quivering|shaking)\s+(leaves?|trees?|branches?)\b"
        ],
        "sound_folder": "triggers/wind",
        "priority": 1
    },
    
    "thunder_lightning": {
        "patterns": [
            r"\b(thunder|lightning|bolt|flash|strike|crack|boom|rumble|roll|crash)\b",
            r"\b(thunder|lightning)\s+(cracking|rolling|rumbling|booming|crashing|striking|flashing|roaring)\b",
            r"\b(cracking|rolling|rumbling|booming|crashing|striking|flashing|roaring)\s+(thunder|lightning)\b",
            r"\b(distant|close|nearby|far)\s+(thunder|lightning)\b"
        ],
        "sound_folder": "triggers/thunder",
        "priority": 1
    },
    
    "rain_water": {
        "patterns": [
            r"\b(rain|drizzle|shower|downpour|deluge|sprinkle|mist|drops?)\b",
            r"\b(rain|water)\s+(pattering|drumming|pouring|falling|dripping|splashing|flowing|rushing)\b",
            r"\b(pattering|drumming|pouring|falling|dripping|splashing|flowing|rushing)\s+(rain|water)\b",
            r"\b(river|stream|brook|creek|waterfall|cascade|rapids|waves?|ocean|sea|lake|pond)\b",
            r"\b(water|river|stream)\s+(flowing|rushing|babbling|gurgling|splashing|crashing|roaring)\b",
            r"\b(flowing|rushing|babbling|gurgling|splashing|crashing|roaring)\s+(water|river|stream)\b",
            r"\b(dripping|splashing|splatter|splash|drip|drop)\s+(water|rain)\b"
        ],
        "sound_folder": "triggers/water",
        "priority": 1
    },
    
    "storm_weather": {
        "patterns": [
            r"\b(storm|tempest|squall|blizzard|hail|sleet|cyclone|hurricane|typhoon)\b",
            r"\b(raging|fierce|violent|wild|terrifying|howling|roaring)\s+(storm|tempest)\b",
            r"\b(storm|tempest)\s+(raging|fierce|violent|wild|terrifying|howling|roaring)\b"
        ],
        "sound_folder": "triggers/storm",
        "priority": 1
    },
    
    # FIRE & HEAT SOUNDS
    "fire_sounds": {
        "patterns": [
            r"\b(fire|flame|blaze|inferno|bonfire|hearth|embers?|ashes?|sparks?)\b",
            r"\b(fire|flame|embers?)\s+(crackling|roaring|burning|flickering|dancing|leaping|devouring)\b",
            r"\b(crackling|roaring|burning|flickering|dancing|leaping|devouring)\s+(fire|flame|embers?)\b",
            r"\b(wood|log|branch|twig)\s+(burning|crackling|popping|snapping)\b",
            r"\b(burning|crackling|popping|snapping)\s+(wood|log|branch|twig)\b",
            r"\b(smoke|smoldering|smoldering)\s+(rising|curling|billowing|drifting)\b"
        ],
        "sound_folder": "triggers/fire",
        "priority": 1
    },
    
    # FOOTSTEPS & MOVEMENT
    "footsteps": {
        "patterns": [
            r"\b(footsteps?|footfall|tread|step|stomp|tramp|march|stride|pace)\b",
            r"\b(heavy|light|soft|loud|distant|approaching|retreating|echoing)\s+(footsteps?|footfall)\b",
            r"\b(footsteps?|footfall)\s+(heavy|light|soft|loud|distant|approaching|retreating|echoing)\b",
            r"\b(boots?|shoes?|slippers?|sandals?)\s+(on|against|against)\s+(stone|wood|metal|cobblestone|gravel|dirt)\b",
            r"\b(walking|running|marching|striding|pacing|tramping|stomping)\b",
            r"\b(creaking|squeaking|groaning)\s+(floorboards?|stairs?|steps?)\b"
        ],
        "sound_folder": "triggers/footsteps",
        "priority": 2
    },
    
    "horse_movement": {
        "patterns": [
            r"\b(horse|mare|stallion|pony|steed|mount)\b",
            r"\b(hooves?|hoofbeats?)\s+(on|against|against)\s+(cobblestone|stone|dirt|grass|road)\b",
            r"\b(horse|mare|stallion)\s+(galloping|trotting|cantering|walking|running|charging)\b",
            r"\b(galloping|trotting|cantering|walking|running|charging)\s+(horse|mare|stallion)\b",
            r"\b(neighing|whinnying|snorting|breathing)\s+(horse|mare|stallion)\b"
        ],
        "sound_folder": "triggers/horse",
        "priority": 2
    },
    
    "carriage_wheels": {
        "patterns": [
            r"\b(carriage|wagon|cart|coach|chariot|buggy)\b",
            r"\b(wheels?|axles?)\s+(turning|rolling|creaking|squeaking|rumbling)\b",
            r"\b(turning|rolling|creaking|squeaking|rumbling)\s+(wheels?|axles?)\b",
            r"\b(carriage|wagon|cart)\s+(rolling|rumbling|creaking|approaching|passing)\b"
        ],
        "sound_folder": "triggers/carriage",
        "priority": 2
    },
    
    # COMBAT & WEAPONS
    "sword_combat": {
        "patterns": [
            r"\b(sword|blade|steel|metal)\s+(clashing|ringing|singing|whistling|swishing|slicing)\b",
            r"\b(clashing|ringing|singing|whistling|swishing|slicing)\s+(sword|blade|steel|metal)\b",
            r"\b(swords?|blades?)\s+(crossing|meeting|striking|parrying|blocking)\b",
            r"\b(steel|metal)\s+(against|meeting|striking)\s+(steel|metal)\b"
        ],
        "sound_folder": "triggers/sword",
        "priority": 3
    },
    
    "armor_combat": {
        "patterns": [
            r"\b(armor|mail|plate|chainmail|breastplate|helmet|shield)\b",
            r"\b(armor|mail|plate)\s+(clanking|rattling|jingling|creaking|scraping)\b",
            r"\b(clanking|rattling|jingling|creaking|scraping)\s+(armor|mail|plate)\b",
            r"\b(metal|steel)\s+(clanking|rattling|jingling)\b"
        ],
        "sound_folder": "triggers/armor",
        "priority": 3
    },
    
    "battle_combat": {
        "patterns": [
            r"\b(battle|combat|fight|war|conflict|skirmish|clash|melee)\b",
            r"\b(raging|fierce|terrifying|epic|heroic|desperate|bloody)\s+(battle|combat|fight)\b",
            r"\b(battle|combat|fight)\s+(raging|fierce|terrifying|epic|heroic|desperate|bloody)\b",
            r"\b(arrows?|bolts?|missiles?)\s+(whistling|flying|striking|hitting)\b",
            r"\b(bowstring|string)\s+(twanging|snapping|releasing)\b"
        ],
        "sound_folder": "triggers/battle",
        "priority": 3
    },
    
    # MAGIC & SUPERNATURAL
    "magic_spells": {
        "patterns": [
            r"\b(magic|spell|enchantment|sorcery|wizardry|incantation|ritual)\b",
            r"\b(magic|spell)\s+(crackling|humming|whispering|singing|roaring|exploding)\b",
            r"\b(crackling|humming|whispering|singing|roaring|exploding)\s+(magic|spell)\b",
            r"\b(wizard|mage|sorcerer|warlock|witch|enchanter)\s+(casting|chanting|muttering)\b",
            r"\b(casting|chanting|muttering)\s+(spell|magic|incantation)\b"
        ],
        "sound_folder": "triggers/magic",
        "priority": 2
    },
    
    "supernatural": {
        "patterns": [
            r"\b(ghost|spirit|phantom|specter|apparition|wraith|shade)\b",
            r"\b(ghost|spirit|phantom)\s+(whispering|moaning|wailing|sighing|laughing|crying)\b",
            r"\b(whispering|moaning|wailing|sighing|laughing|crying)\s+(ghost|spirit|phantom)\b",
            r"\b(ethereal|otherworldly|supernatural|mystical)\s+(whispers?|voices?|sounds?)\b"
        ],
        "sound_folder": "triggers/supernatural",
        "priority": 2
    },
    
    # ANIMALS & CREATURES
    "birds": {
        "patterns": [
            r"\b(bird|owl|eagle|hawk|raven|crow|sparrow|finch|robin|wren)\b",
            r"\b(bird|owl|eagle)\s+(chirping|singing|calling|crying|hooting|screeching|whistling)\b",
            r"\b(chirping|singing|calling|crying|hooting|screeching|whistling)\s+(bird|owl|eagle)\b",
            r"\b(wings?)\s+(flapping|beating|rustling|whirring)\b"
        ],
        "sound_folder": "triggers/birds",
        "priority": 2
    },
    
    "wolves_dogs": {
        "patterns": [
            r"\b(wolf|wolves|dog|hound|puppy|canine)\b",
            r"\b(wolf|dog)\s+(howling|barking|growling|whining|yelping|snarling)\b",
            r"\b(howling|barking|growling|whining|yelping|snarling)\s+(wolf|dog)\b",
            r"\b(pack|wolves|dogs)\s+(howling|barking|growling)\b"
        ],
        "sound_folder": "triggers/wolves",
        "priority": 2
    },
    
    "other_animals": {
        "patterns": [
            r"\b(cat|kitten|feline)\s+(purring|meowing|hissing|growling|yowling)\b",
            r"\b(purring|meowing|hissing|growling|yowling)\s+(cat|kitten|feline)\b",
            r"\b(snake|serpent)\s+(hissing|slithering|coiling|striking)\b",
            r"\b(bear|bear)\s+(roaring|growling|snarling|charging)\b",
            r"\b(lion|tiger|leopard)\s+(roaring|growling|snarling|prowling)\b"
        ],
        "sound_folder": "triggers/animals",
        "priority": 2
    },
    
    # HUMAN SOUNDS
    "human_voices": {
        "patterns": [
            r"\b(scream|shriek|yell|shout|cry|wail|sob|weep|laugh|giggle|chuckle)\b",
            r"\b(desperate|piercing|bloodcurdling|terrifying|anguished)\s+(scream|shriek|cry)\b",
            r"\b(raucous|hearty|booming|soft|gentle|hushed)\s+(laugh|laughter)\b",
            r"\b(whisper|murmur|mutter|mumble|grumble|groan|sigh)\b",
            r"\b(soft|gentle|hushed|urgent|desperate)\s+(whisper|murmur)\b"
        ],
        "sound_folder": "triggers/human_voices",
        "priority": 2
    },
    
    "human_body": {
        "patterns": [
            r"\b(heartbeat|heart|pulse)\s+(racing|pounding|thumping|beating|hammering)\b",
            r"\b(racing|pounding|thumping|beating|hammering)\s+(heartbeat|heart|pulse)\b",
            r"\b(breath|breathing)\s+(ragged|labored|heavy|shallow|quick|slow)\b",
            r"\b(ragged|labored|heavy|shallow|quick|slow)\s+(breath|breathing)\b",
            r"\b(footsteps?|footfall)\s+(approaching|retreating|echoing|distant)\b"
        ],
        "sound_folder": "triggers/human_body",
        "priority": 2
    },
    
    # MECHANICAL & OBJECTS
    "doors_hinges": {
        "patterns": [
            r"\b(door|gate|portal|entrance)\b",
            r"\b(door|gate)\s+(slamming|banging|knocking|creaking|squeaking|opening|closing)\b",
            r"\b(slamming|banging|knocking|creaking|squeaking|opening|closing)\s+(door|gate)\b",
            r"\b(hinges?)\s+(rattling|creaking|squeaking|groaning|protesting)\b",
            r"\b(rattling|creaking|squeaking|groaning|protesting)\s+(hinges?)\b",
            r"\b(lock|latch|bolt)\s+(clicking|snapping|sliding|turning)\b"
        ],
        "sound_folder": "triggers/doors",
        "priority": 2
    },
    
    "bells_clocks": {
        "patterns": [
            r"\b(bell|chime|gong|toll|ring)\b",
            r"\b(bell|chime)\s+(tolling|chiming|ringing|pealing|clanging|jingling)\b",
            r"\b(tolling|chiming|ringing|pealing|clanging|jingling)\s+(bell|chime)\b",
            r"\b(clock|timepiece)\s+(ticking|chiming|striking|ringing)\b",
            r"\b(ticking|chiming|striking|ringing)\s+(clock|timepiece)\b"
        ],
        "sound_folder": "triggers/bells",
        "priority": 2
    },
    
    "books_pages": {
        "patterns": [
            r"\b(book|tome|volume|manuscript|parchment|scroll)\b",
            r"\b(pages?|leaves?)\s+(turning|rustling|fluttering|flicking|flipping)\b",
            r"\b(turning|rustling|fluttering|flicking|flipping)\s+(pages?|leaves?)\b",
            r"\b(paper|parchment)\s+(rustling|crinkling|tearing|folding)\b"
        ],
        "sound_folder": "triggers/books",
        "priority": 2
    },
    
    # ENVIRONMENTAL & ATMOSPHERIC
    "forest_nature": {
        "patterns": [
            r"\b(forest|woods|grove|thicket|jungle|wilderness)\b",
            r"\b(trees?|branches?|leaves?)\s+(rustling|swaying|creaking|groaning|falling)\b",
            r"\b(rustling|swaying|creaking|groaning|falling)\s+(trees?|branches?|leaves?)\b",
            r"\b(underbrush|bushes?|shrubs?)\s+(rustling|crackling|moving)\b"
        ],
        "sound_folder": "triggers/forest",
        "priority": 2
    },
    
    "cave_underground": {
        "patterns": [
            r"\b(cave|cavern|tunnel|passage|grotto|chamber|dungeon)\b",
            r"\b(echoing|resonating|reverberating)\s+(footsteps?|voices?|sounds?)\b",
            r"\b(dripping|trickling|flowing)\s+(water|liquid)\b",
            r"\b(stalactites?|stalagmites?)\s+(dripping|forming)\b"
        ],
        "sound_folder": "triggers/cave",
        "priority": 2
    },
    
    "castle_architecture": {
        "patterns": [
            r"\b(castle|tower|fortress|citadel|palace|manor|keep)\b",
            r"\b(stones?|walls?|towers?)\s+(creaking|groaning|settling|shifting)\b",
            r"\b(creaking|groaning|settling|shifting)\s+(stones?|walls?|towers?)\b",
            r"\b(drawbridge|portcullis|gate)\s+(lowering|raising|clanking)\b"
        ],
        "sound_folder": "triggers/castle",
        "priority": 2
    }
}

def get_random_sound_from_folder(folder_path: str) -> str:
    """
    Get a random sound file from a trigger folder.
    
    Args:
        folder_path: Path to the trigger folder (e.g., "triggers/footsteps")
        
    Returns:
        Full path to a random sound file, or default if folder doesn't exist
    """
    import os
    import random
    
    # Base path for sound files (adjust as needed)
    base_path = "mobile/app/sounds"  # or wherever your sounds are stored
    
    # Construct full folder path
    full_folder_path = os.path.join(base_path, folder_path)
    
    # Check if folder exists
    if not os.path.exists(full_folder_path):
        # Return default sound if folder doesn't exist
        return f"{folder_path}/default.mp3"
    
    # Get all sound files in the folder
    sound_files = []
    for file in os.listdir(full_folder_path):
        if file.lower().endswith(('.mp3', '.wav', '.ogg')):
            sound_files.append(file)
    
    # If no sound files found, return default
    if not sound_files:
        return f"{folder_path}/default.mp3"
    
    # Return random sound file
    random_sound = random.choice(sound_files)
    return f"{folder_path}/{random_sound}"

def find_trigger_words(text: str) -> List[Dict]:
    """
    Advanced regex-based trigger word detection with folder-based sound pools.
    
    Args:
        text: The text to analyze
        
    Returns:
        List of dictionaries with word/phrase, sound, and timing information
    """
    if not text:
        return []
    
    text_lower = text.lower()
    trigger_words = []
    
    # Calculate estimated reading time (words per minute)
    words = text.split()
    estimated_reading_time_minutes = len(words) / 200.0  # 200 words per minute
    estimated_reading_time_seconds = estimated_reading_time_minutes * 60
    
    # Track used positions to avoid overlapping triggers
    used_positions = set()
    
    # Sort patterns by priority (higher priority first)
    sorted_patterns = sorted(TRIGGER_PATTERNS.items(), key=lambda x: x[1]["priority"], reverse=True)
    
    for pattern_name, pattern_data in sorted_patterns:
        for pattern in pattern_data["patterns"]:
            # Find all matches for this pattern
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            
            for match in matches:
                start_pos = match.start()
                end_pos = match.end()
                
                # Check if this position overlaps with already used positions
                position_overlaps = any(
                    start_pos < used_end and end_pos > used_start
                    for used_start, used_end in used_positions
                )
                
                if not position_overlaps:
                    # Calculate timing based on position in text
                    progress_ratio = start_pos / len(text)
                    timing = progress_ratio * estimated_reading_time_seconds
                    
                    # Get random sound from folder
                    selected_sound = get_random_sound_from_folder(pattern_data["sound_folder"])
                    
                    trigger_words.append({
                        "word": match.group(),
                        "sound": selected_sound,
                        "timing": timing,
                        "position": start_pos,
                        "type": "regex_pattern",
                        "pattern_name": pattern_name,
                        "folder_path": pattern_data["sound_folder"]
                    })
                    
                    # Mark this position as used
                    used_positions.add((start_pos, end_pos))
    
    # Sort by timing
    trigger_words.sort(key=lambda x: x["timing"])
    
    return trigger_words 