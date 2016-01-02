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


"""Ce fichier contient la classe NavireVente, détaillée plus bas."""

from abstraits.obase import BaseObj

class NavireVente(BaseObj):

    """Cette classe enveloppe un navire mis en vente.

    Elle simule certains comportements d'un objet standard afin de permettre
    la vente d'un navire en magasin. C'est, en somme, un nouveau type
    de service.

    L'achat de ce service passe par la création d'une commande en
    chantier naval.

    """

    type_achat = "navire"
    def __init__(self, modele):
        """Constructeur de la classe"""
        BaseObj.__init__(self)
        self.modele = modele

    def __getnewargs__(self):
        return (None, )

    def __repr__(self):
        return "<NavireVente {}>".format(self.modele.cle)

    def __str__(self):
        return self.modele.cle

    @property
    def cle(self):
        return self.modele.cle

    @property
    def m_valeur(self):
        return self.modele.m_valeur

    @property
    def nom_achat(self):
        return self.modele.nom

    def get_nom(self, nombre=1):
        """Retourne le nom complet en fonction du nombre.

        Par exemple :
        Si nombre == 1 : retourne le nom singulier
        Sinon : retourne le nombre et le nom pluriel

        """
        return self.modele.nom

    def acheter(self, quantite, magasin, transaction):
        """Achète les objets dans la quantité spécifiée."""
        salle = magasin.parent
        acheteur = transaction.initiateur
        modele = self.modele

        # On essaye de trouver le chantier naval
        chantier_naval = None
        for chantier in importeur.navigation.chantiers.values():
            if chantier.salle_magasin is salle:
                chantier_naval = chantier
                break

        if chantier_naval is None:
            raise ValueError("Impossible de trouver le chantier naval " \
                    "pour {}".format(salle.ident))

        chantier.ajouter_commande(acheteur, None, "acheter",
                modele.duree_construction, modele.cle)
        acheteur << "Votre commande est envoyée au chantier naval."
        acheteur.envoyer_tip("Pour voir la liste de vos commandes en cours, " \
                "entrez %chantier% %chantier:commandes%.")

    def regarder(self, personnage):
        """Le personnage regarde le service (avant achat)."""
        return self.modele.description_vente.regarder(personnage, self.modele)
