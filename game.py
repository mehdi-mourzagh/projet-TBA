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
        self.history = []

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
        
        history = Command("history", " : afficher l'historique des lieux visités", Actions.history, 0)
        self.commands["history"] = history

        back_cmd = Command("back", " : revenir au lieu précédent", Actions.back, 0)
        self.commands["back"] = back_cmd

        self.commands["retour"] = back_cmd



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


        hebra = Room("la Région d'Hébra", "Une région glaciale avec des montagnes gelées et des plateaux de toundra où souffle un vent mordant. On y trouve le village piaf.")
        korok = Room("la Forêt Korogu", "une forêt ancienne et mystérieuse, cœur du Grand Bois d'Hyrule, où de petites créatures mignonnes appelées Korogus veillent.")
        ordinn = Room("la Région d'Ordinn", "on y trouve la Montagne de la Mort, un puissant volcan explosif qui menace le village Goron. Les Gorons se nourissent de roches provenant du volcan")


        gerudo_high = Room("les Hauteurs Gerudo", "des falaises gelées surplombant le désert, offrant des vues spectaculaires.")
        centre_hyrule = Room("le Centre d'Hyrule", "de vastes plaines parsemé de ruines et sanctuaires, avec le château d'Hyrule au loin.")
        laneyru = Room("Région de Lanelle", "il ya le Domaine Zora et le village cocorico")

        gerudo_desert = Room("le Désert Gerudos", "vous voyez des dunes de sables à perte de vue, les oasis sont rares et les tempêtes de sable fréquente.")
        firone = Room("la Région de Firone", "composée de forêts humides et luxuriantes, le tonnerre frappe souvent et la végétation est très dense.")
        necluda = Room("la Région de Necluda", "on y trouve principalement le village d'Elimith, connu pour ses terres agricoles et sa gastronomie variées.")


        self.rooms.extend([
         hebra, korok, ordinn,
         gerudo_high, centre_hyrule, laneyru,
         gerudo_desert, firone, necluda
         ])


        hebra.exits = {"N": None, "E": korok, "S": gerudo_high, "O": None}
        korok.exits = {"N": None, "E": ordinn, "S": centre_hyrule, "O": hebra}
        ordinn.exits = {"N": None, "E": None, "S": laneyru, "O": korok}


        gerudo_high.exits = {"N": hebra, "E": centre_hyrule, "S": gerudo_desert, "O": None}
        centre_hyrule.exits = {"N": korok, "E": laneyru, "S": firone, "O": gerudo_high}
        laneyru.exits = {"N": ordinn, "E": None, "S": necluda, "O": centre_hyrule}


        gerudo_desert.exits = {"N": gerudo_high, "E": firone, "S": None, "O": None}
        firone.exits = {"N": centre_hyrule, "E": necluda, "S": None, "O": gerudo_desert}
        necluda.exits = {"N": laneyru, "E": None, "S": None, "O": firone}


        iles_ciel_a = Room("L'Île céleste du prélude", "une île flottante parsemée de ruines et enigmes à résoudre.")
        iles_ciel_b = Room("L'Île céleste de Lanelle", "archipel céléste de plateformes anciennes, dominé par des vents puissants.")

        self.rooms.extend([iles_ciel_a, iles_ciel_b])


        centre_hyrule.exits["U"] = iles_ciel_a
        korok.exits["U"] = iles_ciel_b


        iles_ciel_a.exits = {"D": centre_hyrule, "E": iles_ciel_b, "O": None, "N": None, "S": None}
        iles_ciel_b.exits = {"D": korok, "O": iles_ciel_a, "N": None, "E": None, "S": None}


        profondeurs_a = Room("Les profondeurs A", "dans le sous sol du chateau d'Hyrule, vous entendez des bruits étranges venant des ténèbres.")
        profondeurs_b = Room("Les profondeurs B", "dans la grande mine abandonée, il y a des golems antiques et fragements de sonium partout.")

        self.rooms.extend([profondeurs_a, profondeurs_b])

        
        centre_hyrule.exits["D"] = profondeurs_a
        korok.exits["D"] = profondeurs_b

   
        profondeurs_a.exits = {"U": centre_hyrule, "E": profondeurs_b, "O": None, "N": None, "S": None}
        profondeurs_b.exits = {"U": korok, "O": profondeurs_a, "N": None, "E": None, "S": None}

        # Setup player and starting room
        name = input("\nEntrez votre nom: ").strip()
        if not name:
            name = "Joueur"
        self.player = Player(name)
       
        self.player.current_room = iles_ciel_a
        
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
        print(f"\nBienvenue {self.player.name} dans le Royaume d'Hyrule !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        print(self.player.current_room.get_long_description())
    def get_history(self) -> str:
     if not hasattr(self, "history") or not self.history:
        return ""   # chaîne vide si rien

     lines = ["Vous avez déjà visité les pièces suivantes:"]
     for room in self.history:
        # j'affiche la description complète (ou room.name si tu préfères)
        # ici on garde la description stockée (sans "dans"), ce qui colle avec get_long_description
        lines.append(f"    - {room.name}")
     return "\n".join(lines)


def main():
    # Create a game object and play the game
    Game().play()


if __name__ == "__main__":
    main()
