# URL-only veri hazırlama uygulaması

EDA kararlarının kanıtı `01_eda.ipynb` ve `data_preparation_plan.md` içinde
korunur. Uygulama `02_data_preparation.ipynb` dosyasındadır; önceki notebook'un
bellek değişkenlerine bağımlı değildir. Ortam Python 3.12 ve `requirements-eda.txt`.

## Uygulanan politika

- Kaynak hash ve EDA host gruplama sözleşmesi doğrulanır. Aynı satır
  partition'ı korunur; yeniden ayrım veya seed araması yapılmaz.
- `src/features/url_features.py` içindeki ortak offline fonksiyon, URL-only
  yeni özellikleri üretir. Sürüm `url_lexical_v1`; isim/sıra `FEATURE_NAMES`.
  Formül açıklamaları modül ve EDA hazırlık planındadır.
- Eski URLLength, IsHTTPS veya içerik ölçümleri yerinde düzeltilmez. Yeni
  özellikler başka isimli ayrı çıktıda tutulur; eski ham veri korunur.
- Exact URL gruplarında çelişkili hedef veya partition varsa durulur.
  Aynı URL, aynı deterministik çıkarıcı ve aynı hedef için bir temsilci
  seçilir: en küçük source_row. Kayıtlı eski içeriklerin doğru/güncel
  olduğu iddia edilmez; URL-only görünümde tekrar ağırlığı azaltılır.
- Bütün kaynak satırları temsilciye veya gerekçeli karantinaya bağlanır.
  Girdi hatası sahte sıfır özelliklere çevrilmez. Eksik URL/etiket gibi
  kaynak bütünlüğü sorunları sessizce karantinaya atılmak yerine işlemi durdurur.
- IQR silme, kırpma, veriyle öğrenilmiş doldurma, ölçekleme veya encoding yoktur.
  Test/validasyon verisinde yalnız önceden belirlenmiş dönüşüm ve bütünlük
  kontrolleri yapılır; dağılım/başarı üzerinden özellik seçilmez.

## Çıktılar

`data/processed/url_lexical_v1/`:

| Dosya | Amaç |
|---|---|
| features.csv | source_row indeksi ve 14 sayısal özellik |
| target.csv | source_row ve is_phishing (1 phishing, 0 meşru) |
| metadata.csv | source_row, URL, hostname_group, original_label, partition |
| source_mapping.csv | Her kaynak satırının temsilcisi, partition'ı ve durumu |
| quarantine.csv | Kabul edilmeyen URL satırının source_row ve red sebebi |
| schema.json | Sıralı özellikler, hedef ve anahtar sözleşmesi |

`source_row` sıfırdan başlayan kaynak CSV veri satırı pozisyonudur; başlık satırı
dahil değildir. **Model girdisi değildir.** Üç ana tablo bu anahtarla birleştirilir.
Rol 2 yalnız `schema.json` içindeki alanları X olarak seçmelidir. Hedef veya
kimlik metadata'sı X'e eklenmemelidir. Preprocessing yalnız train'de fit edilir.

Gerçek başlangıç/son kayıt sayıları, kaynak/modül/çıktı SHA-256 özetleri ve
ortam sürümleri `reports/data_preparation/summary.json` içinde; partition
boyutları `partition_summary.csv` içindedir. Bunlar çalışma sırasında üretilir;
raporlar büyük veri dosyalarının yerini tutmaz. CSV'ler yerelde Git dışında kalır.

## Doğrulama ve tekrar üretim

### Doğrulanan ilk çalışma

| Ölçüm | Sonuç |
|---|---:|
| Kaynak satır | 235.795 |
| Yeni lexical gözlem | 235.370 |
| Temsilciye eşlenen tekrar satırı | 425 |
| Karantina | 0 |
| Eğitim satırı | 141.001 |
| Doğrulama satırı | 46.855 |
| Test satırı | 47.514 |

