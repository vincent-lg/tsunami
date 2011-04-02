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


"""Package contenant la commande 'addroom'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.interpreteur.masque.exceptions.erreur_interpretation import \
    ErreurInterpretation


class CmdAddroom(Commande):
    
    """Commande 'addroom'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "addroom", "addroom")
        self.schema = "<direction> <nv_ident_salle>"
        self.nom_categorie = "batisseur"
        self.aide_courte = "ajoute une salle à l'univers"
        self.aide_longue = \
            "Cette commande permet d'ajouter une salle à l'univers. Elle " \
            "prend en paramètre la direction constante dans laquelle " \
            "vous voulez créer la salle (ce ne peut pas être " \
            "|ent|escalier|ff| par exemple car ce n'est pas un nom " \
            "constant) puis l'identifiant de la salle à créer. Exemple " \
            "de syntaxe : %addroom% |ent|est picte:5|ff|."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        direction = dic_masques["direction"].direction
        zone = dic_masques["nv_ident_salle"].zone
        mnemonic = dic_masques["nv_ident_salle"].mnemonic
        salle = personnage.salle
        dir_opposee = salle.sorties.get_nom_oppose(direction)
        
        if salle.sorties.sortie_existe(direction):
            raise ErreurInterpretation(
                "Cette direction a déjà été définie dans cette salle.")
        
        nv_coords = getattr(salle.coords, direction.replace("-", ""))
        if nv_coords.valide and nv_coords in type(self).importeur.salle:
            raise ErreurInterpretation(
                "Ces coordonnées sont déjà utilisées.")
        
        x, y, z, valide = nv_coords.tuple_complet()
        
        try:
            nv_salle = type(self).importeur.salle.creer_salle(zone, mnemonic,
                    x, y, z, valide)
        except ValueError as err_val:
            personnage << str(err_val) + "."
        else:
            salle.sorties.ajouter_sortie(direction, direction,
                    salle_dest=nv_salle, corresp=dir_opposee)
            nv_salle.sorties.ajouter_sortie(dir_opposee, dir_opposee,
                    salle_dest=salle, corresp=direction)
            
            personnage << "La salle {} a bien été ajouté vers {}.".format(
                    nv_salle.ident, salle.sorties[direction].nom_complet)
