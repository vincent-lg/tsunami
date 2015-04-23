# -*-coding:Utf-8 -*
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


"""Fichier contenant le type machine."""

from bases.objet.attribut import Attribut
from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.flottant import Flottant
from primaires.interpreteur.editeur.selection import Selection
from primaires.objet.conteneur import ConteneurObjet
from .base import BaseType

class Machine(BaseType):

    """Type d'objet: machine."""

    nom_type = "machine"
    nettoyer = False

    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.flags = 1 # ne peut pas prendre
        self.machine_conteneur = False
        self.poids_max = 0

        self.etendre_editeur("m", "machine conteneur", Flag, self,
                "machine_conteneur")
        self.etendre_editeur("x", "poids max", Flottant, self, "poids_max")

        # Attributs propres à l'objet (non au prototype)
        self._attributs = {
            "conteneur": Attribut(
                lambda obj: ConteneurObjet(obj),
                ("", )),
        }

    def peut_contenir(self, objet, qtt=1):
        """Retourne True si le conteneur peut prendre l'objet."""
        poids = objet.poids * qtt
        contenu = self.poids - self.prototype.poids_unitaire
        poids_max = self.poids_max
        return contenu + poids <= poids_max

    def calculer_poids(self):
        """Retourne le poids de l'objet et celui des objets contenus."""
        poids = self.poids_unitaire
        for o, nb in self.conteneur.iter_nombres():
            poids += o.poids * nb

        return round(poids, 3)

    def contient(self, objet, quantite):
        """Retourne True si le conteneur contient l'objet, False sinon.

        Si l'objet est présente au moins dans la quantité indiquée,
        retourne True mais False si ce n'est pas le cas.
        Si on cherche un objet en quantité N et que l'objet est trouvé
        en quantité >= N, on retourne True sinon False.

        """
        for o, qtt in self.conteneur.iter_nombres():
            if objet is o:
                if qtt >= quantite:
                    return True
                return False

        return False

    def combien_dans(self, objet):
        """Retourne combien d'objet indiqué sont dans le conteneur."""
        for o, qtt in self.conteneur.iter_nombres():
            if objet is o:
                return qtt

        return 0

    def etendre_script(self):
        """Extension du scripting."""
        evt_entrepose = self.script.creer_evenement("entrepose")
        evt_entrepose.aide_courte = "le personnage entrepose quelque " \
                "chose dans la machine"
        evt_entrepose.aide_longue = \
            "Cet évènement est appelé quand le personnage entrepose " \
            "quelque chose dans la machine. Le sous-évènement " \
            "\"avant\" est appelé avant d'entreposer quoique ce " \
            "soit, ce qui permet éventuellement d'empêcher " \
            "l'exécution de la commande. L'évènement \"après\", " \
            "au contraire, est appelé quand les objets ont été " \
            "entreposés et ne devrait servir qu'à l'affichage."
        var_perso = evt_entrepose.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage entreposant les objets"
        var_objet = evt_entrepose.ajouter_variable("machine", "Objet")
        var_objet.aide = "la machine-même"

        # Sous-évènements
        evt_entrepose_avt = evt_entrepose.creer_evenement("avant")
        evt_entrepose_avt.aide_courte = "avant d'entreposer"
        evt_entrepose_avt.aide_longue = \
            "Cet évènement est appelé avant que le personnage " \
            "n'entrepose dans la machine. Il a été prouvé que la " \
            "machine pouvait contenir les objets indiqués (en " \
            "terme de poids maximum, notamment). Il reste cependant " \
            "à vérifier d'autres facteurs. Cet évènement permet " \
            "donc de contrôler les types des objets que l'on veut " \
            "entreposer et appliquer un traitement particulier dessus."
        var_objet = evt_entrepose_avt.ajouter_variable("objet", "Objet")
        var_objet.aide = "l'objet que l'on veut entreposé"

        evt_entrepose_apr = evt_entrepose.creer_evenement("après")
        evt_entrepose_apr.aide_courte = "après avoir entreposé"
        evt_entrepose_apr.aide_longue = \
            "Cet évènement est appelé quand les objets ont été " \
            "correctement entreposés. Il s'agit surtout du moment " \
            "d'afficher le message personnalisé confirmant que " \
            "l'on a bien entreposé dans la machine."
        var_objets = evt_entrepose_apr.ajouter_variable("objets", "list")
        var_objets.aide = "les objets entreposés"

        evt_recupere = self.script.creer_evenement("récupère")
        evt_recupere.aide_courte = "le personnage récupère quelque " \
                "chose dans la machine"
        evt_recupere.aide_longue = \
            "Cet évènement est appelé quand le personnage récupère " \
            "quelque chose dans la machine. Le sous-évènement " \
            "\"avant\" est appelé avant de récupérer quoique ce " \
            "soit, ce qui permet éventuellement d'empêcher " \
            "l'exécution de la commande. L'évènement \"après\", " \
            "au contraire, est appelé quand les objets ont été " \
            "récupérés et ne devrait servir qu'à l'affichage."
        var_perso = evt_recupere.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage récupérant les objets"
        var_objet = evt_recupere.ajouter_variable("machine", "Objet")
        var_objet.aide = "la machine-même"

        # Sous-évènements
        evt_recupere_avt = evt_recupere.creer_evenement("avant")
        evt_recupere_avt.aide_courte = "avant de récupérer"
        evt_recupere_avt.aide_longue = \
            "Cet évènement est appelé avant que le personnage " \
            "ne récupère dans la machine."
        var_objet = evt_recupere_avt.ajouter_variable("objet", "Objet")
        var_objet.aide = "l'objet que l'on veut récupérer"

        evt_recupere_apr = evt_recupere.creer_evenement("après")
        evt_recupere_apr.aide_courte = "après avoir récupéré"
        evt_recupere_apr.aide_longue = \
            "Cet évènement est appelé quand les objets ont été " \
            "correctement récupérés. Il s'agit surtout du moment " \
            "d'afficher le message personnalisé confirmant que " \
            "l'on a bien récupéré depuis la machine."
        var_objets = evt_recupere_apr.ajouter_variable("objets", "list")
        var_objets.aide = "les objets récupérés"

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        poids_max = enveloppes["x"]
        poids_max.apercu = "{objet.poids_max} kg"
        poids_max.prompt = "Poids max du conteneur : "
        poids_max.aide_courte = \
            "Entrez le |ent|poids maximum|ff| du conteneur ou " \
            "|cmd|/|ff| pour revenir à la fenêtre parente.\n\n" \
            "Poids maximum actuel : {objet.poids_max}"

    def objets_contenus(self, conteneur):
        """Retourne les objets contenus."""
        objets = []
        for objet in list(conteneur.conteneur._objets):
            objets.append(objet)
            objets.extend(objet.prototype.objets_contenus(objet))

        return objets

    def detruire_objet(self, conteneur):
        """Détruit l'objet passé en paramètre.

        On va détruire tout ce qu'il contient.

        """
        for objet in list(conteneur.conteneur._objets):
            if conteneur is not objet and objet.unique and objet.e_existe:
                importeur.objet.supprimer_objet(objet.identifiant)

    # Actions sur les objets
    def regarder(self, personnage):
        """Le personnage regarde l'objet"""
        msg = BaseType.regarder(self, personnage)
        if not getattr(self, "conteneur", False):
            return msg

        objets = []
        for o, nb in self.conteneur.get_objets_par_nom():
            objets.append(o.get_nom(nb))

        if objets:
            msg += "Vous voyez à l'intérieur :"
            msg += "\n  " + "\n  ".join(objets)
        else:
            msg += "Vous ne voyez rien à l'intérieur."

        return msg
