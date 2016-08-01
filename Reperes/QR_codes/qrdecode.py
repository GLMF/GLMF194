#!/usr/bin/python3

from PIL import Image
from sys import exit,stderr
from argparse import *
from qrcorps import *
from qrcodestandard import *
from qrcodeoutils import *

class qrdecode:
  """
  La classe stocke tout, les informations utiles sont construites au fur et à mesure
  """

#    Initialisation de l’instance

  def __init__(self):
    """
    self.fichier est le nom du fichier
    self.corrige signale si on doit corriger ou non la zone de données
    self.image est un tableau qui contient l’image en noir et blanc
    self.module contient la taille d’un module (les carrés noirs et blancs)
    self.qr contient le tableau de bits
    self.qr précise si l’image est orientée correctement
    self.dim contient le nombre de modules en largeur et en hauteur
    self.form contient les deux zones de format
    self.formatok précise si les formats sont validés et s’il a fallu en corriger
    self.nivcor est le niveau de correction
    self.gris contient le masque de la zone qui contient les données (message et code correcteur)
    self.masque contient la fonction qui démasque les données
    self.version contient la version
    self.mode contient le mode (byte, alphanumérique, numérique, kanji)
    self.longueur contient la longueur des données (message et code correcteur)
    self.longclair est la longueur du code en clair
    self.code contient le message (clair+redondant)
    self.clair contient le code en clair
    self.redondant contient le code correcteur
    self.messageok signale si le message en clair est cohérent et le nombre d’erreurs corrigées si nécessaire
    self.message contient le message final
    """

    [self.fichier,self.corrige,self.tout,self.image,self.module,self.qr,self.esttourne,self.dim,self.form,
      self.formatok,self.nivcor,self.gris,self.masque,self.version,self.mode,self.longueur,
      self.longclair,self.clair,self.redondant,self.messageok,self.code,self.message]=[None]*22

#    Affichage du message mais aussi de toutes les informations utiles

  def __str__(self):
    """
    Voici ce que la méthode peut retourner :
    Fichier : glmf3err.png
    Niveau de correction : L
    Masque :
    █··█··
    █··█··
    █··█··
    █··█··
    █··█··
    █··█··
    Dimensions : 29×29
    Version : 3
    Il y a eu besoin de corriger 7 erreur(s) dans la zone de données.
    Mode : Byte
    Longueur du message : 37
    Message :
    Lisez GNU/Linux magazine France. 😃
    """

    if self.tout:
      ch=""
      if self.fichier is not None:
        ch=ch+"Fichier : "+self.fichier+"\n"
      if self.formatok is not None and self.formatok is not True:
        ch=ch+"Il y a eu besoin de corriger la zone de format.\n"
      if self.nivcor is not None:
        ch=ch+"Niveau de correction : "+nomnivcor[self.nivcor]+"\n"
      if self.masque is not None:
        ch=ch+"Masque :\n"
        ch=ch+dessine([[self.masque(i,j) for j in range(6)] for i in range(6)])
      if self.dim is not None:
        ch=ch+"Dimensions : "+str(self.dim)+"×"+str(self.dim)+"\n"
      if self.version is not None:
        ch=ch+"Version : "+str(self.version)+"\n"
      if self.messageok is not None and self.messageok is not True:
        ch=ch+"Il y a eu besoin de corriger %d erreur(s) dans la zone de données.\n"%self.messageok
      if self.mode is not None:
        ch=ch+"Mode : "+modes[self.mode]+"\n" # modes est dans qrcodestandard
      if self.longclair is not None:
        ch=ch+"Longueur du message : "+str(self.longclair)+"\n"
      if self.message is not None:
        ch=ch+"Message :\n"+self.message+"\n"

      if ch:
        return ch[:-1]
      return "Rien n’est défini. 😱"
    else:
      return self.message

  def __repr__(self):
    if self.message is not None:
      return self.message
    return "Rien n’est défini. 😱"

