from models.mahasiswa_model import MahasiswaModel

class MahasiswaController:
    def __init__(self):
        self.model = MahasiswaModel()

    def get_all(self):
        return self.model.get_all()

    def search(self, keyword):
        if keyword.strip():
            return self.model.search(keyword)
        return self.model.get_all()

    def get_by_nim(self, nim):
        return self.model.get_by_nim(nim)

    def save(self, nim, nama, prodi, jk, tempat, tgl, alamat, desa, kec, kab, prov):
        existing = self.model.get_by_nim(nim)
        data_base = (nama, prodi, jk, tempat, tgl or None, alamat, desa, kec, kab, prov)
        if existing:
            self.model.update((*data_base, nim))
            return "update"
        else:
            self.model.insert((nim, *data_base))
            return "insert"

    def delete(self, nim):
        self.model.delete(nim)

    def count(self):
        return self.model.count()
