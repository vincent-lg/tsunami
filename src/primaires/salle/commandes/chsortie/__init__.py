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


"""Package contenant la commande 'chsortie'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.interpreteur.masque.exceptions.erreur_interpretation import \
    ErreurInterpretation

class CmdChsortie(Commande):
    
    """Commande 'chsortie'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "chsortie", "setexit")
        self.schema = "<direction> <ident_salle>"
        self.nom_categorie = "batisseur"
        self.aide_courte = "modifie une sortie de la salle courante"
        self.aide_longue = \
            "Cette commande permet de configurer une sortie de la salle " \
            "où vous vous trouvez. Vous devez lui préciser le nom de " \
            "la direction constante dans laquelle vous voulez créer " \
            "votre sortie, puis l'identifiant de la salle à lier. " \
            "Si vous vous trouvez dans la salle |ent|picte:1|ff| et " \
            "que vous entrez %chsortie% |ent|nord picte:2|ff|, une " \
            "sortie |ent|nord|ff| sera créée menant de la salle " \
            "|ent|picte:1|ff| à |ent|picte:2|ff|. Sa réciproque sera " \
            "également créée, c'est-à-dire la sortie |ent|sud|ff| " \
            "menant de |ent|picte:2|ff| vers |ent|picte:1|ff|."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        direction = dic_masques["direction"].direction
        salle = personnage.salle
        d_salle = dic_masques["ident_salle"].salle
        dir_opposee = salle.sorties.get_nom_oppose(direction)
        
        if salle.sorties.sortie_existe(direction):
            raise ErreurInterpretation(
                "|err|Cette direction a déjà été définie dans la salle " \
                "courante.|ff|")
        
        if d_salle.sorties.sortie_existe(dir_opposee):
            raise ErreurInterpretation(
                "|err|La direction opposée a déjà été définie dans {}.|ff|". \
                format(d_salle.ident))
        
        if salle is d_salle:
            raise ErreurInterpretation(
                "|err|La salle de destination est la même que la salle " \
                "d'origine.|ff|")
        
        salle.sorties.ajouter_sortie(direction, direction,
                salle_dest=d_salle, corresp=dir_opposee)
        d_salle.sorties.ajouter_sortie(dir_opposee, dir_opposee,
                salle_dest=salle, corresp=direction)
        
        personnage << "|att|La sortie {} reliant {} à {} a été créée.\n" \
                "La réciproque a été créée également (sortie {} dans {}).|ff|" \
                .format(direction, salle.ident, d_salle.ident, dir_opposee,
                    d_salle.ident)
