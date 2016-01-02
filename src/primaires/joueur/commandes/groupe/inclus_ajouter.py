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


"""Fichier contenant le paramètre 'ajouter' de la commande 'groupe inclus'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.interpreteur.masque.exceptions.erreur_interpretation import \
    ErreurInterpretation

class PrmInclusAjouter(Parametre):
    
    """Commande 'groupe inclus ajouter'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "ajouter", "add")
        self.schema = "<groupe1:groupe_existant> <groupe2:groupe_existant>"
        self.aide_courte = "ajoute un groupe inclus"
        self.aide_longue = \
            "Cette commande permet d'ajouter un groupe inclus. Le premier " \
            "groupe à entrer est celui dans lequel on doit inclure le " \
            "second groupe précisé. Exemple : %groupe% %groupe:inclus% " \
            "%groupe:inclus:ajouter% |cmd|administrateur joueur|ff| " \
            "inclura le groupe |tit|joueur|ff| dans le groupe " \
            "|tit|administrateur|ff|."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        nom_groupe = dic_masques["groupe1"].nom_groupe
        groupe = type(self).importeur.interpreteur.groupes[nom_groupe]
        nom_a_inclure = dic_masques["groupe2"].nom_groupe
        
        if nom_a_inclure in groupe.groupes_inclus:
            raise ErreurInterpretation(
                "|err|Le groupe {} est déjà inclus dans {}.|ff|".format(
                nom_a_inclure, nom_groupe))
        
        groupe.ajouter_groupe_inclus(nom_a_inclure)
        personnage << "Le groupe {} a bien été ajouté dans {}.".format(
                nom_a_inclure, nom_groupe)
