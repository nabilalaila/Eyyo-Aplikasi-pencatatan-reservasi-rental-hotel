import csv
import os
import pandas as pd
from datetime import datetime #untuk menyesuaikan tanggal (ada yg 30 & 31)

def login():
    with open("dataadmin.csv", 'r') as datauser: #with open agar setelah buka lgsg tutup, r untuk membaca saja
        baca = csv.reader(datauser) #pasangan r line 7
        os.system("cls")
        print("-"*115)
        print("Masuk Aplikasi".center(115))
        print("-"*115)
        username = input('Username: ')
        password = input('Password: ')
        adaUser = False
        for row in baca:
            if row[0] == username and row[1] == password: #kolom
                adaUser = True
                break
        if adaUser == True:
            print('Selamat datang di Eyyo App! 😊')
        else:
            input('Yah, username/password yang kamu masukkan salah. Coba lagi yuk🙌\nTekan enter untuk lanjut => ')
            os.system("cls")
            login()

def check_username(username):
    with open("dataadmin.csv",'r') as datauser:
        baca = csv.reader(datauser)
        for row in baca:
            if row[0] == username:
                return True
        return False

def signup():
    with open("dataadmin.csv",'a+', newline='') as datauser: #a+ = append and read, newline agar di bawah
        nulis = csv.writer(datauser)
        print("-"*115)
        print("Daftar Akun".center(115))
        print("-"*115)
        username = input('Masukkan Username: ')
        password = input('Masukkan Password: ')
        if check_username(username):
            input('Yah, username sudah dipakai orang lain. Ganti yang lain yaa🙌\nTekan enter untuk lanjut => ')
            os.system("cls")
            signup()
        else:
            dataYangDitambah = [username, password]
            nulis.writerow(dataYangDitambah)
            os.system("cls")

def namapelanggan():
    global nomorreservasi, nama
    os.system("cls") 
    print("-" * 115)
    print("Nama Pelanggan".center(115)) 
    print("-" * 115)
    nama = input("Masukkan nama pelanggan => ")
    tanggal_hari_ini = datetime.now().date() #mengambil tanggal hari ini, krn format asli datetime tanggal & jam
    try:
        baca = pd.read_csv("History Reservasi.csv", header=None) #lihat csv tidak ada header, jadi satu baris
        rows = list(baca) #history jadi 1 list
        if len(rows) == 0: #jika tidak ada history
            nomorreservasi = f"{tanggal_hari_ini}-01" #-01 maka jadi history pertama
        else:
            nomorreservasi = f"{tanggal_hari_ini}-0{len(baca)+1}"
    except pd.errors.EmptyDataError:
        nomorreservasi = f"{tanggal_hari_ini}-01"

def filterhotelberdasarkanharga():
    os.system('cls')
    print("-" * 115)
    print("Pilih Range Harga Hotel".center(115))
    print("-" * 115)
    print("|1| Rp 100.000 - Rp 400.000\n|2| Rp 401.000 - Rp 700.000\n|3| Rp 701.000 - Rp 1.000.000")
    pilihan = input("Ketik 1/2/3 => ")
    os.system("cls")
    print("-" * 115)
    print("Hotel yang Tersedia".center(115))
    print("-" * 115)
    nomorhotel = 0 #supaya muncul nomor pada tampilan hotel sesuai range
    with open("Hotel+kamar.csv", 'r+') as daftarhotel, open("Tampunganpesananhotel.csv", 'r+', newline="") as tampungandata: #r+ read write
        baca = csv.reader(daftarhotel, delimiter=";") #delimiter = pemisah kolom, read hotel + kamar
        nulis = csv.writer(tampungandata) #nulisnya di tampungan pesanan hotel
        if pilihan in ["1", "2", "3"] :
            for row in baca:
                harga = int(row[3])
                if ((pilihan == "1" and 100000 <= harga <= 400000) or (pilihan == "2" and 401000 <= harga <= 700000) or (pilihan == "3" and 700000 <= harga <= 1000000)) and int(row[5]) >= 1 : #row 5 > 1 maka bisa dipesan, kalau 0 tidak bisa dipesan
                    nomorhotel += 1
                    print(f"{nomorhotel}. {row[0]}\n   Tipe Kamar          : {row[1]}\n   Alamat Hotel        : {row[2]}\n   Rating              : {row[4]}⭐\n   Harga per Malam     : Rp {row[3]}\n   Kamar yang Tersedia : {row[5]}\n")
                    global datayangditampung
                    datayangditampung = [row[0],row[1],row[2],row[4],row[3],row[5]]
                    nulis.writerow(datayangditampung)
            tampungandata.close()
            global pilihhotel
            pilihhotel = int(input("Pilih hotel yang akan dipesan dengan ketik nomornya => "))
            banyakKamar() #setelah milih hotel, akan diarahkan pada fungsi banyakKamar
        else:
            input("Wah, yang kamu ketik salah nih. Ketik 1/2/3 yaa\nKlik enter untuk lanjut => ")
            os.system("cls")
            filterhotelberdasarkanharga()

def banyakKamar():
    os.system("cls")
    print("-" * 115)
    print("Kamar yang Dipesan".center(115))
    print("-" * 115)
    global jumlahKamar, pesanankamar
    jumlahKamar = input("Ada berapa kamar yang ingin dipesan => ")
    read = pd.read_csv("Tampunganpesananhotel.csv", header=None)
    pesanankamar = list(read.iloc[pilihhotel-1]) #-1 karena pada csv dari 0, sedangkan di iloc mulai dari 1
    kamar = pesanankamar[5] #5 untuk ketersediaan kamar
    if jumlahKamar.isdigit() == True:
        if (int(kamar))-int(jumlahKamar) >= 0:
            tanggalmenginap()
        else:
            input(f"Jumlah kamar yang kamu masukkan terlalu banyak. Kamar yang tersedia hanya {int(kamar)}\nKlik enter untuk lanjut => ")
            banyakKamar()
    else:
        input("Wah, yang kamu ketik salah nih. Ketik berupa angka yaa\nKlik enter untuk lanjut => ")
        os.system("cls")
        banyakKamar()

