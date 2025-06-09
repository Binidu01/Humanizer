from flask import Flask, render_template, request
import re
import random
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from typing import List

# Initialize Flask app
app = Flask(__name__)

# Download NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

class TextHumanizer:
    def __init__(self):
        self.sentence_variations = [
            self.vary_sentence_lengths,
            self.add_colloquialisms,
            self.insert_pauses,
            self.use_synonyms,
            self.restructure_sentences,
            self.add_redundancy,
            self.vary_connectors
        ]
    
    def humanize(self, text: str, intensity: int = 3) -> str:
        sentences = sent_tokenize(text)
        humanized_sentences = []
        
        for sentence in sentences:
            for _ in range(intensity):
                transform = random.choice(self.sentence_variations)
                sentence = transform(sentence)
            humanized_sentences.append(sentence)
        
        humanized_text = ' '.join(humanized_sentences)
        humanized_text = self.add_human_touches(humanized_text)
        return humanized_text
    
    def get_synonyms(self, word: str, pos: str = None) -> List[str]:
        synonyms = set()
        pos_mapping = {
            'NN': wordnet.NOUN,
            'JJ': wordnet.ADJ,
            'VB': wordnet.VERB,
            'RB': wordnet.ADV
        }
        
        if pos:
            wordnet_pos = pos_mapping.get(pos[:2], None)
            if wordnet_pos:
                for syn in wordnet.synsets(word, pos=wordnet_pos):
                    for lemma in syn.lemmas():
                        synonym = lemma.name().replace('_', ' ')
                        if synonym.lower() != word.lower() and len(synonym.split()) == 1:
                            synonyms.add(synonym)
        else:
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    synonym = lemma.name().replace('_', ' ')
                    if synonym.lower() != word.lower() and len(synonym.split()) == 1:
                        synonyms.add(synonym)
        return list(synonyms)
    
    def vary_sentence_lengths(self, text: str) -> str:
        """Break up or combine sentences to vary length"""
        if random.random() < 0.3:
            clauses = re.split(r'[,;]', text)
            if len(clauses) > 1 and random.random() < 0.5:
                return '. '.join([c.strip().capitalize() for c in clauses if c.strip()]) + '.'
        return text
    
    def add_colloquialisms(self, text: str) -> str:
        """Add informal expressions"""
        colloquialisms = [
            ('you know', 0.3),
            ('I mean', 0.2),
            ('sort of', 0.2),
            ('kind of', 0.2),
            ('well', 0.1),
            ('actually', 0.1),
            ('basically', 0.1)
        ]
        
        words = word_tokenize(text)
        for phrase, prob in colloquialisms:
            if random.random() < prob and len(words) > 5:
                insert_pos = random.randint(1, len(words)-1)
                words.insert(insert_pos, phrase)
        
        return ' '.join(words)
    
    def insert_pauses(self, text: str) -> str:
        """Add human-like pauses and filler words"""
        fillers = ['uh', 'um', 'ah', 'er']
        if random.random() < 0.2 and len(word_tokenize(text)) > 8:
            filler = random.choice(fillers)
            words = word_tokenize(text)
            insert_pos = random.randint(1, len(words)-1)
            words.insert(insert_pos, filler)
            return ' '.join(words)
        return text
    
    def use_synonyms(self, text: str) -> str:
        """Replace words with synonyms where appropriate"""
        words = word_tokenize(text)
        pos_tags = nltk.pos_tag(words)
        
        for i, (word, tag) in enumerate(pos_tags):
            if tag.startswith('NN') or tag.startswith('JJ') or tag.startswith('VB'):
                if random.random() < 0.3:
                    syns = self.get_synonyms(word, tag)
                    if syns:
                        words[i] = random.choice(syns)
        
        return ' '.join(words)
    
    def restructure_sentences(self, text: str) -> str:
        """Change sentence structure while preserving meaning"""
        patterns = [
            (r'(\w+) is (\w+)', r'\1 can be described as \2'),
            (r'It is (.*?) that', r'One could argue that'),
            (r'There are (.*?) that', r'We find \1 which'),
            (r'The (.*?) of (.*?) is', r'\2 has a \1 that is')
        ]
        
        for pattern, replacement in patterns:
            if re.search(pattern, text):
                if random.random() < 0.5:
                    text = re.sub(pattern, replacement, text)
                    break
        return text
    
    def add_redundancy(self, text: str) -> str:
        """Add some human-like redundancy"""
        redundant_phrases = [
            ('in other words', 0.1),
            ('that is to say', 0.1),
            ('as I mentioned earlier', 0.05),
            ('to put it simply', 0.1)
        ]
        
        for phrase, prob in redundant_phrases:
            if random.random() < prob:
                words = word_tokenize(text)
                insert_pos = random.randint(1, len(words)-1)
                words.insert(insert_pos, phrase)
                text = ' '.join(words)
        return text
    
    def vary_connectors(self, text: str) -> str:
        """Vary sentence connectors to be less formulaic"""
        connectors = {
            'however': ['but', 'though', 'that said', 'on the other hand'],
            'therefore': ['so', 'thus', 'as a result', 'consequently'],
            'additionally': ['also', 'furthermore', 'what\'s more', 'plus']
        }
        
        words = word_tokenize(text)
        for i, word in enumerate(words):
            lower_word = word.lower()
            if lower_word in connectors and random.random() < 0.7:
                words[i] = random.choice(connectors[lower_word])
        return ' '.join(words)
    
    def add_human_touches(self, text: str) -> str:
        """Final cleanup and addition of human-like features"""
        if random.random() < 0.2:
            sentences = sent_tokenize(text)
            if len(sentences) > 1:
                idx = random.randint(0, len(sentences)-2)
                sentences[idx] = sentences[idx].rstrip('.') + '...'
                text = ' '.join(sentences)
        
        if random.random() < 0.15:
            remarks = [
                ' (or so it seems)',
                ' (in my experience)',
                ' (at least that\'s what I think)',
                ' (if you ask me)'
            ]
            insert_pos = text.rfind('.')
            if insert_pos != -1:
                text = text[:insert_pos] + random.choice(remarks) + text[insert_pos:]
        
        if random.random() < 0.1:
            words = word_tokenize(text)
            for i in range(1, len(words)):
                if words[i-1] not in ['.', '!', '?'] and random.random() < 0.05:
                    words[i] = words[i].lower()
            text = ' '.join(words)
        return text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ai_text = request.form.get('ai_text', '')
        intensity = int(request.form.get('intensity', 3))
        
        humanizer = TextHumanizer()
        humanized_text = humanizer.humanize(ai_text, intensity)
        
        return render_template('index.html', 
                            ai_text=ai_text,
                            humanized_text=humanized_text,
                            intensity=intensity)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)