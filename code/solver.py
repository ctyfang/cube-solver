# Import relevant libraries and functions
import numpy as np
from random import randint

# Initialize cube state as a 3D char array
global cube_state
global moves
global wcross_turns
global wcorn_turns
global second_turns
global ycross_turns
global yedge_turns
global posit_turns
global reorient_turns

moves = []

# Initialize solved cube state
cube_state = np.array([np.full((3,3), color, dtype = 'str') for color in ['R', 'G', 'B', 'O', 'W', 'Y']])

# Set cube state manually
#cube_state = [
#    [
#        ['G','O','Y'],
#        ['G','R','W'],
#        ['B','W','G']
#    ],
#    [
#        ['B','O','Y'],
#        ['R','G','Y'],
#        ['O','W','W']
#    ],
#    [
#        ['B','B','O'],
#        ['B','B','Y'],
#        ['R','R','G']
#    ],
#    [
#        ['G','R','W'],
#        ['B','O','W'],
#        ['W','G','B']
#    ],
#    [
#        ['O','G','W'],
#        ['Y','W','R'],
#        ['O','B','R']
#    ],
#    [
#        ['R','G','Y'],
#        ['O','Y','Y'],
#        ['Y','O','R']
#    ]
#]
    
cube_state = np.array(cube_state)

# Generate Look-Up Dictionaries for conversion of face COLOR to INDEX
global ftoi
ftoi = {'R': 0, 'G': 1, 'B': 2, 'O': 3, 'W': 4, 'Y': 5}

# Generate Look-Up Dictionaries for relative positions of faces
# Given an X-Y-Z coordinate system and assuming the cube has sidelength = 1 unit
# R is in-plane with X = 1
# O is in-plane with X = 0
# G is in-plane with Y = 0
# B is in-plane with Y = 1
# W is in-plane with Z = 1
# Y is in-plane with Z = 0

global relations
relations = {'R' : {'left':'G', 'right':'B', 'opposite':'O', 'above':'W', 'below':'Y'},
             'O' : {'left':'B', 'right':'G', 'opposite':'R', 'above':'W', 'below':'Y'},
             'G' : {'left':'O', 'right':'R', 'opposite':'B', 'above':'W', 'below':'Y'},
             'B' : {'left':'R', 'right':'O', 'opposite':'G', 'above':'W', 'below':'Y'},
             'W' : {'left':'G', 'right':'B', 'opposite':'Y', 'above':'O', 'below':'R'},
             'Y' : {'left':'G', 'right':'B', 'opposite':'W', 'above':'R', 'below':'O'}}

# Functions for manipulation of faces in X, Y, and Z
def turn_x(sign, direction):
    
    # Determine which x-plane face is being manipulated
    if sign == '+':
        side = 'R'
        up_row = 2
        down_row = 0
               
    else:
        side = 'O'
        up_row = 0
        down_row = 2
    
    # Store face that is in-plane with turning axis
    main_old = np.array(cube_state[ftoi[side]])
    main_new = np.transpose(main_old)
    
    # Store tiles perpendicular to turning face
    left_old = cube_state[ftoi[relations[side]['left']], :, 2]
    right_old = cube_state[ftoi[relations[side]['right']], :, 0]
    up_old = cube_state[ftoi[relations[side]['above']], up_row, :]
    down_old = cube_state[ftoi[relations[side]['below']], down_row, :]

    # Execute direction dependent transformation of perpendicular tiles
    if direction == 'cw':
        
        main_new = np.fliplr(main_new)
        left_new = np.array(down_old)
        right_new = np.array(up_old)
        up_new = np.array(left_old)
        down_new = np.array(right_old)
        
        if side == 'O':
            left_new = left_new[::-1]
            right_new = right_new[::-1]

        else:
            up_new = up_new[::-1]
            down_new = down_new[::-1]

    else:
        main_new = np.flipud(main_new)        
        left_new = np.array(up_old)
        right_new = np.array(down_old)
        up_new = np.array(right_old)
        down_new = np.array(left_old)

        if side == 'O':
            up_new = up_new[::-1]
            down_new = down_new[::-1]

        else:
            left_new = left_new[::-1]
            right_new = right_new[::-1]
    
    # Assign transformed cubies to input state
    cube_state[ftoi[side]] = main_new
    cube_state[ftoi[relations[side]['left']], :, 2] = left_new
    cube_state[ftoi[relations[side]['right']], :, 0] = right_new
    cube_state[ftoi[relations[side]['above']], up_row, :] = up_new
    cube_state[ftoi[relations[side]['below']], down_row, :] = down_new

def turn_y(sign, direction):
    
    if sign == '+':
        side = 'B'
        up_col = 2
        down_col = 2
 
    else:
        side = 'G'
        up_col = 0
        down_col = 0
       
    # store main then permute
    main_old = np.array(cube_state[ftoi[side]])
    main_new = np.transpose(main_old)
    
    #print(relations[side])
    # acquire perpendicular rows/columns
    left_old = cube_state[ftoi[relations[side]['left']], :, 2]
    right_old = cube_state[ftoi[relations[side]['right']], :, 0]
    up_old = cube_state[ftoi[relations[side]['above']], :, up_col]
    down_old = cube_state[ftoi[relations[side]['below']], :, down_col]

    if direction == 'ccw':
        main_new = np.flipud(main_new)
        left_new = np.array(up_old)
        right_new = np.array(down_old)
        up_new = np.array(right_old)
        down_new = np.array(left_old)
        
        if side == 'G':
            left_new = left_new[::-1]
            down_new = down_new[::-1]

        else:
            right_new = right_new[::-1]
            up_new = up_new[::-1]

    else:
        
        main_new = np.fliplr(main_new)
        
        left_new = np.array(down_old)
        right_new = np.array(up_old)
        up_new = np.array(left_old)
        down_new = np.array(right_old)
        
        if side == 'B':
            right_new = right_new[::-1]
            down_new = down_new[::-1]

        else:
            left_new = left_new[::-1]
            up_new = up_new[::-1]
            
    
    cube_state[ftoi[side]] = main_new
    cube_state[ftoi[relations[side]['left']], :, 2] = left_new
    cube_state[ftoi[relations[side]['right']], :, 0] = right_new
    cube_state[ftoi[relations[side]['above']], :, up_col] = up_new
    cube_state[ftoi[relations[side]['below']], :, down_col] = down_new