def tanggalmenginap():
    os.system("cls")
    print("-" * 115)
    print("Lama Menginap".center(115))
    print("-" * 115)
    print("Kapan mulai menginap? (Jam check-in hotel jam 13.00)".center(115))
    global tanggal_checkin, bulan_checkin, tahun_checkin, tanggal_checkout, bulan_checkout, tahun_checkout
    tanggal_checkin = int(input("Tanggal                           => "))
    bulan_checkin = int(input("Bulan (Tulis dalam bentuk angka)  => "))
    tahun_checkin = int(input('Tahun                             => '))
    print("Kapan selesai menginap? (Jam check-out hotel jam 12.00)".center(115))
    tanggal_checkout = int(input("Tanggal                           => "))
    bulan_checkout = int(input("Bulan (Tulis dalam bentuk angka)  => "))
    tahun_checkout = int(input('Tahun                             => '))
    global checkin, checkout, hari_menginap, jumlah_hari_inap
    checkin = datetime(tahun_checkin, bulan_checkin, tanggal_checkin)
    checkout = datetime(tahun_checkout, bulan_checkout, tanggal_checkout)
    hari_menginap = checkout - checkin
    jumlah_hari_inap = hari_menginap.days
    os.system("cls")
    layanantambahan() 

def closing():
    os.system("cls")
    print("Apakah kamu ingin keluar dari aplikasi?".center(115))
    pilihtutup = input("|1| Ya, keluar\n|2| Kembali ke menu utama\nKetik 1/2 => ")
    if pilihtutup == "1":
        os.system("cls")
        print("Terimakasih sudah pakai Eyyo untuk catat reservasi pelanggan dan edit hotel".center(115))
        print("Semangat kerjanya dan see you on next chance 👋".center(115))
        print("- Eyyo Team -".center(115))
    elif pilihtutup == "2":
        menu()
    else:
        input("Wah, yang kamu ketik salah nih. Ketik 1/2 yaa\nKlik enter untuk lanjut => ")
        os.system("cls")
        closing()

def lanjut(): 
    os.system("cls")
    print("Yay, kamu berhasil melakukan pencatatatan 🥳".center(115))
    lanjutTidak = input("|1| Lanjut mencatatat lagi\n|2| Tutup aplikasi\n|3| Kembali ke menu awal\nKetik (1/2/3) => ")
    if lanjutTidak == "1":
        reservasi()
    elif lanjutTidak == "2":
        closing()
    elif lanjutTidak == "3":
        menu()
    else:
        input("Wah, yang kamu ketik salah nih. Ketik 1/2/3 yaa\nKlik enter untuk lanjut => ")
        os.system("cls")
        lanjut()

def pembayaran():
    os.system("cls")
    print("-" * 115)
    print("Konfirmasi Pembayaran".center(115))
    print("-" * 115)
    print("Apakah pelanggan sudah membayar?\n|1| Sudah\n|2| Belum")
    global confirm
    confirm = input("Ketik (1/2) => ")
    if confirm == "1":
        with open("History Reservasi.csv", "a", newline="") as historyreservasi:
            datareservasi = [nomorreservasi,nama,pesananfiks[0], pesananfiks[1], pesananfiks[2], jumlahKamar, checkin.strftime("%Y-%m-%d"), checkout.strftime("%Y-%m-%d"), hari_menginap.days, jenis_tambahan, totalKeseluruhan, "Sudah"]
            writer = csv.writer(historyreservasi)
            writer.writerow(datareservasi)
            historyreservasi.close()
            updatekamartersedia()
    elif confirm == "2":
        with open("History Reservasi.csv", "a", newline="") as historyreservasi:
            datareservasi = [nomorreservasi,nama,pesananfiks[0], pesananfiks[1], pesananfiks[2], jumlahKamar, checkin.strftime("%Y-%m-%d"), checkout.strftime("%Y-%m-%d"), hari_menginap.days, jenis_tambahan, totalKeseluruhan, "Belum"]
            writer = csv.writer(historyreservasi)
            writer.writerow(datareservasi)
            historyreservasi.close()
            updatekamartersedia()
    else:
        input("Wah, yang kamu ketik salah nih. Ketik 1/2 yaa\nKlik enter untuk lanjut => ")
        os.system("cls")
        pembayaran()

def updatekamartersedia():
    if confirm == "1" or "2":
        namahotel = pesananfiks[0]
        tipekamar = pesananfiks[1]
        with open("Hotel+kamar.csv", "r") as datahotel:
            reader = csv.reader(datahotel, delimiter=";")
            rows = list(reader)
            for i in range(1, len(rows)):
                if rows[i][0] == namahotel and rows[i][1] == tipekamar:
                    rows[i][5] = int(rows[i][5]) - int(jumlahKamar)
        with open("Hotel+kamar.csv", "w", newline="") as datahotel:
            writer = csv.writer(datahotel, delimiter=";")
            writer.writerows(rows)
    lanjut()

