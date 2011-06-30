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


"""Ce fichier contient le MOTD (Message Of The Day). C'est le message
que reçoit un client qui vient de se connecter.

En général, il s'agit d'un message de présentation, un dessin ASCII, un rappel
du nom du MUD, éventuellement de la version, des auteurs / contributeurs,
du code-base...

"""

MOTD = """
Bienvenue sur


 ,ggg,        gg                                                
dP""Y8b       dP                                                
Yb, `88      d8'                                                
 `"  88    ,dP'                                    gg           
     88aaad8"                                      ""           
     88''''Yb,      ,gggg,gg    ,g,       ,g,      gg    ,ggg,  
     88     "8b    dP"  "Y8I   ,8'8,     ,8'8,     88   i8" "8i 
     88      `8i  i8'    ,8I  ,8'  Yb   ,8'  Yb    88   I8, ,8I 
     88       Yb,,d8,   ,d8b,,8'_   8) ,8'_   8) _,88,_ `YbadP' 
     88        Y8P"Y8888P"`Y8P' "YY8P"PP' "YY8P"88P""Y8888P"Y888


                                        Version {Version}

"""
