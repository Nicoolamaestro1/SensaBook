import re
from collections import Counter
from typing import Dict, List, Tuple
from app.models.book import Book, Chapter, Page
from sqlalchemy.orm import Session

class BookAnalyzer:
    """Analyzes book content and generates appropriate sound mappings"""
    
    # Base sound mappings that can be customized per book
    BASE_SCENE_MAPPINGS = {
        "night": {
            "keywords": ["night", "dark", "darkness", "shadow", "shadows", "moon", "stars", "starry", "evening", "dusk", "twilight", "black", "gloom", "obscure"],
            "sound_file": "night_ambience.mp3",
            "priority": 3
        },
        "storm": {
            "keywords": ["storm", "thunder", "lightning", "rain", "downpour", "tempest", "gale", "wind", "stormy", "thunderstorm", "tempestuous"],
            "sound_file": "storm.mp3",
            "priority": 4
        },
        "forest": {
            "keywords": ["forest", "trees", "woods", "grove", "thicket", "wilderness", "nature", "leaves", "branch", "branches"],
            "sound_file": "night_forest.mp3",
            "priority": 2
        },
        "castle": {
            "keywords": ["castle", "keep", "tower", "gates", "fortress", "palace", "citadel", "stone", "walls", "fortress"],
            "sound_file": "stone_echoes.mp3",
            "priority": 5
        },
        "mountains": {
            "keywords": ["mountains", "cliff", "peak", "valley", "summit", "ridge", "alpine", "high", "elevation"],
            "sound_file": "windy_mountains.mp3",
            "priority": 3
        },
        "indoors": {
            "keywords": ["cabin", "indoors", "inside", "house", "room", "building", "apartment", "home", "wall", "walls", "roof"],
            "sound_file": "cabin.mp3",
            "priority": 1
        },
        "fear": {
            "keywords": ["superstition", "afraid", "creepy", "haunted", "dark", "disaster", "evil", "terrifying", "horror", "scary", "frightening"],
            "sound_file": "tense_drones.mp3",
            "priority": 6
        },
        "travel": {
            "keywords": ["carriage", "train", "journey", "trip", "traveling", "voyage", "expedition", "road", "path", "way"],
            "sound_file": "horse_carriage.mp3",
            "priority": 2
        },
        "library": {
            "keywords": ["museum", "library", "books", "research", "study", "academic", "scholarly", "reading", "knowledge"],
            "sound_file": "quiet_museum.mp3",
            "priority": 2
        },
        "eating": {
            "keywords": ["dinner", "supper", "eating", "meal", "restaurant", "food", "dining", "feast", "table", "kitchen"],
            "sound_file": "restaurant_murmur.mp3",
            "priority": 1
        }
    }
    
    BASE_WORD_MAPPINGS = {
        "thunder": "thunder-city-377703.mp3",
        "lightning": "flash_pop.mp3",
        "door": "door_creak.mp3",
        "bird": "bird_chirp.mp3",
        "horse": "horse_neigh.mp3",
        "owl": "owl_hoot.mp3",
        "scream": "distant_scream.mp3",
        "fire": "fire_crackle.mp3",
        "wind": "wind.mp3",
        "chains": "chains_rattle.mp3",
        "footsteps": "footstep_wood.mp3",
        "clank": "armor_clank.mp3",
        "book": "page_turn.mp3",
        "bell": "bell_ring.mp3",
        "creak": "wood_creak.mp3",
        "laugh": "soft_laughter.mp3",
        "heartbeat": "heartbeat_slow.mp3",
        "whisper": "whisper_ghostly.mp3"
    }
    
    # Genre-specific mappings
    GENRE_MAPPINGS = {
        "horror": {
            "additional_scenes": {
                "gothic": {
                    "keywords": ["vampire", "dracula", "undead", "blood", "coffin", "grave", "tomb", "death", "mortal"],
                    "sound_file": "gothic_castle_ambience.mp3",
                    "priority": 7
                },
                "supernatural": {
                    "keywords": ["ghost", "spirit", "phantom", "haunted", "supernatural", "otherworldly", "ethereal"],
                    "sound_file": "whisper_ghostly.mp3",
                    "priority": 6
                }
            },
            "additional_words": {
                "vampire": "vampire_hiss.mp3",
                "blood": "blood_drip.mp3",
                "wolf": "wolf_howl.mp3",
                "howl": "wolf_howl.mp3"
            }
        },
        "fantasy": {
            "additional_scenes": {
                "magical": {
                    "keywords": ["magic", "spell", "wizard", "sorcerer", "enchantment", "mystical", "arcane"],
                    "sound_file": "atmosphere-sound-effect-239969.mp3",
                    "priority": 5
                },
                "battle": {
                    "keywords": ["battle", "war", "sword", "shield", "armor", "combat", "fighting", "clash"],
                    "sound_file": "tense_drones.mp3",
                    "priority": 6
                }
            },
            "additional_words": {
                "sword": "sword_clash.mp3",
                "armor": "armor_clank.mp3",
                "magic": "magic_spell.mp3"
            }
        },
        "adventure": {
            "additional_scenes": {
                "wilderness": {
                    "keywords": ["wilderness", "adventure", "exploration", "unknown", "dangerous", "treasure"],
                    "sound_file": "windy_mountains.mp3",
                    "priority": 4
                }
            },
            "additional_words": {
                "footsteps": "footsteps-approaching-316715.mp3"
            }
        }
    }
    
    def analyze_book_content(self, book: Book, db: Session) -> Tuple[Dict, Dict]:
        """
        Analyzes all content in a book and generates appropriate sound mappings.
        Returns (scene_mappings, word_mappings)
        """
        # Get all text content from the book
        all_text = self._extract_all_text(book, db)
        
        # Analyze the content
        scene_mappings = self._generate_scene_mappings(all_text, book.genre)
        word_mappings = self._generate_word_mappings(all_text, book.genre)
        
        return scene_mappings, word_mappings
    
    def _extract_all_text(self, book: Book, db: Session) -> str:
        """Extracts all text content from the book"""
        all_text = []
        
        # Get all pages for this book
        pages = db.query(Page).filter(Page.book_id == book.id).all()
        
        for page in pages:
            if page.content:
                all_text.append(page.content.lower())
        
        return " ".join(all_text)
    
    def _generate_scene_mappings(self, text: str, genre: str = None) -> Dict:
        """Generates scene mappings based on text analysis"""
        scene_mappings = {}
        
        # Start with base mappings
        for scene_name, mapping in self.BASE_SCENE_MAPPINGS.items():
            # Check if this scene is relevant to the text
            keyword_count = sum(1 for keyword in mapping["keywords"] if keyword in text)
            if keyword_count > 0:
                scene_mappings[scene_name] = {
                    "keywords": mapping["keywords"],
                    "sound_file": mapping["sound_file"],
                    "priority": mapping["priority"],
                    "relevance_score": keyword_count
                }
        
        # Add genre-specific mappings
        if genre and genre.lower() in self.GENRE_MAPPINGS:
            genre_mappings = self.GENRE_MAPPINGS[genre.lower()]
            for scene_name, mapping in genre_mappings.get("additional_scenes", {}).items():
                keyword_count = sum(1 for keyword in mapping["keywords"] if keyword in text)
                if keyword_count > 0:
                    scene_mappings[scene_name] = {
                        "keywords": mapping["keywords"],
                        "sound_file": mapping["sound_file"],
                        "priority": mapping["priority"],
                        "relevance_score": keyword_count
                    }
        
        # Sort by priority and relevance
        sorted_mappings = dict(sorted(
            scene_mappings.items(),
            key=lambda x: (x[1]["priority"], x[1]["relevance_score"]),
            reverse=True
        ))
        
        return sorted_mappings
    
    def _generate_word_mappings(self, text: str, genre: str = None) -> Dict:
        """Generates word mappings based on text analysis"""
        word_mappings = {}
        
        # Start with base word mappings
        for word, sound_file in self.BASE_WORD_MAPPINGS.items():
            if word in text:
                word_mappings[word] = sound_file
        
        # Add genre-specific word mappings
        if genre and genre.lower() in self.GENRE_MAPPINGS:
            genre_mappings = self.GENRE_MAPPINGS[genre.lower()]
            for word, sound_file in genre_mappings.get("additional_words", {}).items():
                if word in text:
                    word_mappings[word] = sound_file
        
        return word_mappings
    
    def create_book_with_mappings(self, title: str, author: str, genre: str, chapters_data: List[Dict], db: Session) -> Book:
        """
        Creates a book with automatically generated sound mappings.
        chapters_data should be a list of dicts with 'title' and 'pages' (list of content strings)
        """
        # Create the book first
        book = Book(
            title=title,
            author=author,
            genre=genre
        )
        db.add(book)
        db.flush()  # Get the book ID
        
        # Create chapters and pages
        for chapter_num, chapter_data in enumerate(chapters_data, 1):
            chapter = Chapter(
                book_id=book.id,
                chapter_number=chapter_num,
                title=chapter_data.get('title', f'Chapter {chapter_num}')
            )
            db.add(chapter)
            db.flush()
            
            # Create pages
            for page_num, content in enumerate(chapter_data['pages'], 1):
                page = Page(
                    chapter_id=chapter.id,
                    book_id=book.id,
                    page_number=page_num,
                    content=content
                )
                db.add(page)
        
        # Analyze the book and generate mappings
        scene_mappings, word_mappings = self.analyze_book_content(book, db)
        
        # Update the book with the mappings
        book.scene_mappings = scene_mappings
        book.word_mappings = word_mappings
        
        db.commit()
        return book

def get_soundscape_for_page(book: Book, page_content: str) -> Dict:
    """
    Gets soundscape for a specific page using the book's stored mappings.
    """
    text = page_content.lower()
    carpet_tracks = []
    triggered_sounds = []
    
    # Check scene mappings
    if book.scene_mappings:
        for scene_name, mapping in book.scene_mappings.items():
            keyword_count = sum(1 for keyword in mapping["keywords"] if keyword in text)
            if keyword_count > 0:
                carpet_tracks.append(mapping["sound_file"])
    
    # Check word mappings
    if book.word_mappings:
        for word, sound_file in book.word_mappings.items():
            if word in text:
                triggered_sounds.append({
                    "word": word,
                    "sound": sound_file,
                    "position": text.find(word)
                })
    
    # If no scenes detected, use default
    if not carpet_tracks:
        carpet_tracks = ["default_ambience.mp3"]
    
    return {
        "carpet_tracks": carpet_tracks,
        "triggered_sounds": triggered_sounds
    } 