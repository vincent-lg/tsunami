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


"""Fichier contenant la classe Instruction, détaillée plus bas ; et
l'exception ErreurExecution.

"""

from collections import OrderedDict

from abstraits.obase import BaseObj, MetaBaseObj
from .exceptions import ErreurScripting

instructions = OrderedDict() # dictionnaire des instructions {nom: classe}

class MetaInstruction(MetaBaseObj):

    """Métaclasse des instructions.

    Pour chaque classe héritée d'Instruction, elle l'ajoute dans
    le dictionnaire instructions.

    Ce dictionnaire est ensuite utilisé par la classe Instruction pour
    des comportements génériques.

    Note : seules les instructions de premier niveau, c'est-à-dire
    directement héritée de la classe Instruction, sont ajoutées dans le
    dictionnaire.
    Les classes héritant de ces classes de premier niveau ne sont pas
    ajoutées.

    """

    def __init__(cls, nom, bases, dict):
        MetaBaseObj.__init__(cls, nom, bases, dict)
        # On ajoute la classe dans le dictionnaire
        if "Instruction" in [classe.__name__ for classe in bases]:
            if nom in instructions:
                raise ValueError("une classe portant le nom {} existe déjà " \
                        "dans le dictionnaire des instructions".format(nom))

            instructions[nom] = cls

class Instruction(BaseObj, metaclass=MetaInstruction):

    """Classe abstraite définissant une instruction.

    Les différents types d'instructions doivent en hériter.
    Par exemple, l'instruction conditionnelle, la fonction, les boucles si
    existent.

    Cette classe propose plusieurs mécanismes génériques de manipulation
    d'instruction.

    """

    cfg = None
    def __init__(self):
        """Construction d'une instruction.

        Note : on ne doit pas construire une instruction mais une de ses
        classes filles.

        """
        BaseObj.__init__(self)
        self.niveau = 0
        self._construire()

    def __getnewargs__(self):
        return ()

    @classmethod
    def peut_interpreter(cls, chaine):
        """Cette classe doit retourner True si elle peut interpréter la chaîne.

        La chaîne passée en paramètre doit donc correspondre à
        un certain schéma attendu par ce type d'instruction.

        Par exemple, la chaîne :
            'si depuis = "ouest":'
        peut être compris par une instruction de type Condition, mais pas
        par une Action.

        Cette méthode est appelée quand on insère une ligne dans l'éditeur
        de script.

        """
        raise NotImplementedError

    @classmethod
    def construire(cls, chaine):
        """Construit une instruction.

        """
        raise NotImplementedError

    @classmethod
    def test_interpreter(cls, chaine):
        """Cherche le type d'instruction pouvant interpréter la chaîne.

        Elle appelle pour cela la méthode peut_interpreter de chaque type
        d'instruction contenu dans le dictionnaire instructions.

        """
        for classe in instructions.values():
            if classe.peut_interpreter(chaine):
                return classe

        raise ValueError("Cette instruction ne peut être interprétée.")

    def deduire_niveau(self, dernier_niveau):
        """Change la valeur du niveau d'indentation de l'instruction.

        Par défaut c'est le même niveau.

        """
        self.niveau = dernier_niveau

    def get_niveau_suivant(self):
        """Retourne le niveau présumé de l'instruction suivante."""
        return self.niveau

class ErreurExecution(ErreurScripting):

    """Classe représentant une erreur d'exécution du scripting.

    Cette exception est levée quand une erreur se produit lors de
    l'exécution d'un script.

    """
    pass
