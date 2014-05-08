lagon = importeur.salle.creer_etendue("lagon")
obstacle = importeur.salle.obstacles["falaise"]
coords = [
        (2, 0),
        (2, 1),
        (2, 2),
        (2, 3),
        (2, 4),
        (2, 5),
]

for coord in coords:
    lagon.ajouter_obstacle(coord, obstacle)
