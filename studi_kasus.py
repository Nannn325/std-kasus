import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class QualityControlBotol:
    def __init__(self):
        self.data = pd.DataFrame(columns=['Timestamp', 'Berat1', 'Berat2', 'Berat3', 'Berat4', 'Berat5'])
        self.spec_limit = {'min': 590, 'max': 610}  # contoh batas spesifikasi (gram)
    
    def tambah_data(self, berat_botol):
        """Menambahkan data sampel baru"""
        if len(berat_botol) != 5:
            raise ValueError("Jumlah sampel harus 5 botol")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data = {'Timestamp': timestamp,
                    'Berat1': berat_botol[0],
                    'Berat2': berat_botol[1],
                    'Berat3': berat_botol[2],
                    'Berat4': berat_botol[3],
                    'Berat5': berat_botol[4]}
        
        self.data = self.data.append(new_data, ignore_index=True)
        print("Data berhasil ditambahkan pada", timestamp)
    
    def hitung_statistik(self):
        """Menghitung statistik untuk setiap sampel"""
        if self.data.empty:
            return None
            
        statistik = pd.DataFrame()
        berat_cols = ['Berat1', 'Berat2', 'Berat3', 'Berat4', 'Berat5']
        
        # Hitung mean, range, dan std dev untuk setiap sampel
        statistik['Timestamp'] = self.data['Timestamp']
        statistik['Mean'] = self.data[berat_cols].mean(axis=1)
        statistik['Range'] = self.data[berat_cols].max(axis=1) - self.data[berat_cols].min(axis=1)
        statistik['Std Dev'] = self.data[berat_cols].std(axis=1)
        
        return statistik
    
    def cek_kualitas(self):
        """Memeriksa apakah sampel memenuhi spesifikasi"""
        if self.data.empty:
            return None
            
        hasil_cek = pd.DataFrame()
        berat_cols = ['Berat1', 'Berat2', 'Berat3', 'Berat4', 'Berat5']
        
        # Cek setiap botol dalam sampel
        for col in berat_cols:
            hasil_cek[col] = self.data[col].between(self.spec_limit['min'], self.spec_limit['max'])
        
        # Cek apakah semua botol dalam sampel memenuhi spesifikasi
        hasil_cek['Semua_OK'] = hasil_cek.all(axis=1)
        
        return hasil_cek
    
    def plot_control_chart(self):
        """Membuat control chart untuk berat botol"""
        if self.data.empty:
            print("Tidak ada data untuk ditampilkan")
            return
            
        statistik = self.hitung_statistik()
        berat_cols = ['Berat1', 'Berat2', 'Berat3', 'Berat4', 'Berat5']
        
        plt.figure(figsize=(12, 8))
        
        # Plot X-bar chart (rata-rata sampel)
        plt.subplot(2, 1, 1)
        plt.plot(statistik['Timestamp'], statistik['Mean'], 'bo-', label='Rata-rata')
        plt.axhline(y=np.mean(self.data[berat_cols].values), color='g', linestyle='--', label='Grand Mean')
        plt.axhline(y=self.spec_limit['min'], color='r', linestyle=':', label='Batas Spesifikasi')
        plt.axhline(y=self.spec_limit['max'], color='r', linestyle=':')
        plt.title('X-bar Chart - Rata-rata Berat Botol per Sampel')
        plt.ylabel('Berat (gram)')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        
        # Plot R chart (range sampel)
        plt.subplot(2, 1, 2)
        plt.plot(statistik['Timestamp'], statistik['Range'], 'ro-', label='Range')
        plt.axhline(y=np.mean(statistik['Range']), color='g', linestyle='--', label='Rata-rata Range')
        plt.title('R Chart - Range Berat Botol per Sampel')
        plt.ylabel('Range (gram)')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()
    
    def generate_report(self):
        """Membuat laporan ringkasan"""
        if self.data.empty:
            return "Tidak ada data untuk dilaporkan"
            
        statistik = self.hitung_statistik()
        hasil_cek = self.cek_kualitas()
        
        report = f"""
        LAPORAN KONTROL KUALITAS BERAT BOTOL
        =====================================
        Periode: {self.data['Timestamp'].iloc[0]} sampai {self.data['Timestamp'].iloc[-1]}
        Jumlah Sampel: {len(self.data)}
        Jumlah Botol Diperiksa: {len(self.data) * 5}
        
        Spesifikasi Berat Botol: {self.spec_limit['min']}g - {self.spec_limit['max']}g
        
        Statistik Keseluruhan:
        - Rata-rata berat: {np.mean(self.data[['Berat1', 'Berat2', 'Berat3', 'Berat4', 'Berat5']].values):.2f}g
        - Standar Deviasi: {np.std(self.data[['Berat1', 'Berat2', 'Berat3', 'Berat4', 'Berat5']].values):.2f}g
        - Range rata-rata per sampel: {np.mean(statistik['Range']):.2f}g
        
        Kualitas Produk:
        - Jumlah sampel yang memenuhi spesifikasi: {sum(hasil_cek['Semua_OK'])} dari {len(hasil_cek)} ({sum(hasil_cek['Semua_OK'])/len(hasil_cek)*100:.1f}%)
        - Jumlah botol di luar spesifikasi: {len(hasil_cek)*5 - sum(hasil_cek[['Berat1', 'Berat2', 'Berat3', 'Berat4', 'Berat5']].sum())}
        """
        
        return report

# Contoh penggunaan
if __name__ == "__main__":
    qc = QualityControlBotol()
    
    # Simulasi input data setiap 4 jam selama 3 hari (18 sampel)
    np.random.seed(42)
    base_weight = 600  # berat target 600g
    for i in range(18):
        # Tambahkan variasi acak pada berat botol
        weights = np.random.normal(loc=base_weight, scale=3, size=5).round(1)
        qc.tambah_data(weights)
        
        # Update timestamp untuk simulasi
        if i > 0:
            qc.data.at[i, 'Timestamp'] = (datetime.strptime(qc.data.at[i-1, 'Timestamp'], "%Y-%m-%d %H:%M:%S") 
                                        + timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S")
    
    # Hitung statistik
    stats = qc.hitung_statistik()
    print("\nStatistik Sampel:")
    print(stats.head())
    
    # Cek kualitas
    quality_check = qc.cek_kualitas()
    print("\nHasil Pemeriksaan Kualitas:")
    print(quality_check.head())
    
    # Generate report
    print(qc.generate_report())
    
    # Tampilkan control chart
    qc.plot_control_chart()
