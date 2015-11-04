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


"""Fichier contenant la classe Script détaillée plus bas."""

from abstraits.obase import *
from primaires.format.fonctions import *
from primaires.scripting.bloc import Bloc
from primaires.scripting.evenement import Evenement

scripts = []

class Script(BaseObj):

    """Classe contenant un script.

    Un script est un ensemble d'évènements. Chaque instance devant faire
    appel à un évènement doit contenir un attribut possédant un script
    l'identifiant comme l'auteur des évènements qu'il contient.

    Par exemple :
    >>> class Personnage:
    ...     def __init__(self):
    ...         self.script = Script(self)

    Comme indiqué, chaque instance de script peut contenir un ou plusieurs
    évènements qu'il est nécessaire de définir précisément avant l'appel.
    Chaque évènement peut contenir plusieurs sous-évènements. Pour plus
    d'informations, voir la classe Evenement définie dans ce package.

    A noter que c'est l'évènement qui stocke les instructions, pas le script
    lui-même.

    Pour se construire, un script prend en paramètre :
    -   parent -- l'objet qui appellera le script

    """

    _nom = "script"
    _version = 1
    def __init__(self, parent):
        """Constructeur d'un script"""
        BaseObj.__init__(self)
        self.parent = parent
        self.__blocs = {}
        self.__evenements = {}
        self._construire()
        self.init()

    def __getnewargs__(self):
        return (None, )

    def __getitem__(self, evenement):
        """Retourne l'évènement correspondant.

        L'évènement doit être une chaîne de caractères.

        """
        evenement = supprimer_accents(evenement).lower()
        return self.__evenements[evenement]

    def __setstate__(self, dico_attrs):
        """A la récupération du script, appelle init."""
        BaseObj.__setstate__(self, dico_attrs)
        scripts.append(self)

    def init(self):
        """Initialisation du script.

        Cette méthode est à redéfinir dans les classes-filles pour, par
        exemple, ajouter de nouveaux évènements.

        """
        pass

    @property
    def evenements(self):
        return dict(self.__evenements)

    @property
    def blocs(self):
        """Retourne un dictionnaire déréférencé des blocs."""
        return dict(self.__blocs)

    def copier_depuis(self, script):
        """Copie le script self depuis le script indiqué."""
        for evenement in script.evenements.values():
            sa_evenement = supprimer_accents(evenement.nom).lower()
            if sa_evenement in self.__evenements.keys():
                evt = self.__evenements[sa_evenement]
            else:
                evt = self.creer_evenement_dynamique(evenement.nom)
            
            evt.copier_depuis(evenement)
    
    def creer_evenement(self, evenement):
        """Crée et ajoute l'évènement dont le nom est précisé en paramètre.

        L'évènement doit être une chaîne de caractères non vide. Si
        l'évènement existe, le retourne. Sinon, retourne le créé.

        """
        if not evenement:
            raise ValueError("Un nom vide a été passé en paramètre de " \
                    "creer_evenement.")

        sa_evenement = supprimer_accents(evenement).lower()

        if sa_evenement in self.__evenements.keys():
            evt = self.evenements[sa_evenement]
            evt.nom = evenement
            return evt

        nouv_evenement = Evenement(self, evenement)
        self.__evenements[sa_evenement] = nouv_evenement

        return nouv_evenement

    def creer_evenement_dynamique(self, nom):
        """Essaye de créer un évènement dynamique du nom indiqué.

        Retourne l'évènement si l'évènement a pu être créé, None sinon.

        """
        if supprimer_accents(nom) not in \
                importeur.scripting.commandes_dynamiques_sa:
            return None

        commande = importeur.scripting.get_commande_dynamique(nom)
        evenement = self.creer_evenement(commande.nom_francais)
        evenement.aide_courte = commande.aide_courte_evt
        evenement.aide_longue = str(commande.aide_longue_evt)
        var_perso = evenement.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage exécutant la commande"
        var_elt = evenement.ajouter_variable("element", "object")
        var_elt.aide = "l'élément observé par le personnage"
        return evenement

    def supprimer_evenement(self, evenement):
        """Supprime l'évènement en le retirant du script."""
        evenement = supprimer_accents(evenement).lower()
        del self.__evenements[evenement]

    def creer_bloc(self, nom):
        """Crée un nouveau bloc."""
        if nom in self.__blocs:
            raise ValueError("le bloc '{}' existe déjà".format(nom))

        bloc = Bloc(self, nom)
        self.__blocs[nom] = bloc
        return bloc

    def supprimer_bloc(self, nom):
        """Supprime un bloc."""
        if nom not in self.__blocs:
            raise ValueError("le bloc '{}' n'existe pas".format(nom))

        self.__blocs[nom].detruire()
        del self.__blocs[nom]
