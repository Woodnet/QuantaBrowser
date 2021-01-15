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
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
from urllib import request
import sys
from pypac import PACSession, get_pac
import shutil

try:
    os.system("cls")
except:
    os.system("clear")

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.resize(1300,750)

        self.setWindowIcon(QIcon('icons/shield.png'))

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)

        #self.tabs.setStyleSheet("QWidget {background-color: black;}")
        self.tabs.setStyleSheet("QWidget {font-family:Consolas;font-size: 20px;color: cornflowerblue;border-bottom: 3px solid gray;}")

        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)
        self.status = QStatusBar()
        self.status.setStyleSheet("QWidget {font-size:17px;color:cornflowerblue;font-family:Courier;border-left:3px solid cornflowerblue;background-color: whitesmoke;}")

        self.setStatusBar(self.status)
        navtb = QToolBar("Status Bar")

        self.addToolBar(navtb)

        back_btn = QAction( QIcon(os.path.join('icons','back_ICON.png')), "Zurück", self)
        back_btn.setStatusTip("Zurück zur nächsten Seite")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        back_btn.setShortcut(QKeySequence("Ctrl+B"))
        navtb.addAction(back_btn)

        next_btn = QAction( QIcon(os.path.join('icons','forward_ICON.png')), "Nächste Seite", self)
        next_btn.setStatusTip("Nächste Seite")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction( QIcon(os.path.join('icons','reload_ICON.png')), "Neu laden", self)
        reload_btn.setStatusTip("Seite neu laden")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)
        home_btn = QAction( QIcon(os.path.join('icons','home_ICON.png')), "Home", self)
        #home_btn.setShortcut(QKeySequence("Ctrl+Shift+A"))
        home_btn.setShortcut(QKeySequence("Ctrl+H"))
        home_btn.setStatusTip("Zu Home")
        home_btn.triggered.connect(self.navigate_home)

        navtb.addAction(home_btn)
        navtb.addSeparator()
        navtb.setStyleSheet("background-color: white;")
        navtb.setIconSize(QSize(35,35))
        self.urlbar = QLineEdit()
        self.urlbar.setAlignment(Qt.AlignLeft)
        font = self.urlbar.font()
        font.setPointSize(14)
        self.urlbar.setStyleSheet("background-color:whitesmoke;color:black;padding:5px;border-radius:2px;border:2px solid gray22;")
        self.urlbar.setFont(font)
        if (self.urlbar.text() == ""):
            self.urlbar.setPlaceholderText("Website URL oder Google-Suche..")
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        self.httpsicon = QLabel()
        self.httpsicon.setPixmap( QPixmap( os.path.join('icons','lock.png') ) )
        navtb.addWidget(self.httpsicon)

        navtb.addWidget(self.urlbar)
        stop_btn = QAction(QIcon(os.path.join('icons','stop_ICON.png')), "Laden stoppen", self)
        stop_btn.setStatusTip("Laden der Seite stoppen")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)

        copy_site = QAction(QIcon(os.path.join('icons','copy_icon.png')), "Quelltext kopieren", self)
        copy_site.setStatusTip("Quelltext der Seite kopieren")
        copy_site.triggered.connect(self.copy_SITE)
        navtb.addAction(copy_site)

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "HTML/HOME.html"))
        local_url = QUrl.fromLocalFile(file_path)

        self.add_new_tab(local_url, 'Home')
        self.show()
        self.setWindowTitle("QuantaBrowser")

        #extractAction = QAction("&GET TO THE CHOPPAH!!!", self)
        #extractAction.setShortcut("Ctrl+Q")
        #extractAction.setStatusTip('Leave The App')
        #extractAction.triggered.connect(self.close_application)

        #self.statusBar()

        #mainMenu = self.menuBar()
        #fileMenu = mainMenu.addMenu('&File')
        #fileMenu.addAction(extractAction)
        #self.setStyleSheet("""QMenuBar {
            # background-color: whitesmoke;
        #}""")

    def copy_SITE(self):
        qurl = self.tabs.currentWidget().url()
        #PyQt5.QtCore.QUrl('http://www.google.com')
        Q = "%s"%(qurl)
        arguments = Q.split("'")
        URL = arguments[1]
        response = request.urlopen(URL)
        other_args = URL.split('.')
        if ("www" in URL):
            __file_name = other_args[1]
        else:
            __file_name = other_args[0]
        try:
            file = open('C:/Users/datei_%s.html'%(__file_name),"w")
            file.write(response.read().decode())
            file.close()
        except Exception as e:
            print("Fehler beim Speichern der Datei! \n\n%s\n\n"%(e))

    def add_new_tab(self, qurl = None, label ="Neuer Tab"):
        if (qurl is None):
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "HTML/HOME.html"))
            qurl = QUrl.fromLocalFile(file_path)
            #self.tabs.currentWidget().setUrl(local_url)
            #qurl = QUrl('http://www.google.com')
            #self.urlbar.setStyleSheet("background-color:whitesmoke;color:black;padding:5px;border-radius:2px;text-align:center;border:2px solid mediumseagreen;")

        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser = browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i = i, browser = browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if (i == -1):
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_title(self, browser):
        if (browser != self.tabs.currentWidget()):
            return

        title = self.tabs.currentWidget().page().title()

        self.setWindowTitle("% s - QuantaBrowser" % title)

    def navigate_home(self):
        unsichere_URLS = [
            'bild.de'
        ]
        q = QUrl(self.urlbar.text())
        ttt = self.urlbar.text()
        print(ttt)
        #print(unsichere_URLS)
        for URL in unsichere_URLS:
            if (URL in ttt):
                unsicher = True
                self.urlbar.setStyleSheet("background-color:whitesmoke;color:black;padding:5px;border-radius:2px;text-align:center;border:2px solid darkred;")
                break
            else:
                unsicher = False
        google_search = False
        if (q.scheme() == ""):
            if ("." not in ttt):
                google_search = True
                self.urlbar.setStyleSheet("background-color:whitesmoke;color:black;padding:5px;border-radius:2px;text-align:center;border:2px solid mediumseagreen;")
            else:
                q.setScheme("http")
                self.urlbar.setStyleSheet("background-color:whitesmoke;color:black;padding:5px;border-radius:2px;text-align:center;border:2px solid darkred;")
                google_search = False
        if (unsicher == False):
            if (google_search == True):
                new_q = QUrl("https://www.google.com/search?-b-d&q=%s"%(ttt))
                file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "HTML/HOME.html"))
                local_url = QUrl.fromLocalFile(file_path)
                self.tabs.currentWidget().setUrl(local_url)
                self.urlbar.setStyleSheet("background-color:whitesmoke;color:black;padding:5px;border-radius:2px;text-align:center;border:2px solid mediumseagreen;")
            else:
                file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "HTML/HOME.html"))
                local_url = QUrl.fromLocalFile(file_path)
                self.tabs.currentWidget().setUrl(local_url)
                self.urlbar.setStyleSheet("background-color:whitesmoke;color:black;padding:5px;border-radius:2px;text-align:center;border:2px solid mediumseagreen;")
        else:
            self.redirect_to_unsicher_nachricht()

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        ttt = self.urlbar.text()
        if ("." not in ttt):
            google_search = True
        else:
            q.setScheme("http")
            google_search = False
        if (google_search == True):
            new_q = QUrl("https://www.google.com/search?-b-d&q=%s"%(ttt))
            self.tabs.currentWidget().setUrl(new_q)
            self.urlbar.setStyleSheet("background-color:whitesmoke;color:black;padding:5px;border-radius:2px;text-align:center;border:2px solid mediumseagreen;")
        else:
            self.tabs.currentWidget().setUrl(q)
        q = QUrl(self.urlbar.text())

        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser = None):

        if browser != self.tabs.currentWidget():
            return
        HTTP_pixmap = QPixmap('icons/unsecured-shield.svg')
        HTTPS_pixmap = QPixmap('icons/shield_2.png')
        __HTTPS_PIXMAP = HTTPS_pixmap.scaled(40, 40)
        __HTTP_PIXMAP = HTTP_pixmap.scaled(40, 40)

        if ("HTML/HOME.html" != q.toString()):
            if (q.scheme() == 'https'):
                # Secure padlock icon
                self.httpsicon.setPixmap(__HTTPS_PIXMAP)
                self.urlbar.setStyleSheet("background-color:whitesmoke;color:black;padding:5px;border-radius:2px;text-align:center;border:2px solid mediumseagreen;")

            else:
                # Insecure padlock icon
                self.httpsicon.setPixmap(__HTTP_PIXMAP)
                self.urlbar.setStyleSheet("background-color:whitesmoke;color:black;padding:5px;border-radius:2px;text-align:center;border:2px solid darkred;")
        else:
            self.httpsicon.setPixmap(__HTTPS_PIXMAP)
            self.urlbar.setStyleSheet("background-color:whitesmoke;color:black;padding:5px;border-radius:2px;text-align:center;border:2px solid gray22;")

        if ("HTML/HOME.html" != q.toString()):
            self.urlbar.setText(q.toString())
        else:
            self.urlbar.setText("")
        self.urlbar.setCursorPosition(0)

app = QApplication(sys.argv)
app.setApplicationName("QuantaBrowser")
window = MainWindow()

# loop
app.exec_()