Host grup sayıları eğitimde 132.045, doğrulama ve testte ayrı ayrı 44.016
olarak korundu. Satır sayıları yalnız tekrarların temsilciye eşlenmesiyle azaldı.
Altı otomatik test geçti; notebook bağımsız çekirdekte çalıştırıldı ve çıktı
dosyaları diskten doğrulandı. Ham veri, EDA, API ve ayrım dosyalarının hash
kontrolleri geçti. Bu sayılar ilk çalışmanın kaydıdır; farklı kaynakta son
durum için üretilmiş `summary.json` esas alınmalıdır.

### Kontroller

Notebook kaynak ve ayrımı kontrol eder, dosyaları üretir ve diskten tekrar
okuyarak X/y/metadata uyumunu doğrular. Kayıt dengesi, hedef dönüşümü, URL
benzersizliği, host örtüşmesi ve örnek satırlarda training/live parity kontrolü
yapılır. EDA, ham veri, ayrım kilidi ve backend hash'leri korunur.

```powershell
python -m unittest discover -s tests
python src/features/url_features.py "https://example.com/login?id=1"
```

Sınır durumları: HTTP/HTTPS, query içinde https, port/userinfo, IPv4/IPv6,
Unicode/IDNA, boş query parçaları ve geçersiz URL/port/kontrol karakterleri.
Kaynak/etiket çelişkileri ve kümeler arası URL/host örtüşmeleri durdurulur.

Yeni kaynakta Run All deterministik yerel çıktıları yeniler. Raporlanmış
çıktılarla çalışmak için kaynak CSV ve yerel EDA manifesti gerekir. Ayrım
dosyaları yoksa sessizce başka bir ayrım üretilmez.

## EDA bulgularının durum takibi

İkinci notebook'un 6–7. bölümleri her bulguyu yapılan işlem ve kalan sınırla
eşler. `reports/data_preparation/finding_status.csv` 22 başlığın durumunu
tutar. “Kapsam dışında” ile “uygulandı/doğrulandı” farklı durumlardır.

`before_after_training.csv` karşılaştırması EDA'daki aynı 141.254 eğitim
kaynak satırında yapılır: tekrar satırları temsilcisine eşlenir. Böylece
tekilleşme nedeniyle fark sayıları yapay olarak azalmış görünmez. Yeni
uzunluk, HTTPS, rakam sayısı/oranı kendi açık tanımlarına karşı kontrol edilir.
Eski üretici formülünün doğrulandığı iddia edilmez.

`domain_difference_classification.csv` host/netloc farklarında port ve userinfo
durumlarını sınıflandırır. `remediation_summary.json` durum ve doğrulama özetidir.
Büyük satır bazlı farklar `data/processed/url_lexical_v1/training_correction_details.csv`
içinde yereldir. `training_diagnostic_counts.csv` yalnız eğitim için yeniden
hesaplanan eşittir, soru işareti ve ampersand sayılarıdır; **14 özellikli model
sözleşmesini genişletmez**. Bu dosyalardaki source_row da model girdisi değildir.

Bu ek inceleme mevcut X/y dosyalarını yeniden yazmaz; hash'lerini doğrular.
Önceki notebook ve API değiştirilmez. Belirsiz oranlar, referans ve içerik
özellikleri hâlâ açık konulardır; kapsam dışına almak veri hatasını çözmek değildir.

## Açık sınırlar ve sonraki işler

14 lexical özellik çıkarımı uygulanmıştır; backend entegrasyonu ve model
eğitimi yapılmamıştır. API'nin eski extractor'ı ve fallback güven yüzdeleri
bu yeni şemanın servis edildiği anlamına gelmez. Sertifika geçerliliği,
domain yaşı, sayfa HTML'si ve referans skorları bu sürümde yoktur.
Sayfa özellikli orijinal veri kaynak olarak korunur; ayrı bir içerik akışı
istenirse ona özel veri erişim/çıkarım sözleşmesi gerekir.

Host gruplaması registered-domain/kampanya bağımsızlığı sağlamaz. Önceki
deneylerde görülen veri dış test yerine geçmez. Kişisel veri içerebilen URL
metadata'sı herkese açık raporlara veya depoya yüklenmemelidir.

Veri: Prasad ve Chandra (2024), PhiUSIIL, UCI, CC BY 4.0.
https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset
