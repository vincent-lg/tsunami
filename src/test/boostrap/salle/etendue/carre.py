carre = importeur.salle.creer_etendue("carre")
obstacle = importeur.salle.obstacles["falaise"]
coords = [
        (10, 10),
        (11, 10),
        (12, 10),
        (13, 10),
        (14, 10),
        (14, 11),
        (14, 12),
        (14, 13),
        (14, 14),
        (13, 14),
        (12, 14),
        (11, 14),
        (10, 14),
        (10, 13),
        (10, 12),
        (10, 11),
        # Centre
        (12, 13),
]

for coord in coords:
    carre.ajouter_obstacle(coord, obstacle)
