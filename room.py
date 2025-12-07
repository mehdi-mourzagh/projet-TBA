# Define the Room class.

# room.py
from __future__ import annotations
from typing import Dict, Optional


class Room:
    """
    Représente une salle / un lieu du jeu.

    Attributs
    ---------
    name : str
        Nom de la salle (ex. "Région d'Hébra").
    description : str
        Description du lieu (sans le mot "dans").
    exits : Dict[str, Optional[Room]]
        Dictionnaire des sorties par direction ('N','E','S','O','U','D').
    """

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
        self.exits: Dict[str, Optional["Room"]] = {}

    def get_exit(self, direction: str) -> Optional["Room"]:
        if not direction:
            return None
        return self.exits.get(direction.upper())

    def get_exit_string(self) -> str:
        """Retourne une ligne listant les sorties valides (ex : 'Sorties: N, E')."""
        valid_exits = [d for d, r in self.exits.items() if r is not None]
        if not valid_exits:
            return "Sorties : aucune"
        return "Sorties : " + ", ".join(valid_exits)

    def get_long_description(self) -> str:
        """
        Construit et retourne la description complète affichée au joueur.

        Exemple de sortie :
        "\nVous êtes dans la Région d'Hébra, des montagnes gelées...\n\nSorties : N, E\n"
        """
        desc = self.description.strip()
       
        header = f"\nVous êtes dans {self.name}, {desc}\n\n"
        return header + self.get_exit_string() + "\n"