def rincianpemesanan():
    os.system("cls")
    print("-" * 115)
    print("Rincian Pemesanan".center(115))
    print("-" * 115)
    read = pd.read_csv("Tampunganpesananhotel.csv", header=None)
    global pesananfiks, totalhargahotel, totalKeseluruhan
    pesananfiks = list(read.iloc[pilihhotel-1])
    totalhargahotel = int(pesananfiks[4]*jumlah_hari_inap*int(jumlahKamar))
    totalKeseluruhan = totalhargahotel+harga_tambahan
    print(f"Nomor Reservasi    : {nomorreservasi}\nNama Pelanggan     : {nama}\n")
    print(f"{pesananfiks[0]}\nTipe Kamar           : {pesananfiks[1]}\nAlamat               : {pesananfiks[2]}\nRating               : {pesananfiks[3]}⭐\nTanggal              : {checkin.strftime('%d-%m-%Y')} - {checkout.strftime('%d-%m-%Y')}\nKamar yang Dipesan   : {jumlahKamar}")
    print(f"Harga                : Rp {int(pesananfiks[4])}/d X {jumlahKamar} Kamar X {(jumlah_hari_inap)} Hari\n                     : Rp {int(pesananfiks[4]*jumlah_hari_inap*int(jumlahKamar))}\nLayanan Tambahan     : {jenis_tambahan}\nHarga                : Rp {harga_tambahan}")
    print(f"Total Keseluruhan    : Rp {totalKeseluruhan}\n")
    choice = input("|1| Lanjut ke tahap berikutnya\n|2| Ganti hotel \n|3| Ganti tanggal menginap\n|4| Ganti layanan tambahan\n|5| Batalkan transaksi\nKetik (1/2/3/4/5) => ")
    if choice == "1":
        pembayaran()
    elif choice == "2":
        filterhotelberdasarkanharga()
    elif choice == "3":
        tanggalmenginap()
    elif choice == "4":
        layanantambahan()
    elif choice == "5":
        closing()
    else: 
        print(" 😮 Wah yang kamu ketik salah nih. Ketik (1/2/3/4/5) yaa 🙉".center(115))
        input("Klik enter untuk lanjut => ")
        os.system("cls")
        rincianpemesanan()    

def layanantambahan():
    os.system("cls")
    print("-" * 115)
    print("Layanan Tambahan Hotel".center(115))
    print("-" * 115)
    print("|1| Spa\n    Harga = Rp 150.000\n|2| Antar - Jemput Hotel\n    Harga = Rp 200.000\n|3| Spa dan Antar - Jemput Hotel\n    Harga = Rp 350.000 \n|4| Tidak Pesan\n|5| Batalkan Transaksi\n")
    global layanan, jenis_tambahan, harga_tambahan
    layanan = (input("Pilih dengan ketik (1/2/3/4/5) => "))
    jenis_tambahan = "-"
    harga_tambahan = 0
    if layanan == "1":
        jenis_tambahan = "Spa"
        harga_tambahan = 150000
        rincianpemesanan()
    elif layanan == "2":
        jenis_tambahan = "Antar - Jemput Hotel"
        harga_tambahan = 200000
        rincianpemesanan()
    elif layanan == "3":
        jenis_tambahan = "Spa dan Antar - Jemput Hotel"
        harga_tambahan = 350000
        rincianpemesanan()
    elif layanan == "4":
        rincianpemesanan()
    elif layanan == "5":
        closing()
    else:
        input("Wah, yang kamu ketik salah nih. Ketik 1/2/3/4/5 yaa\nKlik enter untuk lanjut => ")
        os.system("cls")
        layanantambahan()

def tambah_hotel_baru():
    os.system("cls")
    print("-" * 115)
    print("Tambah Hotel Baru".center(115))
    print("-" * 115)
    namaHotel = input("Nama            : ")
    alamatHotel = input("Alamat          : ")
    ratingHotel = input("Rating          : ")
    banyakkamarinput = input("Ada berapa banyak tipe kamar yang ingin kamu tambahkan? ")
    while banyakkamarinput.isdigit() == False:
        input("Wah, yang kamu ketik salah nih. Tulis pakai angka yaa\nKlik enter untuk lanjut => ")
        banyakkamarinput = input("Ada berapa banyak kamar yang ingin kamu tambahkan? ")
    global datakamar, j
    datakamar = []
    nomor = 0
    for j in range(0,int(banyakkamarinput)):
        nomor += 1
        print(f"\nKamar ke - {nomor}\n")
        global kamar, harga, jml_kmr
        kamar = input("Tipe Kamar            : ")
        harga = input("Harga Kamar           : ")
        while harga.isdigit() == False:
            input("Wah, yang kamu ketik salah nih. Tulis harga dengan angka yaa\nKlik enter untuk lanjut => ")
            harga = input("Harga per malam     : ")
        jml_kmr = input("Jumlah Kamar Tersedia : ")
        while jml_kmr.isdigit() == False:
            input("Wah, yang kamu ketik salah nih. Tulis persediaan kamar dengan angka yaa\nKlik enter untuk lanjut => ")
            jml_kmr = input("Jumlah Kamar Tersedia : ")
        if jml_kmr.isdigit() == True:
            datakamar.append((kamar,harga,jml_kmr))
    os.system("cls")
    print("-" * 115)
    print("Tambah Hotel Baru".center(115))
    print("-" * 115)
    print(f"Data hotel yang kamu tambahkan : \n\nNama           : {namaHotel}\nAlamat         : {alamatHotel}\nRating         : {ratingHotel}")
    nomor = 0
    for x in range(0,len(datakamar)):
        nomor += 1
        print(f"\nKamar ke - {nomor}")
        print(f"Tipe Kamar     : {datakamar[x][0]}\nHarga          : {datakamar[x][1]}\nKamar Tersedia : {datakamar[x][2]}")
    print("\n|1| Data sudah benar \n|2| Ganti data")
    confirm = input("Ketik 1/2 => ")
    if confirm == "1":
        with open("Hotel+kamar.csv", "a", newline="") as menambahHotel:
            os.system("cls")
            for y in datakamar:
                tambahanHotel = [namaHotel, y[0], alamatHotel, y[1], ratingHotel, y[2]]
                writer = csv.writer(menambahHotel, delimiter=";")
                writer.writerow(tambahanHotel)
        menambahHotel.close()
        print("Yay, kamu berhasil menambahkan data hotel 🥳".center(115))
        print("|1| Tambahkan data hotel lagi\n|2| Kembali ke menu edit data hotel\n|3| Kembali ke menu awal\n|4| Tutup aplikasi")
        pilih = (input("Ketik 1/2/3/4 => "))
        if pilih == "1":
            tambah_hotel_baru()
        elif pilih == "2":
            editdatahotel()
        elif pilih == "3":
            menu()
        elif pilih == "4":
            closing()
        else:
            input("Wah, yang kamu ketik salah nih. Ketik 1/2/3/4 yaa\nKlik enter untuk lanjut => ")
            os.system("cls")
            closing()
    elif confirm == "2":
        tambah_hotel_baru()
    else:
        input("Wah, yang kamu ketik salah nih. Ketik 1/2 yaa\nKlik enter untuk lanjut => ")
        os.system("cls")
        tambah_hotel_baru()
    
