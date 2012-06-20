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
# LIABLE FOR ANY teleporterCT, INteleporterCT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant l'action effacer_memoire."""

from primaires.scripting.action import Action

class ClasseAction(Action):
    
    """Efface une mémoire de scripting."""
    
    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.effacer_salle, "Salle", "str")
        cls.ajouter_types(cls.effacer_perso, "Personnage", "str")
        cls.ajouter_types(cls.effacer_objet, "Objet", "str")
    
    @staticmethod
    def effacer_salle(salle, cle):
        """Efface une mémoire de salle."""
        if salle in importeur.scripting.memoires:
            if cle in importeur.scripting.memoires[salle]:
                del importeur.scripting.memoires[salle][cle]
            else:
                raise ErreurExecution("la mémoire {}:{} n'existe pas".format(
                        salle, cle))
            if not importeur.scripting.memoires[salle]:
                del importeur.scripting.memoires[salle]
        else:
            raise ErreurExecution("pas de mémoire pour {}".format(salle))
    
    @staticmethod
    def effacer_perso(personnage, cle):
        """Efface une mémoire de personnage."""
        if personnage in importeur.scripting.memoires:
            if cle in importeur.scripting.memoires[personnage]:
                del importeur.scripting.memoires[personnage][cle]
            else:
                raise ErreurExecution("la mémoire {}:{} n'existe pas".format(
                        personnage, cle))
            if not importeur.scripting.memoires[personnage]:
                del importeur.scripting.memoires[personnage]
        else:
            raise ErreurExecution("pas de mémoire pour {}".format(personnage))
    
    @staticmethod
    def effacer_objet(objet, cle):
        """Efface une mémoire d'objet."""
        if objet in importeur.scripting.memoires:
            if cle in importeur.scripting.memoires[objet]:
                del importeur.scripting.memoires[objet][cle]
            else:
                raise ErreurExecution("la mémoire {}:{} n'existe pas".format(
                        objet, cle))
            if not importeur.scripting.memoires[objet]:
                del importeur.scripting.memoires[objet]
        else:
            raise ErreurExecution("pas de mémoire pour {}".format(objet))
