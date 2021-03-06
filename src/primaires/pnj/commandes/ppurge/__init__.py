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


"""Package contenant la commande 'ppurge'.

"""

from primaires.interpreteur.commande.commande import Commande

class CmdPpurge(Commande):
    
    """Commande 'ppurge'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "ppurge", "ppurge")
        self.groupe = "administrateur"
        self.nom_categorie = "batisseur"
        self.schema = "<ident_prototype_pnj>"
        self.aide_courte = "retire un PNJ de la salle"
        self.aide_longue = \
            "Cette commande permet de faire disparaître un PNJ " \
            "de la salle. Vous devez préciser en paramètre l'identifiant " \
            "du prototype et tous les PNJ de ce prototype présents " \
            "dans la salle seront effacés. Cette suppression est " \
            "définitive. Le prototype ne sera, en revanche, pas supprimé."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        prototype = dic_masques["ident_prototype_pnj"].prototype
        salle = personnage.salle
        nb_det = 0
        for personnage in salle.personnages:
            if hasattr(personnage, "prototype") and personnage.prototype is \
                    prototype:
                salle.retirer_personnage(personnage)
                personnage.salle = None
                importeur.pnj.supprimer_PNJ(personnage.identifiant)
                nb_det += 1
        
        if nb_det == 1:
            personnage << "{} PNJ a été retiré de cette salle.".format(
                    nb_det)
        elif nb_det > 1:
            personnage << "{} PNJs ont été retirés de cette salle.".format(
                    nb_det)
        else:
            personnage << "|att|Aucun PNJ modelé sur ce prototype n'est " \
                    "présent dans cette salle.|ff|"
