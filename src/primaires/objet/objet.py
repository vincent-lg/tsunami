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


"""Ce fichier contient la classe Objet, détaillée plus bas."""

from datetime import datetime

from abstraits.obase import BaseObj

class Objet(BaseObj):

    """Cette classe contient un Objet issu d'un prototype.

    Pour rappel, un prototype définit une suite d'action propre au type de
    l'objet, ainsi que des attributs génériques. Les administrateurs en
    charge de l'univers créent des prototypes et sur ce prototype (qui est
    une sorte de modèle), des objets sont créés.
    L'objet peut avoir des attributs se distinguant du prototype mais
    conserve une référence vers son prototype.

    Petite subtilité : la méthode __getattr__ a été redéfinie pour qu'il
    ne soit pas nécessaire de faire :
    >>> self.prototype.nom
    pour accéder au nom de l'objet.
    >>> self.nom
    suffit. La méthode va automatiquement chercher l'attribut dans
    'self.prototype' si l'attribut n'existe pas. Cela veut dire que si
    vous faites :
    >>> self.nom = "un autre nom"
    vous modifiez le nom de l'objet, sans modifier le prototype
    (le prototype ne doit pas être modifié depuis l'objet). Le nom de
    l'objet changera donc et sera différent de celui du prototype, le
    temps de la durée de vie de l'objet. Pour que :
    >>> self.nom
    fasse de nouveau référence au nom du prototype, il est conseillé de
    supprimer le nom de l'objet :
    >>> del self.nom
    Ce mécanisme permet une assez grande flexibilité. Si par exemple vous
    modifiez la description du prototype, tous les objets créés sur ce
    prototype, (ceux créés comme ceux prochainement créés), seront affectés
    par ce changement, sauf si ils définissent une description propre.

    """

    enregistrer = True
    def __init__(self, prototype):
        """Constructeur de l'objet"""
        BaseObj.__init__(self)
        self.prototype = prototype
        self.contenu = None # contenu dans
        self.ajoute_a = datetime.now()
        if prototype:
            self.identifiant = prototype.cle + "_" + str(
                    prototype.no)
            prototype.no += 1
            prototype.objets.append(self)

            # On copie les attributs propres à l'objet
            # Ils sont disponibles dans le prototype, dans la variable
            # _attributs
            # C'est un dictionnaire contenant en clé le nom de l'attribut
            # et en valeur le constructeur de l'objet
            for nom, val in prototype._attributs.items():
                setattr(self, nom, val.construire(self))

    def __getnewargs__(self):
        return (None, )

    def __getattr__(self, nom_attr):
        """Si le nom d'attribut n'est pas trouvé, le chercher
        dans le prototype

        - D'abord on cherche dans la classe
          Si trouvé et que c'est une méthode d'objet on lui passe en
          paramètre l'objet au lieu du prototype
        - Sinon on regarde dans le prorotype.

        """
        try:
            attribut = getattr(type(self.prototype), nom_attr)
            assert callable(attribut)
            return MethodeObjet(attribut, self)
        except (AttributeError, AssertionError) as err:
            return getattr(self.prototype, nom_attr)

    def __repr__(self):
        return "<objet {}>".format(self.identifiant)

    def __str__(self):
        return self.nom_singulier

    def __iter__(self):
        """Parcourt les objets contenus."""
        return iter(self.conteneur)

    @property
    def poids(self):
        """Retourne le poids total.

        Ce peut être :
        *   Le point unitaire pour un objet standard
        *   Le poids unitaire plus le poids de tous les objets
            contenus pour un conteneur.

        """
        return self.calculer_poids()

    @property
    def grand_parent(self):
        """Retourne le grand parent de l'objet."""
        if hasattr(self.contenu, "grand_parent"):
            return self.contenu.grand_parent
        else:
            return self.contenu

    @property
    def str_grand_parent(self):
        """Retourne une chaîne représentant le grand parent."""
        parent = self.grand_parent
        if parent is None:
            return "aucun"
        else:
            return parent.nom_unique

    def extraire_contenus(self, quantite=None, contenu_dans=None):
        """Extrait les objets contenus."""
        res = [self]
        if quantite is not None:
            quantite[self] = 1
        if contenu_dans is not None:
            contenu_dans[self] = self.contenu

        if hasattr(self, "conteneur"):
            for objet in self.conteneur:
                if objet.prototype.unique:
                    res.extend(objet.extraire_contenus(quantite, contenu_dans))
                else:
                    res.append(objet.prototype)
                    if quantite is not None:
                        if objet.prototype in quantite:
                            quantite[objet.prototype] += objet.nombre
                        else:
                            quantite[objet.prototype] = objet.nombre
                    if contenu_dans is not None:
                        contenu_dans[objet.prototype] = self

        return res

    def extraire_contenus_qtt(self):
        """Extrait les objets contenus."""
        res = [(self, 1)]
        if hasattr(self, "conteneur"):
            for objet in self.conteneur._objets:
                res.extend(objet.extraire_contenus_qtt())
            for objet in self.conteneur._non_uniques:
                res.append((objet.prototype, objet.nombre))

        return res

    def detruire(self):
        """Destruction de l'objet"""
        if self in self.prototype.objets:
            self.prototype.objets.remove(self)

        if self.contenu and self in self.contenu:
            self.contenu.retirer(self)

        self.prototype.detruire_objet(self)
        BaseObj.detruire(self)

class MethodeObjet:

    """Classe enveloppant une méthode d'objet."""

    def __init__(self, methode, objet):
        self.methode = methode
        self.objet = objet

    def __call__(self, *args, **kwargs):
        return self.methode(self.objet, *args, **kwargs)