def tambah_kamar_hotel():
    os.system("cls")
    print("-" * 115)
    print("Tambah Data Kamar".center(115))
    print("-" * 115) 
    print("Pilih hotel yang ingin ditambahkan kamar :")
    listhotel = []
    listkamar = []
    nomor = 0
    with open("Hotel+kamar.csv", "r") as bacadatahotel:
        baca = csv.reader(bacadatahotel, delimiter=";")
        list_baca = list(baca)
    for row in list_baca:
        if row[0] not in listkamar:
            listkamar.append(row[0])
            listhotel.append((row[0], row[2], row[4]))
            nomor += 1
            print(f"{nomor}. {row[0]}")
        else:
            continue
    hotel = input("\nPilih hotel dengan ketik nomornya => ")
    while int(hotel) > nomor:
        input("Wah, yang kamu ketik salah nih. Pilih nomor yang tersedia yaa\nKlik enter untuk lanjut => ")  
        hotel = input("\nPilih hotel dengan ketik nomornya => ")
    listkamarhotel = []
    if int(hotel) <= int(len(listhotel)):
        datahotel = listhotel[int(hotel)-1]
        os.system("cls")
        print("-" * 115)
        print(f"Kamu Sedang Menambahkan Data Kamar di {datahotel[0]}".center(115))
        print("-" * 115) 
        banyakkamarditambah = input("Ketik berapa tipe kamar yang ingin ditambahkan => ")
        while banyakkamarditambah.isdigit() == False:
            input("Wah, yang kamu ketik salah nih. Tulis pakai angka yaa\nKlik enter untuk lanjut => ")
            banyakkamarditambah = input("Ada berapa banyak kamar yang ingin kamu tambahkan? ")
        if banyakkamarditambah.isdigit() == True:
            nomorurut = 0
            os.system("cls")
            for j in range (0,int(banyakkamarditambah)):
                nomorurut+=1
                print("-" * 115)
                print("Kamar yang Ingin Ditambahkan".center(115))
                print("-" * 115)
                print(f"Tipe kamar ke-{nomorurut}")
                tipekamar = input("Tipe kamar          : ")
                hargakamar = input("Harga per malam     : ")
                while hargakamar.isdigit() == False:
                    input("Wah, yang kamu ketik salah nih. Tulis harga dengan angka yaa\nKlik enter untuk lanjut => ")
                    hargakamar = input("Harga per malam     : ")
                persediaan = input("Kamar yang tersedia : ")
                while persediaan.isdigit() == False:
                    input("Wah, yang kamu ketik salah nih. Tulis persediaan kamar dengan angka yaa\nKlik enter untuk lanjut => ")
                    persediaan = input("Kamar yang tersedia : ")
                    os.system("cls")
                if persediaan.isdigit() == True:
                    os.system("cls")
                    listkamarhotel.append((datahotel[0], tipekamar, datahotel[1], hargakamar, datahotel[2], persediaan))
            os.system("cls")
            print(f"Apakah kamu yakin akan menambahkan tipe kamar ini?".center(115))
            nomorurt = 0
            for d in listkamarhotel:
                nomorurt+=1
                print(f"Tipe kamar ke-{nomorurut}\nTipe kamar          : {d[1]}\nHarga per malam     : {d[3]}\nKamar yang tersedia : {d[5]}\n")
            yakin = input("|1| Ya, saya yakin\n|2| Ubah data\n|3| Batalkan edit\nKetik 1/2/3 => ")
            if yakin == "1":
                for a in listkamarhotel:
                    with open("Hotel+kamar.csv","a", newline="") as datakamar:
                        writer = csv.writer(datakamar, delimiter=";")
                        writer.writerow(a)
                    datakamar.close()
                os.system("cls")
                print("Yay, kamu berhasil menambahkan data kamar 🥳".center(115))
                pilih = input("|1| Tambahkan data kamar lagi\n|2| Kembali ke menu edit data hotel\n|3| Kembali ke menu awal\n|4| Tutup aplikasi\nKetik 1/2/3/4 => ")
                if pilih == "1":
                    tambah_kamar_hotel()
                elif pilih == "2":
                    editdatahotel()
                elif pilih == "3":
                    menu()
                elif pilih == "4":
                    closing()
                else:
                    input("Wah, yang kamu ketik salah nih. Ketik nomor hotel yang tersedia yaa\nKlik enter untuk lanjut => ")
                os.system("cls")
                closing()
            elif yakin == "2":
                tambah_kamar_hotel()
            elif yakin == "3":
                closing()
            else:
                input("Wah, yang kamu ketik salah nih. Ketik nomor hotel yang tersedia yaa\nKlik enter untuk lanjut => ")
                os.system("cls")
                closing()
        else: 
            input("Wah, yang kamu ketik salah nih. Ketik nomor hotel yang tersedia yaa\nKlik enter untuk lanjut => ")
            os.system("cls")
            tambah_kamar_hotel()

