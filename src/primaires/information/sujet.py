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

from abstraits.obase import BaseObj
from primaires.format.description import Description
from primaires.format.fonctions import supprimer_accents, couper_phrase

class SujetAide(BaseObj):
    
    """Classe représentant un sujet d'aide.
    
    Un sujet d'aide est une aide disponible in-game sur un sujet précis.
    Il peut être consultable par un certain groupe de personnes (seulement
    les administrateurs du jeu, par exemple) et peut être lié à d'autres
    sujets.
    
    Ses attributs sont :
        cle -- la clé identifiant le sujet pour les immortels
        titre -- le titre du sujet
        contenu -- le contenu du sujet d'aide
        mots_cles -- des mots-clés pointant vers ce sujet
        str_groupe -- une chaîne décrivant le groupe autorisé
        sujets_lies -- les sujets liés (des objets SujetAide contenus
                       dans une liste)
    
    """
    
    enregistrer = True
    _nom = "sujet_aide"
    _version = 1
    def __init__(self, cle):
        """Constructeur du sujet d'aide."""
        BaseObj.__init__(self)
        self.cle = cle
        self.titre = "un sujet d'aide"
        self.pere = None
        self.contenu = Description(parent=self, scriptable=False)
        self.mots_cles = []
        self._str_groupe = "joueur"
        self.__sujets_lies = []
        self.__sujets_fils = []
    
    def __getnewargs__(self):
        return ("", )
    
    def __str__(self):
        return "aide:" + self.titre
    
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
        return ", ".join([s.titre for s in self.sujets_lies]) or \
                "aucun sujet lié"
    
    @property
    def sujets_fils(self):
        """Retourne une liste déréférencée des sujets fils."""
        return [s for s in self.__sujets_fils if s is not None]
    
    @property
    def tab_sujets_fils(self):
        """Retourne un tableau des sujets fils."""
        lignes = []
        taille = max([len(s.titre) for s in self.sujets_fils] or (10, ))
        if taille > 30:
            taille = 30
        
        sep = "+" + 17 * "-" + "+" + (taille + 2) * "-" + "+"
        en_tete = sep + "\n" + "| |tit|" + "Sujet".ljust(15) + "|ff| |"
        en_tete += " |tit|" + "Titre".ljust(taille) + "|ff| |\n" + sep
        for s in self.sujets_fils:
            ligne = "| |ent|" + s.cle.ljust(15) + "|ff| | "
            ligne += couper_phrase(s.titre, taille).ljust(taille) + " |"
            lignes.append(ligne)
        if lignes:
            return en_tete + "\n" + "\n".join(lignes) + "\n" + sep
        else:
            return "|att|Aucun sujet affilié.|ff|"
    
    def sommaire(self, personnage, indent=""):
        """Renvoie le sommaire du sujet, si sommaire il y a."""
        ret = ""
        i = 1
        for sujet in self.sujets_fils:
            if importeur.interpreteur.groupes.explorer_groupes_inclus(
                    personnage.grp, sujet.str_groupe):
                ret += "\n" + indent + str(i) + ". |cmd|"
                ret += sujet.titre.capitalize() + "|ff|"
                if self.sujets_fils:
                    ret += sujet.sommaire(personnage, \
                            indent=indent+"{}.".format(i))
                i += 1
        return ret
    
    def est_lie(self, sujet):
        """Retourne True si le sujet est lié, False sinon."""
        return sujet in self.__sujets_lies and self in sujet.__sujets_lies
    
    def ajouter_lie(self, sujet):
        """Lie un sujet au courant."""
        self.__sujets_lies.append(sujet)
        sujet.__sujets_lies.append(self)
    
    def supprimer_lie(self, sujet):
        """Supprime un sujet de la liste des sujets liés."""
        self.__sujets_lies.remove(sujet)
        sujet.__sujets_lies.remove(self)
    
    def est_fils(self, sujet):
        """Retourne True si le sujet est fils de celui-ci, False sinon."""
        return sujet in self.__sujets_fils and sujet.pere is self
    
    def ajouter_fils(self, sujet):
        """Ajoute le sujet aux fils."""
        self.__sujets_fils.append(sujet)
        sujet.pere = self
    
    def supprimer_fils(self, sujet):
        """Supprime le sujet des fils."""
        self.__sujets_fils.remove(sujet)
        sujet.pere = None
    
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
    
    def vider(self):
        """Prépare la destruction du sujet."""
        for s in self.sujets_fils:
            s.pere = self.pere
            if self.pere:
                self.pere.ajouter_fils(s)
        if self.pere is not None:
            self.pere.supprimer_fils(self)
        for s in self.sujets_lies:
            s.supprimer_lie(self)
    
    def afficher_pour(self, personnage):
        """Affiche le sujet d'aide pour personnage."""
        nb_ti = int((31 - len(self.titre)) / 2)
        ret = "|tit|" + "-" * nb_ti + "= " + self.titre.capitalize()
        ret += " =" + "-" * nb_ti
        ret += "|ff|\n"
        if self.sujets_fils:
            ret += "\nSommaire :"
            ret += self.sommaire(personnage) + "\n"
        ret += "\n" + self.afficher_contenu(personnage)
        if self.sujets_lies:
            sujets_lies = []
            for sujet in self.sujets_lies:
                if self.importeur.interpreteur.groupes. \
                        explorer_groupes_inclus(personnage.grp,
                        sujet.str_groupe):
                    sujets_lies.append(sujet)
            if sujets_lies:
                s = len(sujets_lies) > 1 and "s" or ""
                ret += "\n\nSujet{s} lié{s} : |ent|".format(s=s)
                ret += "|ff|, |ent|".join([s.titre for s in sujets_lies])
                ret += "|ff|."
        return ret
    
    def afficher_contenu(self, personnage, ident="", sp="|sp|"):
        """Affiche le contenu de self et ses sujets fils."""
        ret = "\n".join(self.contenu.paragraphes)
        for i, s in enumerate(self.sujets_fils):
            if importeur.interpreteur.groupes.explorer_groupes_inclus(
                    personnage.grp, s.str_groupe):
                ret += "\n" + sp + "\n|tit|" + ident + str(i + 1) + ". " + \
                    s.titre.capitalize() + "|ff|"
            ret += "\n\n" + s.afficher_contenu(personnage,
                    ident=ident + "{}.".format(i + 1), sp="\n\n")
        
        return ret
