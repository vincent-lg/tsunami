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


"""Fichier contenant le type boussole."""

from primaires.interpreteur.editeur.uniligne import Uniligne
from bases.objet.attribut import Attribut
from primaires.objet.types.instrument import Instrument
from corps.fonctions import lisser

class Boussole(Instrument):
    
    """Type d'objet: boussole.
    
    """
    
    nom_type = "boussole"
    
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        Instrument.__init__(self, cle)
        self.precision = 10
        self.etendre_editeur("r", "précision", Uniligne, self, "precision")
    
    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        precision = enveloppes["r"]
        precision.apercu = "{objet.precision}"
        precision.prompt = "Précision (en degré) de la boussole : "
        precision.aide_courte = \
            "Entrez la |ent|précision|ff| de la boussole, |cmd|1|ff| au " \
            "minimum.\n" \
            "Plus le chiffre est bas, plus la boussole est précise.\n" \
            "Entrez |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\n" \
            "Précision actuelle : {objet.precision}"
        precision.type = int
    
    # Actions sur les objets
    def regarder(self, personnage):
        """Quand on regarde la boussole."""
        moi = Instrument.regarder(self, personnage)
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None or \
                salle.navire.etendue is None:
            return moi
        
        navire = salle.navire
        vent = navire.vent.copier()
        vent.tourner_autour_z(180)
        ven_dir = (vent.direction + 90) % 360
        ven_dir = round(ven_dir / self.precision) * self.precision
        nav_dir = (navire.direction.direction + 90) % 360
        nav_dir = round(nav_dir / self.precision) * self.precision
        msg_vent = lisser("Le vent souffle de le {} ({}°).".format(
                vent.nom_direction, ven_dir))
        msg_navire = lisser("Le navire se dirige vers le {} ({}°).".format(
                navire.direction.nom_direction, nav_dir))
        
        moi += "\n\n" + msg_vent + "\n" + msg_navire
        return moi
