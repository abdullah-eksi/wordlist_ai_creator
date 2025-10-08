
from dataclasses import dataclass
from typing import List, Optional
from colorama import Fore

@dataclass
class UserInfo:
    name: Optional[str] = None
    surname: Optional[str] = None
    nickname: Optional[str] = None
    birth_date: Optional[str] = None
    birth_year: Optional[str] = None
    
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    hobbies: Optional[str] = None
    favorite_color: Optional[str] = None
    favorite_animal: Optional[str] = None
    favorite_food: Optional[str] = None
    family_names: Optional[str] = None
    pet_names: Optional[str] = None
    friend_names: Optional[str] = None
    job: Optional[str] = None
    company: Optional[str] = None
    school: Optional[str] = None
    memorable_dates: Optional[str] = None
    lucky_numbers: Optional[str] = None
    keywords: Optional[str] = None

class UserInfoCollector:
    
    def collect_info(self) -> UserInfo:
        print(f"{Fore.YELLOW}📋 Wordlist oluşturmak için bilgilerinizi giriniz:")
        print(f"{Fore.CYAN}(Boş bırakmak istediğiniz alanlar için Enter'a basın)\n")
        
        print(f"{Fore.MAGENTA}🔸 KİŞİSEL BİLGİLER:")
        name = input(f"{Fore.WHITE}İsim: ").strip() or None
        surname = input(f"{Fore.WHITE}Soyisim: ").strip() or None
        nickname = input(f"{Fore.WHITE}Kullanıcı adı/Nick: ").strip() or None
        birth_date = input(f"{Fore.WHITE}Doğum tarihi (GG/AA/YYYY): ").strip() or None
        birth_year = input(f"{Fore.WHITE}Doğum yılı: ").strip() or None
        
        print(f"\n{Fore.MAGENTA}🔸 İLETİŞİM:")
        email = input(f"{Fore.WHITE}E-mail: ").strip() or None
        phone = input(f"{Fore.WHITE}Telefon: ").strip() or None
        
        print(f"\n{Fore.MAGENTA}🔸 LOKASYON:")
        city = input(f"{Fore.WHITE}Şehir: ").strip() or None
        country = input(f"{Fore.WHITE}Ülke: ").strip() or None
        
        print(f"\n{Fore.MAGENTA}🔸 İLGİ ALANLARI:")
        hobbies = input(f"{Fore.WHITE}Hobiler (virgülle ayırın): ").strip() or None
        favorite_color = input(f"{Fore.WHITE}Sevilen renk: ").strip() or None
        favorite_animal = input(f"{Fore.WHITE}Sevilen hayvan: ").strip() or None
        favorite_food = input(f"{Fore.WHITE}Sevilen yemek: ").strip() or None
        
        print(f"\n{Fore.MAGENTA}🔸 AİLE VE ARKADAŞLAR:")
        family_names = input(f"{Fore.WHITE}Aile üyesi isimleri (virgülle ayırın): ").strip() or None
        pet_names = input(f"{Fore.WHITE}Evcil hayvan isimleri (virgülle ayırın): ").strip() or None
        friend_names = input(f"{Fore.WHITE}Arkadaş isimleri (virgülle ayırın): ").strip() or None
        
        print(f"\n{Fore.MAGENTA}🔸 İŞ VE EĞİTİM:")
        job = input(f"{Fore.WHITE}Meslek: ").strip() or None
        company = input(f"{Fore.WHITE}Şirket: ").strip() or None
        school = input(f"{Fore.WHITE}Okul: ").strip() or None
        
        print(f"\n{Fore.MAGENTA}🔸 ÖZEL BİLGİLER:")
        memorable_dates = input(f"{Fore.WHITE}Önemli tarihler (virgülle ayırın): ").strip() or None
        lucky_numbers = input(f"{Fore.WHITE}Şanslı sayılar (virgülle ayırın): ").strip() or None
        keywords = input(f"{Fore.WHITE}Özel kelimeler (virgülle ayırın): ").strip() or None
        
        return UserInfo(
            name=name, surname=surname, nickname=nickname,
            birth_date=birth_date, birth_year=birth_year,
            email=email, phone=phone,
            city=city, country=country,
            hobbies=hobbies, favorite_color=favorite_color,
            favorite_animal=favorite_animal, favorite_food=favorite_food,
            family_names=family_names, pet_names=pet_names, friend_names=friend_names,
            job=job, company=company, school=school,
            memorable_dates=memorable_dates, lucky_numbers=lucky_numbers, keywords=keywords
        )
    
    def get_non_empty_fields(self, user_info: UserInfo) -> dict:
        return {k: v for k, v in user_info.__dict__.items() if v is not None and v.strip()}