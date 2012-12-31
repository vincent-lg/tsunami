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


"""Jeu de poquiir."""

from random import *

from primaires.commerce.transaction import *
from primaires.objet.conteneur import SurPoids
from .. import BaseJeu
from .combinaisons import combinaisons

class Jeu(BaseJeu):
    
    """Ce jeu définit le jeu de poquiir.
    
    Il est rattaché au plateau poquiir.
    
    """
    
    nom = "poquiir"
    def init(self):
        """Construction du jeu."""
        self.nb_joueurs_min = 2
        self.nb_joueurs_max = 6
        self.en_main = {}
        self.tableau = []
        self.tableau = []
        self.non_distribuees = list(self.plateau.pieces)
        self.abandons = []
        self.petite_blinde = 0
        self.pot = 0
        self.sommes_manche = {}
        self.tour = 1
    
    @property
    def grande_blinde(self):
        """Retourne le montant de la grande blinde."""
        return self.petite_blinde * 2
    
    def peut_commencer(self):
        """La partie peut-elle commencer ?"""
        if not self.partie.en_cours:
            self.partie.envoyer(
                    "|err|La partie n'a pas encore commencée.|ff|")
            return False
        
        if self.petite_blinde == 0:
            self.partie.envoyer("Le montant de la petite blinde n'a pas " \
                    "été fixé.")
            return False
        
        return True
    
    def peut_jouer(self, personnage):
        """Le personnage peut-il jouer ?"""
        if personnage in self.abandons:
            personnage << "Vous avez abandonné cette manche."
            return False
        
        return True
    
    def jouer(self, personnage, msg):
        """Joue au jeu.
        
        Les possibilités sont :
            m <montant> : pour miser (raise) davantage
            s : suivre (check) sans miser davantage
            ab : abandonner
        
        """
        possibilites = \
            "Les possibilités sont :\n\n" \
            " |cmd|m <montant>|ff| pour miser davantage (exemple " \
            "|cmd|m 200|ff|\n" \
            " |cmd|s|ff| pour suivre sans miser davantage\n" \
            " |cmd|ab|ff| pour abandonner la manche\n\n" \
            "|att|Les montants sont toujours donnés en pièces de bronze.|ff|"
        
        if msg:
            opt = msg.split(" ")[0].lower()
            reste = msg[len(opt):]
            if opt == "m":
                try:
                    montant = int(reste)
                except ValueError:
                    personnage << "|err|Montant {} invalide|ff|.".format(
                            reste)
                    return False
                else:
                    return self.monter(personnage, montant)
            elif opt == "s":
                return self.suivre(personnage)
            elif opt == "ab":
                self.abandonner(personnage)
                return True
            else:
                personnage << possibilites
                return False

        return False
    
    def monter(self, personnage, montant):
        """Le personnage mise davantage."""
        en_jeu = self.sommes_manche.get(personnage, 0)
        if montant <= 0 or montant % self.petite_blinde != 0:
            personnage << "|err|Vous devez miser un multiple de {}." \
                    "|ff|".format(self.petite_blinde)
            return False
        
        payer = self.payer(personnage, montant)
        if payer:
            personnage << "Vous misez {}.".format(montant)
            self.partie.envoyer("{{}} mise {}.".format(montant),
                    personnage)
            self.sommes_manche[personnage] = en_jeu + montant
            return True
        
        return False
    
    def suivre(self, personnage):
        """Suit la manche.
        
        Cela peut vouloir dire mettre la main au porte-feuille.
        
        """
        enjeu = self.sommes_manche.get(personnage, 0)
        max_enjeu = 0
        if self.sommes_manche:
            max_enjeu = max(self.sommes_manche.values())
        if self.tour == 1 and max_enjeu < self.grande_blinde:
            max_enjeu = self.grande_blinde
        
        if max_enjeu > enjeu:
            montant = max_enjeu - enjeu
            payer = self.payer(personnage, montant)
            if payer:
                personnage << "Vous suivez en misant {}.".format(montant)
                self.partie.envoyer("{{}} suit en misant {}.".format(
                        montant), personnage)
                self.sommes_manche[personnage] = max_enjeu
                self.verifier_tour()
                return True
            return False
        else:
            personnage << "Vous suivez."
            self.partie.envoyer("{} suit.", personnage)
            self.sommes_manche[personnage] = enjeu
            self.verifier_tour()
            return True
    
    def abandonner(self, personnage):
        """Abandonne la partie."""
        self.abandons.append(personnage)
        personnage << "Vous abandonnez cette manche."
        self.partie.envoyer("{} abandonne cette manche.", personnage)
        self.verifier_tour()
        return True
    
    def payer(self, personnage, montant):
        """Le personnage essaye de payer le montant demandé.
        
        Retourne True si il y réussi, False sinon.
        
        """
        # Constitution de la transaction
        try:
            transaction = Transaction.initier(personnage, None, montant)
        except FondsInsuffisants:
            personnage << "|err|Vous n'avez pas assez d'argent.|ff|"
            return False
        
        # On prélève l'argent
        transaction.payer()
        self.pot += montant
        return True
    
    def verifier_tour(self):
        """Vérifie si un tour (une main) se termine.
        
        La condition pour que cela arrive est que tous les joueurs
        toujours dans la manche ont misés autant.
        
        """
        enjeux = self.sommes_manche.copy()
        no = 0
        for abandon in self.abandons:
            no += 1
            if abandon in enjeux:
                del enjeux[abandon]
        
        min_enjeu = max_enjeu = 0
        joueurs = self.partie.joueurs
        if enjeux:
            min_enjeu = min(enjeux.values())
            max_enjeu = max(enjeux.values())
        
        fini = no + len(enjeux) == len(joueurs) and min_enjeu == max_enjeu
        if fini:
            self.sommes_manche = {}
            tour = self.tour + 1
            methode = "tour_" + str(tour)
            self.tour += 1
            getattr(self, methode)()
    
    def get_combinaison(self, personnage):
        """Retourne la combinaison ou None si aucune."""
        pieces = list(self.en_main.get(personnage))
        if pieces is None:
            return None
        
        pieces.extend(self.tableau)
        
        # On tri les pièces
        d_pieces = {}
        for piece in pieces:
            points = piece.points
            liste = d_pieces.get(points, [])
            liste.append(piece)
            d_pieces[points] = liste
        
        p_pieces = sorted([liste for liste in d_pieces.values()],
                key=lambda liste: liste[0].points, reverse=True)
        
        essai = None
        for combinaison in combinaisons:
            pieces = list(p_pieces)
            essai = combinaison.forme(pieces)
            if essai:
                break
        
        return essai
    
    def get_points_pieces(self, joueur):
        """Retourne les points des pièces du joueur."""
        pieces = list(self.en_main.get(joueur, []))
        pieces.extend(self.tableau)
        if pieces:
            return sum(p.points for p in pieces)
        
        return 0
        
    def choisir_piece(self):
        """Choisit et retourne une pièce parmi les non distribuées.
        
        La pièce retournée est considérée comme distribuée, on ne sait pas
        si c'est sur le tableau ou à un personnage, mais on la retire des
        pièces distribuées et on recalcul les combinaisons de chacun.
        
        """
        piece = choice(self.non_distribuees)
        self.non_distribuees.remove(piece)
        return piece
    
    def initier_tour(self):
        """Commence la manche."""
        self.tour_1()
        self.partie.en_cours = True
        
    def tour_1(self):
        """Commence une manche.
        
        On distribue les pièces des joueurs.
        
        """
        for joueur in self.partie.joueurs:
            piece_1 = self.choisir_piece()
            piece_2 = self.choisir_piece()
            self.en_main[joueur] = [piece_1, piece_2]
            joueur << "Vous recevez {} et {}.".format(
                    piece_1.nom_complet_indefini, piece_2.nom_complet_indefini)
    
    def tour_2(self):
        """On pose le flop (les trois premières cases sur le tableau)."""
        p1 = self.choisir_piece()
        p2 = self.choisir_piece()
        p3 = self.choisir_piece()
        self.tableau = [p1, p2, p3]
        noms = [p.nom_complet_indefini for p in (p1, p2, p3)]
        noms = noms[0] + ", " + noms[1] + " et " + noms[2]
        self.partie.envoyer("Trois pièces sont retournées face " \
                "visible sur le tableau :\n- {}".format(noms))
    
    def tour_3(self):
        """On ne retourne qu'une pièce."""
        piece = self.choisir_piece()
        self.tableau.append(piece)
        self.partie.envoyer("On retourne {} face visible sur le " \
                "tableau.".format(piece.nom_complet_indefini))
    
    def tour_4(self):
        """On ne retourne qu'une pièce."""
        piece = self.choisir_piece()
        self.tableau.append(piece)
        self.partie.envoyer("On retourne {} face visible sur le " \
                "tableau.".format(piece.nom_complet_indefini))
    
    def tour_5(self):
        """On détermine le ou les vainqueurs de la manche."""
        # On cherche toutes les combinaisons
        joueurs = []
        combinaisons = {}
        for joueur in self.partie.joueurs:
            if joueur not in self.abandons:
                joueurs.append(joueur)
                combinaisons[joueur] = self.get_combinaison(joueur)
        
        if len(joueurs) == 1:
            joueur = joueurs[0]
            return self.gagner(joueur, masque=True,
                    combinaisons=combinaisons)
        
        if len(combinaisons) == 1:
            return self.gagner(joueur, combinaisons=combinaisons)
        
        # On cherche la combinaison la plus élevée
        if any(combinaisons.values()):
            lst_combinaisons = sorted([(j, cbn) for j, cbn in \
                    combinaisons.items() if cbn], key=lambda couple: \
                    couple[1].points_complet, reverse=True)
            
            t_combinaisons = list(lst_combinaisons)
            lst_combinaisons = []
            points = None
            for joueur, combinaison in t_combinaisons:
                if points is None:
                    points = combinaison.points_complet
                    lst_combinaisons.append((joueur, combinaison))
                    continue
                
                if points == combinaison.points_complet:
                    lst_combinaisons.append((joueur, combinaison))
                else:
                    break
            
            if len(lst_combinaisons) == 1:
                self.gagner(lst_combinaisons[0][0], combinaisons=combinaisons)
            else:
                # On cherche les gagnants
                t_combinaisons = sorted([(j, cbn) for j, cbn in \
                        lst_combinaisons], key=lambda couple: \
                        couple[1].points_exterieurs, reverse=True)
                
                joueurs = [j for j, cbn in t_combinaisons]
                self.gagner(*joueurs, combinaisons=combinaisons)
        else:
            t_joueurs = []
            for joueur in joueurs:
                points = self.get_points_pieces(joueur)
                t_joueurs.append((joueur, points))
            
            t_joueurs = sorted(t_joueurs, lambda couple: couple[1],
                    reverse=True)
            for joueur, points in list(t_joueurs):
                if points != t_joueurs[0][1]:
                    t_joueurs.remove((joueur, points))
            joueurs = [j for j, p in t_joueurs]
            self.gagner(*joueurs)
    
    def gagner(self, *joueurs, masque=False, combinaisons=None):
        """Les joueurs indiqués ont gagnés la partie."""
        if not masque:
            combinaisons = combinaisons if combinaisons else {}
            for joueur, combinaison in combinaisons.items():
                piece1, piece2 = self.en_main.get(joueur, (None, None))
                nom = "rien"
                if combinaison:
                    nom = combinaison.nom
                
                if piece1 and piece2:
                    msg = "{{}} avait {} et {}, ce qui lui donne {}.".format(
                            piece1.nom_complet_indefini,
                            piece2.nom_complet_indefini, nom)
                    self.partie.envoyer(msg, joueur)
        
        if len(joueurs) == 1:
            joueur = joueurs[0]
            pot = self.pot
            joueur.envoyer("Vous remportez le pot total de {} pièces de " \
                    "bronze !".format(pot))
            self.partie.envoyer("{{}} remporte le pot total de {} pièces de " \
                    "bronze !".format(pot), joueur)
            self.donner_argent(joueur, pot)
        else:
            partage = self.pot // len(joueurs)
            for joueur in joueurs:
                joueur.envoyer("Vous remportez le pot partagé de {} pièces " \
                        "de bronze !".format(partage))
                self.partie.envoyer("{{}} remporte le pot partagé de {} " \
                        "pièces de bronze !".format(partage), joueur)
                self.donner_argent(joueur, partage)
        
        blinde = self.petite_blinde
        self.init()
        self.petite_blinde = blinde
        self.partie.en_cours = False
    
    def donner_argent(self, joueur, montant):
        """Donne l'argent au joueur.
        
        Si le joueur ne peut pas prendre l'argent, le pose.
        
        """
        # D'abord on cherche l'argent le plus faible
        prototypes = [p for p in importeur.objet.prototypes.values() if \
                p.est_de_type("argent") and p.m_valeur == 1]
        prototype = prototypes[0]
        try:
            joueur.ramasser(prototype, qtt=montant)
        except SurPoids:
            joueur << "|att|C'est trop lourd pour vous, l'argent se " \
                    "retrouve par terre.|ff|"
            joueur.salle.objets_sol.ajouter(prototype, montant)
    
    def opt_b(self, personnage, montant):
        """Change la petite blinde."""
        if self.partie.en_cours:
            personnage << "|err|La partie a déjà commencée.|ff|"
            return
        
        if not montant:
            personnage << "|err|Précisez un montant pour la petite " \
                    "blinde.|ff|"
            return
        
        try:
            montant = int(montant)
            assert montant > 1
        except (ValueError, AssertionError):
            personnage << "|err|Montant invalide.|ff|"
        else:
            self.petite_blinde = montant
            self.partie.envoyer("La petite blinde est à présent à " \
                    "{} pièces de bronze.".format(montant))
    
    def opt_c(self, personnage, reste):
        """Affiche la combinaison."""
        combinaison = self.get_combinaison(personnage)
        if combinaison:
            personnage << "Votre plus forte combinaison : {}.".format(
                    combinaison.nom)
        else:
            personnage << "Vous ne possédez aucune combinaison."
    
    def opt_p(self, personnage, reste):
        """Renvoie le pot total."""
        personnage << "Le pot total contient {} pièces de bronze.".format(
                self.pot)
    
    def opt_s(self, personnage, reste):
        """Retourne le montant que doit payer le personnage pour pouvoir suivre."""
        montant = 0
        enjeu = self.sommes_manche.get(personnage, 0)
        max_enjeu = 0
        if self.sommes_manche:
            max_enjeu = max(self.sommes_manche.values())
        if self.tour == 1 and max_enjeu < self.grande_blinde:
            max_enjeu = self.grande_blinde
        
        if max_enjeu > enjeu:
            montant = max_enjeu - enjeu
        
        personnage << "Pour suivre, vous devez payer {} pièces de " \
                "bronze.".format(montant)
    
    def opt_j(self, personnage, reste):
        """Lance la partie."""
        if self.partie.en_cours:
            personnage << "|err|La partie a déjà commencée.|ff|"
            return
        
        if self.petite_blinde == 0:
            personnage << "|err|La petite blinde n'a pas encore été fixée.|ff|"
            return
        
        self.initier_tour()
