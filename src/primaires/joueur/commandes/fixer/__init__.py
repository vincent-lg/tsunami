# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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


"""Package contenant la commande 'fixer'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.format.fonctions import contient

class CmdFixer(Commande):
    
    """Commande 'fixer'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "fixer", "fix")
        self.groupe = "joueur"
        self.schema = "(<message> a/to <nombre>)"
        self.aide_courte = "fixe l'apprentissage d'un talent"
        self.aide_longue = \
            "Cette commande permet de fixer un seuil à l'apprentissage d'un " \
            "talent, afin d'économiser des points d'apprentissage. Sans " \
            "argument, la commande renvoie une liste de vos seuils actuels. " \
            "Pour débloquer un talent, utilisez la valeur |ent|0|ff|."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        if dic_masques["message"] is not None:
            nom_talent = dic_masques["message"].message
            try:
                limite = dic_masques["nombre"].nombre
                limite = int(limite)
                assert limite >= 0
            except (AttributeError, ValueError, AssertionError):
                personnage << "|err|Vous devez préciser un nombre positif " \
                        "ou nul.|ff|"
            else:
                for talent in importeur.perso.talents.values():
                    if contient(talent.nom, nom_talent) \
                            and talent.cle in personnage.talents:
                        personnage.l_talents[talent.cle] = limite
                        if limite < personnage.get_talent(talent.cle):
                            personnage << "|err|Votre connaissance de ce " \
                                    "talent est déjà supérieure à " \
                                    "{}%.|ff|".format(limite)
                            return
                        if limite == 0:
                            del personnage.l_talents[talent.cle]
                            personnage << "Le talent {} est débloqué.".format(
                                    talent.nom)
                        else:
                            personnage << "Vous avez bloqué le talent " \
                                    "{} à {}%.".format(talent.nom, limite)
                        return
                personnage << "|err|Le talent '{}' est introuvable.|ff|".format(
                        nom_talent)
        else:
            if not personnage.l_talents:
                personnage << "|att|Vous n'avez aucun seuil défini.|ff|"
                return
            ret = "Vos talents bloqués :"
            lignes = []
            for cle, limite in personnage.l_talents.items():
                talent = importeur.perso.talents[cle]
                ligne = talent.nom + " (" + str(limite) + "%)"
                lignes.append(ligne)
            ret += "\n- " + "\n- ".join(lignes)
            personnage << ret
