# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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

"""Fichier contenant les constantes du module secondaire rapport."""

TYPES = (
    "bug",
    "évolution",
    "suggestion",
)

CATEGORIES = (
    "auberge",
    "autre",
    "botanique",
    "combat",
    "commerce",
    "communication",
    "confort",
    "crafting",
    "cuisine",
    "design",
    "exploration",
    "équilibrage",
    "familier",
    "faute",
    "jeu",
    "magie",
    "météo",
    "modération",
    "navigation",
    "progression",
    "quête",
    "réseau",
    "scripting",
    "sécurité",
    "XP",
)

STATUTS = (
    "nouveau",
    "en cours",
    "fermé",
    "rejeté",
    "dupliqué",
)

CLR_STATUTS = {
    "nouveau": "|vrc|",
    "en cours": "|vr|",
    "fermé": "|grf|",
    "rejeté": "|rgc|",
    "dupliqué": "|cy|",
}

CLR_AVC = (
    "|rg|",
    "|rgc|",
    "|jn|",
    "|bc|",
    "|cyc|",
    "|cy|",
    "|vr|",
    "|vrc|",
)

PRIORITES = (
    "faible",
    "normale",
    "haute",
    "urgente",
    "immédiate",
)

PRIORITES_VAL = {
    "faible": 0,
    "normale": 1,
    "haute": 2,
    "urgente": 3,
    "immédiate": 4,
}

ATTRS_STATUTS = {
    "en cours": (
        ("avancement", 0),
        ("ouvert", True)),
    "fermé": (
        ("avancement", 100),
        ("ouvert", False)),
    "rejeté": (
        ("ouvert", False),),
    "dupliqué": (
        ("ouvert", False ),),
}

COMPLETE = {
    "titre": "titre",
    "description": "description",
}
