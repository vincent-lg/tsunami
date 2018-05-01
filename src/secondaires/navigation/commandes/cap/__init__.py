# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Package contenant la commande 'cap'."""

from primaires.interpreteur.commande.commande import Commande
from .creer import PrmCreer
from .etendre import PrmEtendre
from .fermer import PrmFermer
from .liste import PrmListe
from .supprimer import PrmSupprimer
from .voir import PrmVoir

# Constantes
AIDE = """
Cette commande permet de créer, construire, lister et voir les caps
créés. Un cap dans sa forme la plus simple est une ligne droite entre
deux points : le point de départ et le point d'arrivée. Un équipage
peut recevoir l'ordre de suivre ce cap (tenant compte ou non des
obstacles qui pourraient se présenter). Dans sa forme la plus complexe
et la plus utile, un cap est un ensemble de points : le point de
départ puis un certain nombre de points intermédiaires jusqu'au point
d'arrivée, qui peut être le point de départ, si vous voulez par exemple
faire une route de patrouille pour certains navires.
Pour créer un cap, il vous faut vous trouver sur un navire : les
coordonnées du navire seront sélectionnées comme le point de départ
du cap. La première chose est donc d'aller dans le navire et de
l'emmener où vous voulez que le chemin commence, puis d'entrer la
commande %cap% %cap:créer%.
Pour ajouter un point à ce cap (au moins un point de départ et un
point d'arrivée sont nécessaires), restez dans le navire et emmenez-le
aux nouvelles coordonnées du point suivant. C'est pourquoi il est
préférable de voyager sur un navire pilote qui ne sert qu'à sélectionner
les points : souvenez-vous qu'un cap intermédiaire rejoint en ligne
droite deux points. Donc la technique la plus simple, après avoir
créé votre cap, est de manoeuvrer votre navire pilote pour qu'il se
rende aux nouvelles coordonnées, en lui faisant suivre le chemin que
vous comptez faire. Avant de virer, ajoutez un point au chemin en
entrant la commande %cap% %cap:étendre%. De cette façon, le système
trouvera la route d'un chemin en joignant les points par des segments
droits. Une petite précaution est malgré tout à prendre concernant
les terres et autres obstacles qui ne se déplacent pas : si un
équipage a pour objectif de suivre un trajet indiqué, il va essayer
d'amener le navire précisément sur chaque point, ce qui veut dire qu'il
ne pourra pas le faire si la terre est trop proche, car elle va gêner
sa manoeuvre. Essayez de préférence de créer un cap en pleine mer,
à au moins une vingtaine de brasses des côtes les plus proches.
Enfin, si vous voulez faire un cap qui se rejoint (c'est-à-dire
qu'un équipage ayant pour tâche de suivre ce cap va suivre chaque
point pour revenir à son point de départ, et ce, à l'infini), il
vous faut fermer le cap. Cette commande peut être entrée de n'importe
où. Elle va compléter le cap en traçant le dernier segment entre le
dernier point entré grâce à %cap% %cap:étendre% et le point de départ
du cap. Ce dernier cap doit obéir aux mêmes règles (le dernier point
du chemin doit permettre de rejoindre le premier point en ligne
droite). Pour fermer un cap, utilisez la commande %cap% %cap:fermer%.
""".strip()

class CmdCap(Commande):

    """Commande 'cap'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "cap", "course")
        self.groupe = "administrateur"
        self.nom_categorie = "navire"
        self.aide_courte = "manipule les caps maritimes"
        self.aide_longue = AIDE

    def ajouter_parametres(self):
        """Ajout des paramètres."""
        self.ajouter_parametre(PrmCreer())
        self.ajouter_parametre(PrmEtendre())
        self.ajouter_parametre(PrmFermer())
        self.ajouter_parametre(PrmListe())
        self.ajouter_parametre(PrmSupprimer())
        self.ajouter_parametre(PrmVoir())
