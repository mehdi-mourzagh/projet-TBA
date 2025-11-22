# Define the Player class.
class Player:
    """
    Représente le joueur et gère sa position dans le jeu.

    L'objet Player contient le nom du joueur et la salle courante dans laquelle
    il se trouve. La méthode move permet de se déplacer vers une direction
    cardinale si une sortie est présente.

    Attributs:

    name : str
        Nom du joueur.
    current_room : Optional[Room]
        Salle actuelle du joueur (None si non initialisée).

    Méthodes:

    move(direction: str) -> bool
        Tente de déplacer le joueur dans la direction donnée ('N','E','S','O').
        Retourne True si le déplacement réussi (nouvelle salle), False sinon.

    Exemples:

    >>> r1 = Room("Start", "une aire de départ.")
    >>> r2 = Room("North", "une clairière au nord.")
    >>> r1.exits['N'] = r2
    >>> p = Player("Test")
    >>> p.current_room = r1
    >>> p.move('N')
    True
    >>> p.current_room is r2
    True
    >>> # tenter d'aller à l'ouest là où il n'y a pas de sortie
    >>> p.move('O')
    False
    """

    def __init__(self, name):
        self.name = name
        self.current_room = None

    # Define the move method.
    def move(self, direction):
        # Vérifier que le joueur est dans une salle.
        if self.current_room is None:
            print("\nLe joueur n'est dans aucune salle.\n")
            return False

        # Utiliser l'API de Room pour récupérer la sortie en sécurité.
        next_room = None
        try:
            next_room = self.current_room.get_exit(direction)
        except Exception:
            next_room = None

        # Si la sortie est absente ou None, afficher un message et retourner False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False

        # Déplacer le joueur vers la salle suivante.
        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True

    