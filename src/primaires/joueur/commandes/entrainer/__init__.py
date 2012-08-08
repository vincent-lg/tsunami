# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Package contenant la commande 'entrainer'"""

from primaires.interpreteur.commande.commande import Commande

class CmdEntrainer(Commande):
    
    """Commande 'entrainer'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "entraîner", "train")
        self.groupe = "joueur"
        self.schema = "(<stat_ent> depuis/from <niveau_secondaire>)"
        self.aide_courte = "entraîne une caractéristique"
        self.aide_longue = \
            "Cette commande permet de vous entraîner auprès d'un " \
            "maître afin d'augmenter, en pratiquant, certaines " \
            "statistiques. Sans argument, cette commande demande " \
            "quelles caractéristiques peuvent être entraînés avec " \
            "les maîtres présents dans la salle. Si vous voulez " \
            "entraîner une caractéristique, vous devez préciser " \
            "le nom de la caractéristique (par exemple |cmd|force|ff|) " \
            "suivi, après du mot-clé, du niveau secondaire que vous " \
            "utiliserez pour payer cette statistique. Chaque " \
            "apprentissage vous coûtera un certain pourcentage " \
            "d'expérience du niveau secondaire que vous choisissez. " \
            "Ce pourcentage dépendra de votre connaissance dans la " \
            "caractéristique : si par exemple vous avez 20 en force, " \
            "vous aurez besoin de 10% d'XP du niveau secondaire " \
            "choisi pour gagner un point en force."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        # La première étape est de chercher les "maîtres" dans la salle
        maitres = [p for p in personnage.salle.PNJ if p.entraine_stats]
        stats = {} # nom: prototype
        max = {} # nom_stat: valeur_max
        for pnj in maitres:
            for stat, niveau in pnj.entraine_stats.items():
                if niveau > max.get(stat, 0):
                    stats[stat] = pnj
                    max[stat] = niveau
        
        if dic_masques["stat_ent"]:
            stat = dic_masques["stat_ent"].stat_ent
            niveau = dic_masques["niveau_secondaire"].niveau_secondaire
            if personnage.niveaux.get(niveau) < personnage.stats[stat].base:
                # Compléter...
                pass
