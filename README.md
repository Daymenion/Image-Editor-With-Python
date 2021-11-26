“PHOTO EDITOR PROJECT Mehmet ÜNLÜ - 05200000789

Proje Özeti ve kapsamı
======================

*Bu proje; fotoğrafları düzenlemek, onları kırpmak, onların üzerine
çizim eklemek, fotoğrafın üzerine yeni fotoğraflar eklemek, filtre
eklemek, fotoğrafların üzerinde morphologic işlemler yapmak, video
işlemek ve benzeri özellikleri içinde bulunduran genel kapsamlı bir
projedir.*

*Proje; 3.8 python sürümüyle requirements.txt’de yazılan kütüphaneler
kullanılarak oop standartları ile Pycharm Profesional Edition 2021.2.3
sürümüyle Mehmet Ünlü tarafından yapılmıştır ve MIT lisans
kapsamındadır, free to use olarak sonraki kullanımlarında ücretsiz ve
sınırsız olarak kullanılabilir. *

 PROJECT FEATURES
=================

1) Görüntü Yükleme ve Kaydetme
------------------------------

Görüntü yükleme ve kadetme işlemi interface.py dosyasında yapılmaktadır.

### Görüntü Yükleme

def new\_button\_released(self, event):\
if self.winfo\_containing(event.x\_root, event.y\_root) ==
self.new\_button:\
if self.master.is\_draw\_state:\
self.master.interface\_functions.deactivate\_draw()\
if self.master.is\_crop\_state:\
self.master.interface\_functions.deactivate\_crop()\
if self.master.is\_paste\_state:\
self.master.interface\_functions.deactivate\_paste()\
\
filename = filedialog.askopenfilename()\
image = cv2.cvtColor(np.array(Image.open(filename)),
cv2.COLOR\_BGR2RGB)\
\
if image is not None:\
self.master.filename = filename\
self.master.original\_image = image.copy()\
self.master.processed\_image = image.copy()\
self.master.interface\_functions.show\_image()\
self.master.is\_image\_selected = True\
self.master.num\_rows, self.master.num\_cols =
self.master.processed\_image.shape\[:2\]

Öncelikle eventin new button üzerinde olup olmadığı kontrol edilir.
Sonrasında draw, crop, ya da paste stateleri kontrol edilir, eğer
onlardan bazıları aktif haldeyse deaktif yapılır. Fotoğraf seçilmemişken
bu statelerde bulunamazsınız, buradaki kontrolün sebebi ise tekrardan
fotoğraf seçilmek istenirse programın bize hata fırlatmaması ya da ara
yüzde değişik olaylarla karşılaşılmaması içindir.

Hata kontrolünden sonra ise tkinterın filedialog yardımı ile
kullanıcının dosya seçemesi sağlanır seçtiği dosya yolu filename olarak
kaydedilir. Sonrasında ise Pillowun open komutu ile fotoğraf açılır,
arraye dönüştürülür ve sonrasında bgr2rgbye dönüştürülür ve image yerel
değişkenine atanır. Canvasda renklerin farklı görünmemesi için bu
bgr2rgb işlemini yapıyoruz. Çünkü resimler default olarak bgr olarak
açılırlar, sonrasında yaptığımız tüm işlemler rgbye göre olduğu için bu
hatayı önlemeyi amaçlıyorum.

Eğer image seçilmişse ana classımız olan master’a kaydedilme işlemleri
yapılır. Oop yapısı ile projeyi yapmış bulunduğum için bunu yapmam
gerekiyor aksi halde her fonksiyonun aynı yerde olduğu 600 satırlık bir
kod yazmam gerekirdi ve birçok fonksiyonda garbage collector bizim
resmimizi boşaltacağı için hatalarla yüzleşmek zorunda kalırdım.

Burada dikkat etmemiz gereken kısım işlenmesi için ayrı bir fotoğraf,
cache olarak arka planda tutulması için ayrı bir fotoğraf tutmamız
gerekir aksi halde her bir deneme için kullanıcının tekrardan uygulamayı
başlatması gerekir

![](media/image1.png){width="6.268055555555556in"
height="4.277083333333334in"}

New butonuna tıkladıktan sonra Sample imagestan CreationOfAdam tablosunu
seçiyorum.

![](media/image2.png){width="6.268055555555556in"
height="4.246527777777778in"}

Fotoğraf seçildikten sonra canvasta fotoğrafımız oluşturuluyor.
(interfaceFunctions kısmında anlatıyorum görüntünün nasıl
oluşturulduğunu)

### Görüntünün Üzerine Görüntü Ekleme

def addMoreImage\_button\_released(self, event):\
if self.winfo\_containing(event.x\_root, event.y\_root) ==
self.addMoreImage\_button:\
if self.check\_status():\
filename = filedialog.askopenfilename()\
image = cv2.cvtColor(np.array(Image.open(filename)),
cv2.COLOR\_BGRA2RGBA)\
\
if image is not None:\
self.master.more\_imageFilename = filename\
self.master.more\_image = image.copy()\
self.master.interface\_functions.activate\_paste()

Eventi kontrol ettikten sonra statüleri kontrol etme fonksiyonuna
gönderiyoruz. Check\_status sonrasında da çok fazla kullanacağımız bir
fonksiyon şimdiden buraya koyuyorum.

def check\_status(self):\
if self.master.is\_image\_selected:\
if self.master.is\_crop\_state:\
self.master.interface\_functions.deactivate\_crop()\
if self.master.is\_draw\_state:\
self.master.interface\_functions.deactivate\_draw()\
if self.master.is\_paste\_state:\
self.master.interface\_functions.deactivate\_paste()\
return True\
return False

Öncelikle fotoğraf seçili mi diye kontrol ediyoruz, sonrasında ise crop,
draw, paste statüleri kontrol ediliyor ve true değerini yolluyoruz. True
yollamamız demek yapılacak işin devam edilmesi manasına geliyor, false
ise sürecin durdurulmasına, zira fotoğraf seçilmemişse süreç devam
etmemeli.

Ana fotoğrafın üzerine fotoğraf ekleme görevini üstlenen buradaki
fonksiyonumuzda ekstra olarak aktivate paste fonksiyonuna yolluyoruz
çünkü sonradan eklenen fotoğrafı nereye eklemek istediğinizi
seçebilirsiniz. Paste kısmını uzaysal dönüşüm işlemlerinde göstereceğim.

![](media/image3.png){width="6.268055555555556in"
height="3.1770833333333335in"}

### Görüntüyü Görüntü Dosyasının Üzerine Kaydetme

def save\_button\_released(self, event):\
if self.winfo\_containing(event.x\_root, event.y\_root) ==
self.save\_button:\
if self.check\_status():\
save\_image = self.master.processed\_image\
image\_filename = self.master.filename\
cv2.imwrite(image\_filename, save\_image)

Gerekli kontrolden sonra zaten halihazırda filename’i master class
içerisinde tutuyorduk, işlenmiş olan fotoğrafımızı cv2’nin imwrite
fonksiyonu ile o filename’e kaydetiyorum böylece üzerine yazmış
oluyorum.

CreationOfAdam1 diye denemeniz için kopya fotoğraf oluşturuyorum. Asıl
fotoğrafın kaybolmaması için. Sizde onun üzerinden deneyebilirsiniz.

![](media/image4.png){width="6.268055555555556in"
height="3.5756944444444443in"}

### Görüntüyü Farklı İsimle Kaydetme

def save\_as\_button\_released(self, event):\
if self.winfo\_containing(event.x\_root, event.y\_root) ==
self.save\_as\_button:\
if self.check\_status():\
original\_file\_type = self.master.filename.split('.')\[-1\]\
filename = filedialog.asksaveasfilename()\
filename = filename + "." + original\_file\_type\
\
save\_image = self.master.processed\_image\
cv2.imwrite(filename, save\_image)\
\
self.master.filename = filename

Filedialogdan Asksaveasfılename fonksiyonunu kullanarak kullanıcıdan
dosya adını alıyoruz. Bundan önce ise hali hazırda var olan filename i
split edip dosya formatını alıyoruz ki yeni fotoğrafımızı o formatla
kaydedelim, sonrasında ise kullanıcının verdiği isimle split edilmiş
filenameyi birleştirip kaydediyoruz. İsim vermezseniz yinede kaydodulur.

![](media/image5.png){width="6.268055555555556in"
height="4.209722222222222in"}

Kaydetme klasorü windowsdan gelen bir özelliklik olarak son açılan
dosyayanın konumuna tabidir. İsterseniz farklı bir yere
kaydedebilirsiniz.

![](media/image6.png){width="6.268055555555556in"
height="2.520138888888889in"}

2) Ara yüz / Form Ortamı Oluşturma
----------------------------------

Temel olarak proje, 2 tip python dosyasından oluşmaktadır. Arayüz
dosyaları ve arayüzdeki bazı işleri yapacak olan arayüz fonksiyonları.
Arayüz dosyalarını inceleyelim.

### \_\_init\_\_.py

Arayüz fonksiyonlarını başlatan \_\_init\_\_.py dosyasıdır. Main.py i
import eder ve rootu main yaparak mainloopa alır, tek amacı budur.

from main import Main\
\
\
root = Main()\
root.mainloop()

Programın daha anlaşılır olabilmesi ve oop yapısına uygun olabilmesi
için tercih ettim.

### main.py

Main dosyası Arayüzümüzün master dosyasıdır. Bu yüzden init olarak
kendisini işaret eder, ve interface framemizi alır. Global olarak
kullanılacak olan değişkenlerin tutulduğu yerdir.

