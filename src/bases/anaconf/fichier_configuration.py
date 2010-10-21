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


# On aura besoin des regex pour analyser le fichier
import re

# On utilise le module textwrap pour tout aligner
import textwrap

"""Ce fichier décrit la classe FichierConfiguration, détaillée plus bas."""

class FichierConfiguration:
    """Cette classe définit un fichier de configuration.
    Le fichier créé par cette classe est déjà ouvert. La classe se contente
    de l'analyser et de placer les données dans un dictionnaire.
    
    """
    def __init__(self, chaine):
        """Constructeur d'un fichier de configuration.
        On lui passe la chaîne lue dans le fichier, non analysée.
        Cette chaîne contient donc les données brutes, il faut l'analyser.
        
        """
        self.fichier = chaine
        self.donnees = {}
        # On analyse la chaîne
        t_contenu = []
        for ligne in chaine.split('\n'):
            t_contenu.append(ligne.strip())
        contenu = "\n".join(t_contenu)
        # On imbrique les lignes découpées
        # Elles finissent par un signe \
        contenu = contenu.replace("\\\n", " ")
        # A présent, on lit les données
        for i, ligne in enumerate(contenu.split("\n")):
            if ligne == "":
                continue
            elif ligne.startswith("#"): # c'est un commentaire
                continue
            elif "=" not in ligne:
                print("Le signe '=' n'a pas été trouvé sur la ligne " \
                        "{0}: {1}".format(i+1, ligne))
            else:
                nom_donnee = ligne.split("=")[0].strip()
                donnee = "=".join(ligne.split("=")[1:]).strip()
                self.donnees[nom_donnee] = donnee
    
    def mettre_a_jour(self, autre_fichier):
        """On met à jour l'attribut 'chaine' en fonction de cet autre fichier
        de configuration :
        On parcourt les données de cet autre fichier.
        *   Si la donnée est présente dans self.donnees, on la réécrit
            sans savoir si elle est identique ou non, on l'écrase)
        *   Sinon on ne la réécrit pas
        
        """
        for nom_don, val_don in autre_fichier.donnees.items():
            if nom_don in self.donnees.keys(): # la donnée existe
                # On la met à jour
                self.donnees[nom_don] = val_don
                # On utilise les regex pour remplacer la ligne concernée dans
                # self.fichier
                # 1- on cherche la position de la donnée
                t_match = re.search(r"^" + nom_don + r" *=", self.fichier, re.M)
                if t_match is None:
                    # La donnée n'a pas été trouvée
                    raise RuntimeError("la donnée {0} n'a pas été trouvée " \
                            "dans le fichier à mettre à jour".format(nom_don))
                debut = t_match.start()
                egal = t_match.end()
                # 2- maintenant on cherche la fin
                t_match = re.search("(?<!\\\\)\n", self.fichier[debut:])
                fin = debut + t_match.end()
                t_nom = len(nom_don)
                nou_val = (" \\\n" + " " * (t_nom + 2)).join( \
                        textwrap.wrap(val_don, 75 - t_nom))
                self.fichier = self.fichier[:egal] + " " + nou_val + \
                        self.fichier[fin - 1:]

