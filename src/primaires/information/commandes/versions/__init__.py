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


"""Package contenant la commande 'versions'."""

from primaires.interpreteur.commande.commande import Commande
from .ajouter import PrmAjouter
from .editer import PrmEditer
from .supprimer import PrmSupprimer

class CmdVersions(Commande):
    
    """Commande 'versions'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "versions", "versions")
        self.schema = "(<nombre>)"
        self.aide_courte = "permet de suivre les modifications"
        self.aide_longue = \
            "Cette commande renvoie les |ent|nombre|ff| dernières " \
            "modifications enregistrées par les administrateurs. Si vous " \
            "ne précisez pas de nombre, elle renvoie simplement les " \
            "modifications que vous n'avez pas encore vues."
    
    def ajouter_parametres(self):
        """Ajout des paramètres"""
        prm_ajouter = PrmAjouter()
        prm_editer = PrmEditer()
        prm_supprimer = PrmSupprimer()
        
        self.ajouter_parametre(prm_ajouter)
        self.ajouter_parametre(prm_editer)
        self.ajouter_parametre(prm_supprimer)
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        versions = type(self).importeur.information.versions
        modifs = ""
        if dic_masques["nombre"] is not None:
            nombre = dic_masques["nombre"].nombre
            if nombre > len(versions):
                personnage << "|err|Le nombre précisé est supérieur au " \
                        "nombre de modifications.|ff|"
            else:
                personnage << versions.afficher(nombre)
        else:
            ret = versions.afficher_dernieres_pour(personnage)
            if not ret:
                personnage << "|att|Aucune modification pour l'instant.|ff|"
            else:
                personnage << ret
