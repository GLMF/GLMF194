#!/usr/bin/python3

from qrcorps import *

# Masque pour coder et décoder les zones de format

masquef=[int(i) for i in "101010000010010"]

# Calcul du reste de la zone de format

def resteformat(n):
  mod=16*1335 # 0x357
  n*=1024
  for i in range(5):
    if len(bin(n))>=len(bin(mod)):
      n^=mod
    mod//=2
  return n

# Les quatre niveaux de correction Low, Medium, Quality, High

niveaucorrection={(0,1):"L",(0,0):"M",(1,1):"Q",(1,0):"H"}
correctionniveau={v:c for c,v in niveaucorrection.items()}
nomnivcor={"L":"Low","M":"Medium","Q":"Quality","H":"High"}

# Les huit masques pour le message

masques={(0,0,0):lambda i,j:(i+j)%2==0,
         (0,0,1):lambda i,j:i%2==0,
         (0,1,0):lambda i,j:j%3==0,
         (0,1,1):lambda i,j:(i+j)%3==0,
         (1,0,0):lambda i,j:(i//2+j//3)%2==0,
         (1,0,1):lambda i,j:(i*j)%2==0 and (i*j)%3==0,
         (1,1,0):lambda i,j:((i*j)%3+i*j)%2==0,
         (1,1,1):lambda i,j:((i*j)%3+i+j)%2==0
         }

# Une grande cible

cible=[[1,0,1,1,1,0,1] for _ in range(7)]
cible[1][2:5]=[0]*3
cible[5][2:5]=[0]*3
cible[0]=[1]*7
cible[6]=[1]*7

# Une minicible

minicible=[[1,0,1,0,1] for _ in range(5)]
minicible[1][2]=0
minicible[3][2]=0
minicible[0]=[1]*5
minicible[4]=[1]*5

# Les coordonnées des centres des minicibles en fonction de la version

minicibles={1:[],
            2:[18],3:[22],4:[26],5:[30],6:[34],
            7:[6,22,38],8:[6,24,42],9:[6,26,46],10:[6,28,50],11:[6,30,54],12:[6,32,58],13:[6,34,62],
            14:[6,26,46,66],15:[6,26,48,70],16:[6,26,50,74],17:[6,30,54,78],18:[6,30,56,82],19:[6,30,58,86],20:[6,34,62,90],
            21:[6,28,50,72,94],22:[6,26,50,74,98],23:[6,30,54,78,102],24:[6,28,54,80,106],25:[6,32,58,84,110],26:[6,30,58,86,114],
            27:[6,34,62,90,118],28:[6,26,50,74,98,122],29:[6,30,54,78,102,126],30:[6,26,52,78,104,130],31:[6,30,56,82,108,134],
            32:[6,34,60,86,112,138],33:[6,30,58,86,114,142],34:[6,34,62,90,118,146],35:[6,30,54,78,102,126,150],36:[6,24,50,76,102,128,154],
            37:[6,28,54,80,106,132,158],38:[6,32,58,84,110,136,162],39:[6,26,54,82,110,138,166],40:[6,30,58,86,114,142,170]
            }

# La fonction qui retourne la zone grisée

def griser(dimension,version):
  tablegris=[[False for _ in range(9)]+[True for _ in range(dimension-17)]+[False for _ in range(8)] for _ in range(6)] # True si on décode avec masque, False sinon
  tablegris=tablegris+[[False for _ in range(dimension)]] # et pas [[False]*dim], gare aux copies par référence pour la suite
  tablegris=tablegris+[[False for _ in range(9)]+[True for _ in range(dimension-17)]+[False for _ in range(8)] for _ in range(2)]
  tablegris=tablegris+[[True for _ in range(6)]+[False]+[True for _ in range(dimension-7)] for _ in range(dimension-17)]
  tablegris=tablegris+[[False for _ in range(9)]+[True for _ in range(dimension-9)] for _ in range(8)]

  for ci in minicibles[version]: # minicibles est dans qrcodestandard
    for cj in minicibles[version]:
      if (ci,cj) not in {(6,6),(6,max(minicibles[version])),(max(minicibles[version]),6)}:
        for i in range(ci-2,ci+3):
          tablegris[i][cj-2:cj+3]=[False]*5

  if version>=7:
    for i in range(6):
      tablegris[i][-11:-8]=[False]*3
    for i in range(3):
      tablegris[-11+i][0:6]=[False]*6

  return tablegris

# Tableau des panachages des données selon les versions des QR codes

tableau={1:{"L":"(26,19)","M":"(26,16)","Q":"(26,13)","H":"(26,9)"},
         2:{"L":"(44,34)","M":"(44,28)","Q":"(44,22)","H":"(44,16)"},
         3:{"L":"(70,55)","M":"(70,44)","Q":"2×(35,17)","H":"2×(35,13)"},
         4:{"L":"(100,80)","M":"2×(50,32)","Q":"2×(50,24)","H":"4×(25,9)"},
         5:{"L":"(134,108)","M":"2×(67,43)","Q":"2×(33,15),2×(34,16)","H":"2×(33,11),2×(34,12)"},
         6:{"L":"2×(86,68)","M":"4×(43,27)","Q":"4×(43,19)","H":"4×(43,15)"},
         7:{"L":"2×(98,78)","M":"4×(49,31)","Q":"2×(32,14),4×(33,15)","H":"4×(39,13),(40,14)"},
         8:{"L":"2×(121,97)","M":"2×(60,38),2×(61,39)","Q":"4×(40,18),2×(41,19)","H":"4×(40,14),2×(41,15)"},
         9:{"L":"2×(146,116)","M":"3×(58,36),2×(59,37)","Q":"4×(36,16),4×(37,17)","H":"4×(36,12),4×(37,13)"},
         10:{"L":"2×(86,68),2×(87,69)","M":"4×(69,43),(70,44)","Q":"6×(43,19),2×(44,20)","H":"6×(43,15),2×(44,16)"},
         11:{"L":"4×(101,81)","M":"(80,50),4×(81,51)","Q":"4×(50,22),4×(51,23)","H":"3×(36,12),8×(37,13)"},
         12:{"L":"2×(116,92),2×(117,93)","M":"6×(58,36),2×(59,37)","Q":"4×(46,20),6×(47,21)","H":"7×(42,14),4×(43,15)"},
         13:{"L":"4×(133,107)","M":"8×(59,37),(60,38)","Q":"8×(44,20),4×(45,21)","H":"12×(33,11),4×(34,12)"},
         14:{"L":"3×(145,115),(146,116)","M":"4×(64,40),5×(65,41)","Q":"11×(36,16),5×(37,17)","H":"11×(36,12),5×(37,13)"},
         15:{"L":"5×(109,87),(110,88)","M":"5×(65,41),5×(66,42)","Q":"5×(54,24),7×(55,25)","H":"11×(36,12),7×(37,13)"},
         16:{"L":"5×(122,98),(123,99)","M":"7×(73,45),3×(74,46)","Q":"15×(43,19),2×(44,20)","H":"3×(45,15),13×(46,16)"},
         17:{"L":"(135,107),5×(136,108)","M":"10×(74,46),(75,47)","Q":"(50,22),15×(51,23)","H":"2×(42,14),17×(43,15)"},
         18:{"L":"5×(150,120),(151,121)","M":"9×(69,43),4×(70,44)","Q":"17×(50,22),(51,23)","H":"2×(42,14),19×(43,15)"},
         19:{"L":"3×(141,113),4×(142,114)","M":"3×(70,44),11×(71,45)","Q":"17×(47,21),4×(48,22)","H":"9×(39,13),16×(40,14)"},
         20:{"L":"3×(135,107),5×(136,108)","M":"3×(67,41),13×(68,42)","Q":"15×(54,24),5×(55,25)","H":"15×(43,15),10×(44,16)"},
         21:{"L":"4×(144,116),4×(145,117)","M":"17×(68,42)","Q":"17×(50,22),6×(51,23)","H":"19×(46,16),6×(47,17)"},
         22:{"L":"2×(139,111),7×(140,112)","M":"17×(74,46)","Q":"7×(54,24),16×(55,25)","H":"34×(37,13)"},
         23:{"L":"4×(151,121),5×(152,122)","M":"4×(75,47),14×(76,48)","Q":"11×(54,24),14×(55,25)","H":"16×(45,15),14×(46,16)"},
         24:{"L":"6×(147,117),4×(148,118)","M":"6×(73,45),14×(74,46)","Q":"11×(54,24),16×(55,25)","H":"30×(46,16),2×(47,17)"},
         25:{"L":"8×(132,106),4×(133,107)","M":"8×(75,47),13×(76,48)","Q":"7×(54,24),22×(55,25)","H":"22×(45,15),13×(46,16)"},
         26:{"L":"10×(142,114),2×(143,115)","M":"19×(74,46),4×(75,47)","Q":"28×(50,22),6×(51,23)","H":"33×(46,16),4×(47,17)"},
         27:{"L":"8×(152,122),4×(153,123)","M":"22×(73,45),3×(74,46)","Q":"8×(53,23),26×(54,24)","H":"12×(45,15),28×(46,16)"},
         28:{"L":"3×(147,117),10×(148,118)","M":"3×(73,45),23×(74,46)","Q":"4×(54,24),31×(55,25)","H":"11×(45,15),31×(46,16)"},
         29:{"L":"7×(146,116),7×(147,117)","M":"21×(73,45),7×(74,46)","Q":"(53,23),37×(54,24)","H":"19×(45,15),26×(46,16)"},
         30:{"L":"5×(145,115),10×(146,116)","M":"19×(75,47),10×(76,48)","Q":"15×(54,24),25×(55,25)","H":"23×(45,15),25×(46,16)"},
         31:{"L":"13×(145,115),3×(146,116)","M":"2×(74,46),29×(75,47)","Q":"42×(54,24),(55,25)","H":"23×(45,15),28×(46,16)"},
         32:{"L":"17×(145,115)","M":"10×(74,46),23×(75,47)","Q":"10×(54,24),35×(55,25)","H":"19×(45,15),35×(46,16)"},
         33:{"L":"17×(145,115),(146,116)","M":"14×(74,46),21×(75,47)","Q":"29×(54,24),19×(55,25)","H":"11×(45,15),46×(46,16)"},
         34:{"L":"13×(145,115),6×(146,116)","M":"14×(74,46),23×(75,47)","Q":"44×(54,24),7×(55,25)","H":"59×(46,16),(47,17)"},
         35:{"L":"12×(151,121),7×(152,122)","M":"12×(75,47),26×(76,48)","Q":"39×(54,24),14×(55,25)","H":"22×(45,15),41×(46,16)"},
         36:{"L":"6×(151,121),14×(152,122)","M":"6×(75,47),34×(76,48)","Q":"46×(54,24),10×(55,25)","H":"2×(45,15),64×(46,16)"},
         37:{"L":"17×(152,122),4×(153,123)","M":"29×(74,46),14×(75,47)","Q":"49×(54,24),10×(55,25)","H":"24×(45,15),46×(46,16)"},
         38:{"L":"4×(152,122),18×(153,123)","M":"13×(74,46),32×(75,47)","Q":"48×(54,24),14×(55,25)","H":"42×(45,15),32×(46,16)"},
         39:{"L":"20×(147,117),4×(148,118)","M":"40×(75,47),7×(76,48)","Q":"43×(54,24),22×(55,25)","H":"10×(45,15),67×(46,16)"},
         40:{"L":"19×(148,118),6×(149,119)","M":"18×(75,47),31×(76,48)","Q":"34×(54,24),34×(55,25)","H":"20×(45,15),61×(46,16)"}
         }

# Caractères du mode alphanumérique

alphanum="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"

# Les quatre noms des modes

modes={0:"Numeric",1:"Alphanumeric",2:"Byte",3:"Kanji"}

# Longueurs en bits du champ qui donne la longueur du message

def longbin(version,mode):
  if version<=9:
    return {0:10,1:9,2:8,3:8}[mode]
  elif version<=26:
    return {0:12,1:11,2:16,3:10}[mode]
  return {0:14,1:13,2:16,3:12}[mode]

# Coordonnées suivantes dans le parcours du code

def suivant(i,j,direction,dimension):
  j-=1
  if j%2!=(dimension%2+(j<6))%2:
    j+=2
    i+=direction
    if i==-1:
      j-=2
      i=0
      direction=1
    if i==dimension:
      j-=2
      i=dimension-1
      direction=-1
    if j==6:
      j=5
  return i,j,direction

# Transformation du contenu brut en liste

def blocs(l):
  return list(eval(l.replace("×","*").replace("),",")+")))

# Transformation de la liste précédente en panachage des coordonnées

def court2long(l):
  l1=blocs(l)
  for i in range(0,len(l1),2):
    l1[i:i+2]=l1[i:i+2][::-1]
  l2=[[-1]]
  for i in range(len(l1)//2):
    l2.append([1+j+l2[-1][-1] for j in range(l1[2*i])])
  del l2[0]
#  print(l2)
  l3=[]
  for i in range(max(len(l) for l in l2)):
    for j in range(len(l2)):
      try:
        l3.append(l2[j][i])
      except IndexError:
#        print(j,i)
#        pass
        l3.append(-1)
#  print(l3)
  l4=[[max(l3)]]
  for i in range(len(l1)//2):
    l4.append([1+j+l4[-1][-1] for j in range(l1[2*i+1]-l1[2*i])])
  del l4[0]
  l5=[]
  for i in range(max(len(l) for l in l4)):
    for j in range(len(l4)):
#      try:
        l5.append(l4[j][i])
#      except IndexError:
#        pass
#        l5.append(-1)
  return l3,l5

# La même vrai/faux

def court2vf(l):
  l1=blocs(l)
  clair=l1[1::2]
  M=max(clair)
  m=min(clair)
  s1=M*len(l1)//2
  s2=sum(clair)
  l2=[True]*m*len(clair)
  l2+=[False]*(M-m)*l1.count(m)
  l2+=[True]*(M-m)*l1.count(M)
#  for n in l1[1::2]:
#    l2+=[True]*n
#    if n<m:
#      l2+=[False]*(m-n)
#  print(l2)
  l3=sum(l1[2*i]-l1[2*i+1] for i in range(len(clair)))
#  print(l3,s2)
#  print(l2,l3,s1,len(l1)//2)
  return l2,l3,s1,len(l1)//2

# La même en blocs

def court2blocs(l):
  l1=blocs(l)
  for i in range(0,len(l1),2):
    l1[i:i+2]=l1[i:i+2][::-1]
  l2,l3=[0],[0]
  for i in range(len(l1)//2):
    l2.append(l2[-1]+l1[2*i])
    l3.append(l3[-1]+l1[2*i+1]-l1[2*i])
#  print(l2,l3)
  return l2,l3

# Corrige une paire de données en clair avec le complément redondant

def corrige(clair,redondant):
  toutpoly=message2poly(clair+redondant)
  syndrome=[toutpoly(F256(F256.exp(i))) for i in range(len(redondant)//8)]
  if set(syndrome)!={F256(0)}:
    syndpoly=Polynome(tuple(syndrome[::-1]))
    r,v,rr,vv=Polynome.construction([1]+[0]*syndpoly.degre()),Polynome.construction([0]),syndpoly,Polynome.construction([1])
    while r.degre()>=len(syndpoly)//2:
#    while not r.estzero():
      q=r//rr
      r,v,rr,vv=rr,vv,r-q*rr,v-q*vv
    vder=v.der()
    racines=[i for i in range(255,255-len(toutpoly),-1) if v(F256(F256.exp(i)))==F256(0)]
    if 2*len(racines)>=len(syndrome):
      print("Il y a trop d’erreurs dans le bloc n°"+str(ii)+".")
      exit(1)
    erreurs={i:r(F256(F256.exp(i)))/vder(F256(F256.exp(i)))/F256(F256.exp(i)) for i in racines}
    for i in erreurs:
      toutpoly[255-i]+=erreurs[i]
    toutmessage=poly2message(toutpoly)
    return toutmessage[:len(clair)],toutmessage[len(clair):],len(racines)
  return clair,redondant,0

# Calcule le malus total d’un tableau QR

def malus(table):
  m=0

  def m1(ligne): # Malus des suites trop longues
    ch="".join(map(str,ligne))
    c=0
#    i=-1
    for cinq in ["11111","00000"]:
      i=-1
      while i<len(ch):
        i+=1
#      for cinq in ["11111","00000"]:
        if cinq in ch[i:]:
          i+=ch[i:].index(cinq)
          c-=2
          while ch[i]==cinq[0]:
            i+=1
            c+=1
            if i==len(ch):
              break
    return c

  for l in table:
    m+=m1(l)
  for i in range(len(table)):
    m+=m1([l[i] for l in table])

  def m2(table): # Malus des carrés
    c=0
    for i in range(len(table)-1):
      for j in range(len(table)-1):
        c+=3*(table[i][j]==table[i+1][j]==table[i][j+1]==table[i+1][j+1])
    return c

  m+=m2(table)

  def m3(ligne): # Malus des 10111010000
    ch="".join(map(str,ligne))
    return 40*(ch.count("10111010000")+ch.count("00001011101"))

  for l in table:
    m+=m3(l)
  for i in range(len(table)):
    m+=m3([l[i] for l in table])

  def m4(table): # Malus du trop grand écart
    m4n=sum(sum(l) for l in table)
    m4t=len(table)**2
    pourcent=100*m4n//m4t//5*5
    return min(abs(50-pourcent),abs(50-pourcent+5))//5*10

  m+=m4(table)

  return m

if __name__=="__main__":
  print(bin(resteformat(10)))
  court2vf(tableau[10]["L"])