def turn_z(sign, direction):
    
    if sign == '+':
        side = 'W'
        index = 0
 
    else:
        side = 'Y'
        index = 2
            
    # store main then permute
    main_old = np.array(cube_state[ftoi[side]])
    main_new = np.transpose(main_old)
    
    left_old = cube_state[ftoi[relations[side]['left']], index, :]
    right_old = cube_state[ftoi[relations[side]['right']], index, :]
    up_old = cube_state[ftoi[relations[side]['above']], index, :]
    down_old = cube_state[ftoi[relations[side]['below']], index, :]

    if direction == 'cw':
        # permute the front, then all affected rows/cols
        main_new = np.fliplr(main_new)
        left_new = np.array(down_old)
        right_new = np.array(up_old)
        up_new = np.array(left_old)
        down_new = np.array(right_old)

    else:
        main_new = np.flipud(main_new)
        left_new = np.array(up_old)
        right_new = np.array(down_old)
        up_new = np.array(right_old)
        down_new = np.array(left_old)
    
    cube_state[ftoi[side]] = main_new
    cube_state[ftoi[relations[side]['left']], index, :] = left_new
    cube_state[ftoi[relations[side]['right']], index, :] = right_new
    cube_state[ftoi[relations[side]['above']], index, :] = up_new
    cube_state[ftoi[relations[side]['below']], index, :] = down_new

# Compile X/Y/Z turning functions
tot_turns = 0
def turn(color, direction = 'cw'):
    global tot_turns
    tot_turns = tot_turns + 1
    
    if (direction == 'cw'):
        move = color
    else:
        move = color + "\'"
        
    #print(move)
    moves.append(move)
    
    # See which face is closest to next face on list
    # Re-orient
    # Execute
        
    if color == 'R':
        turn_x('+', direction)
        
    elif color == 'O':
        turn_x('-', direction)
        
    elif color == 'G':
        turn_y('-', direction)
        
    elif color == 'B':
        turn_y('+', direction)
        
    elif color == 'W':
        turn_z('+', direction)
        
    else:
        turn_z('-', direction)

# Determines whether a tile is an edge
# It should be noted that a particular cube face only has 3 types of tiles
# [CORNERS, EDGES, CENTERS]
def is_edge(row, col):
    
    # an edge piece can be in four possible locations
    # (0,1), (1,0), (1,2), (2,1)
    if row == 0 and col == 1:
        return 'above'
    
    elif row == 1 and col == 0:
        return 'left'
        
    elif row == 1 and col == 2:
        return 'right'
        
    elif row == 2 and col == 1:
        return 'below'
        
    else:
        return 0

# Given an edge tile, determines parameters of the tile perpendicular to it
def identify_edge(face, rel_location):
    
    if face == 'W':
        index = [0, 1]
        L_index = index
        R_index = index
        U_index = index
        D_index = index

    elif face == 'Y':
        index = [2, 1]
        L_index = index
        R_index = index
        U_index = index
        D_index = index

    else:
        if face == 'R':
            U_index = [2, 1]
            D_index = [0, 1]
        
        elif face == 'O':
            U_index = [0, 1]
            D_index = [2, 1]

        elif face == 'G':
            U_index = [1, 0]
            D_index = [1, 0]

        else:
            U_index = [1, 2]
            D_index = [1, 2]
            

        L_index = [1, 2]
        R_index = [1, 0]

    if rel_location == 'left':
        nonwhite_id = cube_state[ftoi[relations[face]['left']], L_index[0], L_index[1]]
        nonwhite_face = relations[face]['left']

    elif rel_location == 'right':
        nonwhite_id = cube_state[ftoi[relations[face]['right']], R_index[0], R_index[1]]
        nonwhite_face = relations[face]['right']
    
    elif rel_location == 'above':
        nonwhite_id = cube_state[ftoi[relations[face]['above']], U_index[0], U_index[1]]
        nonwhite_face = relations[face]['above']
    
    else:
        nonwhite_id = cube_state[ftoi[relations[face]['below']], D_index[0], D_index[1]]
        nonwhite_face = relations[face]['below']

    return nonwhite_id, nonwhite_face

# Randomize the cube state with a given number of turns
def randomize(num_moves):
    
    int_to_face = { 0: 'R', 1: 'G', 2: 'O', 3: 'B', 4: 'W', 5: 'Y'}
    int_to_dir = { 0: 'cw', 1: 'ccw'}

    for i in range (0, num_moves):
        face = int_to_face[randint(0, 5)]
        direction = int_to_dir[randint(0, 1)]
        
        turn(face, direction)
        
