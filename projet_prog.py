## Importation des données du csv sur Python
#Importer les données
import pandas as pd #biblio pandas: pour lire les données et pouvoir les traiter
import requests # permet de faire des requetes html en python
import io #permet de gérer les str


url = "https://raw.githubusercontent.com/margueritepap/projet_eivp_info/main/donnees.csv" # prend le fichier csv depuis git
download = requests.get(url).content #le télécharge

df = pd.read_csv(io.StringIO(download.decode('utf-8'))) #lis le contenu du fichier et le change en données exploitables par pandas (dataframe=df)
df['sent_at']=pd.to_datetime(df.sent_at)                 #pour que les dates soient considérées comme du temps


# print (df) #affiche toutes les données du fichier
#Séparer et convertir les données en listes exploitables

donnees_lignes = df.values.tolist()
tete=df.columns.values.tolist()
print (donnees_lignes)
print(tete)



## Evolution d’une variable en fonction du temps
#Convertir
## Calcul des valeurs statistiques
from math import * #pour le calcul de l'écart type


def min_max(doc,nom):                         #nom=le nom de la colonne dont veut le min/max
    min=doc[nom][0]
    max=doc[nom][0]
    i=0                                       #indice du min
    I=0                                       #indice du max
    for k in range(doc.shape[0]):
        if doc[nom][k]<min:
            min=doc[nom][k]
            i=k
        elif doc[nom][k]>max:
            max=doc[nom][k]
            I=k
    return min,i,max,I

def moyenne(L):
    l=len(L)
    m=0
    for k in range (l):
        m+=L[k]
    return m/l

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

def mediane(L):
    Li=tri_rapide(L)
    l=len(L)
    m=int(l%2) #parité du nb d'éléments de la liste
    if l!=0:
        if m==0: #si nb pair d'éléments
            i=int(l/2)
            mo=(Li[i-1]+Li[i+1])/2
            return int(mo)
        else: #si nb impaire d'éléments
            i=int((l-1)/2)
            return Li[i]
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


#Fonction de calcul de humidex
def indice_humidex (T,H):#prend en arguments la liste de Temp et de %Hum
    t=T[0]
    h=H[0]
    hum=[] #liste des indices humidex pour chaque paire temp/%humidité
    for k in range (len(T)):
        I=(log(t/100)+((17.27*t)/(237.3+t)))/17.27
        rosee=(237.3*I)/(1-I)
        hum+=t+0.5555*(6.11*exp(5417.753*(1/273.16-1/(273.15+rosee)))-10)
        t=T[k]
        h=H[k]
    return hum

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


def locali_dates(doc,heure):                     #renvoie la ligne de la date "la plus proche" dans le doc de celle qu'on a rentré dans la fonction, on a besoin de la même écriture de l'heure
    tri_rapide(doc['sent_at'])                   
    a=0
    b=doc.shape[0]                               #car c'est le nombre de lignes
    c=doc.shape[0]//2
    d=timedelta(minutes=1)                       #si on sait qu'on rentre une heure du tableau on peut mettre un temps plus court, c'était pour être sûre que la boucle s'arrêterait toujours
    if heure<=doc['sent_at'][0]:
        return 0
    elif heure>=doc['sent_at'][doc.shape[0]-1]:
        return doc.shape[0]-1
    else:
        while abs(heure-doc['sent_at'][c])>d:    #problème, en fonction de d on aura pas forcément la date la plus proche mais c'est pour être sûr que la boucle s'arrêtera pour toutes/un max de dates
            if heure<=doc['sent_at'][c]:
                b=c
                c=c//2
            else:
                a=c
                c=(a+b)//2
        return c


    
 def Graphe(doc, nom, start=fichi['sent_at'][0], end=fichi['sent_at'][fichi.shape[0]-1]):     #nom correspond au nom de la colonne (doit être entre guillemets), ne marque que pour le fichier fichi
    Y=doc['sent_at']                                                                          #ça marche parce qu'on connait le nom de la colonne avec les dates
    X=[doc[nom][k] for k in range(doc.shape[0])]                                              #dans le range c'est le nombre de lignes
    med=mediane(doc,nom)[0]
    moy=moyenne(doc,nom)
    plt.close()
    plt.plot(X,Y)
    plt.plot(min_max(doc,nom)[0],min_max(doc,nom)[1], color='black', marker=(5,1))
    plt.plot(min_max(doc,nom)[2],min_max(doc,nom)[3], color='black', marker=(5,1))
    plt.plot([med,med],[0,doc['sent_at'][doc.shape[0]-1]], color='green')                     #trace une ligne horizontale pour la médiane
    plt.plot([moy,moy],[0,doc['sent_at'][doc.shape[0]-1]], color='magenta')                   #trace une ligne horizontale pour la moyenne
    pyplot.title('Evolution de ', nom, 'en octobre 2019')
    plt.show()











