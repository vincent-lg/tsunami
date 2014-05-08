modele = importeur.navigation.creer_modele("barque_peche")
centre = modele.ajouter_salle(0, 0, 0, "1")
centre.titre = "Le centre de la barque"
avant = modele.ajouter_salle(0, 1, 0, "2")
avant.titre = "L'avant de la barque"
