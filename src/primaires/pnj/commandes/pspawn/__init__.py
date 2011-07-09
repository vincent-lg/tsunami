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


"""Package contenant la commande 'pspawn'.

"""

from primaires.interpreteur.commande.commande import Commande

class CmdPspawn(Commande):
    
    """Commande 'pspawn'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "pspawn", "pspawn")
        self.groupe = "administrateur"
        self.nom_categorie = "batisseur"
        self.schema = "(<nombre>) <ident_prototype_pnj>"
        self.aide_courte = "fait apparaître un PNJ dans la salle"
        self.aide_longue = \
            "Cette commande permet de faire apparaître un PNJ dans " \
            "la salle où vous vous trouvez. Elle prend en paramètre " \
            "obligatoire le prototype depuis lequel créer le PNJ."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        prototype = dic_masques["ident_prototype_pnj"].prototype
        salle = personnage.salle
        nb_pnj = 1
        if dic_masques["nombre"] is not None:
            nb_pnj = dic_masques["nombre"].nombre
            i = 0
            while i < nb_pnj:
                pnj = type(self).importeur.pnj.creer_PNJ(prototype)
                pnj.salle = salle
                i += 1
            salle.envoyer("{} apparaissent du néant.".format(
                    prototype.get_nom(nb_pnj)))
        else:
            pnj = type(self).importeur.pnj.creer_PNJ(prototype)
            pnj.salle = salle
            salle.envoyer("{} apparaît du néant.".format(
                    pnj.nom_singulier))