def hapus_hotel():
    os.system("cls")
    print("-" * 115)
    print("Hapus Data Hotel".center(115))
    print("-" * 115) 
    nomorhotel = 0
    listhotel = []
    with open("Hotel+kamar.csv", "r") as bacadatahotel:
        baca = csv.reader(bacadatahotel, delimiter=";")
        list_baca = list(baca)
        elemenhanyasekali = set()
    for row in list_baca:
        if row[0] not in elemenhanyasekali:
            listhotel.append((row[0], row[2], row[3], row[4], row[5]))
            elemenhanyasekali.add(row[0])
    for x in listhotel:
        nomorhotel += 1
        print(f"{nomorhotel}. {x[0]}\n   Alamat Hotel    : {x[1]}\n   Rating          : {x[3]}⭐\n   Harga per malam : Rp {x[2]}\n")
    hapus = input("Pilih data hotel yang ingin kamu hapus dengan ketik nomornya => ")
    fiks_hapus = int(hapus) - 1
    if 0< int(hapus) <= int(len(listhotel)):
        os.system("cls")
        print("-" * 115)
        print("Hapus Data Hotel".center(115))
        print("-" * 115)
        print(f"Apakah kamu yakin menghapus data {listhotel[fiks_hapus][0]}?\n".center(115))
        milih = input("|1| Ya, saya yakin\n|2| Ganti data yang ingin dihapus\nKetik 1/2 => ") 
        if milih == "1":
            df = pd.read_csv("Hotel+kamar.csv", delimiter= ";", header=None)
            remove = df.isin([listhotel[fiks_hapus][0]]).any(axis=1)
            df = df[~remove]
            df.to_csv("Hotel+kamar.csv", index=False, sep= ";", header=None)
            os.system("cls")
            print("Yay, kamu berhasil menghapus data hotel 🥳".center(115))
            print("|1| Hapus data hotel lagi\n|2| Kembali ke menu edit data hotel\n|3| Kembali ke menu awal\n|4| Tutup aplikasi")
            pilih = (input("Ketik 1/2/3/4 => "))
            if pilih == "1":
                hapus_hotel()
            elif pilih == "2":
                editdatahotel()
            elif pilih == "3":
                menu()
            elif pilih == "4":
                closing()
            else:
                input("Wah, yang kamu ketik salah nih. Ketik 1/2/3/4 yaa\nKlik enter untuk lanjut => ")
                os.system("cls")
                closing()
        elif milih == "2":
            hapus_hotel()
        else: 
            input("Wah, yang kamu ketik salah nih. Ketik 1/2 yaa\nKlik enter untuk lanjut => ")
            os.system("cls")
            closing()
    else:
        input("Wah, yang kamu ketik salah nih. Ketik nomor hotel yang ada yaa\nKlik enter untuk lanjut => ")
        os.system("cls")
        hapus_hotel()
    
def edit_deskripsi_hotel():
    os.system("cls")
    print("-" * 115)
    print("Ganti Deskripsi Hotel".center(115))
    print("-" * 115)
    print("Data hotel mana yang ingin diganti?\n")
    nomorhotel = 0
    listhotel = []
    with open("Hotel+kamar.csv", "r") as bacadatahotel:
        baca = csv.reader(bacadatahotel, delimiter=";")
        list_baca = list(baca)
    for row in list_baca:
        if row[0] not in listhotel:
            listhotel.append(row[0])
            nomorhotel += 1
            print(f"{nomorhotel}. {row[0]}")
        else:
            continue
    editHotel = int(input("\nPilih dengan ketik nomornya => "))
    if editHotel <= int(len(listhotel)):
        global hotelyangdiedit
        hotelyangdiedit = listhotel[int(editHotel)-1]
        os.system("cls")
        print("-" * 115)
        print(f"Edit Data {hotelyangdiedit}".center(115))
        print("-" * 115)
        print("Data apa yang ingin kamu edit? \n|1| Nama Hotel\n|2| Alamat Hotel\n|3| Rating Hotel\n|4| Harga per Malam\n|5| Ganti Hotel yang Diedit\n|6| Batal Mengedit")
        pilihan = input("Ketik 1/2/3/4/5/6 => ")
        if pilihan == "1":
            gantinamahotel()
        elif pilihan == "2":
            gantiAlamatHotel()
        elif pilihan == "3":
            gantiRatingHotel()
        elif pilihan == "4":
            gantiHargaHotel()
        elif pilihan == "5":
            edit_deskripsi_hotel()
        elif pilihan == "6":
            closing()
        else:
            input("Wah, yang kamu ketik salah nih. Ketik 1/2/3/4/5/6 yaa\nKlik enter untuk lanjut => ")
            os.system("cls")
            closing()   
    else: 
        input("Wah, yang kamu ketik salah nih. Ketik nomor hotel yang ada yaa\nKlik enter untuk lanjut => ")
        os.system("cls")
        edit_deskripsi_hotel()   
    
def gantinamahotel():
    os.system("cls")
    print("-" * 115)
    print("Ganti Nama Hotel".center(115))
    print("-" * 115)
    print(f"Nama Hotel Lama : {hotelyangdiedit}")
    namaHotelBaru = input("Nama Hotel Baru : ")
    os.system("cls")
    print(f"Kamu akan mengganti nama {hotelyangdiedit}".center(115))
    print(f"Menjadi {namaHotelBaru}".center(115))
    print("Apakah kamu yakin? \n|1| Ya, saya yakin\n|2| Ganti nama lagi \n|3| Kembali ke menu edit deskripsi hotel\n|4| Batalkan mengedit")
    choice = input("Ketik 1/2/3/4 => ")
    if choice == "1":
        df = pd.read_csv("Hotel+kamar.csv", header= None, sep= ";")
        df.replace(hotelyangdiedit, namaHotelBaru, inplace= True)
        df.to_csv('Hotel+kamar.csv', index=False, header=False, sep=";")
        os.system("cls")
        print("Yay, kamu berhasil mengganti nama hotel 🥳".center(115))
        print("|1| Ganti nama hotel lagi\n|2| Kembali ke menu edit deskripsi hotel\n|3| Kembali ke menu awal\n|4| Tutup aplikasi")
        pilih = (input("Ketik 1/2/3/4 => "))
        if pilih == "1":
            gantinamahotel()
        elif pilih == "2":
            edit_deskripsi_hotel()
        elif pilih == "3":
            menu()
        elif pilih == "4":
            closing()
        else:
            input("Wah, yang kamu ketik salah nih. Ketik 1/2/3/4 yaa\nKlik enter untuk lanjut => ")
            os.system("cls")
            closing() 
    elif choice == "2":
        gantinamahotel()
    elif choice == "3":
        menu()
    elif choice == "4":
        closing()
    else:
        input("Wah, yang kamu ketik salah nih. Ketik 1/2/3/4 yaa\nKlik enter untuk lanjut => ")
        os.system("cls")
        gantinamahotel() 

