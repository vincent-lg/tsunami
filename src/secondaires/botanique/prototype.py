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
from corps.fonctions import valider_cle
from corps.aleatoire import varier
from primaires.format.fonctions import supprimer_accents
from .cycle import Cycle

class PrototypePlante(BaseObj):
    
    """Classe décrivant le prototype d'un végétal.
    
    Les informations contenues dans les objets de ce type sont communes
    à une espèce de plante. On y trouve :
    cle -- la clé identifiante unique de la plante
    croissance -- une liste des cycles de croissance de maturation
    
    Beaucoup d'informations sont définies pour chaque cycle. Une
    cycle dur au minimum un an (souvent plusieurs) et détermine
    la croissance de la plante. Chaque cycle contient plusieurs périodes
    qui reviennent chaque année.
    Par exemple :
        un pommier se trouve au début à l'état de graine (cycle invisible)
        puis à l'état de pouce
        puis à l'état de jeune pommier. Ce cycle contient :
            une période d'arbre nu
            une période de floraison
        un cycle mature
        ...
    
    Pour plus d'informations, consultez la classe Cycle (définie dans
    le fichier cycle.py) et la classe Periode (définie dans le fichier
    periode.py).
    
    """
    
    enregistrer = True
    def __init__(self, cle=""):
        """Constructeur du prototype."""
        BaseObj.__init__(self)
        self.n_id = 1
        if cle:
            valider_cle(cle)
            self.cle = cle
        self.cycles = []
        self.plantes = []
    
    def __getnewargs__(self):
        return ()
    
    def __repr__(self):
        return "<prototype de plante {}>".format(repr(self.cle))
    
    def __str__(self):
        return self.cle
    
    @property
    def valide(self):
        """Retourne True si le prototype est valide, False sinon.
        
        Un prototype est valide si il défini au moins un cycle et si chacun
        de ses cycles contient au moins une période.
        
        """
        return len(self.cycles) > 0 and all(len(c.periodes) > 0 for c in \
                self.cycles)
    
    def ajouter_cycle(self, nom, age):
        """Ajoute un cycle et le retourne.
        
        Si le cycle existe (le nom ou l'âge est déjà pris), lève une exception
        ValueError.
        
        """
        if self.est_cycle(nom):
            raise ValueError("le cycle {} existe déjà".format(nom))
        
        cycle = Cycle(nom.lower(), age, self)
        self.cycles.append(cycle)
        return cycle
    
    def est_cycle(self, nom):
        """Retourne True si le cycle est trouvé, False sinon.
        
        La recherche ne tient pas compte des accents ou majuscules /
        minuscules.
        
        """
        nom = supprimer_accents(nom).lower()
        for cycle in self.cycles:
            if supprimer_accents(cycle.nom) == nom:
                return True
        
        return False
    
    def get_cycle(self, nom):
        """Retourne le cycle si existe.
        
        Si il n'existe pas, lève l'exception ValueError.
        
        """
        nom = supprimer_accents(nom).lower()
        for cycle in self.cycles:
            if supprimer_accents(cycle.nom) == nom:
                return cycle
        
        raise ValueError("cycle {} introuvable".format(nom))
    
    def supprimer_cycle(self, nom):
        """Supprime le cycle donné.
        
        Si le cycle n'est pas trouvé, lève l'exception ValueError.
        
        """
        nom = supprimer_accents(nom).lower()
        for cycle in list(self.cycles):
            if supprimer_accents(cycle.nom) == nom:
                self.cycles.remove(cycle)
                cycle.detruire()
                return
        
        raise ValueError("cycle {} introuvable".format(nom))
        
    def detruire(self):
        """Destruction du prototype."""
        for plante in list(self.plantes):
            if plante.e_existe:
                importeur.botanique.supprimer_plante(plante.identifiant)
        
        for cycle in self.cycles:
            cycle.detruire()
        
        BaseObj.detruire(self)
