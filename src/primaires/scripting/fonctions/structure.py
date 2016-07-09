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


"""Fichier contenant la fonction structure."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne la structure précisée."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.structure, "str", "Fraction")
        cls.ajouter_types(cls.structure_objet, "Objet")
        cls.ajouter_types(cls.structure_salle, "Salle")
        cls.ajouter_types(cls.structure_personnage, "Personnage")

    @staticmethod
    def structure(groupe, id):
        """Retourne la structure spécifiée.

        Cette fonction retourne la structure du groupe et de l'ID
        indiquée. Elle crée une alerte si la structure ne peut être
        trouvée.

        Paramètres à préciser :

          * groupe : le nom du groupe de la sstructure (une chaîne)
          * id : l'identifiant cette structure dans son groupe (un nombre)

        La première structure créée dans un groupe possède l'ID
        1. La seconde l'ID 2. Et ainsi de suite. Ne vous fiez pas
        au nombre de structures du groupe pour déduire les ID,
        cependant. Si les structures d'ID 1, 2 puis 3 sont créées,
        puis que celle d'ID 2 est supprimée, la prochaine créée
        aura l'ID 4. Il y aura donc les structures d'ID 1, 3 et 4.

        Exemples d'utilisation :

          journal = structure("journal", 8)

        """
        st_groupe = importeur.scripting.structures.get(groupe)
        if st_groupe is None:
            raise ErreurExecution("Le groupe {} est inconnu".format(repr(
                    groupe)))

        structure = st_groupe.get(int(id))
        if structure is None:
            raise ErreurExecution("La structure de groupe {} et d'ID " \
                    "{} est introuvable".format(repr(groupe), int(id)))

        return structure

    @staticmethod
    def structure_salle(salle):
        """Retourne une structure simple représentant la salle spécifiée.

        Les structures sont extrêmement pratiques pour modifier
        certaines informations, quand les actions ou fonctions existantes
        ne suffisent pas. Ces modifications peuvent être parfois très
        spécifiques, comme par exemple, dans ce contexte, changer
        le flag de salle en intérieur ou extérieur, ou bien la placer
        en salle illuminée ou non.

        Paramètres à entrer :

          * salle : la salle dont on veut obtenir la structure.

        Cases de la structure :

            * titre : le titre de la salle ;
            * zone : le nom de zone de la salle ;
            * mnemonique : le mnémonique de la salle ;
            * terrain : le nom du terrain de la salle ;
            * interieur : 0 pour extérieur, 1 pour intérieur ;
            * illuminee : 0 pour obscure, 1 pour illuminée.

        Exemples d'utilisation :

          # Récupère la structure de la salle dans la variable 'salle'
          structure = structure(salle)
          # Modifie le titre de la salle
          ecrire structure "titre" "Un champ de lave pétrifié"
          # Passe la salle en extérieur
          ecrire structure "interieur" 0
          # Enregistre les modifications
          appliquer salle structure

        """
        return salle.get_structure()

    @staticmethod
    def structure_personnage(personnage):
        """Retourne une structure simple représentant le personnage spécifié.

        Les structures sont extrêmement pratiques pour modifier
        certaines informations, quand les actions ou fonctions existantes
        ne suffisent pas. Ces modifications peuvent être parfois très
        spécifiques, comme par exemple, dans ce contexte, changer
        le flag pk d'un joueur, ou bien lui donner faim ou soif.

        Paramètres à entrer :

          * personnage : le personnage dont on veut obtenir la structure.

        Cases de la structure : les cases de la structure peuvent
        être différentes en fonction de si vous lui passez en paramètre
        un joueur ou un PNJ. Les trois cas sont détaillés plus bas :
        les cases communes aux joueurs ou PNJ, les cases propres aux
        joueurs et les cases propres aux PNJ. Notez que le signe
        **ls** placé entre parenthèse indique que cette case est
        en lecture seule : vous pouvez récupérer sa valeur, mais
        vous ne pouvez la changer pour des raisons de sécurité.

        Cases pour joueurs et PNJ :

          * groupe (ls) : le nom du groupe auquel appartient le personnage ;
          * salle : la salle (type salle) où le personnage se trouve ;
          * race : le nom de la race du personnage (une chaîne) ;
          * genre (ls) : le nom du genre du personnage (une chaîne) ;
          * soif : un nombre entre 0 (pas soif) et 100 (presque mort0 ;
          * faim : un nombre entre 0 (pas faim) et 100 (presque mort0 ;
          * estomac : le poids de l'estomac (0 = vide, 3 = poids maximum) ;
          * niveau : le niveau principal du personnage (entre 1 et 100) ;
          * xp : l'XP principale du personnage ;
          * pk : le flag PK du personnage (0 = off, 1 = on).

        Cases propres aux joueurs :

          * nom : le nom du joueur (une chaîne) ;
          * creation : date de création du joueur (temps variable) ;
          * derniere_connexion : date de dernière connexion (temps variable).

        Exemples d'utilisation :

          joueur = joueur("Kredh")
          structure = structure(joueur)
          # Modifie le nom du joueur
          ecrire structure "nom" "Oscar"
          # Retire le flag PK du joueur
          ecrire structure "pk" 0
          # Enregistre les modifications
          appliquer joueur structure

        """
        return personnage.get_structure()

    @staticmethod
    def structure_objet(objet):
        """Retourne une structure simple représentant l'objet spécifié.

        Les structures sont extrêmement pratiques pour modifier
        certaines informations, quand les actions ou fonctions existantes
        ne suffisent pas. Ces modifications peuvent être parfois très
        spécifiques, comme par exemple, dans ce contexte, changer
        le flag d'un objet.

        Paramètres à entrer :

          * objet : l'objet dont on veut obtenir la structure.

        Cases de la structure :

            * visible : l'objet est-il visible (0 ou 1).

        Exemples d'utilisation :

          # Récupère la structure de l'objet dans la variable 'objet'
          structure = structure(objet)
          # Modifie la visibilité de l'objet
          ecrire structure "visible" 0
          # Enregistre les modifications
          appliquer objet structure

        """
        return objet.get_structure()