#    On charge et on recadre l’image

  def chargeim(self):
    parser=ArgumentParser(description="Lis et corrige un code QR.")
    parser.add_argument("-i",required=True,metavar="image",help="Image d’entrée.")
    parser.add_argument("-c",choices=["1","0"],default="1",help="Corrige ou non les erreurs (peut planter si non).")
    parser.add_argument("-a",choices=["1","0"],default="0",help="On affiche tout ou seulement le message.")
    arguments=parser.parse_args()
    self.fichier=arguments.i
    self.corrige=int(arguments.c)
    self.tout=int(arguments.a)

    try:
      im=Image.open(self.fichier)
    except IOError:
      print("Fichier "+self.fichier+" inexistant.",file=stderr)
      exit(1)

    im=im.convert('1') # On convertit en noir et blanc
    pix=im.load()
    self.image=[]

    for i in range(im.height):
      self.image.append([0+(pix[j,i]==0) for j in range(im.width)])

    while sum(self.image[0])==0: # Recadrages des bords
      self.image=self.image[1:]
    while sum(self.image[-1])==0:
      self.image=self.image[:-1]
    self.image=[[0]*len(self.image[0])]*2+self.image+[[0]*len(self.image[0])]*2
    while True:
      s=0
      for l in self.image:
        s+=l[0]
      if s==0:
        for i in range(len(self.image)):
          self.image[i]=self.image[i][1:]
      else:
        break
    while True:
      s=0
      for l in self.image:
        s+=l[-1]
      if s==0:
        for i in range(len(self.image)):
          self.image[i]=self.image[i][:-1]
      else:
        break
    for i in range(len(self.image)):
      self.image[i]=[0,0]+self.image[i]+[0,0]

#    On calcule la dimension d’un module

  def dims(self):
    if self.image is None:
      self.chargeim()

#    i=0
#    etat0,etat1=0,0
#    no0,no1=[],[]

#    while not(len(no0)==2 or len(no1)==2): # Tant qu’on n’a pas eu 010 quelque part
#      if self.image[i][i]!=etat0:
#        etat0=self.image[i][i]
#        no0.append(i)
#      if self.image[-i-1][-i-1]!=etat1:
#        etat1=self.image[-i-1][-i-1]
#        no1.append(i)
#      i+=1

#    if len(no0)<len(no1): # Si seule no1 est pleine
#      self.module=no1[0]-no1[1]
#    else: # Sinon, on a forcément une cible parmi les deux
#      self.module=no0[1]-no0[0]

    graphe=[[None,0,None,None],[None,0,1,None],[None,None,1,0],[None]*4]
    motif=[self.image[i][i] for i in range(len(self.image))]
    _,coord1=regraph(graphe,motif,0,3)
    _,coord2=regraph(graphe,motif[::-1],0,3)
    coord=min(coord1,coord2)
    self.module=coord[2]-coord[1]

#    On transforme l’image en un tableau de 0 et de 1

  def stockeim(self):
    if self.module is None:
      self.dims()
    debut,taille=2,self.module
    self.qr=[]
    for i in range(debut,len(self.image)-debut,taille):
      self.qr.append([])
      for j in range(debut,len(self.image[0])-debut,taille):
        self.qr[-1].append(self.image[i][j])

#    On tourne le code si nécessaire pour avoir le coin neutre en bas à droite

  def placeim(self):
    if self.qr is None:
      self.stockeim()

    for i in range(7): # Reconnaissance du coin sans cible
      if self.qr[i][:7]!=cible[i]: # cible est dans qrcodestandard
        coin=2
        break
      if self.qr[-i-1][:7]!=cible[i]:
        coin=1
        break
      if self.qr[i][-7:]!=cible[i]:
        coin=3
        break
      if self.qr[-i-1][-7:]!=cible[i]:
        coin=0
        break

#    def tourner90(matrice):
#      nl=len(matrice)
#      nc=len(matrice[0])
#      m=[[0 for _ in range(nl)] for _ in range(nc)]
#      for i in range(nl):
#        for j in range(nc):
#          m[j][i]=matrice[i][-j-1]
#      return m

    for _ in range(coin): # On tourne le nombre de fois qu’il faut
      self.qr=tourner90(self.qr)
    self.esttourne=True

