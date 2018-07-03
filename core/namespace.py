'''
   Copyright (C) 1997-2017 JDERobot Developers Team

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Library General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, see <http://www.gnu.org/licenses/>.

   Authors : Pushkal Katara (katarapushkal@gmail.com)

  '''
class Namespace:
    def __init__(self):
        self.id = None
        self.name = None
        self.functions = None
        self.variables = None

    def createNode(self, doc):
        namespaceElement = doc.createElement('namespace')
        namespaceElement.setAttribute('id', str(self.id))
        nameElement = doc.createElement('name')
        nameElement.appendChild(doc.createTextNode(self.name))
        functionsElement = doc.createElement('functions')
        functionsElement.appendChild(doc.createTextNode(self.functions))
        namespaceElement.appendChild(functionsElement)
        variablesElement = doc.createElement('variables')
        variablesElement.appendChild(doc.createTextNode(self.variables))
        namespaceElement.appendChild(variablesElement)
        return namespaceElement

    def parse(self, element):
        self.id = element.getAttribute('id')
        self.name = element.getElementsByTagName('name')
        self.functions = element.getElementsByTagName('functions')
        self.variables = element.getElementsByTagName('variables')
        return self
