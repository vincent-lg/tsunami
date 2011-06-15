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
        """Retourne un dictionnaire déréférencé des membres"""
        return list(self.__membres)
    
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
        nom = supprimer_accents(nom_membre)
        noms = [(supprimer_accents(membre.nom), i) for i, membre in \
                enumerate(self.__membres)]
        noms = dict(noms)
        
        try:
            membre = self.__membres[noms[nom]]
        except KeyError:
            raise KeyError("le membre {} est introuvable dans " \
                    "l'équipement de {}".format(nom_membre, self.personnage))
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
        if membre.equipe:
            raise ValueError("le membre {} possède déjà l'objet {} " \
                    "équipé".format(nom_membre, membre.equipe))
        
        if objet is None:
            raise ValueError("l'objet passé en paramètre est None. Pour " \
                    "retirer un objet équipé, utilisez la méthode " \
                    "desequiper_objet")
        
        membre.equipe = objet
    
    def desequiper_objet(self, nom_membre):
        """Retire un objet de l'équipement.
        
        """
        membre = self.get_membre(nom_membre)
        membre.objet = None
    
    def tenir_objet(self, nom_membre, objet):
        """Fait tenir l'objet objet au membre nom_membre. """
        membre = self.get_membre(nom_membre)
        if membre.tenu:
            raise ValueError("le membre {} tient déjà l'objet {} ".format(
                    nom_membre, membre.tenu))
        
        if objet is None:
            raise ValueError("l'objet passé en paramètre est None. Pour " \
                   "retirer un objet tenu, utilisez la méthode retirer_objet")
        
        membre.tenu = objet
    
    def retirer_objet(self, nom_membre):
        """Retire l'objet tenu sur nom_membre."""
        membre = self.get_membre(nom_membre)
        membre.tenu = None

class Equipes(BaseObj):
    
    """Classe se comportement comme un objet conteneur, contenant
    les objets équipés.
    
    """
    
    def __init__(self, equipement):
        """Constructeur du conteneur"""
        BaseObj.__init__(self)
        self.equipement = equipement
    
    def __getnewargs__(self):
        return (None, )

    def __iter__(self):
        return iter([membre.equipe for membre in self.equipement.membres \
                if membre.equipe])
    
    def ajouter(self, objet):
        """Ajoute un objet à l'équipoement"""
        raise NotImplementedError
    
    def retirer(self, objet):
        """Retire l'objet passé en paramètre"""
        for membre in self.equipement.membres:
            if membre.equipe is objet:
                self.equipement.desequiper_objet(membre.nom)

class Tenus(BaseObj):
    
    """Classe se comportant comme un objet conteneur, contenant
    les objets tenus.
    
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
    
    def ajouter(self, objet):
        """Ajoute un objet à l'équipoement"""
        raise NotImplementedError
    
    def retirer(self, objet):
        """Retire l'objet passé en paramètre"""
        for membre in self.equipement.membres:
            if membre.tenu is objet:
                self.equipement.retirer_objet(membre.nom)