import tkinter as tk\
from tkinter import ttk\
from interface import Interface\
from InterfaceFunctions import InterfaceFunctions\
\
\
class Main(tk.Tk):\
\
def \_\_init\_\_(self):\
tk.Tk.\_\_init\_\_(self)\
\
self.filename = ""\
self.more\_imageFilename = ""\
self.original\_image = None\
self.processed\_image = None\
self.rotating\_image = None\
self.drawing\_cache = list()\
self.more\_image = None\
self.is\_image\_selected = False\
self.is\_draw\_state = False\
self.is\_crop\_state = False\
self.is\_paste\_state = False\
self.num\_rows, self.num\_cols = None, None\
self.filtering\_frame = None\
self.adjusting\_frame = None\
self.edge\_detection\_frame = None\
\
self.title("Image Editor by Daymenion")\
\
self.interface = Interface(master=self)\
separator1 = ttk.Separator(master=self, orient=tk.HORIZONTAL)\
self.interface\_functions = InterfaceFunctions(master=self)\
\
self.interface.pack(fill=tk.BOTH)\
separator1.pack(fill=tk.X, padx=10, pady=5)\
self.interface\_functions.pack(fill=tk.BOTH, padx=10, pady=10, expand=1)

İnterfaceimizi mainloopa packliyoruz ve daha güzel görünmesi için birkaç
pad ayarı yapıyoruz.

### interface.py

İnterface, isminden de anlaşılacağı gibi ara yüzümüzün ta kendisidir.
Bütün frameler gibi masterı master class olarak alır, yani main
dosyamızı. İçerisinde Button tanımlamaları, label tanımlamaları ve diğer
TopLevellara hangi şartlarda nasıl geçileceğine dair düzenlemeleri
içerir. Diğer TopLevellara geçişimizi sağlayan yer de haliyle burasıdır.

class Interface(Frame):\
\
def \_\_init\_\_(self, master=None):\
Frame.\_\_init\_\_(self, master=master, bg='gray', width=1280,
height=100)\
\
self.pasted = False\
\
self.new\_button = Button(self, text="New", bg='gold', fg='black',
width=10, font="ariel 13 bold")\
self.save\_button = Button(self, text="Save", bg='black', fg='gold',
width=10, font="ariel 13 bold")

……….

def filter\_button\_released(self, event):\
if self.winfo\_containing(event.x\_root, event.y\_root) ==
self.filter\_button:\
if self.check\_status():\
self.master.filtering\_frame = FilteringTopLevel(master=self.master)\
self.master.filtering\_frame.grab\_set()

Yukarıda örnek bazı buttonlar ve örnek olarak diğer toplevelara nasıl
geçileceğini gösterilmektedir. Diğer Toplevellara geçmek için tkinter
içerisinde olan grab.set() i kullanıyoruz. Arayüzde, elbetteki işlemler
event fonksiyonlarıyla yapılıyor bu sayede nereye tıkladığınız hatta
draw da olacağı gibi (ileride göreceksiniz) event üzerinden diğer
bilgilere erişeceğiz.

Burada bir farka değinmek gerekirse Frame ile TopLevel arasındaki
farktır. Frame ana mainloop içerisinde gösterilen elementler için
kullanılır, Toplevel ise yeni bir pencere içerisinde bazı şeyleri
seçtirtmek istiyorsanız ve bunları arayüze daha sonra gönderecek veya
göndermeyecekseniz (TopLevel üzerinde kullanıcaksanız) kullanılır.
Arayüz oluşturan temel yapımız Frame olduğu için Frame kısımlarını
anlatıyorum. Diğer TopLevel kısımlarını ise onun konusun geldiğinde
göreceğiz.

### interfaceFunctions.py

İsminden de anlaşılacağı gibi interface fonksiyonlarını tutan
framemimizdir. Bu Framein en temel amacı görüntü oluşturmaktır, diğer
TopLevellardan gelen ya da interfaceden gelen görüntüyü ve değişikleri
oluşturur. Bunu yapabilmek içinde canvas bu Frame de tanımlanmıştır.

class InterfaceFunctions(Frame):\
def \_\_init\_\_(self, master=None):\
Frame.\_\_init\_\_(self, master=master, bg="black", width=1280,
height=720)\
\
self.shown\_image = None\
self.x = 0\
self.y = 0\
self.crop\_start\_x = 0\
self.crop\_start\_y = 0\
self.crop\_end\_x = 0\
self.crop\_end\_y = 0\
self.rectangle\_id = 0\
self.ratio = 0\
self.rotate\_angle = 0\
\
self.canvas = Canvas(self, bg="black", width=1280, height=720)\
self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

Canvası ve canvas ayarlarını görmektesiniz, görüntü oluşturma işini
yapan fonksiyonumuz ise show\_image fonksiyonudur.

def show\_image(self, img=None):\
self.clear\_canvas()\
\
if img is None:\
image = self.master.processed\_image.copy()\
else:\
image = img\
\
image = cv2.cvtColor(image, cv2.COLOR\_BGR2RGB)\
height, width, channels = image.shape\
ratio = height / width\
\
new\_width = width\
new\_height = height\
\
if height &gt; self.winfo\_height() or width &gt; self.winfo\_width():\
if ratio &lt; 1:\
new\_width = self.winfo\_width()\
new\_height = int(new\_width \* ratio)\
else:\
new\_height = self.winfo\_height()\
new\_width = int(new\_height \* (width / height))\
\
self.shown\_image = cv2.resize(image, (new\_width, new\_height))\
self.shown\_image =
ImageTk.PhotoImage(Image.fromarray(self.shown\_image))\
\
self.ratio = height / new\_height\
\
self.canvas.config(width=new\_width, height=new\_height)\
self.canvas.create\_image(new\_width / 2, new\_height / 2,
anchor=CENTER, image=self.shown\_image)

Bu kısımda öncelikle parametre olarak bize bir image gönderilmemiş ise
işlenmiş olan görüntümüzün kopyasını alıyoruz, gönderilmiş ise o image
üzerinden işlem yapıyoruz. BGR olma ihtimaline karşın dönüşüm
uyguluyoruz. İmage’in kanallarını alıyoruz ve en boy oranını çıkıyoruz.
Bu sayede image croplanmışsa ya da image’in boyutu canvasın boyutundan
büyükse orantılayacağız. Canvas boyutu ile karşılaştırıp oranlama işlemi
yapıyoruz. Eğer width’i height’ından büyük ise width’i canvas widthine
eşitleyip, sonrasında ise yeni width’i oranla çarparak yeni heigthı elde
ediyoruz böylece, oranlamayı da bozmamış oluyoruz. Eğer orantılaması
böyle değilse ise canvasın boyutlarını image boyutlarına atıyoruz.
Fotoğrafı bu yeni boyutlara göre resize edip onu bir photo image’a
dönüştürüyoruz ki böylece canvasda gösterebilelim (canvas.create\_image
photoimage formatını kabul eder). Sonrasında ise image’ı canvasda
yaratıyoruz.

3) Görüntüyü Filtreleme
-----------------------

Arayüzden filtreleme butonuna tıkladıktan sonra (fotoğraf seçili
olmalı). İnterface.py içerisinde yer alan bu event fonksiyonu ile
filteringTopLevelini açıyoruz. Grabset Toplevellara geçiş için
kullanılan tkinter fonksiyonlarından birisidir.

def filter\_button\_released(self, event):\
if self.winfo\_containing(event.x\_root, event.y\_root) ==
self.filter\_button:\
if self.check\_status():\
self.master.filtering\_frame = FilteringTopLevel(master=self.master)\
self.master.filtering\_frame.grab\_set()

Filtering Top Leveli; 2 değişkene, 11 farklı filtrelemeye, aply ve
cancel buttonlarına sahip bir Top Leveldir.

class FilteringTopLevel(Toplevel):\
def \_\_init\_\_(self, master=None):\
Toplevel.\_\_init\_\_(self, master=master)\
\
self.original\_image = self.master.processed\_image\
self.filtered\_image = None\
\
self.negative\_button = Button(master=self, text="Negative")\
self.black\_white\_button = Button(master=self, text="Black White")

Local değişkenimiz olan self.orginal\_image bir cache olarak kullanılır,
hali hazırda işleniyor olan ana resmimizi alır. Kullanıcı, süreci
cancellarsa yada farklı filtrelemeler farklı zamanlarda kullanılmak
istenirse ana resmimizi değiştirmemiz gerekir. Eğer ana resmimizi
değiştirirsek kullanıcı geri adım atmak istediğinde, fotoğraf çoktan
değişmiş olacak ve haliyle kullanıcı yaptığı şeyden dolayı pişmanlık
duyabilecektir.

![](media/image7.png){width="1.9270833333333333in"
height="3.9479166666666665in"} Açılan Filter Top Leveli

### Negative Filter

def negative\_button\_released(self, event):\
self.negative()\
self.show\_image()

Negative button basıldığında yukarıdaki event fonksiyonumuza gideriz ve
oradan da negative fonksiyonumuza gidilir ve fotoğrafa negative filter
eklenir. Sonrasında da show\_image a yollanarak filterlanmış fotoğraf
ekran da gösterilir.

def show\_image(self):\
self.master.interface\_functions.show\_image(img=self.filtered\_image)

Unutmayın bu gösterilme kaydetme işlemi değildir, eklediğiniz
filterların orijinal fotoğrafa uygulanması için Apply tuşuna basmanız
gerekir.

def negative(self):\
self.filtered\_image = cv2.bitwise\_not(self.original\_image)

Negative filtresini cv2’deki bitwise\_not fonksiyonu ile yapıyoruz.

![](media/image8.png){width="6.268055555555556in"
height="3.6166666666666667in"}

Çok basit bir şey olsa da ona değinme gereği duyuyorum. Eventin farklı
türleri bulunmaktadır bu eventimiz;

self.negative\_button.bind("&lt;ButtonRelease&gt;",
self.negative\_button\_released)

Diğer eventler gibi Button released ile oluşturulmuştur. Yani Mouse 1
tuşu ile butona bastığınızda değil, o tuş üzerindeyken mouse u
bıraktığınızda çalışır. Yani basitçe tıklama mantığıdır o tuşa
tıklamanız gerekir. Bu tip En yaygın buton eventidir gördüğünüz
neredeyse her uygulama bunu mutlaka bulundurur. Bunun yararı ise,
yanlışlıkla bir buttona bastığınızda, elinizi mouse 1 den kaldırmayarak
mouse imlecinizi başka yere taşıyıp o butonun aktifleşmesini
önleyebilirsiniz.

