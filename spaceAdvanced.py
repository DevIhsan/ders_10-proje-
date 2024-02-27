from turtle import *
from random import randint # random integer
import time
import winsound
from mlnumbers import classifyNumbers, storeNumbers
from mlmodel import trainModel

API_KEY = "652f1e80-c526-11ee-8583-b325169fb6da3a8047c7-59d7-4c79-84a4-3d4a873872e1"
trainModel(API_KEY)
# pencere kodları
wn = Screen()
wn.title("Space Game") # string tipi
wn.bgpic("bg2.gif")
wn.setup(768, 768) # genişlik ve yükseklik

for i in range(1,4): # 1 dahil ancak 4 dahil değildir
    wn.addshape("spaceship" + str(i) + ".gif")

for i in range(1,9):
    wn.addshape("enemy" + str(i) + ".gif")

for i in range(1, 7):
    wn.addshape("missile" + str(i) + ".gif")

for i in range(1, 12):
    wn.addshape("bullet" + str(i) + ".gif")
    
for i in range(1, 7):
    wn.addshape("ex" + str(i) + ".gif")

player = Turtle() # PARANTEZE DİKKAT !!!
player.shape("spaceship3.gif")
player.speed(5)
player.up() # çizim yapmıyoruz
player.goto(0, -150)
player.live = 5



missile = Turtle() # PARANTEZE DİKKAT !!!
missile.shape("missile1.gif")
missile.up()
missile.ht() # hideturtle gizle bloğu
missile.speed(0) # fastest
missile.shapesize(5)
missile.is_active = False

bullet = missile.clone() # atama yapıyoruz değişkeni 0 yap bloğu
bullet.shape("bullet1.gif")
bullet.seth(270) # 0 sağ taraf 90 yukarı  180 sol taraf 270 aşağı taraf
bullet.speed(5)
bullet.is_active = False # bullet pencereden çıkınca oyuncumuzu vurmaması için bu değişken eklendi

yaz = Turtle() # PARANTEZE DİKKAT !!!
yaz.speed(0)
yaz.up()
yaz.goto(0, 300)
yaz.ht()
yaz.color("dark blue")

brightness = Turtle() # parlaklık kuklası tanımladık PARANTEZE DİKKAT !!!
brightness.color("white")
brightness.shape("circle")
brightness.ht()
brightness.is_active = True

explosion = Turtle() # parlaklık kuklası tanımladık PARANTEZE DİKKAT !!!
explosion.shape("ex1.gif")
explosion.ht() 
explosion.is_active = False

puan = 0
game_over = False  # F HARFİ BÜYÜK DİKKAT !!!

hedefler = [] # liste oluşturduk

for i in range(1):
    hedefler.append(Turtle()) # bir listeye elemanları append metodu ile ekliyoruz !!!
    
for hedef in hedefler: # PARANTEZ YOK !!!!!
    hedef.speed(0)
    hedef.shape("enemy" + str(randint(1,8)) + ".gif")
    hedef.up()
    hedef.goto(randint(-350, 350), randint(350, 500)) # yatayda ve dikeyde rastgele konuma git.


mod = "train"

    
# function definition  -> fonksiyon tanımlamak
def move_player(x, y): # oyuncumuzun hareket fonksiyonunu tanımladık
    player.goto(x, y)
    
def missile_setup():
    winsound.PlaySound("laser1.wav", winsound.SND_ASYNC) # P ve S harflari BÜYÜK
    missile.showturtle()
    missile.shape("missile" + str(randint(1,6)) + ".gif")
    missile.goto(player.pos()) # position of player pos() PARANTEZE DİKKAT !!!
    missile.is_active = True # missile atıldığında bu değişken False yapılacak ve her defasında tek missile atılacak
    
def missile_move():  # func definiton
    y = missile.ycor()  # y koor bilgisini al
    y = y + 20  # y += 20 aynı anlamdadır
    missile.sety(y) # y konumunu set et
    
def patlama(missile): # Patlama efekti veriliyor. Hangi missile patlıyor ise orada patlama efekti oluşuyor.
    brightness.up()
    brightness.speed(0)
    brightness.goto(missile.pos()) # brightness kuklası missile konumuna git diyoruz.
    brightness.showturtle()
        
    for i in range(10):
        brightness.turtlesize(10-i, 10-i) # i her döngüde artıyor bu yüzden 10-i ise azalıyor.
        
    brightness.ht()
     
def explode(missile): # Patlama efekti veriliyor. Hangi missile patlıyor ise orada patlama efekti oluşuyor.
    explosion.up()
    explosion.speed(0)
    explosion.goto(missile.pos()) # brightness kuklası missile konumuna git diyoruz.
    explosion.showturtle()
        
    for i in range(1,7):
        time.sleep(0.1)
        explosion.shape("ex" + str(i) + ".gif") # i her döngüde artıyor bu yüzden 10-i ise azalıyor.
        
    explosion.ht()
# patlama func definition işlemi bu satırda bitmiştir.
    

def train(decision):
        training_data = [hedef.xcor(),hedef.ycor(),hedefler[0].xcor(),hedefler[0].ycor()]

        training_label = decision

        storeNumbers(API_KEY, training_data, training_label)

