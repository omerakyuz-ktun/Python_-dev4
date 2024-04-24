import sqlite3

def metinleri_sqlite_kaydet(metin1, metin2):
  conn = sqlite3.connect('benzerlik.db')
  c = conn.cursor()

  c.execute("CREATE TABLE IF NOT EXISTS metinler (id INTEGER PRIMARY KEY AUTOINCREMENT, metin TEXT)")

  c.execute("DELETE FROM metinler")
  c.execute("INSERT INTO metinler (metin) VALUES (?)", (metin1,))
  c.execute("INSERT INTO metinler (metin) VALUES (?)", (metin2,))

  conn.commit()
  conn.close()

def metinleri_al():

  conn = sqlite3.connect('benzerlik.db')
  c = conn.cursor()

  c.execute("SELECT metin FROM metinler")
  metinler = c.fetchall()

  conn.close()
  return metinler

def benzer_kelimeleri_bul(metin1, metin2):
  kelimeler1 = metin1.split()
  kelimeler2 = metin2.split()

  benzer_kelimeler = {}
  sayac = 0
  for kelime in kelimeler1:
    if kelime in kelimeler2:
      if kelime not in benzer_kelimeler:
        benzer_kelimeler[kelime] = []
      benzer_kelimeler[kelime].append(sayac)
      sayac += 1

  ortak_kelime_sayisi = len(benzer_kelimeler)
  toplam_kelime_sayisi = len(kelimeler1) + len(kelimeler2) - ortak_kelime_sayisi

  benzerlik_orani = (ortak_kelime_sayisi / toplam_kelime_sayisi)

  metin1_yeni = ""
  for i, kelime in enumerate(kelimeler1):
    if kelime in benzer_kelimeler:
      metin1_yeni += f"{kelime} ({','.join(str(x) for x in benzer_kelimeler[kelime])}) "
    else:
      metin1_yeni += f"{kelime} "

  metin2_yeni = ""
  for i, kelime in enumerate(kelimeler2):
    if kelime in benzer_kelimeler:
      metin2_yeni += f"{kelime} ({','.join(str(x) for x in benzer_kelimeler[kelime])}) "
    else:
      metin2_yeni += f"{kelime} "

  print("**İki metinde de kullanılan ortak kelimeler numaralandırılıyor...**")
  print(f"Metin 1 : {metin1_yeni}")
  print(f"Metin 2 : {metin2_yeni}")
  print(f"Benzerlik Katsayısı: {benzerlik_orani:.2f}")

  with open("benzerlik_durumu.txt", "w") as f:
    f.write(f"Metin 1 : {metin1_yeni}\nMetin 2 : {metin2_yeni}\n\nBenzerlik Katsayısı: {benzerlik_orani:.2f}")

def main():

  metin1 = input("Birinci metni giriniz: ")
  metin2 = input("Ikinci metni giriniz: ")

  metinleri_sqlite_kaydet(metin1, metin2)
  metinler = metinleri_al()

  benzer_kelimeleri_bul(metinler[0][0], metinler[1][0])

if __name__ == "__main__":
  main()