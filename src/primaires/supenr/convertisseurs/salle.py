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


"""Fichier contenant les convertisseurs de la classe Salle."""

class Convertisseur:
    """Classe pour envelopper les convertisseurs."""
    def depuis_version_0(objet, classe):
        objet.set_version(classe, 1)
        objet._zone = objet._zone.lower()
    def depuis_version_1(objet, classe):
        objet.set_version(classe, 2)
        objet._personnages.parent = objet
    def depuis_version_2(objet, classe):
        objet.set_version(classe, 3)
        objet._nom_zone = objet._zone
        del objet._zone
    def depuis_version_3(objet, classe):
        objet.set_version(classe, 4)
        objet.script._Script__evenements["entre"]["avant"]._Evenement__tests = objet.script._Script__evenements["arrive"]["avant"]._Evenement__tests
        objet.script._Script__evenements["entre"]["apres"]._Evenement__tests = objet.script._Script__evenements["arrive"]["apres"]._Evenement__tests
        objet.script._Script__evenements["dit"]._Evenement__tests = objet.script._Script__evenements["dire"]._Evenement__tests
        del objet.script._Script__evenements["arrive"]
        del objet.script._Script__evenements["dire"]