### Black and White Filter

def black\_white\_released(self, event):\
self.black\_white()\
self.show\_image()

def black\_white(self):\
self.filtered\_image = cv2.cvtColor(self.original\_image,
cv2.COLOR\_BGR2GRAY)\
self.filtered\_image = cv2.cvtColor(self.filtered\_image,
cv2.COLOR\_GRAY2RGB)

Black and white filtresini de hepimizin ilk aklına gelen yolla
yapıyorum. CVt colorla fotoğrafı GRAY yani black and white formatına
sokup sonrasında tekrardan rgb’e dönüştürüyorum.

![](media/image9.png){width="6.268055555555556in"
height="3.6597222222222223in"}

### Sepia Filter

def sepia\_button\_released(self, event):\
self.sepia()\
self.show\_image()

def sepia(self):\
kernel = np.array(\[\[0.272, 0.534, 0.131\],\
\[0.349, 0.686, 0.168\],\
\[0.393, 0.769, 0.189\]\])\
\
self.filtered\_image = cv2.filter2D(self.original\_image, -1, kernel)

Sepia filterını filter2D ile yapıyorum. Öncelikle bir tane array
oluşturuyorum ve kernele atıyorum. Array değerleri sepia filtresi için
önceden belirlenmiş birçok yerde bulunabilecek değerler isterseniz küçük
değişikliklerle sepia oranını da değiştirebilirsiniz. Sonrasında da
filter2D ile bu kerneli fotoğrafımıza uyguluyoruz.

![](media/image10.png){width="6.268055555555556in"
height="3.6534722222222222in"}

### Emboss Filter

def emboss\_button\_released(self, event):\
self.emboss()\
self.show\_image()

Aynı işlemi sadece array değerlerini değiştirerek burada da uyguluyoruz.

def emboss(self):\
kernel = np.array(\[\[0, -1, -1\],\
\[1, 0, -1\],\
\[1, 1, 0\]\])\
\
self.filtered\_image = cv2.filter2D(self.original\_image, -1, kernel)

![](media/image11.png){width="6.268055555555556in"
height="3.5590277777777777in"}

### Gaussian Blur Filter

def gaussian\_blur\_button\_released(self, event):\
self.gaussian\_blur()\
self.show\_image()

cv2’deki gaussianBlur fonksiyonu ile filtreyi uyguluyoruz.

def gaussian\_blur(self):\
self.filtered\_image = cv2.GaussianBlur(self.original\_image, (41, 41),
0)

![](media/image12.png){width="6.268055555555556in"
height="3.535416666666667in"}

### Median Blur Filter

def median\_blur\_button\_released(self, event):\
self.gaussian\_blur()\
self.show\_image()

Gaussıan Blue ile Median Blurun Blur uygulama değerini aynı tuttum
isterseniz onu da değiştirebilirsiniz.

def median\_blur(self):\
self.filtered\_image = cv2.medianBlur(self.original\_image, 41)

![](media/image13.png){width="6.268055555555556in"
height="3.5430555555555556in"}

### Edges of Photo Filter

def edges\_button\_released(self, event):\
self.edges()\
self.show\_image()

Pillowdaki find Edges kulanarak oluşturduğumuz bir filtredir.

def edges(self):\
self.filtered\_image =
np.array(Image.fromarray(self.original\_image).filter(FIND\_EDGES))

![](media/image14.png){width="6.268055555555556in"
height="3.5618055555555554in"}

### Foil Art Filter

def foilPic\_button\_released(self, event):\
self.foilPic()\
self.show\_image()

Pillowdaki emboss fonksiyonu ile oluşturduğumuz bir filtredir. Alçı
kabartarak yapılmış bir görünüm edası verdiği için bu tarz bir isim
seçtim.

def foilPic(self):\
self.filtered\_image =
np.array(Image.fromarray(self.original\_image).filter(EMBOSS))

![](media/image15.png){width="6.268055555555556in"
height="3.5409722222222224in"}

### Sharp Paint Filter

def pencilPic\_button\_released(self, event):\
self.pencilPic()\
self.show\_image()

Bu filteryi pillowun edge enhance more filtresi ile yapıyorum. Daha net
ve gerçek fotoğraflarda daha belirdin sonuçlar verecektir.

def pencilPic(self):\
self.filtered\_image =
np.array(Image.fromarray(self.original\_image).filter(EDGE\_ENHANCE\_MORE))

![](media/image16.png){width="6.268055555555556in"
height="3.5388888888888888in"}

### Oil Paint Filter

def oilPic\_button\_released(self, event):\
self.oilPic()\
self.show\_image()

Sharp paintle arasındaki fark burada edge\_enhance ken orada
edge\_enhance\_more filtresini kullanıyoruz.

def oilPic(self):\
self.filtered\_image =
np.array(Image.fromarray(self.original\_image).filter(EDGE\_ENHANCE))

![](media/image17.png){width="6.268055555555556in"
height="3.609027777777778in"}

### Sketch Light Filter

def sketchPic\_button\_released(self, event):\
self.sketchPic()\
self.show\_image()

Pillowdaki countour filtresiyle de bu fonksiyonu uyguluyorum.

def sketchPic(self):\
self.filtered\_image =
np.array(Image.fromarray(self.original\_image).filter(CONTOUR))

![](media/image18.png){width="6.268055555555556in"
height="3.642361111111111in"}

### Apply Button

def apply\_button\_released(self, event):\
self.master.image\_cache.append(self.master.processed\_image.copy())\
self.master.processed\_image = self.filtered\_image\
self.show\_image()\
self.close()

image\_cache’e filterlanmamış bir önceki adımdaki image cache’e eklenir.
Daha detaylı anlatım için ekstra özellikler kısmına bakınız. Bundan
sonra ise filterlanmış image hali hazırda işlenen fotoğrafa atanır ve bu
fotoğraf canvasda gösterilip Top Level kapatalır.

def close(self):\
self.destroy()

### Cancel Button

def cancel\_button\_released(self, event):\
self.master.interface\_functions.show\_image()\
self.close()

Ana fotoğrafımız canvasa gönderilip Top Level kapatılır.

4) Histogram Eşikleme
---------------------

Morphologic işlemler kısmında bulunmaktadır, o kısma bakınız.

5) Uzaysal Dönüşüm İşlemleri
----------------------------

Uzaysal Dönüşüm işlemleri için bir Top Level bulunmamaktadır onun yerine
arayüz içerisinde yer almaktadır.

![](media/image19.png){width="6.268055555555556in"
height="0.6923611111111111in"}

Arayüzde bulunduğu için butonları ve labelleri, interface.py içerisinde,
işlemler (fonksiyonlar) ise interfaceFunctions.py içerisinde
bulunmaktadır.

self.draw\_button.bind("&lt;ButtonRelease&gt;",
self.draw\_button\_released)\
self.undo\_button.bind("&lt;ButtonRelease&gt;",
self.undo\_button\_released)\
self.forward\_button.bind("&lt;ButtonRelease&gt;",
self.forward\_button\_released)\
self.crop\_button.bind("&lt;ButtonRelease&gt;",
self.crop\_button\_released)\
self.rotate\_button.bind("&lt;ButtonRelease&gt;",
self.rotate\_button\_released)\
self.saveRotation\_button.bind("&lt;ButtonRelease&gt;",
self.saveRotation\_button\_released)\
self.resize\_button.bind("&lt;ButtonRelease&gt;",
self.resize\_button\_released)\
self.addMoreImage\_button.bind("&lt;ButtonRelease&gt;",
self.addMoreImage\_button\_released)\
self.flip\_button.bind("&lt;ButtonRelease&gt;",
self.flip\_button\_released)\
self.contrast\_button.bind("&lt;ButtonRelease&gt;",
self.contrast\_button\_released)

### Draw State

def draw\_button\_released(self, event):\
if self.winfo\_containing(event.x\_root, event.y\_root) ==
self.draw\_button:\
if self.check\_status():\
self.master.interface\_functions.activate\_draw()

Draw butonuna basıldığında statüler kontrol edilip interface functions
activate draw a gönderilir. Draw, paste ve crop stateleri için activate,
deactivate, start ve main olmak üzere fonksiyonlara ayrılmıştır. Bu üç
durumda da button motiona ihtiyacımız olduğu için böyle bir yol izledim.

def activate\_draw(self):\
self.canvas.bind("&lt;ButtonPress&gt;", self.start\_draw)\
self.canvas.bind("&lt;B1-Motion&gt;", self.draw)\
\
self.master.is\_draw\_state = True

mouse 1 e basıldığında start draw’a gider ve başlangıç konumunu alır,
mouse 1 bırakılmadan mousun hareketini de draw’a yollar.

def start\_draw(self, event):\
self.master.image\_cache.append(self.master.processed\_image.copy())\
self.x = event.x\
self.y = event.y

Event’den x ve y değerlerini alıp local değişkinimize atar, Üstte
yaptığımız işlem ise cache oluşturmak bunu elimizdeki fotoğrafın
değiştirildiği tüm yerlerde göreceksiniz. Bundan 10) ekstra özellikler
kısmında bahsediyor olacağım.

def draw(self, event):\
self.canvas.create\_line(self.x, self.y, event.x, event.y, width=2,\
fill="red", capstyle=ROUND, smooth=True)\
\
cv2.line(self.master.processed\_image, (int(self.x \* self.ratio),
int(self.y \* self.ratio)),\
(int(event.x \* self.ratio), int(event.y \* self.ratio)),\
(0, 0, 255), thickness=int(self.ratio \* 2),\
lineType=8)\
\
self.x = event.x\
self.y = event.y

