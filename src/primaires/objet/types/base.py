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


"""Ce fichier contient la classe BaseType, détaillée plus bas."""

from abstraits.id import ObjetID
from bases.collections.liste_id import ListeID
from primaires.format.description import Description
from primaires.objet.script import ScriptObjet
from . import MetaType

class BaseType(ObjetID, metaclass=MetaType):
    
    """Classe abstraite représentant le type de base d'un objet.
    
    Si des données doivent être communes à tous les types d'objet
    (un objet a un nom, une description, quelque soit son type) c'est dans
    cette classe qu'elles apparaissent.
    
    """
    
    groupe = "prototypes_objets"
    sous_rep = "objets/prototypes"
    nom_type = "" # à redéfinir
    nom_scripting = "l'objet"
    _nom = "base_type_objet"
    _version = 2
    
    # Types enfants
    types = {}
    def __init__(self, cle=""):
        """Constructeur d'un type"""
        ObjetID.__init__(self)
        self.cle = cle
        self._attributs = {}
        self.no = 0 # nombre d'objets créés sur ce prototype
        self.nom_singulier = "un objet indéfini"
        self.etat_singulier = "est posé là"
        self.nom_pluriel = "objets indéfinis"
        self.etat_pluriel = "sont posés là"
        self.noms_sup = []
        self.description = Description(parent=self)
        self.objets = ListeID(self)
        self.unique = True # par défaut tout objet est unique
        self._prix = 1 # valeur en magasin
        self.sans_prix = False
        self.poids_unitaire = 1 # 1 Kg
        
        # Equipement
        self.emplacement = ""
        self.epaisseur = 1
        self.positions = ()
        
        # Script
        self.script = ScriptObjet(self)
        self.etendre_script()
        
        # Editeur
        self._extensions_editeur = []
        
        # Erreur de validation du type
        self.err_type = "Le type de '{}' est invalide."
    
    def __getnewargs__(self):
        return ()
    
    def __str__(self):
        return self.cle
    
    def __getstate__(self):
        """Retourne le dictionnaire à enregistrer."""
        attrs = dict(ObjetID.__getstate__(self))
        del attrs["_extensions_editeur"]
        del attrs["_attributs"]
        return attrs
    
    def _get_prix(self):
        """Retourne le prix"""
        return self._prix
    def _set_prix(self, prix):
        """Modifie le prix"""
        self._prix = int(prix)
        self.enregistrer()
    prix = property(_get_prix, _set_prix)
    
    def etendre_script(self):
        """Méthode appelée pour étendre le scripting.
        
        Si une classe-fille la surcharge, elle peut ajouter des évènements
        au script de ce type d'objet, par exemple.
        
        """
        pass
    
    def etendre_editeur(self, raccourci, ligne, editeur, objet, attribut, *sup):
        """Permet d'étendre l'éditeur d'objet en fonction du type.
        
        Paramètres à entrer :
        -   raccourci   le raccourci permettant d'accéder à la ligne
        -   ligne       la ligne de l'éditeur (exemple 'Description')
        -   editeur     le contexte-éditeur (exemple Uniligne)
        -   objet       l'objet à éditer
        -   attribut    l'attribut à éditer    
        
        Cette méthode est appelée lors de la création de l'éditeur de
        prototype.
        
        """
        self._extensions_editeur.append(
            (raccourci, ligne, editeur, objet, attribut, sup))
    
    def reduire_editeur(self, raccourci):
        """Permet de supprimer un contexte-éditeur de la liste d'extensions."""
        sup = ()
        for editeur in self._extensions_editeur:
            if editeur[0] == raccourci:
                sup = editeur
                break
        if sup:
            self._extensions_editeur.remove(sup)
    
    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes.
        
        On récupère un dictionnaire représentant la présentation avec en
        clé les raccourcis et en valeur les enveloppes.
        
        Cela peut permettre de travailler sur les enveloppes ajoutées par
        'etendre_editeur'.
        
        """
        pass
    
    def get_nom(self, nombre=1):
        """Retourne le nom complet en fonction du nombre.
        
        Par exemple :
        Si nombre == 1 : retourne le nom singulier
        Sinon : retourne le nombre et le nom pluriel
        
        """
        if nombre <= 0:
            raise ValueError("la fonction get_nom a été appelée " \
                    "avec un nombre négatif ou nul.")
        elif nombre == 1:
            return self.nom_singulier
        else:
            if self.noms_sup:
                noms_sup = list(self.noms_sup)
                noms_sup.reverse()
                for nom in noms_sup:
                    if nombre >= nom[0]:
                        return nom[1]
            return str(nombre) + " " + self.nom_pluriel
    
    def get_nom_etat(self, nombre):
        """Retourne le nom et l'état en fonction du nombre."""
        nom = self.get_nom(nombre)
        if nombre == 1:
            return nom + " " + self.etat_singulier
        else:
            if self.noms_sup:
                noms_sup = list(self.noms_sup)
                noms_sup.reverse()
                for nom_sup in noms_sup:
                    if nombre >= nom_sup[0]:
                        return nom + " " + nom_sup[2]
            return nom + " " + self.etat_pluriel
    
    def est_de_type(self, nom_type):
        """Retourne True si le type d'objet est de celui entré ou dérivé.
        
        Par exemple, si on test si une épée est une arme, retournera True
        car le type 'arme' a pour classes-filles 'épée' (notamment).
        
        """
        classe = type(self).importeur.objet.types[nom_type]
        return isinstance(self, classe)
    
    @staticmethod
    def calculer_poids(objet):
        """Retourne le poids de l'objet."""
        return objet.poids_unitaire
    
    # Actions sur les objets
    def regarder(self, personnage):
        """Le personnage regarde l'objet"""
        salle = personnage.salle
        personnage << "Vous regardez {} :".format(self.nom_singulier)
        autre = "{{}} regarde {}.".format(self.nom_singulier)
        salle.envoyer(autre, personnage)
        
        # Appel du script regarde.avant
        self.script["regarde"]["avant"].executer(
                objet=self, personnage=personnage)
        
        description = str(self.description)
        if not description:
            description = "Il n'y a rien de bien intéressant à voir."
        
        personnage << "\n" + description
        
        # Appel du script regarde.après
        self.script["regarde"]["apres"].executer(
                objet=self, personnage=personnage)
        return ""

ObjetID.ajouter_groupe(BaseType)
