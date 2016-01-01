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


"""Package contenant le paramètre 'installer' de la commande 'neige'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.salle.bonhomme_neige import BonhommeNeige

class PrmInstaller(Parametre):
    
    """Commande 'neige installer'"""
    
    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "installer", "install")
        self.schema = "<nom_objet> sur/on <bh_emplacement> de/of " \
                "<element_observable>"
        self.aide_courte = "installe un élément sur un bonhomme"
        self.aide_longue = \
            "Cette commande permet d'installer un élément sur un bonhomme " \
            "de neige. Vous devez préciser le nom de l'objet à installer, " \
            "suivi du mot-clé |cmd|sur|ff| (|cmd|on|ff| en anglais), suivi " \
            "du nom de l'emplacement, suivi du mot-clé |cmd|de|ff| " \
            "(|cmd|of|ff| en anglais), suivi enfin du nom du bonhomme de " \
            "neige, dans l'ordre (faites attention à la syntaxe, " \
            "les mot-clés sont essentiels). " \
            "Les éléments disponibles diffèrent d'un bonhomme de neige " \
            "à l'autre et c'est à vous de les trouver, bien que la " \
            "description du dit bonhomme peut parfois vous y aider."
    
    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire_simple.iter_objets_qtt(" \
                "True), )"
        nom_objet.proprietes["quantite"] = "True"
        nom_objet.proprietes["conteneur"] = "True"
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        salle = personnage.salle
        objet, conteneur = list(dic_masques["nom_objet"].objets_conteneurs)[0]
        emplacement = dic_masques["bh_emplacement"].emplacement
        bonhomme = dic_masques["element_observable"].element
        personnage.agir("neige")
        if not isinstance(bonhomme, BonhommeNeige):
            personnage << "|err|Ceci n'est pas un bonhomme de neige.|ff|"
            return
        
        modele = bonhomme.prototype
        element = modele.get_element(emplacement)
        if element is None or element.etat_min > bonhomme.etat:
            personnage << "|err|Vous ne pouvez rien mettre ici.|ff|"
            return
        
        if not objet.peut_prendre:
            personnage << "Vous ne pouvez pas prendre {} avec vos " \
                    "mains...".format(objet.nom_singulier)
            return
        
        if personnage.nb_mains_libres < 1:
            personnage << "|err|Il vous faut au moins une main " \
                    "de libre.|ff|"
            return
        
        if not element.accepte_objet(objet):
            personnage << "|err|Vous ne pouvez mettre cela ici.|ff|"
            return
        
        if bonhomme.elements.get(element.nom):
            personnage << "|err|Ce bonhomme de neige a déjà quelque " \
                    "chose ici.|ff|"
            return
        
        conteneur.retirer(objet)
        bonhomme.elements[element.nom] = objet
        objet.contenu = bonhomme
        personnage.envoyer_lisser("Vous installez {} {} {} de {}.".format(
                objet.get_nom(), element.connecteur, element.nom_complet,
                bonhomme.get_nom()))
        salle.envoyer_lisser("{{}} s'active autour de {}.".format(
                bonhomme.get_nom()), personnage)
