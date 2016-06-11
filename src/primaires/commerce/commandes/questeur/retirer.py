# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   create of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this create of conditions and the following disclaimer in the documentation
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


"""Fichier contenant le paramètre 'retirer' de la commande 'questeur'."""

from primaires.format.fonctions import contient
from primaires.interpreteur.masque.parametre import Parametre

class PrmRetirer(Parametre):

    """Commande 'questeur retirer'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "retirer", "withdraw")
        self.schema = "<nombre> <type_piece>"
        self.aide_courte = "retire de l'argent"
        self.aide_longue = \
            "Cette commande vous permet de retirer de l'argent depuis un " \
            "questeur. Les paramètres à préciser sont le nombre de pièces " \
            "que vous souhaitez retirer de votre compte ainsi que le type " \
            "de pièce (|ent|bronze|ff| par exemple). Vous devez bien " \
            "entendu posséder un compte dans le questeur et avoir assez " \
            "d'argent dessus."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        if not importeur.commerce.questeur_existe(salle):
            personnage << "|err|Aucun questeur n'est présent là où " \
                    "vous vous trouvez.|ff|"
            return

        questeur = importeur.commerce.questeurs[salle]
        nombre = dic_masques["nombre"].nombre
        nom_type = dic_masques["type_piece"].nom_type
        prototype = None
        for t_prototype in questeur.monnaies:
            if contient(t_prototype.nom_singulier, nom_type):
                prototype = t_prototype
                break

        if prototype is None:
            personnage << "|err|Vous ne pouvez retirer cela.|ff|"
            return

        if questeur.servant is None:
            personnage << "|err|Personne n'est présent pour s'en charger.|ff|"
            return

        total = nombre * prototype.m_valeur
        if questeur.comptes.get(personnage, 0) < total:
            personnage << "|err|Vous ne possédez pas assez sur ce compte.|ff|"
            return

        personnage.envoyer("{{}} prend {} de ses coffres et vous les " \
                "donne.".format(prototype.get_nom(nombre)), questeur.servant)
        questeur.prelever(personnage, prototype, nombre)
