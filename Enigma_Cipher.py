import random
import datetime
import time
from tqdm import tqdm

random.seed(10)
daily_key = [[random.choice(range(26)),random.choice(range(26)),random.choice(range(26))] for k in range(31)] #réglage initial de la machine pour chaque jour du mois
today = datetime.datetime.now().day

###Fonctions utiles sur les permutations et les rotors

def pwr(n) :
    """
    Entree : un entier n
    Sortie : une permutation aléatoire sur [0,n-1]
    """
    P = []
    C = [k for k in range(n)]
    while len(C) != 0 :
        i = random.choice(C)
        P.append(i)
        C.remove(i)
    return(P)

class permutation :
    def __init__(self,L) : #perm est la liste des images des L entiers (on len(L)) par la permutation
        if type(L) == int :
            self.perm = pwr(L)
            self.length = L
        elif type(L) == list :
            self.perm = L
            self.length = len(L)

def identite(n) :
    """
    Entree : un entier n
    Sortie : la permutation identité sur [0,n-1]
    """
    L = [k for k in range(n)]
    return(permutation(L))

def composition(s1,s2) :
    """
    Entree : Deux permutations sur le même ensemble
    Sortie : La permutation composée des deux permutations, s1 'rond' s2
    """
    L = [s1.perm[k] for k in s2.perm]
    comp = permutation(L)
    return(comp)

def circu(n) :
    """
    Entree : un entier n
    Sortie : la permutation dans [0,n-1] circulaire de taille n
    """
    L = [k for k in range(n)]
    L = L[1:] + L[0:1]
    return(permutation(L))

def iteration(s,k) :
    """
    Entree : une permutation s, un entier k
    Sortie : la permutation s itérée k fois, s^k
    """
    T = identite(s.length)
    for i in range(k) :
        T = composition(T,s)
    return(T)

def orbit(s) :
    """
    Entree : une permutation s
    Sortie : la liste de ses orbites
    """
    L = s.perm
    O = []
    deja_vu = []
    i = 0
    while i != s.length :
        if L[i] not in deja_vu :
            orb = [L[i]]
            j = L[i]
            while L[j] != L[i] :
                deja_vu.append(L[j])
                orb.append(L[j])
                j = L[j]
            O.append(orb)
        i += 1
    return(O)

def motif(s) :
    """
    Entree : une permutation s
    Sortie : le motif de la décomposition de s, ie la liste ordonnée de manière croissante des longueurs de ses orbites
    """
    orb = orbit(s)
    long = [len(k) for k in orb]
    return(sorted(long))

def inverse(s) :
    """
    Entree : une permutation s
    Sortie : son inverse
    """
    L = s.perm
    I = [L.index(k) for k in range(s.length)]
    return(permutation(I))


class rotor(permutation) :
    def __init__(self,L) :
        super().__init__(L)
        self.pos = 0

    def clear(self) :
        """
        Entree : None
        Sortie : methode qui remet le rotor dans sa position initiale, la numéro 0
        """
        self.shift(26-self.pos)

    def shift(self,k) :
        """
        Entree : entier k
        Sortie : methode qui décale le rotor k fois via la méthode p^k 'rond' p^{-k} où k est la permutation circulaire
        """
        P = circu(self.length)
        Pk = iteration(P,k)
        Pmk = inverse(Pk)
        I = composition(Pk,self)
        I = composition(I,Pmk)
        self.perm = I.perm
        self.pos = (self.pos + k)%self.length




def reflecteur() :
    """
    Entree : None
    Sortie : un reflecteur enigma aléatoire, ie une permutation formée par 13 transpositions disjointes
    """
    L = [k for k in range(26)]
    random.shuffle(L)
    C = [(L[2*k],L[2*k+1]) for k in range(13)]
    T = [0]*26
    for (fst,snd) in C :
        T[fst],T[snd] = snd,fst
    return(rotor(T))

def tableau() :
    """
    Entree : None
    Sortie : un tableau de connexion enigma, ie une permutation formée de 10 transpositions disjointes et 6 points fixes
    """
    L = [k for k in range(26)]
    random.shuffle(L)
    C = [(L[2*k],L[2*k+1]) for k in range(10)]
    T = [k for k in range(26)]
    for (fst,snd) in C :
        T[fst],T[snd] = snd,fst
    return(rotor(T))

daily_tableau = [tableau() for k in range(31)] #Les configurations du tableau de connexion pour chaque jours du mois

