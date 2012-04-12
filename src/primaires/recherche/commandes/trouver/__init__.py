# -*-coding:Utf-8 -*

# Copyright (c) 2012 NOEL-BARON Léo
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


"""Package contenant la commande 'trouver'."""

import getopt
import shlex
import re

from primaires.interpreteur.commande.commande import Commande

class CmdTrouver(Commande):
    
    """Commande 'trouver'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "trouver", "find")
        self.nom_categorie = "divers"
        self.schema = "<cherchable> (<message>)"
        self.aide_courte = "permet de rechercher dans l'univers"
        self.aide_longue = \
                "Cette commande est le moteur de recherche de l'univers. " \
                "Elle permet d'effectuer des recherches dans diverses " \
                "catégories, selon des paramètres optionnels fins (la " \
                "syntaxe est celle des options sous Linux). Pour plus de " \
                "l'aide sur une catégorie en particulier, entrez %trouver% " \
                "|cmd| <objet de la recherche> -a|ff|/|cmd|--aide|ff|. Les " \
                "objets de recherche disponibles sont : "
        self.aide_longue += ", ".join(
                [c for c in importeur.recherche.cherchables.keys()]) + "."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        cherchable = dic_masques["cherchable"].cherchable
        # On crée les listes d'options
        opt_courtes = "ao:c:" + cherchable.courtes
        opt_longues = ["aide", "org=", "colonnes="] + cherchable.longues
        retour = []
        tri = ""
        colonnes = []
        if dic_masques["message"] is None:
            retour = cherchable.items
        else:
            message = dic_masques["message"].message
            try:
                options, args = getopt.getopt(shlex.split(message),
                        opt_courtes, opt_longues)
            except (getopt.GetoptError, ValueError) as err:
                personnage << "|err|Une option n'a pas été reconnue ou bien " \
                        "interprétée.|ff|"
                return False
            # On catch les options génériques
            nettoyer = []
            for opt, arg in options:
                if opt in ("-a", "--aide"):
                    personnage << cherchable.aide
                    return
                elif opt in ("-o", "--org"):
                    if arg in cherchable.attributs_tri:
                        tri = arg
                    else:
                        personnage << "|err|Vous ne pouvez trier ainsi.|ff|"
                        tri = ""
                    nettoyer.append((opt, arg))
                elif opt in ("-c", "--colonnes"):
                    try:
                        colonnes = arg.split(", ")
                        for c in colonnes:
                            assert c in cherchable.colonnes
                    except AssertionError:
                        personnage << "|err|Les colonnes spécifiées sont " \
                                "invalides.|ff|"
                        colonnes = []
                    nettoyer.append((opt, arg))
            for couple in nettoyer:
                options.remove(couple)
            try:
                retour = cherchable.tester(options, cherchable.items)
            except TypeError:
                personnage << "|err|Les options n'ont pas été bien " \
                        "interprétées.|ff|"
                return False
        # Post-traitement et affichage
        if not retour:
            personnage << "|att|Aucun retour pour ces paramètres de " \
                    "recherche.|ff|"
        else:
            # On trie la liste de retour
            if tri:
                retour = sorted(retour, key=lambda obj: getattr(obj, tri))
            retour_aff = []
            if colonnes:
                retour_tab = []
                longueurs = []
                for i, o in enumerate(retour):
                    retour_tab.append([])
                    for l, c in enumerate(colonnes):
                        if callable(cherchable.colonnes[c]):
                            aff = cherchable.colonnes[c](o)
                        else:
                            aff = getattr(o, cherchable.colonnes[c])
                        retour_tab[i].append(aff)
                        try:
                            if longueurs[l] < len(aff):
                                longueurs[l] = len(aff)
                        except IndexError:
                            longueurs.append(len(aff))
                    for i, c in enumerate(colonnes):
                        if longueurs[i] < len(c):
                            longueurs[i] = len(c)
                for ligne in retour_tab:
                    c_ligne = []
                    for l, elt in enumerate(ligne):
                        plus = len(re.findall("\|[a-z]{2}\|.*\|ff\|", elt)) * 8
                        plus += len(re.findall("\|[a-z]{3}\|.*\|ff\|",
                                elt)) * 9
                        c_ligne.append(elt.ljust(longueurs[l] + plus))
                    retour_aff.append("| " + " | ".join(c_ligne) + " |")
                somme_lg = -1
                for l in longueurs:
                    somme_lg += l + 3
                en_tete = ["+" + "-" * somme_lg + "+",
                    "| |tit|" + "|ff| | |tit|".join(
                            [c.capitalize().ljust(longueurs[i]) \
                            for i, c in enumerate(colonnes)]) + " |ff||",
                    "+" + "-" * somme_lg + "+"]
                retour_aff = en_tete + retour_aff
                retour_aff += ["+" + "-" * somme_lg + "+"]
            else:
                for o in retour:
                    retour_aff.append(cherchable.afficher(o))
            if not tri and not colonnes:
                retour_aff = sorted(retour_aff)
            personnage << "\n".join(retour_aff)
