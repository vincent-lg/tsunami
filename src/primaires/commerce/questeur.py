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


"""Fichier contenant la classe Questeur, détaillée plus bas."""

from abstraits.obase import BaseObj

class Questeur(BaseObj):

    """Classe définissant un questeur monétaire.

    Un questeur est une sorte de banque, permettant de :
    * Conserver de la monnaie déposée
    * Retirer la monnaie dans la quantité et la valeur souhaitée
    * Récupérer des lettres de crédits pour les grosses sommes.

    À la différence de la plupart des banques sur les MUD, les questeurs
    ne partagent pas les informations. Si un joueur dépose de l'argent
    dans un questeur à un endroit il ne pourra pas le récupérer dans
    un autre questeur.

    """

    enregistrer = True
    def __init__(self, salle):
        """Constructeur du questeur."""
        BaseObj.__init__(self)
        self.salle = salle
        self.comptes = {}
        self.monnaies = []
        self.prototype_servant = None
        self.taux_deposer = 95
        self.montant_min = 5
        self._construire()

    def __getnewargs__(self):
        return (None, )

    @property
    def servant(self):
        """Retourne, si présent, le PNJ servant dans la salle.

        On parcourt pour ce faire les personnages de la salle. Si un
        PNJ est trouvé avec le prototype indiqué dans l'attribut
        prototype_servant, le PNJ est retourné. Sinon, on retourne None
        ce qui veut dire qu'aucun servant n'est disponible (le questeur
        est inutilisable par les joueurs).

        """
        if self.prototype_servant is None or self.salle is None:
            return None

        for personnage in self.salle.personnages:
            if hasattr(personnage, "prototype") and \
                    personnage.prototype is self.prototype_servant:
                return personnage

        return None

    def deposer(self, joueur, argent, nombre):
        """Dépose de l'argent sur le compte du joueur.

        Les paramètres à entrer sont :
            Le joueur sur le compte duquel on dépose de l'argent
            L'objet de type argent
            Le nombre d'objets déposés.

        """
        montant = o_montant = nombre * argent.m_valeur
        if montant < self.montant_min:
            return 0

        # Le montant est estimé en fonction du taux_deposer
        if 1 <= self.taux_deposer <= 100:
            montant = int(self.taux_deposer / 100 * montant)

        if montant == 0:
            return 0

        s_montant = o_montant - montant # Montant superflu
        self.salle.zone.argent_total += montant

        # On prélève l'argent du joueur
        preleve = False
        t_conteneurs = [o for o in \
                joueur.equipement.inventaire if o.est_de_type("conteneur")]
        for t_conteneur in t_conteneurs:
            if t_conteneur.contient(argent, nombre):
                t_conteneur.conteneur.retirer(argent, nombre)
                preleve = True
                break

        if not preleve:
            return 0

        t_montant = self.comptes.get(joueur, 0)
        t_montant += montant
        self.comptes[joueur] = t_montant
        self._enregistrer()
        return montant

    def get_valeur_compte(self, joueur):
        """Retourne le montant retenu pour le joueur."""
        return self.comptes.get(joueur, 0)

    def prelever(self, joueur, argent, nombre):
        """Prélève l'argent désiré.

        Les paramètres à entrer sont :
            Le joueur qui doit recevoir la somme
            Le prototype d'objet décrivant la monnaie
            Le nombre de pièces à retirer.

        """
        montant = argent.m_valeur * nombre
        detenu = self.get_valeur_compte(joueur)
        if detenu < montant:
            return

        t_montant = detenu - montant
        self.comptes[joueur] = t_montant
        joueur.ramasser_ou_poser(argent, qtt=nombre)
        self._enregistrer()
