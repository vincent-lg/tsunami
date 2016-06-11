# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Package contenant le paramètre 'créer' de la commande 'meteo'."""

from primaires.format.tableau import Tableau
from primaires.interpreteur.masque.parametre import Parametre
from primaires.interpreteur.editeur.presentation import Presentation

class PrmCreer(Parametre):

    """Commande 'meteo créer'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "creer", "create")
        self.schema = "(<cle>)"
        self.aide_courte = "crée une perturbation"
        self.aide_longue = \
            "Cette commande permet de créer une perturbation météorologique " \
            "dans la salle où vous vous trouvez (par exemple, faire " \
            "apparaître un nuage). La salle où vous vous trouvez est prise "\
            "comme point de départ. Notez que vous ne pourrez pas faire " \
            "apparaître une perturbation si une autre est présente ou trop " \
            "proche. Les perturbations ont en effet des rayons " \
            "d'action, et deux perturbations ne doivent pas entrer en " \
            "conflit (un nuage ne doit pas en recouvrir un second, " \
            "par exemple). Si vous ne savez pas quelles perturbations " \
            "sont disponibles, entrez la commande sans paramètre."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        if dic_masques["cle"]:
            cle = dic_masques["cle"].cle
            classe = None
            for t_classe in importeur.meteo.perturbations:
                if t_classe.nom_pertu == cle and t_classe.origine:
                    classe = t_classe
                    break

            if classe is None:
                personnage << "|err|Cette perturbation n'existe pas.|ff|"
                return

            if not personnage.salle.coords.valide:
                personnage << "|err|Vous vous trouvez dans une salle sans " \
                        "coordonnées.|ff|"
                return

            n_pertu = classe(personnage.salle.coords.get_copie())
            for pertu in importeur.meteo.perturbations_actuelles:
                if n_pertu.va_recouvrir(pertu):
                    personnage << "|err|Une autre perturbation est trop " \
                            "proche de vous.|ff|"
                    n_pertu.detruire()
                    return
            personnage << "Vous avez bien créé une nouvelle perturbation " \
                    "{}.".format(n_pertu.nom_pertu)
            importeur.meteo.perturbations_actuelles.append(n_pertu)
            n_pertu.envoyer_message_debut()
        else:
            tableau = Tableau("Perturbations existantes")
            tableau.ajouter_colonne("Clé")
            tableau.ajouter_colonne("Attributs")
            for perturbation in sorted(importeur.meteo.perturbations,
                    key=lambda p: p.nom_pertu):
                attributs = ", ".join(perturbation.attributs)
                tableau.ajouter_ligne(perturbation.nom_pertu, attributs)

            personnage << tableau.afficher()
