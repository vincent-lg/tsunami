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


"""Ce fichier contient la classe Annonces détaillée plus bas."""

from textwrap import wrap

from abstraits.obase import BaseObj

class Annonces(BaseObj):

    """Classe conteneur des differentes annonces (organisation de tournois, etc)."""

    enregistrer = True

    def __init__(self):
        """Constructeur du conteneur"""

        BaseObj.__init__(self)
        self.__annonces = []
        self._deja_vues = {}

    def __getnewargs__(self):
        return ()

    def __len__(self):
        return len(self.__annonces)

    def __getitem__(self, id):
        """Retourne une annonce par son index."""

        return self.__annonces[id]

    def __setitem__(self, id, modif):
        """Edite une annonce enregistrée."""

        self.__annonces[id] = modif

    def __delitem__(self, id):
        """Supprime une annonce avec l'index passé en paramètre."""

        del self.__annonces[id]

    def append(self, texte):
        """Ajoute une annonce à la liste."""

        self.__annonces.append(texte)
        type(self).importeur.communication.canaux["info"].envoyer_imp("|vr|Une nouvelle annonce a été créée.|ff|") # On prévient les joueurs qu'une nouvelle annonce a été créée.

    def afficher(self, offset=0, afficher_id=False):
        """Retourne les dernières annonces jusqu'à l'offset (qui limite le nombre d'annonces a afficher)."""

        annonces = self.__annonces
        if offset > 0:
            annonces = annonces[-offset:]
        if len(annonces) > 0:
            for i in range(len(annonces)):
                id = "[|rgc|" + str(self.__annonces.index(annonces[i]) + 1)
                id += "|ff|] "
                indent = "\n" + (len(id) - 9) * " "
                if afficher_id:
                    annonces[i] = id + indent.join(wrap(annonces[i], 75)) # wrap permet de limiter la largeur du texte.
                else:
                    annonces[i] = "- " + indent.join(wrap(annonces[i], 75))
            return "\n\n".join(annonces) # On saute deux lignes entre chaque annonce (pour différencier les différentes annonces).
        else:
            return ""

    def afficher_dernieres_pour(self, personnage, lire=True):
        """Affiche les dernières annonces nons lues par 'personnage'."""

        ret = ""
        derniere = 0
        if personnage in self._deja_vues:
            derniere = self._deja_vues[personnage]
        if len(self) - derniere > 0:
            if personnage.nom_groupe == "administrateur":
                ret = self.afficher(len(self) - derniere, True)
            else:
                ret = self.afficher(len(self) - derniere)
        if lire:
            self._deja_vues[personnage] = len(self)
        return ret
