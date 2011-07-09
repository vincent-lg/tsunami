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


"""Package contenant l'éditeur 'raedit'.
Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from .presentation import EdtPresentation
from primaires.format.fonctions import supprimer_accents, contient

class EdtRaedit(Editeur):
    
    """Classe définissant l'éditeur d'objet 'raedit'.
    
    """
    
    nom = "raedit"
    
    def __init__(self, personnage, objet=None):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Editeur.__init__(self, instance_connexion, None)
        self.personnage = personnage
        self.ajouter_option("q", self.opt_quitter)
        self.ajouter_option("d", self.opt_suppr_race)
    
    def __getnewargs__(self):
        return (None, )
    
    def accueil(self):
        """Message d'accueil de l'éditeur.
        On affiche les races déjà existantes.
        
        """
        msg = "| |tit|Editeur de race|ff|".ljust(87) + "|\n"
        msg += self.opts.separateur + "\n\n"
        msg += \
            " Pour créer ou éditer une race, entrez |ent|son nom|ff| ; " \
            "pour en supprimer une,\n" \
            " entrez |cmd|/d <nom de la race>|ff|.\n\n" \
            " Races existantes :"
        
        races = sorted(type(self).importeur.perso.races, key=str)
        for race in races:
            msg += "\n   |ent|" + race.nom + "|ff|"
        
        if len(races) == 0:
            msg += "\n |att|Aucune race pour le moment.|ff|"
        
        msg += "\n\n [|cmd|Q|ff|]uitter la fenêtre"
         
        return msg
    
    def opt_quitter(self, argument):
        """Option quitter."""
        self.pere.joueur.contextes.retirer()
        self.pere.envoyer("Fermeture de l'éditeur.")
    
    def opt_suppr_race(self, arguments):
        """Option suppression.
        Supprime une race.
        Syntaxe : /d <nom de la race>
        
        """
        nom = supprimer_accents(arguments).lower()
        noms = [(supprimer_accents(race.nom).lower(), race) for race in \
                type(self).importeur.perso.races]
        noms = dict(noms)
        
        try:
            race = noms[nom]
        except KeyError:
            self.pere << "|err|Cette race est introuvable.|ff|"
        else:
            if type(self).importeur.perso.race_est_utilisee(race):
                self.pere << "|err|Cette race est utilisée. Vous ne pouvez " \
                        "la supprimer.|ff|"
            else:
                type(self).importeur.perso.supprimer_race(race.nom)
                self.actualiser()
    
    def interpreter(self, msg):
        """Interprétation du message"""
        msg = msg.lower()
        if msg == "q":
            return self.opt_quitter("")
        
        if len(msg) < 3:
            self.pere << "|err|Ce nom de race est trop court.|ff|"
            return
        
        race = None
        races = sorted(type(self).importeur.perso.races, key=str)
        for t_race in races:
            if contient(t_race.nom, msg):
                race = t_race
                break
        
        if not race:
            race = type(self).importeur.perso.creer_race(msg)
        
        enveloppe = EnveloppeObjet(EdtPresentation, race, "")
        enveloppe.parent = self
        contexte = enveloppe.construire(self.personnage)
        
        self.migrer_contexte(contexte)

