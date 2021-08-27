import sys
import sqlite3
import datetime
from PyQt5 import QtWidgets, uic


class DatabaseUtilities:
    def __init__(self):
        self.connection = sqlite3.connect("gural_porselen_plaka_sistemi.db")
        self.my_cursor = self.connection.cursor()

    def create_izinliler_table_in_database(self):
        self.my_cursor.execute("Create table if not exists izinliler (kullanici_adi TEXT, parola TEXT)")
        self.connection.commit()

    def create_BEKLENEN_ARACLAR_table_in_database(self):
        self.my_cursor.execute("""Create table if not exists 
        BEKLENEN_ARACLAR (ID INTEGER, arac_plakasi TEXT, 
        firma_adi TEXT, teslim_alinacak_urun TEXT, 
        tahmini_gelis_saati TEXT, teslimat_noktasi TEXT)""")

    def create_CIKIS_YAPAN_ARACLAR_table_in_database(self):
        self.my_cursor.execute("""Create table if not exists 
                CIKIS_YAPAN_ARACLAR (ID INTEGER, arac_plakasi TEXT, 
                firma_adi TEXT, teslim_alinacak_urun TEXT, 
                cikis_saati TEXT)""")
        self.connection.commit()

    def create_tablewidget_for_BEKLENEN_ARACLAR(self):
        self.table_beklenen_araclar = QtWidgets.QTableWidget()
        self.table_beklenen_araclar.setColumnCount(6)
        self.table_beklenen_araclar.setHorizontalHeaderLabels(
            ["ID", "araç plakası", "firma adı", "teslim alınacak ürün", "tahmini geliş saati", "teslimat noktası"])
        self.table_beklenen_araclar.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_beklenen_araclar.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        return self.table_beklenen_araclar

    def create_tablewidget_for_GIRIS_YAPAN_ARACLAR(self):
        self.table_giris_yapan_araclar = QtWidgets.QTableWidget()
        self.table_giris_yapan_araclar.setColumnCount(5)
        self.table_giris_yapan_araclar.setHorizontalHeaderLabels(
            ["ID", "araç plakası", "firma adı", "teslim alınacak ürün", "giriş saati"])
        self.table_giris_yapan_araclar.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_giris_yapan_araclar.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        return self.table_giris_yapan_araclar

    def display_BEKLENEN_ARACLAR(self):
        sql_query = "SELECT * from BEKLENEN_ARACLAR"
        result = self.my_cursor.execute(sql_query)
        self.table_beklenen_araclar.setRowCount(0)
        for row_index, row_data in enumerate(result):
            self.table_beklenen_araclar.insertRow(row_index)
            for coloumn_number, coloumn_data in enumerate(row_data):
                self.table_beklenen_araclar.setItem(row_index, coloumn_number, QtWidgets.QTableWidgetItem(str(coloumn_data)))

    def display_GIRIS_YAPAN_ARACLAR(self):
        sql_query = "SELECT * from GIRIS_YAPAN_ARACLAR"
        result = self.my_cursor.execute(sql_query)
        self.table_giris_yapan_araclar.setRowCount(0)
        for row_index, row_data in enumerate(result):
            self.table_giris_yapan_araclar.insertRow(row_index)
            for coloumn_number, coloumn_data in enumerate(row_data):
                self.table_giris_yapan_araclar.setItem(row_index, coloumn_number, QtWidgets.QTableWidgetItem(str(coloumn_data)))

    def update_database(self):
        self.clear_database()
        self.display_BEKLENEN_ARACLAR()

    def clear_database(self):
        while self.table_beklenen_araclar.rowCount() > 0:
            self.table_beklenen_araclar.removeRow(0)

    def update_database_for_GIRIS_YAPAN_ARACLAR(self):
        self.clear_database()
        self.display_GIRIS_YAPAN_ARACLAR()

    def clear_database_for_GIRIS_YAPAN_ARACLAR(self):
        while self.table_giris_yapan_araclar.rowCount() > 0:
            self.table_giris_yapan_araclar.removeRow(0)

    def create_GIRIS_YAPAN_ARACLAR_table_in_database(self):
        self.my_cursor.execute("""Create table if not exists 
                GIRIS_YAPAN_ARACLAR (ID INTEGER, arac_plakasi TEXT, 
                firma_adi TEXT, teslim_alinacak_urun TEXT, 
                giris_saati TEXT)""")
        self.connection.commit()