def gantiAlamatHotel():
    os.system("cls")
    print("-" * 115)
    print("Ganti Alamat Hotel".center(115))
    print("-" * 115)
    with open("Hotel+kamar.csv", "r") as bacadatahotel:
        baca = csv.reader(bacadatahotel, delimiter=";")
        list_baca = list(baca)
    for x in list_baca:
        if x[0] == hotelyangdiedit:
            Alamatyangdiedit = x[2]
    df = pd.read_csv("Hotel+kamar.csv", delimiter=";", header=None)
    print(f"Alamat Hotel Lama : {Alamatyangdiedit}")
    AlamatHotelBaru = input("Alamat Hotel Baru : ")
    os.system("cls")
    print(f"Kamu akan mengganti alamat {Alamatyangdiedit}".center(115))
    print(f"Menjadi {AlamatHotelBaru}".center(115))
    print("Apakah kamu yakin? \n|1| Ya, saya yakin\n|2| Ganti alamat lagi  \n|3| Kembali ke menu edit deskripsi hotel\n|4| Batalkan mengedit")
    choice = input("Ketik 1/2/3/4 =>")
    if choice == "1":
        df = pd.read_csv("Hotel+kamar.csv", header=None, sep=";")
        df.replace(Alamatyangdiedit, AlamatHotelBaru, inplace= True)
        df.to_csv('Hotel+kamar.csv', index=False, header=False, sep=";") 
        os.system("cls")
        print("Yay, kamu berhasil mengganti alamat hotel 🥳".center(115))
        print("|1| Ganti alamat hotel lagi\n|2| Kembali ke menu edit deskripsi hotel\n|3| Kembali ke menu awal\n|4| Tutup aplikasi")
        pilih = (input("Ketik 1/2/3/4 => "))
        if pilih == "1":
            gantiAlamatHotel()
        elif pilih == "2":
            edit_deskripsi_hotel()
        elif pilih == "3":
            menu()
        elif pilih == "4":
            closing()
        else:
            input("Wah, yang kamu ketik salah nih. Ketik 1/2/3/4 yaa\nKlik enter untuk lanjut => ")
            os.system("cls")
            closing()
    elif choice == "2":
        gantiAlamatHotel()
    elif choice == "3":
        menu()
    elif choice == "4":
        closing()
    else:
        input("Wah, yang kamu ketik salah nih. Ketik 1/2/3/4 yaa\nKlik enter untuk lanjut => ")
        os.system("cls")
        gantiAlamatHotel()

def gantiRatingHotel():
    os.system("cls")
    print("-" * 115)
    print("Ganti Rating Hotel".center(115))
    print("-" * 115)
    with open("Hotel+kamar.csv", "r") as bacadatahotel:
        baca = csv.reader(bacadatahotel, delimiter=";")
        list_baca = list(baca)
    for x in list_baca:
        if x[0] == hotelyangdiedit:
            ratingyangdiedit = x[4]
    print(f"Rating Hotel Lama : {ratingyangdiedit}")
    RatingHotelBaru = input("Rating Hotel Baru : ")
    os.system("cls")
    print(f"Kamu akan mengganti rating {ratingyangdiedit}".center(115))
    print(f"Menjadi {RatingHotelBaru}".center(115))
    print("Apakah kamu yakin? \n|1| Ya, saya yakin\n|2| Ganti rating lagi  \n|3| Kembali ke menu edit deskripsi hotel\n|4| Batalkan mengedit")
    choice = input("Ketik 1/2/3/4 =>")
    if choice == "1":
        df = pd.read_csv("Hotel+kamar.csv", header=None, sep=";")
        df.loc[df[0] == hotelyangdiedit, 4] = RatingHotelBaru
        df.to_csv('Hotel+kamar.csv', index=False, header=False, sep=";")
        os.system("cls")
        print("Yay, kamu berhasil mengganti rating hotel 🥳".center(115))
        print("|1| Ganti rating hotel lagi\n|2| Kembali ke menu edit deskripsi hotel\n|3| Kembali ke menu awal\n|4| Tutup aplikasi")
        pilih = (input("Ketik 1/2/3/4 => "))
        if pilih == "1":
            gantiRatingHotel()
        elif pilih == "2":
            edit_deskripsi_hotel()
        elif pilih == "3":
            menu()
        elif pilih == "4":
            closing()
        else:
            input("Wah, yang kamu ketik salah nih. Ketik 1/2/3/4 yaa\nKlik enter untuk lanjut => ")
            os.system("cls")
            closing()
    elif choice == "2":
        gantiRatingHotel()
    elif choice == "3":
        menu()
    elif choice == "4":
        closing()
    else:
        input("Wah, yang kamu ketik salah nih. Ketik 1/2/3/4 yaa\nKlik enter untuk lanjut => ")
        os.system("cls")
        gantiRatingHotel()

