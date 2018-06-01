'''
   Copyright (C) 1997-2018 JDERobot Developers Team

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

from PyQt5.QtWidgets import QFileDialog

class ImportManager():
    """
    Functionality:
    Import PreBuild State into Current State
    Verify Configurations
    Verify Libraries
    Verify Functions
    Verify Variables

    :param rootState: Root Imported State
    :param config: Configurations of Imported State
    :param libraries: Libraries of Imported State
    :param functions: Functions of Imported State
    :param variables: Variables of Imported State

    Returns list of States which needs to be Imported
    """
    def __init__(self):
        self.importState = None
        self.config = None
        self.libraries = None
        self.functions = None
        self.variables = None

    def updateIDs(self, importState, stateID):
        """ Wrapper upon UpdateState """
        self.updateStates(importState, stateID)
        return importState

    def updateStates(self, importState, stateID):
        """ Assign New IDs to Imported State Data Recursively """
        for child in importState.getChildren():
            child.setID(stateID)
            stateID += 1
            self.updateStates(child, stateID)
