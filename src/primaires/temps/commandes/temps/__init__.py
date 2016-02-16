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


"""Package contenant la commande 'temps'.

"""

from datetime import datetime, timedelta
import re
from time import time

from primaires.format.date import get_date
from primaires.interpreteur.commande.commande import Commande

# Constantes
EXP = (
    re.compile("^(m)([0-9]+)\-([0-9]+)\-([0-9]+)\s*([0-9]+)\:([0-9]+)$", re.I),
    re.compile("^(m)([0-9]+)\-([0-9]+)\s*([0-9]+)\:([0-9]+)$", re.I),
    re.compile("^(m)([0-9]+)\s*([0-9]+)\:([0-9]+)$", re.I),
    re.compile("^(m)\s*([0-9]+)\:([0-9]+)$", re.I),
    re.compile("^(r)([0-9]+)\-([0-9]+)\-([0-9]+)\s*([0-9]+)\:([0-9]+)$", re.I),
    re.compile("^(r)([0-9]+)\-([0-9]+)\s*([0-9]+)\:([0-9]+)$", re.I),
    re.compile("^(r)([0-9]+)\s*([0-9]+)\:([0-9]+)$", re.I),
    re.compile("^(r)\s*([0-9]+)\:([0-9]+)$", re.I),
)

class CmdTemps(Commande):

    """Commande 'temps'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "temps", "time")
        self.schema = "(<texte_libre>)"
        self.aide_courte = "affiche la date et l'heure de l'univers"
        self.aide_longue = \
            "Cette commande affiche la date et l'heure actuelles de l'univers."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        temps = importeur.temps.temps
        mtn = datetime.now()
        r_annee = mtn.year
        r_mois = mtn.month
        r_jour = mtn.day
        r_heure = mtn.hour
        r_minute = mtn.minute
        m_annee = temps.annee
        m_mois = temps.mois
        m_jour = temps.jour
        m_heure = temps.heure
        m_minute = temps.minute
        cnv = None
        if dic_masques["texte_libre"]:
            texte = dic_masques["texte_libre"].texte

            # Essaye d'obtenir les informations depuis l'expression
            for expression in EXP:
                reg = expression.search(texte)
                if reg:
                    groupe = reg.groups()

                    if groupe[0] == "m":
                        annee = m_annee
                        mois = m_mois
                        jour = m_jour
                    else:
                        annee = r_annee
                        mois = r_mois
                        jour = r_jour

                    if len(groupe) == 3:
                        cnv, heure, minute = groupe
                    elif len(groupe) == 4:
                        cnv, jour, heure, minute = groupe
                    elif len(groupe) == 5:
                        cnv, mois, jour, heure, minute = groupe
                    else:
                        cnv, annee, mois, jour, heure, minute = groupe

                    annee = int(annee)
                    mois = int(mois)
                    jour = int(jour)
                    heure = int(heure)
                    minute = int(minute)
                    break

            # Affichage simple de la transformation attendue
            if cnv == "m":
                msg = "Transformation vers le temps réel de "
                # Calcul du nombre de secondes IRL
                secondes = (annee - m_annee) * 31104000
                secondes += (mois - m_mois) * 2592000
                secondes += (jour - m_jour) * 86400
                secondes += (heure - m_heure) * 3600
                secondes += (minute - m_minute) * 60
                secondes = int(secondes * temps.vitesse_ecoulement)
                projection = mtn + timedelta(seconds=secondes)
                resultat = "{} (secondes={})".format(get_date(
                        projection).capitalize(), secondes)
            elif cnv == "r":
                msg = "Transformation vers le temps IG de "
                resultat = "inconnu"
            else:
                personnage << "|err|Syntaxe de temps invalide.|ff|"
                return

            msg += "{}-{}-{} {}:{}".format(annee, mois, jour, heure, minute)
            msg += "\n" + resultat
            personnage << msg
            return

        personnage << "Nous sommes le {}.\nIl est {}.".format(
                temps.date_formatee, temps.heure_formatee)
