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


"""Ce fichier contient l'exception DepassementStat, détaillée plus bas.

Les exceptions levées lors d'un dépassement de stat se trouvent également ici.

"""

from bases.exceptions.base import ExceptionMUD

class DepassementStat(ExceptionMUD):
    
    """Exception DepassementStat.
    
    Cette exception est une classe-mère appelée quand une stat prend une
    valeur qu'elle n'est pas supposée prendre.
    Ces valeurs se retrouvent dans les flags d'exception.
    
    """
    pass

class StatI0(DepassementStat):
    
    """Cette exception est appelée si la stat est inférieure à 0."""
    pass

class StatIE0(DepassementStat):
    
    """Cette exception est appelée si la stat est inférieure ou égale à 0."""
    pass

class StatSM(DepassementStat):
    
    """Cette exception est appelée si la stat est supérieure au max."""
    pass

class StatSEM(DepassementStat):
    
    """Cette exception est appelée si la stat est supérieure ou égale au max.
    
    """
    pass
