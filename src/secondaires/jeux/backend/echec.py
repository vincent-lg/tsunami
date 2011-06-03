from bases.collections.liste_id import ListeID

from .chesswm import *

STR_COULEURS = ["blanc","noir"]
COULEURS = [WHITE, BLACK]

AVANT, ENCOURS, PAUSE, FINIE = (0, 1, 2, 3)

class echec(Game):

    nom = "echec"
    max_joueur = 2
    
    def __init__(self):
        Game.__init__(self)
        self.setup()
        self.joueurs = [None, None]
        self.etat = AVANT
    
    def arriverPif(self, joueur):
        if not self.arriver(0, joueur):
            if not self.arriver(1, joueur):
                return False
        return True
    
    def arriver(self, numero, joueur):
        if self.joueurs[numero] == None:
            self.joueurs[numero] = joueur
            joueur << "Vous êtes les {}s\n".format(STR_COULEURS[numero])
            if self.joueurs[not numero]:
                self.joueurs[not numero] << "Un adversaire se place en " \
                "face de vous"
        else:
            return False
        return True
    
    def dire(self, joueur, message):
        n = not self.numero(joueur)
        if self.joueurs[n]:
            joueur << "Vous dites : " + message
            self.joueurs[n] << "Votre adversaire dit : " + message
        else:
            joueur << "Vous n'avez personne à qui parler"
    
    def quitter(self, joueur):
        n = self.numero(joueur)
        self.joueurs[n] = None
        if self.joueurs[not n]:
            self.joueurs[not n] << "Votre adversaire est parti"
        self.pause()
    
    def demarrer(self):
        if None in self.joueurs:
            return False
        if not self.etat in [AVANT, FINIE]:
            return False
        if self.etat == FINIE:
            self.setup()
        self.etat = ENCOURS
        self.envoyer(self.plateau())
        self.envoyer("\nLa partie commence\n")
        self.joueurs[0] << "C'est à vous de jouer"
        return True
    
    def pause(self):
        if self.etat == PAUSE:
            self.etat = ENCOURS
            self.envoyer("La partie reprend")
        elif self.etat == ENCOURS:
            self.etat = PAUSE
            self.envoyer("La partie est en pause")
        else:
            return False
        return True
    
    def envoyer(self, msg):
        if self.joueurs[0]:
            self.joueurs[0] << msg
        if self.joueurs[1]:
            self.joueurs[1] << msg
    
    def numero(self, joueur):
        if self.joueurs[0] == joueur:
            return 0
        elif self.joueurs[1] == joueur:
            return 1
        else:
            raise(ValueError("Le joueur n'est pas dans la partie"))
    
    def plateau(self):
        return str(self.board)
    
    def jouer(self, joueur, cmd):
        
        if self.etat == AVANT:
            joueur << "La partie n'a pas encore commencé"
            return
        elif self.etat == PAUSE:
            joueur << "La partie est en pause"
            return
        elif self.etat == FINIE:
            joueur << "La partie est finie"
            return
        
        n = self.numero(joueur)
        
        if self.board.get_turn() != COULEURS[n]:
            joueur << "Ce n'est pas à vous de jouer"
            return
        
        move = None
        
        try:
            move = self.board.parse(cmd)
        except ParseError as error:
            joueur << str(error)
            return
        
        self.move(move)
        
        self.envoyer(str(self.board))
        
        result = self.board.check_result()
        
        self.envoyer("\nLes {couleur}s ont joué {coup}" \
            .format(couleur=STR_COULEURS[n] , coup=cmd))
        
        if result == MATE:
            joueur << "\nEchec et mat !\nVous avez gagné"
            self.joueurs[not n] << "\nEchec et mat !\nVous avez perdu"
            self.etat = FINIE
        elif result == STALEMATE:
            self.envoyer("\nLa partie est nulle")
            self.etat = FINIE
        else:
            if self.board.is_check(COULEURS[not n]):
                self.joueurs[not n] << "\nVous êtes en échec !"
            self.joueurs[not n] << "\nC'est à vous de jouer"

