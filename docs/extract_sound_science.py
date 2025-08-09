import pdfplumber
import sys

def extract_sound_science_pdfs():
    """Extract content from psychoacoustics and audio pattern recognition PDFs"""
    
    pdfs = [
        ("1912.10211.pdf", "Psychoacoustics Research Paper"),
        ("AudioUI02acoustics.pdf", "Audio UI Acoustics Paper")
    ]
    
    for pdf_file, description in pdfs:
        print(f"\n{'='*70}")
        print(f"EXTRACTING FROM: {description}")
        print(f"FILE: {pdf_file}")
        print(f"{'='*70}")
        
        try:
            with pdfplumber.open(pdf_file) as pdf:
                num_pages = len(pdf.pages)
                print(f"PDF has {num_pages} pages")
                
                # Extract title and abstract
                print(f"\nSEARCHING FOR TITLE AND ABSTRACT:")
                print("-" * 50)
                
                title_abstract = ""
                for page_num in range(min(10, num_pages)):
                    try:
                        page = pdf.pages[page_num]
                        text = page.extract_text()
                        
                        if text and text.strip():
                            lower_text = text.lower()
                            
                            # Look for title/abstract indicators
                            if any(keyword in lower_text for keyword in ['abstract', 'introduction', 'title', 'summary']):
                                print(f"\n--- POTENTIAL TITLE/ABSTRACT PAGE {page_num + 1} ---")
                                print(text[:800])
                                print("...")
                                title_abstract += f"\n--- PAGE {page_num + 1} ---\n{text}\n"
                                
                    except Exception as e:
                        print(f"\n--- PAGE {page_num + 1} --- (Error: {e})")
                        continue
                
                # Save title and abstract
                if title_abstract:
                    output_file = f"{pdf_file.replace('.pdf', '')}_title_abstract.txt"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(title_abstract)
                    print(f"\nTitle and abstract saved to '{output_file}'")
                
                # Look for key sound science concepts
                print(f"\nSEARCHING FOR KEY SOUND SCIENCE CONCEPTS:")
                print("-" * 50)
                
                sound_concepts = []
                sound_keywords = [
                    'psychoacoustics', 'frequency', 'amplitude', 'pitch', 'loudness',
                    'timbre', 'harmonics', 'overtones', 'resonance', 'reverberation',
                    'echo', 'absorption', 'reflection', 'diffraction', 'interference',
                    'masking', 'critical bands', 'auditory scene', 'spatial audio',
                    'binaural', 'stereo', 'surround', 'ambisonics', 'head-related',
                    'transfer function', 'impulse response', 'spectrum', 'waveform',
                    'envelope', 'attack', 'decay', 'sustain', 'release', 'adsr',
                    'filter', 'equalizer', 'compressor', 'reverb', 'delay', 'chorus',
                    'modulation', 'oscillator', 'synthesizer', 'sampler'
                ]
                
                for page_num in range(min(100, num_pages)):
                    try:
                        page = pdf.pages[page_num]
                        text = page.extract_text()
                        
                        if text and text.strip():
                            # Look for sound science concept pages
                            found_concepts = []
                            for concept in sound_keywords:
                                if concept in text.lower():
                                    found_concepts.append(concept)
                            
                            if found_concepts:
                                print(f"\n--- SOUND CONCEPTS FOUND ON PAGE {page_num + 1} ---")
                                print(f"Concepts: {', '.join(found_concepts)}")
                                print(f"Content preview: {text[:300]}...")
                                sound_concepts.append((page_num + 1, found_concepts, text[:500]))
                                
                    except Exception as e:
                        continue
                
                # Save sound concepts
                if sound_concepts:
                    output_file = f"{pdf_file.replace('.pdf', '')}_sound_concepts.txt"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(f"KEY SOUND SCIENCE CONCEPTS FOUND IN {description.upper()}:\n")
                        f.write("=" * 60 + "\n\n")
                        for page_num, concepts, content in sound_concepts:
                            f.write(f"PAGE {page_num} - Concepts: {', '.join(concepts)}\n")
                            f.write(f"Content: {content}\n")
                            f.write("-" * 50 + "\n\n")
                    print(f"\nSound concepts saved to '{output_file}'")
                
                # Look for practical applications
                print(f"\nSEARCHING FOR PRACTICAL APPLICATIONS:")
                print("-" * 50)
                
                applications = []
                app_keywords = [
                    'application', 'implementation', 'example', 'case study',
                    'experiment', 'evaluation', 'results', 'conclusion',
                    'recommendation', 'guideline', 'best practice', 'methodology'
                ]
                
                for page_num in range(min(50, num_pages)):
                    try:
                        page = pdf.pages[page_num]
                        text = page.extract_text()
                        
                        if text and text.strip():
                            # Look for application pages
                            found_apps = []
                            for app in app_keywords:
                                if app in text.lower():
                                    found_apps.append(app)
                            
                            if found_apps:
                                print(f"\n--- APPLICATIONS FOUND ON PAGE {page_num + 1} ---")
                                print(f"Application types: {', '.join(found_apps)}")
                                print(f"Content preview: {text[:300]}...")
                                applications.append((page_num + 1, found_apps, text[:500]))
                                
                    except Exception as e:
                        continue
                
                # Save applications
                if applications:
                    output_file = f"{pdf_file.replace('.pdf', '')}_applications.txt"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(f"PRACTICAL APPLICATIONS FOUND IN {description.upper()}:\n")
                        f.write("=" * 60 + "\n\n")
                        for page_num, apps, content in applications:
                            f.write(f"PAGE {page_num} - Applications: {', '.join(apps)}\n")
                            f.write(f"Content: {content}\n")
                            f.write("-" * 50 + "\n\n")
                    print(f"\nApplications saved to '{output_file}'")
                
        except Exception as e:
            print(f"Error extracting PDF {pdf_file}: {e}")
            continue

if __name__ == "__main__":
    extract_sound_science_pdfs()
