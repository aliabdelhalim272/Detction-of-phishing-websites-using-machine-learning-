# İlk EDA kararları

## Kabul edilen akademik araştırma sorusu ve hipotez

**Research question:** How effectively can recorded URL and webpage features
distinguish phishing websites from legitimate websites?

**H₀:** The distribution of recorded URL length is the same for phishing and
legitimate websites.

**H₁:** The distribution of recorded URL length differs between phishing and
legitimate websites.

Bu iki yönlü hipotez, dağılımlar görüldükten sonra kabul edildiği için keşifseldir.
Değişken kayıtlı URLLength, gruplar kaynak label=0 phishing ve label=1 meşrudur.
Ölçüm tanımı belirsizliği ve host/URL bağımlılığı korunur; sonuç gerçek metin
uzunluğuna veya nedenselliğe genellenmez. İnceleme eğitim verisinde yapılacaktır.
Hipotezin uygulaması ana notebook'un 15. bölümündedir; güncel sayısal sonuç
`reports/hypothesis/result.json` dosyasında tutulur.

## İlk veri incelemesinin yöntem kararları

Bu belge ilk altı bölümün yöntem kararlarını açıklar. Sayısal bulguların kaynağı
`notebooks/01_eda.ipynb` ve `reports/initial_audit/` çıktılarıdır.

1. **Ham veri değişmez.** Dosya SHA-256 özeti kaydedilir ve çalışma sonunda
   tekrar kontrol edilir. Kaynak satır numarası pandas'ın sıfırdan başlayan
   veri satırı indeksidir; CSV başlığı bu numaraya dahil değildir.
2. **Tekrar URL otomatik silinmez.** Tam satır tekrarları ile aynı URL'nin
   farklı özellikli ölçümleri ayrı incelenir. Aynı URL'deki etiket çelişkileri
   ayrımı durdurur. Yinelenen kayıtların eğitim ağırlığı sonraki karardır.
3. **Öğrenilen dönüşüm uygulanmaz.** Eksikler, negatifler, yer tutucular ve
   sonsuz sayılar denetlenir; global doldurma, ölçekleme veya kırpma yapılmaz.
4. **Sabit host bazlı ayrım.** URL'den ayrıştırılan hostname IDNA biçimine
   çevrilir, küçük harf ve sondaki nokta normalizasyonu yapılır. Yaklaşık
   60/20/20 host grubu, sabit 42/43 tohumlarıyla ayrılır. Satır oranları ve
   sınıf oranlarının tam eşitliği garanti edilmez. Etiketlere göre tohum aranmaz.
5. **Üçlü ayrım doğrulanır.** Kümeler arasında kaynak satırı, URL ve host
   örtüşmesi olmaması kontrol edilir. Kaynak/ayar kilidi ve satır manifesti
   yerelde tutulur; kaynak veya ayrım değişirse yeniden çalışma durur.
6. **Sınırlar korunur.** Host gruplaması registered-domain veya kampanya
   bağımsızlığı değildir. Kayıt başına güvenilir zaman bilgisi doğrulanmadığından
   zamansal ayrım yapılmaz. Önceki deneylerde veri görüldüğü için yeni ayrım
   hiç görülmemiş dış test olarak sunulamaz.
7. **Eğitim EDA'sı tamamlandı.** Dağılımlar, sabit sütunlar, aykırı değerler,
   hedef ilişkileri, korelasyon ve özellik kökeni yalnızca eğitim verisinde
   incelendi. Akademik ön işleme ve modelleme sırası ana notebook'un
   12. bölümündedir; akademik modelleme henüz uygulanmadı.

## 11. bölümden hazırlık kararlarına aktarılacaklar

- `reports/provenance/feature_inventory.csv` 56 alanı kapsar. Ölçüm temeli
  kategorileri değerlendirmedir; orijinal formülün doğrulandığı anlamına gelmez.
- `URLSimilarityIndex`, `TLDLegitimateProb`, `URLCharProb` için referans
  evreni, hedef kullanımı, öğrenme örneklemi ve hesaplama zamanı belirsizdir.
  Sızıntı var/yok sonucu kesinleştirilmemiştir.
- Kayıtlı özellikler, tanımları ve ölçüm belirsizlikleriyle birlikte incelenir.
  Kaynak değerler sessizce farklı formüllerle değiştirilmez.
- Sayfa ölçümlerindeki güçlü ayrımlar, toplama koşulları ve olası erişim
  başarısızlıklarıyla birlikte yorumlanır; model başarısının kanıtı değildir.
- Kaynakta `label=0` phishing, `label=1` meşrudur. Modelleme ve metriklerde
  pozitif sınıf phishing olacaksa dönüşüm açıkça kaydedilmelidir.
