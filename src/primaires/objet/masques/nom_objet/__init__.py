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


"""Fichier contenant le masque <nom_objet>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation
from primaires.format.fonctions import *

class NomObjet(Masque):
    
    """Masque <nom_objet>.
    On attend un nom d'objet en paramètre.
    
    """
    
    nom = "nom_objet"
    nom_complet = "nom d'un objet"
    
    def __init__(self):
        """Constructeur du masque"""
        Masque.__init__(self)
        self.proprietes["conteneurs"] = "(personnage.salle.objets_sol, )"
        self.proprietes["type"] = "None"
        self.proprietes["tout_interpreter"] = "True"
    
    @property
    def objet(self):
        """Retourne le premier objet."""
        return self.objets[0][0]
    
    @property
    def objets_seuls(self):
        """Retourne un tuple des objets sans leur conteneur."""
        objets = []
        for o, c in self.objets:
            objets.append(o)
        
        return tuple(objets)
    
    def init(self):
        """Initialisation des attributs"""
        self.objets = []
    
    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        nom = liste_vers_chaine(commande)
        
        if not nom:
            raise ErreurValidation( \
                "Précisez un nom d'objet.")
        
        # Attention : sauf avis contraire, le masque interprète la commande
        # entière. Les "avis contraires" en question sont un masque, comme
        # un mot-clé, cherchant dans les masques précédents
        # Exemple : get <nom_objet> from ...
        # nom_objet se valide. Le mot-clé from n'a plus rien à valider
        # mais il sait qu'il doit chercher dans le masque précédemment validé
        # (ici nom_objet) pour trouver l'objet
        if self.proprietes["tout_interpreter"] == "True":
            commande[:] = []
        self.a_interpreter = nom
        masques.append(self)
        return True
    
    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        nom = self.a_interpreter
        conteneurs = self.conteneurs
        o_type = self.type
        objets = []
        
        for c in conteneurs:
            for o in c:
                if contient(o.nom_singulier, nom):
                    if o_type and not o.prototype.est_de_type(o_type):
                        raise ErreurValidation(
                                "|err|" + o.err_type.format(o.nom_singulier) \
                                + "|ff|")
                    
                    print(o, o.contenu)
                    objets.append((o, o.contenu))
        
        if not objets:
            raise ErreurValidation(
                "|err|Ce nom d'objet est introuvable.|ff|")
        
        self.objets = objets
        
        return True