class Login(QtWidgets.QWidget, DatabaseUtilities):
    def __init__(self):
        super(Login, self).__init__()
        self.setWindowTitle("ANPR SYSTEM")
        self.setGeometry(0, 0, 512, 512)
        self.login_init_ui()
        self.create_izinliler_table_in_database()

    def login_init_ui(self):
        self.kullanici_adi_sor = QtWidgets.QLabel("Kullanıcı adı")
        self.parola_sor = QtWidgets.QLabel("Parola")
        self.kullaniciAdi = QtWidgets.QLineEdit()
        self.parola = QtWidgets.QLineEdit()
        self.parola.setEchoMode(QtWidgets.QLineEdit.Password)
        self.girisYap = QtWidgets.QPushButton("Giriş yap")
        self.izin = QtWidgets.QPushButton("İzin iste")
        self.yazi_alani = QtWidgets.QLabel("")  # yani bu benim duruma göre cereceğim mesaj

        v_box = QtWidgets.QVBoxLayout()
        v_box.addStretch()

        v_box.addWidget(self.kullanici_adi_sor)
        v_box.addWidget(self.kullaniciAdi)
        v_box.addWidget(self.parola_sor)
        v_box.addWidget(self.parola)
        v_box.addWidget(self.girisYap)
        v_box.addWidget(self.yazi_alani)
        v_box.addStretch()
        v_box.addWidget(self.izin)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()
        self.setLayout(h_box)

        self.girisYap.clicked.connect(self.giris_func)
        self.izin.clicked.connect(self.izin_iste)

    def giris_func(self):
        kullanici_adi = self.kullaniciAdi.text()
        parolasi = self.parola.text()

        self.my_cursor.execute("Select * From izinliler where kullanici_adi = ? and parola = ?",(kullanici_adi, parolasi))
        data = self.my_cursor.fetchall()
        if len(data) == 0:
            self.yazi_alani.setText("Bilgilerinizi yanlış girdiniz veya giriş izniniz yok! ")
        else:
            menu = MainWindow()
            widget.addWidget(menu)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def izin_iste(self):
        if len(self.kullaniciAdi.text()) != 0 and len(self.parola.text()) != 0:
            self.yazi_alani.setText("İzin talebiniz yetkiliye iletildi.")
        else:
            self.yazi_alani.setText("Lütfen izin istemek için bilgilerinizi eksiksiz giriniz!")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.main_init_ui()
        self.choose_detection_type = Detection()
        self.setCentralWidget(self.choose_detection_type) # ortata bir tane widget eklemek istiyorum bu da benim self.pencerem

    def main_init_ui(self):
        main_menu = self.menuBar()
        self.db_menu = main_menu.addMenu("Veritabanı işlemleri")
        actionExpected_vehicles = QtWidgets.QAction("Beklenen araçlar", self)
        self.db_menu.addAction(actionExpected_vehicles)
        actionRegistered_vehicles = QtWidgets.QAction("Kayıtlı araçlar", self)
        self.db_menu.addAction(actionRegistered_vehicles)
        actionEntry_Exit = QtWidgets.QAction("Yapılan giriş/çıkışlar", self)
        self.db_menu.addAction(actionEntry_Exit)
        actionBlacklist = QtWidgets.QAction("Kara liste", self)
        self.db_menu.addAction(actionBlacklist)
        actionAllowed = QtWidgets.QAction("İzinlileri yönet", self)
        self.db_menu.addAction(actionAllowed)

        main_menu.triggered.connect(self.response)

    def response(self, action):
        if action.text() == "Beklenen araçlar":
            exp_vhcles_menu = ExpectedVehiclesMENU()
            widget.addWidget(exp_vhcles_menu)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        elif action.text() == "Kayıtlı araçlar":
            rgstred_vhcles = RegisteredVehicles()
            widget.addWidget(rgstred_vhcles)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        elif action.text() == "Yapılan giriş/çıkışlar":
            entry_exit = EntryExitRecords()
            widget.addWidget(entry_exit)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        elif action.text() == "Kara liste":
            blacklist = Blacklist()
            widget.addWidget(blacklist)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        elif action.text() == "İzinlileri yönet":
            allowed = AllowedOnes()
            widget.addWidget(allowed)
            widget.setCurrentIndex(widget.currentIndex() + 1)

class Detection(QtWidgets.QDialog):
    def __init__(self):
        super(Detection, self).__init__()
        self.detect_init_ui()

    def detect_init_ui(self):
        self.real_time = QtWidgets.QPushButton("Gerçek zamanlı plaka tanıma",self)
        self.image = QtWidgets.QPushButton("Fotoğraftan plaka tanıma",self)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addStretch()

        v_box.addWidget(self.real_time)
        v_box.addWidget(self.image)
        v_box.addStretch()

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()
        self.setLayout(h_box)

class ExpectedVehicles(QtWidgets.QWidget, DatabaseUtilities):
    def __init__(self):
        super(ExpectedVehicles, self).__init__()
        self.create_table()
        self.display_BEKLENEN_ARACLAR()

    def create_table(self):
        v_box = QtWidgets.QVBoxLayout()
        table = self.create_tablewidget_for_BEKLENEN_ARACLAR()
        v_box.addWidget(table)
        v_box.addStretch()
        self.setLayout(v_box)

