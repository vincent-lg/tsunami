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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT master OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'info' de la commande 'matelot'."""

from textwrap import dedent

from primaires.interpreteur.masque.parametre import Parametre

class PrmInfo(Parametre):

    """Commande 'matelot info'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "info", "info")
        self.schema = "<cle>"
        self.nom_groupe = "administrateur"
        self.tronquer = True
        self.aide_courte = "affiche les info du matelot"
        self.aide_longue = \
            "Cette commande permet d'afficher le détail des " \
            "informations d'un matelot. Vous devez préciser en " \
            "paramètre l'identifiant du PNJ derrière le matelot."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère le matelot
        identifiant = dic_masques["cle"].cle
        try:
            matelot = importeur.navigation.matelots[identifiant]
        except KeyError:
            personnage << "|err|Le matelot d'identifiant {} n'est " \
                    "pas trouvable.|ff|".format(repr(identifiant))
            return

        pnj = matelot.personnage
        msg = dedent("""
            Informations sur le matelot {identifiant} :
              Actif sur {cle_navire} ({nom_navire}).
              Au poste : {poste}.
              Statut du PNJ : {statut}.
              Ordres en cours : {ordres}.
            """.strip("\n"))

        navire = matelot.equipage.navire
        cle_navire = navire and navire.cle or "|att|inconnu|ff|"
        nom_navire = navire and navire.nom_personnalise or ""
        poste = matelot.poste.nom
        if pnj:
            if pnj.etats:
                statut = "|att|occupé|ff|"
                etats = ", ".join(e.cle for e in pnj.etats)
                statut += " (" + etats + ")"
            else:
                statut = "libre"
        else:
            statut = "|err|INEXISTANT|ff|"

        ordres = matelot.ordres
        if ordres:
            ab_ordres = ordres[:10]
            ab_ordres = ", ".join(o.cle for o in ab_ordres)
            if len(ordres) > 10:
                ab_ordres += "..."
            ordres = ab_ordres
        else:
            ordres = "aucun"

        personnage << msg.format(identifiant=identifiant,
                cle_navire=cle_navire, nom_navire=nom_navire,
                poste=poste, statut=statut, ordres=ordres)
