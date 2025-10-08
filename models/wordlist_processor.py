

from typing import List, Set
from colorama import Fore
from models.user_info import UserInfo
import re

class WordlistProcessor:
    
    def __init__(self):
        self.common_numbers = ['1', '12', '123', '1234', '2023', '2024', '2025', '01', '00', '21', '22', '23']
        self.special_chars = ['!', '@', '#', '$', '%', '*', '&']
        self.leet_map = {
            'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7', 'g': '6', 'l': '1'
        }
    
    def create_variations(self, base_words: List[str], user_info: UserInfo) -> List[str]:
        print(f"{Fore.YELLOW}🔄 Kelime varyasyonları oluşturuluyor...")
        
        variations = set()
        for word in base_words:
            if word and len(word) >= 2:
                variations.add(word.lower())
                variations.add(word.upper())
                variations.add(word.capitalize())
        
        if user_info.birth_year:
            self.common_numbers.extend([user_info.birth_year, user_info.birth_year[-2:]])
        if user_info.lucky_numbers:
            numbers = [num.strip() for num in user_info.lucky_numbers.split(',')]
            self.common_numbers.extend(numbers)
        
        for word in base_words[:15]:
            if word and len(word) >= 3:
                for num in self.common_numbers:
                    variations.add(f"{word}{num}")
                    variations.add(f"{num}{word}")
        
        for word in base_words[:10]:
            if word and len(word) >= 3:
                for char in self.special_chars:
                    variations.add(f"{word}{char}")
                    if len(word) >= 4:
                        variations.add(f"{char}{word}")
        
        for word in base_words[:12]:
            if word and len(word) >= 4:
                leet_word = self._to_leet_speak(word.lower())
                if leet_word != word.lower():
                    variations.add(leet_word)
                    variations.add(f"{leet_word}123")
                    variations.add(f"{leet_word}2024")
        if user_info.name and user_info.surname:
            name_combos = self._create_name_combinations(user_info.name, user_info.surname)
            variations.update(name_combos)
        if user_info.email:
            email_vars = self._create_email_variations(user_info.email)
            variations.update(email_vars)
        if user_info.phone:
            phone_vars = self._create_phone_variations(user_info.phone)
            variations.update(phone_vars)
        
        result = list(variations)
        print(f"{Fore.GREEN}✓ {len(result)} varyasyon oluşturuldu")
        return result
    
    def _to_leet_speak(self, word: str) -> str:
        leet_word = word
        for normal, leet in self.leet_map.items():
            leet_word = leet_word.replace(normal, leet)
        return leet_word
    
    def _create_name_combinations(self, name: str, surname: str) -> Set[str]:
        combinations = set()
        
        name_clean = name.lower().strip()
        surname_clean = surname.lower().strip()
        
        if name_clean and surname_clean:
            combinations.add(f"{name_clean}{surname_clean}")
            combinations.add(f"{surname_clean}{name_clean}")
            combinations.add(f"{name_clean}.{surname_clean}")
            combinations.add(f"{name_clean}_{surname_clean}")
            combinations.add(f"{name_clean[0]}{surname_clean}")
            combinations.add(f"{name_clean}{surname_clean[0]}")
            combinations.add(f"{name_clean[0]}{surname_clean[0]}")
            full_name = f"{name_clean}{surname_clean}"
            for num in ['123', '2024', '01']:
                combinations.add(f"{full_name}{num}")
        
        return combinations
    
    def _create_email_variations(self, email: str) -> Set[str]:
        variations = set()
        if '@' in email:
            username = email.split('@')[0].lower()
            variations.add(username)
            clean_username = username.replace('.', '').replace('_', '')
            variations.add(clean_username)
            for num in ['123', '2024']:
                variations.add(f"{clean_username}{num}")
        
        return variations
    
    def _create_phone_variations(self, phone: str) -> Set[str]:
        variations = set()
        digits = re.sub(r'\D', '', phone)
        
        if len(digits) >= 6:
            variations.add(digits[-4:])
            if len(digits) >= 6:
                variations.add(digits[-6:])
            clean_digits = digits.lstrip('0')
            if len(clean_digits) >= 4:
                variations.add(clean_digits[:4])
        
        return variations
    
    def clean_and_filter(self, wordlist: List[str]) -> List[str]:
        print(f"{Fore.YELLOW}🧹 Wordlist temizleniyor...")
        
        cleaned = set()
        
        for word in wordlist:
            if word and isinstance(word, str):
                word = word.strip()
                if len(word) >= 3 and len(word) <= 50:
                    if re.match(r'^[a-zA-Z0-9@#$%&*!._-]+$', word):
                        cleaned.add(word)
        
        result = sorted(list(cleaned))
        print(f"{Fore.GREEN}✓ {len(result)} temiz kelime hazırlandı")
        return result
    
    def save_wordlist(self, wordlist: List[str], filename: str) -> int:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for word in wordlist:
                    f.write(f"{word}\n")
            
            print(f"\n{Fore.GREEN}✅ Wordlist kaydedildi: {filename}")
            print(f"{Fore.CYAN}📊 Toplam kelime sayısı: {len(wordlist)}")
            return len(wordlist)
        except Exception as e:
            print(f"{Fore.RED}❌ Dosya kaydetme hatası: {e}")
            return 0