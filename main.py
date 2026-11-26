"""Aplikasi CLI SIMPOS dengan autentikasi dan pembatasan role."""
from getpass import getpass

from services import auth, inventory, master_data, production, reports


def pause():
    input("\\nTekan Enter untuk kembali ke menu...")


def read_int(prompt, minimum=1):
    while True:
        try:
            value = int(input(prompt))
            if value < minimum:
                print(f"Masukkan angka minimal {minimum}.")
                continue
            return value
        except ValueError:
            print("Input harus berupa bilangan bulat.")


def read_float(prompt):
    while True:
        try:
            value = float(input(prompt).replace(",", "."))
            if value <= 0:
                print("Masukkan angka lebih dari nol.")
                continue
            return value
        except ValueError:
            print("Input harus berupa angka.")


def show_rows(rows):
    if not rows:
        print("Belum ada data.")
        return
    for row in rows:
        print(" | ".join(f"{key}: {value}" for key, value in row.items()))


def supplier_menu():
    print("\\n--- DATA PEMASOK ---")
    print("1. Lihat pemasok\\n2. Tambah pemasok\\n3. Ubah pemasok\\n4. Hapus pemasok")
    choice = input("Pilih: ").strip()
    if choice == "1":
        show_rows(master_data.list_suppliers())
    elif choice == "2":
        name = input("Nama pemasok: ").strip()
        kind = input("Jenis pemasok: ").strip()
        phone = input("Telepon (opsional): ").strip()
        address = input("Alamat (opsional): ").strip()
        print(f"Pemasok tersimpan dengan ID {master_data.add_supplier(name, kind, phone, address)}.")
    elif choice == "3":
        sid = read_int("ID pemasok: ")
        name = input("Nama baru: ").strip()
        kind = input("Jenis pemasok: ").strip()
        phone = input("Telepon: ").strip()
        address = input("Alamat: ").strip()
        print("Data diperbarui." if master_data.update_supplier(sid, name, kind, phone, address) else "Pemasok tidak ditemukan.")
    elif choice == "4":
        sid = read_int("ID pemasok: ")
        print("Data dihapus." if master_data.delete_supplier(sid) else "Pemasok tidak ditemukan.")


def material_menu():
    print("\\n--- DATA BAHAN BAKU ---")
    print("1. Lihat bahan\\n2. Tambah bahan\\n3. Ubah bahan\\n4. Hapus bahan")
    choice = input("Pilih: ").strip()
    if choice == "1":
        show_rows(master_data.list_materials())
    elif choice == "2":
        name = input("Nama bahan: ").strip()
        unit = input("Satuan (kg/liter): ").strip()
        notes = input("Keterangan (opsional): ").strip()
        print(f"Bahan tersimpan dengan ID {master_data.add_material(name, unit, notes)}.")
    elif choice == "3":
        mid = read_int("ID bahan: ")
        name = input("Nama baru: ").strip()
        unit = input("Satuan: ").strip()
        notes = input("Keterangan: ").strip()
        print("Data diperbarui." if master_data.update_material(mid, name, unit, notes) else "Bahan tidak ditemukan.")
    elif choice == "4":
        mid = read_int("ID bahan: ")
        print("Data dihapus." if master_data.delete_material(mid) else "Bahan tidak ditemukan.")


def choose_items(prompt):
    items = []
    print(prompt)
    while True:
        material_id = read_int("ID bahan (0 untuk selesai): ", minimum=0)
        if material_id == 0:
            break
        quantity = read_float("Jumlah: ")
        items.append((material_id, quantity))
        if input("Tambah bahan lagi? (y/t): ").strip().lower() != "y":
            break
    return items


def receipt_menu():
    print("\\n--- PENERIMAAN BAHAN ---")
    show_rows(master_data.list_suppliers())
    supplier_id = read_int("ID pemasok: ")
    show_rows(master_data.list_materials())
    items = choose_items("Masukkan bahan yang diterima.")
    notes = input("Catatan (opsional): ").strip()
    receipt_id = inventory.receive_materials(supplier_id, items, notes)
    print(f"Penerimaan ID {receipt_id} tersimpan dengan status Menunggu. Stok belum bertambah.")


def review_receipt_menu():
    print("\\n--- VERIFIKASI PENERIMAAN ---")
    show_rows(inventory.list_receipts())
    receipt_id = read_int("ID penerimaan yang diperiksa: ")
    print("1. Setujui\\n2. Tolak")
    choice = input("Pilih keputusan: ").strip()
    if choice not in ("1", "2"):
        print("Pilihan tidak valid.")
        return
    decision = "Disetujui" if choice == "1" else "Ditolak"
    notes = input("Catatan verifikasi (opsional): ").strip()
    inventory.review_receipt(receipt_id, decision, notes)
    if decision == "Disetujui":
        print("Penerimaan disetujui. Stok bahan baku sudah ditambahkan.")
    else:
        print("Penerimaan ditolak. Stok tidak berubah.")


def production_menu():
    print("\\n--- BUAT BATCH PRODUKSI ---")
    show_rows(master_data.list_materials())
    items = choose_items("Masukkan bahan yang digunakan untuk batch.")
    notes = input("Catatan batch (opsional): ").strip()
    batch_id = production.create_batch(items, notes)
    print(f"Batch berhasil dibuat. ID: {batch_id}")


def batch_status_menu():
    print("\\n--- PERBARUI STATUS BATCH ---")
    show_rows(production.list_batches())
    batch_id = read_int("ID batch: ")
    print("1. Persiapan\\n2. Proses Produksi\\n3. Selesai")
    statuses = {"1": "Persiapan", "2": "Proses Produksi", "3": "Selesai"}
    status = statuses.get(input("Pilih status: ").strip())
    if not status:
        print("Pilihan status tidak valid.")
        return
    print("Status diperbarui." if production.update_batch_status(batch_id, status) else "Batch tidak ditemukan.")


