import json, threading, xmlrpc.server
import datetime
import random as rd

list_pasien = []                # list untuk menyimpan data seluruh pasien di rumah sakit
pasien_daftar = [[], [], []]    # list untuk menyimpan data seluruh pasien yang telah mendaftar, idx 0 = poli mata, idx 1 = poli gigi, idx 2 = poli bedah

def waktu(list): 
# tampilkan waktu perkiraan konsultasi di klinik atau fasilitas kesehatan
  today = datetime.datetime.now()   # mendapatkan waktu hari ini
  next_day = today + datetime.timedelta(days=1) # mendapatkan waktu besok hari
  start_layanan = datetime.datetime(next_day.year, next_day.month, next_day.day, 8, 30, 0)  # mengset waktu mulainya pelayanan klinik, pelayanan dimulai pukul 8.30
  
  selisih = len(list) * 30  # asumsi setiap pasien mendapat waktu layanan selama 30 menit
  layanan = start_layanan + datetime.timedelta(minutes=selisih) # mengset perkiraan waktu layanan untuk pasien yang mendaftar
  return layanan.strftime("%d %B %Y, pukul %H:%M")

def add_mata(idx):
# tambah pasien untuk poli mata
  p_mata = {'antrean': len(pasien_daftar[0]) + 1, 'pasien': list_pasien[idx], 'waktu': waktu(pasien_daftar[0])}
  pasien_daftar[0].append(p_mata)
  print(f"Pasien {list_pasien[idx]['rm']} ditambahkan ke antrean poli mata")
  return '\nPendaftaran di Poli Mata Berhasil!'

def add_gigi(idx):
# tambah pasien untuk poli gigi
  p_gigi = {'antrean': len(pasien_daftar[1]) + 1, 'pasien': list_pasien[idx], 'waktu': waktu(pasien_daftar[1])}
  pasien_daftar[1].append(p_gigi)
  print(f"Pasien {list_pasien[idx]['rm']} ditambahkan ke antrean poli gigi")
  return '\nPendaftaran di Poli Gigi Berhasil!'

def add_bedah(idx):
# tambah pasien untuk poli bedah
  p_bedah = {'antrean': len(pasien_daftar[2]) + 1, 'pasien': list_pasien[idx], 'waktu': waktu(pasien_daftar[2])}
  pasien_daftar[2].append(p_bedah)
  print(f"Pasien {list_pasien[idx]['rm']} ditambahkan ke antrean poli bedah")
  return '\nPendaftaran di Poli Bedah Berhasil!'

def rekamMedis():
# tampilkan rekam medis pasien
  rm = rd.randint(1111, 9999)
  for i in range(0, len(list_pasien)):  # cek apakah rm sudah ada atau belum, jika ada maka rm diganti
    if rm == list_pasien[i]['rm']:
      rm = rd.randint(1111, 9999)
  return rm

def add_pasien(new_pasien):
# tambah pasien baru
  pasien = {
    'rm': rekamMedis(),
    'nik': new_pasien[0],
    'nama': new_pasien[1],
    'jenis_kelamin': new_pasien[2],
    'tempat_lahir': new_pasien[3],
    'tanggal_lahir': new_pasien[4],
    'hp': new_pasien[5],
    'alamat': new_pasien[6],
    'penjamin': new_pasien[7]
  }

  list_pasien.append(pasien)
  print(f"Pasien baru dengan Rekam Medis {pasien['rm']} berhasil terdaftar di Rumah Sakit GoHealth")
  return '\nData Berhasil Ditambahkan --melanjutkan proses pendaftaran'

def search_pasien(id, nama, tanggal_lahir):
# mencari pasien berdasarkan id (rm / nik), nama, dan tanggal lahir di list_pasien
  found = -1
  i = 0
  while i < len(list_pasien):
    if (list_pasien[i]['rm'] == id or list_pasien[i]['nik'] == id) and list_pasien[i]['nama'] == nama and list_pasien[i]['tanggal_lahir'] == tanggal_lahir:
      found = i
    i = i + 1
  return found

def get_pasien():
# mengambil data seluruh pasien di rumah sakit
  data = json.dumps(list_pasien)
  return data

def get_pasien_daftar():
# mengambil data seluruh pasien yang sudah terdaftar di poli (dari list pasien_daftar)
  data = json.dumps(pasien_daftar)
  return data
  
def handle_server(server):
# method handler
  print('Server berhasil connect')
  
  # mendaftarkan method ke server
  server.register_function(add_pasien, "add_pasien")
  server.register_function(get_pasien, "get_pasien")
  server.register_function(get_pasien_daftar, "get_pasien_daftar")
  server.register_function(search_pasien, "search_pasien")
  server.register_function(add_mata, "add_mata")
  server.register_function(add_gigi, "add_gigi")
  server.register_function(add_bedah, "add_bedah")

  # running Server
  server.serve_forever()

server = xmlrpc.server.SimpleXMLRPCServer(("10.20.224.162", 6667))

# thread
t = threading.Thread(target=handle_server, args=(server, ))
t.start()
