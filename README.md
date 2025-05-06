# 🌤️ Hava Durumuna Göre Kıyafet Önerisi

Bu proje, kullanıcıların arayüze girdikleri şehrin hava durumuna göre uygun kıyafet önerileri almasını sağlayan bir web uygulamasıdır.

## 🎯 Projenin Amacı

- Kullanıcıların girdiği şehir için güncel hava durumu bilgisini almak
- Hava durumuna göre uygun kıyafet önerileri sunmak
- Kullanıcı dostu bir arayüz ile kolay kullanım sağlamak

## 🛠️ Kullanılan Teknolojiler

- **Python**: Ana programlama dili
- **Streamlit**: Web arayüzü için kullanılan framework
- **LangChain**: Yapay zeka entegrasyonu için
- **OpenAI GPT-4**: Doğal dil işleme ve öneriler için
- **WeatherAPI**: Hava durumu verilerini çekmek için


## 🔧 Gereksinimler

- Python 3.9
- Langchain API anahtarı
- OpenAI API anahtarı
- WeatherAPI anahtarı

## 🛠️ Kullanılan Araçlar (Tools)

- **get_weather**: Belirtilen konum için güncel hava durumu bilgisini çeker.
  
- **recommend_clothing**: Hava durumu bilgisine göre uygun kıyafet önerileri sunar
  - Sıcaklık aralığına göre öneriler
  - Hava koşullarına göre özel öneriler (yağmurlu, karlı, rüzgarlı, güneşli)
  - Mevsimsel uygunluk 