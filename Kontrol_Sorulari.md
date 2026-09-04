# Bölüm 2: Kontrol Soruları ve Yanıtları

### 1. `list` yerine `deque` kullanılması gereken senaryo ve Big-O gerekçesi
* **Senaryo:** Gerçek zamanlı bir log akış sisteminde veya anlık mesaj kuyruğunda (FIFO queue), verilerin sürekli olarak listenin en başından eklenip çıkarılması (`popleft()` veya `appendleft()`).
* **Big-O Gerekçesi:** `list` arka planda dinamik dizi kullandığı için sol tarafa ekleme/çıkarma yapmak $O(N)$ maliyetlidir (elemanların bellekte tek tek kaydırılması gerekir). `deque` (double-ended queue) ise çift yönlü bağlı liste mantığıyla çalıştığı için her iki uctan ekleme ve çıkarma işlemleri **$O(1)$** sabit zamanlıdır.

### 2. Decorator'da `functools.wraps` kullanılmazsa ne kaybedilir?
* **Meta Veri Kaybı:** Sarmalanan orijinal fonksiyonun `__name__` (adı), `__doc__` (dokümantasyonu) ve `__annotations__` bilgileri silinir; yerine sarmalayan (wrapper) fonksiyonun bilgileri geçer.
* **Hata Ayıklama ve Test Sorunları:** `pytest` gibi test framework'leri veya `help()` gibi araçlar fonksiyonu yanlış tanır. Stack trace loglarında hata orijinal fonksiyon yerine wrapper içinde görünür, bu da debugging sürecini zorlaştırır.

### 3. `Protocol` ile `ABC` (Abstract Base Class) arasındaki fark
* **Fark:** `ABC` **nominal subtyping** (isimsel kalıtım) uygular; sınıfın o mimariden türediğini açıkça belirtmesi (`class A(Base):`) şarttır. `Protocol` ise **structural subtyping** (yapısal / duck typing) uygular; kalıtım zorunluluğu yoktur, sınıfın ilgili metodik imzalara sahip olması yeterlidir.
* **Örnek:** `Yazici` adında bir `Protocol` içinde `bas()` metodu tanımlıysa, `Sinif` adındaki başka bir sınıf hiçbir miras almadan doğrudan içine `bas()` metodu yazarsa Python tarafından o protokola uygun kabul edilir. `ABC` kullanılsaydı `class Sinif(Yazici):` şeklinde kalıtım alınması zorunlu olurdu.

### 4. 100 GB'lık CSV'yi 8 GB RAM'de işlemek için 3 strateji
* **Parçalı Okuma (Chunking):** Pandas `read_csv` fonksiyonunun `chunksize` parametresi kullanılarak veri setinin örneğin 100 binlik bloklar halinde RAM'e alınıp işlenmesi.
* **Lazy Evaluation (Polars / Dask):** Veriyi anında belleğe yüklemek yerine optimize edilmiş bir işlem planı çıkaran Polars Lazy API veya Dask kütüphaneleriyle verinin akış modunda işlenmesi.
* **Gömülü Veritabanı Kullanımı (DuckDB / SQLite):** Büyük CSV dosyasının DuckDB gibi bellek dostu bir analitik veritabanına aktarılıp, tüm filtreleme ve dönüşümlerin disk üzerinden SQL sorgularıyla yapılması.

### 5. `pytest` fixture `scope` parametresi ve veritabanı testindeki seçimi
* **Görevi:** Bir fixture fonksiyonunun ne sıklıkla çalıştırılacağını ve önbelleğe (cache) alınacağını belirler (`function`, `class`, `module`, `session`).
* **Veritabanı Testindeki Seçim:** Genellikle **`session`** veya **`module`** seçilir. Her test fonksiyonu için (`function` scope) sıfırdan veritabanı ayağa kaldırmak test sürecini felç edecek kadar yavaşlatır. `session` skoru ile tüm testler boyunca bir kez veritabanı kurulur, testler bittiğinde temizlenir.