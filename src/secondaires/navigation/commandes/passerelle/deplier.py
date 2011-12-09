# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   raise of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this raise of conditions and the following disclaimer in the documentation
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


"""Fichier contenant le paramètre 'déplier' de la commande 'passerelle'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.salle.sorties import NOMS_OPPOSES
from primaires.vehicule.vecteur import Vecteur

class PrmDeplier(Parametre):
    
    """Commande 'passerelle déplier'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "déplier", "out")
        self.aide_courte = "déplie la passerelle présente"
        self.aide_longue = \
            "Cette commande déplie la passerelle présente dans la salle où " \
            "vous vous trouvez."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None or \
                salle.navire.etendue is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return
        
        navire = salle.navire
        etendue = navire.etendue
        if not hasattr(salle, "passerelle"):
            personnage << "|err|Il n'y a pas de passerelle ici.|ff|"
            return
        
        passerelle = salle.passerelle
        if not passerelle:
            personnage << "|err|Vous ne voyez aucune passerelle ici.|ff|"
            return
        
        if passerelle.baissee:
            personnage << "|err|Cette passerelle est déjà dépliée.|ff|"
        elif not navire.immobilise:
            personnage << "|err|L'ancre du navire n'a pas été jetée.|ff|"
        else:
            position = Vecteur(*salle.coords.tuple())
            distance = 10
            dest = None
            # Cherche la salle la plus proche
            for t_salle in etendue.cotes.values():
                vecteur = Vecteur(*t_salle.coords.tuple())
                diff = position - vecteur
                if diff.norme < distance:
                    dest = t_salle
                    distance = diff.norme
            
            if dest is None or distance > 1:
                personnage << "|err|Vous ne pouvez déployer votre " \
                        "passerelle ici.|ff|"
                return
            
            try:
                ts_sortie = dest.sorties.get_sortie_par_nom("passerelle")
            except KeyError:
                ts_sortie = None
            
            if ts_sortie is not None:
                personnage << "|err|Vous ne pouvez déplier votre " \
                        "passerelle ici.|ff|"
                return
            
            # On cherche la meilleure sortie
            sorties = ["est", "sud", "ouest", "nord", "sud-est",
                    "sud-ouest", "nord-ouest", "nord-est"]
            
            dir = None
            for nom in sorties:
                oppose = NOMS_OPPOSES[nom]
                if salle.sorties[nom] is None and dest.sorties[oppose] is None:
                    dir = nom
                    break
            
            if dir is None:
                personnage << "|err|Impossible de trouver un emplacement " \
                        "libre pour déplier la passerelle.|ff|"
                return
            
            salle.sorties.ajouter_sortie(dir, "passerelle", "la", dest, oppose)
            salle.enregistrer()
            dest.sorties.ajouter_sortie(oppose, "passerelle", "la", salle, dir)
            dest.enregistrer()
            passerelle.baissee = True
            personnage << "Vous déployez {}.".format(passerelle.nom)
