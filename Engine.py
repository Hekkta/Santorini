from tkinter import *
import tkinter.messagebox
import math
import time

root = Tk()
frames_list = []
btn_list = []
charactersPlaced = 0
turn = 0
picked = -1
height = 0
build_num = -1
char_loc = [0, 0]
strt_mat = [0] * 28

amountOfLoops = 0;

def create_frames_and_buttons():  #creating the board
    ndex = 0
    x = 0
    for i in range(5):
        for x in range(5):
            frames_list.append(Frame(root, width=100, height=100))
            frames_list[ndex].propagate(False)
            frames_list[ndex].grid(row=i, column=x, sticky="nsew", padx=2, pady=2)
            btn_list.append(Button(frames_list[ndex], text="0", bg='white', font="Helvetica 16 bold",
                   command=lambda ndex=ndex: pick_character_location(ndex)))
            btn_list[ndex].pack(expand=True, fill=BOTH)
            x += 1
            ndex += 1
    root.resizable(width=False, height=False)

# Checks to see if the square is empty
# Returns True if empty - False if full
def isSquareEmpty(square):
    return square["bg"] == 'white'


def pick_character_location(button_number):  #initial choice of character locations
    global btn_list, charactersPlaced
    
    # Places the first two characters as Blue
    if charactersPlaced < 2:
        if isSquareEmpty(btn_list[button_number]):
            btn_list[button_number]["bg"] = 'blue'
            charactersPlaced += 1
    #Then The second two as red
    elif charactersPlaced < 4:
        if isSquareEmpty(btn_list[button_number]):
            btn_list[button_number]["bg"] = 'red'
            charactersPlaced += 1
    else:
        pick_current_character(button_number)


def pick_current_character(button_number):  #picking a character to move
    global btn_list, turn, picked, height
    if picked != -1:
        # If a character has been picked then move onto moving
        move_current_character(button_number)
    elif ((turn == 0 and btn_list[button_number]["bg"] == 'blue') or 
          (turn == 1 and btn_list[button_number]["bg"] == 'red')):
            btn_list[button_number]["borderwidth"] = 10
            picked = button_number
            height = int(btn_list[button_number]["text"])



def move_current_character(button_number):   #move phase
    global btn_list, turn, picked, height, build_num

    startingSquare = btn_list[picked]
    finishSquare   = btn_list[button_number]
    squareColour = "white"
    
    if turn == 0:
        squareColour = 'blue' # Blue players Turn
    elif turn == 1:
        squareColour = 'red' # Red Players Turn

    if build_num != -1:
        build1(button_number)
    else:
        if isSquareEmpty(finishSquare) and distance(button_number, picked) == 1 and int(finishSquare["text"]) - height < 2:
            finishSquare["bg"] = squareColour
            startingSquare["bg"] = 'white'
            startingSquare["borderwidth"] = 2
            build_num = button_number



def build1(button_number):  #build phase
    global btn_list, turn, build_num, picked

    if isSquareEmpty(btn_list[button_number]) and distance(button_number, build_num) == 1 and int(btn_list[button_number]["text"]) < 4:
        btn_list[button_number]["text"] = int(btn_list[button_number]["text"]) + 1
        build_num = -1
        picked = -1
        turn = (turn+1) % 2
        seconds = time.time()
        #evaluate(0)
        #print(time.time() - seconds)
        #evaluate(1)
        #print(time.time() - seconds)
        #print(amountOfLoops)
        evaluate(2)
        print(time.time() - seconds)
        print(amountOfLoops)
        #evaluate(3)
        #print(time.time() - seconds)


def distance(x, y):  #distance function for the 5x5 board
    if x < 0 or y < 0 or x > 24 or y > 24:
        return 25
    row_x = math.floor(x/5)
    row_y = math.floor(y/5)
    column_x = x % 5
    column_y = y % 5
    result = max(abs(row_x - row_y), abs(column_x - column_y))
    return result