Hem kullanıcının çizdiği line ı görebilmesi hem de bu line ın fotoğrafın
kendisinde oluşturmak için canvas.create\_line ile cv2.line
kullanıyorum. Başlangıç noktaları self.x ve self.y olup event.x ve
evet.y’e kadar line çizecek maouse 1 basılı oldukça. Self.ratio 1.0
değerinde olacaktır. Fotoğrafımız show image kısmında yeniden
boyutlandırılmışsa değişecektir diğer türlü 1.0 değerdindedir.

self.ratio = height / new\_height

Her adımda da selx, ve self y değerlerini değiştireceğiz.

def deactivate\_paste(self):\
self.canvas.unbind("&lt;ButtonPress&gt;")\
self.canvas.unbind("&lt;B1-Motion&gt;")\
self.canvas.unbind("&lt;ButtonRelease&gt;")\
\
self.master.is\_paste\_state = False

Deactiveta ise mouse hareketlerini devre dışı bırakıp state i false
çeker.

![](media/image20.png){width="6.268055555555556in"
height="3.540277777777778in"}

### Crop State

def crop\_button\_released(self, event):\
if self.winfo\_containing(event.x\_root, event.y\_root) ==
self.crop\_button:\
if self.check\_status():\
self.master.interface\_functions.activate\_crop()

def activate\_crop(self):\
self.canvas.bind("&lt;ButtonPress&gt;", self.start\_crop)\
self.canvas.bind("&lt;B1-Motion&gt;", self.crop)\
self.canvas.bind("&lt;ButtonRelease&gt;", self.end\_crop)\
\
self.master.is\_crop\_state = True

Mouse hareketlerimizi devreye sokuyoruz

def start\_crop(self, event):\
self.master.image\_cache.append(self.master.processed\_image.copy())\
self.crop\_start\_x = event.x\
self.crop\_start\_y = event.y

Cachemizi fotoğrafımızı ekleyip, başlangıç noktalarını alıyoruz. Mouse 1
ile

def crop(self, event):\
if self.rectangle\_id:\
self.canvas.delete(self.rectangle\_id)\
\
self.crop\_end\_x = event.x\
self.crop\_end\_y = event.y\
\
self.rectangle\_id = self.canvas.create\_rectangle(self.crop\_start\_x,
self.crop\_start\_y,\
self.crop\_end\_x, self.crop\_end\_y, width=1)

crop aşaması devam ettikçe rectangle çizmeye devam etmesini istemiyoruz,
sadece o anda bulunduğumuz yerde rectangle olmasını istiyoruz o yüzden
her mouse hareketi ile daha önceki rectangle’ı siliyoruz bu sayede
croplamaya çalışırken bir tane rectangle olur. Aksi halde mouse hareket
ettirirken sürekli olarak farklı yerlerde rectangle çizmeye devam eder.
Mouse 1 i bıraktığımızda da end cropa gönderir ve kırpma işmemimiz
tamalanır.

def end\_crop(self, event):\
if self.crop\_start\_x &lt;= self.crop\_end\_x and self.crop\_start\_y
&lt;= self.crop\_end\_y:\
start\_x = int(self.crop\_start\_x \* self.ratio)\
start\_y = int(self.crop\_start\_y \* self.ratio)\
end\_x = int(self.crop\_end\_x \* self.ratio)\
end\_y = int(self.crop\_end\_y \* self.ratio)\
elif self.crop\_start\_x &gt; self.crop\_end\_x and self.crop\_start\_y
&lt;= self.crop\_end\_y:\
start\_x = int(self.crop\_end\_x \* self.ratio)\
start\_y = int(self.crop\_start\_y \* self.ratio)\
end\_x = int(self.crop\_start\_x \* self.ratio)\
end\_y = int(self.crop\_end\_y \* self.ratio)\
elif self.crop\_start\_x &lt;= self.crop\_end\_x and self.crop\_start\_y
&gt; self.crop\_end\_y:\
start\_x = int(self.crop\_start\_x \* self.ratio)\
start\_y = int(self.crop\_end\_y \* self.ratio)\
end\_x = int(self.crop\_end\_x \* self.ratio)\
end\_y = int(self.crop\_start\_y \* self.ratio)\
else:\
start\_x = int(self.crop\_end\_x \* self.ratio)\
start\_y = int(self.crop\_end\_y \* self.ratio)\
end\_x = int(self.crop\_start\_x \* self.ratio)\
end\_y = int(self.crop\_start\_y \* self.ratio)\
\
x = slice(start\_x, end\_x, 1)\
y = slice(start\_y, end\_y, 1)\
\
self.master.processed\_image = self.master.processed\_image\[y, x\]\
self.master.image\_cache.append(self.master.processed\_image.copy())\
\
self.show\_image()

Koşullarla cropun start ve end noktalarını belirleriz, örneğin
self.crop\_start\_x, self crop\_end\_x den büyükse start\_x noktamız
self.crop\_end\_x noktamız olur. Değerleri farklı koşullara göre
ayarladıktan sonra da x ve y noktalarını ve slice gönderip, elimizdeki
fotoğrafın o kısmını main fotoğrafımıza atarız sonrada cache’imize bir
örnek göndeririz.

![](media/image21.png){width="6.268055555555556in"
height="3.560416666666667in"}

### Paste State

def addMoreImage\_button\_released(self, event):\
if self.winfo\_containing(event.x\_root, event.y\_root) ==
self.addMoreImage\_button:\
if self.check\_status():\
filename = filedialog.askopenfilename()\
image = cv2.cvtColor(np.array(Image.open(filename)),
cv2.COLOR\_BGRA2RGBA)\
\
if image is not None:\
self.master.more\_imageFilename = filename\
self.master.more\_image = image.copy()\
self.master.interface\_functions.activate\_paste()

Bu şekilde fotoğrafı ekliyoruz, zaten bunu ilk kısımda anlatmıştım.

def activate\_paste(self):\
self.canvas.bind("&lt;ButtonPress&gt;", self.start\_paste)\
self.canvas.bind("&lt;B1-Motion&gt;", self.pasting)\
self.canvas.bind("&lt;ButtonRelease&gt;", self.end\_paste)\
\
self.master.is\_paste\_state = True

Button press ile start paste’e yolluyoruz ve mouse hareketini takip
ediyoruz mouse1’i bıraktığınız anda fotoğraf oraya yapıştırılır.

def start\_paste(self, event):\
self.master.image\_cache.append(self.master.processed\_image.copy())\
self.x = event.x\
self.y = event.y

def pasting(self, event):\
global img\
img = ImageTk.PhotoImage(file=self.master.more\_imageFilename)\
self.canvas.create\_image(self.x, self.y, image=img)\
self.x = event.x\
self.y = event.y

Garbage collectorun fotoğraf erişimimize engel olmaması için image ı
global yapıyoruz. Az önce aldığımız fotoğraf filename’ındeki fotoğrafı
da Photo ımage olarak açıyoruz ki canvas da değişiklikler yapabilelim ve
gösterebilelim.

def end\_paste(self, event):\
master\_image = Image.fromarray(self.master.processed\_image).copy()\
pasting\_image = Image.fromarray(self.master.more\_image).copy()\
\
position = (self.x - int(pasting\_image.width/2), self.y -
int(pasting\_image.height/2))\
master\_image.paste(pasting\_image, position, pasting\_image)\
\
self.master.processed\_image = np.array(master\_image)\
self.show\_image()

Mouse 1 release edildiğinde en son atanan x ve y değerlerine göre paste
işlemi yapılır. Öncelikle pillowdaki fromarray fonksiyonu ile cv2 ile
açtığımız fotoğrafları paste işlemini yapacağımız forma sokuyoruz. Paste
işlemini pillowdaki paste fonksiyonu ile position’a yapıyoruz. Position
en son atanan, mouse 1 bırakılmadan önceki en son yerdeki self.x ve
self.y i alır. Fotoğraf canvasda yaratılırken ortalanarak
yaratılacaktır. Ama yapıştırma işlemindeki position başlangıç noktasını
alır haliyle başlangıç noktası olarak self.x den yapıştıracağımız
fotoğrafın genişliğinin yarısını çıkarıp self.y den ise yüksekliğinin
yarısını çıkararak ayarlıyoruz. Fotoğrafın orta noktasını o anki yere
taşıyoruz kısacası.

![](media/image22.png){width="6.268055555555556in"
height="3.647222222222222in"}

### Rotate State

def rotate\_button\_released(self, event):\
if self.winfo\_containing(event.x\_root, event.y\_root) ==
self.rotate\_button:\
if self.check\_status():\
self.master.interface\_functions.rotate(self.rotate\_entry.get())

Rotate butonuna tıklandığında, interfaceFunctionsdan rotate fonksiyonuna
rotate girmenizi istediğim entrty varlığındaki girdi yollanır.

def rotate(self, rotateAngle):\
if rotateAngle == '':\
rotateAngle = 60\
else:\
float(rotateAngle)\
self.rotate\_angle += rotateAngle\
self.master.rotating\_image =
np.array(Image.fromarray(self.master.processed\_image).rotate(self.rotate\_angle))\
self.master.image\_cache.append(self.master.rotating\_image.copy())\
self.show\_image(image=self.master.rotating\_image)

![](media/image23.png){width="1.4270833333333333in"
height="1.0833333333333333in"} Eğer entry’e bir değer girmezseniz
default olarak 60 derece alınır. Burada yaptığım en önemli nokta
döndürmelerinizin devamlılığını sağlamaktır. Eğer rotatelenmiş bir
fotoğrafı sürekli olarak döndürürseniz piksel kaybı, rotateAngle/360
sayısında döndürmeye kadar düşer ve elinizde pikselleşmiş ve merkeze
göre spiral bir hal alan görüntü oluşur. Bunu korumanın yolunu
düşünürken de böyle bir metod aklıma geldi. Kullanıcı her rotate tuşuna
bastırıldığında rotateAngle katlanır ve local bir değişken, original
görüntümüzün bu ölçüde döndürülmüş halini tutar ve canvasda değiştirir
bu sayede. Tek bir fotoğraf sürekli döndürülmüş olmaz. Kullanıcı
saveRotation tuşuna bastığında da fotoğrafımızın en son değiştirilmiş
hali işlenen fotoğrafımıza atanır.