class ExpectedVehiclesMENU(QtWidgets.QMainWindow):
    def __init__(self):
        super(ExpectedVehiclesMENU, self).__init__()
        self.exp_vhcles_menu_init_ui()
        self.exp_vhcles_table = ExpectedVehicles()
        self.setCentralWidget(self.exp_vhcles_table)

    def exp_vhcles_menu_init_ui(self):
        main_menu = self.menuBar()
        self.exp_vhcles_menu = main_menu.addMenu("Düzenle")
        actionEkle = QtWidgets.QAction("Ekle", self)
        self.exp_vhcles_menu.addAction(actionEkle)

        actionCikart = QtWidgets.QAction("Çıkart", self)
        self.exp_vhcles_menu.addAction(actionCikart)

        main_menu.triggered.connect(self.response)

    def response(self, action):
        if action.text() == "Ekle":
            insert = Insertion()
            widget.addWidget(insert)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        elif action.text() == "Çıkart":
            delete = Deletion()
            widget.addWidget(delete)
            widget.setCurrentIndex(widget.currentIndex() + 1)

class Insertion(QtWidgets.QWidget, DatabaseUtilities):
    def __init__(self):
        super(Insertion, self).__init__()
        self.insertion_init_ui()

    def insertion_init_ui(self):
        self.v_box = QtWidgets.QVBoxLayout()
        self.plaka_sor = QtWidgets.QLabel("araç plakası: ")
        self.plaka_al = QtWidgets.QLineEdit()
        h_box_1 = QtWidgets.QHBoxLayout()
        h_box_1.addWidget(self.plaka_sor)
        h_box_1.addWidget(self.plaka_al)
        self.firma_sor = QtWidgets.QLabel("firma adı: ")
        self.firma_al = QtWidgets.QLineEdit()
        h_box_2 = QtWidgets.QHBoxLayout()
        h_box_2.addWidget(self.firma_sor)
        h_box_2.addWidget(self.firma_al)
        self.urun_sor = QtWidgets.QLabel("teslim alınacak ürün: ")
        self.urun_al = QtWidgets.QLineEdit()
        h_box_3 = QtWidgets.QHBoxLayout()
        h_box_3.addWidget(self.urun_sor)
        h_box_3.addWidget(self.urun_al)
        self.saat_sor = QtWidgets.QLabel("tahmini geliş saati: ")
        self.saat_al = QtWidgets.QLineEdit()
        h_box_4 = QtWidgets.QHBoxLayout()
        h_box_4.addWidget(self.saat_sor)
        h_box_4.addWidget(self.saat_al)
        self.adres_sor = QtWidgets.QLabel("teslimat noktası: ")
        self.adres_al = QtWidgets.QLineEdit()
        h_box_5 = QtWidgets.QHBoxLayout()
        h_box_5.addWidget(self.adres_sor)
        h_box_5.addWidget(self.adres_al)
        self.ekle_button = QtWidgets.QPushButton("Veritabanına ekle")
        self.guncelle_button = QtWidgets.QPushButton("Veritabanını güncelle")
        self.message = QtWidgets.QLabel("")
        self.v_box.addLayout(h_box_1)
        self.v_box.addLayout(h_box_2)
        self.v_box.addLayout(h_box_3)
        self.v_box.addLayout(h_box_4)
        self.v_box.addLayout(h_box_5)
        self.v_box.addWidget(self.ekle_button)
        self.v_box.addWidget(self.guncelle_button)
        self.v_box.addWidget(self.message)
        self.setLayout(self.v_box)
        self.ekle_button.clicked.connect(self.add_to_database)
        self.guncelle_button.clicked.connect(self.update_database_after_insertion)

    def add_to_database(self):
        self.plaka = self.plaka_al.text()
        self.firma = self.firma_al.text()
        self.urun = self.urun_al.text()
        self.saat = self.saat_al.text()
        self.adres = self.adres_al.text()
        all_data_for_insertion = (self.plaka, self.firma, self.urun, self.saat, self.adres)
        sql_command = """Insert into BEKLENEN_ARACLAR 
        (arac_plakasi, firma_adi, teslim_alinacak_urun, tahmini_gelis_saati, 
        teslimat_noktasi) VALUES (?, ?, ?, ?, ?)"""
        self.my_cursor.execute(sql_command, all_data_for_insertion)
        self.message.setText("Araç beklenen araçlar veritabanına eklendi! ")
        self.connection.commit()

    def update_database_after_insertion(self):
        table = self.create_tablewidget_for_BEKLENEN_ARACLAR()
        self.v_box.addWidget(table)
        self.setLayout(self.v_box)
        self.update_database()

