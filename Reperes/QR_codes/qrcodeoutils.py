#!/usr/bin/python3

def memorise(f):
  cache=dict()

  def fonctionmemorisee(*args):
    if args not in cache:
      cache[args]=f(*args)
    return cache[args]

  fonctionmemorisee.cache=cache
  return fonctionmemorisee

def veriftype(f):
  def nouveau(self,autre):
    if (hasattr(autre.__class__,'priorite') and autre.__class__.operatorPrecedence>self.__class__.operatorPrecedence):
      return NotImplemented

    if type(self) is not type(autre):
      try:
        autre=self.__class__(autre)
      except TypeError:
        try:
          self=autre.__class__(self)
        except TypeError:
          message='Pas d’isomorphisme entre %s de type %s vers le type %s dans la fonction %s'
          raise TypeError(message%(autre,type(autre).__name__,type(self).__name__,f.__name__))
      except Exception as e:
        message='Erreur de type dans les arguments %r et %r pour la fonction %s. Raison:%s'
        raise TypeError(message%(self,autre,f.__name__,type(autre).__name__,type(self).__name__,e))

    return f(self,autre)

  return nouveau

class ElementAnneau(object):
  def __radd__(self,autre):
    return self+autre
  def __rsub__(self,autre):
    return -self+autre
  def __rmul__(self,autre):
    return self*autre

def bezout(n,a): # a<n au=1 [n]
  r,u,v,rr,uu,vv=a,1,0,n,0,1
  while rr!=0:
    q=r//rr
    r,u,v,rr,uu,vv=rr,uu,vv,r-q*rr,u-q*uu,v-q*vv
  return u%n

def algoeuclideetendu(a,b):
  if abs(b)>abs(a):
    (x,y,d)=algoeuclideetendu(b,a)
    return (y,x,d)

  zero=a.__class__(0)
  un=a.__class__(1)
  if abs(b)==0:
    return (un,zero,a)
  x1,x2,y1,y2=zero,un,un,zero
  while abs(b)>0:
    q,r=divmod(a,b)
    x=x2-q*x1
    y=y2-q*y1
    a,b,x2,x1,y2,y1=b,r,x1,x,y1,y

  return (x2,y2,a)

def bin2dec(n):
  if isinstance(n,str):
    n=[int(i) for i in n]
  s=0
  for b in n:
    s*=2
    s+=b
  return s

def dec2bin(n,lon):
  liste=[int(i) for i in bin(n)[2:]]
  liste=[0]*(lon-len(liste))+liste
  return liste

def dessine(tableau):
  dic={0:"·",1:"█",False:"·",True:"█"}
  c=""
  for l in tableau:
    c=c+''.join(dic[i] for i in l)+"\n"
  return c

def regraph(g,l,deb,fin):
  pos=deb
  coord=[]
  for i in range(len(l)):
#    print(l[i],i,pos)
    if l[i] in g[pos]:
      npos=g[pos].index(l[i])
      if npos!=pos:
        coord.append(i)
      pos=npos#g[pos].index(l[i])
    elif i!=len(l)-1:
      return False,coord
  return pos==fin,coord

def tourner90(matrice):
  nl=len(matrice)
  nc=len(matrice[0])
  m=[[0 for _ in range(nl)] for _ in range(nc)]
  for i in range(nl):
    for j in range(nc):
      m[j][i]=matrice[i][-j-1]
  return m

if __name__=="__main__":
  g=[[None,0,None,None],[None,0,1,None],[None,None,1,0],[None]*4]
  l=[0,0,0,0,1,1,0,0]
  print(regraph(g,l,0,3))
