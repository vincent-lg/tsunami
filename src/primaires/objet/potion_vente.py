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


"""Ce fichier contient la classe PotionVente, détaillée plus bas."""

from abstraits.obase import BaseObj
from corps.fonctions import lisser

class PotionVente(BaseObj):

    """Cette classe enveloppe un conteneur de potion et une potion.

    Elle simule certains comportements d'un objet standard afin de permettre
    la vente des deux en magasin via la syntaxe /s conteneur/potion (voir
    l'éditeur de magasin du module salle).

    """

    type_achat = "potion"
    def __init__(self, proto_conteneur, proto_potion):
        """Constructeur de la classe"""
        BaseObj.__init__(self)
        self.conteneur = proto_conteneur
        self.potion = proto_potion

    def __getnewargs__(self):
        return (None, None)

    def __repr__(self):
        return "<{} dans {}>".format(self.potion.cle, self.conteneur.cle)

    def __str__(self):
        return self.conteneur.cle + "/" + self.potion.cle

    @property
    def cle(self):
        return self.conteneur.cle + "/" + self.potion.cle

    @property
    def m_valeur(self):
        return self.conteneur.prix + self.potion.prix

    @property
    def nom_achat(self):
        if self.potion == "eau":
            nom = "eau"
        else:
            nom = self.potion.nom_singulier
        ajout = lisser(
                " " + self.conteneur.connecteur.format(s="") + " " + nom)
        return self.conteneur.nom_singulier + ajout

    def get_nom(self, nombre=1):
        """Retourne le nom complet en fonction du nombre.

        Par exemple :
        Si nombre == 1 : retourne le nom singulier
        Sinon : retourne le nombre et le nom pluriel

        """
        ajout = ""
        if self.potion is not None:
            s = "s" if nombre > 1 else ""
            if self.potion == "eau":
                nom = "eau"
            else:
                nom = self.potion.get_nom()
            ajout = lisser(
                    " " + self.conteneur.connecteur.format(s=s) + " " + nom)
        if nombre <= 0:
            raise ValueError("la fonction get_nom a été appelée " \
                    "avec un nombre négatif ou nul.")
        elif nombre == 1:
            return self.conteneur.nom_singulier + ajout
        else:
            if self.conteneur.noms_sup:
                noms_sup = list(self.conteneur.noms_sup)
                noms_sup.reverse()
                for nom in noms_sup:
                    if nombre >= nom[0]:
                        return nom[1] + ajout
            return str(nombre) + " " + self.conteneur.nom_pluriel + ajout

    def acheter(self, quantite, magasin, transaction):
        """Achète les objets dans la quantité spécifiée."""
        salle = magasin.parent
        for i in range(quantite):
            conteneur = importeur.objet.creer_objet(self.conteneur)
            conteneur.potion = importeur.objet.creer_objet(self.potion)
            salle.objets_sol.ajouter(conteneur)

    def regarder(self, personnage):
        """Le personnage regarde le service (avant achat)."""
        msg = self.conteneur.regarder(personnage) + "\n"
        msg += self.potion.regarder(personnage)
        return msg
