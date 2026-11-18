# PhiUSIIL sütun sözlüğü

Bu sözlük yerel CSV'deki 56 sütunu açıklar. **Bir alanın anlamını bilmek,
orijinal çıkarım formülünü veya CSV ile birebir uyumunu doğrulamak değildir.**
Sütunların yazım hataları CSV ile eşleşmesi için korunmuştur.

## Kaynaklar ve doğrulama durumu

- **U:** [UCI veri kaydı](https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset).
  Etiket anlamı, FILENAME alanının göz ardı edilebilmesi, sütun listesi ve genel
  veri kapsamı için birincil kaynak. Her sütunun ayrıntılı formülünü sunmaz.
- **C:** [Yazarın CharConRate.ipynb dosyası](https://github.com/arvindbitm/PhiUSIIL/blob/main/CharConRate.ipynb).
- **T:** [Yazarın WebPageTitleMatchScore.ipynb dosyası](https://github.com/arvindbitm/PhiUSIIL/blob/main/WebPageTitleMatchScore.ipynb).
- [Yazarın reposu](https://github.com/arvindbitm/PhiUSIIL) ve
  [ilişkili makale](https://doi.org/10.1016/j.cose.2023.103545).
  Makalenin tam metnine araştırma sırasında erişilemedi; okunmuş kabul edilmedi.

**U-doğrudan:** Belirtilen anlam UCI'de açıkça açıklanıyor.
**Kod bulundu:** Yazarın uygulaması incelendi, yerel CSV ile sayısal uyum henüz sınanmadı.
**Yorum:** Sütun adından çıkarılan çalışma açıklaması; kesin algoritma doğrulanmadı.
Yorum durumundaki satırların kaynağı UCI formülleri değil, açıkça bu yorumdur.
Özelliklerin tamamının doğrulandığı iddia edilmez.

## Sütunlar

| Sütun | Türkçe çalışma açıklaması | Grup / kullanım amacı | Durum | Kaynak |
|---|---|---|---|---|
| FILENAME | Kaynak dosya kimliği; UCI göz ardı edilebileceğini belirtir. | İzlenebilirlik; model girdisi değil | U-doğrudan | U |
| URL | Kaydedilmiş web adresi. | Ham metin, tekrar kontrolü ve host çıkarımı | Yorum | Sütun adı |
| URLLength | Kaydedilmiş URL uzunluğu; hangi gösterimin sayıldığı doğrulanmalı. | URL / uzunluk | Yorum | Sütun adı |
| Domain | Kaydedilmiş domain veya host metni. | Domain / gruplama adayı; registered-domain olduğu varsayılmaz | Yorum | Sütun adı |
| DomainLength | Kaydedilmiş domain uzunluğu. | Domain / uzunluk | Yorum | Sütun adı |
| IsDomainIP | Domain yerine IP adresi kullanımı göstergesi. | URL-domain / gösterge | Yorum | Sütun adı |
| TLD | Kaydedilmiş üst seviye alan adı uzantısı. | Kategorik özellik adayı | Yorum | Sütun adı |
| URLSimilarityIndex | URL benzerlik skoru; referans kümesi ve algoritma ayrıca doğrulanmalı. | Referans tabanlı skor / köken incelemesi | Yorum | Sütun adı |
| CharContinuationRate | Karakter türlerine göre en uzun kesintisiz dizileri kullanan oran. | Türetilmiş karakter özelliği | Kod bulundu | C |
| TLDLegitimateProb | Uzantıyla ilişkili meşruluk olasılığı olarak yorumlanan değer; hangi evrenden hesaplandığı belirsiz. | Referans tabanlı istatistik / sızıntı incelemesi | Yorum | Sütun adı |
| URLCharProb | URL karakterleriyle ilişkili olasılık skoru; referans dağılımı ve formülü doğrulanmalı. | Referans tabanlı karakter istatistiği | Yorum | Sütun adı |
| TLDLength | Kaydedilmiş uzantı uzunluğu. | Domain / uzunluk | Yorum | Sütun adı |
| NoOfSubDomain | Kaydedilmiş alt alan adı sayısı; www ve çok parçalı uzantı kuralları doğrulanmalı. | Domain / sayım | Yorum | Sütun adı |
| HasObfuscation | URL gizleme veya kodlama tekniği algılanması göstergesi. | URL / gösterge | Yorum | Sütun adı |
| NoOfObfuscatedChar | Gizlenmiş/kodlanmış kabul edilen karakter sayısı; algılama kuralı belirsiz. | URL / sayım | Yorum | Sütun adı |
| ObfuscationRatio | Gizlenmiş/kodlanmış karakter oranı; payda doğrulanmalı. | URL / oran | Yorum | Sütun adı |
| NoOfLettersInURL | URL'deki harf sayısı; sayılan URL parçası ve karakter kümesi doğrulanmalı. | URL / sayım | Yorum | Sütun adı |
| LetterRatioInURL | Harf oranı; kullanılan payda doğrulanmalı. | URL / oran | Yorum | Sütun adı |
| NoOfDegitsInURL | URL'deki rakam sayısı; özgün yazım korunmuştur. | URL / sayım | Yorum | Sütun adı |
| DegitRatioInURL | Rakam oranı; payda doğrulanmalı, özgün yazım korunmuştur. | URL / oran | Yorum | Sütun adı |
| NoOfEqualsInURL | URL'deki eşittir işaretlerinin sayısı. | URL / sayım | Yorum | Sütun adı |
| NoOfQMarkInURL | URL'deki soru işaretlerinin sayısı. | URL / sayım | Yorum | Sütun adı |
| NoOfAmpersandInURL | URL'deki ampersand işaretlerinin sayısı. | URL / sayım | Yorum | Sütun adı |
| NoOfOtherSpecialCharsInURL | Diğer özel karakterlerin sayısı; karakter listesi doğrulanmalı. | URL / sayım | Yorum | Sütun adı |
| SpacialCharRatioInURL | Özel karakter oranı; karakter listesi ve payda doğrulanmalı. | URL / oran | Yorum | Sütun adı |
| IsHTTPS | HTTPS kullanım göstergesi olarak yorumlanır; sertifika geçerliliği değildir. | URL / gösterge | Yorum | Sütun adı |
| LineOfCode | Sayfanın kaynak kodundaki satır sayısı olarak yorumlanır. | Sayfa içeriği / sayım | Yorum | Sütun adı |
| LargestLineLength | Kaynak koddaki en uzun satırın uzunluğu olarak yorumlanır. | Sayfa içeriği / uzunluk | Yorum | Sütun adı |
| HasTitle | Sayfa başlığının bulunması göstergesi. | Sayfa içeriği / gösterge | Yorum | Sütun adı |
| Title | Kaydedilmiş sayfa başlık metni. | Ham metin / özellik adayı | Yorum | Sütun adı |
| DomainTitleMatchScore | Başlık parçalarının dönüştürülmüş domain metniyle eşleşme skoru. | Başlık-domain / türetilmiş skor | Kod bulundu | T |
| URLTitleMatchScore | Başlık parçalarının dönüştürülmüş URL metniyle eşleşme skoru. | Başlık-URL / türetilmiş skor | Kod bulundu | T |
| HasFavicon | Site simgesinin bulunması göstergesi. | Sayfa içeriği / gösterge | Yorum | Sütun adı |
| Robots | Robot yönergeleriyle ilişkili gösterge; robots.txt mi yoksa HTML metadata mı olduğu doğrulanmalı. | Sayfa / anlam ayrıntısı belirsiz | Yorum | Sütun adı |
| IsResponsive | Duyarlı sayfa tasarımı algılanması göstergesi; ölçüm kuralı belirsiz. | Sayfa davranışı / gösterge | Yorum | Sütun adı |
| NoOfURLRedirect | URL yönlendirme sayısı olarak yorumlanır; 0/1 gözlenmesi tek başına tanımı değiştirmez. | Yönlendirme / sayım adayı | Yorum | Sütun adı |
| NoOfSelfRedirect | Kendine yönlendirme sayısı olarak yorumlanır; kendine yönlendirme kuralı belirsiz. | Yönlendirme / sayım adayı | Yorum | Sütun adı |
| HasDescription | Sayfa açıklamasının bulunması göstergesi. | Sayfa içeriği / gösterge | Yorum | Sütun adı |
| NoOfPopup | Açılır pencere sayısı; statik veya çalıştırılarak algılama yöntemi belirsiz. | Sayfa / sayım | Yorum | Sütun adı |
| NoOfiFrame | iframe öğelerinin sayısı. | Sayfa içeriği / sayım | Yorum | Sütun adı |
| HasExternalFormSubmit | Harici hedefe veri gönderen form göstergesi; harici tanımı doğrulanmalı. | Form / gösterge | Yorum | Sütun adı |
| HasSocialNet | Sosyal ağ bağlantısı veya içeriği algılanması göstergesi; kapsam belirsiz. | Sayfa içeriği / gösterge | Yorum | Sütun adı |
| HasSubmitButton | Form gönderme düğmesi bulunması göstergesi. | Form / gösterge | Yorum | Sütun adı |
| HasHiddenFields | Gizli form alanı bulunması göstergesi. | Form / gösterge | Yorum | Sütun adı |
| HasPasswordField | Parola giriş alanı bulunması göstergesi. | Form / gösterge | Yorum | Sütun adı |
| Bank | Bankacılıkla ilişkili ifade göstergesi; aranılan metin alanı ve sözlük doğrulanmalı. | Anahtar kelime / gösterge | Yorum | Sütun adı |
| Pay | Ödemeyle ilişkili ifade göstergesi; eşleme kuralı doğrulanmalı. | Anahtar kelime / gösterge | Yorum | Sütun adı |
| Crypto | Kriptoyla ilişkili ifade göstergesi; eşleme kuralı doğrulanmalı. | Anahtar kelime / gösterge | Yorum | Sütun adı |
| HasCopyrightInfo | Telif hakkı bilgisi algılanması göstergesi. | Sayfa içeriği / gösterge | Yorum | Sütun adı |
| NoOfImage | Görsel sayısı; hangi öğelerin sayıldığı doğrulanmalı. | Sayfa kaynakları / sayım | Yorum | Sütun adı |
| NoOfCSS | CSS kaynağı sayısı; satır içi ve harici CSS kapsamı doğrulanmalı. | Sayfa kaynakları / sayım | Yorum | Sütun adı |
| NoOfJS | JavaScript kaynağı sayısı; satır içi ve harici script kapsamı doğrulanmalı. | Sayfa kaynakları / sayım | Yorum | Sütun adı |
| NoOfSelfRef | Aynı siteye yönelen referans sayısı; host veya registered-domain kuralı belirsiz. | Bağlantılar / sayım | Yorum | Sütun adı |
| NoOfEmptyRef | Boş kabul edilen referans sayısı; boş dize, # vb. kapsamı doğrulanmalı. | Bağlantılar / sayım | Yorum | Sütun adı |
| NoOfExternalRef | Harici referans sayısı; harici hedef kuralı doğrulanmalı. | Bağlantılar / sayım | Yorum | Sütun adı |
| label | Kaynak sınıf etiketi: 0 phishing, 1 meşru. | Hedef; model girdisi olamaz | U-doğrudan | U |

## Yazarın kodundan elde edilen ayrıntılar

### CharContinuationRate

Fonksiyon, girdideki en uzun ardışık harf, rakam ve diğer karakter dizilerinin
uzunluklarını toplayıp girdi uzunluğuna böler. Paylaşılan çağrı akışı domain
alanındaki protokolü, başlangıç www parçasını ve son noktadan sonraki uzantıyı
çıkarır. Bu nedenle tam URL üzerinde aynı fonksiyonu çağırmak eşdeğer sayılmaz.
Bu bir entropi tanımı değildir. Uygulamanın yerel CSV ile uyumu henüz sınanmadı.

### Başlık eşleşme skorları

Kod, başlığı boşluklardan parçalara ayırır. URL/domain metninden protokol,
www, kayıtlı TLD ve eğik çizgi parçalarını çıkarır. Başlık parçalarının
eşleşen uzunluklarından yüzde tabanlı bir skor toplar ve eşleşen metni siler;
99,9 üzerini 100'e çeker. Büyük/küçük harf ve boş girdi davranışı önemlidir.
Paylaşılan notebook'ta hata çıktıları da vardır; eksiksiz üretim kodu veya
CSV'ye birebir uygunluk kanıtı olarak değerlendirilmez.

## Kullanım sınırı

Bu sözlük bir özellik seçimi listesi değildir. Bir özelliğin anlamı makul olsa
bile canlıda aynı şekilde üretilebilmesi, referans veri kullanımı ve etiket
sızıntısı ayrıca incelenir. CSV üzerinde sonraki formül kontrolleri eğitim
kayıtlarında yapılmalı; test dağılımları karar üretmek için kullanılmamalıdır.
