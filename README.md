# Wordlist Creator - AI Destekli Şifre Kelime Listesi Oluşturucu

Kişiselleştirilmiş wordlist oluşturmak için Google Gemini AI kullanılan Python uygulaması.

## 📋 Proje Açıklaması

Bu uygulama, kullanıcıların kişisel bilgileri doğrultusunda güvenlik testleri için özelleştirilmiş wordlist'ler oluşturur. Google Gemini AI modeli kullanarak akıllı kelime kombinasyonları üretir.

## 🚀 Özellikler

- **AI Destekli Kelime Üretimi**: Google Gemini AI ile akıllı kelime kombinasyonları
- **Kişiselleştirme**: Hedef Kullanıcı bilgileri bazında özelleştirilmiş wordlist
- **Kelime Varyasyonları**: Otomatik leet speak, sayı ve özel karakter kombinasyonları
- **Akıllı Filtreleme**: Temizleme ve gereksiz kelimeleri eleme
- **Renkli Konsol**: Colorama ile görsel geri bildirim
- **Esnek Yapılandırma**: `.env` dosyası ile kolay konfigürasyon

## 📁 Proje Yapısı

```text
wordlist_creator/
├── wordlist_generator.py      # Ana uygulama dosyası
├── models/                    # Modül dizini
│   ├── user_info.py          # Kullanıcı bilgi toplama sınıfı
│   ├── gemini_model.py       # Google Gemini AI entegrasyonu
│   └── wordlist_processor.py # Kelime işleme ve varyasyon oluşturma
├── requirements.txt          # Python paket gereksinimleri
├── .env                     # Ortam değişkenleri konfigürasyonu
└── README.md               # Bu dosya
```

## 🛠️ Kurulum

### 1. Python Gereksinimlerini Yükleyin

```bash
pip install -r requirements.txt
```

### 2. Google Gemini API Anahtarı Alın

- [Google AI Studio](https://aistudio.google.com/) adresinden API anahtarı alın
- `.env` dosyasındaki `GEMINI_API_KEY` değerini güncelleyin

### 3. Konfigürasyon

`.env` dosyasındaki ayarları ihtiyacınıza göre düzenleyin:

- `GEMINI_MODEL`: Kullanılacak AI model (varsayılan: gemini-2.5-flash)
- `MIN_WORD_LENGTH`: Minimum kelime uzunluğu (varsayılan: 3)
- `MAX_WORD_LENGTH`: Maksimum kelime uzunluğu (varsayılan: 50)
- `DEFAULT_OUTPUT_FILE`: Varsayılan çıktı dosyası adı

## 🎯 Kullanım

```bash
python wordlist_generator.py
```

Uygulama size aşağıdaki bilgileri soracak:

- Kişisel bilgiler (isim, soyisim, doğum tarihi)
- İletişim bilgileri (e-mail, telefon)
- Lokasyon (şehir, ülke)
- İlgi alanları ve hobiler
- Aile/arkadaş isimleri
- İş ve eğitim bilgileri
- Özel kelimeler ve sayılar

## 📊 Çıktı Örneği

Program çalıştıktan sonra:

1. **AI Temel Kelimeler**: Gemini AI tarafından üretilen temel kelimeler
2. **Varyasyonlar**: Otomatik oluşturulan kelime varyasyonları
3. **AI Geliştirmeler**: AI tarafından geliştirilmiş kelime kombinasyonları
4. **Final Wordlist**: Temizlenmiş ve filtrelenmiş final liste

## 🔧 Modüller

### `wordlist_generator.py`

- Ana uygulama sınıfı
- Kullanıcı arayüzü ve iş akışı yönetimi
- Konfigürasyon yönetimi

### `models/user_info.py`

- `UserInfo` dataclass: Kullanıcı bilgi yapısı
- `UserInfoCollector`: Konsol üzerinden kullanıcı bilgi toplama

### `models/gemini_model.py`

- `GeminiWordlistGenerator`: Google Gemini AI entegrasyonu
- Temel kelime üretimi ve wordlist geliştirme

### `models/wordlist_processor.py`

- `WordlistProcessor`: Kelime işleme ve varyasyon oluşturma
- Leet speak dönüşümü, sayı/karakter kombinasyonları
- Temizleme ve filtreleme işlemleri

## ⚙️ Gereksinimler

- Python 3.7+
- Google Gemini API anahtarı
- İnternet bağlantısı (AI API erişimi için)

### Python Paketleri

- `google-generativeai`: Google Gemini AI API
- `colorama`: Renkli konsol çıktısı
- `python-dotenv`: Ortam değişkeni yönetimi
- `typing-extensions`: Tip desteği

## 🔒 Güvenlik Notu

Bu araç sadece güvenlik testleri ve eğitim amaçlı kullanılmalıdır. Kendi sisteminizde veya izniniz olan sistemlerde test yapmak için kullanın.

