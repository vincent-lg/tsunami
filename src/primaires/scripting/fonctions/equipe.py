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


"""Fichier contenant la fonction équipe."""

from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):

    """Teste si un personnage équipe un objet."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.possede_proto, "Personnage", "str")

    @staticmethod
    def possede_proto(personnage, critere):
        """Retourne vrai si le personnage équipe ce prototype, faux sinon.

        Paramètres à préciser :

          * personnage : le personnage à tester
          * critere : le critère de recherche.

        Le critère peut être une simple clé de prototype d'objet. Dans
        ce cas, la fonction cherche si le personnage équipe ce prototype
        d'objet. Plusieurs syntaxes secondaires sont également supportées :

          * +nom du type : vérifie si le personnage équipe un type d'objet.
          * *membre : vérifie si ce membre est équipé.

        Exemples d'utilisation :

          # Teste si le personnage équipe l'objet 'sabre_fer'
          si equipe(personnage, "sabre_fer"):
             ...
          finsi
          # Ou le capture
          sabre = equipe(personnage, "sabre_fer")
          # On peut faire ensuite si sabre: pour vérifier que le sabre
          # de fer a été trouvé équipé par le personnage
          # Teste si le personnage équipe une arme
          si equipe(personnage, "+arme"):
             ...
          finsi
          # Ou, là encore
          arme = equipe(personnage, "+arme")
          si arme:
              # ...
          finsi
          # Test si le personnage porte quelque chose sur son dos
          si equipe(personnage, "*dos"):
              ...
          finsi
          # Si vous voulez savoir de quel objet il s'agit
          cape = equipe(personnage, "*dos")
          si cape:
              # cape contient le premier objet trouvé sur le membre de nom dos
          finsi

        """
        if critere.startswith("*"):
            # C'est un nom de membre
            nom_membre = critere[1:]
            membre = personnage.equipement.get_membre(nom_membre)
            if membre.equipe:
                return membre.equipe[0]

            return membre.tenu
        elif critere.startswith("+"):
            nom_type = critere[1:]
            for o in personnage.equipement.equipes:
                if o.est_de_type(nom_type):
                    return o

            return None
        else:
            prototype = critere
            for o in personnage.equipement.equipes:
                if o.cle == prototype:
                    return o

            return None
