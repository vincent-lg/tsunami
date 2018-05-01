# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Fichier définissant la classe MotCle, détaillée plus bas."""

from primaires.format.fonctions import supprimer_accents
from primaires.interpreteur.commande.commande import Commande
from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *

class MotCle(Commande):

    """Un mot-clé est un masque simple.

    Il se compose de deux mots-clés en fonction de la langue utilisée :
    -   un en anglais ;
    -   un en français.

    """

    def __init__(self, francais, anglais):
        """Constructeur du mot-clé"""
        Masque.__init__(self)
        self.francais = francais
        self.anglais = anglais
        self.nom = francais
        self.gauche = False

    def __str__(self):
        """Fonction d'affichage"""
        return self.francais + "/" + self.anglais

    @property
    def nom_francais(self):
        return self.francais

    def init(self):
        """On ne fait rien."""
        pass

    def repartir(self, personnage, masques, commande):
        """Répartition du masque.

        Si la commande est vide, on va la chercher dans le dernier masque
        réparti.

        """
        langue = personnage.langue_cmd
        anglais, francais = self.anglais, self.francais
        if langue == "anglais":
            mot_cle = anglais
        elif langue == "francais":
            mot_cle = supprimer_accents(francais)
        else:
            raise ValueError("langue {} inconnue".format(langue))

        if not commande:
            # Le paramètre peut se trouver dans le masque précédent
            masque = masques[-1]
            commande[:] = chaine_vers_liste(masque.a_interpreter)
            str_commande = liste_vers_chaine(commande)
            sa_commande = supprimer_accents(str_commande).lower()
            mot_cle = " " + mot_cle + " "
            if mot_cle in sa_commande:
                if self.gauche:
                    fin = sa_commande.index(mot_cle)
                else:
                    fin = sa_commande.rindex(mot_cle)

                masque.a_interpreter = str_commande[:fin]
                fin += len(mot_cle)
                commande[:] = commande[fin:]
                valide = True
            else:
                valide = False
        else:
            str_commande = liste_vers_chaine(commande)
            sa_commande = supprimer_accents(str_commande).lower()

            if sa_commande.startswith(mot_cle) or \
                    sa_commande.startswith(" " + mot_cle):
                plus = 0
                if sa_commande.startswith(" "):
                    plus = 1

                commande[:] = commande[len(mot_cle) + plus:]
                valide = True
            else:
                valide = False

        if valide:
            masques.append(self)

        return valide

    def valider(self, personnage, dic_masques):
        """Fonction de validation du masque mot-clé.

        Un mot-clé a été validé lors de la répartition ; il est donc
        automatiquement validé.

        """
        return True

    def est_parametre(self):
        """Retourne False puisque c'est un mot-clé."""
        return False

    def est_mot_cle(self):
        """Retourne True puisque c'est un mot-clé."""
        return True

    def nom_complet_pour(self, personnage=None):
        """Retourne le mot-clé en fonction de la langue."""
        mots_cles = {
            "anglais": self.anglais,
            "francais": self.francais,
        }

        if personnage:
            return mots_cles[personnage.langue_cmd]
        else:
            return self.francais + "/" + self.anglais
