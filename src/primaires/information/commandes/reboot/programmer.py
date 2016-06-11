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


"""Fichier contenant le paramètre 'programmer' de la commande 'reboot'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmProgrammer(Parametre):

    """Commande 'reboot programmer'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "programmer", "program")
        self.tronquer = True
        self.schema = "<nombre>"
        self.aide_courte = "programme un reboot"
        self.aide_longue = \
            "Cette sous-commande programme un reboot. Vous devez " \
            "préciser en paramètre le temps en minutes avant reboot. " \
            "Par exemple %reboot% %reboot:programmer%|ent| 15|ff| " \
            "pour programmer un reboot dans 15 minutes."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        nombre = dic_masques["nombre"].nombre
        s = "s" if nombre > 1 else ""
        personnage << "Programmation d'un reboot dans {} minute{s}.".format(
                nombre, s=s)
        importeur.information.programmer_reboot(nombre * 60)
