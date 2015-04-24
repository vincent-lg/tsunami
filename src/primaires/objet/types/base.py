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

from fractions import Fraction

from abstraits.obase import BaseObj
from primaires.format.description import Description
from primaires.objet.script import ScriptObjet
from . import MetaType

# Constantes
FLAGS = {
    "ne peut pas prendre": 1,
}

class BaseType(BaseObj, metaclass=MetaType):

    """Classe abstraite représentant le type de base d'un objet.

    Si des données doivent être communes à tous les types d'objet
    (un objet a un nom, une description, quelque soit son type) c'est dans
    cette classe qu'elles apparaissent.

    Notons les attributs d'objet :
        empilable_sur -- une liste de chaînes définissant les types
                         sur lesquels on peut empiler le type d'objet
        empilable_sous -- une liste de chaînes identiques mais
                          désignant les types d'objets qui peuvent être
                          empilés par-dessus le type défini. On évitera
                          d'utiliser cet attribut sauf si le type
                          d'objet est défini dans un module secondaire

    """

    nom_type = "" # à redéfinir
    nom_scripting = "l'objet"
    type_achat = "objet"
    _nom = "base_type_objet"
    _version = 3

    # Doit-t-on nettoyer l'objet en cas d'inactivité
    nettoyer = True

    # Type d'objet sélectable dans le oedit
    selectable = True

    # Types enfants
    types = {}
    enregistrer = True

    # Équipement
    empilable_sur = []
    empilable_sous = []

    def __init__(self, cle=""):
        """Constructeur d'un type"""
        BaseObj.__init__(self)
        self.cle = cle
        self._attributs = {}
        self.no = 0 # nombre d'objets créés sur ce prototype
        self.nom_singulier = "un objet indéfini"
        self.etat_singulier = "est posé là"
        self.nom_pluriel = "objets indéfinis"
        self.etat_pluriel = "sont posés là"
        self.noms_sup = []
        self.description = Description(parent=self)
        self.objets = []
        self.unique = True # par défaut tout objet est unique
        self.flags = 0
        self._prix = 1 # valeur en magasin
        self.sans_prix = False
        self.poids_unitaire = 1 # 1 Kg
        self.depecer_de = []

        # Equipement
        self.peut_prendre = True # définit si on peut manipuler l'objet à main
        self.peut_tenir = False # définit si on peut tenir un objet par-dessus
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

        self._construire()

    def __getnewargs__(self):
        return ()

    def __repr__(self):
        return "<{} {}>".format(self.nom_type, self.cle)

    def __str__(self):
        return self.cle

    def __getstate__(self):
        """Retourne le dictionnaire à enregistrer."""
        attrs = self.__dict__.copy()
        if "_extensions_editeur" in attrs:
            del attrs["_extensions_editeur"]
        if "_attributs" in attrs:
            del attrs["_attributs"]
        return attrs

    def _get_prix(self):
        """Retourne le prix"""
        return self._prix
    def _set_prix(self, prix):
        """Modifie le prix"""
        self._prix = int(prix)
    prix = property(_get_prix, _set_prix)

    @property
    def m_valeur(self):
        return self._prix

    @property
    def nom_achat(self):
        return self.nom_singulier

    @property
    def poids(self):
        """Retourne le poids unitaire."""
        return self.poids_unitaire

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

    def get_nom(self, nombre=1, pluriels=True):
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
            if pluriels and self.noms_sup:
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

    def extraire_contenus(self, quantite=None, contenu_dans=None):
        """Méthode redéfinie pour la manipulation d'objets non uniques."""
        return [self]

    def extraire_contenus_qtt(self):
        """Méthode redéfinie pour la manipulation d'objets non uniques."""
        return [(self, 1)]

    def est_de_type(self, nom_type):
        """Retourne True si le type d'objet est de celui entré ou dérivé.

        Par exemple, si on test si une épée est une arme, retournera True
        car le type 'arme' a pour classes-filles 'épée' (notamment).

        """
        classe = importeur.objet.types[nom_type]
        prototype = hasattr(self, "prototype") and self.prototype or self
        return isinstance(prototype, classe)

    def calculer_poids(self):
        """Retourne le poids de l'objet."""
        return self.poids_unitaire

    def objets_contenus(self, objet):
        """Retourne les objets contenus."""
        return []

    def detruire_objet(self, objet):
        """Détruit l'objet passé en paramètre.

        Par défaut cette méthode ne fait rien, mais si le type
        est fait pour contenir d'autres objets, il doit les détruire.

        """
        pass

    # Actions sur les objets
    def acheter(self, quantite, magasin, transaction):
        """Achète les objets dans la quantité spécifiée."""
        salle = magasin.parent
        objets = []
        for i in range(quantite):
            objet = importeur.objet.creer_objet(self)
            salle.objets_sol.ajouter(objet)
            objets.append(objet)

        return objets

    def peut_vendre(self, vendeur):
        """Retourne True si peut vendre l'objet."""
        return True

    def estimer_valeur(self, magasin, vendeur):
        """Estime la valeur d'un objet."""
        valeur = self.m_valeur
        return valeur * 0.7

    def regarder(self, personnage, variables=None):
        """Le personnage regarde l'objet"""
        salle = personnage.salle
        variables = variables or {}
        personnage << "Vous regardez {} :".format(self.get_nom())
        autre = "{{}} regarde {}.".format(self.get_nom())
        salle.envoyer(autre, personnage)

        # Appel du script regarde.avant
        self.script["regarde"]["avant"].executer(
                objet=self, personnage=personnage)

        description = self.description.regarder(personnage, self, variables)
        if not description:
            description = "Il n'y a rien de bien intéressant à voir."

        personnage << description

        # Appel du script regarde.après
        self.script["regarde"]["apres"].executer(
                objet=self, personnage=personnage)
        return ""

    def veut_jeter(self, personnage, sur):
        """Méthode appelée pour tester si le personnage peut jeter l'objet.

        On doit préciser :
            personnage -- le personnage voulant jeter l'objet
            sur -- sur quoi veut-il jeter l'objet ?

        Le dernier paramètre peut être n'importe quel élément observable
        (un autre objet, un autre personnage...).

        La méthode doit retourner :
            Une chaîne vide si l'objet ne peut pas être lancé
            Un nom de méthode à appeler si l'objet peut être lancé

        """
        return ""

    def jeter(self, personnage, sur):
        """Jète self sur sur.

        Les paramètres sont les mêmes que veut_jeter.

        On retourne :
            True si on a pu jeter l'objet
            False sinon

        """
        return False

    def poser(self, objet, personnage, qtt=1):
        """L'objet est posé."""
        objet.script["pose"].executer(objet=objet, personnage=personnage,
                quantite=Fraction(qtt))

    def detruire(self):
        """Destruction du prototype d'objet."""
        # Destruction des objets à dépecer
        for proto in self.depecer_de:
            if self in proto.a_depecer:
                del proto.a_depecer[self]

        BaseObj.detruire(self)

    def nettoyage_cyclique(self):
        """Nettoyage cyclique de l'objet si besoin."""
        pass