# Given random cube state, complete the white cross
def white_cross():
    global tot_turns
    tot_turns = 0
    #iterations = 0
    
    while(True):
        
        completed_count = 0
        #iterations += 1
        piece_located = False
        
        # iterate over every cube face until you find a white edge tile
        for face in ['Y', 'R', 'O', 'G', 'B', 'W']:
            
            #ndenumerate returns coordinates and values of that array
            for index, color in np.ndenumerate(cube_state[ftoi[face]]):
                        
                if(color == 'W' and is_edge(index[0], index[1])):
                    
                    # store indices and location id
                    row = index[0]
                    col = index[1]
                    location = is_edge(row, col)
                    
                    # print("DEBUG: current face is {}, location is {}".format(face, location))
                    # print(cube_state)
                    
                    # identify the edge tile by color and location
                    nonwhite_id, nonwhite_face = identify_edge(face, location)
                    
                    # Check that the located piece wasn't one that's already done
                    if(face == 'W' and nonwhite_id == nonwhite_face):
                        completed_count += 1
                        # print('DEBUG: Found a completed tile')
                        continue
                        
                    piece_located = True
                    # print('DEBUG: found a white tile!!!')
                    # print('DEBUG: it\'s on the {} face, in row {}, col {}'.format(face, row, col))
                    break
            
            
            if(piece_located == True):
                break
        
        # --- COMPLETION CHECK ---
        if(completed_count == 4):
            break
        
        # --- SCENARIO CHECK AND MOVE EXECUTION---
        # BOTTOM scenario, we rotate bottom face until color matches
        if(face == 'Y'):

            # determine the relation between current face and the correct face
            if(relations[nonwhite_face]['left'] == nonwhite_id):
                turn('Y', 'ccw')
                
            elif(relations[nonwhite_face]['right'] == nonwhite_id):
                turn('Y', 'cw')
                
            elif(relations[nonwhite_face]['opposite'] == nonwhite_id):
                turn('Y', 'cw')
                turn('Y', 'cw')
                
            # turn nonwhite_id face twice
            turn(nonwhite_id, 'cw')
            turn(nonwhite_id, 'cw')
            
        # TOP scenario, we rotate the cubie down to the bottom row of the side
        elif(face == 'W'):
            
            nonwhite_id, nonwhite_face = identify_edge(face, location)

            turn(nonwhite_face, 'cw')
            turn(nonwhite_face, 'cw')
            
            # Experimental
            if(relations[nonwhite_face]['left'] == nonwhite_id):
                turn('Y', 'ccw')
                
            elif(relations[nonwhite_face]['right'] == nonwhite_id):
                turn('Y', 'cw')
                
            elif(relations[nonwhite_face]['opposite'] == nonwhite_id):
                turn('Y', 'cw')
                turn('Y', 'cw')
                
            turn(nonwhite_id, 'cw')
            turn(nonwhite_id, 'cw')
            
        # SIDE scenario, we check if that face is picky, then execute an
        # appropriate moveset to get it to the bottom row
        else:
            
            # check white row/col above the face, is this portion of the cross complete?
            if(face == 'R'):
                index = [2, 1]

            elif(face == 'O'):
                index = [0, 1]

            elif(face == 'G'):
                index = [1, 0]

            else:
                index = [1, 2]
            
            # if this face already has a completed cross above it..
            if((cube_state[ftoi[relations[face]['above']], index[0], index[1]] == 'W') and (cube_state[ftoi[face], 0, 1] == face)):
                
                # move to bottom row
                if(location == 'left'):
                    turn(face, 'ccw')
                    
                elif(location == 'right'):
                    turn(face, 'cw')
                    
                # move the tile to its corresponding face
                if(relations[face]['left'] == nonwhite_id):
                    turn('Y', 'ccw')
                    
                elif(relations[face]['right'] == nonwhite_id):
                    turn('Y', 'cw')
                  
                elif(relations[face]['opposite'] == nonwhite_id):
                    turn('Y', 'cw')
                    turn('Y', 'cw')
                
                turn(face, 'cw')
                # at this point.. white tile is below it's correct position
                # moveset is D R L' F' R' L, while facing nonwhite_face, white above
                turn('Y', 'cw')
                turn(relations[nonwhite_id]['right'], 'cw')
                turn(relations[nonwhite_id]['left'], 'ccw')
                turn(nonwhite_id, 'ccw')
                turn(relations[nonwhite_id]['right'], 'ccw')
                turn(relations[nonwhite_id]['left'], 'cw')
            
            else:
                if(location == 'left'):
                    turn(face, 'ccw')
                    
                elif(location == 'right'):
                    turn(face, 'cw')
                    
    
                elif(location == 'above'):
                    turn(face, 'cw')
                    turn(face, 'cw')
                    # print('DEBUG: nw_id is ' + nonwhite_id)
                
                if(relations[face]['left'] == nonwhite_id):
                    turn('Y', 'ccw')
                        
                elif(relations[face]['right'] == nonwhite_id):
                    turn('Y', 'cw')
                
                elif(relations[face]['opposite'] == nonwhite_id):
                    turn('Y', 'cw')
                    turn('Y', 'cw')
                
                # at this point.. white tile is below it's correct position
                # moveset is D R L' F' R' L, while facing nonwhite_face, white above
                turn('Y', 'cw')
                turn(relations[nonwhite_id]['right'], 'cw')
                turn(relations[nonwhite_id]['left'], 'ccw')
                turn(nonwhite_id, 'ccw')
                turn(relations[nonwhite_id]['right'], 'ccw')
                turn(relations[nonwhite_id]['left'], 'cw')
        
        # --- FINAL CHECK OF ITERATIONS DONE AND OUTPUT STATE ---                 
#        print('{} iterations done..'.format(iterations))
#        print(cube_state)
    print("WHITECROSS Turns = " + str(tot_turns))
    global wcross_turns
    wcross_turns = tot_turns

def is_corner(index):
    
    if(index[0] == 0 and index[1] == 0):
        return 'above-left'
    elif(index[0] == 0 and index[1] == 2):
        return 'above-right'
        
    elif(index[0] == 2 and index[1] == 0):
        return 'below-left'
        
    elif(index[0] == 2 and index[1] == 2):
        return 'below-right'
        
    else:
        return False

# Given a face, and a location on that face, checks if it's connected tiles
# match the connected face
def check_corner(face, rel_location, solving = False):
    
    # TOP FACE
    if face == 'W':
        
        # CALC INDICES OF CONNECTED TILES
        if(rel_location[0] == 'above'):
            Y_index = [0, 2]
            X_index = [0, 0]

            if rel_location[1] == 'right':
                X_index = Y_index
                Y_index = [0, 0]
                

        else:
            Y_index = [0, 0]
            X_index = [0, 2]

            if rel_location[1] == 'right':
                X_index = Y_index
                Y_index = [0, 2]
    
    # BOTTOM FACE
    elif face == 'Y':
        
        if rel_location[0] == 'above':
            X_index = [2, 2]
            Y_index = [2, 0]

            if rel_location[1] == 'right':
                X_index = Y_index
                Y_index = [2, 2]

        else:
            X_index = [2, 0]
            Y_index = [2, 2]

            if rel_location[1] == 'right':
                X_index = Y_index
                Y_index = [2, 0]
    
    # 1/4 SIDE FACES  
    else:
        
        if face == 'R' or face == 'O':
            
            if rel_location[0] == 'above' and rel_location[1] == 'left':
                X_index = [0,2]

                if face == 'R':
                    Y_index = X_index[::-1]

                else:
                    Y_index = X_index

                    
            elif rel_location[0] == 'above' and rel_location[1] == 'right':
                X_index = [0,0]

                if face == 'R':
                    Y_index = [2,2]

                else:
                    Y_index = X_index
                    
            elif rel_location[0] == 'below' and rel_location[1] == 'left':
                X_index = [2,2]

                if face == 'R':
                    Y_index = [0,0]

                else:
                    Y_index = [2,2]

            else:
                X_index = [2,0]

                if face == 'R':
                    Y_index = X_index[::-1]

                else:
                    Y_index = X_index
       
        else:
            if rel_location[0] == 'above' and rel_location[1] == 'left':
                X_index = [0,2]

                if face == 'G':
                    Y_index = [0,0]

                else:
                    Y_index = [2,2]

                    
            elif rel_location[0] == 'above' and rel_location[1] == 'right':
                X_index = [0,0]
                Y_index = [2,0]

                if face == 'B':
                    Y_index = Y_index[::-1]
                    
            elif rel_location[0] == 'below' and rel_location[1] == 'left':
                X_index = [2,2]
                Y_index = [2,0]

                if face == 'B':
                    Y_index = Y_index[::-1]

            else:
                X_index = [2,0]
                Y_index = [0,0]

                if face == 'B':
                    Y_index = [2,2]

    if(solving == True):
        return X_index
        
    # STORE X DATA
    if rel_location[1] == 'left':
        X_face = relations[face]['left']
            
    else:
        X_face = relations[face]['right']

    # STORE Y DATA
    if rel_location[0] == 'above':
        Y_face = relations[face]['above']

    else:
        Y_face = relations[face]['below']

        
    X_id = cube_state[ftoi[X_face], X_index[0], X_index[1]]
    Y_id = cube_state[ftoi[Y_face], Y_index[0], Y_index[1]]

    
    # --- ACTUAL CHECK ---
    # 3 possible scenarios, right position wrong orient, right, wrong position
    
    # wrong position
    if X_id != X_face and Y_id != Y_face:
        return 0

    # right position, right orientation
    elif X_id == X_face and Y_id == Y_face:
        return 1
    
    # right position, wrong orientation
    else:
        return 2
    


