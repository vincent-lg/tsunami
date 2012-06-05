# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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

"""Ce fichier contient la classe Equipement, détaillée plus bas."""

from abstraits.obase import *
from primaires.format.fonctions import supprimer_accents
from primaires.objet.conteneur import SurPoids
from .membre import Membre

class Equipement(BaseObj):
    
    """Equipement d'un personnage.
    
    """
    
    def __init__(self, personnage, squelette):
        """Constructeur de l'équipement.
        -   personnage  Le personnage dont ce sera l'équipement
        -   squelette   Le squelette servant de base aux membres copiés
        
        """
        BaseObj.__init__(self)
        self.personnage = personnage
        self.squelette = squelette
        self.__membres = []
        self.equipes = Equipes(self)
        self.tenus = Tenus(self)
        
        if squelette:
            squelette.personnages.append(personnage)
            # Construction des membres copiés depuis le squelette
            for membre in squelette.membres:
                self.__membres.append(Membre(membre.nom, modele=membre,
                        parent=personnage))
    
    def __getnewargs__(self):
        return (None, None)
    
    @property
    def membres(self):
        """Retourne une liste déréférencée des membres"""
        return list(self.__membres)
    
    @property
    def inventaire(self):
        """Retourne la liste des objets tenus.
        
        Il s'agit d'un inventaire, car les objets sont aussi ceux contenus
        dans les conteneurs équipés / tenus.
        
        Pour connaître le conteneur contenant l'objet, on se reporte à
        objet.contenu.
        
        """
        return Inventaire(self, simple=False)
    
    @property
    def inventaire_simple(self):
        """Retourne l'inventaire simple, c'est-à-dire sans les objets équipés.
        
        Attention cependant : cette méthode retourne les objets contenus
        dans un conteneur équipés. Si par exemple l'équipement contient un
        sac à dos, le sac à dos lui-même ne figurera pas dans la liste,
        en revanche son contenu y figurera.
        
        """
        return Inventaire(self, simple=True)
    
    @property
    def inventaire_qtt(self):
        """Retourne l'inventaire (objet, quantité)."""
        return Inventaire(self, simple=False).iter_objets_qtt()
    
    @property
    def poids(self):
        """Retourne le poids de tous les objets tenus ou équipés."""
        poids = 0
        for membre in self.membres:
            objets = list(membre.equipe) + [membre.tenu]
            objets = [o for o in objets if o is not None]
            for o in objets:
                poids += o.poids
        
        return round(poids, 3)
    
    def get_membre(self, nom_membre):
        """Récupère le membre dont le nom est nom_membre.
        
        On peut très bien passer par self.membres[nom_membre], la méthode
        courante a simplement l'avantage d'afficher une erreur explicite
        en cas de problème.
        
        """
        nom = supprimer_accents(nom_membre)
        noms = [(supprimer_accents(membre.nom), i) for i, membre in \
                enumerate(self.__membres)]
        noms = dict(noms)
        
        try:
            membre = self.__membres[noms[nom]]
        except KeyError:
            raise KeyError("le membre {} est introuvable dans " \
                    "l'équipement de {}".format(nom_membre, self.personnage))
        
        return membre
    
    def ajouter_membre(self, membre):
        """Ajoute un nouveau membre en se servant de "membre" comme modèle"""
        membre = Membre(membre.nom, modele=membre, parent=self.personnage)
        self.__membres.append(membre)
    
    def supprimer_membre(self, nom):
        """Supprime le membre de nom nom"""
        nom = supprimer_accents(nom).lower()
        noms = [(supprimer_accents(membre.nom).lower(), i) for i, membre in \
                enumerate(self.__membres)]
        noms = dict(noms)
        
        try:
            membre = self.__membres[noms[nom]]
        except KeyError:
            raise KeyError("le membre {} est introuvable dans " \
                    "l'équipement de {}".format(nom, self.personnage))
        del self.__membres[noms[nom]]
    
    def membre_est_equipe(self, nom_membre):
        """Retourne True si le membre est équipé, False sinon.
        
        Un membre est équipé si son attribut objet n'est pas None.
        Si le membre ne peut être trouvé dans l'équipement, une exception est
        levée.
        
        """
        membre = self.get_membre(nom_membre)
        return membre.equipe is not None
    
    def equiper_objet(self, nom_membre, objet):
        """Equipe le membre nom_membre avec l'objet.
        
        Si le membre possède un objet, une exception est levée.
        
        """
        membre = self.get_membre(nom_membre)
        if objet is None:
            raise ValueError("l'objet passé en paramètre est None. Pour " \
                    "retirer un objet équipé, utilisez la méthode " \
                    "desequiper_objet")
        
        membre.equipe.append(objet)
        objet.contenu = self.equipes
    
    def desequiper_objet(self, nom_membre):
        """Retire un objet de l'équipement.
        
        """
        membre = self.get_membre(nom_membre)
        membre.equipe.pop(-1)
    
    def tenir_objet(self, nom_membre=None, objet=None):
        """Fait tenir l'objet objet au membre nom_membre. """
        if nom_membre:
            membre = self.get_membre(nom_membre)
        else:
            membre = None
            for m in self.membres:
                if m.tenu is None and m.peut_tenir():
                    membre = m
                    break
            
            if membre is None:
                raise ValueError("aucun membre n'est disponible")
        
        if membre.tenu:
            raise ValueError("le membre {} tient déjà l'objet {} ".format(
                    nom_membre, membre.tenu))
        
        if objet is None:
            raise ValueError("l'objet passé en paramètre est None. Pour " \
                   "retirer un objet tenu, utilisez la méthode retirer_objet")
        
        membre.tenu = objet
        objet.contenu = self.tenus
    
    def retirer_objet(self, nom_membre):
        """Retire l'objet tenu sur nom_membre."""
        membre = self.get_membre(nom_membre)
        objet = membre.tenu
        membre.tenu = None
    
    def remonter_membre(self, nom_membre):
        """Remonte un membre dans la liste des membres."""
        membre = self.get_membre(nom_membre)
        indice = self.__membres.index(membre)
        if indice != 0: # ne fait rien si le membre est déjà tout en haut
            membre = self.__membres.pop(indice)
            self.__membres.insert(indice - 1, membre)
    
    def descendre_membre(self, nom_membre):
        """Descend un membre dans la liste des membres."""
        membre = self.get_membre(nom_membre)
        indice = self.__membres.index(membre)
        if indice != len(self.__membres) - 1: # si le membre n'est pas en bas
            membre = self.__membres.pop(indice)
            self.__membres.insert(indice + 1, membre)
    
    def cb_peut_tenir(self):
        """Retourne le nombre de membres pouvant tenir quelque chose."""
        nb = 0
        for membre in self.membres:
            if membre.tenu is None and membre.peut_tenir():
                nb += 1
        
        return nb
    
    def supporter_poids_sup(self, poids, recursif=True):
        """Méthode vérifiant que le conteneur peut contenir le poids.
        
        Ici, on vérifie que le personnage peut porter davantage.
        
        """
        poids_max = self.personnage.poids_max
        poids_actuel = self.poids
        if poids_actuel + poids > poids_max:
            raise SurPoids("Vous ne pouvez porter davantage.")
        
        return True