def evaluate(m):
    global btn_list, turn, strt_mat, mat_list_prop, mat_list_temp
    turn_copy = turn
    i = 0
    n = 2*m #moves have to be in 2s
    
    for button in btn_list:  # creating a matrix out of the current position
        strt_mat[i] = int(button["text"]) * 10 # Times the height by 10
        if button["bg"] == 'blue':
            strt_mat[i] += 1 # Add 1 if a blue character is found
        elif button["bg"] == 'red':
            strt_mat[i] += 2 # Add 2 if a red character is found
        i += 1

    # Initialise local variables
    depth = 0
    counter_one = 0
    counter_two = 0
    base_moves = []
    mat_list_temp = [0]
    mat_list_list_prop = []
    mat_list_prop = [strt_mat]
    
    # Move through the amount of moves requested
    while depth < n:
        mat_list_temp = []
        new_matrices = []
        for matrix in mat_list_prop:
            # Check matrix 27 is invalid?? 
            if matrix[27] == -1:
                continue
            charLocation = find_char_loc(matrix, turn)
            # Cycle through 16 values
            while counter_one < 16:
                # Check if the move is invalid? If it isn't add it to the possible moves?
                moved = move_char_mat(matrix, counter_one, depth, charLocation)
                if moved[27] != -1:
                    mat_list_temp.append(moved)
                counter_one += 1
                while counter_two < 8:
                    if len(mat_list_temp) == 0 or move_char_mat(matrix, counter_one-1, depth, charLocation)[27] == -1:
                        break
                    if build_mat(mat_list_temp[len(mat_list_temp)-1], counter_two, depth, counter_one-1)[27] != -1:
                        new_matrices.append(build_mat(mat_list_temp[len(mat_list_temp)-1], counter_two, depth, counter_one-1))
                        if depth == 0:
                            base_moves.append(build_mat(mat_list_temp[len(mat_list_temp)-1], counter_two, depth, counter_one-1))
                    counter_two += 1
                counter_two = 0
            counter_one = 0


        depth += 1
        mat_list_prop = new_matrices
        mat_list_list_prop.append(new_matrices)
        j = 0
        turn = (turn+1) % 2
    analyse2(mat_list_list_prop, turn_copy, n)
    turn = turn_copy




def move_char_mat(matrix, num, depth, loc): #moves the characters in matrix form
    global turn, char_loc

    # Create a new Temporary Matrix
    matrix1 = matrix.copy()
    # Find the index of the movement
    index = math.floor(num/8)
    # Search the matrix for a character
    char_loc = loc
    # Table for acceptable movement
    move_mat = [-6, -5, -4, -1, 1, 4, 5, 6]
    # Possible Squares
    move_square = move_mat[num % 8] + char_loc[index] #square it will move to

    # Check that the square is valid
    if -1 < move_square < 25:
        # Check that the square is next to us
        # Check that the square is empty
        # Check that the the square is only 1 floor higher?
        if distance(char_loc[index], move_square) == 1 and matrix1[move_square] % 10 == 0 and (matrix1[move_square] - matrix1[char_loc[index]]) < 15:
            # Remove the character from the square it's on
            matrix1[char_loc[index]] -= turn + 1
            # Add the character to the square it's moved to
            matrix1[move_square] += turn + 1
            matrix1[25 + turn] = math.floor(matrix[move_square] / 10) #This adds to going up buildings
            char_loc[index] = move_square
        else:
            # Invalid Move
            matrix1[27] = -1
    else:
        # Invalid Move
        matrix1[27] = -1
    return matrix1


