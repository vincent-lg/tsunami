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


"""Fichier contenant le masque <flags_groupes>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation
from primaires.format.fonctions import *
from primaires.interpreteur.groupe.groupe import FLAGS
class FlagsGroupes(Masque):
    
    """Masque <flags_groupes>.

    On attend un ou plusieurs flags séparés par des espaces.
    
    """
    
    nom = "flags_groupes"
    nom_complet = "flags de groupes"
    
    def init(self):
        """Initialisation des attributs"""
        self.flags = []
    
    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        flags = liste_vers_chaine(commande)
        
        if not flags:
            raise ErreurValidation( \
                "Précisez au moins un flag de groupe.")
        
        commande[:] = []
        self.a_interpreter = flags
        masques.append(self)
        return True
    
    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        flags = self.a_interpreter
        flags = flags.split(" ")
        p_flags = list(FLAGS.keys())
        noms_flags = [supprimer_accents(f) for f in FLAGS.keys()]
        v_flags = []
        for flag in flags:
            n_flag = supprimer_accents(flag).lower()
            if n_flag not in noms_flags:
                raise ErreurValidation(
                        "Flag de groupe {} inconnu.".format(flag))
            v_flag = p_flags[noms_flags.index(n_flag)]
            v_flags.append(v_flag)
        
        self.flags = v_flags
        return True
