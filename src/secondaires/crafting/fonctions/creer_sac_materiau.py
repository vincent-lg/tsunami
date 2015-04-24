# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Fichier contenant la fonction creer_sac_materiau."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Crée un sac de matériau."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.creer_sac_materiau, "str")
        cls.ajouter_types(cls.creer_sac_materiau, "str", "Fraction")
        cls.ajouter_types(cls.creer_sac_materiau, "str", "Fraction", "str")

    @staticmethod
    def creer_sac_materiau(matiere, quantite=1, sac=""):
        """Crée un sac matériau contenant la matière précisée.

        Cette fonction ne fait que créer un ou plusieurs objets.
        Il faut ensuite les poser ou les donner à un personnage,
        sans quoi ils disparaîtront au prochain reboot et ne seront
        pas même utilisables avant cela. Consultez les
        exemples plus bas pour voir quelques solutions.

        Paramètres à préciser :

          * matiere : la clé de la matière première à faire apparaître ;
          * nombre : le nombre à mettre en sac (1 si non précisé) ;
          * sac : le prototype de sac de matériau à utiliser.

        Si le troisième paramètre n'est pas renseigné, le système
        recherchera le sac de matériau qui peut correspondre à
        la matière que l'on veut faire apparaître.

        Cette fonction retourne une liste d'objets : en effet,
        si la quantité de matières est trop importante pour un seul sac,
        en fait apparaître plusieurs.

        Exemples d'utilisation :

          # Partant du principe qu'il existe une matière première 'farine_ble'
          # Et un sac de matériau 'sac' qui accepte la farine
          objets = creer_sac_materiau("farine_ble", 5)
          # Crée 5 unités de farine (peut-être 5 livres)
          pour chaque objet dans objets:
              poser salle objet
          fait
          # Si vous voulez impérativement que la farine soit mise en sac
          objets = creer_sac_materiau("farine_ble", 5, "sac")

        """
        # Récupère le prototype de la matière
        matiere = importeur.objet.prototypes[matiere]
        if not matiere.est_de_type("matériau"):
            raise ErreurExecution("{} n'est pas de type matériau".format(
                    repr(matiere.cle)))

        # Si besoin, cherche le sac
        if sac:
            sac = importeur.objet.prototypes[sac]
            if not sac.est_de_type("sac de matériau"):
                raise ErreurExecution("{} n'est pas un sac de " \
                        "matériau".format(repr(sac.cle)))
        else:
            type_sac = importeur.objet.types["sac de matériau"]
            prototypes_sac = [p for p in importeur.objet.prototypes.values() \
                    if isinstance(p, type_sac)]

            sac = None
            for prototype in prototypes_sac:
                for nom_type in prototype.materiaux_admis:
                    type_materiau = importeur.objet.types[nom_type]
                    if isinstance(matiere, type_materiau):
                        sac = prototype
                        break

            if sac is None:
                raise ErreurExecution("Impossible de trouver un sac " \
                        "de matériau pour {}".format(repr(matiere.cle)))

        # Crée autant de sacs que nécessaire
        quantite = int(quantite)
        poids_max = sac.poids_max
        qtt_max = int(poids_max / matiere.poids_unitaire)
        objets = []
        fini = False
        while quantite > 0:
            qtt = qtt_max
            if qtt >= quantite:
                qtt = quantite
                fini = True

            objet = importeur.objet.creer_objet(sac)
            objet.materiau = matiere
            objet.quantite = qtt
            objets.append(objet)
            quantite -= qtt

        return objets