def build_mat(matrix, inner_num, depth, outer_num):
    global turn, char_loc
    # Create a temporary matrix
    matrix1 = matrix.copy()
    # Create a temporary character location
    character_loc = char_loc.copy()
    # Get the current index
    index = math.floor(outer_num/8)
    # Get the squares around the character
    build_matrix = [-6, -5, -4, -1, 1, 4, 5, 6]
    build_square = character_loc[index] + build_matrix[inner_num] #square it will build on

    # Make sure the build square is valid
    if -1 < build_square < 25:
        # Check that the square is next to us
        # Check that the square is empty
        # Check that the square is not at max build level
        if distance(character_loc[index], build_square) == 1 and matrix1[build_square] % 10 == 0 and matrix1[build_square] < 35:
            # Build a new level
            matrix1[build_square] += 10
            # If we have finished then set the number to finish
            if depth == 0:
                matrix1[27] = (8*outer_num)+inner_num
            else:
                # Otherwise append the current number
                matrix1.append((8*outer_num)+inner_num)
        else:
            # Invalid Move
            matrix1[27] = -1
        return matrix1
    else:
        # Invalid Move
        matrix1[27] = -1
        return matrix1




def find_char_loc(matrix, turn): #Finding the character locations in matrix form
    global amountOfLoops
    amountOfLoops = amountOfLoops + 1
    counter_one = 0
    counter_two = 0
    character_loc = [0, 0]
    for entry in matrix:  # finding the characters
        if entry % 10 == turn + 1 and counter_one < 2:
            character_loc[counter_one] = counter_two
            counter_one += 1
            if counter_one == 2:
                return character_loc
                break
        counter_two += 1


def analyse2(matrix_list, turn_copy, n):
    global turn

    eval_list = [] #list of evaluations

    for outcome in matrix_list[len(matrix_list)-1]: #getting the evals from the last set of outcomes
        eval_list.append(outcome[25 + (turn % 2)]-outcome[25 + ((turn + 1) % 2)])

    for j in range(1, n):
        i = 0
        eval_list_copy = eval_list.copy()
        eval_list = []
        eval = eval_list_copy[0]
        print(len(eval_list_copy))
        print(len(matrix_list[len(matrix_list)-j]))
        variable_thing = matrix_list[len(matrix_list)-j][0][len(matrix_list[len(matrix_list)-j][0])-2]
        u = 0
        for entry in matrix_list[len(matrix_list)-j]:
            if variable_thing != entry[len(entry)-1]:
                u += 1
            variable_thing = entry[len(matrix_list)-j]
        print("length variable list")
        print(u)
        for outcome in matrix_list[len(matrix_list)-j]: #getting the eval from the last list in outcome
            if i == 0:
                last_move = outcome[len(outcome)-2]
                last_move_backup = outcome[len(outcome)-1]
            else:
                if i == len(matrix_list[len(matrix_list)-j])-1: #if it's the last move in the list...
                    if outcome[len(outcome)-2] != last_move or last_move_backup > outcome[len(outcome)-1]: #if the last move is a new one...
                        eval_list.append(eval)
                        eval_list.append(eval_list_copy[i])
                        break
                        #print("move diff", + outcome[len(outcome)-2])
                    else: #if it's the same move
                        #print("here 3")
                        if j % 2 == 1:
                            eval = min(eval, eval_list_copy[i])
                        elif j % 2 == 0:
                            eval = max(eval, eval_list_copy[i])
                        eval_list.append(eval)
                if outcome[len(outcome)-2] != last_move or last_move_backup > outcome[len(outcome)-1]:
                    eval_list.append(eval)
                    eval = eval_list_copy[i]
                    last_move = outcome[len(outcome)-2]
            if j % 2 == 1:
                eval = min(eval, eval_list_copy[i])
            elif j % 2 == 0:
                eval = max(eval, eval_list_copy[i])
            last_move_backup = outcome[len(outcome) - 1]
            i += 1
    print("eval list")
    print(eval_list)
    print(len(eval_list))

    best_move = eval_list[0]
    i = 0
    r = 0
    for move in eval_list:
        if move > best_move:
            r = i
            best_move = move
        i += 1
    print(matrix_list[0][r])

create_frames_and_buttons()

root.mainloop()

