# İlk EDA kararları

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
   incelendi. Bulgular [veri hazırlama planına](data_preparation_plan.md)
   dönüştürüldü; planlanan temizleme ve özellik işlemleri henüz uygulanmadı.

## 11. bölümden hazırlık kararlarına aktarılacaklar

- `reports/provenance/feature_inventory.csv` 56 alanı kapsar. Kullanılabilirlik
  kategorileri değerlendirmedir; orijinal formülün doğrulandığı anlamına gelmez.
- `URLSimilarityIndex`, `TLDLegitimateProb`, `URLCharProb` için referans
  evreni, hedef kullanımı, öğrenme örneklemi ve hesaplama zamanı belirsizdir.
  Sızıntı var/yok sonucu kesinleştirilmemiştir.
- URL'den üretilebilecek yeni özellikler de mevcut CSV alanlarıyla otomatik
  eşdeğer değildir. Açık isim, formül, sürüm, hata ve normalizasyon politikası gerekir.
- Sayfa ölçümleri URL metninden elde edilemez; veri kümesindeki güçlü ayrımlar
  canlı kullanılabilirlik kanıtı değildir. Güncel sayfayı tekrar indirmek de
  eski gözlemin HTML'sini yeniden elde etmek anlamına gelmez.
- Backend beş URL özelliği üretir. Kaynakta `label=1` meşru, backend'de
  `prediction=1` phishing yorumlanır. Eğitim/servis hedef sözleşmesi açık olmalıdır.
- Backend yalnız statik olarak incelendi; tahmin modeli veya API değiştirilmedi.
- 12. bölümde önerilen hazırlık akışı ve açık sorular yazıldı. Mevcut API
  kapsamına uygun ilk URL-only teslim önerisi, içerik seçeneğinden ayrıldı.
  Ortak modül, temiz CSV ve ekip entegrasyonu henüz uygulanmadı.

### Kaynaklar

- [PhiUSIIL, UCI](https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset)
- [GroupShuffleSplit, scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html)
