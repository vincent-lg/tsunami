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


"""Ce fichier décrit la classe FichierConfiguration, détaillée plus bas."""

import re
import textwrap

from .exceptions import *

class FichierConfiguration:
    
    """Cette classe définit un fichier de configuration.
    
    Le fichier créé par cette classe est déjà ouvert. La classe se contente
    de l'analyser et de placer les données dans un dictionnaire.
    
    Elle est également en charge de mettre un jour un fichier en tenant
    compte d'un autre fichier (mettre à jour un modèle en tenant compte
    des données configurées, ici).
    
    """
    
    def __init__(self, nom, chaine, logger):
        """Constructeur d'un fichier de configuration.
        
        On lui passe la chaîne lue dans le fichier, non analysée.
        Cette chaîne contient donc les données brutes, il faut l'analyser.
        
        """
        self.nom = nom
        self.fichier = chaine
        self.donnees = {}
        self.lignes = {}
        self.logger = logger
        
        # On analyse la chaîne
        t_contenu = chaine.split("\n")
        contenu = chaine
        delimiteurs = ('\\', ',', '[', '{', '(')
        
        # On lit les données
        i = 0
        while i < len(t_contenu):
            ligne = t_contenu[i]
            if ligne.strip() == "":
                i += 1
                continue
            elif ligne.lstrip().startswith("#"):
                i += 1
                continue
            elif "=" not in ligne:
                self.logger.warning("[{}:{}]: le signe '=' n'a pas été " \
                        "trouvé ('{}')".format(self.nom, i + 1, ligne))
                i += 1
            else:
                nom_donnee = ligne.split("=")[0].strip()
                donnee = "=".join(ligne.split("=")[1:]).lstrip()
                
                # Si la ligne se poursuit, on continue
                ligne_debut = i
                while ligne.rstrip()[-1] in delimiteurs or \
                        ligne.lstrip().startswith("#"):
                    i += 1
                    if i >= len(t_contenu):
                        break
                    
                    ligne = t_contenu[i]
                    donnee += "\n" + ligne
                
                ligne_fin = i
                self.lignes[nom_donnee] = (ligne_debut, ligne_fin)
                self.donnees[nom_donnee] = donnee
                i += 1
    
    def mettre_a_jour(self, autre_fichier):
        """Met à jour l'attribut 'chaine' en fonction d'un autre fichier.
        
        On parcourt les données de cet autre fichier.
        *   Si la donnée est présente dans self.donnees, on la réécrit
            sans savoir si elle est identique ou non, on l'écrase)
        *   Sinon on ne la réécrit pas.
        
        """
        t_contenu = self.fichier.split("\n")
        for nom_don, val_don in autre_fichier.donnees.items():
            if nom_don in self.donnees.keys(): # la donnée existe
                # On la met à jour
                self.donnees[nom_don] = val_don
                if nom_don not in self.lignes:
                    # La donnée n'a pas été trouvée
                    raise ErreurInterpretation("la donnée {} n'a pas " \
                            "été trouvée dans le fichier à mettre à " \
                            "jour".format(nom_don))
                debut, fin = self.lignes[nom_don]
                nv_val = nom_don + " = " + val_don
                nv_val = nv_val.split("\n")
                t_contenu = t_contenu[:debut] + nv_val + t_contenu[fin + 1:]
        
        self.fichier = "\n".join(t_contenu)