# WHITE CORNERS
def white_corners():
    global tot_turns
    tot_turns = 0
    # white corner can be on 1/6 ftoi, in 1/4 corners
    iterations = 0
    
    while True:
        
        completed_corners = 0
        corner_found = False
        
        # --- LOCATE THE CORNER ---
        
        # iterate through each tile on each tile
        for face in ['R', 'O', 'G', 'B', 'W', 'Y']:
        
            for index, color in np.ndenumerate(cube_state[ftoi[face]]):
                
                # check if tile is white and is a corner
                if(cube_state[ftoi[face], index[0], index[1]] == 'W' and is_corner(index)):
                    #print(face)
                    location = is_corner(index)
                    #print(location)
                    location = location.split('-')
                    #print(location)
#                    print('DEBUG: LOCATION IS {},{} on {} face'.format(location[0], location[1], face))
                    
                    if face == 'W' and check_corner(face, location) == 1:
                        completed_corners += 1
                        #print('DEBUG: Its done already')
                        continue
                    
                    corner_found = True
                    break
                    
            
            if corner_found == True or completed_corners == 4:
                break
        
        if completed_corners == 4 or iterations == 40:
            break
        
        iterations += 1
        
    # --- IS THE PIECE ON A XY FACE OR Z ---
        
        if face == 'W':

            if location[0] == 'above' and location[1] == 'left':
                turn(relations[face][location[1]], 'ccw')
                turn('Y', 'ccw')
                turn(relations[face][location[1]], 'cw')
                    
            elif location[0] == 'above' and location[1] == 'right':
                turn(relations[face][location[1]], 'cw')
                turn('Y', 'cw')
                turn(relations[face][location[1]], 'ccw')
                    
            elif location[0] == 'below' and location[1] == 'left':
                turn(relations[face][location[1]], 'cw')
                turn('Y', 'cw')
                turn(relations[face][location[1]], 'ccw')
                    
            else:
                turn(relations[face][location[1]], 'ccw')
                turn('Y', 'ccw')
                turn(relations[face][location[1]], 'cw')
                       
        elif face == 'Y':

            if location[0] == 'above' and location[1] == 'left':
                turn(relations[face][location[1]], 'cw')
                turn('Y', 'ccw')
                turn(relations[face][location[1]], 'ccw')
                    
            elif location[0] == 'above' and location[1] == 'right':
                turn(relations[face][location[1]], 'ccw')
                turn('Y', 'cw')
                turn(relations[face][location[1]], 'cw')
                    
            elif location[0] == 'below' and location[1] == 'left':
                turn('Y', 'cw')
                turn(relations[face][location[1]], 'cw')
                turn('Y', 'ccw')
                turn(relations[face][location[1]], 'ccw')
                    
            else:
                turn(relations[face][location[1]], 'cw')
                turn('Y', 'ccw')
                turn(relations[face][location[1]], 'ccw')
                
        else:
            
            
                # rotate to third row
            if location[0] == 'above':   
                if location[1] == 'left':
                    turn(face, 'ccw')
                    turn('Y', 'ccw')
                    #print(cube_state)
                    turn(face, 'cw')
                            
                else:
                    turn(face, 'cw')
                    turn('Y', 'cw')
                    turn(face, 'ccw')
                        
                # solve!!!
            else:
                indices = check_corner(face, location, True)
                #print(indices)
            
                if location[1] == 'left':
                    target_color = cube_state[ftoi[relations[face]['left']], indices[0], indices[1]]
    
                    if relations[face]['opposite'] == target_color:
                        turn(target_color, 'cw')
                        turn('Y', 'ccw')
                        turn(target_color, 'ccw')
                            
                    elif relations[face]['right'] == target_color:
                        turn('Y', 'ccw')
                        turn(target_color, 'cw')
                        turn('Y', 'ccw')
                        turn(target_color, 'ccw')
                            
                    elif face == target_color:
                        turn('Y', 'cw')
                        turn('Y', 'cw')
                        turn(target_color, 'cw')
                        turn('Y', 'ccw')
                        turn(target_color, 'ccw')
                            
                    else:
                        turn('Y', 'cw')
                        turn(target_color, 'cw')
                        turn('Y', 'ccw')
                        turn(target_color, 'ccw')
                        
                else:
                    target_color = cube_state[ftoi[relations[face]['right']], indices[0], indices[1]]
                    
                    if relations[face]['opposite'] == target_color:
                        turn(target_color, 'ccw')
                        turn('Y', 'cw')
                        turn(target_color, 'cw')
                            
                    elif relations[face]['left'] == target_color:
                        turn('Y', 'cw')
                        turn(target_color, 'ccw')
                        turn('Y', 'cw')
                        turn(target_color, 'cw')
                            
                    elif face == target_color:
                        turn('Y', 'ccw')
                        turn('Y', 'ccw')
                        turn(target_color, 'ccw')
                        turn('Y', 'cw')
                        turn(target_color, 'cw')
                            
                    else:
                        turn('Y', 'ccw')
                        turn(target_color, 'ccw')
                        turn('Y', 'cw')
                        turn(target_color, 'cw')
      
    print("WHITECORNERS Turns = " + str(tot_turns))
    global wcorn_turns
    wcorn_turns = tot_turns
                             