def gantiHargaHotel(): 
    os.system("cls")
    print("-" * 115)
    print("Ganti Harga Hotel".center(115))
    print("-" * 115)
    print("Pilih kamar yang ingin diedit")
    nomor = 0 
    data_kamar =[]
    with open("Hotel+kamar.csv", "r") as bacadatahotel:
        baca = csv.reader(bacadatahotel, delimiter=";")
        list_baca = list(baca)
    for x in list_baca:
        if x[0] == hotelyangdiedit:
            nomor += 1
            kamaryangmaudiedit = x[1]
            hargayangmaudiedit = x[3]
            print(f"{nomor}. {kamaryangmaudiedit}\n   Harga : {hargayangmaudiedit}")
            data_kamar.append((kamaryangmaudiedit, hargayangmaudiedit))
    pilih = input("Pilih kamar yang ingin kamu ingin edit dengan ketik nomornya => ")
    pilih_fiks = int(pilih)-1
    data_terpilih = data_kamar[pilih_fiks]
    os.system("cls")
    print("-" * 115)
    print(f"Kamu akan mengganti harga kamar {data_terpilih[0]} ".center(115))
    print("-" * 115)
    print(f"Harga Hotel Lama : {data_terpilih[1]}")
    HargaHotelBaru = input("Harga Hotel Baru : ")
    while HargaHotelBaru.isdigit() == False:
        input("Wah, yang kamu ketik salah nih. Tulis harga dengan angka yaa\nKlik enter untuk lanjut => ")
        HargaHotelBaru = input("Harga per malam     : ")
    os.system("cls")
    print(f"Kamu akan mengganti harga {data_terpilih[1]}".center(115))
    print(f"Menjadi {HargaHotelBaru}".center(115))
    print("Apakah kamu yakin? \n|1| Ya, saya yakin\n|2| Ganti harga lagi  \n|3| Kembali ke menu edit deskripsi hotel\n|4| Batalkan mengedit")
    choice = input("Ketik 1/2/3/4 =>")
    if choice == "1":
        df = pd.read_csv("Hotel+kamar.csv", header= None, sep=";")
        df.loc[(df[0] == hotelyangdiedit) & (df[1] == data_terpilih[0]), 3] = HargaHotelBaru
        df.to_csv('Hotel+kamar.csv', index=False, header=False, sep=";")
        os.system("cls")
        print("Yay, kamu berhasil mengganti harga hotel 🥳".center(115))
        print("|1| Ganti harga hotel lagi\n|2| Kembali ke menu edit deskripsi hotel\n|3| Kembali ke menu awal\n|4| Tutup aplikasi")
        pilih = (input("Ketik 1/2/3/4 => "))
        if pilih == "1":
            gantiHargaHotel()
        elif pilih == "2":
            edit_deskripsi_hotel()
        elif pilih == "3":
            menu()
        elif pilih == "4":
            closing()
        else:
            input("Wah, yang kamu ketik salah nih. Ketik 1/2/3/4 yaa\nKlik enter untuk lanjut => ")
            os.system("cls")
            closing()
    elif choice == "2":
        gantiHargaHotel()
    elif choice == "3":
        menu()
    elif choice == "4":
        closing()
    else:
        input("Wah, yang kamu ketik salah nih. Ketik 1/2/3/4 yaa\nKlik enter untuk lanjut => ")
        os.system("cls")
        gantiHargaHotel()

def edit_kamar_tersedia():
    os.system("cls")
    print("-" * 115)
    print("Edit Jumlah Kamar yang Tersedia".center(115))
    print("-" * 115)
    print("Pilih hotel yang ingin diedit : ")
    nomorhotel = 0
    listhotel = []
    with open("Hotel+kamar.csv", "r") as bacadatahotel:
        baca = csv.reader(bacadatahotel, delimiter=";")
        list_baca = list(baca)
    for row in list_baca:
        if row[0] not in listhotel:
            listhotel.append(row[0])
            nomorhotel += 1
            print(f"{nomorhotel}. {row[0]}")
        else:
            continue
    editHotel = int(input("\nPilih dengan ketik nomornya => "))
    if 0 < editHotel <= int(len(listhotel)):
        global hotelyangdiedit
        hotelyangdiedit = listhotel[int(editHotel)-1]
        os.system("cls")
        print("-" * 115)
        print("Pilih Kamar yang Ingin Diedit".center(115))
        print("-" * 115)
        nomor = 0 
        data_kamar =[]
        with open("Hotel+kamar.csv", "r") as bacadatahotel:
            baca = csv.reader(bacadatahotel, delimiter=";")
            list_baca = list(baca)
        for x in list_baca: 
            if x[0] == hotelyangdiedit:
                nomor += 1
                kamaryangmaudiedit = x[1]
                persediaanyangmaudiedit = x[5]
                print(f"{nomor}. {kamaryangmaudiedit}\n   Kamar tersedia : {persediaanyangmaudiedit}")
                data_kamar.append((kamaryangmaudiedit, persediaanyangmaudiedit))
        pilih = input("\nPilih kamar yang ingin kamu inginkan dengan ketik nomornya => ")
        pilih_fiks = int(pilih)-1
        if int(pilih) <= len(data_kamar):
            data_terpilih = data_kamar[pilih_fiks]
            os.system("cls")
            print("-" * 115)
            print(f"Mengganti Persediaan Kamar {data_terpilih[0]} ".center(115))
            print("-" * 115)
            print(f"Jumlah kamar tersedia (lama) : {data_terpilih[1]}")
            persediaankamarbaru = input("Jumlah kamar tersedia (baru) : ")
            while persediaankamarbaru.isdigit() == False:
                input("Wah, yang kamu ketik salah nih. Tulis dengan angka yaa\nKlik enter untuk lanjut => ")
                persediaankamarbaru = input("Jumlah kamar tersedia (baru) : ")
            os.system("cls")
            print(f"Kamu akan mengganti {data_terpilih[1]} kamar".center(115))
            print(f"Menjadi {persediaankamarbaru} kamar".center(115))
            print("Apakah kamu yakin? \n|1| Ya, saya yakin\n|2| Ubah data yang diedit  \n|3| Batalkan mengedit")
            choice = input("Ketik 1/2/3 =>")
            if choice == "1":
                df = pd.read_csv("Hotel+kamar.csv", header= None, sep=";")
                df.loc[(df[0] == hotelyangdiedit) & (df[1] == data_terpilih[0]), 5] = persediaankamarbaru
                df.to_csv('Hotel+kamar.csv', index=False, header=False, sep=";")
                os.system("cls")
                print("Yay, kamu berhasil mengganti persediaan kamar hotel 🥳".center(115))
                print("|1| Edit persediaan kamar lagi\n|2| Kembali ke menu awal\n|3| Tutup aplikasi")
                pilih = (input("Ketik 1/2/3 => "))
                if pilih == "1":
                    edit_kamar_tersedia()
                elif pilih == "2":
                    menu()
                elif pilih == "3":
                    closing()
                else:
                    input("Wah, yang kamu ketik salah nih. Ketik 1/2/3 yaa\nKlik enter untuk lanjut => ")
                    os.system("cls")
                    closing()
            elif choice == "2":
                edit_deskripsi_hotel()
            elif choice == "3":
                closing()
            else:
                input("Wah, yang kamu ketik salah nih. Ketik 1/2/3 yaa\nKlik enter untuk lanjut => ")
                os.system("cls")
                edit_kamar_tersedia()
        else: 
           input("Wah, yang kamu ketik salah nih. Ketik nomor hotelnya yaa\nKlik enter untuk lanjut => ")
           os.system("cls")
           edit_kamar_tersedia() 
    else:
        input("Wah, yang kamu ketik salah nih. Ketik 1/2/3 yaa\nKlik enter untuk lanjut => ")
        os.system("cls")
        edit_kamar_tersedia()
        

