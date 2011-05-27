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


"""Package contenant l'éditeur 'rapporteur'.
"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.description import Description
from primaires.interpreteur.editeur.choix import Choix
from primaires.interpreteur.editeur.uniligne import Uniligne

from .enregistrer import Enregistrer

class EdtRapporteur(Presentation):
    
    """Classe définissant l'éditeur de rapport 'rapporteur'.
    
    """
    
    nom = "rapporteur"
    
    def __init__(self, personnage, rapport):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        
        Presentation.__init__(self, instance_connexion, rapport)
        if personnage and rapport:
            self.construire(rapport)
    
    def __getnewargs__(self):
        return (None, None)
    
    def construire(self, rapport):
        """Construction de l'éditeur"""
        
        rapports = type(self).importeur.rapports
        statuts = rapports.statuts
        nomType = rapports.nomType(rapport.typeRapport)
        determinant_nom = rapports.determinant_nom(rapport.typeRapport)
        
        # Titre
        resume = self.ajouter_choix("résumé", "r", Uniligne, rapport,"resume")
        resume.parent = self
        resume.prompt = "Résumé du {} : ".format(nomType)
        resume.apercu = "{objet.resume}"
        resume.aide_courte = \
            "Entrez le |ent|résumé|ff| du " + nomType + " |cmd|/|ff| " \
            "pour revenir à la fenêtre parente.\n\nRésumé actuel : " \
            "|bc|{objet.resume} |ff|"
        
        # Statut
        statut = self.ajouter_choix("statut", "s", Choix, rapport,"statut")
        statut.parent = self
        statut.prompt = "Statut du {} : ".format(nomType)
        statut.apercu = "{objet.statut}"
        statut.aide_courte = \
            "Entrez le numéro du |ent|statut|ff| du " + nomType + "\n" \
            "Statut possible :\n" + \
            "".join([ str(i) + " " + statuts[i] + "\n" for i in range(0,len(statuts))]) + \
            "|cmd|/|ff| pour revenir à la fenêtre parente.\n\nStatut actuel : " + \
            "|bc|{objet.statut} |ff|"
        
        # Description
        description = self.ajouter_choix("description", "d", Description, rapport)
        description.parent = self
        description.apercu = "{objet.description.paragraphes_indentes}"
        description.aide_courte = \
            "| |tit|" + "Description du {}".format(nomType)
        
        # Enregistrer
        enregistrer = self.ajouter_choix("enregistrer le {}".format(nomType), \
                "e", Enregistrer, rapport)
        enregistrer.parent = self
        enregistrer.aide_courte = "| |tit|" + "Enregistrer le {}.".format(nomType)
            
            
