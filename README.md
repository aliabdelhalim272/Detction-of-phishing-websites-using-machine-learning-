# Detection of Phishing Websites Using Machine Learning

Bu repo phishing tespiti projesinin veri analizini ve ekip uygulamasını içerir.
Şu anda ham veriyi anlamaya yönelik EDA aşamasındayız. Kaynak, yapı, kalite,
tekrar ve grup bazlı ayrım kontrolleri notebook'ta uygulanır. Henüz satır
silme, eksik doldurma, özellik seçimi veya model eğitimi uygulanmaz.

## Dosya düzeni

```text
data/
  raw/                 Orijinal veri; değiştirilmez
  processed/           Bulgulara göre üretilecek işlenmiş veri
notebooks/
  01_eda.ipynb         EDA soruları, kontrolleri, bulguları ve yorumları
src/
  backend_api/         Ekibin mevcut API kodu
reports/
  figures/             Analizden üretilecek grafikler
docs/                  Kaynak bilgisi, veri sözlüğü ve karar notları
models/                Ekibin model dosyaları
static/                Ekibin mevcut arayüzü
requirements.txt       Mevcut uygulamanın bağımlılıkları
```

Notebook keşif ve açıklama içindir. Tekrar kullanılacak veri hazırlama ve
özellik çıkarma fonksiyonları ihtiyaç doğduğunda `src/` altına taşınır.
`docs/` tanımları ve gerekçeleri, `reports/` üretilmiş grafik ve teslim
raporlarını içerir. İhtiyaç oluşmadan yeni klasör veya notebook kopyası eklenmez.

## Başlangıç

VS Code'da bu repo klasörünü açıp `notebooks/01_eda.ipynb` dosyasını kullanın.
İlk yedi bölüm analiz kodu ve çıktıları içerir; 8–12. bölümler sonraki
incelemelerin planıdır. 7. bölüm yalnızca eğitim verisinde tek değişkenli
dağılımları inceler; tablolar `reports/distributions/`, grafikler
`reports/figures/` altında saklanır. EDA için Python 3.12 ve `requirements-eda.txt`
kullanılır; `requirements.txt` mevcut backend içindir.

```powershell
python -m pip install -r requirements-eda.txt
```

İlgili Python ortamını notebook çekirdeği olarak seçip hücreleri sırayla çalıştırın.
Repo kökünden veya `notebooks/` dizininden çalıştırılabilir.
`reports/eda.html` kaydedilmiş çalışmanın tarayıcı görünümüdür; notebook yeniden
çalıştırıldığında HTML kendiliğinden yenilenmez.

Kalite tabloları `reports/initial_audit/` altında, sabit ayrımın satır eşlemesi
`data/processed/split_manifest.csv` ve ayarları `split_metadata.json` içinde
tutulur. Bu klasörde henüz temizlenmiş veri seti yoktur. Ayrım kilidi mevcutsa
notebook aynı kaynak, ayar ve satır ayrımını doğrular; farklıysa durur.

Önceki deneylerde bu veri kümesinin tamamı görülmüştür. Yeni ayrım ilerideki
çalışmayı düzenler; geriye dönük hiç görülmemiş bir test kümesi oluşturmaz.

Her kontrolde soru, yöntem, bulgu, yorum/sınırlılık ve karar kaydedilir.
Bağımsız model değerlendirmesi planlanıyorsa hedefe göre özellik seçimi ve
öğrenilen dönüşümler öncesinde test kümesi ayrılır. Temizleme akışı
bulgulardan sonra oluşturulur; ham veri yerinde değiştirilmez.

## Veri kaynağı

56 sütunun Türkçe açıklaması, kullanım grubu, kaynakları ve doğrulanma durumu
[sütun sözlüğünde](docs/data_dictionary.md) bulunur. Aynı tablo notebook'un
veri yapısı bölümünde de gösterilir; kesin formülü doğrulanmayanlar işaretlidir.

PhiUSIIL Phishing URL (Website), Arvind Prasad ve Shalini Chandra (2024),
[UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset), CC BY 4.0.

Yerel kaynak: `data/raw/PhiUSIIL_Phishing_URL_Dataset.csv`.
Kaynak etiketler: `0` phishing, `1` meşru. Ham ve işlenmiş CSV dosyaları
mevcut `.gitignore` kurallarıyla Git dışında tutulur.
