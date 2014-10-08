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


"""Ce fichier contient la classe NourritureVente, détaillée plus bas."""

from abstraits.obase import BaseObj
from corps.fonctions import lisser

class NourritureVente(BaseObj):

    """Cette classe enveloppe un conteneur de nourriture et de la nourriture.

    Elle simule certains comportements d'un objet standard afin de permettre
    la vente des deux en magasin via la syntaxe /s conteneur/n1+n2+n3 (voir
    l'éditeur de magasin du module salle).

    """

    type_achat = "nourriture"
    def __init__(self, proto_conteneur, liste_nourriture):
        """Constructeur de la classe"""
        BaseObj.__init__(self)
        self.conteneur = proto_conteneur
        self.nourriture = liste_nourriture
        self._construire()

    def __getnewargs__(self):
        return (None, [])

    def __repr__(self):
        return "<{} dans {}>".format(self.nourriture, self.conteneur.cle)

    def __str__(self):
        return self.conteneur.cle + "/" + "+".join(
                n.cle for n in self.nourriture)

    @property
    def cle(self):
        return self.conteneur.cle + "/" + "+".join(
                n.cle for n in self.nourriture)

    @property
    def m_valeur(self):
        return self.conteneur.prix + sum(n.prix for n in self.nourriture)

    @property
    def nom_achat(self):
        dico_qtt = {}
        for proto in self.nourriture:
            if proto not in dico_qtt:
                dico_qtt[proto] = 1
            else:
                dico_qtt[proto] += 1
        nourriture = [o.get_nom(nb) for o, nb in dico_qtt.items()]
        if len(nourriture) > 1:
            ajout = ", ".join(nourriture[:-1]) + " et " + nourriture[-1]
        else:
            ajout = nourriture[0]
        ajout = " (" + ajout + ")"
        return self.conteneur.nom_singulier + ajout

    def get_nom(self, nombre=1):
        """Retourne le nom complet en fonction du nombre.

        Par exemple :
        Si nombre == 1 : retourne le nom singulier
        Sinon : retourne le nombre et le nom pluriel

        """
        ajout = ""
        if self.nourriture is not None:
            dico_qtt = {}
            for proto in self.nourriture:
                if proto not in dico_qtt:
                    dico_qtt[proto] = 1
                else:
                    dico_qtt[proto] += 1
            nourriture = [o.get_nom(nb) for o, nb in dico_qtt.items()]
            if len(nourriture) > 1:
                ajout = ", ".join(nourriture[:-1]) + " et " + nourriture[-1]
            else:
                ajout = nourriture[0]
            ajout = " (" + ajout + ")"
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
            for item in self.nourriture:
                conteneur.nourriture.append(importeur.objet.creer_objet(item))
            salle.objets_sol.ajouter(conteneur)

    def regarder(self, personnage):
        """Le personnage regarde le service (avant achat)."""
        return self.conteneur.regarder(personnage)
