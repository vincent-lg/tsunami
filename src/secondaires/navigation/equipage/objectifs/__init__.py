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


"""Package contenant les objectifs.

Un objectif est un certain but à atteindre. Par exemple, rejoindre
le point (x, y) indiqué. Pour atteindre cet objectif, le commandant
doit donner plusieurs ordres à son équipage ayant pour but de modifier
la vitesse, la direction du navire. Il doit également tenir compte des
chemins disponibles et des obstacles qui pourraient survenir sur tel
ou tel chemin. En somme, un objectif est une partie importante de
l'intelligence artificielle d'un équipage. Un ordre (tel que donné par
équipage/crew ordonner/order) peut donner un objectif mais il est à noter
que, dans ce cas, l'objectif sera décomposé en ordres par un commandant
(c'est-à-dire un capitaine ou second PNJ). Un navire sans capitaine n'est
pas capable de ce type d'objectifs.

Chaque objectif est décrit dans une classe à part.

"""

from secondaires.navigation.equipage.objectifs.couler import Couler
from secondaires.navigation.equipage.objectifs.rejoindre import Rejoindre
from secondaires.navigation.equipage.objectifs.rejoindre_navire import \
        RejoindreNavire
from secondaires.navigation.equipage.objectifs.rejoindre_et_couler import \
        RejoindreEtCouler
from secondaires.navigation.equipage.objectifs.suivre_cap import SuivreCap
from secondaires.navigation.equipage.objectifs.suivre_navire import \
        SuivreNavire
