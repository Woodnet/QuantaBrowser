#
#       Author: Pulsar
#       Date: 13.01.12020/2020
#       Python-Version: 3.8.2
#       The QuantaWebBrowser
#       GitHub: https://www.github.com/Woodnet
#       Twitter: https://www.twitter.com/7Pulsar
#
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView,QWebEnginePage as QWebPage
from PyQt5.QtWebEngineWidgets import QWebEngineSettings as QWebSettings
import sys,os
from cryptography.fernet import Fernet

class Second(QMainWindow):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)
        self.setGeometry(100, 50, 700, 400)
        self.setWindowTitle("BETA-QuantaBrowser")
        self.setWindowIcon(QIcon('icons/warning_2.png'))
        l1 = QLabel(self)
        self.setStyleSheet("background-color: red;")
        self.setStyleSheet("color: whitesmoke;")
        l1.setText('BETA-VERSION (INACTIVE)')
        l1.setFont(QFont('Arial', 33))
        l1.setStyleSheet("border: 41px solid red;")
        l1.adjustSize()
        l1.move(10, 100)

class MainWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)

        self.resize(1200,700)

        self.browser = QWebView()
        self.setWindowIcon(QIcon('icons/shield.png'))

        vbox = QToolBar("Übersicht_2")
        vbox.setIconSize(QSize(34,34))
        self.addToolBar(Qt.BottomToolBarArea,vbox)

        navtb = QToolBar("Übersicht")
        navtb.setIconSize(QSize(32,32))
        self.addToolBar(navtb)

        back_btn = QAction( QIcon(os.path.join('icons','back_ICON.png')), "Zurück", self)
        back_btn.setStatusTip("Zurück zur letzten Seite")
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        next_btn = QAction( QIcon(os.path.join('icons','forward_ICON.png')), "Nächste Seite", self)
        next_btn.setStatusTip("Zur nächsten Seite")
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        reload_btn = QAction( QIcon(os.path.join('icons','reload_ICON.png')), "Neu laden", self)
        reload_btn.setStatusTip("Seite neu laden")
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        home_btn = QAction( QIcon(os.path.join('icons','home_ICON.png')), "Home", self)
        home_btn.setStatusTip("Nach Hause")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        self.httpsicon = QLabel() # Yes, really!
        self.httpsicon.setPixmap( QPixmap( os.path.join('icons','lock_nssl.png') ) )
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        #self.urlbar.setText('URL://')
        font = self.urlbar.font()
        font.setPointSize(15)
        self.urlbar.setFont(font)
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction(QIcon(os.path.join('icons','stop.png')), "Stop", self)
        stop_btn.setStatusTip("Laden stoppen")
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        ADDON_1 = QAction(QIcon(os.path.join('icons','locked_3.png')), "Quanta-Verschlüsselung", self)
        ADDON_1.setStatusTip("Laden stoppen")
        ADDON_1.triggered.connect(self.encryption_addon_1)
        navtb.addAction(ADDON_1)
        self.dialog = Second(self)

        font = ADDON_1.font()
        font.setPointSize(43)
        ADDON_1.setFont(font)

        self.browser.setUrl(QUrl("https://www.google.de"))
        self.setCentralWidget(self.browser)
        title = self.browser.page().title()
        self.setWindowTitle("%s - QuantaBrowser"%(title))
        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)

    def redirect_to_unsicher_nachricht(self):
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "HTML/unsicher_nachricht.html"))
        local_url = QUrl.fromLocalFile(file_path)
        self.browser.load(local_url)

    def encryption_addon_1(self):
        self.dialog.show()

    def update_urlbar(self, q):
        HTTP_pixmap = QPixmap('icons/unsecured-shield.svg')
        HTTPS_pixmap = QPixmap('icons/shield_2.png')
        __HTTPS_PIXMAP = HTTPS_pixmap.scaled(30, 30)
        __HTTP_PIXMAP = HTTP_pixmap.scaled(25, 25)

        if (q.scheme() == 'https'):
            # Secure padlock icon
            self.httpsicon.setPixmap(__HTTPS_PIXMAP)

        else:
            # Insecure padlock icon
            self.httpsicon.setPixmap(__HTTP_PIXMAP)

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("%s - QuantaBrowser" % title)

    def navigate_to_url(self):
        unsichere_URLS = []
        q = QUrl(self.urlbar.text())
        ttt = self.urlbar.text()
        print(ttt)
        #print(unsichere_URLS)
        for URL in unsichere_URLS:
            if (URL in ttt):
                unsicher = True
                break
            else:
                unsicher = False
        if (q.scheme() == ""):
            q.setScheme("http")
        if (unsicher == False):
            self.browser.setUrl(q)
        else:
            self.redirect_to_unsicher_nachricht()

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.de"))



app = QApplication(sys.argv)

app.setApplicationName("QuantaBrowser")
app.setOrganizationName("Quanta")
app.setOrganizationDomain("https://www.github.com/Woodnet")
#print(dir(app))

window = MainWindow()
window.show()

app.exec_()
