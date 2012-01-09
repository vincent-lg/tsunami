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


"""Fichier contenant la classe SalleNavire, détaillée plus bas."""

from collections import OrderedDict

from primaires.salle.salle import Salle

# Constantes
NOMS_SORTIES = OrderedDict()
NOMS_SORTIES["sud"] = "arrière"
NOMS_SORTIES["ouest"] = "bâbord"
NOMS_SORTIES["nord"] = "avant"
NOMS_SORTIES["est"] = "tribord"
NOMS_SORTIES["bas"] = "bas"
NOMS_SORTIES["haut"] = "haut"

ARTICLES = {
    "bâbord": "",
    "tribord": "",
    "avant": "l'",
    "arrière": "l'",
    "bas": "le",
    "haut": "le",
}

NOMS_CONTRAIRES = {
    "nord": "sud",
    "ouest": "est",
    "est": "ouest",
    "sud": "nord",
    "haut": "bas",
    "bas": "haut",
}

class SalleNavire(Salle):
    
    """Classe représentant une salle de navire.
    
    Une salle de navire est une salle standard comportant quelques
    informations supplémentaires, comme les éléments dérfinis dans cette
    salle ou le navire qu'elles composent.
    
    """
    
    def __init__(self, zone, mnemonic, r_x=0, r_y=0, r_z=0, modele=None,
            navire=None):
        """Constructeur du navire."""
        Salle.__init__(self, zone, mnemonic, valide=False)
        self.navire = navire
        self.modele = modele
        self.elements = []
        self.r_x = r_x
        self.r_y = r_y
        self.r_z = r_z
        if navire:
            # Déduit les coordonnées
            pass
    
    @property
    def r_coords(self):
        """Retourne les coordonnées relatives de la salle."""
        return (self.r_x, self.r_y, self.r_z)
    
    @property
    def passerelle(self):
        """Retourne la passerelle de la salle ou None."""
        elts = [e for e in self.elements if e.nom_type == "passerelle"]
        print(elts, self.elements)
        if elts:
            return elts[0]
        
        return None
    
    @property
    def ancre(self):
        """Retourne l'ancre de la salle ou None."""
        elts = [e for e in self.elements if e.nom_type == "ancre"]
        if elts:
            return elts[0]
        
        return None
    
    @property
    def voiles(self):
        """Retourne les voiles de la salle."""
        return [e for e in self.elements if e.nom_type == "voile"]
    
    @property
    def gouvernail(self):
        """Retourne le gouvernail de la salle ou None."""
        elts = [e for e in self.elements if e.nom_type == "gouvernail"]
        if elts:
            return elts[0]
        
        return None
    
    @property
    def loch(self):
        """Retourne le loch de la salle ou None."""
        elts = [e for e in self.elements if e.nom_type == "loch"]
        if elts:
            return elts[0]
        
        return None
    
    @property
    def rames(self):
        """Retourne les rames de la salle ou None."""
        elts = [e for e in self.elements if e.nom_type == "rames"]
        if elts:
            return elts[0]
        
        return None
    
    def ajouter_element(self, element):
        """Ajoute un élément dans la salle."""
        self.elements.append(element)
        self.enregistrer()
    
    def retirer_element(self, cle):
        """Retire l'élément de cle indiqué."""
        for i, elt in enumerate(self.elements):
            if elt.cle == cle:
                del self.elements[i]
                self.enregistrer()
                return
        
        raise ValueError("l'élément {} n'a pas pu être trouvé".format(cle))
    
    def decrire_plus(self, personnage):
        """Ajoute les éléments observables dans la description de la salle."""
        msg = []
        for element in self.elements:
            msg.append(element.get_description_ligne(element, personnage))
        
        return "\n".join(msg)
    
    def get_elements_observables(self, personnage):
        """Retourne la liste des éléments observables."""
        elts = Salle.get_elements_observables(self, personnage)
        for element in self.elements:
            elts.append(element)
        
        return elts
