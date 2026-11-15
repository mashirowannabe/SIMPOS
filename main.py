"""Aplikasi CLI SIMPOS."""

from services import inventory, master_data, production, reports


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
    print(f"Penerimaan berhasil disimpan. ID: {receipt_id}")


def production_menu():
    print("\\n--- PRODUKSI ---")
    show_rows(master_data.list_materials())
    items = choose_items("Masukkan bahan yang digunakan untuk batch.")
    notes = input("Catatan batch (opsional): ").strip()
    batch_id = production.create_batch(items, notes)
    print(f"Batch berhasil dibuat. ID: {batch_id}")


def batch_status_menu():
    show_rows(production.list_batches())
    batch_id = read_int("ID batch: ")
    print("1. Persiapan\\n2. Fermentasi\\n3. Pematangan\\n4. Selesai")
    statuses = {"1": "Persiapan", "2": "Fermentasi", "3": "Pematangan", "4": "Selesai"}
    status = statuses.get(input("Pilih status: ").strip())
    if not status:
        print("Pilihan status tidak valid.")
        return
    print("Status diperbarui." if production.update_batch_status(batch_id, status) else "Batch tidak ditemukan.")


def product_menu():
    show_rows(production.list_batches())
    batch_id = read_int("ID batch yang sudah selesai: ")
    weight = read_float("Berat kompos yang dihasilkan (kg): ")
    product = production.record_product(batch_id, weight)
    print(f"Produk tercatat dengan ID {product['id_produk']}; rendemen {product['rendemen']:.2f}%.")


def quality_menu():
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


def main():
    while True:
        print("\\n========================================")
        print(" SIMPOS - MANAJEMEN PRODUKSI PUPUK KOMPOS")
        print("========================================")
        print("1. Manajemen pemasok")
        print("2. Manajemen bahan baku")
        print("3. Penerimaan bahan baku")
        print("4. Buat batch produksi")
        print("5. Ubah status batch")
        print("6. Catat hasil produksi")
        print("7. Pengujian kualitas")
        print("8. Laporan dan statistik")
        print("0. Keluar")

        choice = input("Pilih menu: ").strip()
        try:
            if choice == "1": supplier_menu()
            elif choice == "2": material_menu()
            elif choice == "3": receipt_menu()
            elif choice == "4": production_menu()
            elif choice == "5": batch_status_menu()
            elif choice == "6": product_menu()
            elif choice == "7": quality_menu()
            elif choice == "8": report_menu()
            elif choice == "0":
                print("Terima kasih telah menggunakan SIMPOS.")
                break
            else: print("Pilihan tidak tersedia.")
        except Exception as exc:
            print(f"\\nTerjadi kesalahan: {exc}")
        if choice != "0":
            pause()


if __name__ == "__main__":
    main()