def product_menu():
    print("\\n--- CATAT HASIL PRODUKSI ---")
    show_rows(production.list_batches())
    batch_id = read_int("ID batch yang sudah selesai: ")
    weight = read_float("Berat kompos yang dihasilkan (kg): ")
    product = production.record_product(batch_id, weight)
    print(f"Produk tercatat dengan ID {product['id_produk']}; rendemen {product['rendemen']:.2f}%.")


def quality_menu():
    print("\\n--- PENGUJIAN KUALITAS ---")
    show_rows(production.list_products())
    product_id = read_int("ID produk: ")
    ph_text = input("pH (kosongkan jika tidak diuji): ").strip()
    moisture_text = input("Kadar air % (kosongkan jika tidak diuji): ").strip()
    ph = float(ph_text.replace(",", ".")) if ph_text else None
    moisture = float(moisture_text.replace(",", ".")) if moisture_text else None
    color = input("Warna: ").strip()
    texture = input("Tekstur: ").strip()
    aroma = input("Aroma: ").strip()
    notes = input("Catatan: ").strip()
    test_id = production.record_quality(product_id, ph, moisture, color, texture, aroma, notes)
    print(f"Pengujian tersimpan dengan ID {test_id}.")


def report_menu():
    print("\\n--- LAPORAN STOK ---")
    show_rows(reports.stock_report())
    print("\\n--- LAPORAN PRODUKSI ---")
    show_rows([reports.production_report()])


def user_menu(current_user):
    print("\\n--- MANAJEMEN PENGGUNA ---")
    show_rows(auth.list_users())
    print("1. Tambah akun Orang Lapangan\\n2. Aktifkan/nonaktifkan akun")
    choice = input("Pilih: ").strip()
    if choice == "1":
        name = input("Nama pengguna: ").strip()
        username = input("Username: ").strip()
        password = getpass("Password awal (minimal 8 karakter): ")
        user_id = auth.create_user(name, username, password, "Orang Lapangan")
        print(f"Akun Orang Lapangan berhasil dibuat. ID: {user_id}")
    elif choice == "2":
        user_id = read_int("ID pengguna: ")
        active = input("Aktifkan akun? (y/t): ").strip().lower() == "y"
        if auth.set_user_status(user_id, active, current_user["id_pengguna"]):
            print("Status akun diperbarui.")
        else:
            print("Pengguna tidak ditemukan.")


def login():
    print("========================================")
    print("       SIMPOS - LOGIN PENGGUNA")
    print("========================================")
    for attempt in range(3):
        username = input("Username: ").strip()
        password = getpass("Password: ")
        user = auth.authenticate(username, password)
        if user:
            return user
        print(f"Username/password salah atau akun nonaktif. Sisa percobaan: {2 - attempt}")
    return None


def admin_menu(user):
    while True:
        print("\\n========================================")
        print(" SIMPOS | MENU ADMIN/SUPERVISOR")
        print(f" Login: {user['nama_pengguna']}")
        print("========================================")
        print("1. Manajemen pemasok")
        print("2. Manajemen bahan baku")
        print("3. Verifikasi penerimaan bahan")
        print("4. Monitoring stok dan produksi")
        print("5. Manajemen pengguna")
        print("0. Logout")
        choice = input("Pilih menu: ").strip()
        try:
            if choice == "1": supplier_menu()
            elif choice == "2": material_menu()
            elif choice == "3": review_receipt_menu()
            elif choice == "4": report_menu()
            elif choice == "5": user_menu(user)
            elif choice == "0":
                print("Logout berhasil.")
                return
            else: print("Pilihan tidak tersedia.")
        except Exception as exc:
            print(f"\\nTerjadi kesalahan: {exc}")
        if choice != "0":
            pause()


def field_menu(user):
    while True:
        print("\\n========================================")
        print(" SIMPOS | MENU ORANG LAPANGAN")
        print(f" Login: {user['nama_pengguna']}")
        print("========================================")
        print("1. Lihat stok bahan baku")
        print("2. Catat penerimaan bahan")
        print("3. Buat batch produksi")
        print("4. Perbarui status batch")
        print("5. Catat hasil produksi")
        print("6. Input pengujian kualitas")
        print("7. Lihat aktivitas produksi")
        print("0. Logout")
        choice = input("Pilih menu: ").strip()
        try:
            if choice == "1": show_rows(master_data.list_materials())
            elif choice == "2": receipt_menu()
            elif choice == "3": production_menu()
            elif choice == "4": batch_status_menu()
            elif choice == "5": product_menu()
            elif choice == "6": quality_menu()
            elif choice == "7":
                print("--- BATCH PRODUKSI ---")
                show_rows(production.list_batches())
                print("--- HASIL PRODUK ---")
                show_rows(production.list_products())
            elif choice == "0":
                print("Logout berhasil.")
                return
            else: print("Pilihan tidak tersedia.")
        except Exception as exc:
            print(f"\\nTerjadi kesalahan: {exc}")
        if choice != "0":
            pause()


def main():
    while True:
        try:
            user = login()
        except Exception as exc:
            print(f"Gagal mengakses database: {exc}")
            return
        if user is None:
            print("Terlalu banyak percobaan login. Aplikasi ditutup.")
            return
        print(f"\\nSelamat datang, {user['nama_pengguna']} ({user['role']}).")
        if user["role"] == "Admin":
            admin_menu(user)
        elif user["role"] == "Orang Lapangan":
            field_menu(user)


if __name__ == "__main__":
    main()