def perm_crypt(refl,tablo,R1,R2,R3) :
    """
    Entree : un réflecteur, un tableau de connexion et 3 rotors
    Sortie : la permutation provenant de la combinaison tableau -> 3 rotors -> réflecteur -> 3 rotors -> tableau
    """
    tablm = inverse(tablo)
    R1m,R2m,R3m = inverse(R1),inverse(R2),inverse(R3)
    C = composition(tablo,R1)
    C = composition(C,R2)
    C = composition(C,R3)
    C = composition(C,refl)
    C = composition(C,R3m)
    C = composition(C,R2m)
    C = composition(C,R1m)
    C = composition(C,tablm)
    return(C)

###Définition des fonctions de chiffrage d'enigma

#Définition des rotors, du réflecteur et du tableau de connexion, dans la réalité, seuls les rotors et le réflecteur sont connus publiquement
I = identite(26)
R1,R2,R3,refl = rotor(26),rotor(26),rotor(26),reflecteur()
tabl=daily_tableau[today]
print("Le réglage initial du jour est :\n",daily_key[today],"\nLe tableau de connexion du jour est : \n",I.perm,"\n",tabl.perm,"\nLa permutation du premier rotor est :\n",I.perm,"\n",R1.perm,"\nLa permutation du deuxième rotor est :\n",I.perm,"\n",R2.perm,"\nLa permutation du troisième rotor est :\n",I.perm,"\n",R3.perm,"\nLa permutation du réflecteur est :\n",I.perm,"\n",refl.perm,"\n")

#fonction de chiffrage sans interface H/M
def enigma(text,cle,R1,R2,R3,refl,tablo) :
    """
    Entree : un string (le message en clair), une clé de chiffrage (la position initiale des rotors), 3 rotors, un reflecteur et un tableau de connexion
    Sortie : un texte crypté avec la machine enigma au réglages entrés
    """
    #formalisation du message
    text = text.replace(" ","")
    #écriture du message en clair
    R1.clear()
    R1.shift(cle[0])
    R2.clear()
    R3.shift(cle[1])
    R3.clear()
    R3.shift(cle[2])
    txt_cry = ''
    for k in range(len(text)) :
        P = perm_crypt(refl,tablo,R1,R2,R3)
        lettre = (ord(text[k])-97)
        chf_cry = P.perm[lettre]
        txt_cry += chr(97+chf_cry)

        R1.shift(1)
        if R1.pos == 0 :
            R2.shift(1)
            if R2.pos == 0 :
                R3.shift(1)
    return(txt_cry)

#test unitaire

def test_enigma() :
    mot = 'bonjour'*10
    L = range(26)
    a,b,c = random.choice(L),random.choice(L),random.choice(L)
    mot_cry = enigma(mot,[a,b,c],R1,R2,R3,refl,tabl)
    if mot != enigma(mot_cry,[a,b,c],R1,R2,R3,refl,tabl) :
        raise Exception("Pas d'inversibilité du chiffrage'")

def enigma_user(text,cle) :
    """
    Entree : un string (le message en clair) et une clé de chiffrage choisie par l'utilisateur composée de 3 lettres
    Sortie : le message chiffré avec pour 6 premiers caractère, la clé utilisateur chiffrée deux fois avec le réglage du jour
    """
    user_key = cle*2
    user_key_cry = enigma(user_key,daily_key[today],R1,R2,R3,refl,tabl)
    user_settings = [ord(k)-97 for k in cle]
    text_cry = enigma(text,user_settings,R1,R2,R3,refl,tabl)
    return user_key_cry + ' ' +  text_cry

### On va maintenant définir des fonctions qui retrouvent les paramètres du jours à savoir la clé de réglage ainsi que les connexions du tableau

#La fonction suivante résume le travail des cryptographes qui analysaient des dizaines de messages pour trouver les permutations intermédiaires
#Les résultats de cette fonction sont en réalités déterminés empiriquement
def permR() :
    """
    Sortie : les permutations Beta0, Beta1 et Beta2 où Betai = tableau -> rotors+réflecteur après i+3 mouvements -> (rotors+réflecteur après i mouvements)^{-1} -> tableau
    """
    #initialisation des rotors
    key  = daily_key[today]
    R1.clear()
    R1.shift(key[0])
    R2.clear()
    R2.shift(key[1])
    R3.clear()
    R3.shift(key[2])
    inter = []
    for k in range(6) :
        i = perm_crypt(refl,tabl,R1,R2,R3)
        inter.append(i)
        R1.shift(1)
        if R1.pos == 0 :
            R2.shift(1)
            if R2.pos == 0 :
                R3.shift(1)
    beta0 = composition(inter[3],inverse(inter[0]))
    beta1 = composition(inter[4],inverse(inter[1]))
    beta2 = composition(inter[5],inverse(inter[2]))
    Beta = [beta0,beta1,beta2]
    return(Beta)