def second_layer_incomplete():
    
    is_incomplete = False
    
    for face in ['R', 'B', 'G', 'O']:
        if not np.array_equiv(cube_state[ftoi[face], 1, :], np.array([face, face, face])):
            is_incomplete = True
            break
        
    return is_incomplete
        
def second_layer():
    iterations = 0
    global tot_turns
    global second_turns
    tot_turns = 0
    
    # While the second layeer is incomplete, continue solving
    while second_layer_incomplete():
        
        piece_found = False
        
        # Check the yellow cross pieces and find an edge piece without any yellow
        for location, indices in [['above', [0, 1]], ['below', [2, 1]], ['left', [1, 0]], ['right', [1, 2]]]:
            
            if cube_state[ftoi['Y'], indices[0], indices[1]] != 'Y':
                nonwhite_id, nonwhite_face = identify_edge('Y', location)
                
                if nonwhite_id != 'Y':
                    piece_found = True
                    yellow_id = cube_state[ftoi['Y'], indices[0], indices[1]]
                    break
        
        # If a non-yellow edge cubie was found, execute F2L or F2R
        if piece_found == True:
            # Match the edge
            if relations[nonwhite_face]['left'] == nonwhite_id:
                turn('Y', 'ccw')
                
            elif relations[nonwhite_face]['right'] == nonwhite_id:
                turn('Y', 'cw')
                
            elif relations[nonwhite_face]['opposite'] == nonwhite_id:
                turn('Y', 'cw')
                turn('Y', 'cw')
                    
            # Execute F2L or F2R    
            # U R U’ R’ U’ F’ U F
            if relations[nonwhite_id]['left'] == yellow_id:
                turn('Y', 'cw')
                turn(relations[nonwhite_id]['left'], 'cw')
                turn('Y', 'ccw')
                turn(relations[nonwhite_id]['left'], 'ccw')
                turn('Y', 'ccw')
                turn(nonwhite_id, 'ccw')
                turn('Y', 'cw')
                turn(nonwhite_id, 'cw')
                
            # U’ L’ U L U F U’ F’
            else:
                turn('Y', 'ccw')
                turn(relations[nonwhite_id]['right'], 'ccw')
                turn('Y', 'cw')
                turn(relations[nonwhite_id]['right'], 'cw')
                turn('Y', 'cw')
                turn(nonwhite_id, 'cw')
                turn('Y', 'ccw')
                turn(nonwhite_id, 'ccw')
        
        # If a non-yellow edge cubie wasn't found, orientation of an edge is wrong
        else:
            
            # Locate the edge of incorrect orientation
            for face in ['R', 'O', 'G', 'B']:
                
#                print('For face {}'.format(face))
#                print(cube_state[ftoi[face], 1, 1:3])
                
#                currface_id = cube_state [ftoi[face], 1, 0]
#                perpface_id, perpface = identify_edge(face, 'left')
                
                # Find an incorrect piece
                if (cube_state[ftoi[face], 1, 0] != face) and (np.array_equiv(cube_state[ftoi[face], 1, 1:3], np.array([face, face]))):
                    break
                
            turn('Y', 'cw')
            turn(relations[face]['left'], 'cw')
            turn('Y', 'ccw')
            turn(relations[face]['left'], 'ccw')
            turn('Y', 'ccw')
            turn(face, 'ccw')
            turn('Y', 'cw')
            turn(face, 'cw')
            
        iterations += 1
    print("SECONDLAY Turns = " + str(tot_turns))    
    second_turns = tot_turns

def cross_incomplete():
    
    if cube_state[ftoi['Y'], 0, 1] != 'Y' or cube_state[ftoi['Y'], 1, 0] != 'Y' or cube_state[ftoi['Y'], 1, 2] != 'Y' or cube_state[ftoi['Y'], 2, 1] !='Y':
        return True
        
    else:
        return False
        
        
def analyze_cross():
    
    # check four edges of yellow face
    # count the number of yellow tiles, store nonyellow_id and face of them

    # if count = 0, we have the dot
    # else, we have bar or L
    #   if faces are opposite, we have bar
    #   else, which face has the other tile to it's right? face to the left is where we want to face
    yellow_count = 0
    nonyellow_faces = []
    
    for location, edge_index in [['above', [0, 1]], ['left', [1, 0]], ['right', [1, 2]], ['below', [2, 1]]]:
        if cube_state[ftoi['Y'], edge_index[0], edge_index[1]] == 'Y':
            nonyellow_id, nonyellow_face = identify_edge('Y', location)
            nonyellow_faces.append(nonyellow_face)
            yellow_count += 1
            
    if yellow_count == 0:
        return 'dot', 'R'
        
    else:
        if relations[nonyellow_faces[0]]['opposite'] == nonyellow_faces[1]:
            return 'bar', relations[nonyellow_faces[0]]['left']

        elif relations[nonyellow_faces[0]]['right'] == nonyellow_faces[1]:
            return 'hook', relations[nonyellow_faces[0]]['left']

        else:
            return 'hook', relations[nonyellow_faces[1]]['left']
            
        
def yellow_cross():

    iterations = 0
    global tot_turns
    global ycross_turns
    tot_turns = 0
    
    while cross_incomplete():  
         
        current_state, face = analyze_cross()
        
        if current_state == 'dot' or current_state == 'bar':
            
            # F R U R' U' F'
            turn(face, 'cw')
            turn(relations[face]['left'], 'cw')
            turn('Y', 'cw')
            turn(relations[face]['left'], 'ccw')
            turn('Y', 'ccw')
            turn(face, 'ccw')
            
        else:
            
            # F U R U’ R’ F’
            turn(face, 'cw')
            turn('Y', 'cw')
            turn(relations[face]['left'], 'cw')
            turn('Y', 'ccw')
            turn(relations[face]['left'], 'ccw')
            turn(face, 'ccw')
            
        iterations += 1
    
    print("YELLOWCROSS Turns = " + str(tot_turns))
    ycross_turns = tot_turns
#    print('Total iterations = {}'.format(iterations))


global correct_relations 
correct_relations = {'R':{'left':'G', 'right':'B'},
                            'O':{'left':'B', 'right':'G'},
                            'G':{'left':'O', 'right':'R'},
                            'B':{'left':'R', 'right':'O'}}

