

import os
import sys
import warnings
import logging
from typing import List, Optional
from datetime import datetime
from colorama import init, Fore, Style
from dotenv import load_dotenv



# Kendi modellerimizi import et
from models.user_info import UserInfoCollector, UserInfo
from models.gemini_model import GeminiWordlistGenerator
from models.wordlist_processor import WordlistProcessor

class WordlistCreator:
    
    def __init__(self):
      
        init(autoreset=True)
        
        # .env dosyasını yükle
        load_dotenv()
        
        # Konfigürasyon
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.gemini_model = os.getenv('GEMINI_MODEL', 'gemini-pro')
        self.min_word_length = int(os.getenv('MIN_WORD_LENGTH', '3'))
        self.max_word_length = int(os.getenv('MAX_WORD_LENGTH', '50'))
        self.default_output_file = os.getenv('DEFAULT_OUTPUT_FILE', 'custom_wordlist.txt')
        self.debug_mode = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
        
        # Sınıfları başlat
        self.user_collector = UserInfoCollector()
        self.processor = WordlistProcessor()
        self.gemini_generator = None
        
        # API key kontrolü
        self._check_api_key()
        
    def _check_api_key(self):
        if not self.gemini_api_key or self.gemini_api_key == 'your_gemini_api_key_here':
            print(f"{Fore.RED}❌ HATA: Gemini API anahtarı bulunamadı!")
            print(f"{Fore.YELLOW}📝 Lütfen .env dosyasında GEMINI_API_KEY değerini ayarlayın.")
            print(f"{Fore.CYAN}🔗 API anahtarı için: https://aistudio.google.com/")
            sys.exit(1)
    
    def _print_banner(self):
        banner = f"""
{Fore.CYAN}{'='*60}
{Fore.YELLOW}    🚀  WORDLIST GENERATOR 🚀
{Fore.CYAN}{'='*60}
{Fore.GREEN}✨ AI Destekli Kişiselleştirilmiş Wordlist Oluşturucu
{Fore.MAGENTA}🤖 Gemini AI Model: {self.gemini_model}
{Fore.BLUE}📅 Tarih: {datetime.now().strftime('%d/%m/%Y %H:%M')}
{Fore.CYAN}{'='*60}
        """
        print(banner)
    
    def _print_configuration(self):
        if self.debug_mode:
            print(f"\n{Fore.YELLOW}🔧 MEVCUT KONFIGÜRASYON:")
            print(f"{Fore.WHITE}├─ Gemini Model: {self.gemini_model}")
            print(f"{Fore.WHITE}├─ Min Kelime Uzunluğu: {self.min_word_length}")
            print(f"{Fore.WHITE}├─ Max Kelime Uzunluğu: {self.max_word_length}")
            print(f"{Fore.WHITE}├─ Varsayılan Çıktı: {self.default_output_file}")
            print(f"{Fore.WHITE}└─ Debug Mode: {self.debug_mode}")
    
    def create_wordlist(self):
        try:
            # Banner'ı göster
            self._print_banner()
            self._print_configuration()
            
            # Kullanıcı bilgilerini topla
            print(f"\n{Fore.YELLOW}📋 ADIM 1: Kullanıcı Bilgileri Toplama")
            user_info = self.user_collector.collect_info()
            
            # Toplanan bilgileri göster
            self._show_collected_info(user_info)
            
            # Gemini AI'ı başlat
            print(f"\n{Fore.YELLOW}🤖 ADIM 2: AI Bağlantısı Kurma")
            self.gemini_generator = GeminiWordlistGenerator(self.gemini_api_key, self.gemini_model)
            
            # AI ile temel kelimeler oluştur
            print(f"\n{Fore.YELLOW}🧠 ADIM 3: AI ile Temel Kelimeler Oluşturma")
            base_words = self.gemini_generator.generate_base_words(user_info)
            
            if self.debug_mode and base_words:
                print(f"{Fore.CYAN}🔍 İlk 10 temel kelime: {base_words[:10]}")
            
            # Kelime varyasyonları oluştur
            print(f"\n{Fore.YELLOW}🔄 ADIM 4: Kelime Varyasyonları Oluşturma")
            variations = self.processor.create_variations(base_words, user_info)
            
            # AI ile wordlist'i geliştir
            print(f"\n{Fore.YELLOW}🚀 ADIM 5: AI ile Wordlist Geliştirme")
            enhanced_words = self.gemini_generator.enhance_wordlist(base_words)
            
            # Tüm kelimeleri birleştir
            all_words = base_words + variations + enhanced_words
            
            # Temizle ve filtrele
            print(f"\n{Fore.YELLOW}🧹 ADIM 6: Wordlist Temizleme ve Filtreleme")
            final_wordlist = self.processor.clean_and_filter(all_words)
            
            # Sonuçları göster
            self._show_statistics(base_words, variations, enhanced_words, final_wordlist)
            
            # Dosyaya kaydet
            print(f"\n{Fore.YELLOW}💾 ADIM 7: Wordlist Kaydetme")
            output_file = self._get_output_filename()
            saved_count = self.processor.save_wordlist(final_wordlist, output_file)
            
            if saved_count > 0:
                self._show_completion_message(output_file, saved_count)
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⚠️  İşlem kullanıcı tarafından iptal edildi.")
        except Exception as e:
            print(f"\n{Fore.RED}❌ Beklenmeyen hata: {e}")
            if self.debug_mode:
                import traceback
                traceback.print_exc()
    
    def _show_collected_info(self, user_info: UserInfo):
        non_empty = self.user_collector.get_non_empty_fields(user_info)
        
        if non_empty:
            print(f"\n{Fore.GREEN}✅ Toplanan Bilgiler ({len(non_empty)} alan):")
            for key, value in non_empty.items():
                # Uzun değerleri kısalt
                display_value = value if len(value) <= 30 else value[:30] + "..."
                print(f"{Fore.WHITE}├─ {key.replace('_', ' ').title()}: {display_value}")
        else:
            print(f"{Fore.YELLOW}⚠️  Hiç bilgi girilmedi, genel wordlist oluşturulacak.")
    
    def _show_statistics(self, base_words: List[str], variations: List[str], 
                        enhanced_words: List[str], final_wordlist: List[str]):
        print(f"\n{Fore.CYAN}📊 WORDLIST İSTATİSTİKLERİ:")
        print(f"{Fore.WHITE}├─ AI Temel Kelimeler: {len(base_words)}")
        print(f"{Fore.WHITE}├─ Varyasyonlar: {len(variations)}")
        print(f"{Fore.WHITE}├─ AI Geliştirmeler: {len(enhanced_words)}")
        print(f"{Fore.WHITE}├─ Toplam Ham: {len(base_words) + len(variations) + len(enhanced_words)}")
        print(f"{Fore.GREEN}└─ Final Temiz Wordlist: {len(final_wordlist)}")
    
    def _get_output_filename(self) -> str:
        print(f"\n{Fore.CYAN}💾 Dosya Kaydetme Seçenekleri:")
        print(f"{Fore.WHITE}1. Varsayılan dosya adı ({self.default_output_file})")
        print(f"{Fore.WHITE}2. Özel dosya adı belirt")
        print(f"{Fore.WHITE}3. Tarih-saat ile otomatik adlandır")
        
        choice = input(f"{Fore.YELLOW}Seçiminiz (1-3): ").strip()
        
        if choice == "2":
            custom_name = input(f"{Fore.WHITE}Dosya adı (.txt otomatik eklenecek): ").strip()
            if custom_name:
                if not custom_name.endswith('.txt'):
                    custom_name += '.txt'
                return custom_name
        elif choice == "3":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"wordlist_{timestamp}.txt"
        
        return self.default_output_file
    
    def _show_completion_message(self, filename: str, word_count: int):
        completion_message = f"""
{Fore.GREEN}{'='*60}
{Fore.YELLOW}    🎉 WORDLIST BAŞARIYLA OLUŞTURULDU! 🎉
{Fore.GREEN}{'='*60}
{Fore.CYAN}📁 Dosya: {filename}
{Fore.CYAN}📊 Toplam Kelime: {word_count:,}
{Fore.CYAN}📅 Oluşturulma: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}


        """
        print(completion_message)

def main():
    try:
        # Gerekli paketlerin yüklü olup olmadığını kontrol et
        required_packages = {
            'colorama': 'colorama',
            'python-dotenv': 'dotenv',
            'google-generativeai': 'google.generativeai'
        }
        missing_packages = []
        
        for package_name, import_name in required_packages.items():
            try:
                __import__(import_name)
            except ImportError:
                missing_packages.append(package_name)
        
        if missing_packages:
            print(f"{Fore.RED}❌ Eksik paketler: {', '.join(missing_packages)}")
            print(f"{Fore.YELLOW}📦 Kurulum için: pip install {' '.join(missing_packages)}")
            return
        
        # Ana uygulamayı başlat
        creator = WordlistCreator()
        creator.create_wordlist()
        
    except Exception as e:
        print(f"{Fore.RED}❌ Program başlatma hatası: {e}")

if __name__ == "__main__":
    main()
