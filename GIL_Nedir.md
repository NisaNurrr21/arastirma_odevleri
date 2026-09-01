# Python'da GIL (Global Interpreter Lock) Nedir?

Python'un standart derleyicisi olan CPython, bellek yönetimini "Reference Counting" (Referans Sayımı) adı verilen bir yöntemle yapar. Bellekteki bir nesneye kaç farklı değişkenin ihtiyaç duyduğu sayılır; bu sayı sıfıra düştüğünde nesne bellekten silinir. 

Eğer birden fazla iş parçacığı (thread) aynı anda bu referans sayılarını değiştirmeye kalkarsa veri bozulmaları yaşanır. CPython bu kaosu önlemek için **GIL (Global Interpreter Lock)** kilit mekanizmasını kullanır. GIL, aynı anda yalnızca **tek bir iş parçacığının** Python kodunu çalıştırmasına izin veren mutlak bir köprü bekçisidir.

## Ne Zaman Engel Olur? (CPU-Bound İşlemler)
İşlemcinin (CPU) tam kapasite çalıştığı matematiksel hesaplamalar ve devasa döngüler **CPU-bound** (işlemciye bağlı) görevlerdir. Bu durumlarda `threading` kullanmak performansı artırmaz.

**Benchmark Testimiz:**
Testimizde 50 milyonluk bir matematiksel sayma işlemini iki farklı thread'e böldük ve işlem **0.92 saniye** sürdü. Thread'ler gerçekten paralel çalışabilseydi süre yarıya düşerdi. Ancak GIL kilidi nedeniyle thread'ler sıraya girdi; biri sayım yaparken diğeri kilitli kalıp beklediği için hiçbir hız kazanımı sağlanamadı.

## Ne Zaman Engel Olmaz? (I/O-Bound İşlemler)
API'den veri çekmek, veritabanına sorgu atmak veya diske dosya yazmak **I/O-bound** (girdi/çıktı) işlemlerdir. Bu süreçlerde işlemci hesaplama yapmaz, sadece ağdan veya diskten gelecek veriyi bekler. Python bu bekleme durumlarında **GIL kilidini otomatik olarak serbest bırakır.** 

**Benchmark Testimiz:**
Testimizde `time.sleep(1)` ile 1 saniyelik bir API bekleme simülasyonunu iki thread ile çalıştırdık. GIL burada sistemi kilitleseydi sürenin 2 saniye olması gerekirdi, ancak test **1.01 saniye** içinde bitti. Yani Python ilk thread beklemeye geçtiği an GIL'i açtı, ikinci thread de aynı anda görevine başladı ve kusursuz bir eş zamanlılık yakalandı.

## Çözüm Yolları
Veri mühendisliği süreçlerinde GIL darboğazını aşmanın temel yolları:
* **Multiprocessing:** Thread'ler yerine tamamen ayrı süreçler (process) başlatmak. Her sürecin kendi bağımsız belleği ve GIL kilidi olur.
* **C/Rust Uzantıları:** Hesaplama yükünü Python döngüleri yerine, Polars veya Numpy gibi veriyi C/Rust tarafında işleyip GIL'i bypass eden kütüphanelere devretmek.