def check_relations(face):
    
    score = 0
    
    curr_id = cube_state[ftoi[face], 2, 1]
    left_id = cube_state[ftoi[relations[face]['left']], 2, 1]
    right_id = cube_state[ftoi[relations[face]['right']], 2, 1]

    if correct_relations[curr_id]['left'] == left_id:
        score += 1
        
    if correct_relations[curr_id]['right'] == right_id:
        score += 1
        
    return curr_id, left_id, right_id, score
    
def relation_score(face):

    score = 0
    
    curr_id = cube_state[ftoi[face], 2, 1]
    left_id = cube_state[ftoi[relations[face]['left']], 2, 1]
    right_id = cube_state[ftoi[relations[face]['right']], 2, 1]

    if correct_relations[curr_id]['left'] == left_id:
        score += 1
        
    if correct_relations[curr_id]['right'] == right_id:
        score += 1
        
    return score
    
    
def yellow_edges():
    global tot_turns
    global yedge_turns
    tot_turns = 0
    # Arbitrarily set initial face
    scores = {'R':relation_score('R'),
              'O':relation_score('O'),
              'G':relation_score('G'),
              'B':relation_score('B')
              }
              
    score_sum = 0
    wrong_face = 'none'
    
    for face in scores:
        score_sum += scores[face]
        
        if scores[face] == 0:
            wrong_face = face 
    
    if score_sum == 0:
        face = 'R'
        
        # R U R’ U R U U R’ U
        turn(relations[face]['left'], 'cw')
        turn('Y', 'cw')
        turn(relations[face]['left'], 'ccw')
        turn('Y', 'cw')
        turn(relations[face]['left'], 'cw')
        turn('Y', 'cw')
        turn('Y', 'cw')
        turn(relations[face]['left'], 'ccw')
        turn('Y', 'cw')
        
        face = 'O'
        turn(relations[face]['left'], 'cw')
        turn('Y', 'cw')
        turn(relations[face]['left'], 'ccw')
        turn('Y', 'cw')
        turn(relations[face]['left'], 'cw')
        turn('Y', 'cw')
        turn('Y', 'cw')
        turn(relations[face]['left'], 'ccw')
        turn('Y', 'cw')
        
    elif score_sum == 8:
        pass
    
    else:
        if scores[relations[wrong_face]['right']] == 0:
            pass
           
        else:
            wrong_face = relations[wrong_face]['left']
        
        turn(relations[wrong_face]['left'], 'cw')
        turn('Y', 'cw')
        turn(relations[wrong_face]['left'], 'ccw')
        turn('Y', 'cw')
        turn(relations[wrong_face]['left'], 'cw')
        turn('Y', 'cw')
        turn('Y', 'cw')
        turn(relations[wrong_face]['left'], 'ccw')
        turn('Y', 'cw')
        
    curr_id = cube_state[ftoi['R'], 2, 1]
    curr_face = 'R'
    
    if curr_id == relations[curr_face]['left']:
        turns = 1
        
    elif curr_id == relations[curr_face]['right']:
        turns = 3
        
    elif curr_id == relations[curr_face]['opposite']:
        turns = 2
        
    else:
        turns = 0
        
    
    for i in range(0, turns):
        turn('Y', 'ccw')
    
    print("YELLOWEDGES Turns = " + str(tot_turns))
    yedge_turns = tot_turns

def score_corner(face, rel_location):
    
    # TOP FACE
    if face == 'W':
        
        # CALC INDICES OF CONNECTED TILES
        if(rel_location[0] == 'above'):
            Y_index = [0, 2]
            X_index = [0, 0]

            if rel_location[1] == 'right':
                X_index = Y_index
                Y_index = [0, 0]
                

        else:
            Y_index = [0, 0]
            X_index = [0, 2]

            if rel_location[1] == 'right':
                X_index = Y_index
                Y_index = [0, 2]
    
    # BOTTOM FACE
    elif face == 'Y':
        
        if rel_location[0] == 'above':
            X_index = [2, 2]
            Y_index = [2, 0]

            if rel_location[1] == 'right':
                X_index = Y_index
                Y_index = [2, 2]

        else:
            X_index = [2, 0]
            Y_index = [2, 2]

            if rel_location[1] == 'right':
                X_index = Y_index
                Y_index = [2, 0]
    
    # 1/4 SIDE FACES  
    else:
        
        if face == 'R' or face == 'O':
            
            if rel_location[0] == 'above' and rel_location[1] == 'left':
                X_index = [0,2]

                if face == 'R':
                    Y_index = X_index[::-1]

                else:
                    Y_index = X_index

                    
            elif rel_location[0] == 'above' and rel_location[1] == 'right':
                X_index = [0,0]

                if face == 'R':
                    Y_index = [2,2]

                else:
                    Y_index = X_index
                    
            elif rel_location[0] == 'below' and rel_location[1] == 'left':
                X_index = [2,2]

                if face == 'R':
                    Y_index = [0,0]

                else:
                    Y_index = [2,2]

            else:
                X_index = [2,0]

                if face == 'R':
                    Y_index = X_index[::-1]

                else:
                    Y_index = X_index
       
        else:
            if rel_location[0] == 'above' and rel_location[1] == 'left':
                X_index = [0,2]

                if face == 'G':
                    Y_index = [0,0]

                else:
                    Y_index = [2,2]

                    
            elif rel_location[0] == 'above' and rel_location[1] == 'right':
                X_index = [0,0]
                Y_index = [2,0]

                if face == 'B':
                    Y_index = Y_index[::-1]
                    
            elif rel_location[0] == 'below' and rel_location[1] == 'left':
                X_index = [2,2]
                Y_index = [2,0]

                if face == 'B':
                    Y_index = Y_index[::-1]

            else:
                X_index = [2,0]
                Y_index = [0,0]

                if face == 'B':
                    Y_index = [2,2]
    
    # STORE X DATA
    if rel_location[1] == 'left':
        X_face = relations[face]['left']
            
    else:
        X_face = relations[face]['right']

    # STORE Y DATA
    if rel_location[0] == 'above':
        Y_face = relations[face]['above']

    else:
        Y_face = relations[face]['below']

    X_id = cube_state[ftoi[X_face], X_index[0], X_index[1]]
    Y_id = cube_state[ftoi[Y_face], Y_index[0], Y_index[1]]
    
    if rel_location[0] == 'above':
        curr_index1 = 0
        
    else:
        curr_index1 = 2
        
    if rel_location[1] == 'left':
        curr_index2 = 0
        
    else:
        curr_index2 = 2
        
    curr_id = cube_state[ftoi[face], curr_index1, curr_index2]
    
    # --- ACTUAL CHECK ---
    # 3 possible scenarios, right position wrong orient, right, wrong position
    corner_colors = {X_id, Y_id, curr_id}
