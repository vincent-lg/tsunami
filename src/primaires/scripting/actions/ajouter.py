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


"""Fichier contenant l'action ajouter"""

from primaires.scripting.actions.ajouter_a_liste import ClasseAction as CA
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(CA):

    """Ajoute un élément."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.ajouter_a_liste, "object", "list")
        cls.ajouter_types(cls.ajouter_magasin, "Salle", "Fraction",
                "str", "str")
        cls.ajouter_types(cls.ajouter_magasin_unique, "Salle", "Objet")

    @staticmethod
    def ajouter_magasin(salle, quantite, service, cle):
        """Ajoute un service à l'inventaire du magasin.

        Paramètres à préciser :

          * salle : la salle contenant le magasin
          * quantite : la quantité de services à ajouter
          * service : le type de service (objet, potion, navire...)
          * cle : la clé du service (la clé de l'objet par exemple)

        Cette action s'utilise de façon très similaire à l'option
        /s dans l'éditeur de magasin d'une salle. Le service et
        la clé ont besoin d'être utilisés conjointement : le service
        le plus simple est 'objet' qui permet d'ajouter un ou plusieurs
        objets à la vente dans le magasin. Mais un magasin peut vendre
        d'autres services, comme des potions, de la nourriture, des
        navires, des familiers, des matelots, ainsi de suite. Pour
        chaque type de service, le nom à entrer est différent. Notez
        cependant qu'à la différence de l'option /s dans l'éditeur
        du magasin d'une salle, cette action ajoute le service directement
        dans l'inventaire du magasin, ce qui veut dire qu'il sera
        proposé en vente. En revanche, cela veut aussi dire qu'au
        renouvellement du magasin, qui arrive généralement au moins
        une fois par jour IG, le service ajouté disparaîtra.

        Exemples d'utilisation :

          salle = salle("zone:mnemo")
          # Ajoute 5 objets 'chausse_laine'
          ajouter salle 5 "objet" "chaussette_laine"
          # Ajoute 2 navires 'barque_peche'
          ajouter salle 2 "navire" "barque_peche"
          # Ajoute 4 familiers 'cheval_blanc'
          ajouter salle 4 "familier" "cheval_blanc"

        """
        quantite = int(quantite)
        if quantite < 1:
            raise ErreurExecution("Quantité {} négative ou nulle".format(
                    quantite))

        if service not in importeur.commerce.types_services:
            raise ErreurExecution("Type de service {} inconnu".format(
                    repr(service)))

        objets = importeur.commerce.types_services[service]
        if cle not in objets:
            raise ErreurExecution("le produit {} de service {} n'a " \
                    "pas pu être trouvé".format(repr(cle), repr(service)))

        service = objets[cle]
        salle.magasin.ajouter_inventaire(service, quantite)

    @staticmethod
    def ajouter_magasin_unique(salle, objet):
        """Ajoute un objet unique à l'inventaire du magasin.

        Cette action permet d'ajouter un objet unique dans
        l'inventaire du magasin. À la différence de la plupart
        des services, l'objet unique conserve l'objet dans le
        magasin, au lieu de son prototype. Ce peut donc être
        nécessaire si vous manipulez des objets modifiés (dont vous
        avez changé le nom, le poids, le prix et autre, probablement
        par scripting). L'objet peut-être soit dans un conteneur,
        posé au sol, ou bien sans aucun lien (nouvellement créé).
        Consultez les exemples ci-dessous pour des plus d'informations.

        Paramètres à préciser :

          * salle : la salle contenant le magasin
          * objet : l'objet à ajouter dans l'inventaire du magasin

        Exemples d'utilisation :

          salle = salle("zone:mnemo")
          # Ajoute un objet unique posé sur le sol
          # (contenu dans la variable 'objet')
          ajouter salle objet
          # Ou bien crée un objet unique
          objet = creer_objet("cle_du_prototype")
          # ... Modification de l'objet
          ajouter salle objet

        """
        if objet.contenu:
            try:
                objet.contenu.retirer(objet)
            except ValueError:
                pass

        salle.magasin.ajouter_inventaire(objet, 1, forcer_unique=True)
