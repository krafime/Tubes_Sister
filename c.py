import json, xmlrpc.client, os, time
from prettytable import PrettyTable as pt

# define client
proxy = xmlrpc.client.ServerProxy('http://192.168.18.77:6667')
# set size layar
screen = os.get_terminal_size().columns

try:
  # deklarasi method fitur yang ada
  
  def hapus():
    # menghapus tampilan
    time.sleep(0.5)
    clear = lambda: os.system("cls")
    clear()

  def menu_awal():
    # tampilan menu awal
    hapus()
    print("+" * 62)
    print(" " * 10, "Pendaftaran Antrean Rumah Sakit GoHealth", " " * 10)
    print("+" * 62, "\n\n")

    print("1. Pendaftaran pasien baru")
    print("2. Pendaftaran pasien lama")
    print("3. Keluar")
    print()

  def menu_poli():
    hapus()
    # tampilkan menu poli
    print("Daftar Poli")
    print("1. Poli Mata")
    print("2. Poli Gigi")
    print("3. Poli Bedah")
    print()

  def poli(x):
    # input pasien pada poli, bila poli yang dipilih salah maka program keluar
    global idx_pasien
    if x not in [1, 2, 3]:
      print("\nMasukan salah! Program keluar.\n\n")
      hapus()
      exit
    else:
      if x == 1:    # add pasien ke list poli mata
        pesan = proxy.add_mata(idx_pasien)
        print(pesan)

      elif x == 2:  # add pasien ke list poli gigi
        pesan = proxy.add_gigi(idx_pasien)
        print(pesan)

      else:         # add pasien ke list poli bedah
        pesan = proxy.add_bedah(idx_pasien)
        print(pesan)

      hapus()   # setelah proses add pasien ke poli, maka layar akan dibersihkan dan melanjutkan proses

  def bukti_daftar(x, nama, tanggal_lahir): # x = poli yang dipilih
    # tampilkan bukti bahwa pasien telah mendaftar di poli yang dipilih
    global idx_pasien
    
    # data_all = proxy.get_pasien() # mendapatkan data seluruh pasien di rumah sakit
    # data_all = json.loads(data_all)

    # mendapatkan seluruh data pasien yang telah mendaftar
    data_pasien_daftar = proxy.get_pasien_daftar()
    data_pasien_daftar = json.loads(data_pasien_daftar)
    
    # mendapatkan data seluruh pasien yang mendaftar di suatu poli
    data_poli = data_pasien_daftar[x - 1] 
    
    # mendapatkan banyaknya pasien yang sudah daftar di suatu poli
    banyak_pasien_poli = len(data_pasien_daftar[x - 1])  
    
    # mendapatkan nomor antrean pasien saat ini
    nomor_antrean = str(banyak_pasien_poli)
    
    # mendapatkan data pasien saat ini
    pasien = data_poli[banyak_pasien_poli - 1]["pasien"]
    
    # mendapatkan estimasi pelayanan pasien saat ini
    estimasi_layanan = data_poli[banyak_pasien_poli - 1]["waktu"] 
        
    # header
    print("\033[1m" + "Bukti Pendaftaran Online".center(screen) + "\033[0m")
    print("Rumah Sakit GoHealth".center(screen))
    print(f"ANTRIAN {nomor_antrean}".center(screen))
    print(f"{estimasi_layanan}".center(screen))
    print("Terima Kasih".center(screen))
    print("---------------------------------------".center(screen))

    # data_pendaftar
    print("\033[1m" + "\n" + "Data Pendaftar" + "\n" + "\033[0m")
    print("No. RM\t: ", pasien["rm"])
    print("NIK\t: ", pasien["nik"])
    print("Nama\t: ", pasien["nama"])
    print("Alamat\t: ", pasien["alamat"])
    print()

    # list_antrean
    print("\033[1m" + "\nList Pasien\n" + "\033[0m")
    tab = pt(["No. Antrean", "Nama", "Estimasi Dilayani"])  # membuat tabel untuk menampilkan 3 pasien terakhir yang terdaftar
    if banyak_pasien_poli <= 3: # mengisi tabel jika pasien yang terdaftar di suatu poli <= 3
      for i in range(0, banyak_pasien_poli):
        tab.add_row([data_poli[i]["antrean"], data_poli[i]["pasien"]["nama"], data_poli[i]["waktu"][23:]])
    else:
      for i in range((banyak_pasien_poli - 3), banyak_pasien_poli):
        tab.add_row([data_poli[i]["antrean"], data_poli[i]["pasien"]["nama"], data_poli[i]["waktu"][23:]])
    print(tab)
    tab.clear_rows()

  while (True):
  # looping forever untuk menampilkan program terus menerus
    menu_awal(); operasi = input("Pilihan : "); hapus()

    if operasi == "1":
    # pendaftaran Pasien Baru
      print("Pendaftaran Pasien Baru".center(screen) + "\n")
      nik = input("NIK : ") ##
      nama = input("Nama : ")
      jenis_kelamin = input("Jenis Kelamin (P / L) : ") ##
      tempat_lahir = input("Tempat Lahir : ")
      tanggal_lahir = input("Tanggal Lahir (dd/mm/yy) : ") ##
      hp = input("HP : ")
      alamat = input("Alamat : ")
      penjamin = input("Nama Penjamin : ")

      new_pasien = [
                    nik, nama, jenis_kelamin, tempat_lahir, tanggal_lahir, hp, alamat, penjamin
                   ]

      pesan = proxy.add_pasien(new_pasien); print(pesan)

      idx_pasien = proxy.search_pasien(nik, nama, tanggal_lahir) # mendapatkan index pasien

      menu_poli(); x = int(input("Pilihan Poli : "))
      poli(x); bukti_daftar(x, nama, tanggal_lahir)

    elif operasi == "2":
      print("Data Pasien")
      id = input("NIK / No RM : ")
      nama = input("Nama : ")
      tanggal_lahir = input("Tanggal Lahir (dd/mm/yy) : ")

      idx_pasien = proxy.search_pasien(id, nama, tanggal_lahir)  # mendapatkan index pasien

      if idx_pasien != -1:
        print("\nPasien ditemukan! --melanjutkan proses pendaftaran\n")

        menu_poli(); x = int(input("Pilihan Poli : "))
        poli(x); bukti_daftar(x, nama, tanggal_lahir)

      else:
        print("\nPasien tidak ditemukan!")
        hapus()

    else:
      print("Keluar dari Program")
      exit()

    print("\n\n\n")
    repeat = input("Ingin kembali ke menu awal? (Y/T) : ")
    hapus()

    if not (repeat == "Y" or repeat == "y"):
      print("TERIMA KASIH TELAH MENGGUNAKAN APLIKASI PENDAFTARAN ONLINE")
      exit()

except KeyboardInterrupt:
  print("\n\n\n!!!Program Keluar!!!")