#    print('CORNER COLORS')
#    print(corner_colors)
    
    correct_colors = {'Y', relations[face][rel_location[1]], relations[face][rel_location[0]]}
#    print('CORRECT COLORS')
#    print(correct_colors)

    matches = corner_colors & correct_colors
    
    if len(matches) == 3:
        return 1
        
    else:
        return 0
        
def position_yellow_corners():
    global tot_turns
    global posit_turns
    tot_turns = 0
    
    for iterations in range (0, 3):        
        score_sum = 0
        
        for location in ['above-left', 'above-right', 'below-left', 'below-right']:
            
            location_list = location.split('-')
            score = score_corner('Y', location_list)
            score_sum += score
            
            if score == 1:
                target_location = location
        
        
#        print('DEBUG: Score = {}'.format(score_sum))
        if score_sum == 4:
            pass
        
        elif score_sum == 1:
#            print('Target location is {}'.format(target_location))
            if target_location == 'above-left':
                face = relations['Y']['above']

            elif target_location == 'above-right':
                face = relations['Y']['right']

            elif target_location == 'below-left':
                face = relations['Y']['left']

            else:
                face = relations['Y']['below']

            # U R U' L' U R' U' L
            turn('Y', 'cw')
            turn(relations[face]['left'], 'cw')
            turn('Y', 'ccw')
            turn(relations[face]['right'], 'ccw')
            turn('Y', 'cw')
            turn(relations[face]['left'], 'ccw')
            turn('Y', 'ccw')
            turn(relations[face]['right'], 'cw')
            
        else:
            
            face = 'R'
            # U R U' L' U R' U' L
            turn('Y', 'cw')
            turn(relations[face]['left'], 'cw')
            turn('Y', 'ccw')
            turn(relations[face]['right'], 'ccw')
            turn('Y', 'cw')
            turn(relations[face]['left'], 'ccw')
            turn('Y', 'ccw')
            turn(relations[face]['right'], 'cw')
    
    score_sum = 0
    
    for location in ['above-left', 'above-right', 'below-left', 'below-right']:
            
        location_list = location.split('-')
        score = score_corner('Y', location_list)
        score_sum += score
            
#    print('DEBUG: Score = {}'.format(score_sum))
#    
#    if score_sum == 0 or score_sum == 1:
#        print(cube_state)
#        print('ERROR')
#    print(score_corner('Y', ['above', 'left']))
#    print(score_corner('Y', ['above', 'right']))
#    print(score_corner('Y', ['below', 'left']))
#    print(score_corner('Y', ['below', 'right'])) 

    print("POSITIONYELLOWCORNERS Turns = " + str(tot_turns)) 
    posit_turns = tot_turns

def score_corner_orientation(face, rel_location):
    
    # TOP FACE
    if face == 'W':
        
        # CALC INDICES OF CONNECTED TILES
        if(rel_location[0] == 'above'):
            Y_index = [0, 2]
            X_index = [0, 0]

            if rel_location[1] == 'right':
                X_index = Y_index
                Y_index = [0, 0]
                

        else:
            Y_index = [0, 0]
            X_index = [0, 2]

            if rel_location[1] == 'right':
                X_index = Y_index
                Y_index = [0, 2]
    
    # BOTTOM FACE
    elif face == 'Y':
        
        if rel_location[0] == 'above':
            X_index = [2, 2]
            Y_index = [2, 0]

            if rel_location[1] == 'right':
                X_index = Y_index
                Y_index = [2, 2]

        else:
            X_index = [2, 0]
            Y_index = [2, 2]

            if rel_location[1] == 'right':
                X_index = Y_index
                Y_index = [2, 0]
    
    # 1/4 SIDE FACES  
    else:
        
        if face == 'R' or face == 'O':
            
            if rel_location[0] == 'above' and rel_location[1] == 'left':
                X_index = [0,2]

                if face == 'R':
                    Y_index = X_index[::-1]

                else:
                    Y_index = X_index

                    
            elif rel_location[0] == 'above' and rel_location[1] == 'right':
                X_index = [0,0]

                if face == 'R':
                    Y_index = [2,2]

                else:
                    Y_index = X_index
                    
            elif rel_location[0] == 'below' and rel_location[1] == 'left':
                X_index = [2,2]

                if face == 'R':
                    Y_index = [0,0]

                else:
                    Y_index = [2,2]

            else:
                X_index = [2,0]

                if face == 'R':
                    Y_index = X_index[::-1]

                else:
                    Y_index = X_index
       
        else:
            if rel_location[0] == 'above' and rel_location[1] == 'left':
                X_index = [0,2]

                if face == 'G':
                    Y_index = [0,0]

                else:
                    Y_index = [2,2]

                    
            elif rel_location[0] == 'above' and rel_location[1] == 'right':
                X_index = [0,0]
                Y_index = [2,0]

                if face == 'B':
                    Y_index = Y_index[::-1]
                    
            elif rel_location[0] == 'below' and rel_location[1] == 'left':
                X_index = [2,2]
                Y_index = [2,0]

                if face == 'B':
                    Y_index = Y_index[::-1]

            else:
                X_index = [2,0]
                Y_index = [0,0]

                if face == 'B':
                    Y_index = [2,2]
    
    # STORE X DATA
    if rel_location[1] == 'left':
        X_face = relations[face]['left']
            
    else:
        X_face = relations[face]['right']

    # STORE Y DATA
    if rel_location[0] == 'above':
        Y_face = relations[face]['above']

    else:
        Y_face = relations[face]['below']

    X_id = cube_state[ftoi[X_face], X_index[0], X_index[1]]
    Y_id = cube_state[ftoi[Y_face], Y_index[0], Y_index[1]]
    
    if rel_location[0] == 'above':
        curr_index1 = 0
        
    else:
        curr_index1 = 2
        
    if rel_location[1] == 'left':
        curr_index2 = 0
        
    else:
        curr_index2 = 2
        
    curr_id = cube_state[ftoi[face], curr_index1, curr_index2]
    
#    print('Curr = {}\n X_face = {}\n Y_face = {}'.format(face, X_face, Y_face))
    
    X_face = cube_state[ftoi[X_face], 2, 1]
    Y_face = cube_state[ftoi[Y_face], 2, 1]

    if X_id == X_face and Y_id == Y_face and curr_id == face:
        return 1
        
    else:
        return 0

