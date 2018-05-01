# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Package contenant la commande 'appâter'."""

from primaires.interpreteur.commande.commande import Commande

class CmdAppater(Commande):
    
    """Commande 'appâter'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "appâter", "bait")
        self.schema = "<nom_objet>"
        self.aide_courte = "appâte un ameçon"
        self.aide_longue = \
            "Cette commande permet d'appâter un hameçon. Vous devez " \
            "tenir une canne à pêche et préciser le nom de l'appât. " \
            "Certains appâts, plus durs à trouver que d'autres, " \
            "attirent aussi plus le poisson et peuvent augmenter la " \
            "chance de pêcher une prise rare. Dès lors que vous avez " \
            "pêché quelque chose, vous devez appâter de nouveau " \
            "l'hameçon de la canne avant de la relancer."
    
    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire_simple.iter_objets_qtt(" \
                "True), )"
        nom_objet.proprietes["quantite"] = "True"
        nom_objet.proprietes["conteneur"] = "True"
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande."""
        appat = dic_masques["nom_objet"].objet
        if not appat.est_de_type("appât"):
            personnage << "|err|Vous ne pouvez appâter {}.|ff|".format(
                    appat.get_nom())
            return
        
        canne = None
        for membre in personnage.equipement.membres:
            for objet in membre.equipe:
                if objet.est_de_type("canne à pêche"):
                    canne = objet
                    break
        
        if canne is None:
            personnage << "|err|Vous n'équipez aucune canne à pêche.|ff|"
            return
        
        if (getattr(canne, "appat", None) is not None
                and appat.prototype == canne.appat.prototype):
            personnage << "|err|Vous avez déjà appâté {} avec {}.|ff|".format(
                    canne.get_nom(), appat.get_nom())
            return
        
        personnage.agir("appater")
        appat.contenu.retirer(appat)
        a_appat = canne.appat
        if a_appat:
            importeur.objet.supprimer_objet(a_appat.identifiant)
        
        canne.appat = appat
        personnage << "Vous appâtez {} avec {}.".format(
                canne.get_nom(), appat.get_nom())
        personnage.salle.envoyer("{{}} appâte {} avec {}.".format(
                canne.get_nom(), appat.get_nom()), personnage)
