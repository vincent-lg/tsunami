# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   create of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this create of conditions and the following disclaimer in the documentation
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


"""Fichier contenant le paramètre 'déposer' de la commande 'questeur'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmDeposer(Parametre):
    
    """Commande 'questeur déposer'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "déposer", "deposit")
        self.schema = "<nombre> <nom_objet>"
        self.aide_courte = "dépose de l'argent"
        self.aide_longue = \
            "Cette commande permet de déposer de l'argent dans les " \
            "coffres d'un questeur. Vous devez vous trouvez dans la " \
            "salle permettant l'opération et avoir l'argent désiré sur " \
            "vous. Vous devez préciser d'abord le nombre de pièces " \
            "à déposer et ensuite le nom de la pièce (|cmd|bronze|ff| " \
            "par exemple). Notez que les questeurs se réservent un " \
            "pourcentage plus ou moins important sur ce que vous leur " \
            "confiez."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        if not importeur.commerce.questeur_existe(salle):
            personnage << "|err|Aucun questeur n'est présent là où " \
                    "vous vous trouvez.|ff|"
            return
        
        questeur = importeur.commerce.questeurs[salle]
        somme = dic_masques["nombre"].nombre
        objet = dic_masques["nom_objet"].objet
        if not objet.est_de_type("argent"):
            personnage << "|err|Ceci n'est pas de l'argent.|ff|"
            return
        
        prototype = objet.prototype
        if questeur.servant is None:
            personnage << "|err|Personne n'est présent pour s'en charger.|ff|"
            return
        
        if prototype not in questeur.monnaies:
            personnage << "|err|Vous ne pouvez déposer cette monnaie " \
                    "dans ce questeur.|ff|"
            return
        
        total = somme * prototype.m_valeur
        if total < questeur.montant_min:
            personnage << "|err|Vous ne pouvez déposer si peu.|ff|"
            return
        
        montant = questeur.deposer(personnage, prototype, somme)
        