- Kategorik encoding ve ölçekleme yalnız eğitimde öğrenilir; kimlik ve hedef
  alanları model girdilerinin dışında tutulur.
- Ana notebook'un 12. bölümünde hocanın gerekliliklerine uygun akademik
  ön işleme, iki model, karşılaştırma, yorum ve teslim akışı tanımlanmıştır.

## Akademik ham X/y şeması — uygulanan ilk ön işleme

- Ana notebook'un 13. bölümünde 56 kaynak sütunun her biri için kullanım
  kararı ve gerekçe İngilizce tabloda kaydedildi.
- X: 47 kayıtlı sayısal özellik ve TLD (kategorik). Kaynak sayfa özellikleri
  dahil tutulur; ölçüm tanımlarındaki belirsizlikler geçerlidir.
- FILENAME, URL, Domain girdiden ayrıldı; kimlik/grup metadata'sında korundu.
  Title ayrı metin analizi tasarlanmadığı için ilk deneyden çıkarıldı.
- URLSimilarityIndex, TLDLegitimateProb ve URLCharProb referans kökeni ve
  hesaplama zamanı belirsizliği nedeniyle ana deneyde kullanılmıyor.
  Bu karar sızıntının kanıtlandığı anlamına gelmez.
- y = 1 - label, phishing=1. Kaynak label da türetilmiş hedef de X içinde değil.
- Kayıtlı gözlemler silinmedi; eski URLLength/IsHTTPS/ratio sütunları sessizce
  farklı bir formülle değiştirilmedi. Orijinal host partition atamaları korundu.
- İndeks/hedef eşleşmesi, sonlu sayısal değerler, eksiksiz TLD ve kümeler
  arasında satır/URL/host örtüşmesinin olmaması kontrol edilir.
- X/y notebook belleğinde hazırdır. Encoding, scaling, hipotez testi ve
  model eğitimi bu adımda uygulanmaz. Ön işleme sonraki adımda yalnız
  eğitimde fit edilecek pipeline ile tamamlanacaktır.

## Eğitimde öğrenilen encoding ve scaling

- 14. bölümde TLD için OneHotEncoder eğitim kategorilerini öğrenir;
  bilinmeyen kategoriler TLD bloğunda sıfır vektörü olarak işlenir.
- Doğrusal model dalında 47 sayısal alan StandardScaler ile yalnız eğitimde
  öğrenilen ortalama/varyans kullanılarak ölçeklenir. Ağaç modeli dalında
  sayısal değerler korunur; iki dal da aynı TLD göstergelerini üretir.
- ColumnTransformer/Pipeline kullanılır; doğrulama ve testte yalnız transform
  uygulanır. Öğrenilen parametrelerin değişmediği, matris boyutları, sonluluk
  ve yapay bilinmeyen kategori davranışı notebook'ta doğrulanır.
- İmputation, kırpma, model fit veya hipotez testi uygulanmadı. Kategorileri
  yeniden gruplamak için holdout performansı kullanılmadı.
- Çapraz doğrulama gerekirse her fold'da ön işleme yeniden fit edilmeli;
  mevcut tüm eğitimde hazırlanmış matrisler bu amaçla doğrudan bölünmemelidir.

## Keşifsel hipotez değerlendirmesi

- Soru iki dağılımın farklı olup olmadığıdır; yalnız medyan testi yapılmaz.
- Her eğitim hostname'inden bir kayıt seed=20261121 ile etikete/uzunluğa
  bakılmadan seçilir. Tüm satırların özeti de betimsel referans olarak gösterilir.
- ECDF'ler arasındaki maksimum fark D hesaplanır. Sürekli dağılım varsayımına
  dayalı KS p-değeri kullanılmaz; bağlı/kesikli uzunluklar üzerinde sabit
  sınıf sayılı 1.999 etiket permütasyonu ile p tahmin edilir.
- Monte Carlo p=(aşım+1)/(B+1), en küçük raporlanabilir değer 0,0005'tir.
  Bu çözünürlük sınırında sonuç kesin p olarak yorumlanmaz. Alfa=0,05'tir.
- Host temsilcilerinin H₀ altında değiştirilebilirliği varsayılır. Registered-domain
  veya kampanya bağımlılığı sürebileceğinden sonuç bağımsız doğrulama değildir.
- Etki büyüklükleri D, medyan farkı ve bağlı değerleri içeren sıra etkisidir.
  Kayıtlı uzunluk tanımı belirsizliği ve EDA sonrası seçim açıkça raporlanır.
- Model veri tabloları değiştirilmez; model eğitimi uygulanmaz.

## Model karşılaştırma protokolü

- Majority baseline, Logistic Regression ve Random Forest aynı eğitim /
  doğrulama ayrımıyla karşılaştırılır; test bu adımda skorlanmaz.
