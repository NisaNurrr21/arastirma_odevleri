# Veri İşleme Kodu Nasıl Test Edilir?

Veri mühendisliğinde en büyük tehlike, kodun hata verip çökmesi değil, **sessiz veri bozulmasıdır (silent data corruption)**. Standart birim testleri (unit tests) fonksiyonların mantığını doğrulamak için harikadır; ancak milyonlarca satırlık veri akışlarında (ETL/ELT) şema kaymaları, beklenmeyen null değerler veya mantıksal tutarsızlıklar ancak veriye özel test stratejileriyle yakalanabilir.

## 1. Şema Testi (Schema Testing)
Gelen verinin yapısal bütünlüğünü garanti altına alır. Verinin içindeki değerlerden ziyade formatsal sözleşmelere (contracts) odaklanır. `Pandera` veya `Pydantic` gibi araçlarla entegre edilir.
* **Ne İşe Yarar?** Üretim ortamında bir API'den veya kaynaktan gelen veri setinde beklenmeyen bir sütun adının değişmesi veya veri tipinin `Integer` yerine `String` gelmesi durumunda pipeline'ı anında durdurarak sistemin bozuk veriyle beslenmesini engeller.

## 2. İnvaryant Testi (Invariant Testing)
Verinin içeriği veya boyutu nasıl değişirse değişsin, iş mantığı gereği **asla ihlal edilmemesi gereken evrensel kuralların** test edilmesidir.
* **Ne İşe Yarar?** Örneğin bir e-ticaret sepet analizinde `toplam_tutar` hiçbir zaman kalemlerin toplamından küçük olamaz veya stok miktarları negatif bir değere düşemez. Bu tür matematiksel değişmezler kod içerisinde assert kurallarıyla sürekli denetlenir.

## 3. Altın Dosya (Golden File) Testi
Karmaşık dönüşüm mantıkları, pencere fonksiyonları (window functions) ve join operasyonları içeren devasa çıktıların her satırını manuel kontrol etmek imkansızdır.
* **Ne İşe Yarar?** Uzmanlar tarafından doğrulanmış, %100 hatasız referans bir çıktı dosyası (**golden file**) proje deposunda saklanır. Kodda her değişiklik yapıldığında üretilen yeni çıktı, bayt bazında bu altın dosya ile karşılaştırılarak beklenmeyen bir yan etki (regression) oluşup oluşmadığı anlaşılır.

## 4. Özellik Tabanlı Test (Property-Based Testing)
Geliştiricinin test yazarken akıl edemeyeceği uç durumları (edge cases) otomatik olarak keşfetmek için kullanılır. `Hypothesis` gibi kütüphaneler yardımıyla verinin özellikleri tanımlanır.
* **Ne İşe Yarar?** Test aracı, koda yüzlerce farklı rastgele, anormal, aşırı büyük veya boş girdi vererek kodun çöküp çökmediğini veya mantıksal hata verip vermediğini stres testine tabi tutar.