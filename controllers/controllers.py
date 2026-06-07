from models.dosen_model import DosenModel
from models.matakuliah_model import MatakuliahModel
from models.krs_model import KrsModel
from models.nilai_model import NilaiModel

class DosenController:
    def __init__(self):
        self.model = DosenModel()

    def get_all(self):      return self.model.get_all()
    def search(self, kw):   return self.model.search(kw) if kw.strip() else self.model.get_all()
    def get_options(self):  return self.model.get_options()
    def count(self):        return self.model.count()

    def save(self, nuptk, nama, pend, jabatan, jk, alamat):
        existing = self.model.get_by_nuptk(nuptk)
        if existing:
            self.model.update((nama, pend, jabatan, jk, alamat, nuptk))
            return "update"
        else:
            self.model.insert((nuptk, nama, pend, jabatan, jk, alamat))
            return "insert"

    def delete(self, nuptk): self.model.delete(nuptk)


class MatakuliahController:
    def __init__(self):
        self.model = MatakuliahModel()

    def get_all(self):      return self.model.get_all()
    def search(self, kw):   return self.model.search(kw) if kw.strip() else self.model.get_all()
    def get_options(self):  return self.model.get_options()
    def count(self):        return self.model.count()

    def save(self, kode, nama, sks, semester):
        existing = self.model.get_by_kode(kode)
        if existing:
            self.model.update((nama, sks, semester, kode))
            return "update"
        else:
            self.model.insert((kode, nama, sks, semester))
            return "insert"

    def delete(self, kode): self.model.delete(kode)


class KrsController:
    def __init__(self):
        self.model = KrsModel()

    def get_all(self):          return self.model.get_all()
    def get_by_nim(self, nim):  return self.model.get_by_nim(nim)
    def search(self, kw):       return self.model.search(kw) if kw.strip() else self.model.get_all()
    def count(self):            return self.model.count()

    def save(self, id_krs, nim, kode_mk, kelas, ruang, hari, jam, nuptk):
        if id_krs:
            self.model.update((nim, kode_mk, kelas, ruang, hari, jam, nuptk, id_krs))
            return "update"
        else:
            self.model.insert((nim, kode_mk, kelas, ruang, hari, jam, nuptk))
            return "insert"

    def delete(self, id_krs): self.model.delete(id_krs)


class NilaiController:
    def __init__(self):
        self.model = NilaiModel()

    def get_by_nim(self, nim):          return self.model.get_by_nim(nim)
    def get_all_detail(self):           return self.model.get_all_with_detail()
    def konversi(self, angka):          return self.model.konversi(angka)
    def hitung_ip(self, data):          return self.model.hitung_ip(data)

    def save(self, id_nilai, id_krs, nilai_angka):
        if id_nilai:
            self.model.update(id_nilai, id_krs, nilai_angka)
            return "update"
        else:
            return self.model.insert(id_krs, nilai_angka)

    def delete(self, id_nilai): self.model.delete(id_nilai)
