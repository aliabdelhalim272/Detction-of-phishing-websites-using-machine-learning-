# 12. EDA sonucu ve veri hazırlama yol haritası

## 12.1. Kapsam ve durum

EDA'daki bulgular bu belgede hazırlık kararlarına dönüştürülür. **Bu belge bir
uygulama planıdır; aşağıdaki işlemler henüz uygulanmadı.** Şu ana kadar ham
veri ve eğitim kayıtları değişmedi; ayrım manifesti ve EDA raporları üretildi.
Temiz CSV, ortak özellik çıkarma modülü veya eğitilmiş model henüz üretilmedi.

Mevcut API yalnız URL metniyle çalıştığı için önerilen ilk teslim **URL-only**
bir veri/özellik sözleşmesidir. İçerik tabanlı araştırma ayrı bir seçenek olarak
korunur; bu öneri içerik özelliklerinin yararsız veya hatalı olduğu anlamına gelmez.
Ekip içerik toplama seçeneğini benimserse onun veri erişim ve çıkarım sözleşmesi
ayrıca hazırlanmalıdır.

## 12.2. Kanıttan karara

| Konu | Kanıt / bölüm | Planlanan işlem | Gerekçe / sınır | Durum |
|---|---|---|---|---|
| Ham veri | SHA-256 ve 235.795 kaynak kayıt; 2–4 | Orijinali salt kaynak olarak koru; çıktıları ayrı üret | İzlenebilirlik ve yeniden üretim | Mevcut koruma sürer |
| Eksik ve sonsuz değerler | Taranan alanlarda yok; 4 | Bu sürümde doldurma uygulama; yeni veri için doğrulama ekle | Sorun yokken global imputation gereksiz | Planlandı |
| Etiket | Kaynak 0 phishing, 1 meşru; 2 ve 11 | Teslimde is_phishing = 1 - label; orijinal etiketi metadata'da koru | API 1'i phishing yorumluyor; çift hedef girdiye giremez | Planlandı |
| Tekrar URL | 425 ek kayıt, 850 gözlem; özellikler farklı, etiket çelişkisi yok; 5 | URL-only çıktıda aynı extractor aynı girdiyi ürettikten sonra exact URL başına ilk kaynak satırını temsilci seç; tüm kaynak satırı eşlemesini sakla | Bu akışta aynı URL aynı yeni X ve y üretir. Kayıtlı içerik özellikleri için rastgele temsilci seçilmez | URL-only için planlandı |
| Ayrım | Sabit host ayrımı ve örtüşme kontrolleri; 6 | Var olan partition atamalarını koru; temsilci satır partition'ı devralır | Satır seçimi sonrası yeni seed arama yok | Planlandı |
| Domain farkları | Eğitimde 18 hostname/netloc farkı; 6 ve 11 | Ham Domain'i koru; hostname'i URL parser ile ayrı metadata alanı üret | Port ve userinfo hostname değildir; modelde host kimliği kullanma | Planlandı |
| URLLength | Eğitimde 112.331 fark; 112.329'u -1; 6.2 | Yeni url_length alanını mevcut girdinin karakter sayısı olarak açıkça hesapla | Eski sütunu sessizce düzeltme; -1 sebebi doğrulanmadı | Planlandı |
| HTTPS | Şemayla 271 fark; metin içi https aramasıyla 0 fark; 11 | Yeni has_https yalnız parsed scheme == https olsun | Sertifika doğrulaması veya güvenlik kararı değildir | Planlandı |
| Karakter sayımı | =, ?, & ve oran formüllerinde farklar; 6.2 ve 10 | Yeni lexical sözleşmede sayılacak girdiyi ve karakterleri açık tanımla | Eski sayaç/ratio formüllerinin kopyalandığı iddia edilmez | Planlandı |
| Referans skorları | Köken/formül/zaman belirsiz; 9 ve 11 | URL-only ilk teslim X'ine URLSimilarityIndex, TLDLegitimateProb, URLCharProb alma | Tedbir ve erişilebilirlik kararı; sızıntı kanıtı olduğu söylenmez | Planlandı |
| Sayfa ve başlık alanları | API üretmiyor; kuvvetli sınıf farkları var; 9–11 | İlk URL-only X'ine içerik, başlık ve davranış alanlarını alma; kaynakta koru | Canlıda elde edilemeyen girdilerle model sözleşmesi kurulmaz | Planlandı |
| Aykırı değerler | 9 sıfır-IQR alan; diğerlerinde en az bir eşik dışı %52,02; 8 | Toplu IQR silme/kırpma yapma; açık doğrulama ihlallerini ayrı incele | İstatistiksel uçluk hata tanısı değildir | Planlandı |
| Sıfır yoğunluğu / korelasyon | 10 alan en az %95 sıfır; 7 yüksek korelasyon çifti; 7 ve 10 | Sırf sıfır oranı/korelasyon nedeniyle sütun eleme yapma | Tanım ve canlı kullanılabilirlik önce gelir; model katkısı Rol 2'de | Planlandı |
| TLD ve alt domain sayısı | Nadir kategoriler ve suffix kuralı belirsiz; 7 ve 11 | İlk lexical sözleşmeye TLD encoding ve subdomain sayısı ekleme | Belgeli PSL/suffix politikası olmadan kestirme nokta sayımıyla taklit etme | İlk sürüm kapsam kararı |
| Fitted preprocessing | Veri dönüşümü henüz fit edilmedi | Imputer/scaler/encoder/threshold seçimlerini Rol 2'ye bırak; yalnız train'de fit | Doğrulama/testten öğrenme yok | Rol 2 aktarımı |
| API ve değerlendirme | 5 özellik, farklı hedef/özellik kuralları; 11 | Ortak extractor ve hedef sürümüyle entegrasyon için teslim şartı yaz | API bu plan sırasında değiştirilmez; eski model tak-çalıştır değildir | Sonraki ekip işi |

