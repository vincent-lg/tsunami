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


"""Fichier contenant le paramètre 'liste' de la commande 'navire'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmListe(Parametre):
    
    """Commande 'navire liste'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "liste", "list")
        self.schema = ""
        self.aide_courte = "liste les navires existants"
        self.aide_longue = \
            "Cette commande liste les navires existants."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        navires = list(type(self).importeur.navigation.navires.values())
        navires = sorted(navires, key=lambda n: n.cle)
        if navires:
            lignes = [
                "  Clé             | Étendue         | " \
                "Coordonnées     | Vitesse    | Direction"]
            for navire in navires:
                vitesse = navire.vitesse_noeuds
                vitesse = round(vitesse, 3)
                vitesse = str(vitesse).replace(".", ",")
                direction = navire.direction.direction
                direction = round(direction, 3)
                direction = str(direction).replace(".", ",")
                etendue = navire.etendue and navire.etendue.cle or "aucune"
                lignes.append(
                    "  {:<15} | {:<15} | {:>15} | {:>10} | {:>9}".format(
                    navire.cle, etendue,
                    navire.position.coordonnees, vitesse,
                    direction))
            personnage << "\n".join(lignes)
        else:
            personnage << "Aucun navire n'est actuellement défini."