def saveRotation\_button\_released(self, event):\
if self.winfo\_containing(event.x\_root, event.y\_root) ==
self.saveRotation\_button:\
if self.check\_status():\
self.master.processed\_image = self.master.rotating\_image

30 derecelik açı ile 4 kere döndürülmüş bir fotoğraf. Her rotate tuşuna
basısınızda bir kere döndürür. Kaydetmek için save rotatin tuşuna
basmayı unutmayınız.

![](media/image24.png){width="6.268055555555556in"
height="4.151388888888889in"}

### Resize State

def resize\_button\_released(self, event):\
if self.winfo\_containing(event.x\_root, event.y\_root) ==
self.resize\_button:\
if self.check\_status():\
self.master.interface\_functions.resizing(self.resizeX\_entry.get(),
self.resizeY\_entry.get())

Resize butonuna tıklandığında interface Functions’dan resize
fonksiyonuna gönderilir.

def resizing(self, x, y):\
if x or y == '':\
x, y = 500, 500\
else:\
x, y = int(x), int(y)\
self.master.image\_cache.append(self.master.processed\_image.copy())\
self.master.processed\_image =
np.array(Image.fromarray(self.master.processed\_image).resize((x, y)))\
self.master.image\_cache.append(self.master.processed\_image.copy())\
self.show\_image()

![](media/image25.png){width="1.21875in" height="0.9166666666666666in"}
Rotate yaptığımız gibi basit bir değer kontrolü yapıyoruz, eğer değer
girmeyi unutursanız otamatik olarak 500x500 olarak resize eder. Değerler
1280x720 gibi önce x sonra y değeri olacak şekilde girilmelidir.

![](media/image26.png){width="5.614583333333333in"
height="7.864583333333333in"}

### Flipping State

def flip\_button\_released(self, event):\
if self.winfo\_containing(event.x\_root, event.y\_root) ==
self.flip\_button:\
if self.check\_status():\
self.master.interface\_functions.flipping()

Flip butonuna bastığınızda interface Functionsdan flipping fonksiyonuna
yollanır.

def flipping(self):\
self.master.image\_cache.append(self.master.processed\_image.copy())\
flipping\_image = Image.fromarray(self.master.processed\_image).copy()\
flipping\_image = flipping\_image.transpose(Image.FLIP\_LEFT\_RIGHT)\
self.master.processed\_image = np.array(flipping\_image).copy()\
self.master.image\_cache.append(self.master.processed\_image.copy())\
self.show\_image()

Fotoğrafımız diğer işlemlerde olduğu gibi cache e atılır, fotoğrafımızın
bir kopyası pillow formatına dönüştürülür ve pillowdaki transpose
fonksiyonuna flip left to rigt vererek flipleme işlemini yapıyoruz.

![](media/image27.png){width="6.268055555555556in"
height="3.6222222222222222in"}

6) Yoğunluk Dönüşüm İşlemler
----------------------------

Morfolojik işlemlerle beraber anlatıyorum.

7) Morfolojik İşlemler
----------------------

Morfolojik işlemler ve Yoğunluk dönüşüm işlemleri Adjusting Top Level
içerisinde yer almaktadır.

def adjust\_button\_released(self, event):\
if self.winfo\_containing(event.x\_root, event.y\_root) ==
self.adjust\_button:\
if self.check\_status():\
self.master.adjusting\_frame = AdjustingTopLevel(master=self.master)\
self.master.adjusting\_frame.grab\_set()

Adjusting Top Level’da fotoğrafın parlaklık, r g b ayarları, kernel size
değiştirme seçeneği ile Erosion, Dilation, Openning, Closing, Gradient,
Top Hat, Black Hat, Ellipse, Rectangle, Cross, Histogram Eşikleme, Log
Transformation, Gamma Transformation morfolojik ve yoğunluk dönüşün
işlemlerini yapabilir, bunları kaydedebilir, yanlışlıkla eklediğiniz bir
filtre sonrası filtreleri temizleyebilir, işlemi iptal edebilir ya da ön
izleyebilirsiniz. ![](media/image28.png){width="2.6770833333333335in"
height="8.291666666666666in"}

Bu top levelda işlemleri gerçekleştirmek için pythonun dictionary
nimetlerinden yarlanıyorum.

self.isGetApplied = False\
self.morphologyDict = {\
"isGetHistogram": \[False, self.histogram\_button\_released\],\
"isGetErosion": \[False, True, cv2.MORPH\_ERODE\],\
"isGetDilation": \[False, True, cv2.MORPH\_DILATE\],\
"isGetOpen": \[False, True, cv2.MORPH\_OPEN\],\
"isGetClose": \[False, True, cv2.MORPH\_CLOSE\],\
"isGetGradient": \[False, True, cv2.MORPH\_GRADIENT\],\
"isGetTopHat": \[False, True, cv2.MORPH\_TOPHAT\],\
"isGetBlackHat": \[False, True, cv2.MORPH\_BLACKHAT\],\
"isGetEllipse": \[False, True, cv2.MORPH\_ELLIPSE\],\
"isGetRect": \[False, True, cv2.MORPH\_RECT\],\
"isGetCross": \[False, True, cv2.MORPH\_CROSS\],\
"isGetLogged": \[False, self.log\_button\_released\],\
"isGetPowerLaw": \[False, self.power\_law\_button\_released\]\
}

Bu yapıyı kullanmamın temel amacı r,g,b ve brıghtness ıslemlerını
prewıev butonu sırasında yapıyorum . Haliyle tüm yapının farklı yerlerde
ayrışması yerine tek bir yapıda hepsini toplamak ve kerneli belirlerken
ayrı ayrı uğraşmak yerine tek bir polymorphic yapı oluşturmak için böyle
yapıyorum. Öyleyse önce preview butonundan başlayalım.

### PREVİEW

def preview\_button\_released(self, event):\
self.processing\_image = cv2.convertScaleAbs(self.original\_image,
alpha=self.brightness\_scale.get())\
b, g, r = cv2.split(self.processing\_image)\
\
for b\_value in b:\
cv2.add(b\_value, self.b\_scale.get(), b\_value)\
for g\_value in g:\
cv2.add(g\_value, self.g\_scale.get(), g\_value)\
for r\_value in r:\
cv2.add(r\_value, self.r\_scale.get(), r\_value)\
\
self.processing\_image = cv2.merge((b, g, r))\
\
for key, value in self.morphologyDict.items():\
if value\[0\]:\
if value\[1\] is True:\
self.processing\_image = cv2.morphologyEx(self.processing\_image,
value\[2\], self.get\_kernel(key))\
else:\
value\[1\](event)\
self.show\_image(self.processing\_image)\
self.morphologyDict\["isGetApplied"\]\[0\] = True

Preview butonu tüm işlemlerimizi uygulayan yerdir. Öncelikle
brightness’ı alıp cv2.convertScaleAbs ile alpha değerini parlaklık
skalasında verilen değerle değiştiriyoruz. Sonra da resmimizin b,g,r
değerlerini alıp cv2.add ile ekleme işlemini yapıyoruz. Bu sayede
fotoğrafın piksel yoğunluklarını genel olarak değiştiriyoruz. Sonrasında
da bunları merge edip fotoğrafımıza atıyoruz.

Burada eminim ki aklımıza şu soru gelmiş durumdadır, peki neden bu tarz
bir paterni tercih ettim, neden doğrudan filtreye tıkladığında değil de
preview ile bu işlemi yapıyorum? Bunun birkaç sebebi var; filtrelenmiş,
morphologic değişikliklere uğramış fotoğrafın rgb değerleri oldukça
değişmiş olabiliyor bu sebeple onların rgb değerlerini değiştirmek
oldukça kötü görünen istemediğimiz sonuçlara sebep olabilir. Diğer bir
sebep ise her preview tuşuna bastığımızda tekrardan r,g,b ve brightness
değerlerinin tekrardan uygulanacak olması. Haliyle her değişiklikten
sonra preview a bastığınız da birbirinin üzerine eklenmiş olacaktı ve r
değerini arttırmışsak gitgide kıpkırmızı bir fotoğraf elde etmiş
olacaktık.

R,g,b değerlerini ekledikten sonra dict’deki değerlere bakıyoruz.

"isGetErosion": \[False, True, cv2.MORPH\_ERODE\],

Sözlükteki morphologic değerler bu şekilde ilerler Morphologic olmayan
durum belirten değerler ise bu şekilde ilerler.

"isGetHistogram": \[False, self.histogram\_button\_released\],

En baştaki false değeri, o işlemin yapılmasının istenip istenmediğini
belirtir, butona tıklama eventinizin yaptığı tek şey o False değeri True
yapmaktır. Asıl işlem previewde gerçekleştirilir. Ikinci değer
morphologic işlemlerde True değeridir, bunun sebebi preview da
cv2.morpEx fonksiyonunun kullanılacak olmasını belirtir. Morphologic
olmayan işlemlerde buradaki değer event fonksiyonunun işaretçisidir.
Morphologic işlemlerde 3. değer ise bu işlemi yaparken kullanacağımız
cv2’deki morphologic işlem yer alır. Morphologic olmayan işlemlerde ise
3. Değer yoktur. Rgb’nin nasıl yapılacağını anlatmıştık zaten,
Morphologic işlemler ise şu şekilde uygulanır:

for key, value in self.morphologyDict.items():\
if value\[0\]:\
if value\[1\] is True:\
self.processing\_image = cv2.morphologyEx(self.processing\_image,
value\[2\], self.get\_kernel(key))\
else:\
value\[1\](event)

Dict’in itemlerini for döngüsü ile alıyoruz, en baştaki değeri kontrol
ediyoruz ve bu işlemin yaplmasının istenip istenmediğini alıyoruz. Event
fonksiyonlarımız sadece o değeri değiştirmekle görevlidir, örneğin