class Equipes(BaseObj):
    
    """Classe se comportantt comme un objet conteneur.
    
    Elle contient les objets équipés.
    
    """
    
    def __init__(self, equipement):
        """Constructeur du conteneur"""
        BaseObj.__init__(self)
        self.equipement = equipement
    
    def __getnewargs__(self):
        return (None, )

    def __iter__(self):
        """Retourne une chaîne des objets équipés."""
        objets = tuple(tuple(o.equipe) for o in self.equipement.membres)
        ret = []
        for l in objets:
            for objet in l:
                ret.append(objet)
        
        return iter(ret)
    
    @property
    def grand_parent(self):
        return self.equipement.personnage
    
    def ajouter(self, objet, nombre=1):
        """Ajoute un objet à l'équipoement"""
        raise NotImplementedError
    
    def retirer(self, objet, qtt=1):
        """Retire l'objet passé en paramètre"""
        for membre in self.equipement.membres:
            if membre.equipe and membre.equipe[-1] == objet:
                self.equipement.desequiper_objet(membre.nom)
                return
        
        raise ValueError("l'objet {} n'a pu être trouvé dans cet " \
                "équipement".format(objet.cle))
    
    def supporter_poids_sup(self, poids, recursif=True):
        """Supporte le poids supplémentaire spécifiée.
        
        Redirige sur l'équipement.
        
        """
        return self.equipement.supporter_poids_sup(poids, recursif)

