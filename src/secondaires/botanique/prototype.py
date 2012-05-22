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


"""Ce fichier contient la classe PlantePrototype, détaillée plus bas."""

from abstraits.obase import BaseObj
from corps.aleatoire import varier
from primaires.format.fonctions import supprimer_accents
from .periode import Periode

class PrototypePlante(BaseObj):
    
    """Classe décrivant le prototype d'un végétal.
    
    Les informations contenues dans les objets de ce type sont communes
    à une espèce de plante. On y trouve :
    cle -- la clé identifiante unique de la plante
    periodes -- une liste des périodes de maturation
    
    Beaucoup d'informations sont définies pour chaque période. Une
    période de la plante correspond à un moment de maturation (par exemple,
    entre le premier jour du mois de janvier et le quatrième jour
    de février à plus ou moins 5 jours, la plante est à l'état
    de pouce, rien n'est récoltable dessus).
    
    """
    
    enregistrer = True
    def __init__(self, cle=""):
        """Constructeur du prototype."""
        BaseObj.__init__(self)
        if cle:
            valider_cle(cle)
            self.cle = cle
        self.periodes = []
        self.plantes = []
    
    def __getnewargs__(self):
        return ()
    
    def __repr__(self):
        return "<prototype de plante {}>".format(repr(self.cle))
    
    def __str__(self):
        return self.cle
    
    def get_periode_actuelle(self):
        """Retourne la période actuelle en fonction du temps.
        
        NOTE : si aucune période ne peut être trouvée correspondant
        au temps actuel, retourne la première période.
        Si aucune période n'est définie, lève une exception ValueError.
        
        La période rest retournée aléatoirement en fonction de la variation
        spécifiée.
        
        """
        if not self.periodes:
            raise ValueError("aucune période définie")
        
        tps = importeur.temps.temps
        jour = tps.jour
        mois = tps.mois
        for periode in self.periodes:
            t_j, t_m = periode.fin
            t_j += varier(t_j, periode.variation, min=None)
            if t_j < 0:
                t_m -= t_j // 30
                t_j = t_j % 30
            
            if jour <= t_j and mois <= t_m:
                return periode
        
        return self.periodes[0]
    
    def ajouter_periode(self, nom):
        """Ajoute une période et la retourne.
        
        Si la période existe (le nom est déjà pris), lève une exception
        ValueError.
        
        """
        if self.est_periode(nom):
            raise ValueError("la période {} existe déjà".format(nom))
        
        periode = Periode(nom.lower(), self)
        self.periodes.ajouter(periode)
        return periode
    
    def est_periode(self, nom):
        """Retourne True si la période est trouvée, False sinon.
        
        La recherche ne tient pas compte des accents ou majuscules /
        minuscules.
        
        """
        nom = supprimer_accents(nom).lower()
        for periode in self.periodes:
            if supprimer_accents(periode.nom) == nom:
                return True
        
        return False
    
    def get_periode(self, nom):
        """Retourne la période si existe.
        
        Si elle n'existe pas, lève l'exception ValueError.
        
        """
        nom = supprimer_accents(nom).lower()
        for periode in self.periodes:
            if supprimer_accents(periode.nom) == nom:
                return periode
        
        raise ValueError("période {} introuvable".format(nom))
    
    def supprimer_periode(self, nom):
        """Supprime la période donnée.
        
        Si al période n'est pas trouvée, lève l'exception ValueError.
        
        """
        nom = supprimer_accents(nom).lower()
        for periode in list(self.periodes):
            if supprimer_accents(periode.nom) == nom:
                self.periodes.remove(periode)
                periode.detruire()
                return
        
        raise ValueError("période {} introuvable".format(nom))
        
    def detruire(self):
        """Destruction du prototype."""
        for plante in self.plantes:
            if plante.e_existe:
                importeur.botanique.supprimer_plante(plante.identifiant)
        
        for periode in self.periodes:
            periode.detruire()
        
        BaseObj.detruire(self)
