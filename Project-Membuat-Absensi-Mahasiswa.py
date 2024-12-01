import pandas as pd
import datetime

# Nama file untuk menyimpan data
NAMA_FILE_MAHASISWA = "data-mahasiswa.csv"
NAMA_FILE_ABSENSI = "data-absensi.csv"

# Fungsi untuk menyimpan data ke file CSV
def simpan_data_mahasiswa(df, nama_file=NAMA_FILE_MAHASISWA):
    df.to_csv(nama_file, index=False)

def simpan_data_absensi(df, nama_file=NAMA_FILE_ABSENSI):
    df.to_csv(nama_file, index=False)

# Fungsi untuk memuat data dari file CSV
def muat_data_mahasiswa(nama_file=NAMA_FILE_MAHASISWA):
    try:
        df = pd.read_csv(nama_file)
        # Pastikan NIM disimpan sebagai string
        df['NIM'] = df['NIM'].astype(str)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["NIM", "Nama", "Jurusan"])

def muat_data_absensi(nama_file=NAMA_FILE_ABSENSI):
    try:
        df = pd.read_csv(nama_file)
        # Pastikan NIM disimpan sebagai string
        df['NIM'] = df['NIM'].astype(str)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["NIM", "Nama", "Jurusan", "Tanggal", "Status"])

# Fungsi untuk memvalidasi input NIM hanya berupa angka
def validasi_nim(nim):
    return nim.isdigit()

# Fungsi untuk menambah mahasiswa (cek apakah NIM sudah ada)
def tambah_mahasiswa(data_mahasiswa):
    nim = input("Masukkan NIM Mahasiswa: ").strip()
    
    # Validasi NIM
    while not validasi_nim(nim):
        print("NIM hanya boleh menggunakan angka. Silakan coba lagi.")
        nim = input("Masukkan NIM Mahasiswa: ").strip()
    
    nama = input("Masukkan Nama Mahasiswa: ").strip()
    jurusan = input("Masukkan Jurusan Mahasiswa: ").strip()
    
    # Cek apakah mahasiswa sudah terdaftar
    if nim not in data_mahasiswa['NIM'].values:
        mahasiswa_baru = pd.DataFrame([[nim, nama, jurusan]], columns=["NIM", "Nama", "Jurusan"])
        data_mahasiswa = pd.concat([data_mahasiswa, mahasiswa_baru], ignore_index=True)
        simpan_data_mahasiswa(data_mahasiswa)  # Simpan data setiap kali ada penambahan
        print("Mahasiswa berhasil ditambahkan.")
    else:
        print("Mahasiswa sudah terdaftar.")
    
    return data_mahasiswa

# Fungsi untuk mengisi absensi (cek apakah mahasiswa sudah terdaftar dan belum absensi hari ini)
def isi_absensi(data_mahasiswa, data_absensi):
    nim = input("Masukkan NIM Mahasiswa: ").strip()
    
    # Validasi NIM
    while not validasi_nim(nim):
        print("NIM hanya boleh menggunakan angka. Silakan coba lagi.")
        nim = input("Masukkan NIM Mahasiswa: ").strip()

    tanggal = datetime.date.today().strftime("%Y-%m-%d")
    
    if nim in data_mahasiswa['NIM'].values:
        # Dapatkan data mahasiswa
        mahasiswa = data_mahasiswa[data_mahasiswa['NIM'] == nim].iloc[0]
        nama = mahasiswa['Nama']
        jurusan = mahasiswa['Jurusan']
        
        # Cek apakah sudah absensi hari ini
        if any((data_absensi['NIM'] == nim) & (data_absensi['Tanggal'] == tanggal)):
            print(f"Mahasiswa dengan NIM {nim} sudah absensi hari ini.")
        else:
            status = input("Masukkan Status Kehadiran (Hadir/Tidak Hadir): ").strip().lower()
            # Tambahkan absensi baru dengan tanggal dan status
            absensi_baru = pd.DataFrame([[nim, nama, jurusan, tanggal, status]], columns=["NIM", "Nama", "Jurusan", "Tanggal", "Status"])
            data_absensi = pd.concat([data_absensi, absensi_baru], ignore_index=True)
            simpan_data_absensi(data_absensi)  # Simpan data setiap kali ada absensi baru
            print(f"Absensi untuk NIM {nim} pada {tanggal} telah tercatat.")
    else:
        print("Mahasiswa tidak terdaftar.")
    
    return data_absensi

# Fungsi untuk melihat absensi mahasiswa
def lihat_absensi(data_absensi):
    nim = input("Masukkan NIM Mahasiswa: ").strip()
    
    # Validasi NIM
    while not validasi_nim(nim):
        print("NIM hanya boleh menggunakan angka. Silakan coba lagi.")
        nim = input("Masukkan NIM Mahasiswa: ").strip()

    if nim in data_absensi['NIM'].values:
        data_mahasiswa = data_absensi[data_absensi['NIM'] == nim]
        print(f"\nAbsensi untuk NIM {nim}:")
        print(data_mahasiswa[['Tanggal', 'Status']])
    else:
        print("Mahasiswa tidak terdaftar.")

# Fungsi untuk melihat semua absensi
def lihat_semua_absensi(data_absensi):
    print("\nAbsensi Semua Mahasiswa:")
    print(data_absensi)

# Fungsi utama program
def utama():
    data_mahasiswa = muat_data_mahasiswa()  # Memuat data mahasiswa dari file CSV
    data_absensi = muat_data_absensi()  # Memuat data absensi dari file CSV
    print("Data berhasil dimuat.")
    
    while True:
        print("\nMenu Absensi Mahasiswa")
        print("1. Tambah Mahasiswa")
        print("2. Isi Absensi")
        print("3. Lihat Absensi Mahasiswa")
        print("4. Lihat Semua Absensi")
        print("5. Keluar")
        
        pilihan = input("Pilih menu (1-5): ")
        
        if pilihan == "1":
            data_mahasiswa = tambah_mahasiswa(data_mahasiswa)
        elif pilihan == "2":
            data_absensi = isi_absensi(data_mahasiswa, data_absensi)
        elif pilihan == "3":
            lihat_absensi(data_absensi)
        elif pilihan == "4":
            lihat_semua_absensi(data_absensi)
        elif pilihan == "5":
            print("Keluar dari program...")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

    print("Program selesai.")

if __name__ == "__main__":
    utama()