- Logistic Regression (C=1, lbfgs, max_iter=2000) ve Random Forest (200 ağaç,
  max_depth=20, min_samples_leaf=2, seed=42) ayarları doğrulama ölçümünden
  önce sabitlenmiştir. Sınıf ağırlığı, resampling ve hiperparametre araması yoktur.
- Öğrenilen modeller ham X'ten başlayan kendi ön işleme pipeline'larını
  eğitimde fit eder. Önceden tüm eğitimde dönüştürülmüş matrisler dışarıdan
  modele verilmez; sonraki CV gerekirse tüm pipeline fold içinde fit edilmelidir.
- Pozitif sınıf phishing=1, eşik=0,5. Accuracy yanında phishing precision,
  recall, F1, balanced accuracy, FP/FN ve confusion matrix raporlanır.
- Tercih iki öğrenilen aday arasında doğrulama phishing F1 ile belirlenir;
  eşitlikte recall, yine eşitlikte daha basit Logistic Regression seçilir.
- İç doğrulama farkı istatistiksel üstünlük, dış genelleme veya nihai test
  başarısı olarak sunulmaz. Son test raporu ayrı bir adım olacaktır.

## Kontrollü özellik azaltma deneyi

- 48 özgün özellikli Random Forest referanstır. Ek özellik üretilmez;
  tek bir en fazla 20 özgün özellikli aday denenir.
- Orijinal eğitimin içinde %20 host grubu holdout (seed=142) ayrılır.
  Aynı RF pipeline'ının kopyası inner eğitimde fit edilir; permutation
  importance inner holdout içinden sabit seçilen en fazla 4.000 kayıt üzerinde,
  3 tekrar ve seed=42 ile ölçülür. Başlangıç ve karıştırılmış skorlar aynı
  kayıtlarda ve aynı 0,5 eşikte hesaplanır; fonksiyon içinde alt örnekleme
  yapılmaz. Orijinal validasyon sıralamayı kurmak için kullanılmaz.
- Inner eğitimde mutlak Spearman >=0,90 grafiğinin her bileşeninden en
  yüksek önem sıralı temsilci alınır; eşitlikte özellik adı kullanılır.
  İlk 20 temsilci tek aday kümesini oluşturur. Bu sezgisel tarama, bileşen
  üyelerinin kesin eşdeğer veya gereksiz olduğunu kanıtlamaz.
- Aynı RF ayarları ve 0,5 eşikle tüm eğitimde yeniden fit edilen küçük
  aday orijinal doğrulamada karşılaştırılır. Küçük aday yalnız F1 ve recall
  birlikte gerilemiyorsa seçilir; aksi halde tam model korunur.
- Sonuca bakarak özellik sayısı/eşik taraması yapılmaz. Üç tekrarın sapması
  güven aralığı değildir; korelasyon ve örnekleme önem skorlarını etkileyebilir.
- Sonuçlar `reports/feature_reduction/` altında; nihai tercih yeni protokol
  dosyasındadır. Önceki model karşılaştırması başlangıç referansı olarak kalır.

## Son test için sabitlenen kararlar

- Test skoru üretilmeden önce dosyaya yazılan protokol:
  `reports/final_evaluation/frozen_protocol.json`. Özellik sırası, ayarlar,
  kaynak/manifest hash'leri ve ortam sürümleri kaydedilir; farklı içerikle
  sessizce üzerine yazılmaz.
- Ana aday, doğrulama kuralıyla seçilen 20 özellikli Random Forest'tır.
  200 ağaç, max_depth=20, min_samples_leaf=2, seed=42, eşik=0,5 sabittir.
- Model yeniden eğitilmez; eğitimde fit edilmiş pipeline testte yalnız
  tahmin üretir. Tahminden önce/sonra model durumunun değişmediği denetlenir.
- Majority baseline, 48 alanlı Logistic Regression, 48 alanlı tam RF ve
  20 alanlı azaltılmış RF raporlanır. Ana seçim test sonucuyla değiştirilmez.
- Test 47.583 kayıt içerir. Accuracy, phishing precision/recall/F1,
  balanced accuracy, ROC-AUC, average precision, FP/FN ve confusion matrix
  sunulur; doğrulama/test farkları yüzde puan olarak kaydedilir.
- Sonuçlar `reports/final_evaluation/status.json` ve `test_metrics.csv`
  içinde tutulur. Test sonrası ayar/özellik/eşik araması yapılmaz. Kayıtlı
  ölçümler ve önceki veri görülme geçmişi nedeniyle dış genelleme iddiası yoktur.

### Değerlendirme ve veri kaynakları

- [PhiUSIIL, UCI](https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset)
- [GroupShuffleSplit, scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html)
