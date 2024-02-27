import tkinter as tk
from PIL import Image, ImageTk
import random

from mlnumbers import classifyNumbers, storeNumbers
from mlmodel import trainModel


API_KEY = settings.API_KEY

# oyun her çalıştırıldığında modelimiz tekrar eğitilir
trainModel(API_KEY)

FONT = ("Arial", 14)

class ConquerAIOyunu:
    def __init__(self, window):
        self.window = window
        self.window.title("conquerAI Oyunu")
        self.window.geometry("1350x700")
        self.window.config(bg="#FE938C")
        
        self.training = True

        self.karakter = 1
        self.av = 100
        self.maden = 100
        self.ticaret = 100
        self.savas = 100

        # Seçenek menüsü ile karakter seçimi
        self.karakter_secim = tk.StringVar()
        self.karakter_secim.set("1. Saldırgan")  # Varsayılan olarak Saldırgan karakteri seçili
        self.karakter_menu = tk.OptionMenu(self.window, self.karakter_secim, "1. Saldırgan", "2. Diplomatik", "3. Ekonomik")
        tk.Label(self.window, text="Karakter Seçimi: ", bg="#FFECD6", font=FONT).grid(row=0, column=4,)
        self.karakter_menu.grid(row=0, column=5)

        # Mod seçimi için radyo düğmeleri
        self.mod_secim = tk.StringVar()
        self.mod_secim.set("Train Mode")  # Varsayılan olarak Train Modu seçili
        tk.Radiobutton(self.window, text="Train Mode", variable=self.mod_secim, value="Train Mode", font=FONT).grid(row=1, column=4, padx=5)
        tk.Radiobutton(self.window, text="Play Mode", variable=self.mod_secim, value="Play Mode", font=FONT).grid(row=1, column=5, padx=5)

        # AI oyun modu için buton eklenmesi
        tk.Button(self.window, text="AI PLAY", font=FONT, command=self.play_AI).place(x=1150, y=180)

        # Üst bölümdeki kullanıcı seviyelerini gösteren etiketler
        self.avlan_etiket = tk.Label(self.window, text="Avlanma Seviyesi: 100", font=FONT)
        self.avlan_etiket.grid(row=0, column=0, padx=50)

        self.maden_etiket = tk.Label(self.window, text="Maden Seviyesi: 100", font=FONT)
        self.maden_etiket.grid(row=1, column=0, padx=50)

        self.ticaret_etiket = tk.Label(self.window, text="Ticaret Seviyesi: 100", font=FONT)
        self.ticaret_etiket.grid(row=0, column=2, padx=50)

        self.savas_etiket = tk.Label(self.window, text="Savaş Seviyesi: 100", font=FONT)
        self.savas_etiket.grid(row=1, column=2, padx=50)

        self.av_image = Image.open(r"assets\av_seviyesi.png").resize((100, 100))
        self.av_photo = ImageTk.PhotoImage(self.av_image)
        self.avlan_img_etiket = tk.Label(self.window, image=self.av_photo)
        self.avlan_img_etiket.grid(row=0, column=1)
        
        self.maden_image = Image.open("assets\maden_seviyesi.png").resize((100, 100))
        self.maden_photo = ImageTk.PhotoImage(self.maden_image)
        self.maden_img_etiket  = tk.Label(self.window, image=self.maden_photo)
        self.maden_img_etiket.grid(row=1, column=1)

        self.ticaret_image = Image.open(r"assets\ticaret_seviyesi.png").resize((100, 100))
        self.ticaret_photo = ImageTk.PhotoImage(self.ticaret_image)
        self.ticaret_img_etiket = tk.Label(self.window, image=self.ticaret_photo)
        self.ticaret_img_etiket.grid(row=0, column=3)

        self.savas_image = Image.open("assets\savas_seviyesi.png").resize((100, 100))
        self.savas_photo = ImageTk.PhotoImage(self.savas_image)
        self.savas_img_etiket = tk.Label(self.window, image=self.savas_photo)
        self.savas_img_etiket.grid(row=1, column=3)


        # Orta bölümdeki butonlar ve resimler
        self.avlan_img = Image.open(r"assets\avlan.png").resize((200, 200))
        self.avlan_photo = ImageTk.PhotoImage(self.avlan_img)
        self.avlan_buton = tk.Button(self.window, image=self.avlan_photo, command=self.avlan)
        self.avlan_buton.grid(row=2, column=0, padx=10, pady=20)
        self.avlan_text = tk.Label(self.window, text="AVLAN", font=FONT).grid(row=3, column=0, padx=10)

        self.maden_img = Image.open("assets\maden_islet.png").resize((200, 200))
        self.maden_islet_photo = ImageTk.PhotoImage(self.maden_img)
        self.maden_islet_buton = tk.Button(self.window,  image=self.maden_islet_photo, command=self.maden_islet)
        self.maden_islet_buton.grid(row=2, column=1, padx=10, pady=20)
        self.maden_text = tk.Label(self.window, text="MADEN İŞLET", font=FONT).grid(row=3, column=1, padx=10)

        self.ticaret_yap_img = Image.open(r"assets\ticaret_yap.png").resize((200, 200))
        self.ticaret_yap_photo = ImageTk.PhotoImage(self.ticaret_yap_img)
        self.ticaret_yap_buton = tk.Button(self.window, image=self.ticaret_yap_photo, command=self.ticaret_yap)
        self.ticaret_yap_buton.grid(row=2, column=2, padx=10, pady=20)
        self.ticaret_text = tk.Label(self.window, text="TİCARET YAP", font=FONT).grid(row=3, column=2, padx=10)


        self.savas_karari_img = Image.open("assets\savas_karari.png").resize((200, 200))
        self.savas_karari_photo = ImageTk.PhotoImage(self.savas_karari_img)
        self.savas_karari_buton = tk.Button(self.window, image=self.savas_karari_photo, command=self.savas_karari)
        self.savas_karari_buton.grid(row=2, column=3, padx=10, pady=20)
        self.savas_text = tk.Label(self.window, text="SAVAŞ YAP", font=FONT).grid(row=3, column=3, padx=10)

        #ekstra buton
        self.insa_et_img = Image.open("assets\ev_insaat_img.png").resize((200, 200))
        self.insa_et_photo = ImageTk.PhotoImage(self.insa_et_img)
        self.insa_et_buton = tk.Button(self.window, image=self.insa_et_photo, command=self.insa_et)
        self.insa_et_buton.grid(row=2, column=4, padx=10, pady=20)
        self.insa_text = tk.Label(self.window, text="INSA ET", font=FONT).grid(row=3, column=4, padx=10)


        # Alt bölümde karar sonuçları gösteren etiket
        self.sonuc_etiket = tk.Label(self.window, text="DURUM : ", font=FONT)
        self.sonuc_etiket.grid(row=4, column=0, columnspan=4, pady=30)

    def avlan(self):
        if self.mod_secim.get() == "Train Mode" : self.train("avlan")
        print(self.mod_secim.get())
        # Avlanma işlemi
        if random.randint(0,1) == 1:
            basari = random.randint(1, 10)
            self.sonuc_etiket.config(text=f"Av Başarılı. Başarı : +{basari}")
        else:
            basari = random.randint(-10,-1)
            self.sonuc_etiket.config(text=f"Av Başarısız Kayıp : {basari}")

        self.av += basari
        self.avlan_etiket.configure(text = f"Avlanma Seviyesi: {self.av}")
        
    def maden_islet(self):
        if self.mod_secim.get() == "Train Mode" : self.train("maden_islet")

        # Maden işletme işlemi
        if random.randint(0,1) == 1:
            basari = random.randint(1, 10)
            self.sonuc_etiket.config(text=f"Maden İşletme Başarılı. Başarı : +{basari}")
        else:
            basari = random.randint(-10,-1)
            self.sonuc_etiket.config(text=f"Maden İşletme Başarısız Kayıp : {basari}")

        self.maden += basari
        self.maden_etiket.configure(text = f"Maden Seviyesi: {self.maden}")
        

    def ticaret_yap(self):
        if self.mod_secim.get() == "Train Mode": self.train("ticaret_yap")
        # Ticaret yap işlemi
        if random.randint(0,1) == 1:
            basari = random.randint(1, 10)
            self.sonuc_etiket.config(text=f"Ticaret Başarılı. Başarı : +{basari}")
        else:
            basari = random.randint(-10,-1)
            self.sonuc_etiket.config(text=f"Ticaret Başarısız Kayıp : {basari}")

        self.ticaret += basari
        self.ticaret_etiket.configure(text = f"Ticaret Seviyesi: {self.ticaret}")

    def savas_karari(self):
        if self.mod_secim.get() == "Train Mode": self.train("savas_karari")
        # Savaş kararı işlemi
        if random.randint(0,1) == 1:
            basari = random.randint(1, 10)
            self.sonuc_etiket.config(text=f"Savaş Başarılı. Başarı : +{basari}")
        else:
            basari = random.randint(-10,-1)
            self.sonuc_etiket.config(text=f"Savaş Başarısız Kayıp : {basari}")

        self.savas += basari
        self.savas_etiket.configure(text = f"Savas Seviyesi: {self.savas}")



    def insa_et(self):
        if self.mod_secim.get() == "Train Mode": self.train("insa_et")
        # Insaat kararı işlemi
        if random.randint(0,1) == 1:
            basari = random.randint(1, 10)
            self.sonuc_etiket.config(text=f"Insaat Başarılı. Başarı : +{basari}")
        else:
            basari = random.randint(-10,-1)
            self.sonuc_etiket.config(text=f"Insaat Başarısız. Kayıp : {basari}")

        self.ticaret += basari
        self.ticaret_etiket.configure(text = f"Insaat Seviyesi: {self.ticaret}")


    def train(self, decision):
        training_data = [self.karakter_sec(), self.av, self.maden, self.ticaret, self.savas,]

        training_label = decision

        storeNumbers(API_KEY, training_data, training_label)

    def play_AI(self):
        data = [self.karakter_sec(), self.av, self.maden, self.ticaret, self.savas ]
        result = classifyNumbers(API_KEY, data)

        print(result)

        if result['class_name'] == "avlan": self.avlan()
        elif result['class_name']  == "maden_islet": self.maden_islet()
        elif result['class_name']  == "ticaret_yap": self.ticaret_yap()
        elif result['class_name']  == "savas_karari": self.savas_karari()
        elif result['class_name']  == "insaat": self.insa_et()

    def karakter_sec(self):
        print(self.mod_secim.get())
        return int(self.karakter_secim.get()[0]) # saldırgan 1, diplomatik 2, ekonomik 3


if __name__ == "__main__":
    root = tk.Tk()
    oyun = ConquerAIOyunu(root)
    root.mainloop()