def play_AI():
        data = [hedef.xcor(),hedef.ycor(),hedefler[0].xcor(),hedefler[0].ycor()]
        result = classifyNumbers(API_KEY, data)

        print(result)

        if result['hedefler'] == "hedefler":
            player.goto(hedefler.xcor()+10, hedefler.ycor())
        elif result['hedefler']  == "hedefler": 
            player.goto(hedefler.xcor()-10, hedefler.ycor())
        #elif result['class_name']  == "up": self.ticaret_yap()
        #elif result['class_name']  == "down": self.savas_karari()  

def left():
    player.goto(hedef.xcor())
    player.setx(player.xcor()-10)
    train("player_y")

def right():
    player.goto(hedef.xcor())
    player.setx(player.xcor()+10)
    train("player_x")    
                

    
wn.listen()
wn.onscreenclick(move_player) # ekrana tıklandığında move_player func çağırılıyor ---------func call---- 
wn.onkey(missile_setup, 'space') # klavye tuşumuzun ismini string olarak yazıyoruz
wn.onkey(lambda: player.setx(player.xcor()+10), 'Right') # klavye tuşumuzun ismini string olarak yazıyoruz
wn.onkey(left, "Left") # klavye tuşumuzun ismini string olarak yazıyoruz
time.sleep(1) # oyunun biraz gecikmesi sağlanıyor

# oyunumuzun ana çatısı---------------------------------------------------------------------------------- 
while True: # forever
    for hedef in hedefler: 
        y = hedef.ycor() # hedefin y koor bilgisini alır
        y = y - 5        # y -= 5 aynı anlamda
        hedef.sety(y)    # y konumunu güncelle
        # bullet kodları 
        bullet.fd(10) # düşman aracının ateşi bize doğru ilerliyor.
        
        if missile.is_active:
            missile_move() # func call
        
        if hedef.distance(missile) < 60: # hedefi vurma koşulu
            winsound.PlaySound("patlama.wav", winsound.SND_ASYNC)
            
            missile.ht()
            # patlama(missile) # Hangi missile patlıyor ise bu fonksiyona o missile kuklasını gönderiyoruz ---func call---
            explode(missile)
            
            missile.goto(player.pos())
            missile.is_active = False # missile hareketini engelliyoruz
            
            hedef.ht() # hangi hedef? vurulan hedefi gizliyoruz
            hedef.sety(400)
            hedef.showturtle() # PARANTEZ VAR !!!!
            
            puan += 10 # int tipindedir
            
            yaz.clear()
            yaz.color("spring green") # kalem rengini değiştirdik
            yaz.write("PUAN = " + str(puan), align = 'center', font = ('Courier', 24, 'bold'))
        #  hedefi vurma koşulu bu satırda bitti
        
        # eğer bullet oyuncumuza 50 px'den daha yakınsa VE bullet aktif ise ancak oyuncumuzu vurabiliyor 
        if bullet.distance(player) < 50 and bullet.is_active: # oyuncumuzun vurulma koşulu, and operatörüne dikkat !!!
            player.live -= 1
            bullet.is_active = False # aynı bullet sadece 1 defa oyuncumuzu vurabilsin daha sonra pasif olsun
            yaz.clear()
            yaz.color("red")
            yaz.write('live = '+ str(player.live), align='center', font=('Courier', 24, 'bold'))
        # oyuncumuzun vurulma koşulu  bu satırda bitti  
        
        if (hedef.distance(player) < 20) or (player.live == 0): # or (ya da) kullanarak iki koşulu tek satırda yazabildik !!!
            game_over = True
            break # ilk gördüğü döngü for olduğu için for döngüsünü kırar
            
    # !!! bu satırda for hedef in hedefler: satırındaki for döngüsü bitti ve while True döngüsünün gövdesine geçildi.              
    if puan == 100:
        yaz.clear()
        yaz.color("spring green")
        yaz.write('You win!', align='center', font=('Courier', 24, 'bold'))
        break # ilk gördüğü döngüyü bitirir while True biter.
        
    if game_over: # eğer game over True olursa 
        yaz.clear()
        yaz.color("red")
        yaz.write('Game Over! You Lost', align='center', font=('Courier', 24, 'bold'))
        break # while döngüsü kırılır
    
    # eğer bullet ekranın altından daha aşağı bir konuma gelirse yer değiştiriyor
    if bullet.ycor() < -350:
        bullet.ht()
        bullet.is_active = False # bullet pasif 
        bullet.goto(hedefler[0].pos()) # rastgele bir hedefi seç ve onun konumuna git
        bullet.is_active = True # bullet aktif
        bullet.showturtle()
# while True döngüsü bitti ------------------------------------------------------------------  

winsound.PlaySound('oyunbitti.wav', winsound.SND_ASYNC)
wn.onscreenclick(None) # ekrana tıklama olayını iptal ediyoruz  None = hiç bir şey anlamındadır

for hedef in hedefler: # hedeflerin hepsini gizliyoruz
    hedef.ht()  

# en son kısma yazıyoruz    
wn.mainloop()