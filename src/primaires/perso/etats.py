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


"""Fichier contenant la classe Etats, détaillée plus bas."""

from abstraits.obase import BaseObj

class Etats(BaseObj):

    """Classe définissant plusieurs états simultanés.

    On a généralement un conteneur de ce type par personnage. Il contient
    plusieurs états simultanés (par exemple être assis et pêcher en même
    temps). Plusieurs méthodes permettent d'ajouter, retirer et interroger
    cette liste d'états simultanés.

    La méthode ajouter prend au moins un argument, le nom de l'état. Les
    autres arguments sont conditionnés par l'état : par exemple, pour
    s'asseoir, on attend le détail sur lequel on s'asseoit.

    Pour vérifier si une clé d'état est dans la liste, utiliser la méthode
    __contains__ ('assis' in personnage.etats). Vous pouvez
    également utiliser la méthode get qui retourne, si trouvé, l'état
    correspondant à la clé. Si l'état ne peut être trouvé dans la liste,
    retourne None. Cette méthode est surtout utile pour effectuer des
    opérations précises sur certains états.

    Il existe aussi la méthode retirer qui retire un état, si il est présent.

    """

    def __init__(self, personnage):
        """Constructeur du conteneur."""
        BaseObj.__init__(self)
        self.personnage = personnage
        self.__etats = []
        self._construire()

    def __getnewargs__(self):
        return (None, )

    def __repr__(self):
        return "<Etats de {} ({})>".format(
                self.personnage, ", ".join([repr(etat.cle) for etat in \
                self.__etats]))

    def __iter__(self):
        return iter(self.__etats)

    def __contains__(self, cle_etat):
        return cle_etat in [etat.cle for etat in self.__etats]

    def __bool__(self):
        return bool(self.__etats)

    def __getitem__(self, item):
        return self.__etats[item]

    def __getstate__(self):
        retour = {}
        retour["personnage"] = self.personnage
        retour["etats"] = [e.arguments for e in self.__etats]
        return retour

    def __setstate__(self, dico):
        BaseObj.__setstate__(self, {})
        self.personnage = dico["personnage"]
        etats = dico["etats"]
        for tuple in etats:
            cle = tuple[0]
            args = tuple[1:]
            if cle in importeur.perso.etats:
                self.ajouter(cle, *args)

    def get(self, cle_etat):
        """Retourne, si trouvé, l'état dont la clé correspond.

        Retourne None si l'état n'est pas trouvé.

        """
        for etat in self.__etats:
            if etat.cle == cle_etat:
                return etat

        return None

    def ajouter(self, cle_etat, *args, vider=False):
        """Ajoute un état.

        Le premier argument est la clé de l'état. Les arguments facultatifs
        sont passés au constructeur de l'état.

        L'argument 'vider' permet de vider la liste des états, quand
        on a un état qui doit remplacer tous les autres (le combat par
        exemple).

        """
        if vider:
            self.vider()

        try:
            classe = importeur.perso.etats[cle_etat]
        except KeyError:
            raise ValueError("état {} inconnu".format(repr(cle_etat)))

        etat = classe(self.personnage, *args)
        self.__etats.append(etat)

    def retirer(self, cle_etat, supprimer=True):
        """Retire le premier état dont la clé correspond.

        Si le flag supprimer est à True (par défaut il l'est), alors l'état
        est supprimé proprement c'est-à-dire que sa méthode 'supprimer' est
        appelée. Certains états redéfinissent cette méthode pour des
        actions particulières mais il faut s'assurer dans ce cas que la
        méthode ne s'appelle pas récursivement. Si un état supprimé veut
        retirer un autre état (ce sont des états couplés), alors mettre
        le flag supprimer à False pour éviter une récursion infinie.

        """
        for i, etat in enumerate(list(self.__etats)):
            if etat.cle == cle_etat:
                if supprimer:
                    etat.supprimer()

                del self.__etats[i]
                return

    def vider(self):
        """Vide la liste de tous les états."""
        for etat in self.__etats:
            etat.supprimer()

        self.__etats[:] = []

    def reinitialiser(self):
        """Retire les états à retirer au reboot."""
        for etat in list(self.__etats):
            if not etat.sauvegarder_au_reboot:
                etat.supprimer()
                self.__etats.remove(etat)
