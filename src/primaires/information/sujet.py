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


"""Fichier contenant la classe SujetAide, détaillée plus bas."""

from abstraits.id import ObjetID
from primaires.format.description import Description
from bases.collections.liste_id import ListeID
from primaires.format.fonctions import supprimer_accents

class SujetAide(ObjetID):
    
    """Classe représentant un sujet d'aide.
    
    Un sujet d'aide est une aide disponible in-game sur un sujet précis.
    Il peut être consultable par un certain groupe de personnes (seulement
    les administrateurs du jeu, par exemple) et peut être lié à d'autres
    sujets.
    
    Ses attributs sont :
        titre -- le titre du sujet
        resume -- un résumé du sujet (50 caractères max)
        contenu -- le contenu du sujet d'aide
        mots_cles -- des mots-clés pointant vers ce sujet
        str_groupe -- une chaîne décrivant le groupe autorisé
        sujets_lies -- les sujets liés (des objets SujetAide contenus
                       dans une liste)
    
    """
    
    groupe = "aide"
    sous_rep = "aide/sujets"
    def __init__(self, titre):
        """Constructeur du sujet d'aide."""
        ObjetID.__init__(self)
        self._titre = titre.lower().split(" ")[0]
        self._pere = None
        self.resume = "sujet d'aide"
        self.contenu = Description(parent=self)
        self.mots_cles = []
        self._str_groupe = ""
        self.__sujets_lies = ListeID(parent=self)
        self.__sujets_fils = ListeID(parent=self)
    
    def __getnewargs__(self):
        return ("", )
    
    def __str__(self):
        return "aide:" + self._titre
    
    def _get_titre(self):
        return self._titre
    def _set_titre(self, titre):
        titre = titre.lower().split(" ")[0]
        if titre in [supprimer_accents(s.titre) for s in \
                type(self).importeur.information.sujets] or type(self). \
                importeur.information.get_sujet_par_mot_cle(titre):
            self._titre = titre
    titre = property(_get_titre, _set_titre)
    
    def _get_pere(self):
        if self._pere is None:
            return None
        else:
            return type(self).importeur.parid["aide"][self._pere]
    def _set_pere(self, pere):
        self._pere = pere.id if pere else None
    pere = property(_get_pere, _set_pere)
    
    @property
    def str_mots_cles(self):
        return ", ".join(self.mots_cles) or "aucun mot-clé"
    
    def _get_str_groupe(self):
        return self._str_groupe or "aucun"
    def _set_str_groupe(self, nom_groupe):
        self._str_groupe = nom_groupe
    str_groupe = property(_get_str_groupe, _set_str_groupe)
    
    @property
    def grp(self):
        groupe = type(self).importeur.interpreteur.groupes[self._str_groue]
        return groupe
    
    @property
    def sujets_lies(self):
        """Retourne une liste déréférencée des sujets liés."""
        return [s for s in self.__sujets_lies if s is not None]
    
    @property
    def str_sujets_lies(self):
        """Retourne une chaîne contenant les sujets liés."""
        return ", ".join([s.titre for s in self.sujets_lies]) or "aucun sujet lié"
    
    @property
    def sujets_fils(self):
        """Retourne une liste déréférencée des sujets fils."""
        return [s for s in self.__sujets_fils if s is not None]
    
    @property
    def tab_sujets_fils(self):
        """Retourne un tableau des sujets fils."""
        lignes = []
        taille = max([len(s.titre) for s in self.sujets_fils] or (10, ))
        sep = "+" + (taille + 2) * "-" + "+" + 52 * "-" + "+"
        en_tete = sep + "\n" + "| |tit|" + "Sujet".ljust(taille) + "|ff| |"
        en_tete += " |tit|" + "Résumé".ljust(50) + "|ff| |\n" + sep
        for s in self.sujets_fils:
            ligne = "| |ent|" + s.titre.ljust(taille) + "|ff| | "
            ligne += s.resume.ljust(50) + " |"
            lignes.append(ligne)
        if lignes:
            return en_tete + "\n" + "\n".join(lignes) + "\n" + sep
        else:
            return "|att|Aucun sujet affilié.|ff|"
    
    def est_lie(self, sujet):
        """Retourne True si le sujet est lié, False sinon."""
        return sujet in self.__sujets_lies and self in sujet.__sujets_lies
    
    def ajouter_lie(self, sujet):
        """Lie un sujet au courant."""
        self.__sujets_lies.append(sujet)
        sujet.__sujets_lies.append(self)
        self.enregistrer()
        sujet.enregistrer()
    
    def supprimer_lie(self, sujet):
        """Supprime un sujet de la liste des sujets liés."""
        self.__sujets_lies.remove(sujet)
        sujet.__sujets_lies.remove(self)
        self.enregistrer()
        sujet.enregistrer()
    
    def est_fils(self, sujet):
        """Retourne True si le sujet est fils de celui-ci, False sinon."""
        return sujet in self.__sujets_fils and sujet.pere is self
    
    def ajouter_fils(self, sujet):
        """Ajoute le sujet aux fils."""
        self.__sujets_fils.append(sujet)
        sujet.pere = self
        self.enregistrer()
        sujet.enregistrer()
    
    def supprimer_fils(self, sujet):
        """Supprime le sujet des fils."""
        self.__sujets_fils.remove(sujet)
        sujet.pere = None
        self.enregistrer()
        sujet.enregistrer()
    
    def echanger_fils(self, sujet, bas=False):
        """Change un fils de place vers le haut ou le bas de la liste."""
        i = self.sujets_fils.index(sujet)
        if i == 0 and not bas:
            raise ValueError("le sujet est déjà en haut de la liste")
        elif i == len(self.__sujets_fils) - 1 and bas:
            raise ValueError("le sujet est déjà en bas de la liste")
        del self.__sujets_fils[i]
        if not bas:
            self.__sujets_fils.insert(i - 1, sujet)
        else:
            self.__sujets_fils.insert(i + 1, sujet)

ObjetID.ajouter_groupe(SujetAide)
