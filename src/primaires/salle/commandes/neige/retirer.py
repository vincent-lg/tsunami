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


"""Package contenant le paramètre 'retirer' de la commande 'neige'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.salle.bonhomme_neige import BonhommeNeige
from primaires.objet.conteneur import SurPoids

class PrmRetirer(Parametre):
    
    """Commande 'neige retirer'"""
    
    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "retirer", "remove")
        self.schema = "<bh_emplacement> depuis/from " \
                "<element_observable>"
        self.aide_courte = "retire un élément d'un bonhomme"
        self.aide_longue = \
            "Cette commande permet de retirer un élément d'un " \
            "bonhomme de neige afin de changer si besoin sa décoration. " \
            "Vous pouvez voir les éléments déjà décorés du bonhomme en " \
            "le regardant tout simplement. Pour retirer un élément, " \
            "précisez d'abord le nom de l'élément, suivi du mot-clé " \
            "|cmd|depuis|ff| ou |cmd|from|ff| en anglais, suivi du nom " \
            "du bonhomme de neige."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        salle = personnage.salle
        emplacement = dic_masques["bh_emplacement"].emplacement
        bonhomme = dic_masques["element_observable"].element
        personnage.agir("neige")
        if not isinstance(bonhomme, BonhommeNeige):
            personnage << "|err|Ceci n'est pas un bonhomme de neige.|ff|"
            return
        
        if bonhomme.createur is not personnage:
            personnage << "|err|Ce bonhomme de neige n'est pas à vous.|ff|"
            return
        
        modele = bonhomme.prototype
        if personnage.nb_mains_libres < 1:
            personnage << "|err|Il vous faut au moins une main " \
                    "de libre.|ff|"
            return
        
        element = modele.get_element(emplacement)
        if element is None:
            personnage << "|err|Ce bonhomme de neige ne possède pas " \
                    "cet emplacement.|ff|"
            return
        
        if bonhomme.elements.get(element.nom) is None:
            personnage << "|err|Ce bonhomme de neige n'a pas quelque " \
                    "chose ici.|ff|"
            return
        
        objet = bonhomme.elements[element.nom]
        del bonhomme.elements[element.nom]
        personnage.envoyer_lisser("Vous retirez {} de {}.".format(
                objet.get_nom(), bonhomme.get_nom()))
        salle.envoyer_lisser("{{}} s'active autour de {}.".format(
                bonhomme.get_nom()), personnage)
        try:
            pos = personnage.ramasser(objet)
            assert pos is not None
        except (SurPoids, AssertionError):
            salle.objets_sol.ajouter(objet)
            personnage << "C'est trop lourd, {} tombe à terre.".format(
                    objet.get_nom())