#Le travail des cryptographes polonais commence ici

def permR_bis(cle) :
    """
    Entree : une clé de réglage initial des rotors (une liste de 3 entiers)
    Sortie : la liste des permutations (3 rotors + reflecteur après i+3 mouvement) -> (3 rotors + reflecteurs après i mouvements)^{-1} pour i dans [0,1,2]
    """
    R1.clear()
    R1.shift(cle[0])
    R2.clear()
    R2.shift(cle[1])
    R3.clear()
    R3.shift(cle[2])
    inter = []
    for k in range(6) :
        R1m,R2m,R3m = inverse(R1),inverse(R2),inverse(R3)
        C = composition(R1,R2)
        C = composition(C,R3)
        C = composition(C,refl)
        C = composition(C,R3m)
        C = composition(C,R2m)
        C = composition(C,R1m)
        R1.shift(1)
        if R1.pos == 0 :
            R2.shift(1)
            if R2.pos == 0 :
                R3.shift(1)
        inter.append(C)
    alpha0 = composition(inter[3],inverse(inter[0]))
    alpha1 = composition(inter[4],inverse(inter[1]))
    alpha2 = composition(inter[5],inverse(inter[2]))
    Alpha = [alpha0,alpha1,alpha2]
    return(Alpha)

def triples_R() :
    """
    Entree : une liste de 3 permutations beta0,beta1 et beta2
    Sortie : la liste des positions initiales des rotors pour lesquelles (3 rotors + reflecteur après i+3 mouvement) -> (3 rotors + reflecteurs après i mouvements)^{-1} a le même motif de décomposition que betai
    """
    beta = permR()
    motif0 = motif(beta[0])
    motif1 = motif(beta[1])
    motif2 = motif(beta[2])
    possible = []
    for i in tqdm(range(26)) :
        for j in range(26) :
            for k in range(26) :
                alpha = permR_bis([i,j,k])
                if (motif(alpha[0]) == motif0) and (motif(alpha[1]) == motif1) and (motif(alpha[2]) == motif2) :
                    possible.append([i,j,k])
    return(possible)

#test unitaire de triples_R (le réglage initial du jour doit se trouvé dans les réglages possibles)

def test_triples_R() :
    if daily_key[today] not in triples_R() :
        raise Exception("Le triplé du jour n'apparaît pas dans les triplés possibles'")


t1 = time.time()
triple = triples_R()
t2 = time.time()
print("\nLes triplés de réglage possibles ont été trouvés en ",t2-t1,"secondes")
print("Les triplés de réglages possibles sont :",triple)

N = len(triple)
total_time = N*22
heure = total_time//3600
minute = (total_time-3600*heure)//60
seconde = total_time - 3600*heure - 60*minute
print("\nLa recherche du tableau de connexion prendra jusqu'à",heure,"heures,",minute,"minutes et",seconde,"secondes")

betas = permR()

from itertools import product as produit


def egalite(alphas,betas,sigma):
    """
    Entree : une liste de permutation alphas (contenant alpha0,alpha1,alpha2), une liste de permutations betas (contenant beta0,beta1,beta2) et une permutation  sigma
    Sortie : True si pour tout i, sigma 'rond' alphai 'rond' sigma = betai, False sinon, cela test si sigma peut être la permutation du tableau de connexion
    """
    for i in range(len(betas)) :
        if composition(sigma,composition(alphas[i],sigma)).perm != betas[i].perm :
            return False
    return True

#test unitaire de la fonction egalite
def test_egalite() :
    """
    Le réglage du jour doit vérifier que sigma 'rond' alphai 'rond' sigma = betai pour tout i dans [0,1,2]
    """
    alphas,betas = permR_bis(daily_key[today]),permR()
    if not egalite(alphas,betas,daily_tableau[today]) :
        raise Exception("Les équations alpha/beta ne sont pas vérifiées")

def Sigma(alphas,betas) :
    """
    Entree : les permutation alphas et betas
    Sortie : la permutation du tableau de connexion du jour (sous format liste)
    """
    solutions = []
    for combi in produit(range(26),repeat = 4) : #toute les possibilités sur a,b,c,d,e
        sigma = identite(26)
        for i in range(4) :
            sigma.perm[i] = combi[i]
        for j in range(4) :
            for k in range(3) :
                a = j
                sa = combi[j]
                for l in range(13) :
                    b = betas[k].perm[sa]
                    sa = alphas[k].perm[a]
                    sigma.perm[b] = sa
                    sigma.perm[sa] = b
                    a = b
        if egalite(alphas,betas,sigma):
            solutions.append(sigma)
            break #on quitte la grande boucle si on a trouvé la solution
    if len(solutions) == 0 :
        return([])
    return(solutions[0].perm)

