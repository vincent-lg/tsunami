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


"""Package contenant les différents ordres définis chacun dans un fichier.

La classe-mère des ordres est définie dans le répertoire parent, fichier
ordre.py.

"""

from secondaires.navigation.equipage.volontes.aborder import Aborder
from secondaires.navigation.equipage.volontes.colmater import Colmater
from secondaires.navigation.equipage.volontes.feu import Feu
from secondaires.navigation.equipage.volontes.hisser_voiles import HisserVoiles
from secondaires.navigation.equipage.volontes.jeter_ancre import JeterAncre
from secondaires.navigation.equipage.volontes.lever_ancre import LeverAncre
from secondaires.navigation.equipage.volontes.orienter_voiles import OrienterVoiles
from secondaires.navigation.equipage.volontes.plier_voiles import PlierVoiles
from secondaires.navigation.equipage.volontes.ramer import Ramer
from secondaires.navigation.equipage.volontes.relacher_gouvernail import \
        RelacherGouvernail
from secondaires.navigation.equipage.volontes.relacher_rames import \
        RelacherRames
from secondaires.navigation.equipage.volontes.suivre import Suivre
from secondaires.navigation.equipage.volontes.tenir_gouvernail import \
        TenirGouvernail
from secondaires.navigation.equipage.volontes.tenir_rames import TenirRames
from secondaires.navigation.equipage.volontes.tirer import Tirer
from secondaires.navigation.equipage.volontes.virer import Virer
from secondaires.navigation.equipage.volontes.virer_babord import VirerBabord
from secondaires.navigation.equipage.volontes.virer_tribord import VirerTribord
from secondaires.navigation.equipage.volontes.virer_gouvernail import \
        VirerGouvernail
from secondaires.navigation.equipage.volontes.vitesse import Vitesse
