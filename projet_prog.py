## Importation des données du csv sur Python
#Importer les données
import pandas as pd #biblio pandas: pour lire les données et pouvoir les traiter
import requests # permet de faire des requetes html en python
import io #permet de gérer les str


url = "https://raw.githubusercontent.com/margueritepap/projet_eivp_info/main/donnees.csv" # prend le fichier csv depuis git
download = requests.get(url).content #le télécharge

df = pd.read_csv(io.StringIO(download.decode('utf-8'))) #lis le contenu du fichier et le change en données exploitables par pandas (dataframe=df)


# print (df) #affiche toutes les données du fichier

#Séparer et convertir les données en listes exploitables

donnees_lignes = df.values.tolist()
entete=df.columns.values.tolist()
#print (donnees_lignes)
#print(entete)

#Isoler les colonnes nécessaires
def preleve_colonne(D,n): #prélève la colonne n du tableau D et la renvoie sous forme d'une liste (sans entete)
    l=len(D)
    a=D[0][0] #on sépare les entètes du reste du tableau
    b=[a.split(';')]
    c=float(b[0][n])
    S=[c]
    for k in range (1,l):
        a=D[k][0]
        b=[a.split(';')] #change les ; en ,
        c=float(b[0][n]) #change le str en chiffre
        S+=[c]
    return S


## Evolution d’une variable en fonction du temps
#Récupérer la colonne des dates
def virgule(D): #remplace les ; par des ,
    l=len(D)
    A=[]
    n=0
    for k in range (l):
        i=D[k][0]
        n=i.replace(';',',')
        A+=[[n]]
    return A

def recup_date(L): #récupère la colonne de dates de L
    D=virgule(L)
    l=len(E)
    I=[]
    for k in range (l):
        i=D[k][0]
        e=i.split(',')
        I+=[e[7]]
    return I

#Récupérer séparément les heures et les dates
def divise_dh(L): #sépare l'heure de la date
    l=len(L)
    D=[]
    for k in range (l):
        h=L[k]
        a=h.split()
        D+=[a]
    return D

def preleve_jours(L): #prélève toutes les dates sans les horaires
    l=len(L)
    D=divise_dh(L)
    J=[]
    for k in range (l):
        J+=[D[k][0]]
    return J

def preleve_horaires(L):  #renvoie la liste des horaires
    l=len(L)
    D=divise_dh(L)
    H=[]
    for k in range (l):
        h=D[k][1]
        T=h.split('+')
        t=T[0]
        H+=[t]
    return H

#Calcul des instants des mesures

def timming(L):  #prend en argument un tableau L envoie la liste des instants de mesure
    D=recup_date(L)
    H=preleve_horaires(D)
    l=len(D)
    t=0
    a=H[0].split(':')
    h=float(a[0]) #heure de la 1ere mesure
    m=float(a[1]) #minute de la 1ere mesure
    s=float(a[2]) #seconde de la 2ere mesure
    T=[] #liste des timmings de mesure
    hh=0
    mm=0
    ss=0
    jj=0
    for k in range (l):
        b=H[k].split(':')
        ss=round(float(b[2])-s) #pour chaque mesure on calcule à quel t elle a été réalisée si la première a été réalisée à t=0
        if ss<0:
            ss=ss+60
            mm=mm-1
        mm+=round(float(b[1])-m)
        if mm<0:
            mm=mm+60
            hh=hh-1
        hh+=round(float(b[0])-h)
        if hh>23:
            hh=0
            jj+=1
        sss=str(ss)
        mmm=str(mm)
        hhh=str(hh)
        jjj=str(jj)
        U=[jjj,hhh,mmm,sss]
        t=':'.join(U)
        T+=[t]
    return T
## Calcul des valeurs statistiques
from math import * #pour le calcul de l'écart type

def min(L):
    if len(L)==0:
        return('La liste est vide ')
    m=L[0]
    for k in range (len(L)):
        t=L[k]
        if t<m:
            m=t
    return m

def max(L):
    if len(L)==0:
        return('La liste est vide ')
    m=L[0]
    for k in range (len(L)):
        t=L[k]
        if t>m:
            m=t
    return m

def moyenne(L):
    l=len(L)
    if l==0:
        return 'La liste est vide'
    m=0
    for k in range (l):
        m+=L[k]
    return m/l

def mediane(L):
    l=len(L)
    m=int(l%2) #parité du nb d'éléments de la liste
    if l!=0:
        if m==0: #si nb pair d'éléments
            i=int(l/2)
            mo=(L[i-1]+L[i+1])/2
            return int(mo)
        else: #si nb impaire d'éléments
            i=int((l-1)/2)
            return L[i]
    return "La liste est vide"

def variance(L):
    moy=moyenne(L)
    V=0
    l=len(L)
    if l!=0:
        for k in range (l):
            V+=(L[k]-moy)**2
        return V/l
    else:
        return "La liste est vide"

def ecart_type(L):
    v=variance(L)
    return sqrt(v)

## Calcul de l'indice “humidex”
#Extraction des températures et des taux d'humidité
T=preleve_colonne(donnees_lignes,3)
H=preleve_colonne(donnees_lignes,4)

#Fonction de calcul de humidex

def indice_humidex(T,H):
    l=len(T)
    humi=[]
    for k in range (l):
        t=T[k]
        h=H[k]
        a=10**(7.5*t/(237.7+t))
        i=t+((5/9)*((6.112*a*h/100)-10))
        hum=round(i)
        humi+=[hum]
    return humi


## Calcul de l’indice de corrélation entre un couple de variables

#Calcul du coeff de corrélation linéaire de Bravais-Pearson
def covariance (A,B): #Cov(A,B)
    l=len(A)
    if l!=0:
        c=0
        ma=moyenne(A)
        mb=moyenne(B)
        for k in range (l):
            c+=(A[k]-ma)*(B[k]-mb)
        return c/l
    return "La liste est vide"

def indice_correlation_Barvais_Pearson(A,B): #pour les valeurs régulières, peut atteindre ses limites en cas d'irrégularité
    ea=ecart_type(A)
    eb=ecart_type(B)
    cov=covariance(A,B)
    return cov/(ea*eb)

#Calcul de l'indice de corrélation de Spearman:

#pour des valeurs qui présentent des irrégularités, permet de mettre en évidence une relation non lénaire
def tri_rapide(L):
    if L==[]:
        return L
    L_g=[]
    L_d=[]
    for i in range(1,len(L)):
        if L[i]<=L[0]:
            L_g.append(L[i])
        else:
            L_d.append(L[i])
    return tri_rapide(L_g)+[L[0]]+tri_rapide(L_d)

def rang(a,L): #donne le rang de la première apparaition l'élément a dans la liste L
    T=tri_rapide(L)
    for k in range (len(L)):
        if a==L[k]:
            return k+1
    return "Cet élément n'est pas dans la liste"


def liste_rang(L): #renvoie la liste des rangs des éléments de L
    T=tri_rapide(L)
    r=0
    l=len(L)
    LR=[]
    for k in range (l):
        LR+=[rang(L[k],T)]
    return LR

def indice_correlation_Spearman(A,B):
    LA=liste_rang(A)
    LB=liste_rang(B)
    ea=ecart_type(LA)
    eb=ecart_type(LB)
    cov=covariance(LA,LB)
    return cov/(ea*eb)
