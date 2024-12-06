# Program
# Rancangan Simulasi Antrian Python:
# -Tambah Nasabah
# -Hitung Waktu Tunggu
# -Manajemen Loket
# -Statistik Pelayanan



import queue
import random
import time

class Nasabah:
    def __init__(self, id_nasabah, prioritas=False):
        self.id_nasabah = id_nasabah
        self.prioritas = prioritas
        self.waktu_tunggu = 0  # Waktu tunggu sebelum dilayani
    def __lt__(self, other):
        return self.prioritas < other.prioritas

class Loket:
    def __init__(self, id_loket):
        self.id_loket = id_loket
        self.sedang_melayani = None
        
    def layani(self):
        if self.sedang_melayani:
            print(f"Loket {self.id_loket} sedang melayani Nasabah {self.sedang_melayani.id_nasabah}")
            # Simulasi waktu pelayanan contoh 3 menit
            time.sleep(3)
            print(f"Nasabah {self.sedang_melayani.id_nasabah} selesai dilayani di Loket {self.id_loket}")
            self.sedang_melayani = None
        else:
            print(f"Loket {self.id_loket} tidak ada nasabah untuk dilayani")

    def tambah_nasabah(self, nasabah):
        self.sedang_melayani = nasabah

class Antrian:
    def __init__(self):
        self.antrian_normal = queue.Queue()
        self.antrian_prioritas = queue.PriorityQueue()

    def tambah_nasabah(self, nasabah):
        if nasabah.prioritas:
            self.antrian_prioritas.put((0, nasabah))  # Prioritas lebih tinggi, nilai prioritas 0
        else:
            self.antrian_normal.put(nasabah)

    def proses_antrian(self, lokets):
        # Proses antrian, pilih loket yang kosong dan layani nasabah
        for loket in lokets:
            if loket.sedang_melayani is None:
                if not self.antrian_prioritas.empty():
                    _, nasabah = self.antrian_prioritas.get()
                    loket.tambah_nasabah(nasabah)
                elif not self.antrian_normal.empty():
                    nasabah = self.antrian_normal.get()
                    loket.tambah_nasabah(nasabah)

    def hitung_waktu_tunggu(self):
        total_waktu_tunggu = 0
        total_nasabah = 0

        for nasabah in list(self.antrian_normal.queue):
            total_waktu_tunggu += nasabah.waktu_tunggu
            total_nasabah += 1
        for _, nasabah in list(self.antrian_prioritas.queue):
            total_waktu_tunggu += nasabah.waktu_tunggu
            total_nasabah += 1

        if total_nasabah > 0:
            return total_waktu_tunggu / total_nasabah
        return 0

    def statistik_pelayanan(self):
        print(f"Antrian prioritas: {self.antrian_prioritas.qsize()} nasabah")
        print(f"Antrian normal: {self.antrian_normal.qsize()} nasabah")
        print(f"Waktu tunggu rata-rata: {self.hitung_waktu_tunggu()} detik")

def simulasi():
    # Inisialisasi loket dan antrian
    lokets = [Loket(i) for i in range(1, 4)]  # Tiga loket
    antrian = Antrian()

    # Menambah nasabah (beberapa nasabah prioritas dan normal)
    for i in range(10):
        prioritas = random.choice([True, False])
        nasabah = Nasabah(i+1, prioritas)
        antrian.tambah_nasabah(nasabah)
        print(f"Nasabah {nasabah.id_nasabah} {'prioritas' if prioritas else 'normal'} ditambahkan ke antrian")

    # Proses antrian (layani nasabah)
    for _ in range(5):  # Misal, kita hanya melayani 5 kali dalam simulasi ini
        antrian.proses_antrian(lokets)
        for loket in lokets:
            loket.layani()
        time.sleep(1)  # Menunggu 1 detik untuk simulasi proses berikutnya

    # Statistik pelayanan
    antrian.statistik_pelayanan()

# Menjalankan simulasi
simulasi()
