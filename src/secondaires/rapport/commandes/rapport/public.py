from primaires.interpreteur.masque.parametre import Parametre
from primaires.interpreteur.editeur.presentation import Presentation
 
class PrmPublic(Parametre):
 
    def __init__(self):
        Parametre.__init__(self, "public", "public")
        self.schema = "<nombre>"
        self.aide_courte = "Modifie l'acces a un rapport"
        self.aide_longue = "Cette commande permet de modifier l'acces à un rapport en autorisant l'acces public"

    def interpreter(self, personnage, dic_masques):
        id = dic_masques["nombre"].nombre
        rapport = importeur.rapport.rapports[id]
        try:
	        if rapport.public == False:
	            if personnage.est_immortel() or personnage is rapport.createur:
	                rapport.public = True
	            personnage << "L'acces au rapport #{} a bien changé en acces public.|ff|".format(id)
	        else:
	            personnage << "|err|Vous ne pouvez pas modifier ce rapport|ff|"
	            return
        except KeyError:
            if personnage.est_immortel():
                personnage << "|err|Ce rapport n'existe pas.|ff|"
            else:
                personnage << "|err|Vous ne pouvez pas modifier ce rapport.|ff|"
                return