**Önemli tekrar ayrımı:** Kayıtlı 56 sütunlu gözlemlerden birini daha doğru
olduğu varsayımıyla silmiyoruz. URL-only tabloda yeniden hesaplanmış X ve y'nin
aynılığı doğrulanırsa gereksiz çoklu ağırlığı önlemek için tek temsilci seçmeyi
planlıyoruz. URL'deki harf büyüklüğü, sorgu sırası veya percent-encoding'i
değiştirerek yeni bir URL eşitliği uydurulmaz; exact URL politikası kullanılır.

## 12.3. Önerilen ortak özellik sözleşmesi: url_lexical_v1

Henüz kodlanmamış ilk sürüm taslağıdır. HTTP(S) şeması açıkça verilmeli;
eksik şema otomatik uydurulmamalı. Boş, bozuk host/port veya kontrol karakterli
girdiler hata kaydıyla ayrılmalı; sessizce sıfır özellik üretmemeli.
Kabul edilen girdiler eğitim ve canlıda aynı fonksiyondan geçmeli.

| Alan | Önerilen açık tanım |
|---|---|
| url_length | Kabul edilen özgün URL metnindeki karakter sayısı |
| hostname_length | Parser'ın çıkardığı küçük harf hostname uzunluğu; IPv6 köşeli parantezleri hariç |
| has_at_symbol | Özgün girdide @ bulunması |
| has_dash | Özgün girdide - bulunması |
| count_dots | Özgün girdideki nokta sayısı; subdomain sayısı değildir |
| has_https | Ayrıştırılmış şemanın küçük harf biçimi https ise 1 |
| digit_count | Özgün girdide ASCII 0–9 sayısı |
| digit_ratio | digit_count / url_length |
| path_length | Percent-decoding yapılmadan path uzunluğu |
| query_length | Başındaki ? hariç query uzunluğu |
| count_query_parameters | Query'deki boş olmayan & ile ayrılmış parçaların sayısı |
| count_percent_escapes | Özgün girdide geçerli %HH dizilerinin sayısı |
| hostname_is_ip | Standart IPv4/IPv6 literal hostname ise 1 |
| has_explicit_port | Geçerli açık port yazılmışsa 1 |

Hostname doğrulama/IDNA, Unicode uzunlukları, boşluk ve kullanıcı bilgisi
kuralları modülde belgelenip test edilmelidir. URL kimliği için kullanılan
özgün metin ile gruplama için normalize host ayrı tutulmalıdır. SSL sertifika
geçerliliği ve domain yaşı bu sürümde yoktur; bunlar ağ/registration kaynağı
gerektiren ayrı zenginleştirme işleridir. Uygulanmamış özellik teslim edilmiş sayılmaz.

