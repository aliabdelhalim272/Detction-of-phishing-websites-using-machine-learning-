# Detection of Phishing Websites Using Machine Learning

Bu repo phishing tespiti projesinin veri analizini ve ekip uygulamasını içerir.
EDA tamamlandı; bulgulara dayanan URL-only veri hazırlama uygulaması ayrı
notebook'ta yürütülür. Ham veri değiştirilmez. Sayfa özellikleri sessizce
düzeltilmez; yeni lexical özellikler ortak modülle üretilir. Model eğitimi
ve backend entegrasyonu bu çalışma kapsamında yapılmadı.

## Dosya düzeni

```text
data/
  raw/                 Orijinal veri; değiştirilmez
  processed/           Bulgulara göre üretilecek işlenmiş veri
notebooks/
  01_eda.ipynb         EDA soruları, kontrolleri, bulguları ve yorumları
  02_data_preparation.ipynb  EDA kararlarının uygulanması ve çıktı doğrulaması
src/
  backend_api/         Ekibin mevcut API kodu
  data/                Veri hazırlama ve kaynak satırı eşlemesi
  features/            Ortak, sürümlenmiş URL çıkarım modülü
reports/
  figures/             Analizden üretilecek grafikler
docs/                  Kaynak bilgisi, veri sözlüğü ve karar notları
models/                Ekibin model dosyaları
static/                Ekibin mevcut arayüzü
requirements.txt       Mevcut uygulamanın bağımlılıkları
tests/                 Çıkarım ve veri bütünlüğü testleri
```

Notebook keşif ve açıklama içindir. Tekrar kullanılacak veri hazırlama ve
özellik çıkarma fonksiyonları ihtiyaç doğduğunda `src/` altına taşınır.
`docs/` tanımları ve gerekçeleri, `reports/` üretilmiş grafik ve teslim
raporlarını içerir. İhtiyaç oluşmadan yeni klasör veya notebook kopyası eklenmez.

## Başlangıç

VS Code'da bu repo klasörünü açıp `notebooks/01_eda.ipynb` dosyasını kullanın.
1–11. bölümler EDA kodu ve çıktıları, 12. bölüm kanıta dayalı hazırlık planı
ve durum denetimini içerir. EDA akışı ve plan tamamlandı; veri hazırlama
uygulaması `02_data_preparation.ipynb` içinde ayrıca yapılır. EDA notebook'u
gerekçelerin kaydı olarak korunur. 7. bölüm yalnızca eğitim verisinde tek değişkenli
dağılımları inceler; tablolar `reports/distributions/`, grafikler
`reports/figures/` altında saklanır. EDA için Python 3.12 ve `requirements-eda.txt`
kullanılır; `requirements.txt` mevcut backend içindir.

8. bölüm eğitimde aykırı değer eşiklerini, sıfır IQR durumlarını, uç kayıtları
ve mantıksal kontrol adaylarını inceler. Tablolar `reports/outliers/` altında
tutulur; eşik dışı kayıtlar otomatik silinmez veya kırpılmaz.

9. bölüm eğitimde sınıf içi özellik dağılımlarını, ikili oran farklarını,
sıra tabanlı etki büyüklüklerini ve host ağırlıklı betimsel duyarlılığı
inceler. Tablolar `reports/target_relationships/` altında saklanır;
anlamlılık, nedensellik veya bağımsız test başarısı iddiası sunulmaz.

10. bölüm özellikler arası Pearson/Spearman korelasyonlarını, tam eşitlikleri,
türetme adaylarını ve sınıf içi ilişkileri inceler. Tablolar
`reports/feature_relationships/` altında saklanır; korelasyon nedeniyle
otomatik özellik elemesi uygulanmaz.

11. bölüm 56 sütunun kökenini ve canlı kullanılabilirliğini envanterler;
doğrudan hedef kopyalarını, HTTPS anlamını ve mevcut API sözleşmesini inceler.
Tablolar `reports/provenance/` altında saklanır. API kodu yalnızca statik
olarak okunur; uygulama çalıştırılmaz veya değiştirilmez.

12. bölümdeki 16 karar başlığı, önerilen 14 alanlı URL-only sözleşmesi ve
uygulama sırası [veri hazırlama planında](docs/data_preparation_plan.md)
bulunur. Makinece okunabilir kararlar ve **henüz uygulanmamış** sözleşme
`reports/preparation_plan/` altında EDA'nın plan anındaki durumunu gösterir.
Güncel uygulama çıktısı için `reports/data_preparation/summary.json` kullanılır.
İçerik tabanlı seçenek ayrıca ele alınmıştır.

## Veri hazırlamayı çalıştırma

`02_data_preparation.ipynb` tek başına Run All ile çalışır; önce EDA notebook'unu
aynı oturumda çalıştırmak gerekmez. Ham CSV ile EDA'da oluşturulmuş
`data/processed/split_manifest.csv` ve `split_metadata.json` yerelde bulunmalıdır.
Eksik veya değişmiş ayrım otomatik oluşturulmaz. Repo kökünden testleri çalıştırın:

```powershell
python -m unittest discover -s tests
python src/features/url_features.py "https://example.com/login?id=1"
```

Çıktılar `data/processed/url_lexical_v1/` altında ayrı X, hedef, metadata,
kaynak eşlemesi, karantina ve şema dosyalarıdır. `features.csv` içindeki
`source_row` yalnız indeks/birleşim anahtarıdır; model için `schema.json`
içindeki 14 alan açıkça seçilmelidir. Büyük CSV'ler Git dışında kalır.
Teslimde yerel CSV dosyaları birlikte paylaşılmalıdır; Git checkout'u veriyi
ve yerel ayrım dosyalarını tek başına sağlamaz.

İkinci notebook'un açıklamaları, hedef anlamı ve teslim şartları
[veri hazırlama raporundadır](docs/data_preparation.md). Hazırlık HTML görünümü
`reports/data_preparation.html` dosyasıdır. Şemaya uygun modül henüz API'nin
eski beş özellikli extractor'ının yerine bağlanmadı.

İkinci notebook'un 6–7. bölümleri EDA bulgularının her birini öncesi/sonrası
ve durum tablosuyla izler. `reports/data_preparation/finding_status.csv`
uygulananları, işlem gerektirmeyenleri ve çözülmemiş/kapsam dışı konuları
ayırır. “Orijinal 56 sütunun tamamı düzeltildi” iddiası yoktur.

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
