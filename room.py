# Define the Room class.

class Room:
    """
    Représente une salle du jeu.

    Une instance de Room contient un nom, une description
    et un dictionnaire d'exits mappant des directions ('N', 'E', 'S', 'O')
    vers d'autres Room ou None.

    Attributs:

    name : str
        Nom de la salle
    description : str
        Description textuelle du lieu
        Exemple : "une forêt enchantée. Vous entendez une brise légère..."
    exits : Dict[str, Optional[Room]]
        Dictionnaire des sorties par direction ('N','E','S','O').
        La valeur est soit une instance de Room soit None si aucune sortie.

    Méthodes:

    get_exit(direction: str) -> Optional[Room]
        Retourne la Room située dans la direction demandée (ou None).
    get_exit_string() -> str
        Retourne une chaîne listant les directions de sortie valides.
    get_long_description() -> str
        Construit et retourne la description complète affichée au joueur,
        en insérant le préfixe "Vous êtes dans " devant la description.

    Exemples :

    >>> r1 = Room("A", "une petite pièce lumineuse.")
    >>> r2 = Room("B", "une cave sombre.")
    >>> r1.exits['N'] = r2
    >>> r1.get_exit('N') is r2
    True
    >>> 'N' in r1.exits and r1.exits['N'] is not None
    True
    >>> print(r1.get_long_description())  # doctest: +ELLIPSIS
    Vous êtes dans une petite pièce lumineuse.
    ...
    """
    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
    
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nVous êtes dans {self.description}\n\n{self.get_exit_string()}\n"