def erosion\_button\_released(self, event):\
self.morphologyDict\["isGetErosion"\]\[0\] = True

Eğer butona tıklanmışsa ve değer True ise bu işlem yapılmalıdır, çünkü o
zaman o butona tıklanmış demektir. Eğer öyleyse de 2. Değerimiz olan o
işlemimizin bir morphologic işlem mi yoksa değil mi diye kontrol
ediyoruz. Eğer morphologic işlem ise cv2.morphologyEx ile işlemi
uyguluyoruz, parametre olarak dictimizdeki 3. Değeri yani yapılacak
morphology işleminin ifadesini yolluyoruz örneğin cv2.MORPH\_ERODE.
Kernel boyutu olarak da get\_kernel’e yolluyoruz. Sabit bir 0’larla
doldurulmuş bir kernel belirlemektense daha iyi sonuçlar almak ve
işlemin en doğrusunu yapmak için özel kerneller belirliyorum.
get\_kernel şu şekildedir.

def get\_kernel(self, morph\_name):\
kernel = None\
size = int(self.kernelSize\_scale.get())\
\
try:\
kernel =
cv2.getStructuringElement(shape=self.morphologyDict\[morph\_name\]\[2\],
ksize=(size, size))\
except cv2.error:\
kernel = cv2.getStructuringElement(shape=cv2.MORPH\_ELLIPSE,
ksize=(size, size))\
finally:\
return kernel

Burada ise kullanıcı’nın scaleden verdiği kernel boyutunu alıp try
içerisinde cv2.getStructingElement fonksiyonu ile kernelimizi
üretiyoruz. Kernel oluşturma yapımız dictdeki 3. Değerdir. Peki neden
Try içerisinde yapıyoruz? Çünkü structing element ismindende
anlaşılacağı gibi struct yapısına uygun morpholgyler’de element
oluşturur, örneğin cross, rect, ellipse. Diğer değerlerden birisini
yolladığımızda cv2 error alırız ve o hatayı da yakalayıp ellipse göre
element oluştururuz. Ellipse ile rect öyle sanıyorum ki renkli
fotoğraflarda daha iyi sonuçlar veriyor diye gözlemledim. Son olarak da
üretilen kerneli yolluyoruz. Şimdi preview kısmına geri dönelim:

else:\
value\[1\](event)\
self.show\_image(self.processing\_image)\
self.morphologyDict\["isGetApplied"\]\[0\] = True

Eğer morphologic bir işlem değilse ikinci değeri event fonksiyonunun
işaretçisidir. Öyleyse direkt olarak fonksiyona yollayıp işlemi
gerçekleştirmesini sağlayabiliriz. Bu fonksiyonlar da Histogram, log ve
power law transformationdır. En sonunda da fotoğrafı canvasda gösterip,
isgetApplied değerini True yapıp filtrelerin uygulandığını belirtiyoruz.
Eğer previewe tıklamadan applya tıklamış iseniz bu değer bizim işimize
yarayacaktır. İşlemler üzerine 3 tane örnek fotoğraf koyuyorum. Bundan
sonrasında Morphologic olmayan işlemleri açıklayacağım zaten morphologic
olanların nasıl yapıldığını bu kısımda açıkladım.

Brightness 1.4, kernel size 8 Gradient işlemi, 3.2 Gamma size Power-Law
işlemi:

![](media/image29.png){width="6.268055555555556in" height="3.075in"}

22 Red, -22 Green, 34 Blue, Kernel Size 55 Top Hat, Kernel 55 clip limit
2.0 Histogram işlemi:

![](media/image30.png){width="6.268055555555556in"
height="3.0694444444444446in"}

1.4 brightness, 10 kernel Black Hat, 10 kernel 15.0 clip limit
Histogram, Log trans. İşlemi:

![](media/image31.png){width="6.268055555555556in"
height="3.0652777777777778in"}

### APPLY

def apply\_button\_released(self, event):\
if not self.isGetApplied:\
self.preview\_button\_released(event)\
self.master.image\_cache.append(self.master.processed\_image.copy())\
self.master.processed\_image = self.processing\_image\
self.close(event)

Aplly button preview’a gidilmiş mi diye kontrol edip gidilmemişse oraya
göndererek uygulanması gereken işlemlerin tekrardan uygulanmasını
sağlar, sonrasında da cacheimize depolayıp, işlenmiş foroğrafımızı ana
fotoğrafımıza atıyoruz ve toplevelı kapatıyoruz.

### CANCEL

def cancel\_button\_released(self, event):\
self.close(event)

Burada da basitçe close ve cancel işlemleri görülmekte.

def close(self, event):\
self.show\_image()\
self.destroy()

### CLEAR

clear butonu ile de tüm değerlerimizi başlangıç stagelerine resetleyip.
Orijinal fotomuzu tekrardan işlenecek fotomuza veriyoruz ve canvasda o
fotoğrafı göstertiyoruz.

def clear\_button\_released(self, event):\
for values in self.morphologyDict.values():\
values\[0\] = False\
self.b\_scale.set(0)\
self.r\_scale.set(0)\
self.g\_scale.set(0)\
self.brightness\_scale.set(1.0)\
self.kernelSize\_scale.set(8)\
self.gammaSize\_scale.set(0.5)\
self.clipLimitSize\_scale.set(2.0)\
self.processing\_image = self.original\_image.copy()\
self.show\_image(self.processing\_image)

### Histogram Equalization

Histogram Eşitleme (HE), yoğunluk değerlerini yaymak için istatistiksel
bir yaklaşımdır. Görüntü işlemede HE, herhangi bir görüntünün
kontrastını iyileştirmek, yani karanlık kısmı daha koyu ve parlak kısmı
daha parlak hale getirmek için kullanılır.

Gray ölçekli bir görüntü için, her piksel yoğunluk değeri (parlaklık)
ile temsil edilir; bu yüzden piksel değerlerini doğrudan HE işlevine
besleyebiliriz. Ancak, RGB formatlı renkli bir görüntü için bu şekilde
çalışmaz. R, G ve B'nin her kanalı, bir bütün olarak görüntünün
yoğunluğunu/parlaklığını değil, ilgili rengin yoğunluğunu temsil eder.
Bu nedenle, HE'yi bu renk kanallarında çalıştırmak doğru yol değildir,
nitekim denediğimde de saçma sonuçlar ile karşılaştım. Burada yapmam
gereken ya fotoğrafımı gray ölçeğine çekecektim ki bu hiç istediğim bir
şey değildi, çünkü diğer tüm işlemlerde rgb ölçeğine göre işlem
yapıyordum ya da bu gray ölçeğini bir kenara itip rgb fotoğrafımın
parlaklık değerine ulaşacaktım, ben de ikinci yöntemle yapmayı tercih
ettim.

Önce görüntünün parlaklığını renkten ayırmalı ve ardından parlaklık
üzerinde HE çalıştırmalıyız. Şimdi, YCbCr, HSV, vb. gibi parlaklık ve
rengi ayrı ayrı kodlayan standartlaştırılmış renk uzayları zaten var; bu
yüzden onları burada parlaklığı ayırmak ve sonra yeniden birleştirmek
için kullanabiliriz.

def histogram\_button\_released(self, event):\
self.morphologyDict\["isGetHistogram"\]\[0\] = True\
ycrcb\_img = cv2.cvtColor(self.processing\_image, cv2.COLOR\_RGB2YCrCb)\
ycrcb\_img\[:, :, 0\] = cv2.equalizeHist(ycrcb\_img\[:, :, 0\])\
\
clahe =
cv2.createCLAHE(clipLimit=float(self.clipLimitSize\_scale.get()),\
tileGridSize=(int(self.kernelSize\_scale.get()),
int(self.kernelSize\_scale.get())))\
ycrcb\_img\[:, :, 0\] = clahe.apply(ycrcb\_img\[:, :, 0\])\
self.processing\_image = cv2.cvtColor(ycrcb\_img, cv2.COLOR\_YCrCb2RGB)

Gördüğünüz gibi burada YCbcr a dönüştürüp y kanalını yani parlaklık
kanalını cv2.equalizeHist fonksiyonuna yollayarak EH işlemini yapıyorum.
Aynı zamanda bu fonksiyondan çok daha iyi çalışan adaptif HE olarak
adlandırılan cv2.createCLAHE ve sonrasında da işlemi uygulamak için
apply fonksiyonuna da yolluyorum. Bu sayede hem bazı fotoğraflarda EH’ın
tuhaf çalışmalarının önüne geçiyorum hem de çok daha net bir şekilde
konstrant farkları oluşan görüntüler elde edebiliyorum. Aslında burada
sadece clahe kullanarak da işlemi yapabilirim ama test etmek isterseniz
diye diğer fonksiyonu da orada bırakıyorum. Clahenin değişkenleri olan
cliplimiti clip size scale’i ile, tileGridSize’i da kernel size scale’i
ile ayarlayabilirsiniz. Son olarak da tekrardan rgb’ye dönüştürüp
processing\_image’a atıyorum.

8 kernel size 5.0 Clip Limit size Histogram Eşitleme:

![](media/image32.png){width="6.268055555555556in"
height="3.011111111111111in"}

14 kernel size 15.0 clip limit size Histogram Eşitleme:

![](media/image33.png){width="6.268055555555556in"
height="3.0229166666666667in"}

1 kernel size, 2.0 clip limit size Histogram Eşitleme:

![](media/image34.png){width="6.268055555555556in"
height="3.0444444444444443in"}

### Log Transformation

Matematiksel olarak, log dönüşümleri s = clog(1+r) olarak ifade
edilebilir. Burada s çıkış yoğunluğu, r&gt;=0 pikselin giriş yoğunluğu
ve c bir ölçekleme sabitidir. c, 255/(log (1 + m)) ile verilir; burada
m, görüntüdeki maksimum piksel değeridir. Son piksel değerinin (L-1)
veya 255'i geçmemesi için yapılır. Pratik olarak, log dönüşümü, dar bir
düşük yoğunluklu giriş değerleri aralığını geniş bir çıkış değerleri
aralığına eşler.

