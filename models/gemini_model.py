

import google.generativeai as genai
from typing import List
from colorama import Fore
from models.user_info import UserInfo

class GeminiWordlistGenerator:
    
    def __init__(self, api_key: str, model_name: str = 'gemini-2.5-flash'):
        self.api_key = api_key
        self.model_name = model_name
        self.model = None
        self.setup_gemini()
    
    def setup_gemini(self):
        try:
            genai.configure(api_key=self.api_key)
            print(f"{Fore.CYAN}🔧 Kullanılacak model: {self.model_name}")
            self.model = genai.GenerativeModel(self.model_name)
            print(f"{Fore.GREEN}✓ Gemini AI bağlantısı kuruldu ({self.model_name})")
        except Exception as e:
            raise Exception(f"Gemini AI bağlantı hatası: {e}")
    
    def generate_base_words(self, user_info: UserInfo) -> List[str]:
        print(f"{Fore.YELLOW}🤖 AI ile temel kelimeler oluşturuluyor...")
        
        info_text = self._prepare_user_info(user_info)
        
        prompt = f"""
Aşağıdaki kişisel bilgilere dayanarak şifre oluşturmada kullanılabilecek kelimeler üret:

{info_text}

Şu kuralları takip et:
1. Her kelimeyi yeni satırda yaz
2. Sadece kelimeleri listele, açıklama yapma
3. Türkçe karakterleri İngilizce karakterlere dönüştür
4. En az 50 kelime öner
5. Şu kategorilerden kelimeler dahil et:
   - İsim, soyisim kombinasyonları
   - Doğum yılı ve tarihleri
   - Şehir, ülke isimleri
   - Meslek ve şirket isimleri
   - Hobi ve ilgi alanları
   - Aile üyesi isimleri
   - Evcil hayvan isimleri
   - E-mail adresinden kelimeler
   - Telefon numarasından sayılar

Örnek format:
ahmet1905
yilmaz123
ahmetyilmaz53
istanbul
maviş2005
1990
yazilim
"""
        
        try:
            response = self.model.generate_content(prompt)
            words = [word.strip() for word in response.text.split('\n') if word.strip()]
            print(f"{Fore.GREEN}✓ {len(words)} temel kelime oluşturuldu")
            return words
        except Exception as e:
            print(f"{Fore.RED}✗ AI kelime oluşturma hatası: {e}")
            return []
    
    def enhance_wordlist(self, base_words: List[str]) -> List[str]:
        if not base_words:
            return []
            
        print(f"{Fore.YELLOW}🚀 AI ile wordlist geliştiriliyor...")
        
        sample_words = base_words[:15]
        
        prompt = f"""
Bu kelime listesindeki kalıpları analiz et ve benzer şifre kombinasyonları öner:

{chr(10).join(sample_words)}

Şu kurallara uy:
1. Benzer kalıpları takip eden yeni kombinasyonlar öner
2. Yaygın şifre kalıpları ekle (kelime+sayı, sayı+kelime)
3. Sadece kelimeleri listele
4. En az 25 yeni kelime öner
5. Türkçe karakterleri kullanma

Örnekler:
- Eğer "ahmet" varsa: "ahmet123", "123ahmet", "ahmet2024"
- Eğer "istanbul" varsa: "istanbul34", "34istanbul"
- Eğer meslek adı varsa: meslek adı + yaygın sayılar
"""
        
        try:
            response = self.model.generate_content(prompt)
            enhanced_words = [word.strip() for word in response.text.split('\n') if word.strip()]
            print(f"{Fore.GREEN}✓ AI ile {len(enhanced_words)} ek kelime oluşturuldu")
            return enhanced_words
        except Exception as e:
            print(f"{Fore.RED}✗ AI geliştirme hatası: {e}")
            return []
    
    def _prepare_user_info(self, user_info: UserInfo) -> str:
        info_lines = []
        
        if user_info.name:
            info_lines.append(f"İsim: {user_info.name}")
        if user_info.surname:
            info_lines.append(f"Soyisim: {user_info.surname}")
        if user_info.nickname:
            info_lines.append(f"Kullanıcı adı: {user_info.nickname}")
        if user_info.birth_year:
            info_lines.append(f"Doğum yılı: {user_info.birth_year}")
        if user_info.birth_date:
            info_lines.append(f"Doğum tarihi: {user_info.birth_date}")
        if user_info.city:
            info_lines.append(f"Şehir: {user_info.city}")
        if user_info.country:
            info_lines.append(f"Ülke: {user_info.country}")
        if user_info.job:
            info_lines.append(f"Meslek: {user_info.job}")
        if user_info.company:
            info_lines.append(f"Şirket: {user_info.company}")
        if user_info.school:
            info_lines.append(f"Okul: {user_info.school}")
        if user_info.email:
            info_lines.append(f"E-mail: {user_info.email}")
        if user_info.phone:
            info_lines.append(f"Telefon: {user_info.phone}")
        if user_info.hobbies:
            info_lines.append(f"Hobiler: {user_info.hobbies}")
        if user_info.family_names:
            info_lines.append(f"Aile üyeleri: {user_info.family_names}")
        if user_info.pet_names:
            info_lines.append(f"Evcil hayvanlar: {user_info.pet_names}")
        if user_info.friend_names:
            info_lines.append(f"Arkadaşlar: {user_info.friend_names}")
        if user_info.lucky_numbers:
            info_lines.append(f"Şanslı sayılar: {user_info.lucky_numbers}")
        if user_info.memorable_dates:
            info_lines.append(f"Önemli tarihler: {user_info.memorable_dates}")
        if user_info.keywords:
            info_lines.append(f"Özel kelimeler: {user_info.keywords}")
        
        return '\n'.join(info_lines)