#test unitaire de la fonction Sigma
def test_Sigma() :
    """
    La fonction sigma trouve bien la bonne permutation
    """
    if Sigma(permR_bis(daily_key[today]),permR()) != daily_tableau[today].perm :
        raise Exception("le tableau de connexion renvoyé n'est pas le bon'")

#à décomenter si on veut faire un test unitaire global sur un mois entier attention, cela peut prendre quelques minutes
# for k in range(31) :
#     today = k
#     tabl=daily_tableau[today]
#     test_enigma()
#     test_triples_R()
#     test_egalite()
#     test_Sigma()
#today = datetime.datetime.now().day

t1 = time.time()
for T in tqdm(triple) :
    alphas = permR_bis(T)
    sol = Sigma(alphas, betas)
    if sol != [] :
        cle_du_jour = T
        connexion_du_jour = sol
        break
t2 = time.time()

print("\nLe câblage du tableau de connexion a été déterminé en ",t2-t1,"secondes\n")

print("\nla clé et la permutation du panneau de connexions du jours prédites sont :\n",cle_du_jour," et ",sol)
if cle_du_jour == daily_key[today] and connexion_du_jour == daily_tableau[today].perm :
    print("\nCe sont bien les réglages du jour !")
else :
    print("\nIl y a eu une erreur dans l'algorithme, essayez un autre jour'")

###On a donc établi un algorithme pour trouver les réglages initiaux de la machine enigma, voyons sa précision sur un mois entier

#Décommenter pour pouvoir voir la précision sur 1 mois ATTENTION CELA PEUT PRENDRE BEAUCOUP DE TEMPS (ex : jour 19)

# bonne_predi = 0
#
# for k in range(31) :
#     print("\n----------Jour",k,"---------\n")
#     today = k
#     tabl = daily_tableau[today]
#     print("Le réglage initial du jour est :\n",daily_key[today],"\nLe tableau de connexion du jour est : \n",tabl.perm,"\n")
#
#     t1 = time.time()
#     triple = triples_R()
#     t2 = time.time()
#     print("Les triplés de réglage possibles ont été trouvés en ",t2-t1," secondes")
#     print("Les triplés de réglages possibles sont :",triple)
#     betas = permR()
#     for T in tqdm(triple) :
#         alphas = permR_bis(T)
#         sol = Sigma(alphas, betas)
#         if sol != [] :
#             cle_du_jour = T
#             connexion_du_jour = sol
#             break
#     print("la clé et la permutation du panneau de connexions du jours prédites sont :\n",cle_du_jour," et ",sol)
#     if cle_du_jour == daily_key[today] and connexion_du_jour == daily_tableau[today].perm :
#         bonne_predi += 1
#
# print("Sur 31 jours, il y a eu ",bonne_predi," bonnes prédictions")

###On peut désormais décrypter n'importe quel message

from _string_ import clear as clearmsg

message = clearmsg(input("\nVeuillez rentrer le message à chiffrer (merci de ne pas mettre de chiffres, ils n'apparaîtront pas après chiffrage') :\n"),True,True)

cle = clearmsg(input("\nVeuillez rentrer la clé de réglage des rotors (rentrer 3 lettres) :\n"),True,True)

while len(cle) != 3 :
    cle = clearmsg(input("\nVeuillez rentrer la clé de réglage des rotors (rentrer 3 lettres) :\n"),True,True)

msg_crypte = enigma_user(message,cle)

print("\n Votre message crypté par enigma avec les réglages du jour et votre réglage rotor est :\n",msg_crypte)

print("\n Nous allons désormais tenter de retrouver votre message initial avec les réglages enigma prédits :\n")
cle_crypte = msg_crypte[:6]
dcle = enigma(cle_crypte,cle_du_jour,R1,R2,R3,refl,rotor(connexion_du_jour))

if dcle[:3] == cle :
    res = "juste"
else :
    res = "incorrect"

print("\n La clé utilisateur trouvée est '",dcle[:3],"' cette prédiction est",res)
dcle_int = [(ord(k)-97) for k in dcle[:3]]

msg_decrypte = enigma(msg_crypte[7:],dcle_int,R1,R2,R3,refl,rotor(connexion_du_jour))

if msg_decrypte == message.replace(" ","") :
    res = "juste"
else :
    res = "incorrect"


print("\n Le message initial trouvé (aux espaces près) est '",msg_decrypte,"' cette prédiction est",res)