def log\_button\_released(self, event):\
self.morphologyDict\["isGetLogged"\]\[0\] = True\
\
c = 255 / (np.log(1 + np.max(self.processing\_image)))\
log\_transformed = c \* np.log(1 + self.processing\_image)\
\
self.processing\_image = np.array(log\_transformed, dtype=np.uint8)

![](media/image35.png){width="6.268055555555556in"
height="3.5909722222222222in"}

### Power Law (Gamma) Transformation

Gama düzeltmesi, farklı ekran ayarlarına sahip farklı monitör
türlerinden bakıldığında görüntülerin beyazlaşmasını veya kararmasını
önlemek için görüntüleri bir ekranda doğru şekilde görüntülemek için
önemlidir. Bu transformation yapılır, çünkü gözlerimiz görüntüleri gama
şeklindeki bir eğride algılarken, kameralar görüntüleri doğrusal bir
şekilde yakalar. ![](media/image36.png){width="1.062749343832021in"
height="0.2310323709536308in"} matematiksel ifadesi bu şekilde olan
Power-Law ı kod düzlemine uyarlarsak;

def power\_law\_button\_released(self, event):\
self.morphologyDict\["isGetPowerLaw"\]\[0\] = True\
self.processing\_image = np.array(255 \* (self.processing\_image / 255)
\*\* float(self.gammaSize\_scale.get()),\
dtype='uint8')

1.7 Gamma Size Power-Law

![](media/image37.png){width="6.268055555555556in"
height="3.5881944444444445in"}

10.0 gamma size Power-Law

![](media/image38.png){width="6.268055555555556in"
height="3.546527777777778in"}

8) Canlı Video Üzerinden Şekil Tespiti
--------------------------------------

Benim Gerçekleştirdiğim video işleme task’ı canlı video üzerinden şekil
tespit etmek üzerinedir.

![](media/image39.png){width="3.2083333333333335in"
height="2.5729166666666665in"}İki tane threshold parametresi ve bir tane
area parametresi kullanıyorum. Area parametresi bulunacak olan alanların
min area boyutunu belirtir. Open Camera diyerek süreci
başlatabilirsiniz. Parametre değerlerini işlem başladıktan sonra da
anlık olarak değiştirebilirsiniz. Tespit ve görüntüler canvasda görülür.

### Open Camera

def start\_button\_released(self, event):\
self.video\_capture()

Open cameraya bastığınızda process başlar.

### Finish Process

def finish\_button\_released(self, event):\
self.master.interface\_functions.clear\_canvas()\
if self.master.processed\_image is not None:\
self.master.interface\_functions.show\_image()\
self.finished = True

En son göstrilen camera girdisini ekrandan temizler, eğer ana resmimiz,
video işlemeye girmeden önce seçilmişse, varsa o resim canvasa
götürülür. Ve local değişkenimiz True çekilip altta göreceğimiz döngünün
kırılması sağlanır.

def show\_image(self):\
self.master.interface\_functions.show\_image(image=self.images)

def close(self):\
self.cap.release()\
self.destroy()

### Video Capture

def video\_capture(self):\
self.cap = cv2.VideoCapture(0, cv2.CAP\_DSHOW)\
\
while True:\
self.update()\
if self.finished:\
self.close()\
break\
\
success, img = self.cap.read()\
imgContour = img.copy()\
imgBlur = cv2.GaussianBlur(img, (7, 7), 1)\
imgGray = cv2.cvtColor(imgBlur, cv2.COLOR\_BGR2GRAY)\
\
threshold1 = self.thresholdParam\_scale.get()\
threshold2 = self.thresholdParam2\_scale.get()\
imgCanny = cv2.Canny(imgGray, threshold1, threshold2)\
\
kernel = np.ones((5, 5))\
imgDil = cv2.dilate(imgCanny, kernel, iterations=1)\
\
self.getContours(imgDil, imgContour)\
\
self.images = stackImages(0.8, (\[img, imgGray, imgCanny\],\
\[imgDil, imgContour, imgContour\]))\
\
self.show\_image()\
self.master.update()

local değişkenimize video yakalama işlemini başlatıyoruz. Sonrasında da
while true içerisinde video framelerini okuyacağız. Öncelikle her döngü
başında self’i ve uptade ediyoruz ve self.finished değişkenimizi kontrol
ediyoruz. Yani finish processe basılıp basılmadığını kontrol ediyoruz
basılmışsa da hem döngüyü kırıyoruz hem de close’a yolluyoruz. Döngüyü
kırmamızın sebebi capture bırakılacağı için son döngüden hata almamak
içindir. Camerayı okuyup frame’i ve başarılı olup olmadığını alıyoruz.

Sonrasında da blur uygulayıp uyguladığımız resmin paletini graye
çekiyoruz. Scalelerimizden threshold parametrelerini alıp gray plate
aldığımız resme canny uyguyluyoruz, threshold parametreliyle beraber.
Kernel oluşturup cannylediğimiz fotoğrafa dilate işlemi uyguluyoruz
böylece fotoğrafımızın kenar hatlarını iyice belirginleştirmiş oluyoruz,
bundan sonraki tek ihtiyacımız kenarları cv2.findcontours ile bulup
gerekli çıktıları üretmek. Bu sebeple de getcontours fonksiyonuna
yolluyoruz. Ondan gelen çıktılarla birleştirilmiş resmi ve diğer process
işlemlerinde oluşturduğumuz (imgcanny, imgdil, imggray) gibi
resimlerimizi tek bir fotoğrafta birleştirip ekranda göstermek kalıyor.
Bunun için de stackimages fonksiyonumuza yolluyoruz ve resmi ekranda
gösterip master’ı uptade ediyoruz. Master’ı uptade etmemizin sebebi her
frame’de görüntüyü canvasda yenileyebilmek.

#### getContours

def getContours(self, img, imgContour):\
contours, hierarchy = cv2.findContours(img, cv2.RETR\_EXTERNAL,
cv2.CHAIN\_APPROX\_NONE)\
\# etrafta çok fazla öge varsa ve en çok alana sahip olanların
yakalanmasını istiyorsanız bu yorum satırını açın\
\#contours = sorted(contours, key=cv2.contourArea, reverse=True)\[:5\]\
for cnt in contours:\
area = cv2.contourArea(cnt)\
print(area)\
areaMin = self.areaParam\_scale.get()\
if area &gt; areaMin:\
cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)\
peri = cv2.arcLength(cnt, True)\
approx = cv2.approxPolyDP(cnt, 0.02 \* peri, True)\
print(len(approx))\
objCor = len(approx)\
x, y, w, h = cv2.boundingRect(approx)\
\
if objCor == 3:\
objectType = "Triangle"\
elif objCor == 4:\
aspRatio = w / float(h)\
if 0.98 &lt; aspRatio &lt; 1.03:\
objectType = "Square"\
else:\
objectType = "Rectangle"\
elif objCor &gt; 10:\
objectType = "Circles"\
else:\
objectType = "Polygon"\
\
cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)\
cv2.putText(imgContour, objectType,\
(x + w + 20, y + 20), cv2.FONT\_HERSHEY\_COMPLEX, 0.7,\
(0, 0, 0), 2)\
cv2.putText(imgContour, "Area: " + str(area),\
(x + w + 20, y + 45), cv2.FONT\_HERSHEY\_COMPLEX, 0.7,\
(0, 0, 0), 2)

cv2.Findcontours ile contourları buluyoruz. Contourları Türkçeye
eşyükselti eğrisi olarak çevirebiliriz. Metod parametresi olarak
denemelerimde en iyi çalışanlar external ve none parametreleri oldu, o
yüzden onları tercih ettim. Işık oranınıza ve arka planınıza göre Tree
ile TCos89 daha iyi çalışabilir. Bundan sonra da Contourları for döngüsü
içerisinde döndürüyoruz. Cv2. ContourArea’sı ile her bir contourun
areasını buluyoruz ve kullanıcın vermiş olduğu areadan büyük mü diye
kontrol ediyoruz. Sonrasında da cv2.drawContours ile contoursu
çizdiriyoruz, ben mavi renkde çizdirmeyi tercih ettim gözü daha az
yorması için, isterseniz onu değiştirebilirsiniz. cv2.arcLength(),
konturun çevresini hesaplamak için kullanılır. İkinci argüman True ise,
konturu kapalı olarak kabul eder. Daha sonra bu çevre, bir şekle
yaklaşmak için bir kesinlik faktörü ile cv2.approxPolyDP işlevi için
epsilon değerini hesaplamak için kullanılır. Dörtgeni yumuşatmak ve
yaklaşık olarak hesaplamak için cv2.approxPolyDP işlevini kullanıyorum.
cv2.approxPolyDP, konturlarda belge sınırı gibi keskin kenarların olduğu
durumlarda daha net çalışır. Daha net anlaşılması için cv2.approxPolyDP
nin arkasındaki algoritma olan Douglas-Peucker algoritmasına
bakılabilir.

Approx kenarları tutuğu için len fonksiyonu ile kenar sayısını alıyoruz.
Sonrasında approx’u cv2.boundingBox methodu ile çevresine bir bounding
box çizildeiğinde değerleri neler olacaktır onu alıyoruz. Kenar
sayılarından yola çıkarak object typeları veriyoruz. 10’dan fazla ise
circle olarak tanımlıyorum 4 ile 10 arasındakileri de polygon olarak
tanımlıyorum.

Artık son olarak rectangle yaratmak ve değerleri fotoğrafa eklemek
kalıyor. Cv2.Rectangle ile yukarıda boundingbox ile aldığımız değerlere
çizdiriyoruz. Rectangle bitişiğinin yanına da ObjectType’ı ve Area’ı
bastırıyorum.

#### stackImages

