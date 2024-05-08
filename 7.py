import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QComboBox

class SporTakipUygulamasi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spor Takip Uygulaması")
        self.arayuz_olustur()
        self.veritabani_baglantisi_olustur()

    def arayuz_olustur(self):
        self.duzen = QVBoxLayout()

        # Heading
        self.heading_label = QLabel("SPOR TAKİP UYGULAMASI")
        self.heading_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.duzen.addWidget(self.heading_label)

        # Sporcu Adı
        self.sporcu_label = QLabel("Sporcu Adı:")
        self.sporcu_input = QLineEdit()
        self.duzen.addWidget(self.sporcu_label)
        self.duzen.addWidget(self.sporcu_input)

        # Spor Dalı
        self.spor_dali_label = QLabel("Spor Dalı Seçin:")
        self.spor_dali_combobox = QComboBox()
        self.spor_dali_combobox.addItems(["Futbol", "Voleybol", "Basketbol", "Fitness", "Golf", "Masa Tenisi", "Jimnastik"])
        self.duzen.addWidget(self.spor_dali_label)
        self.duzen.addWidget(self.spor_dali_combobox)

        # Antrenman Detayları
        self.antrenman_detay_label = QLabel("Antrenman Detayları:")
        self.antrenman_detay_input = QTextEdit()
        self.duzen.addWidget(self.antrenman_detay_label)
        self.duzen.addWidget(self.antrenman_detay_input)

        # Takip Bilgisi
        self.takip_bilgisi_label = QLabel("Takip Bilgisi:")
        self.takip_bilgisi_input = QTextEdit()
        self.duzen.addWidget(self.takip_bilgisi_label)
        self.duzen.addWidget(self.takip_bilgisi_input)

        # Kaydet Button
        self.kaydet_button = QPushButton("Kaydet")
        self.kaydet_button.setStyleSheet("background-color: #7B68EE ; color: white;")
        self.kaydet_button.clicked.connect(self.kaydet)
        self.duzen.addWidget(self.kaydet_button)

        # Kaydedilen Bilgiler Paneli
        self.kaydedilen_bilgiler_paneli = QTextEdit()
        self.duzen.addWidget(self.kaydedilen_bilgiler_paneli)

        self.setLayout(self.duzen)

    def veritabani_baglantisi_olustur(self):
        try:
            self.veritabani_baglantisi = sqlite3.connect('spor_takip.db')
            self.cursor = self.veritabani_baglantisi.cursor()
            self.cursor.execute('''DROP TABLE IF EXISTS Antrenmanlar''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Antrenmanlar
                            (id INTEGER PRIMARY KEY,
                            sporcu_adi TEXT,
                            spor_dali TEXT,
                            antrenman_detay TEXT,
                            takip_bilgisi TEXT)''')
            print("Table created successfully")  # Add this line for debugging
            self.veritabani_baglantisi.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Veritabanına bağlanırken bir hata oluştu: {str(e)}")

    def kaydet(self):
        try:
            sporcu_adi = self.sporcu_input.text().strip()
            spor_dali = self.spor_dali_combobox.currentText()
            antrenman_detay = self.antrenman_detay_input.toPlainText().strip()
            takip_bilgisi = self.takip_bilgisi_input.toPlainText().strip()

            if sporcu_adi and spor_dali and antrenman_detay and takip_bilgisi:
                self.cursor.execute("INSERT INTO Antrenmanlar (sporcu_adi, spor_dali, antrenman_detay, takip_bilgisi) VALUES (?, ?, ?, ?)",
                                    (sporcu_adi, spor_dali, antrenman_detay, takip_bilgisi))
                self.veritabani_baglantisi.commit()
                
                # Show a QMessageBox with the entered information
                QMessageBox.information(self, "Başarılı", 
                    f"""Sporcu Adı: {sporcu_adi}
Spor Dalı: {spor_dali}
Antrenman Detayları: {antrenman_detay}
Takip Bilgisi: {takip_bilgisi}
Bilgiler başarıyla kaydedildi!""")

                self.kaydedilen_bilgileri_goster()  # Update the displayed information
            else:
                QMessageBox.warning(self, "Uyarı", "Lütfen tüm bilgileri girin.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Veritabanına bilgi eklenirken bir hata oluştu: {str(e)}")

    def kaydedilen_bilgileri_goster(self):
        try:
            self.cursor.execute("SELECT * FROM Antrenmanlar")
            kaydedilen_bilgiler = self.cursor.fetchall()
            self.kaydedilen_bilgiler_paneli.clear()
            for bilgi in kaydedilen_bilgiler:
                self.kaydedilen_bilgiler_paneli.append(f"Sporcu Adı: {bilgi[1]}\nSpor Dalı: {bilgi[2]}\nAntrenman Detayları: {bilgi[3]}\nTakip Bilgisi: {bilgi[4]}\n\n")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Kaydedilen bilgiler alınırken bir hata oluştu: {str(e)}")

    def closeEvent(self, event):
        self.veritabani_baglantisi.close()
        event.accept()

if __name__ == "__main__":
    uygulama = QApplication(sys.argv)
    pencere = SporTakipUygulamasi()
    pencere.show()
    sys.exit(uygulama.exec_())
