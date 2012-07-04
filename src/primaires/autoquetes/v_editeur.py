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

"""Fichier contenant la clase ValidateurEditeur, définie plus bas."""

import os

from yaml import load

from corps.arborescence import getcwd

## Constantes de validation
CHAMPS_OBLIGATOIRES = (
    "type",
    "aide",
)

CHAMPS_FACULTATIFS = (
    "attribut",
)

CHAMPS_OBLIGATOIRES_TYPE = {
    "entier": (),
    "flottant": (),
}

CHAMPS_FACULTATIFS_TYPE = {
    "entier": (
        "minimum",
        "maximum",
        "unite",
    ),
    "flottant": (
        "minimum",
        "maximum",
        "unite",
    ),
}

CHAMPS_TYPE = {}
for nom_type, champs in CHAMPS_OBLIGATOIRES_TYPE.items():
    CHAMPS_TYPE[nom_type] = CHAMPS_OBLIGATOIRES + CHAMPS_FACULTATIFS + \
            champs + CHAMPS_FACULTATIFS_TYPE[nom_type]

class ValidateurEditeur:
    
    """Cette classe contient des méthodes pour valider les éditeurs autoquête.
    
    Les méthodes définies dans cette classes sont des méthodes abstraites :
    cette classe n'est qu'une enveloppe contenant plusieurs fonctionnalités.
    Voici les différentes méthodes à utiliser dans l'ordre :
        get_config -- retourne la configuration de l'éditeur
        valider_config -- valide la configuration du fichier
        etendre_config -- étend la configuration définie.
    
    Voire chaque méthode pour plus d'informations.
    
    """
    
    @staticmethod
    def get_config(nom):
        """Retourne, si peut être chargée, la configuration YAML de l'éditeur.
        
        On doit préciser en paramètre :
            nom -- le nom du répertoire dans laquel récupérer l'information
        
        Est retourné :
            None si le fichier ne peut être trouvée
            Une liste de dictionnaires permettant d'étendre la configuration
        
        Si une erreur se produit dans le parsage du fichier YAML ou si
        le fichier n'a pas la bonne structure, une exception est levée.
        
        """
        chemin = getcwd() + os.sep + "types" + os.sep + nom + os.sep + \
                "editeur.yml"
        if not os.path.exists(chemin):
            return None
        
        if not os.path.isfile(chemin):
            raise os.error(chemin + " n'est pas un fichier")
        
        if not os.access(chemin, os.R_OK):
            raise os.error(chemin + " ne peut être lu")
        
        with open(chemin, "r") as fichier:
            config = load(fichier)
        
        # Vérifie la syntaxe du fichier
        if not isinstance(config, list):
            raise ValueError("la syntaxe du fichier YAML {} n'est pas " \
                    "valide. Une liste de dictionnaires est attendue".format(chemin))
        
        for elt in config:
            if not isinstance(elt, dict):
                raise ValueError("la syntaxe du fichier YAML {} n'est pas " \
                        "valide. Une liste de dictionnaires est " \
                        "attendue".format(chemin))
        
        return config
    
    @staticmethod
    def valider_config(config):
        """Valide la configuration.
        
        La configuration passée en paramètre doit être sous la forme d'une
        liste de dictionnaires. Chaque élément de la liste représente les
        informations à préciser pour construire un éditeur du type indiqué.
        
        Si une erreur survient, une exception ValueError est levée explicitant le problème.
        
        """
        for e_nom, info in config.items():
            # D'abord vérifie les champs obligatoires
            for nom in CHAMPS_OBLIGATOIRES:
                if nom not in info:
                    raise Valueerror("le champ {} pour l'éditeur {} n'est " \
                            "pas précisé".format(nom, e_nom))
            
            e_type = info["type"]
            if e_type not in CHAMPS_OBLIGATOIRES_TYPES:
                raise ValueError("le type d'éditeur {} pour {} n'existe " \
                        "pas".format(e_type, e_nom))
            
            for nom in info.keys():
                if nom not in CHAMPS_TYPE[e_type]:
                    raise ValueError("l'information {} est inconnue pour le " \
                            "type d'éditeur {} ({})".format(nom, e_type,
                            e_nom))
    
    @staticmethod
    def etendre_config(classe, config):
        """Étend l'éditeur de configuration de la classe.
        
        Chaque classe de la hiérarchie doit avoir un attribut 'editeur'
        contenant la liste des informations de l'éditeur construits sur
        ce type. Cette information est une liste de dictionnaires, comme
        la config. Pour constituer cet attribut de classe, on cherche
        la configuration du parent (qui a normalement été déjà définie)
        et on l'étend avec la nouvelle configuration. Si celle-ci est None,
        la liste est considérée vide.
        
        """
        config = config and config or []
        editeur = None
        for parent in classe.__bases__:
            if hasattr(parent, "editeur"):
                editeur = list(parent.editeur)
        
        if editeur is None:
            if classe.parent is None:
                editeur = []
            else:
                raise ValueError("la configuration d'éditeur du parent de {} " \
                        "n'a pu être trouvée".format(classe))
        
        editeur.extend(config)
        classe.editeur = editeur
