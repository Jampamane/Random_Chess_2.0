from bs4 import BeautifulSoup
from pieces import Pawn
from pieces import Knight
from pieces import Rook
from pieces import Bishop
from pieces import King
from pieces import Queen
from bcolors import ByteColors

class Player():
    def __init__(self, color, page_source):
        self.color = color
        if self.color == "white":
            self.text_color = ByteColors.OKCYAN
        elif self.color == "black":
            self.text_color = ByteColors.OKBLUE
        self.username = (f"{self.text_color}"
                         f"{self.set_username(page_source).upper()}{ByteColors.ENDC}")
        self.time_left = self.set_time(page_source)
        self.pawn1 = Pawn(color)
        self.pawn2 = Pawn(color)
        self.pawn3 = Pawn(color)
        self.pawn4 = Pawn(color)
        self.pawn5 = Pawn(color)
        self.pawn6 = Pawn(color)
        self.pawn7 = Pawn(color)
        self.pawn8 = Pawn(color)
        self.rook1 = Rook(color)
        self.rook2 = Rook(color)
        self.kight1 = Knight(color)
        self.kight2 = Knight(color)
        self.bishop1 = Bishop(color)
        self.bishop2 = Bishop(color)
        self.king = King(color)
        self.queen = Queen(color)
        self.pieces = [self.pawn1, self.pawn2, self.pawn3, self.pawn4,
                       self.pawn5, self.pawn6, self.pawn7, self.pawn8,
                       self.rook1, self.rook2, self.kight1, self.kight2,
                       self.bishop1, self.bishop2, self.king, self.queen]
        self.set_positions(page_source, self.pieces)

    def __call__(self) -> None:
        print(f"{self.username} is "
              f"{self.text_color}{self.color.upper()}{ByteColors.ENDC}"
              f" and they have {ByteColors.FAIL}{self.time_left}{ByteColors.ENDC}"
              f" left on the clock")
        print(f"{self.username} has {ByteColors.WARNING}{len(self.alive_pieces())}{ByteColors.ENDC}"
              f" pieces left on the board \n")

    def has_moved(self, page_source):
        page = BeautifulSoup(page_source, "html.parser")
        moves = page.find_all(class_ = f"{self.color} node")
        selected_move = page.find(class_ = f"{self.color} node selected")
        if selected_move:
            moves.append(selected_move)
        if len(moves) == 0:
            return False
        return True

    def print_last_move(self, page_source, piece):
        page = BeautifulSoup(page_source, "html.parser")
        moves = page.find_all(class_ = f"{self.color} node")
        selected_move = page.find(class_ = f"{self.color} node selected")
        if selected_move:
            moves.append(selected_move)
        if len(moves) == 0:
            print(f"{self.username.center(25, '-')} hasn't moved yet\n")
            return False
        move = moves[-1]
        self.set_time(page_source)
        print(f"{self.username.center(25, '-')} moved their "
              f"{self.text_color}{str(piece).upper()}{ByteColors.ENDC} to "
              f"{self.text_color}{str(move.text).upper()}{ByteColors.ENDC}\n")
        return move

    def create_dict(self, page_source, sort_color = True) -> dict:
        '''
        Reads the browser's HTML and creates a dictionary with piece and location information.
        '''
        piece_dict = {}
        page = BeautifulSoup(page_source, "html.parser")
        board = page.find("wc-chess-board")
        positions = board.find_all("div", lambda text: "piece" in text.lower())
        pieces = [str(piece) for piece in positions]
        #Selects each div compenent that was turned into text
        for piece in pieces: 
            #Deletes the quotation marks and
            #splits the div text component into individual values
            piece_text = piece.replace("\"", "").split()
            #Iterates over each individual value
            for text in piece_text: #div br piece-88
                #Test to see if the value is a 2 character piece identifier
                if len(text) == 2: 
                    if sort_color is True:
                        if self.color[0] == text[0]: #Test for correct color
                            #If not correct color set both to None and break
                            current_piece = None
                            current_position = None
                            break
                    elif sort_color is False:
                        current_piece = text
                try:
                    int(text[-2:]) #Test for 2 chars cast to int
                except ValueError:
                    pass
                else:
                    current_position = text[-2:]
            #Update dictionary if values aren't None
            if current_position is not None and current_piece is not None: 
                piece_dict[current_position] = current_piece
        return piece_dict

    def set_positions(self, page_source, piece_list) -> None:
        '''
        Calls the create_dict function to create a dictionary with piece and location information.
        Uses that information to set the initial position of each piece.
        '''
        dict_ = self.create_dict(page_source).items()
        piece_list_copy = list(piece_list)
        for position, piece in dict_:
            for player_piece in piece_list_copy:
                if piece[-1] == player_piece.char_identifier:
                    player_piece.set_position(position)
                    piece_list_copy.remove(player_piece)
                    break
        if len(piece_list_copy) != 0: #If there is still a piece left in piece_list, 
            for piece in piece_list_copy: #it wasn't found in the HTML and it must be dead
                piece.board_position = "00"

    def set_attribute(self, page_source, class_name) -> str:
        '''
        A bit of repeat logic in figuring out which attribute to set when there are exactly 2 attributes.
        For example, 2 usernames, 2 clocks.
        '''
        page = BeautifulSoup(page_source, "html.parser")
        attributes = page.find_all(class_=class_name)
        flipped = page.find(class_="flipped")
        attribute = ""
        if flipped is not None:
            if self.color == "black":
                attribute = attributes[1].get_text()
            elif self.color == "white":
                attribute = attributes[0].get_text()
        elif flipped is None:
            if self.color == "black":
                attribute = attributes[0].get_text()
            elif self.color == "white":
                attribute = attributes[1].get_text()
        return attribute

    def set_username(self, page_source) -> str:
        username = self.set_attribute(page_source, "user-username-white")
        return username

    def set_time(self, page_source) -> str:
        clock_time = self.set_attribute(page_source, "clock-time-monospace")
        return clock_time

    def alive_pieces(self) -> list:
        pieces = [piece for piece in self.pieces if piece.board_position != "00"]
        return pieces

    def is_turn(self, page_source) -> bool:
        page = BeautifulSoup(page_source, "html.parser")
        if page.find(class_=f"{self.color} node selected") is None:
            return True
        return False

    def check_for_move(self, page_source) -> bool:
        '''
        Function that is used exclusively to figure out where the opponent has moved
        '''
        piece_dict = self.create_dict(page_source)
        piece_list = self.alive_pieces()
        for piece in piece_list:
            try:
                piece_dict[piece.board_position]
            except KeyError:
                if str(piece) == "Pawn":
                    if (self.color == "white" and
                        int(piece.board_position[1]) == 7) or (
                            self.color == "black" and
                            int(piece.board_position[1]) == 2):
                        self.pieces.remove(piece)
                        piece = Queen(self.color)
                        self.pieces.append(piece)
                        self.set_positions(page_source, self.pieces)
                return str(piece)
        return False

    def retrieve_final_moves(self, page_source, all_pieces = None, piece_list = None):
        final_moves = []
        if piece_list is None:
            piece_list = self.alive_pieces()
        if all_pieces is None:
            all_pieces = self.create_dict(page_source, sort_color=False)
        for piece in piece_list:
            moves = piece.return_final_moves(all_pieces)
            if moves is not None:
                for piece, move in moves:
                    final_moves.append((piece, move))
        if len(final_moves == 0):
            return None
        return final_moves

    def retrieve_non_check_moves(self, page_source, opponent):
        player_potential_moves = self.retrieve_final_moves(page_source)
        all_the_pieces = self.create_dict(page_source, sort_color=False)
        opponent_alive_pieces_copy = opponent.alive_pieces()
        opponent_current_positions = {
            piece.board_position: piece for piece in opponent.alive_pieces()}
        non_check_moves = []
        for piece, move in player_potential_moves:
            capture_piece = None
            try:
                capture_piece = opponent_current_positions[move]
            except KeyError:
                pass
            else:
                opponent_alive_pieces_copy.remove(capture_piece)
            all_the_pieces.pop(piece.board_position)
            all_the_pieces[move] = f"{self.color[0]}{piece.char_identifier}"
            opponent_moves = {move: "Value don't matter" for piece, move in
                              opponent.retrieve_final_moves(
                                  page_source, all_the_pieces, opponent_alive_pieces_copy)}
            try:
                if str(piece) == "King":
                    opponent_moves[move]
                elif str(piece) != "King":
                    opponent_moves[self.king.board_position]
            except KeyError:
                non_check_moves.append((piece, move))
            finally:
                all_the_pieces.pop(move)
                all_the_pieces[piece.board_position] = f"{self.color[0]}{piece.char_identifier}"
            if capture_piece is not None:
                opponent_alive_pieces_copy.append(capture_piece)
        if len(non_check_moves) == 0:
            return None
        return non_check_moves

class White(Player):
    def __init__(self, color = "white"):
        super().__init__(color)
        self.pawn1.board_position = "12"
        self.pawn2.board_position = "22"
        self.pawn3.board_position = "32"
        self.pawn4.board_position = "42"
        self.pawn5.board_position = "52"
        self.pawn6.board_position = "62"
        self.pawn7.board_position = "72"
        self.pawn8.board_position = "82"
        self.rook1.board_position = "11"
        self.rook2.board_position = "81"
        self.kight1.board_position= "21"
        self.kight2.board_position= "71"
        self.bishop1.board_position="31"
        self.bishop2.board_position="61"
        self.king.board_position  = "51"
        self.queen.board_position = "41"

class Black(Player):
    def __init__(self, color = "black"):
        super().__init__(color)