class Deletion(QtWidgets.QWidget, DatabaseUtilities):
    def __init__(self):
        super(Deletion, self).__init__()
        self.combine_them_to_create_overall_screen()

    def deletion_init_ui(self):
        self.h_box = QtWidgets.QHBoxLayout()
        self.giris_yapti = QtWidgets.QPushButton("giriş yaptı")
        self.cikis_yapti = QtWidgets.QPushButton("çıkış yaptı")
        self.gelmeyecek = QtWidgets.QPushButton("gelmeyecek")
        self.h_box.addWidget(self.giris_yapti)
        self.h_box.addWidget(self.cikis_yapti)
        self.h_box.addWidget(self.gelmeyecek)
        """self.cikis_yapti.clicked.connect(self.cikis_yap)
        self.gelmeyecek.clicked.connect(self.gelmeyecek)"""

    def selection_changed(self):
        self.index_of_the_selected_row = self.table_beklenen_araclar.currentRow()

    def combine_them_to_create_overall_screen(self):
        self.deletion_init_ui()
        self.create_table_for_deletion()
        self.v_box.addLayout(self.h_box)
        self.setLayout(self.v_box)
        self.display_BEKLENEN_ARACLAR()
        self.table_beklenen_araclar.itemSelectionChanged.connect(self.selection_changed)
        self.giris_yapti.clicked.connect(self.giris_yap)

    def create_table_for_deletion(self):
        self.v_box = QtWidgets.QVBoxLayout()
        table = self.create_tablewidget_for_BEKLENEN_ARACLAR()
        self.v_box.addWidget(table)
        self.v_box.addStretch()
        self.setLayout(self.v_box)

    def giris_yap(self):
        self.insert_into_giris_yap()
        self.delete_from_BEKLENEN_ARACLAR()
        self.create_GIRIS_YAPAN_ARACLAR_table_in_database()
        self.table_1 = self.create_tablewidget_for_GIRIS_YAPAN_ARACLAR()
        self.v_box.addStretch()
        self.v_box.addWidget(self.table_1)
        self.display_GIRIS_YAPAN_ARACLAR()
        self.setLayout(self.v_box)
        self.table_beklenen_araclar.itemSelectionChanged.connect(self.selection_changed)
        self.giris_yapti.clicked.connect(self.giris_yap_2)


    def giris_yap_2(self):
        if self.table_1.isVisible():
            print("yes")
            self.update_database_for_GIRIS_YAPAN_ARACLAR()
        else:
            print("elsee girdi")
            self.giris_yap()


    def insert_into_giris_yap(self):
        licence = self.table_beklenen_araclar.item(self.index_of_the_selected_row, 1).text()
        company = self.table_beklenen_araclar.item(self.index_of_the_selected_row, 2).text()
        product = self.table_beklenen_araclar.item(self.index_of_the_selected_row, 3).text()
        now = datetime.datetime.now()
        fourth_elm = now.strftime("%d-%m-%y %H:%M:%S")
        sql_command = """Insert into GIRIS_YAPAN_ARACLAR 
                (arac_plakasi, firma_adi, teslim_alinacak_urun, giris_saati) VALUES (?, ?, ?, ?)"""
        self.my_cursor.execute(sql_command, (licence, company, product, fourth_elm))
        self.connection.commit()

    def delete_from_BEKLENEN_ARACLAR(self):
        id = self.table_beklenen_araclar.item(self.index_of_the_selected_row, 0).text()
        sql_query = "DELETE FROM BEKLENEN_ARACLAR WHERE ID=" + id
        self.connection.execute(sql_query)
        self.connection.commit()
        self.update_database()


class RegisteredVehicles(QtWidgets.QWidget):
    def __init__(self):
        super(RegisteredVehicles, self).__init__()
        self.rgstred_vhcles_init_ui()
    def rgstred_vhcles_init_ui(self):
        pass

class EntryExitRecords(QtWidgets.QWidget):
    def __init__(self):
        super(EntryExitRecords, self).__init__()
        self.entry_exit_init_ui()
    def entry_exit_init_ui(self):
        pass


class Blacklist(QtWidgets.QWidget):
    def __init__(self):
        super(Blacklist, self).__init__()
        self.blacklist_vhcles_init_ui()
    def blacklist_vhcles_init_ui(self):
        pass

class AllowedOnes(QtWidgets.QWidget):
    def __init__(self):
        super(AllowedOnes, self).__init__()
        self.allowed_init_ui()
    def allowed_init_ui(self):
        pass

# self.baglanti.close()'u unutma !!!!

# main
app2 = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QStackedWidget() # a series of widgets. you are going through this list by loading other ui's.
login = Login()
widget.addWidget(login)
widget.setFixedWidth(800)
widget.setFixedHeight(600)
widget.show()

try:
    sys.exit(app2.exec())  # bu bir loop
except:
    print("Exiting")