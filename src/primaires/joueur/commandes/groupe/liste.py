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


"""Fichier contenant le paramètre 'liste' de la commande 'groupe'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmListe(Parametre):
    
    """Commande 'groupe liste'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "liste", "list")
        self.aide_courte = "affiche la liste des groupes existants"
        self.aide_longue = \
                "Affiche la liste des groupes existants. Pour avoir " \
            "plus d'informations sur un groupe, référez-vous à la commande " \
            "%groupe%."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère les groupes chargés
        groupes = type(self).importeur.interpreteur.groupes._groupes.values()
        cmds = type(self).importeur.interpreteur.groupes.commandes.values()
        groupes = sorted(groupes, key=lambda groupe:groupe.nom)
        if groupes:
            msg = "Liste des groupes existants :\n"
            for groupe in groupes:
                nb_cmds = len([grp_cmd.nom for grp_cmd in \
                        cmds if grp_cmd is groupe])
                msg += "\n  {} ({} commandes)".format(groupe.nom.ljust(15),
                        nb_cmds)
            personnage << msg
        else:
            personnage.envoyer("|att|Aucun groupe n'est chargé. Ce semble " \
                "très improbable.|ff|")
