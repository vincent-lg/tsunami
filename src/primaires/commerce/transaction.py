# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant la classe Transaction, détaillée plus bas."""

class Transaction:
    
    """Cette classe représente une transaction entre deux acteurs.
    
    Certaines méthodes statiques sont utilisées sans créer de transaction :
        somme_argent(objets) -- retourne la somme totale
        get_argent(personnage) -- retourne les objets de type argent détenus
    
    D'autres méthodes nécessitent de créer une transaction. Pour
    créer une transaction, on n'utilise pas directement le constructeur
    mais la méthode initier_transaction.
    
    Les méthodes d'instances sont :
        prelever_argent_du() -- prélève l'argent dû à l'initiateur
    
    """
    
    def __init__(self):
        """Constructeur, à ne pas appeler directement."""
        self.initiateur = None # l'initiateur de la transaction
        self.receveur = None # le receveur de la transaction
        self.somme = 0
        self.argent_donne = {}
        self.argent_rendu = {}
    
    def __repr__(self):
        return "<transaction entre {} et {} pour {}>".format(
                self.initiateur, self.receveur, self.somme)
    
    @staticmethod
    def somme_argent(objets):
        """Retourne la somme de la valeur des objets.
        
        Le type attendu est un dictionnaire avec en clé l'objet (ou son
        prototype, indifféremment) et en valeur la quantité;
        
        """
        somme = 0
        for objet, qtt in objets.items():
            somme += objet.valeur * qtt
        
        return somme
    
    @staticmethod
    def get_argent(personnage):
        """Retourne tout l'argent détenu par le personnage.
        
        C'est un dictionnaire contenant tous les objets de type argent
        détenus par le personnage.
        
        """
        objets = personnage.equipement.inventaire_qtt
        objets = [(o, nb) for o, nb in objets if o.est_de_type("argent")]
        return dict(tuple(objets))
    
    @classmethod
    def initier(cls, initiateur, receveur, somme):
        """Initie une transaction.
        
        Les paramètres à préciser sont :
            initiateur -- l'acteur initiant la transaction
            receveur -- le receveur de la transaction
            somme -- la somme de la transaction
        
        Les acteurs ne sont pas nécessairement des personnages.
        Dans le cas où un personnage achète un objet, la transaction
        initiée l'est apr l'acheteur et le receveur est le magasin.
        
        """
        transaction = cls()
        transaction.initiateur = initiateur
        transaction.receveur = receveur
        transaction.somme = somme
        
        # On calcul l'argent dû et à rendre
        # Dans un cas simple, si on achète un produit à 1€ avec un billet de
        # 10€, l'argent donné est 10€ et l'argent rendu est 9€,
        # probablement décomposé en 9 pièces de 1€.
        argent_dct = Transaction.get_argent(initiateur)
        somme_ini = Transaction.somme_argent(argent_dct)
        if somme_ini < somme:
            raise ValueError("la somme d'argent de l'initiateur ({}) est " \
                    "insuffisante pour cette transaction".format(somme_ini))
        
        # On trie la monnaie 
        argent_tt = sorted(tuple(argent_dct.items()),
                key=lambda t: t[0].valeur, reverse=True)
        print(argent_tt)
        argent_donne = []
        argent_rendu = []
        
        # On décompose la somme en fonction des valeurs
        t_somme = somme
        for argent, qtt in argent_tt:
            if t_somme == 0:
                break
            
            d_somme = t_somme // argent.valeur
            if d_somme > 0:
                if qtt > d_somme:
                    qtt = d_somme
                elif qtt < d_somme:
                    continue
                
                argent_donne.append((argent, qtt))
                t_somme -= qtt * argent.valeur
        
        print(argent_donne)
        # Après cette opération, la somme peut être incomplète
        # La boucle précédente ne réunit que la somme exacte
        # On cherche maintenant une somme supérieure si besoin
        print(t_somme)
        if t_somme > 0:
            for i, (argent, qtt) in enumerate(list(argent_donne)):
                if t_somme == 0:
                    break
                
                j = 0
                t_qtt = argent_dct[argent]
                while j < t_qtt and t_somme > 0:
                    argent_donne[i] = (argent_donne[i][0],
                            argent_donne[i][1] + 1)
                    t_somme -= argent.valeur
                    j += 1
        
        print(argent_donne)
        # On s'occupe de rendre l'argent
        somme_donnee = Transaction.somme_argent(dict(argent_donne))
        if somme_donnee > somme:
            monnaies = sorted([p for p in \
                    importeur.objet.prototypes.values() if p.est_de_type(
                    "argent")], reverse=True)
            t_somme = somme_donnee - somme
            for monnaie in monnaies:
                if t_somme == 0:
                    break
                
                d_somme = t_somme // monnaie.valeur
                if d_somme > 0:
                    argent_rendu.append((monnaie, d_somme))
                    t_somme -= d_somme * monnaie.valeur
        
        somme_rendue = Transaction.somme_argent(dict(argent_rendu))
        if somme != somme_donnee - somme_rendue:
            raise ValueError("la somme attendue ({}) n'est pas égale " \
                    "à la somme donnée ({}) moins la somme rendue ({})".format(
                    somme, somme_donnee, somme_rendue))
        
        self.argent_donne = dict(argent_donne)
        self.argent_rendu = dict(argent_rendu)
        
        return transaction
