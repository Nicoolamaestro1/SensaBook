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
        
        # Enhanced context patterns for narrative flow detection
        self.context_patterns = {
            "intensifiers": ["very", "extremely", "incredibly", "absolutely", "completely", "utterly"],
            "diminishers": ["slightly", "somewhat", "a bit", "kind of", "sort of", "rather"],
            "negation": ["not", "never", "no", "none", "neither", "nor", "doesn't", "isn't", "wasn't"],
            "temporal": ["suddenly", "gradually", "slowly", "quickly", "immediately", "eventually"],
            "spatial": ["near", "far", "above", "below", "inside", "outside", "around", "through"]
        }

    def analyze_emotion(self, text: str) -> EmotionResult:
        """Analyze the emotional content of text with enhanced context analysis."""
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
        
        # Calculate emotion scores with context enhancement
        emotion_scores = defaultdict(float)
        found_keywords = []
        
        # Enhanced keyword analysis with context weighting
        for emotion_type, keywords in self.emotion_keywords.items():
            for keyword, weight in keywords.items():
                if keyword in text:
                    # Apply context-based weight adjustment
                    adjusted_weight = self._adjust_weight_by_context(text, keyword, weight)
                    emotion_scores[emotion_type.value] += adjusted_weight
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
        
        # Enhanced context extraction with narrative flow
        context = self._extract_enhanced_context(text)
        
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
    
    def _adjust_weight_by_context(self, text: str, keyword: str, base_weight: float) -> float:
        """Adjust emotion keyword weight based on surrounding context."""
        adjusted_weight = base_weight
        
        # Find the keyword position
        keyword_pos = text.find(keyword)
        if keyword_pos == -1:
            return base_weight
        
        # Get surrounding context (50 characters before and after)
        start = max(0, keyword_pos - 50)
        end = min(len(text), keyword_pos + len(keyword) + 50)
        context_window = text[start:end]
        
        # Check for intensifiers (increase weight)
        for intensifier in self.context_patterns["intensifiers"]:
            if intensifier in context_window:
                adjusted_weight *= 1.3
                break
        
        # Check for diminishers (decrease weight)
        for diminisher in self.context_patterns["diminishers"]:
            if diminisher in context_window:
                adjusted_weight *= 0.7
                break
        
        # Check for negation (invert emotion or reduce weight)
        for negation in self.context_patterns["negation"]:
            if negation in context_window:
                adjusted_weight *= 0.5  # Reduce weight for negated emotions
                break
        
        # Check for temporal context (sudden changes get higher weight)
        for temporal in self.context_patterns["temporal"]:
            if temporal in context_window:
                if temporal in ["suddenly", "immediately"]:
                    adjusted_weight *= 1.2
                break
        
        return adjusted_weight
    
    def _extract_enhanced_context(self, text: str) -> str:
        """Extract enhanced context with narrative flow detection."""
        sentences = text.split('.')
        if not sentences:
            return text[:100]
        
        # Get the first sentence as base context
        base_context = sentences[0].strip()
        
        # Look for narrative flow indicators
        flow_indicators = []
        
        # Check for emotional progression
        if len(sentences) > 1:
            second_sentence = sentences[1].strip()
            if any(word in second_sentence for word in ["but", "however", "suddenly", "then"]):
                flow_indicators.append("emotional_shift")
        
        # Check for intensity changes
        if any(word in text for word in self.context_patterns["intensifiers"]):
            flow_indicators.append("intensifying")
        
        # Check for spatial context
        spatial_context = []
        for spatial_word in self.context_patterns["spatial"]:
            if spatial_word in text:
                spatial_context.append(spatial_word)
        
        # Build enhanced context
        context_parts = [base_context]
        
        if flow_indicators:
            context_parts.append(f"Flow: {', '.join(flow_indicators)}")
        
        if spatial_context:
            context_parts.append(f"Spatial: {', '.join(spatial_context[:2])}")
        
        return " | ".join(context_parts)

    def analyze_emotional_progression(self, text: str, segment_length: int = 100) -> 'EmotionalProgressionResult':
        """
        Analyze how emotions change throughout a longer text passage.
        
        Args:
            text: The text to analyze
            segment_length: Number of characters per segment for analysis
            
        Returns:
            EmotionalProgressionResult with progression analysis
        """
        # Split text into segments
        segments = self._segment_text(text, segment_length)
        
        # Analyze each segment
        segment_emotions = []
        for i, segment in enumerate(segments):
            emotion_result = self.analyze_emotion(segment)
            segment_emotions.append({
                'segment_index': i,
                'text': segment,
                'emotion': emotion_result.primary_emotion,
                'intensity': emotion_result.intensity,
                'confidence': emotion_result.confidence,
                'keywords': emotion_result.keywords
            })
        
        # Analyze progression patterns
        progression_patterns = self._identify_progression_patterns(segment_emotions)
        
        # Calculate emotional arc metrics
        arc_metrics = self._calculate_emotional_arc(segment_emotions)
        
        return EmotionalProgressionResult(
            segments=segment_emotions,
            progression_patterns=progression_patterns,
            arc_metrics=arc_metrics,
            overall_trend=self._determine_overall_trend(segment_emotions)
        )
    
    def _segment_text(self, text: str, segment_length: int) -> List[str]:
        """Split text into overlapping segments for analysis."""
        segments = []
        start = 0
        
        while start < len(text):
            end = start + segment_length
            
            # Try to break at sentence boundaries
            if end < len(text):
                # Look for sentence endings
                for i in range(end, min(end + 50, len(text))):
                    if text[i] in '.!?':
                        end = i + 1
                        break
            
            segment = text[start:end].strip()
            if segment:
                segments.append(segment)
            
            # Move start position (with some overlap for continuity)
            start = end - 20  # 20 character overlap
            
            if start >= len(text):
                break
        
        return segments
    
    def _identify_progression_patterns(self, segment_emotions: List[Dict]) -> Dict[str, any]:
        """Identify patterns in emotional progression."""
        patterns = {
            'emotional_shifts': [],
            'intensity_fluctuations': [],
            'emotional_stability': 0.0,
            'recurring_emotions': [],
            'emotional_contrast': 0.0
        }
        
        if len(segment_emotions) < 2:
            return patterns
        
        # Track emotional shifts
        for i in range(1, len(segment_emotions)):
            prev_emotion = segment_emotions[i-1]['emotion']
            curr_emotion = segment_emotions[i]['emotion']
            
            if prev_emotion != curr_emotion:
                patterns['emotional_shifts'].append({
                    'position': i,
                    'from': prev_emotion.value,
                    'to': curr_emotion.value,
                    'shift_type': self._classify_shift_type(prev_emotion, curr_emotion)
                })
        
        # Track intensity fluctuations
        intensities = [seg['intensity'] for seg in segment_emotions]
        patterns['intensity_fluctuations'] = self._analyze_intensity_changes(intensities)
        
        # Calculate emotional stability (lower variance = more stable)
        intensity_variance = self._calculate_variance(intensities)
        patterns['emotional_stability'] = max(0, 1 - intensity_variance)
        
        # Find recurring emotions
        emotion_counts = Counter([seg['emotion'].value for seg in segment_emotions])
        patterns['recurring_emotions'] = [
            {'emotion': emotion, 'count': count}
            for emotion, count in emotion_counts.most_common(3)
        ]
        
        # Calculate emotional contrast (difference between highest and lowest intensity)
        patterns['emotional_contrast'] = max(intensities) - min(intensities)
        
        return patterns
    
    def _classify_shift_type(self, from_emotion: EmotionType, to_emotion: EmotionType) -> str:
        """Classify the type of emotional shift."""
        # Define emotional opposites
        opposites = {
            EmotionType.JOY: EmotionType.SADNESS,
            EmotionType.SADNESS: EmotionType.JOY,
            EmotionType.ANGER: EmotionType.FEAR,
            EmotionType.FEAR: EmotionType.ANGER,
            EmotionType.SURPRISE: EmotionType.DISGUST,
            EmotionType.DISGUST: EmotionType.SURPRISE
        }
        
        if opposites.get(from_emotion) == to_emotion:
            return "opposite_shift"
        elif from_emotion == to_emotion:
            return "no_change"
        else:
            return "neutral_shift"
    
    def _analyze_intensity_changes(self, intensities: List[float]) -> List[Dict]:
        """Analyze how intensity changes between segments."""
        changes = []
        
        for i in range(1, len(intensities)):
            change = intensities[i] - intensities[i-1]
            changes.append({
                'position': i,
                'change': change,
                'change_type': 'increase' if change > 0.1 else 'decrease' if change < -0.1 else 'stable',
                'magnitude': abs(change)
            })
        
        return changes
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of a list of values."""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        squared_diff_sum = sum((x - mean) ** 2 for x in values)
        return squared_diff_sum / (len(values) - 1)
    
    def _calculate_emotional_arc(self, segment_emotions: List[Dict]) -> Dict[str, any]:
        """Calculate metrics describing the emotional arc."""
        if not segment_emotions:
            return {}
        
        intensities = [seg['intensity'] for seg in segment_emotions]
        
        arc_metrics = {
            'peak_intensity': max(intensities),
            'valley_intensity': min(intensities),
            'average_intensity': sum(intensities) / len(intensities),
            'arc_shape': self._classify_arc_shape(intensities),
            'climax_position': intensities.index(max(intensities)),
            'resolution_trend': self._analyze_resolution_trend(intensities)
        }
        
        return arc_metrics
    
    def _classify_arc_shape(self, intensities: List[float]) -> str:
        """Classify the shape of the emotional arc."""
        if len(intensities) < 3:
            return "insufficient_data"
        
        # Simple arc classification based on intensity pattern
        first_third = intensities[:len(intensities)//3]
        middle_third = intensities[len(intensities)//3:2*len(intensities)//3]
        last_third = intensities[2*len(intensities)//3:]
        
        first_avg = sum(first_third) / len(first_third)
        middle_avg = sum(middle_third) / len(middle_third)
        last_avg = sum(last_third) / len(last_third)
        
        if middle_avg > first_avg and middle_avg > last_avg:
            return "climactic_rise"  # Builds to climax, then falls
        elif first_avg > middle_avg and first_avg > last_avg:
            return "immediate_impact"  # Starts high, then decreases
        elif last_avg > first_avg and last_avg > middle_avg:
            return "building_tension"  # Builds throughout
        elif abs(first_avg - last_avg) < 0.1:
            return "stable_arc"  # Relatively stable
        else:
            return "complex_arc"  # Complex pattern
    
    def _analyze_resolution_trend(self, intensities: List[float]) -> str:
        """Analyze how the emotional intensity resolves at the end."""
        if len(intensities) < 2:
            return "insufficient_data"
        
        last_quarter = intensities[3*len(intensities)//4:]
        if not last_quarter:
            return "insufficient_data"
        
        # Check if intensity is decreasing at the end (resolution)
        if len(last_quarter) >= 2:
            end_trend = last_quarter[-1] - last_quarter[-2]
            if end_trend < -0.05:
                return "resolving_down"
            elif end_trend > 0.05:
                return "building_up"
            else:
                return "stable_end"
        
        return "unknown"
    
    def _determine_overall_trend(self, segment_emotions: List[Dict]) -> str:
        """Determine the overall emotional trend of the passage."""
        if len(segment_emotions) < 2:
            return "insufficient_data"
        
        first_half = segment_emotions[:len(segment_emotions)//2]
        second_half = segment_emotions[len(segment_emotions)//2:]
        
        first_avg_intensity = sum(seg['intensity'] for seg in first_half) / len(first_half)
        second_avg_intensity = sum(seg['intensity'] for seg in second_half) / len(second_half)
        
        intensity_diff = second_avg_intensity - first_avg_intensity
        
        if intensity_diff > 0.1:
            return "intensifying"
        elif intensity_diff < -0.1:
            return "decreasing"
        else:
            return "stable"
    
    def generate_progression_soundscape(self, progression_result: 'EmotionalProgressionResult') -> Dict:
        """Generate soundscape recommendations based on emotional progression."""
        soundscape = {
            'overall_theme': self._map_progression_to_soundscape_theme(progression_result.overall_trend),
            'segment_sounds': [],
            'transition_sounds': [],
            'dynamic_elements': {}
        }
        
        # Generate sounds for each segment
        for segment in progression_result.segments:
            segment_sound = {
                'segment_index': segment['segment_index'],
                'base_sound': self._map_emotion_to_soundscape(segment['emotion']),
                'intensity_modifier': self._calculate_intensity_modifier(segment['intensity']),
                'volume': self._calculate_volume(segment['intensity'])
            }
            soundscape['segment_sounds'].append(segment_sound)
        
        # Generate transition sounds for emotional shifts
        for shift in progression_result.progression_patterns['emotional_shifts']:
            transition_sound = self._generate_transition_sound(shift)
            soundscape['transition_sounds'].append(transition_sound)
        
        # Add dynamic elements based on arc shape
        soundscape['dynamic_elements'] = self._generate_dynamic_elements(progression_result.arc_metrics)
        
        return soundscape
    
    def _map_progression_to_soundscape_theme(self, trend: str) -> str:
        """Map emotional progression trend to soundscape theme."""
        theme_mapping = {
            'intensifying': 'building_tension',
            'decreasing': 'gentle_resolution',
            'stable': 'consistent_atmosphere'
        }
        return theme_mapping.get(trend, 'adaptive_atmosphere')
    
    def _calculate_intensity_modifier(self, intensity: float) -> str:
        """Calculate how to modify sound based on intensity."""
        if intensity > 0.8:
            return 'high_energy'
        elif intensity > 0.5:
            return 'moderate_energy'
        else:
            return 'low_energy'
    
    def _generate_transition_sound(self, shift: Dict) -> Dict:
        """Generate sound recommendation for emotional transition."""
        transition_sounds = {
            'opposite_shift': 'sudden_impact',
            'neutral_shift': 'gentle_transition',
            'no_change': 'continuity_sound'
        }
        
        return {
            'position': shift['position'],
            'sound_type': transition_sounds.get(shift['shift_type'], 'default_transition'),
            'volume': 0.7,
            'fade_in': 0.5,
            'fade_out': 0.5
        }
    
    def _generate_dynamic_elements(self, arc_metrics: Dict) -> Dict:
        """Generate dynamic sound elements based on emotional arc metrics."""
        dynamic_elements = {}
        
        # Map arc shape to dynamic elements
        arc_shape = arc_metrics.get('arc_shape', 'unknown')
        
        if arc_shape == 'climactic_rise':
            dynamic_elements['build_up'] = 'gradual_intensity_increase'
            dynamic_elements['climax'] = 'sudden_impact'
            dynamic_elements['resolution'] = 'gentle_fade'
        elif arc_shape == 'immediate_impact':
            dynamic_elements['opening'] = 'sudden_impact'
            dynamic_elements['sustain'] = 'maintained_intensity'
            dynamic_elements['ending'] = 'gradual_decline'
        elif arc_shape == 'building_tension':
            dynamic_elements['tension_build'] = 'slow_crescendo'
            dynamic_elements['release'] = 'sudden_release'
        elif arc_shape == 'stable_arc':
            dynamic_elements['ambient'] = 'consistent_atmosphere'
            dynamic_elements['variation'] = 'subtle_changes'
        elif arc_shape == 'complex_arc':
            dynamic_elements['layers'] = 'multiple_sound_layers'
            dynamic_elements['transitions'] = 'smooth_transitions'
            dynamic_elements['dynamics'] = 'variable_intensity'
        
        return dynamic_elements

    def analyze_narrative_structure(self, text: str) -> 'NarrativeStructureResult':
        """
        Analyze the narrative structure of the text to identify story elements.
        
        Args:
            text: The text to analyze for narrative structure
            
        Returns:
            NarrativeStructureResult containing narrative analysis
        """
        if not text:
            return NarrativeStructureResult(
                story_elements=[],
                character_development=[],
                plot_progression={},
                narrative_pacing={},
                conflict_resolution={},
                setting_details={},
                overall_structure="unknown"
            )
        
        # Analyze story elements
        story_elements = self._identify_story_elements(text)
        
        # Analyze character development
        character_development = self._analyze_character_development(text)
        
        # Analyze plot progression
        plot_progression = self._analyze_plot_progression(text)
        
        # Analyze narrative pacing
        narrative_pacing = self._analyze_narrative_pacing(text)
        
        # Analyze conflict and resolution
        conflict_resolution = self._analyze_conflict_resolution(text)
        
        # Analyze setting details
        setting_details = self._analyze_setting_details(text)
        
        # Determine overall structure
        overall_structure = self._classify_narrative_structure(
            story_elements, plot_progression, narrative_pacing
        )
        
        return NarrativeStructureResult(
            story_elements=story_elements,
            character_development=character_development,
            plot_progression=plot_progression,
            narrative_pacing=narrative_pacing,
            conflict_resolution=conflict_resolution,
            setting_details=setting_details,
            overall_structure=overall_structure
        )

    def _identify_story_elements(self, text: str) -> List[Dict]:
        """Identify key story elements in the text."""
        story_elements = []
        text_lower = text.lower()
        
        # Define story element patterns
        story_patterns = {
            'exposition': [
                r'\b(introduc|present|establish|begin|start)\w*\b',
                r'\b(setting|background|context|situation)\b',
                r'\b(once|long ago|in the beginning|at first)\b'
            ],
            'rising_action': [
                r'\b(then|next|suddenly|however|but|meanwhile)\b',
                r'\b(problem|challenge|difficulty|obstacle|conflict)\b',
                r'\b(tension|suspense|build|increase|grow)\b'
            ],
            'climax': [
                r'\b(finally|at last|the moment|peak|highest)\b',
                r'\b(explosion|burst|breakthrough|realization)\b',
                r'\b(critical|decisive|pivotal|turning point)\b'
            ],
            'falling_action': [
                r'\b(after|following|consequently|as a result)\b',
                r'\b(calm|settle|resolve|wind down)\b',
                r'\b(conclusion|ending|final|last)\b'
            ],
            'resolution': [
                r'\b(resolve|solve|fix|heal|reconcile)\b',
                r'\b(peace|harmony|understanding|acceptance)\b',
                r'\b(learn|grow|change|transform)\b'
            ]
        }
        
        for element_type, patterns in story_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    # Get context around the match
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end].strip()
                    
                    story_elements.append({
                        'type': element_type,
                        'keyword': match.group(),
                        'position': match.start(),
                        'context': context,
                        'confidence': self._calculate_story_element_confidence(context, element_type)
                    })
        
        # Remove duplicates and sort by position
        unique_elements = []
        seen_positions = set()
        for element in sorted(story_elements, key=lambda x: x['position']):
            if element['position'] not in seen_positions:
                unique_elements.append(element)
                seen_positions.add(element['position'])
        
        return unique_elements

    def _analyze_character_development(self, text: str) -> List[Dict]:
        """Analyze character development and interactions."""
        character_development = []
        text_lower = text.lower()
        
        # Character-related patterns
        character_patterns = {
            'character_introduction': [
                r'\b(character|person|man|woman|boy|girl|child)\b',
                r'\b(name|called|known as|referred to as)\b',
                r'\b(appearance|looked|appeared|seemed)\b'
            ],
            'character_growth': [
                r'\b(learn|grow|change|develop|evolve|transform)\b',
                r'\b(realize|understand|discover|find out)\b',
                r'\b(overcome|face|deal with|handle)\b'
            ],
            'character_relationships': [
                r'\b(friend|enemy|ally|rival|partner|companion)\b',
                r'\b(love|hate|trust|betray|support|oppose)\b',
                r'\b(together|apart|separate|unite|divide)\b'
            ],
            'character_conflict': [
                r'\b(struggle|fight|argue|disagree|conflict)\b',
                r'\b(anger|fear|sadness|joy|surprise)\b',
                r'\b(decision|choice|dilemma|problem)\b'
            ]
        }
        
        for development_type, patterns in character_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    # Get context around the match
                    start = max(0, match.start() - 60)
                    end = min(len(text), match.end() + 60)
                    context = text[start:end].strip()
                    
                    character_development.append({
                        'type': development_type,
                        'keyword': match.group(),
                        'position': match.start(),
                        'context': context,
                        'intensity': self._calculate_character_intensity(context)
                    })
        
        return character_development

    def _analyze_plot_progression(self, text: str) -> Dict[str, any]:
        """Analyze the progression of the plot."""
        plot_progression = {
            'plot_points': [],
            'story_arc': 'unknown',
            'pacing_indicators': [],
            'tension_levels': []
        }
        
        text_lower = text.lower()
        
        # Plot progression indicators
        progression_indicators = [
            r'\b(begin|start|commence|initiate)\b',
            r'\b(develop|progress|advance|move forward)\b',
            r'\b(complicate|intensify|escalate|heighten)\b',
            r'\b(resolve|conclude|end|finish)\b'
        ]
        
        for i, pattern in enumerate(progression_indicators):
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                plot_progression['plot_points'].append({
                    'stage': ['beginning', 'development', 'complication', 'resolution'][i],
                    'position': match.start(),
                    'keyword': match.group()
                })
        
        # Determine story arc based on plot points
        if len(plot_progression['plot_points']) >= 3:
            plot_progression['story_arc'] = 'complete'
        elif len(plot_progression['plot_points']) >= 2:
            plot_progression['story_arc'] = 'partial'
        else:
            plot_progression['story_arc'] = 'minimal'
        
        return plot_progression

    def _analyze_narrative_pacing(self, text: str) -> Dict[str, any]:
        """Analyze the pacing and rhythm of the narrative."""
        narrative_pacing = {
            'pace_indicators': [],
            'rhythm_patterns': [],
            'temporal_markers': [],
            'overall_pace': 'moderate'
        }
        
        text_lower = text.lower()
        
        # Pacing indicators
        fast_pace = [
            r'\b(suddenly|quickly|rapidly|swiftly|immediately)\b',
            r'\b(urgent|hurry|rush|fast|quick)\b',
            r'\b(explosion|burst|crash|bang|flash)\b'
        ]
        
        slow_pace = [
            r'\b(gradually|slowly|gently|carefully|patiently)\b',
            r'\b(calm|peaceful|tranquil|serene|quiet)\b',
            r'\b(reflect|contemplate|consider|think|ponder)\b'
        ]
        
        # Count pacing indicators
        fast_count = sum(len(re.findall(pattern, text_lower, re.IGNORECASE)) for pattern in fast_pace)
        slow_count = sum(len(re.findall(pattern, text_lower, re.IGNORECASE)) for pattern in slow_pace)
        
        # Determine overall pace
        if fast_count > slow_count * 2:
            narrative_pacing['overall_pace'] = 'fast'
        elif slow_count > fast_count * 2:
            narrative_pacing['overall_pace'] = 'slow'
        else:
            narrative_pacing['overall_pace'] = 'moderate'
        
        # Add pace indicators to the result
        for pattern in fast_pace + slow_pace:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                narrative_pacing['pace_indicators'].append({
                    'type': 'fast' if pattern in fast_pace else 'slow',
                    'keyword': match.group(),
                    'position': match.start()
                })
        
        return narrative_pacing

    def _analyze_conflict_resolution(self, text: str) -> Dict[str, any]:
        """Analyze conflict and resolution patterns."""
        conflict_resolution = {
            'conflicts': [],
            'resolutions': [],
            'tension_arc': 'unknown',
            'resolution_type': 'unknown'
        }
        
        text_lower = text.lower()
        
        # Conflict patterns
        conflict_patterns = [
            r'\b(problem|issue|trouble|difficulty|challenge)\b',
            r'\b(conflict|dispute|argument|fight|battle)\b',
            r'\b(obstacle|barrier|hurdle|impediment|block)\b',
            r'\b(danger|threat|risk|peril|hazard)\b'
        ]
        
        # Resolution patterns
        resolution_patterns = [
            r'\b(solve|resolve|fix|repair|heal)\b',
            r'\b(overcome|defeat|conquer|triumph|succeed)\b',
            r'\b(understand|realize|discover|learn|grow)\b',
            r'\b(peace|harmony|agreement|compromise|reconciliation)\b'
        ]
        
        # Find conflicts
        for pattern in conflict_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                conflict_resolution['conflicts'].append({
                    'keyword': match.group(),
                    'position': match.start(),
                    'type': self._classify_conflict_type(match.group())
                })
        
        # Find resolutions
        for pattern in resolution_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                conflict_resolution['resolutions'].append({
                    'keyword': match.group(),
                    'position': match.start(),
                    'type': self._classify_resolution_type(match.group())
                })
        
        # Determine tension arc
        if conflict_resolution['conflicts'] and conflict_resolution['resolutions']:
            conflict_resolution['tension_arc'] = 'complete'
        elif conflict_resolution['conflicts']:
            conflict_resolution['tension_arc'] = 'rising'
        elif conflict_resolution['resolutions']:
            conflict_resolution['tension_arc'] = 'falling'
        else:
            conflict_resolution['tension_arc'] = 'stable'
        
        return conflict_resolution

    def _analyze_setting_details(self, text: str) -> Dict[str, any]:
        """Analyze setting and environmental details."""
        setting_details = {
            'locations': [],
            'time_periods': [],
            'atmospheric_elements': [],
            'environmental_features': []
        }
        
        text_lower = text.lower()
        
        # Location patterns
        location_patterns = [
            r'\b(house|building|room|chamber|hall)\b',
            r'\b(forest|mountain|river|ocean|desert)\b',
            r'\b(city|town|village|castle|palace)\b',
            r'\b(inside|outside|within|beyond|near|far)\b'
        ]
        
        # Time period patterns
        time_patterns = [
            r'\b(morning|noon|afternoon|evening|night)\b',
            r'\b(spring|summer|autumn|winter|season)\b',
            r'\b(ancient|modern|future|past|present)\b',
            r'\b(century|decade|year|month|week|day)\b'
        ]
        
        # Atmospheric patterns
        atmosphere_patterns = [
            r'\b(dark|light|bright|dim|shadow)\b',
            r'\b(warm|cold|hot|cool|temperature)\b',
            r'\b(quiet|loud|silent|noisy|sound)\b',
            r'\b(fresh|stale|clean|dirty|pure)\b'
        ]
        
        # Find locations
        for pattern in location_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                setting_details['locations'].append({
                    'keyword': match.group(),
                    'position': match.start()
                })
        
        # Find time periods
        for pattern in time_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                setting_details['time_periods'].append({
                    'keyword': match.group(),
                    'position': match.start()
                })
        
        # Find atmospheric elements
        for pattern in atmosphere_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                setting_details['atmospheric_elements'].append({
                    'keyword': match.group(),
                    'position': match.start()
                })
        
        return setting_details

    def _classify_narrative_structure(self, story_elements: List[Dict], plot_progression: Dict, narrative_pacing: Dict) -> str:
        """Classify the overall narrative structure."""
        # Count story elements by type
        element_counts = {}
        for element in story_elements:
            element_type = element['type']
            element_counts[element_type] = element_counts.get(element_type, 0) + 1
        
        # Determine structure based on element distribution
        if element_counts.get('exposition', 0) > 0 and element_counts.get('resolution', 0) > 0:
            if element_counts.get('climax', 0) > 0:
                return 'three_act_structure'
            else:
                return 'two_act_structure'
        elif element_counts.get('rising_action', 0) > 0 and element_counts.get('falling_action', 0) > 0:
            return 'dramatic_arc'
        elif narrative_pacing['overall_pace'] == 'fast':
            return 'action_packed'
        elif narrative_pacing['overall_pace'] == 'slow':
            return 'character_driven'
        else:
            return 'balanced_narrative'

    def _calculate_story_element_confidence(self, context: str, element_type: str) -> float:
        """Calculate confidence score for story element detection."""
        # Base confidence
        confidence = 0.5
        
        # Boost confidence based on context relevance
        context_lower = context.lower()
        
        if element_type == 'exposition':
            if any(word in context_lower for word in ['begin', 'start', 'introduce']):
                confidence += 0.3
        elif element_type == 'climax':
            if any(word in context_lower for word in ['peak', 'highest', 'critical']):
                confidence += 0.3
        elif element_type == 'resolution':
            if any(word in context_lower for word in ['end', 'conclude', 'resolve']):
                confidence += 0.3
        
        # Boost confidence for longer context
        if len(context) > 100:
            confidence += 0.1
        
        return min(confidence, 1.0)

    def _calculate_character_intensity(self, context: str) -> float:
        """Calculate the intensity of character development."""
        intensity = 0.5
        context_lower = context.lower()
        
        # Boost intensity for strong emotional words
        strong_emotions = ['love', 'hate', 'fear', 'anger', 'joy', 'sadness']
        for emotion in strong_emotions:
            if emotion in context_lower:
                intensity += 0.2
        
        # Boost intensity for action words
        action_words = ['fight', 'struggle', 'overcome', 'transform', 'grow']
        for word in action_words:
            if word in context_lower:
                intensity += 0.15
        
        return min(intensity, 1.0)

    def _classify_conflict_type(self, keyword: str) -> str:
        """Classify the type of conflict."""
        keyword_lower = keyword.lower()
        
        if any(word in keyword_lower for word in ['fight', 'battle', 'war']):
            return 'physical_conflict'
        elif any(word in keyword_lower for word in ['argument', 'dispute', 'disagreement']):
            return 'verbal_conflict'
        elif any(word in keyword_lower for word in ['problem', 'issue', 'trouble']):
            return 'internal_conflict'
        elif any(word in keyword_lower for word in ['obstacle', 'barrier', 'hurdle']):
            return 'environmental_conflict'
        else:
            return 'general_conflict'

    def _classify_resolution_type(self, keyword: str) -> str:
        """Classify the type of resolution."""
        keyword_lower = keyword.lower()
        
        if any(word in keyword_lower for word in ['solve', 'fix', 'repair']):
            return 'practical_resolution'
        elif any(word in keyword_lower for word in ['overcome', 'defeat', 'conquer']):
            return 'victory_resolution'
        elif any(word in keyword_lower for word in ['understand', 'realize', 'discover']):
            return 'insight_resolution'
        elif any(word in keyword_lower for word in ['peace', 'harmony', 'agreement']):
            return 'reconciliation_resolution'
        else:
            return 'general_resolution'

    def generate_narrative_soundscape(self, narrative_result: 'NarrativeStructureResult') -> Dict:
        """Generate soundscape recommendations based on narrative structure."""
        soundscape = {
            'overall_theme': '',
            'story_element_sounds': {},
            'character_sounds': {},
            'pacing_sounds': {},
            'conflict_sounds': {},
            'setting_sounds': {},
            'dynamic_elements': {}
        }
        
        # Map overall structure to theme
        structure = narrative_result.overall_structure
        if structure == 'three_act_structure':
            soundscape['overall_theme'] = 'epic_journey'
        elif structure == 'dramatic_arc':
            soundscape['overall_theme'] = 'emotional_rollercoaster'
        elif structure == 'action_packed':
            soundscape['overall_theme'] = 'high_energy'
        elif structure == 'character_driven':
            soundscape['overall_theme'] = 'intimate_focus'
        else:
            soundscape['overall_theme'] = 'balanced_narrative'
        
        # Map story elements to sounds
        for element in narrative_result.story_elements:
            element_type = element['type']
            if element_type == 'exposition':
                soundscape['story_element_sounds'][element_type] = 'gentle_introduction'
            elif element_type == 'rising_action':
                soundscape['story_element_sounds'][element_type] = 'building_tension'
            elif element_type == 'climax':
                soundscape['story_element_sounds'][element_type] = 'intense_climax'
            elif element_type == 'falling_action':
                soundscape['story_element_sounds'][element_type] = 'gradual_release'
            elif element_type == 'resolution':
                soundscape['story_element_sounds'][element_type] = 'peaceful_resolution'
        
        # Map character development to sounds
        for development in narrative_result.character_development:
            dev_type = development['type']
            intensity = development['intensity']
            
            if dev_type == 'character_growth':
                soundscape['character_sounds'][dev_type] = 'transformation_music'
            elif dev_type == 'character_conflict':
                soundscape['character_sounds'][dev_type] = 'tension_music'
            elif dev_type == 'character_relationships':
                soundscape['character_sounds'][dev_type] = 'relationship_theme'
        
        # Map pacing to sounds
        pacing = narrative_result.narrative_pacing['overall_pace']
        if pacing == 'fast':
            soundscape['pacing_sounds'] = 'rapid_rhythm'
        elif pacing == 'slow':
            soundscape['pacing_sounds'] = 'slow_ambient'
        else:
            soundscape['pacing_sounds'] = 'moderate_pace'
        
        # Map conflict resolution to sounds
        conflict_arc = narrative_result.conflict_resolution['tension_arc']
        if conflict_arc == 'rising':
            soundscape['conflict_sounds'] = 'building_conflict'
        elif conflict_arc == 'falling':
            soundscape['conflict_sounds'] = 'resolving_conflict'
        elif conflict_arc == 'complete':
            soundscape['conflict_sounds'] = 'conflict_resolution_cycle'
        
        # Map setting to sounds
        if narrative_result.setting_details['locations']:
            soundscape['setting_sounds'] = 'location_ambience'
        if narrative_result.setting_details['atmospheric_elements']:
            soundscape['setting_sounds'] = 'atmospheric_sounds'
        
        return soundscape

# New dataclass for emotional progression results
@dataclass
class EmotionalProgressionResult:
    segments: List[Dict]
    progression_patterns: Dict[str, any]
    arc_metrics: Dict[str, any]
    overall_trend: str

# New dataclass for narrative structure results
@dataclass
class NarrativeStructureResult:
    story_elements: List[Dict]
    character_development: List[Dict]
    plot_progression: Dict[str, any]
    narrative_pacing: Dict[str, any]
    conflict_resolution: Dict[str, any]
    setting_details: Dict[str, any]
    overall_structure: str

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
    Enhanced to provide both character and word positions for frontend synchronization.
    
    Args:
        text: The text to analyze
        
    Returns:
        List of dictionaries with word/phrase, sound, timing, and position information
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
                    
                    # Calculate word position for frontend synchronization
                    word_position = _calculate_word_position(text, start_pos)
                    
                    # Get random sound from folder
                    selected_sound = get_random_sound_from_folder(pattern_data["sound_folder"])
                    
                    trigger_words.append({
                        "word": match.group(),
                        "sound": selected_sound,
                        "timing": timing,
                        "position": start_pos,  # Character position in text
                        "word_position": word_position,  # Word position (0-indexed)
                        "word_count": len(words),  # Total words in text
                        "type": "regex_pattern",
                        "pattern_name": pattern_name,
                        "folder_path": pattern_data["sound_folder"],
                        "context": _get_word_context(text, start_pos, end_pos)  # Surrounding context
                    })
                    
                    # Mark this position as used
                    used_positions.add((start_pos, end_pos))
    
    # Sort by timing
    trigger_words.sort(key=lambda x: x["timing"])
    
    return trigger_words

def _calculate_word_position(text: str, char_position: int) -> int:
    """
    Calculate the word position (0-indexed) for a given character position.
    
    Args:
        text: The full text
        char_position: Character position in the text
        
    Returns:
        Word position (0-indexed)
    """
    if char_position >= len(text):
        return 0
    
    # Count words up to the character position
    text_before = text[:char_position]
    words_before = text_before.split()
    return len(words_before)

def _get_word_context(text: str, start_pos: int, end_pos: int, context_chars: int = 50) -> str:
    """
    Get surrounding context for a trigger word.
    
    Args:
        text: The full text
        start_pos: Start position of the trigger word
        end_pos: End position of the trigger word
        context_chars: Number of characters to include before and after
        
    Returns:
        Context string with the trigger word highlighted
    """
    # Calculate context boundaries
    context_start = max(0, start_pos - context_chars)
    context_end = min(len(text), end_pos + context_chars)
    
    # Extract context
    context = text[context_start:context_end]
    
    # Add ellipsis if we're not at the beginning/end
    if context_start > 0:
        context = "..." + context
    if context_end < len(text):
        context = context + "..."
    
    return context