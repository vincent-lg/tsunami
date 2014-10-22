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


"""Fichier contenant la fonction peut_prendre."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution
from primaires.objet.conteneur import SurPoids

class ClasseFonction(Fonction):

    """Teste si le personnage peut prendre un ou des objets."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.peut_prendre_objet, "Personnage", "Objet")
        cls.ajouter_types(cls.peut_prendre_proto, "Personnage", "str",
                "Fraction")

    @staticmethod
    def peut_prendre_objet(personnage, objet):
        """Renvoie vrai si le personnage peut prendre l'objet, faux sinon.

        L'objet testé doit être une variable de type Objet.

        """
        # on teste l'inventaire
        for o in personnage.equipement.inventaire:
            if o.est_de_type("conteneur") \
                    and o.accepte_type(objet.poids_unitaire):
                try:
                    o.conteneur.supporter_poids_sup(objet.poids_unitaire,
                            recursif=False)
                except SurPoids:
                    return False
                else:
                    return True
        # on teste les membres
        for membre in personnage.equipement.membres:
            if membre.peut_tenir() and membre.tenu is None:
                return True
        return False

    @staticmethod
    def peut_prendre_proto(personnage, prototype, nb):
        """Renvoie vrai si le personnage peut prendre nb objets, faux sinon.

        Cet usage permet de tester à partir d'un objet non encore créé, et
        surtout de tester une quantité.

        """
        nb = int(nb)
        if not prototype in importeur.objet.prototypes:
            raise ErreurExecution("prototype {} introuvable".format(prototype))
        prototype = importeur.objet.prototypes[prototype]
        # on teste l'inventaire
        for o in personnage.equipement.inventaire:
            if o.est_de_type("conteneur") and o.accepte_type(prototype):
                try:
                    o.conteneur.supporter_poids_sup(
                            prototype.poids_unitaire * nb, recursif=False)
                except SurPoids:
                    return False
                else:
                    return True
        # on teste les membres
        if nb > 1:
            return False
        for membre in personnage.equipement.membres:
            if membre.peut_tenir() and membre.tenu is None:
                return True
        return False