def stackImages(scale, imgArray):\
rows = len(imgArray)\
cols = len(imgArray\[0\])\
rowsAvailable = isinstance(imgArray\[0\], list)\
width = imgArray\[0\]\[0\].shape\[1\]\
height = imgArray\[0\]\[0\].shape\[0\]\
if rowsAvailable:\
for x in range(0, rows):\
for y in range(0, cols):\
if imgArray\[x\]\[y\].shape\[:2\] == imgArray\[0\]\[0\].shape\[:2\]:\
imgArray\[x\]\[y\] = cv2.resize(imgArray\[x\]\[y\], (0, 0), None, scale,
scale)\
else:\
imgArray\[x\]\[y\] = cv2.resize(imgArray\[x\]\[y\],
(imgArray\[0\]\[0\].shape\[1\], imgArray\[0\]\[0\].shape\[0\]),\
None, scale, scale)\
if len(imgArray\[x\]\[y\].shape) == 2: imgArray\[x\]\[y\] =
cv2.cvtColor(imgArray\[x\]\[y\], cv2.COLOR\_GRAY2BGR)\
imageBlank = np.zeros((height, width, 3), np.uint8)\
hor = \[imageBlank\] \* rows\
for x in range(0, rows):\
hor\[x\] = np.hstack(imgArray\[x\])\
ver = np.vstack(hor)\
else:\
for x in range(0, rows):\
if imgArray\[x\].shape\[:2\] == imgArray\[0\].shape\[:2\]:\
imgArray\[x\] = cv2.resize(imgArray\[x\], (0, 0), None, scale, scale)\
else:\
imgArray\[x\] = cv2.resize(imgArray\[x\], (imgArray\[0\].shape\[1\],
imgArray\[0\].shape\[0\]), None, scale,\
scale)\
if len(imgArray\[x\].shape) == 2: imgArray\[x\] =
cv2.cvtColor(imgArray\[x\], cv2.COLOR\_GRAY2BGR)\
ver = np.hstack(imgArray)\
return ver

StackImages herhangi bir class arttibute u kullanmadığı için onu static
bir fonksiyon olarak classın dışarısına tanımlıyorum. Bu fonksiyonda
yaptığımız işlem az önce yaptığımız video işlemlerini frame frame
birleştirmek ve bizde bu birleştirdiğimiz fotoğrafları canvasda
göstereceğiz. Burada yaptığımız şey fotoğrafları boyutlarına göre resize
etmek ve bir image arrayi oluşturup np.hstack ile birleştiriyoruz ve
return ediyoruz. Buranın ekran görüntüsünü haliyle kendi fotoğrafımı ve
odamı paylaşmamak için eklemiyorum program içerisinden deneyebilirsiniz.

9) Özdeğerlendirme Tablosu
--------------------------

![](media/image40.png){width="6.270833333333333in"
height="5.114583333333333in"}

10\) Ekstra Özellikler

Proje kapamında olmayan, uygulamayı güzelleştirmek için eklediğim
özellikleri bu başlık altında yer vereceğ

<span id="_Toc88790484" class="anchor"></span>Undo and Forward Özelliği

self.image\_cache = list()

Ana cacheimizi masterda tanımlıyoruz.

self.forward\_cache = list()

İki defa cache tanımlamak yerine localde bir cache tanımlıyorum. Daha
optimize olması için de her ikisi için fotoğraf yedeklemek yerine
birbiri arasında fotoğrafları döndürmeye çalışıyorum. Gördüğünüz gibi
poplar ile ve appendler ile resmi iki liste arasında geöiştiriyorum ve
ana resmimize atıyorum.

def undo\_image(self):\
if self.master.image\_cache:\
self.master.processed\_image = self.master.image\_cache.pop()\
self.forward\_cache.append(self.master.processed\_image)\
self.show\_image()\
\
def forward\_image(self):\
if self.forward\_cache:\
self.master.processed\_image = self.forward\_cache.pop()\
self.master.image\_cache.append(self.master.processed\_image)\
self.show\_image()

<span id="_Toc88790485" class="anchor"></span>Arka Plan Uygulama Müziği

Arka plan muziğini pygame module’si ile yapıyorum

self.mixer = mixer\
self.mixer.init()\
self.mixer.music.load("./Sample\_Images/Beethoven\_9.Senfoni.mp3")\
self.mixer.music.set\_volume(0.7)\
self.mixer.music.play(-1)

Scaleden değerleri alıp, değer değişikliği olduğunda da onu uyguluyorum.

self.music\_label = Label(self, text="Music Volume", bg='gray',
font="ariel 11 bold")\
self.music\_scale = Scale(self, from\_=0.0, to\_=1.0, length=100,
resolution=0.01,\
orient=HORIZONTAL)

Muziğin sesini kapatmak için 0 a çekin. Muzik beethoven’ın 9.
Senfonisidir.

def music\_volume(self, event):\
self.master.mixer.music.set\_volume(float(self.music\_scale.get()))

<span id="_Toc88790486" class="anchor"></span>Credit Top Leveli

#### Bu projeyi common licence olarak, githup’da paylaştığım için bana dair bilgileri credits page’de paylaşıyorum.

from tkinter import Toplevel, Canvas, Button, Label, NW\
from PIL import ImageTk\
import webbrowser\
\
\
def callback(url):\
webbrowser.open\_new(url)\
\
\
class CreditsTopLevel(Toplevel):\
def \_\_init\_\_(self, master=None):\
Toplevel.\_\_init\_\_(self, master=master, bg='gray', width=1380,
height=700)\
\
self.canvas = Canvas(self, bg="gray", width=560, height=350)\
self.canvas.place(x=10, y=280)\
\
self.img = ImageTk.PhotoImage(file="./Sample\_Images/LeftHand.png")\
self.canvas.create\_image(0, 40, anchor=NW, image=self.img)\
\
self.canvas2 = Canvas(self, bg="gray", width=560, height=350)\
self.canvas2.place(x=800, y=280)\
\
self.img2 = ImageTk.PhotoImage(file="./Sample\_Images/RightHand.png")\
self.canvas2.create\_image(70, 40, anchor=NW, image=self.img2)\
\
self.general\_page = Label(master=self, text="This project offers an
application infrastructure"\
" that allows you to edit photos.\\n"\
"You can learn more about the project and where in the code"\
" does what by reading the Read.me file.\\nRead.me file is in"\
" Turkish, you can translate it to English if you want,\\n"\
" Google translate translates the sentences correctly.\\n"\
" This code tells you how to manipulate form files in general"\
" terms,\\nhow to create form applications in oop structure,\\n"\
" how to make edits on the photos and how to transfer these"\
" arrangements to canvas.\\n You can learn how to use form files via"\
" python and image editing steps in python using this project.\\n"\
"\\nCreating by Daymenion\\n",\
bg="gray", fg="black", font="ariel 15 bold")\
self.instagram\_page = Label(master=self, text="My Instagram Page",
bg="gray", fg="blue",\
font="ariel 15 bold", cursor="hand2")\
self.twitter\_page = Label(master=self, text="My Twitter Page",
bg="gray", fg="blue",\
font="ariel 15 bold", cursor="hand2")\
self.githup\_page = Label(master=self, text="My Githup Page", bg="gray",
fg="blue",\
font="ariel 15 bold", cursor="hand2")\
self.youtube\_page = Label(master=self, text="My Youtube Page",
bg="gray", fg="blue",\
font="ariel 15 bold", cursor="hand2")\
self.linkedin\_page = Label(master=self, text="My Linkedin Page",
bg="gray", fg="blue",\
font="ariel 15 bold", cursor="hand2")\
self.twitch\_page = Label(master=self, text="My Twitch Page", bg="gray",
fg="blue",\
font="ariel 15 bold", cursor="hand2")\
self.discord\_page = Label(master=self, text="My Discord Channel",
bg="gray", fg="blue",\
font="ariel 15 bold", cursor="hand2")\
self.exit\_button = Button(self, text="Exit Credits Page", bg="black",
fg='white', width=15, font="ariel 13 bold")\
\
self.twitch\_page.bind("&lt;Button-1&gt;", lambda e:
callback("https://www.twitch.tv/daymenion"))\
self.discord\_page.bind("&lt;Button-1&gt;", lambda e:
callback("https://discord.com/invite/XZjnjZHJCB"))\
self.linkedin\_page.bind("&lt;Button-1&gt;", lambda e:
callback("https://www.linkedin.com/in/daymenion/"))\
self.githup\_page.bind("&lt;Button-1&gt;", lambda e:
callback("https://github.com/Daymenion"))\
self.instagram\_page.bind("&lt;Button-1&gt;", lambda e:
callback("https://www.instagram.com/daymenion/"))\
self.youtube\_page.bind("&lt;Button-1&gt;", lambda e:
callback("https://www.youtube.com/c/Daymenion"))\
self.twitter\_page.bind("&lt;Button-1&gt;", lambda e:
callback("https://twitter.com/Daymenion"))\
self.exit\_button.bind("&lt;ButtonRelease&gt;",
self.exit\_button\_released)\
\
self.general\_page.place(x=250, y=0)\
self.githup\_page.place(x=600, y=260)\
self.youtube\_page.place(x=600, y=320)\
self.instagram\_page.place(x=600, y=380)\
self.twitter\_page.place(x=600, y=440)\
self.twitch\_page.place(x=600, y=500)\
self.linkedin\_page.place(x=600, y=560)\
self.discord\_page.place(x=600, y=620)\
self.exit\_button.place(x=600, y=650)\
\
self.mainloop(3)\
\
def exit\_button\_released(self, event):\
self.destroy()

<span id="_Toc88790487" class="anchor"></span>İncrease Contrast

Basitçe konstrat arttırma işlemi, kayda değer pek bir şey yok bunun
özelinde.

def contrast(self):\
self.master.image\_cache.append(self.master.processed\_image.copy())\
contrast =
(ImageEnhance.Contrast(Image.fromarray(self.master.processed\_image))).enhance(1.1)\
self.master.processed\_image = np.array(contrast)\
self.master.image\_cache.append(self.master.processed\_image.copy())\
self.show\_image()