def reorient_yellow_corners():
    global tot_turns
    global reorient_turns
    tot_turns = 0
        # Check that cube is not already solved
        # Store base_face
        # orient the cube so it's in the front-top-right
        # Execute R' D' R D 2 times, until it's correctly oriented
    
    # while yellow corners are not all correctly oriented
        
        # find another incorrectly oriented corner
        # rotate top face so that piece is in the front-top-right
        # Execute R' D' R D 2 times, until it's correctly oriented
        
    
    score_sum = 0
    for corner_location in ['above-left', 'above-right', 'below-left', 'below-right']:
        
        score = score_corner_orientation('Y', corner_location.split('-'))
        score_sum += score
        
        if score == 0:
            target_location = corner_location
            
    if score_sum != 4:
        
        if target_location == 'above-left':
            base_face = relations['Y']['above']

        elif target_location == 'above-right':
            base_face = relations['Y']['right']

        elif target_location == 'below-left':
            base_face = relations['Y']['left']

        else:
            base_face = relations['Y']['below']
        
        for count in range(0,2):
            
            if score_corner_orientation(base_face, ['below', 'left']) == 1:
                pass
            
            else:
               # R' D' R D
                turn(relations[base_face]['left'], 'ccw')
                turn(relations[base_face]['above'], 'cw')
                turn(relations[base_face]['left'], 'cw')
                turn(relations[base_face]['above'], 'ccw')
                
                # R' D' R D
                turn(relations[base_face]['left'], 'ccw')
                turn(relations[base_face]['above'], 'cw')
                turn(relations[base_face]['left'], 'cw')
                turn(relations[base_face]['above'], 'ccw') 
        
        score_sum = 0
        for corner_location in ['above-left', 'above-right', 'below-left', 'below-right']:
            
            score = score_corner_orientation('Y', corner_location.split('-'))
            score_sum += score
            
            if score == 0:
                target_location = corner_location
                
        if score_sum != 4:
            
            if target_location == 'above-left':
                new_face = relations['Y']['above']
    
            elif target_location == 'above-right':
                new_face = relations['Y']['right']
    
            elif target_location == 'below-left':
                new_face = relations['Y']['left']
    
            else:
                new_face = relations['Y']['below']
       
        while score_sum != 4:
            if new_face == base_face:
                num_turns = 0
            
            elif new_face == relations[base_face]['left']:
                num_turns = 1
                
            elif new_face == relations[base_face]['opposite']:
                num_turns = 2
                
            else:
                num_turns = 3
            
            for turns in range(0, num_turns):
                turn('Y', 'cw')
            
            for count in range(0,2):
                
                if score_corner_orientation(base_face, ['below', 'left']) == 1:
                    pass
                
                else:
                   # R' D' R D
                    turn(relations[base_face]['left'], 'ccw')
                    turn(relations[base_face]['above'], 'cw')
                    turn(relations[base_face]['left'], 'cw')
                    turn(relations[base_face]['above'], 'ccw')
                    
                    # R' D' R D
                    turn(relations[base_face]['left'], 'ccw')
                    turn(relations[base_face]['above'], 'cw')
                    turn(relations[base_face]['left'], 'cw')
                    turn(relations[base_face]['above'], 'ccw')        
            
            score_sum = 0
            for corner_location in ['above-left', 'above-right', 'below-left', 'below-right']:
                
                score = score_corner_orientation('Y', corner_location.split('-'))
                score_sum += score
                
                if score == 0:
                    target_location = corner_location
                    
            if score_sum != 4:
                
                if target_location == 'above-left':
                    new_face = relations['Y']['above']
        
                elif target_location == 'above-right':
                    new_face = relations['Y']['right']
        
                elif target_location == 'below-left':
                    new_face = relations['Y']['left']
        
                else:
                    new_face = relations['Y']['below']
    
        face = 'R'
        curr_color = cube_state[ftoi[face], 2, 1]
        
        if curr_color == face:
            num_turns = 0
            
        elif curr_color == relations[face]['left']:
            num_turns = 1
            
        elif curr_color == relations[face]['opposite']:
            num_turns = 2
            
        else:
            num_turns = 3
        
        for turns in range(0, num_turns):
            turn('Y', 'ccw')
    
    print("REORIENTCORNERS Turns = " + str(tot_turns))
    reorient_turns = tot_turns
        
def solve():
    white_cross()
    white_corners()
    second_layer()
    yellow_cross()
    yellow_edges()
    position_yellow_corners()
    reorient_yellow_corners()
    
def get_tile(row, col):
    
    valid_colors = ['R','O','G','B','W','Y','X']
    color = " "
    while color not in valid_colors:
        color = input("row %d | col %d \n" % (row,col))
        
    return color
    
def cube_manual_input():
    print("CUBE INPUT BEGINNING")
    
    labels = ["R E D", "G R E E N", "B L U E", "O R A N G E", "W H I T E", "Y E L L O W"]
    
    for face in range(0,len(labels)):
        print(labels[face])
        
        for row in range(0, 3):
            for col in range(0,3):
                
                color = get_tile(row, col)
                
                if(color == 'X'):
                    return 0
                #print("row %d | col %d" % (row,col))
                cube_state[face, row, col] = color
            
        print(cube_state[face])
        
def efficiency_eval(num_runs):
    
    whitecross = np.zeros([num_runs,1])
    secondlay = np.zeros([num_runs,1])
    yellowcross = np.zeros([num_runs,1])
    yellowedges = np.zeros([num_runs,1])
    position = np.zeros([num_runs,1])
    reorient = np.zeros([num_runs,1])
    
    for i in range(0,num_runs):
        randomize(50)
        solve() 
        whitecross[i] = wcross_turns
        secondlay[i] = second_turns
        yellowcross[i] = ycross_turns
        yellowedges[i] = yedge_turns
        position[i] = posit_turns
        reorient[i] = reorient_turns
                
    print(whitecross.mean())
    print(secondlay.mean())
    print(yellowcross.mean())
    print(yellowedges.mean())
    print(position.mean())
    print(reorient.mean())
    means = []
    means.append(whitecross.mean())
    means.append(secondlay.mean())
    means.append(yellowcross.mean())
    means.append(yellowedges.mean())
    means.append(position.mean())
    means.append(reorient.mean())
    means = np.array(means)
    print(means.sum())
    
    
#cube_manual_input()
randomize(30)               
#print(cube_state)
#solve()
#print(cube_state)   
#print("-------------------")
#print("TOTAL Moves = " + str(len(moves)))
efficiency_eval(30)