# On détermine les formats du code et leur validité

  def formats(self):
    if self.esttourne is None:
      self.placeim()
    self.form=[None,None]
    self.form[0]=self.qr[8][:6]+self.qr[8][7:9]+[self.qr[7][8]]
    for i in range(5,-1,-1):
      self.form[0].append(self.qr[i][8])
    self.form[0]=[i^j for (i,j) in zip(self.form[0],masquef)] # masquef est dans qrcodestandard
    self.form[1]=[self.qr[-i-1][8] for i in range(7)]
    self.form[1]=self.form[1]+self.qr[8][-8:]
    self.form[1]=[i^j for (i,j) in zip(self.form[1],masquef)]

#    On vérifie les formats et on les corrige s’il le faut et si on le peut

  def verifformat(self):
    if self.form is None:
      self.formats()
    r0=bin2dec(self.form[0][5:])
    r1=bin2dec(self.form[1][5:])
    hamming={i:set() for i in range(16)}
    for form in range(32):
      r=resteformat(form)
      reste0=r0^r
      reste1=r1^r
      c0=bin(reste0).count("1")
      c1=bin(reste1).count("1")
      hamming[c0].add(form)
      hamming[c1].add(form)
    m=min(h for h in hamming if hamming[h])
    if m:
      self.formatok=False
    else:
      self.formatok=True
    if len(hamming[m])>1:
      print("Erreur, conflit de formats.")
      exit(1)
    self.form[0]=[int(i) for i in bin(hamming[m].pop())[2:]]
    self.form[0]=[0]*(5-len(self.form[0]))+self.form[0]

#    On démasque le code

  def demasque(self):
    if self.formatok is None:
      self.verifformat()

    self.nivcor=niveaucorrection[tuple(self.form[0][:2])] # niveaucorrection est dans qrcodestandard
    self.masque=masques[tuple(self.form[0][2:5])] # masques est dans qrcodestandard

    self.dim=len(self.qr)
    self.version=(self.dim-17)//4
    self.gris=griser(self.dim,self.version) # griser est dans qrcodestandard

    for i in range(self.dim):
      for j in range(self.dim):
        if self.gris[i][j]:
          self.qr[i][j]^=self.masque(i,j)