def editdatahotel(): 
    os.system("cls")
    print("-" * 115)
    print("Edit Data Hotel".center(115))
    print("-" * 115)
    print("|1| Tambah Hotel Baru\n|2| Tambah Kamar Pada Hotel yang Sudah Ada\n|3| Hapus Hotel yang Ada\n|4| Edit Deskripsi Hotel\n|5| Edit Jumlah Kamar Tersedia\n|6| Kembali ke Menu Awal")
    global pilihEdit
    pilihEdit = input("Ketik 1/2/3/4/5/6 => ")
    if pilihEdit == "1":
        tambah_hotel_baru()
    elif pilihEdit == "2":
        tambah_kamar_hotel()
    elif pilihEdit == "3":
        hapus_hotel()
    elif pilihEdit == "4":
        edit_deskripsi_hotel()
    elif pilihEdit == "5":
        edit_kamar_tersedia()
    elif pilihEdit == "6":
        menu()
    else: 
        input("Wah yang kamu ketik salah nih. Ketik 1/2/3/4/5/6 yaa\nKlik enter untuk lanjut => ")
        os.system("cls")
        editdatahotel()

def lihathistory(): 
    os.system("cls")
    print("-" * 115)
    print("History Reservasi Pelanggan".center(115))
    print("-" * 115)
    with open("History Reservasi.csv", "r") as history:
        baca = csv.reader(history)
        nomorhistory = 0
        for row in baca:
            nomorhistory += 1
            print(f"{nomorhistory}. Nomor Reservasi  : {row[0]}\n   Nama Pelanggan   : {row[1]}\n   Nama Hotel       : {row[2]}\n   Tipe Kamar       : {row[3]}\n   Alamat Hotel     : {row[4]}")
            print(f"   Jumlah Kamar     : {row[5]}\n   Tanggal Masuk    : {row[6]}\n   Tanggal Keluar   : {row[7]}\n   Lama Menginap    : {row[8]} Hari\n   Layanan Tambahan : {row[9]}")
            print(f"   Total Pembayaran : Rp {row[10]}\n   Status Pembayaran: {row[11]}\n") 
    pilihan = input("|1| Kembali ke menu awal\n|2| Tutup aplikasi\nKetik 1/2 => ")
    if pilihan == "1":
        menu()
    elif pilihan == "2":
        closing()
    else:
        input("Wah yang kamu ketik salah nih. Ketik 1/2 yaa\nKlik enter untuk lanjut => ")
        os.system("cls")
        lihathistory()

def menu():
    os.system("cls")
    print("-" * 115)
    print("Pilih Menu".center(115))
    print("-" * 115)
    print("|1| Input Reservasi Pelanggan\n|2| Edit Data Hotel\n|3| Lihat History Reservasi Pelanggan\n|4| Tutup Aplikasi")
    pilihanMenu = input("Ketik 1/2/3/4 => ")
    if pilihanMenu == "1":
        reservasi()
    elif pilihanMenu == "2":
        editdatahotel()
    elif pilihanMenu == "3":
        lihathistory()
    elif pilihanMenu == "4":
        closing()
    else:
        print("Wah yang kamu ketik salah nih. Ketik 1/2/3/4 yaa\nKlik enter untuk lanjut =>  ")
        menu()

def intro():
    os.system("cls")
    print("-"*115)
    print("EYYO APP".center(115))
    print("Aplikasi pencatatan reservasi pelanggan dan edit persediaan kamar hotel".center(115))
    print("-" * 115)
    print("Hai! Selamat Datang di Eyyo App 👋".center(115))
    print("Btw, kamu sudah punya akun atau belum?".center(115))
    print("|1| Sudah punya dong\n|2| Belum punya nih")
    pilihan = (input("Ketik(1/2) => "))
    if pilihan == "1":
        login()
    elif pilihan == "2":
        os.system("cls")
        signup()
        login()
    else:
        input("Wah, yang kamu ketik salah nih. Ketik 1/2 yaa\nKlik enter untuk lanjut => ")
        os.system("cls")
        intro()

def reservasi():
    namapelanggan()
    filterhotelberdasarkanharga()

def panggilkode():
    intro()
    menu()

panggilkode()