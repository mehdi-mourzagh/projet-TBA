# Description: Game class

# Import modules
# game.py
from room import Room
from player import Player
from command import Command
from actions import Actions


class Game:
    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.valid_directions = set()

    # Setup the game
    def setup(self):
        # Setup commands (les clés sont en minuscules)
        cmd_help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = cmd_help

        cmd_quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = cmd_quit

        cmd_go = Command(
            "go",
            " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U, D)",
            Actions.go,
            1,
        )
        self.commands["go"] = cmd_go

        # callbacks locaux pour up/down (appellent directement Player.move avec U/D)
        def cmd_up(game, list_of_words, number_of_parameters):
            # ne prend pas de paramètre supplémentaire
            return game.player.move("U")

        def cmd_down(game, list_of_words, number_of_parameters):
            return game.player.move("D")

        cmd_up_obj = Command("up", " : monter d'un niveau (équivalent go U)", cmd_up, 0)
        cmd_down_obj = Command("down", " : descendre d'un niveau (équivalent go D)", cmd_down, 0)
        self.commands["up"] = cmd_up_obj
        self.commands["down"] = cmd_down_obj

        # ---------- Création des lieux (thème : Temple de l'eau) ----------
        # Rez-de-chaussée : grille 3x3 (NW, N, NE, W, CENTRE, E, SW, S, SE)
        nw = Room("Aile nord-ouest", "un couloir envahi d'algues, les mosaïques sont effacées.")
        n = Room("Salle supérieure RC", "une chambre humide surplombant la cour.")
        ne = Room("Aile nord-est", "l'aile nord-ouest, vous voyez des mosaïques effacées et des statues à moitié submergées.")
        w = Room("Aile ouest", " un passage bordé de bassins verts et de vannes rouillées.")
        centre = Room("Salle centrale", "la chambre centrale du temple, il y a un grand pilier inondé.")
        e = Room("Aile est", "une galerie au carrelage glissant, l'eau coule en filet.")
        sw = Room("Aile sud-ouest", "l'aile sud-ouest, il y a des marches couvertes de mousse et de végétation.")
        s = Room("Salle sud", "une galerie où l'eau ruisselle doucement sur les pierres.")
        se = Room("Aile sud-est", "une salle où il y a des statues marines partiellement immergées.")

        # Ajouter au registre des rooms
        self.rooms.extend([nw, n, ne, w, centre, e, sw, s, se])

        # Connexions horizontales/verticales (N,E,S,O) - grille 3x3
        # Ligne nord
        nw.exits = {"N": None, "E": n, "S": w, "O": None}
        n.exits = {"N": None, "E": ne, "S": centre, "O": nw}
        ne.exits = {"N": None, "E": None, "S": e, "O": n}

        # Ligne milieu
        w.exits = {"N": nw, "E": centre, "S": sw, "O": None}
        centre.exits = {"N": n, "E": e, "S": s, "O": w}
        e.exits = {"N": ne, "E": None, "S": se, "O": centre}

        # Ligne sud
        sw.exits = {"N": w, "E": s, "S": None, "O": None}
        s.exits = {"N": centre, "E": se, "S": None, "O": sw}
        se.exits = {"N": e, "E": None, "S": None, "O": s}

        # ---------- 1er étage : 2 salles ----------
        first_a = Room("Galerie supérieure A", "une passerelle surplombant la chambre centrale.")
        first_b = Room("Galerie supérieure B", "une loge humide avec vue sur le pilier.")

        self.rooms.extend([first_a, first_b])

        # Accès vertical vers le 1er étage depuis la salle centrale et depuis la salle N (r0c1)
        centre.exits["U"] = first_a
        n.exits["U"] = first_b

        # Connecter les salles du 1er étage entre elles et redescente
        first_a.exits = {"D": centre, "E": first_b, "O": None, "N": None, "S": None}
        first_b.exits = {"D": n, "O": first_a, "N": None, "E": None, "S": None}

        # ---------- Sous-sol : 2 salles ----------
        basement_a = Room("Galerie inférieure A", "une alcôve immergée, l'air est plus frais.")
        basement_b = Room("Galerie inférieure B", "des canaux sombres où l'eau coule lentement.")

        self.rooms.extend([basement_a, basement_b])

        # Accès vertical vers le sous-sol depuis la salle centrale et depuis la salle N
        centre.exits["D"] = basement_a
        n.exits["D"] = basement_b

        # Connecter les salles du sous-sol entre elles et remontée
        basement_a.exits = {"U": centre, "E": basement_b, "O": None, "N": None, "S": None}
        basement_b.exits = {"U": n, "O": basement_a, "N": None, "E": None, "S": None}

        # Setup player and starting room
        name = input("\nEntrez votre nom: ").strip()
        if not name:
            name = "Joueur"
        self.player = Player(name)
        # Position de départ : Salle centrale
        self.player.current_room = centre
        
        self.valid_directions = set()
        for room in self.rooms:
         for d, target in room.exits.items():
           if target is not None:
             self.valid_directions.add(d.upper())
    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            try:
                raw = input("> ")
            except (KeyboardInterrupt, EOFError):
                print("\n\nInterruption détectée. Fin du jeu.\n")
                break
            self.process_command(raw)
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:
        # Ignore empty or whitespace-only input
        if command_string is None or command_string.strip() == "":
            return

        # Split the command string into a list of words (handles multiple spaces)
        list_of_words = command_string.split()
        # Normalize command word to lowercase
        command_word = list_of_words[0].lower()

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(
                f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n"
            )
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans le temple de l'eau !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        print(self.player.current_room.get_long_description())


def main():
    # Create a game object and play the game
    Game().play()


if __name__ == "__main__":
    main()
