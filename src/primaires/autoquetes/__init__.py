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

"""Fichier contenant le module primaire autoquetes."""

import os

from abstraits.module import *
from corps.arborescence import getcwd
from primaires.format.fonctions import *
from primaires.interpreteur.editeur.presentation import Presentation

from . import commandes
from .editeurs import editeurs
from .types.base import AutoQuete
from .v_editeur import ValidateurEditeur

# Constantes
ATTRIBUTS_AUTOQUETE = (
    "nom_type",
    "est_complete",
)

class Module(BaseModule):
    
    """Classe contenant le module primaire autoquete.
    
    Ce module gère le concept des autoquêtes (connus sous l'ancien système
    sous leur nom anglais "autoquest"). Ces autoquetes (ou quêtes
    automatiques) définissent un comportement plus ou moins aléatoire
    attendu par un joueur, répondant à un besoin plus ou moins réel de
    l'univers. Les différents types d'autoquêtes sont définies dans le
    sous-package types.
    
    L'exemple le plus simple d'autoquête est :
    * Apporter QUELQUE CHOSE à un PNJ et recevoir une récompense.
    
    Le système d'autoquêtes inclut plusieurs sécurité, notamment un système
    permettant d'éviter que les joueurs fassent les autoquêtes en boucle.
    
    La structure d'un t_type d'autoquête doit être assez souple pour répondre
    à la plupart des besoins, présents ou futurs, de ce types de quêtes
    dans l'univers de Vancia. Voire le fichier types/__init__.py pour
    des informations sur la structure des types.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module."""
        BaseModule.__init__(self, importeur, "autoquetes", "primaire")
        self.logger = type(self.importeur).man_logs.creer_logger( \
                "autoquetes", "autoquetes")
        self.commandes = []
        self.types = {}
    
    def init(self):
        """Initialisation du module."""
        self.charger_types()
        
        # On récupère les autoquêtes
        autoquetes = importeur.supenr.charger_groupe(AutoQuete)
        nb_autoquetes = len(autoquetes)
        if autoquetes:
            AutoQuete._no = max(q.id for q in autoquetes)
        
        for autoquete in autoquetes:
            self.autoquetes[autoquete.cle] = autoquete
        
        self.logger.info(format_nb(nb_autoquetes, "{nb} autoquête{s} " \
                "récupérée{s}", fem=True))
        BaseModule.init(self)
    
    def ajouter_commandes(self):
        """Ajout des commandes."""
        self.commandes = [
            commandes.autoquete.CmdAutoquete(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
    
    def charger_types(self):
        """Charge les types d'autoquêtes définis dans le sous-package types."""
        chemin = getcwd() + "/primaires/autoquetes/types"
        for nom in os.listdir(chemin):
            if not nom.startswith("_") and os.path.isdir(chemin + os.sep + nom):
                t_type = __import__("primaires.autoquetes.types." + nom)
                module = getattr(t_type.autoquetes.types, nom)
                if not hasattr(module, "AutoQuete"):
                    raise ValueError("le fichier primaires/autoquetes/" \
                            "types/" + nom + "/__init__.py ne contient pas de classe AutoQuete")
                
                classe = module.AutoQuete
                for attr in ATTRIBUTS_AUTOQUETE:
                    if not hasattr(classe, attr):
                        raise ValueError("la classe d'autoquête " + nom + \
                                " n'a pas d'attribut ou méthode " + repr(attr))
                
                if not hasattr(classe, "parent"):
                    raise ValueError("le type d'autoquête " + nom + \
                            " n'a pas de parent défini")
                
                classe.nom_rep = nom
                self.types[classe.nom_type] = classe
        
        # On ordonne les classes pour qu'elle soit dans l'ordre de plus
        # petit besoin au début. On doit avoir donc en-tête la classe définissant
        # la base qui ne définit rien), puis celle de premier niveau, et ainsi de
        # suite
        noms = []
        for nom, t_type in self.types.items():
            if nom in noms:
                continue
            
            if t_type.parent is None:
                noms.insert(0, nom)
            else:
                if t_type.parent not in self.types:
                    raise ValueError("le parent {} de {} ne peut être " \
                            "trouvé".format(t_type.parent, t_type.nom_type))
                
                if t_type.parent in noms:
                    indice = noms.index(t_type.parent)
                    noms.insert(indice + 1, nom)
                else:
                    noms.append(t_type.parent)
                    noms.append(nom)
        
        classes = [self.types[n] for n in noms]
        
        # On réécrit les classes à présent
        for classe in classes:
            if classe.parent is not None:
                parent = self.types[classe.parent]
                nom_c = classe.nom_type
                nom_c = "".join([(m[0].upper() + m[1:]) for m in \
                        nom_c.split("_")])
                n_classe = type(nom_c, (parent, ), dict(
                        classe.__dict__))
                self.types[classe.nom_type] = n_classe
                classe = n_classe
            
            # Chargement de la configuration des éditeurs du type
            config = ValidateurEditeur.get_config(classe.nom_rep)
            if config:
                ValidateurEditeur.valider_config(config)
            
            ValidateurEditeur.etendre_config(classe, config)
    
    def editer(self, personnage, autoquete):
        """Édite l'autoquête en constituant l'éditeur automatiquement.
        
        On se base sur la configuration dans autoquete.editeur.
        
        """
        editeurs = autoquete.editeur
        presentation = Presentation(personnage.instance_connexion, autoquete)
        for ligne in editeurs:
            nom, info = tuple(ligne.items())
            raccourci = info["raccourci"]
            type = info["type"]
            aide = info["aide"]
            attribut = info.get("attribut")
            edt_type = editeurs[type]
            choix = presentation.ajouter_choix(nom, raccourci, edt_type,
                    autoquete, attribut)
            choix.aide_courte = aide