#    On décode le message binaire et la partie redondante

  def messagebrut(self):
    if None in [self.version,self.masque,self.dim,self.gris,self.nivcor]:
      self.demasque()
    i,j=self.dim-1,self.dim-1
    self.code=[]
    direction=-1

    limite=(16*(4+self.version*(8+self.version))\
           -25*(self.version>=2+self.version//7)**2\
           -(self.version>=7)*(36+self.version//7*40))//8*8
    while len(self.code)<limite:
      if self.gris[i][j]:
        self.code.append(self.qr[i][j])
      i,j,direction=suivant(i,j,direction,self.dim) # suivant est dans qrcodestandard

#    posclair,posredondant=court2long(tableau[self.version][self.nivcor]) # tableau et court2long sont dans qrcodestandard
#    self.clair=[[] for _ in range(len(blocs(tableau[self.version][self.nivcor]))//2)] # blocs est dans qrcodestandard
#    self.redondant=[[] for _ in self.clair]#[[] for _ in blocs(tableau[self.version][self.nivcor])[1:]] # blocs vraiment utile ?

    posclair,lonredondant,lonclair,nbbloc=court2vf(tableau[self.version][self.nivcor])

#    posclair2,lonredondant,lonclair,finclair,nbbloc=court2vf(tableau[self.version][self.nivcor])
    self.clair=[[] for _ in range(nbbloc)]
    self.redondant=[[] for _ in self.clair]

#    print(court2blocs(tableau[self.version][self.nivcor]))
#    print("→",end="")
#    print(posclair)
#    print(finclair,lonclair)
#    print("→",end="")
#    print(posredondant)
#    print(max(posclair),len(posclair))
#    for i in range(len(posclair)):
#        if posclair[i]==-1 or posclair2[i]==False:
#          print(i,posclair[i],posclair2[i])

#    j=0
#    for i in range(len(posclair)):#len(posclair)): # À améliorer
#      if posclair[i]!=-1:
#        self.clair[i%len(self.clair)]+=self.code[j*8:j*8+8]#self.code[posclair[i]*8:posclair[i]*8+8]
#        j+=1

    j=0
    for i in range(lonclair):
      if posclair[i]:
        self.clair[i%nbbloc]+=self.code[j*8:j*8+8]
        j+=1
#    print(j,i)

#      else:
#        self.clair[i%len(self.clair)]+=[0]*8
#    print(self.code[:8]+self.code[32:40],self.clair[0][:16])
#    print(posclair[0],posclair[4])

#    for i in range(len(posredondant)):
#      self.redondant[i%len(self.redondant)]+=self.code[(i+min(posredondant))*8:(i+min(posredondant)+1)*8]#self.code[posredondant[i]*8:posredondant[i]*8+8]

    for i in range(lonredondant):
      self.redondant[i%nbbloc]+=self.code[(i+j)*8:(i+j+1)*8]
#    print(self.redondant)
#    print(finclair)

#    On corrige le message en clair si nécessaire

  def messagecorr(self):
    if None in [self.clair,self.redondant]:
      self.messagebrut()
    compte=0
    if self.corrige:
      for i in range(len(self.clair)):
        self.clair[i],self.redondant[i],c=corrige(self.clair[i],self.redondant[i]) # corrige est dans qrcodestandard
        compte+=c
#        print(c,len(self.clair[i])//8,len(self.redondant[i])//8)
    clair=[]
    for l in self.clair:
      clair+=l
    self.clair=clair
    redondant=[]
    for l in self.redondant:
      redondant+=l
    self.redondant=redondant
    if compte:
      self.messageok=compte
    else:
      self.messakeok=True

#    Et on décode le message en clair

  def decodeqr(self):
    if self.messageok is None:
      self.messagecorr()

    self.mode=3-self.code[:4].index(1)
    self.longueur=longbin(self.version,self.mode) # longbin est dans qrcodestandard

#    ch=""
#    for i in range(0,len(self.clair),8):
#      aj=hex(bin2dec(self.clair[i:i+8]))[2:] # bin2dec est dans qrcodeoutils
#      ch=ch+"0"*(2-len(aj))+aj
#    ch=""
#    for i in range(0,len(self.redondant),8):
#      aj=hex(bin2dec(self.redondant[i:i+8]))[2:]
#      ch=ch+"0"*(2-len(aj))+aj
    self.longclair=bin2dec(self.clair[4:4+self.longueur])

    def numeric():
      n=""
      fin=self.longclair%3
      self.longclair-=fin
      i=4+self.longueur
      while len(n)<self.longclair:
        p=str(bin2dec(self.clair[i:i+10]))
        n=n+"0"*(3-len(p))+p
        i+=10
      if fin==1:
        p=str(bin2dec(self.clair[i:i+4]))
        n=n+"0"*(1-len(p))+p
      elif fin==2:
        p=str(bin2dec(self.clair[i:i+7]))
        n=n+"0"*(2-len(p))+p
      return n#str(int(n))
  
    def alphanumeric():
      ch=""
      fin=self.longclair%2
      self.longclair-=fin
      i=4+self.longueur
      while len(ch)<self.longclair:
        n=bin2dec(self.clair[i:i+11])
        q,r=divmod(n,45)
        ch=ch+alphanum[q]+alphanum[r] # alphanum est dans qrcodestandard
        i+=11
      if fin==1:
        ch=ch+alphanum[bin2dec(self.clair[i:i+6])]
      return ch

    def byte():
      return bytes([bin2dec(self.clair[i:i+8]) for i in range(4+self.longueur,4+self.longueur+self.longclair*8,8)]).decode("utf-8",errors="ignore")

    def kanji():
      raise NotImplementedError

    self.message={0:numeric,1:alphanumeric,2:byte,3:kanji}[self.mode]()

if __name__=="__main__":
  code=qrdecode()
  code.decodeqr()
  print(code)
#  for m in sorted(masques):
#    print(m)
#    print(dessine([[masques[m](j,i) for i in range(6)] for j in range(6)]))