## 12.4. Uygulama sırası

1. **Kaynak ve ayrımı doğrula.** Ham hash, sürümler ve manifest eşleşmeli;
   farklı veri veya ayarda dur. Mevcut atamalar otomatik yeniden oluşturulmasın.
2. **Ortak extractor'ı yaz ve sınır durumlarını test et.** Aynı input aynı
   isim/sıra/tip/değerleri üretmeli. Şema kontrolü sertifika kontrolü değildir.
3. **Özellikleri yeniden üret.** Girdiyi değiştirmeden deterministik lexical
   fonksiyonu uygula; geçersizleri sebebiyle karantinaya ayır. Öğrenilmiş
   dönüşüm yok. Protokol/path/query'yi keyfi normalize ederek kimlik değiştirme.
4. **URL-only tekrar politikasını uygula.** Exact URL gruplarında yeni X ve y
   eşitliğini doğrula; en küçük source_row'u temsilci seç. Aynı URL grubunda
   farklı partition veya çelişkili hedef bulunursa dur. Eşleme tablosu sakla.
5. **X, y ve metadata'yı ayır.** X yalnız sözleşmedeki sayısal alanlar;
   y is_phishing; source_row, URL, hostname_group, partition ve kaynak etiket
   metadata'da. Satır anahtarları ve manifest bağlantısı açık olsun.
6. **Çıktı denetimi yap.** Sayı dengesi, özellikler, hedef, temsilci/eşleme,
   grup örtüşmesi, karantina ve kaynak hash testleri geçsin. Ayrım satır
   sayıları temsilci seçiminden sonra değişebilir; gerçek sayılar raporlansın.
7. **Rol 2 ve backend'e aktar.** Dataset/extractor sürümü, özellik sırası,
   formüller, hedef anlamı, bağımlılıklar ve bilinen sınırları birlikte paylaş.
   İçerik modeli araştırması ayrı bir sözleşmeye tabi olsun.

## 12.5. Beklenen sonraki teslimler ve kabul ölçütleri

| Teslim | Tamamlanma ölçütü | Şu an |
|---|---|---|
| Ortak URL çıkarım modülü | Offline, deterministik; geçerli/geçersiz URL testleri ve training/serving parity | Planlandı, yazılmadı |
| Eğitime hazır lexical CSV | Sayısal X ve phishing=1 hedef; kimlik/hedef sızıntısı yok; manifest bağlantısı var | Üretilmedi |
| Metadata ve temsilci eşlemesi | Her kaynak satırı temsilciye veya gerekçeli karantinaya izlenebilir | Üretilmedi |
| Hazırlık raporu | Başlangıç/son sayıları, değişen alanlar, red sebepleri, sürüm ve hash | EDA raporu var; hazırlık raporu yok |
| Backend entegrasyonu | Aynı modül, schema ve hedef; eski fallback model güveni olarak sunulmuyor | Yapılmadı, ekip entegrasyonu |

Test örnekleri: HTTP/HTTPS ve büyük harf şema, URL içinde başka https metni,
userinfo (@), açık port, IPv4/IPv6, Unicode/IDNA, percent-encoding, boş query
parçaları, eksik şema, bozuk host/port, whitespace ve kontrol karakterleri.
URL'ler ziyaret edilmez. Ham ve üretilmiş büyük CSV'ler Git dışında tutulur.

## 12.6. Sonuçların sınırı

Önceki deneylerde aynı veri görülmüştür; mevcut test geriye dönük tamamen
dokunulmamış test değildir. Host ayrımı registered-domain, kampanya veya zaman
bağımsızlığı sağlamaz. Yeni dış/zamansal değerlendirme ayrıca gereklidir.
Bu EDA model başarısı, güvenli site kararı veya üretime hazır ürün iddiası sunmaz.

Kaynaklar: [sütun sözlüğü](data_dictionary.md), [yöntem kararları](eda_decisions.md),
[notebook](../notebooks/01_eda.ipynb) ve `reports/` altındaki denetim çıktıları.
