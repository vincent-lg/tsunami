# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Ce fichier définit plusieurs fonctions propres au formatage de messages
à envoyer.

Fonctions à appliquer à la réception de message :
-   echapper_sp_cars : échapper les caractères spéciaux utilisés pour les codes
    couleurs ou les codes de formatage

Fonctions à appliquer à l'émission de message :
-   convertir_nl : convertir les sauts de ligne '\n' dans un format
    universellement interprété
-   ajouter_couleurs : ajouter les couleurs en fonction des codes de
    formattage
-   replacer_sp_cars : reconvertir les caractères d'échappement

"""

# Constantes de formatage
sp_cars_a_echapper = { # caractères à échapper
    "|":"|bar|",
}

sp_cars_a_remplacer = {} # dictionnaire miroir de sp_cars_a_echapper
for cle, val in sp_cars_a_echapper.items():
    sp_cars_a_remplacer[val] = cle

NL = "\r\n"

ACCENTS = {
    # Accent:lettre non accentuée
    # Lettres majuscules
    "É":"E",
    "À":"A",
    "È":"E",
    "Ù":"U",
    "Â":"A",
    "Ê":"E",
    "Î":"I",
    "Ô":"O",
    "Û":"U",
    "Ä":"A",
    "Ë":"E",
    "Ï":"I",
    "Ç":"C",
    
    # Lettres minuscules
    "é":"e",
    "à":"a",
    "è":"e",
    "ù":"u",
    "â":"a",
    "ê":"e",
    "î":"i",
    "ô":"o",
    "û":"u",
    "ä":"a",
    "ë":"e",
    "ï":"i",
    "ç":"c",
}

# Couleurs
COULEURS = {
    # Balise: code ANSI
    "|nr|": "\x1b[1m\x1b[30m", # noir
    "|rg|": "\x1b[1m\x1b[31m", # rouge
    "|vr|": "\x1b[1m\x1b[32m", # vert
    "|jn|": "\x1b[1m\x1b[33m", # jaune
    "|bl|": "\x1b[1m\x1b[34m", # bleu
    "|mg|": "\x1b[1m\x1b[35m", # magenta
    "|cy|": "\x1b[1m\x1b[36m", # cyan
    "|bc|": "\x1b[1m\x1b[37m", # blanc
    "|ff|": "\x1b[0m",  # fin de formattage
}

# Fonctions à appliquer à la réception de messages

def echapper_sp_cars(msg):
    """Fonction appelée pour échapper les caractères spéciaux d'une
    chaîne.
    
    Elle doit être appliquée sur les messages réceptionnés, mais pas sur tous.
    Certains messages réceptionnés depuis des personnages immortels doivent
    avoir la possibilité d'ajouter ces codes de formattage.
    
    Pour connaître les caractères à échapper, on se base sur le dictionnaire
    sp_cars_a_echapper.
    
    """
    for car, a_repl in sp_cars_a_echapper.items():
        msg = msg.replace(car, a_repl)
    return msg

def convertir_nl(msg):
    """Cette fonction est appelée pour convertir les sauts de ligne '\n'
    en sauts de ligne compris par tous les clients (y compris telnet).
    
    """
    msg = msg.replace("\n", NL)
    print("c", repr(msg))
    return msg

def ajouter_couleurs(msg):
    """Cette fonction est appelée pour convertir les codes de formatage
    couleur en leur équivalent ANSI.
    On se base sur la constante dictionnaire 'COULEURS'.
    
    """
    for balise, code_ansi in COULEURS.items():
        msg = msg.replace(balise, code_ansi)
    
    return msg

def remplacer_sp_cars(msg):
    """On remplace les caractères d'échappement d'un message, ceux échappés
    par la méthode 'echapper_sp_cars' à la réception du message.
    
    On se base sur le dictionnaire miroir 'sp_cars_a_remplacer'.
    
    """
    for code_car, a_repl in sp_cars_a_remplacer.items():
        msg = msg.replace(code_car, a_repl)
    return msg

def supprimer_accents(msg):
    """Cette fonction permet, avant émission du message, de retirer
    les accents. On se base sur ACCENTS pour ce faire.
    
    """
    for acc, non_acc in ACCENTS.items():
        msg = msg.replace(acc, non_acc)
    
    return msg