class Tenus(BaseObj):
    
    """Classe se comportant comme un objet conteneur.
    
    Elle contient les objets tenus.
    
    """
    
    def __init__(self, equipement):
        """Constructeur du conteneur"""
        BaseObj.__init__(self)
        self.equipement = equipement
    
    def __getnewargs__(self):
        return (None, )

    def __iter__(self):
        return iter([membre.tenu for membre in self.equipement.membres \
                if membre.tenu])
    
    @property
    def grand_parent(self):
        return self.equipement.personnage
    
    def iter_nombres(self):
        objets = list(iter(self))
        qtts = [1] * len(objets)
        return iter(list(zip(objets, qtts)))
    
    def ajouter(self, objet, nombre=1):
        """Ajoute un objet à l'équipoement"""
        raise NotImplementedError
    
    def retirer(self, objet, qtt=1):
        """Retire l'objet passé en paramètre"""
        for membre in self.equipement.membres:
            if membre.tenu is objet:
                self.equipement.retirer_objet(membre.nom)
                return
        
        raise ValueError("l'objet {} n'est pas tenu".format(
                self.objet.cle))
    
    def supporter_poids_sup(self, poids, recursif=True):
        """Supporte le poids supplémentaire spécifiée.
        
        Redirige sur l'équipement.
        
        """
        return self.equipement.supporter_poids_sup(poids, recursif)

class Inventaire:
    
    """Classe représentant un inventaire, un objet temporaire.
    
    Celui-ci contient les objets équipés et leurs contenants.
    Si l'inventaire est dit simple, il ne contiendra que le contenu
    des objets équipés, pas les objets équipés eux-mêmes.
    
    """
    
    def __init__(self, equipement, simple=False):
        """Constructeur de l'inventaire."""
        self.equipement = equipement
        self.simple = simple
        self.objets = []
        self.contenu_dans = {}
        self.quantite = {}
        self.get_objets(simple)
    
    def __iter__(self):
        """Parcourt des objets."""
        return iter(self.objets)
    
    def get_objets(self, simple=False):
        """Récupère les objets de l'inventaire."""
        res = []
        quantite = {}
        contenu_dans = {}
        for membre in self.equipement.membres:
            objets = list(membre.equipe)
            objets = [o for o in objets if o is not None]
            for objet in objets:
                objets = objet.extraire_contenus(quantite, contenu_dans)
                if simple:
                    del objets[0]
                res.extend(objets)
            
            if membre.tenu:
                objets = membre.tenu.extraire_contenus(quantite, contenu_dans)
                res.extend(objets)
        
        self.objets = res
        self.contenu_dans = contenu_dans
        self.quantite = quantite
    
    def iter_objets_qtt(self, conteneur=False):
        """Retourne une liste de tuples (objet, qtt, conteneur).
        
        Si conteneur est à False (par défaut), le tuple ne sera que de
        deux éléments (objet, qtt).
        
        """
        for objet in self.objets:
            qtt = self.quantite[objet]
            if conteneur:
                t_conteneur = self.contenu_dans[objet]
                if hasattr(t_conteneur, "conteneur"):
                    t_conteneur = t_conteneur.conteneur
                
                yield (objet, qtt, t_conteneur)
            else:
                yield (objet, qtt)
