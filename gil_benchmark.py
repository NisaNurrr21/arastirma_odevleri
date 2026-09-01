import time
import threading

def cpu_yogun_islem():
    # GIL'in kilitlediği senaryo: Ağır matematiksel döngü
    sayac = 0
    for _ in range(50_000_000):
        sayac += 1

def io_yogun_islem():
    # GIL'in serbest kaldığı senaryo: API veya disk beklemesi simülasyonu
    time.sleep(1) 

def test_et(fonksiyon, isim):
    baslangic = time.perf_counter()
    
    # İki farklı thread (veznedar) oluşturup aynı görevi veriyoruz
    t1 = threading.Thread(target=fonksiyon)
    t2 = threading.Thread(target=fonksiyon)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    sure = time.perf_counter() - baslangic
    print(f"[{isim}] Toplam Süre: {sure:.2f} saniye")

if __name__ == "__main__":
    print("GIL Benchmark Testi Başlıyor...\n" + "-"*30)
    test_et(cpu_yogun_islem, "CPU-Bound (Hesaplama)")
    test_et(io_yogun_islem, "I/O-Bound (API Beklemesi)")