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

from primaires.interpreteur.commande.commande import Commande

# Constantes
AIDE = """
Permet de connaître la date et l'heure IG (in-game), c'est-à-dire
le temps virtuel du MUD. Vous pouvez également utiliser cette commande
pour convertir un temps réel en temps IG ou inversement, ce qui
est parfois utile pour le RP. Par exemple, savoir quel est le temps
in-game correspondant au premier janvier 2017.
Pour ce faire, il suffit d'entrer le temps à convertir en paramètre
de la commande %temps%. La première lettre informe le système si il
s'agit d'un temps réel ou virtuel : |ent|r|ff| signifie que la date
et l'heure qui suivent sont exprimées en temps réel, |ent|m|ff| indique
que la date et 'heure précisé sont exprimées en temps virtuel
(M pour MUD). Le format de la date et de l'heure à préciser est le suivant :
    <année>-<mois>-<jour> <heure>:<minute>
Vous pouvez omettre l'année et n'écrire que le mois, jour, heure et
minute. Vous pouvez omettre le mois, ou même omettre le jour et ne préciser que l'heure. Voici quelques exemples possibles :

+-------------------+------------------------------------------------+
| Paramètre         | Signification                                  |
+-------------------+------------------------------------------------+
| r2017-01-01 00:00 | Le premier janvier 2017 à minuit               |
| r05-18 15:30      | Le 18 mai de cette année à 15:30               |
| r22 20:00         | Le 22 de ce mois et de cette année à 20:00     |
| r18:00            | Aujourd'hui à 18:00                            |
| m50-01-01 00:00   | Le jour 1 du mois 1 de l'année 50 à minuit     |
| m10-22 6:00       | Le jour 22 du mois 10 de cette année à 6:00    |
| m15 19:45         | Le jour 15 de ce mois et cette année à 19:45   |
| m23:00            | Le même jour IG à 23:00                        |
+-------------------+------------------------------------------------+
""".strip("\n")

EXP = (
    re.compile("^(m)([0-9]+)\-([0-9]+)\-([0-9]+)\s+([0-9]+)\:([0-9]+)$", re.I),
    re.compile("^(m)([0-9]+)\-([0-9]+)\s+([0-9]+)\:([0-9]+)$", re.I),
    re.compile("^(m)([0-9]+)\s+([0-9]+)\:([0-9]+)$", re.I),
    re.compile("^(m)\s*([0-9]+)\:([0-9]+)$", re.I),
    re.compile("^(r)([0-9]+)\-([0-9]+)\-([0-9]+)\s+([0-9]+)\:([0-9]+)$", re.I),
    re.compile("^(r)([0-9]+)\-([0-9]+)\s+([0-9]+)\:([0-9]+)$", re.I),
    re.compile("^(r)([0-9]+)\s+([0-9]+)\:([0-9]+)$", re.I),
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
        self.aide_longue = AIDE

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        temps = importeur.temps.temps
        variable = importeur.temps.variable
        mtn = datetime.now()
        r_annee = mtn.year
        r_mois = mtn.month
        r_jour = mtn.day
        r_heure = mtn.hour
        r_minute = mtn.minute
        m_annee = temps.annee
        m_mois = temps.mois + 1
        m_jour = temps.jour + 1
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

            # Transformation
            if cnv == "m":
                mois -= 1
                jour -= 1
                try:
                    variable.changer_IG(annee, mois, jour, heure, minute)
                except ValueError:
                    personnage << "|err|Syntaxe de temps invalide.|ff|"
            elif cnv == "r":
                try:
                    variable.changer_IRL(annee, mois, jour, heure, minute)
                except ValueError:
                    personnage << "|err|Syntaxe de temps invalide.|ff|"
                    return
            else:
                personnage << "|err|Syntaxe de temps invalide.|ff|"
                return

            personnage << "Le {} à {}\nCorrespond au {}.".format(
                    variable.date_formatee, variable.heure_formatee,
                    variable.aff_reelle[3:])
            return

        personnage << "Nous sommes le {}.\nIl est {}.".format(
                temps.date_formatee, temps.heure_formatee)
