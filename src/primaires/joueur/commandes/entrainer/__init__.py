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
from primaires.perso.exceptions.stat import DepassementStat

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
            "vous aurez besoin de 10 pourcent d'XP du niveau secondaire " \
            "choisi pour gagner un point en force."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        # La première étape est de chercher les "maîtres" dans la salle
        maitres = [p for p in personnage.salle.PNJ if p.entraine_stats]
        stats = {} # nom: prototype
        prototypes = {} # prototype: {stat]
        max = {} # nom_stat: valeur_max
        xps = {} # stat: xp_nécessaire
        for pnj in maitres:
            for stat, niveau in pnj.entraine_stats.items():
                if niveau > max.get(stat, 0):
                    stats[stat] = pnj
                    max[stat] = niveau
                if stat not in xps:
                    base = personnage.stats[stat].base
                    if base < 100 and base < niveau:
                        xp = int(importeur.perso.gen_niveaux.grille_xp[ \
                                base - 1][1] / 2)
                        xps[stat] = xp
                    else:
                        xps[stat] = None
                liste = prototypes.get(pnj, [])
                liste.append(stat)
                prototypes[pnj] = liste
        
        if dic_masques["stat_ent"]:
            stat = dic_masques["stat_ent"].stat_ent
            if stat not in stats:
                personnage << "|err|Aucun maître présent ne peut vous " \
                        "enseigner cela.|ff|"
                return
            
            maitre = stats[stat]
            max = max[stat]
            xp = xps[stat]
            if not dic_masques["niveau_secondaire"]:
                personnage << "|err|Précisez le niveau secondaire " \
                        "contenant l'expérience à verser.|ff|"
                return
            
            niveau = dic_masques["niveau_secondaire"].niveau_secondaire
            if personnage.niveaux.get(niveau, 0) < personnage.stats[stat].base:
                personnage << "|err|Vous n'êtes pas assez expérimenté dans ce niveau.|ff|"
                return
            
            if personnage.stats[stat].base > max:
                personnage.envoyer("|err|{} ne peut vous enseigner davantage " \
                        "cette caractéristique.|ff|", maitre)
                return
            
            if personnage.xps.get(niveau, 0) < xp:
                personnage << "|err|Vous devez avoir au moins {} xp dans " \
                        "ce niveau.|ff|".format(xp)
                return
            
            personnage.agir("entrainer")
            end = 20
            try:
                personnage.stats.endurance -= end
            except DepassementStat:
                personnage << "|err|Vous êtes trop fatigué pour vous entraîner.|ff|"
                return
            
            personnage << "Vous commencez à vous entraîner."
            personnage.salle.envoyer("{} commence à s'entraîner.", personnage)
            personnage.cle_etat = "entrainer"
            yield 60
            personnage.cle_etat = ""
            personnage << importeur.perso.cfg_stats.entrainables[stat]
            personnage.xps[niveau] -= xp
            personnage.gagner_stat(stat)
        else:
            # On affiche les stats que peuvent apprendre les personnages présents
            if not maitres:
                personnage << "|err|Aucun maître n'est actuellement " \
                        "présent.|ff|"
                return
            
            lignes = []
            for p, l_stats in prototypes.items():
                lignes.append(p.nom_singulier + " peut vous enseigner :")
                for s in l_stats:
                    xp = xps[s]
                    if xp is None:
                        xp = "..."
                    else:
                        xp = str(xp)
                    
                    lignes.append("  " + s.ljust(10) + " pour " + \
                            xp.rjust(15) + " XP")
            
            personnage << "\n".join(lignes)
