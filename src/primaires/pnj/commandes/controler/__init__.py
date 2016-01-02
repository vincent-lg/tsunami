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


"""Package contenant la commande 'contrôler'.

"""

from primaires.interpreteur.commande.commande import Commande
from primaires.pnj.contextes.controler import Controler

class CmdControler(Commande):
    
    """Commande 'contrôler'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "contrôler", "control")
        self.groupe = "administrateur"
        self.nom_categorie = "batisseur"
        self.schema = "<cle>"
        self.aide_courte = "contrôle un PNJ"
        self.aide_longue = \
            "Cette commande permet de prendre le contrôle d'un PNJ. Les " \
            "commandes que vous entrerez seront exécutées par lui."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        cle = dic_masques["cle"].cle

        # Si la clé correspond exactement à un identifant de PNJ, c'est lui
        pnj = importeur.pnj.PNJ.get(cle)
        if not pnj:
            # Sinon c'est peut-être une clé de prototype
            proto = importeur.pnj.prototypes.get(cle)
            if proto:
                if len(proto.pnj) == 0:
                    # proto trouvé mais pas de PNJ
                    personnage << "Il n'existe aucun PNJ pour le " \
                                  "prototype {}.".format(proto)
                    return
                elif len(proto.pnj) == 1:
                    pnj = proto.pnj[0]
                else:
                    # Lister les PNJ du proto
                    ids = [x.identifiant for x in proto.pnj]
                    personnage << "PNJ existants pour le prototype {} :\n" \
                            "  {}".format(proto, '\n  '.join(ids))
                    return

        if pnj:
            if pnj.controle_par is not None:
                personnage << "|err|Ce PNJ est déjà contrôlé.|ff|"
                return

            pnj.controle_par = personnage
            contexte = Controler(personnage, pnj)
            personnage.contextes.ajouter(contexte)
            personnage << contexte.accueil()
            return
        personnage << "|err|Aucun PNJ ou prototype de ce nom trouvé.|ff|"
