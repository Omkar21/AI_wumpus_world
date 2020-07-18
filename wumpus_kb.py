
# wumpus_kb.py
# ------------
# Licensing Information:
# Please DO NOT DISTRIBUTE OR PUBLISH solutions to this project.
# You are free to use and extend these projects for EDUCATIONAL PURPOSES ONLY.
# The Hunt The Wumpus AI project was developed at University of Arizona
# by Clay Morrison (clayton@sista.arizona.edu), spring 2013.
# This project extends the python code provided by Peter Norvig as part of
# the Artificial Intelligence: A Modern Approach (AIMA) book example code;
# see http://aima.cs.berkeley.edu/code.html
# In particular, the following files come directly from the AIMA python
# code: ['agents.py', 'logic.py', 'search.py', 'utils.py']
# ('logic.py' has been modified by Clay Morrison in locations with the
# comment 'CTM')
# The file ['minisat.py'] implements a slim system call wrapper to the minisat
# (see http://minisat.se) SAT solver, and is directly based on the satispy
# python project, see https://github.com/netom/satispy .

import utils

# -------------------------------------------------------------------------------
# Wumpus Propositions
# -------------------------------------------------------------------------------

### atemporal variables

proposition_bases_atemporal_location = ['P', 'W', 'S', 'B']


def pit_str(x, y):
    "There is a Pit at <x>,<y>"
    return 'P{0}_{1}'.format(x, y)


def wumpus_str(x, y):
    "There is a Wumpus at <x>,<y>"
    return 'W{0}_{1}'.format(x, y)


def stench_str(x, y):
    "There is a Stench at <x>,<y>"
    return 'S{0}_{1}'.format(x, y)


def breeze_str(x, y):
    "There is a Breeze at <x>,<y>"
    return 'B{0}_{1}'.format(x, y)


### fluents (every proposition who's truth depends on time)

proposition_bases_perceptual_fluents = ['Stench', 'Breeze', 'Glitter', 'Bump', 'Scream']


def percept_stench_str(t):
    "A Stench is perceived at time <t>"
    return 'Stench{0}'.format(t)


def percept_breeze_str(t):
    "A Breeze is perceived at time <t>"
    return 'Breeze{0}'.format(t)


def percept_glitter_str(t):
    "A Glitter is perceived at time <t>"
    return 'Glitter{0}'.format(t)


def percept_bump_str(t):
    "A Bump is perceived at time <t>"
    return 'Bump{0}'.format(t)


def percept_scream_str(t):
    "A Scream is perceived at time <t>"
    return 'Scream{0}'.format(t)


proposition_bases_location_fluents = ['OK', 'L']


def state_OK_str(x, y, t):
    "Location <x>,<y> is OK at time <t>"
    return 'OK{0}_{1}_{2}'.format(x, y, t)


def state_loc_str(x, y, t):
    "At Location <x>,<y> at time <t>"
    return 'L{0}_{1}_{2}'.format(x, y, t)


def loc_proposition_to_tuple(loc_prop):
    """
    Utility to convert location propositions to location (x,y) tuples
    Used by HybridWumpusAgent for internal bookkeeping.
    """
    parts = loc_prop.split('_')
    return (int(parts[0][1:]), int(parts[1]))


proposition_bases_state_fluents = ['HeadingNorth', 'HeadingEast',
                                   'HeadingSouth', 'HeadingWest',
                                   'HaveArrow', 'WumpusAlive']


def state_heading_north_str(t):
    "Heading North at time <t>"
    return 'HeadingNorth{0}'.format(t)


def state_heading_east_str(t):
    "Heading East at time <t>"
    return 'HeadingEast{0}'.format(t)


def state_heading_south_str(t):
    "Heading South at time <t>"
    return 'HeadingSouth{0}'.format(t)


def state_heading_west_str(t):
    "Heading West at time <t>"
    return 'HeadingWest{0}'.format(t)


def state_have_arrow_str(t):
    "Have Arrow at time <t>"
    return 'HaveArrow{0}'.format(t)


def state_wumpus_alive_str(t):
    "Wumpus is Alive at time <t>"
    return 'WumpusAlive{0}'.format(t)


proposition_bases_actions = ['Forward', 'Grab', 'Shoot', 'Climb',
                             'TurnLeft', 'TurnRight', 'Wait']


def action_forward_str(t=None):
    "Action Forward executed at time <t>"
    return ('Forward{0}'.format(t) if t != None else 'Forward')


def action_grab_str(t=None):
    "Action Grab executed at time <t>"
    return ('Grab{0}'.format(t) if t != None else 'Grab')


def action_shoot_str(t=None):
    "Action Shoot executed at time <t>"
    return ('Shoot{0}'.format(t) if t != None else 'Shoot')


def action_climb_str(t=None):
    "Action Climb executed at time <t>"
    return ('Climb{0}'.format(t) if t != None else 'Climb')


def action_turn_left_str(t=None):
    "Action Turn Left executed at time <t>"
    return ('TurnLeft{0}'.format(t) if t != None else 'TurnLeft')


def action_turn_right_str(t=None):
    "Action Turn Right executed at time <t>"
    return ('TurnRight{0}'.format(t) if t != None else 'TurnRight')


def action_wait_str(t=None):
    "Action Wait executed at time <t>"
    return ('Wait{0}'.format(t) if t != None else 'Wait')


def add_time_stamp(prop, t): return '{0}{1}'.format(prop, t)


proposition_bases_all = [proposition_bases_atemporal_location,
                         proposition_bases_perceptual_fluents,
                         proposition_bases_location_fluents,
                         proposition_bases_state_fluents,
                         proposition_bases_actions]


# -------------------------------------------------------------------------------
# Axiom Generator: Current Percept Sentence
# -------------------------------------------------------------------------------

# def make_percept_sentence(t, tvec):

#new method to check the location bounderies

def agent_position_boundery_check(horizontal_counterpart, verticle_counterpart, world_min_pos_x, world_max_pos_x, world_min_pos_y, world_max_pos_y):

    # We need following propositional notations:
    sign_Negation = '~'
    sign_conjunction = '&'
    sign_bidirection = '<=>'
    sign_disjunction = '|'

    prepo_string = ''

    pre_more_equel = '>='

    post_more_equel = '<='

    ''' horizontal_counterpart, 
       verticle_counterpart, 
       world_min_pos_x,
       world_max_pos_x, world_min_pos_y, world_max_pos_y'''

    #write x and x min relation

    verticle_cur_min = verticle_counterpart >= world_min_pos_y

    verticle_cur_max = verticle_counterpart <= world_max_pos_y

    hozinontal_cur_min = horizontal_counterpart >= world_min_pos_x

    horizontal_cur_max = horizontal_counterpart <= world_max_pos_x


    #creating the preposition string here
    prepo_string = hozinontal_cur_min and horizontal_cur_max and verticle_cur_min and verticle_cur_max

    #returning the final pre position string
    return prepo_string

#mehod ends here


def axiom_generator_percept_sentence(t, tvec):
    """
    Asserts that each percept proposition is True or False at time t.
    t := time
    tvec := a boolean (True/False) vector with entries corresponding to
            percept propositions, in this order:
                (<stench>,<breeze>,<glitter>,<bump>,<scream>)
    Example:
        Input:  [False, True, False, False, True]
        Output: '~Stench0 & Breeze0 & ~Glitter0 & ~Bump0 & Scream0'
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # We have to write the prepositional sentense here
    # create an array
    sign_negation = '~'
    sign_conjunction = '&'
    agent_action_array = []

    #create the time string
    string_t = str(t)

    for count_val, boolean_out in enumerate(tvec):
        final_prepo_string = ""

        if not boolean_out:

            #adding negation
            final_prepo_string = final_prepo_string + sign_negation

        final_prepo_string = final_prepo_string+ proposition_bases_perceptual_fluents[count_val] + string_t
        agent_action_array.append(final_prepo_string)

    #the final axiom string
    axiom_str = axiom_str + sign_conjunction.join(agent_action_array)

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str


# -------------------------------------------------------------------------------
# Axiom Generators: Initial Axioms
# -------------------------------------------------------------------------------


#changes made by omkar s kulkarni
def axiom_generator_initial_location_assertions(x, y):
    """
    Assert that there is no Pit and no Wumpus in the location
    x,y := the location
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Comment or delete the next line once this function has been implemented.
    sign_negation = '~'
    sign_conjunction = '&'

    #create the preposition string here
    prepo_string = ''

    #assigning inputs
    horizontal_counterpart = x
    vertical_counterpart = y

    # preposition with no pit and no wumpus
    prepo_string = prepo_string + sign_negation + wumpus_str(horizontal_counterpart, vertical_counterpart) + sign_conjunction + sign_negation + pit_str(horizontal_counterpart, vertical_counterpart)

    #assign the prepo string output to return statment

    axiom_str = axiom_str + prepo_string
    # commenting
    # utils.print_not_implemented()
    #returning the final output
    return axiom_str

#changes made by omkar
#adding method to check three consecutive locations --axiom_generator_pits_and_breezes
def find_adjecent_to_location(horizontal_counterpart, vertical_counterpart):

    left_location = (horizontal_counterpart - 1, vertical_counterpart)

    right_location = (horizontal_counterpart + 1, vertical_counterpart)

    current_location =  (horizontal_counterpart, vertical_counterpart)

    down_location = (horizontal_counterpart, vertical_counterpart - 1)

    up_location = (horizontal_counterpart, vertical_counterpart + 1)


    #append all location in array
    nerer_location = [left_location, right_location, current_location, down_location, up_location ]

    return nerer_location



#Changes ends here --axiom_generator_pits_and_breezes


def axiom_generator_pits_and_breezes(x, y, xmin, xmax, ymin, ymax):
    """
    Assert that Breezes (atemporal) are only found in locations where
    there are one or more Pits in a neighboring location (or the same location!)
    x,y := the location
    xmin, xmax, ymin, ymax := the bounds of the environment; you use these
           variables to 'prune' any neighboring locations that are outside
           of the environment (and therefore are walls, so can't have Pits).
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Create one list for probable pit locations
    probable_pit_blocks = []
    # We need following propositional notations:
    sign_Negation = '~'
    sign_conjunction = '&'
    sign_bidirection = '<=>'
    sign_disjunction = '|'

    left_bracket = '('
    right_bracket = ')'

    #assign given location x and given location y
    given_location_x = x
    given_location_y = y

    #create preposition string to asign
    prepo_string = ''

    prepo_string = prepo_string + breeze_str(given_location_x, given_location_y) + sign_bidirection

    prepo_string = prepo_string + left_bracket

    # Looping over wumpus world
    for (current_x_loc, current_y_loc) in find_adjecent_to_location(given_location_x, given_location_y):

        # cheking possibility of available location

        if agent_position_boundery_check(current_x_loc, current_y_loc, xmin, xmax, ymin, ymax):
            # appending pit in already created list
            probable_pit_blocks.append(pit_str(current_x_loc, current_y_loc))

    prepo_string = prepo_string + sign_disjunction.join(probable_pit_blocks)

    # end the preposition_string
    prepo_string = prepo_string + right_bracket

    #Appending axiom string with preposition
    axiom_str = axiom_str + prepo_string

    return axiom_str


##################################################################################################

def generate_pit_and_breeze_axioms(xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_pits_and_breezes(x, y, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_pits_and_breezes')
    return axioms


def axiom_generator_wumpus_and_stench(x, y, xmin, xmax, ymin, ymax):
    """
    Assert that Stenches (atemporal) are only found in locations where
    there are one or more Wumpi in a neighboring location (or the same location!)
    (Don't try to assert here that there is only one Wumpus;
    we'll handle that separately)
    x,y := the location
    xmin, xmax, ymin, ymax := the bounds of the environment; you use these
           variables to 'prune' any neighboring locations that are outside
           of the environment (and therefore are walls, so can't have Wumpi).
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Create one list for probable pit locations
    probable_stench_blocks = []
    sign_Negation = '~'
    sign_conjunction = '&'
    sign_bidirection = '<=>'
    sign_disjunction = '|'

    left_bracket = '('
    right_bracket = ')'

    #assigning the current location values
    current_location_x_given = x
    current_location_y_given = y

    #creating the preposition string
    prepo_string = ''

    prepo_string = prepo_string + stench_str(current_location_x_given, current_location_y_given) + sign_bidirection

    #Appending bracket
    prepo_string = prepo_string + left_bracket

    # Looping over wumpus world
    for (current_x_loc, current_y_loc) in find_adjecent_to_location(current_location_x_given, current_location_y_given):
        # cheking possibility of available location
        if agent_position_boundery_check(current_x_loc, current_y_loc, xmin, xmax, ymin, ymax):
            # appending pit in already created list
            probable_stench_blocks.append(wumpus_str(current_x_loc, current_y_loc))

    #appending the probable locations of stench blocks
    prepo_string = prepo_string + sign_disjunction.join(probable_stench_blocks)

    # end the preposition_string
    prepo_string = prepo_string + right_bracket

    #assigning preposition statment to return statment
    axiom_str = axiom_str + prepo_string

    #returning final string
    #print('axiom_generator_wumpus_and_stench' + axiom_str)
    return axiom_str


def generate_wumpus_and_stench_axioms(xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_wumpus_and_stench(x, y, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_wumpus_and_stench')
    return axioms


def axiom_generator_at_least_one_wumpus(xmin, xmax, ymin, ymax):
    """
    Assert that there is at least one Wumpus.
    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Create one list for probable pit locations
    probable_wumpus_blocks = []
    # write the required prepositional statments
    sign_disjunction = '|'

    # assign min value to local variable
    map_minimum_x = xmin
    map_minimum_y = ymin
    map_maximum_x = xmax
    map_maximum_y = ymax

    max_x_length = map_maximum_x + 1
    max_Y_length = map_maximum_y + 1

    # create preposition string first
    prepo_string = ''



    # Iterate over all the wumpus world block

    # firstly iterate over x co-ordinates
    for horizontal_counterpart in range(map_minimum_x, max_x_length):

        # iterate over Y co ordinate
        for vertical_counterpart in range(map_minimum_y, max_Y_length):
            # Append the wumpus in predefined wumpus block list

            probable_wumpus_blocks.append(wumpus_str(horizontal_counterpart, vertical_counterpart))

    #appending wumpus blocks to string
    prepo_string = prepo_string + sign_disjunction.join(probable_wumpus_blocks)


    #appending final string to
    axiom_str =axiom_str + prepo_string
    # print('axiom_generator_at_least_one_wumpus'+prepo_string)

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    #print('axiom_generator_at_least_one_wumpus' + axiom_str )
    return axiom_str


def axiom_generator_at_most_one_wumpus(xmin, xmax, ymin, ymax):
    """
    Assert that there is at at most one Wumpus.
    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    #write all the prepositions signs which we required
    sign_negation = '~'
    sign_disjunction = '|'
    sign_conjunction = '&'
    left_bracket = '('
    right_bracket = ')'

    # assign min value to local variable
    map_minimum_x = xmin
    map_minimum_y = ymin
    map_maximum_x = xmax
    map_maximum_y = ymax

    max_x_length = map_maximum_x + 1
    max_Y_length = map_maximum_y + 1

    probable_wumpus_location = []


    #create one preposition string
    prepo_string = ''

    # Iterate over all the wumpus world block
    # firstly iterate over x co-ordinates
    for horizontal_counterpart in range(map_minimum_x, max_x_length):
        # iterate over Y co ordinate
        for vertical_counterpart in range(map_minimum_y, max_Y_length):
            option = ''
            option = sign_negation + wumpus_str(horizontal_counterpart, vertical_counterpart)

            # creating array which store all non wumpus locations
            notWumpusArray = []

            # Iterate over all the wumpus world block
            # firstly iterate over x co-ordinates
            for current_pose_x in range(map_minimum_x, max_x_length):

                # iterate over Y co ordinate
                for current_pose_y in range(map_minimum_y, max_Y_length):

                    #comparing x co-ordinates
                    if current_pose_y == vertical_counterpart and current_pose_x == horizontal_counterpart:

                        #skip this position all other position should be added in no wumpus array
                        pass



                    else:
                        # add the values in wumpus world
                        notWumpusArray.append(
                            left_bracket + option + sign_disjunction + sign_negation + wumpus_str(current_pose_x,
                                                                                                  current_pose_y) + right_bracket)



            #append all the locations by conjunction  with join function
            probable_wumpus_location.append(left_bracket + sign_conjunction.join(notWumpusArray) + right_bracket)

    #append the values to preposition statments
    prepo_string = prepo_string + sign_conjunction.join(set(probable_wumpus_location))

    prepo_string = left_bracket + prepo_string

    prepo_string = prepo_string+ right_bracket

    #Assigning value to return type
    axiom_str = axiom_str + prepo_string

    #check
    #print('axiom_generator_at_most_one_wumpus'+axiom_str)
    #returning final axiom string
    return axiom_str

#########################################################################################2

def axiom_generator_only_in_one_location(xi, yi, xmin, xmax, ymin, ymax, t=0):
    """
    Assert that the Agent can only be in one (the current xi,yi) location at time t.
    xi,yi := the current location.
    xmin, xmax, ymin, ymax := the bounds of the environment.
    t := time; default=0
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Firstly write the required prepositions

    sign_negation = '~'
    sign_disjunction = '|'
    sign_conjunction = '&'

    # write string for preposition statment
    prepo_string = ''

    # assign min value to local variable

    map_minimum_x = xmin
    map_minimum_y = ymin
    map_maximum_x = xmax
    map_maximum_y = ymax

    time_state = t

    one_location_x = xi
    one_location_y = yi

    # write the maximizing limits

    max_x_length = map_maximum_x + 1
    max_Y_length = map_maximum_y + 1

    # create array to store location condition for agent
    agent_postions_status = []

    # iterate over all wumpus locations
    # iterate over x coordinates
    for horizontal_counterpart in range(map_minimum_x, max_x_length):

        # iterate over Y co ordinate
        for vertical_counterpart in range(map_minimum_y, max_Y_length):

            # Compare the x and y co ordinates
            if vertical_counterpart == one_location_y and horizontal_counterpart == one_location_x :

                # append the location
                agent_postions_status.append(state_loc_str(horizontal_counterpart, vertical_counterpart, time_state))

            else:
                # add all not in positions
                agent_postions_status.append(
                    sign_negation + state_loc_str(horizontal_counterpart, vertical_counterpart, time_state))

    # Append the values with conjunction
    prepo_string = prepo_string + sign_conjunction.join(agent_postions_status)

    # put the following preposition statement to output value
    axiom_str = axiom_str + prepo_string

    # Comment or delete the next line once this function has been implemented.
    # commenting as per mentioned
    # utils.print_not_implemented()
    #returning the axiom string as output
    return axiom_str

##############################################--continue

def fetch_direction_array (dir):
    if dir == 'Directions':
        return ['East', 'West', 'North', 'South']
    else:
        return ['EAST', 'WEST', 'NORTH', 'SOUTH']



def axiom_generator_only_one_heading(heading='north', t=0):
    """
    Assert that Agent can only head in one direction at a time.
    heading := string indicating heading; default='north';
               will be one of: 'north', 'east', 'south', 'west'
    t := time; default=0
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # firstly mention the required prepositions
    sign_negation = '~'
    sign_disjunction = '|'
    sign_conjunction = '&'

    # create the agents final heading direction
    agent_dir_bool = []

    # initiate the pre position string
    prepo_string = ''

    # create the list of direction
    agent_pointing_directions = fetch_direction_array('Directions')

    # Looping over the directions
    for dir in agent_pointing_directions:

        direction = dir.upper()

        input_dir = heading.upper()

        time_string = str(t)

        if (direction == input_dir):
            agent_dir_bool.append('Heading' + dir + time_string)
        else:
            agent_dir_bool.append(sign_negation + 'Heading' + dir + time_string)

    # append the condition with and preposition
    prepo_string = prepo_string + sign_conjunction.join(agent_dir_bool)

    # assign to return statment
    axiom_str = axiom_str + prepo_string

    # Comment or delete the next line once this function has been implemented.
    # commenting as per mentioned on instruction
    # utils.print_not_implemented()
    #to check output here
    #print('axiom_generator_only_one_heading'+axiom_str)
    return axiom_str


def axiom_generator_have_arrow_and_wumpus_alive(t=0):
    """
    Assert that Agent has the arrow and the Wumpus is alive at time t.
    t := time; default=0
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # firstly mention the required prepositions
    sign_negation = '~'
    sign_disjunction = '|'
    sign_conjunction = '&'

    #assign time state value
    time_state = t

    # create one preposition string
    prep_string = ''

    prep_string = prep_string + state_wumpus_alive_str(time_state) + sign_conjunction

    prep_string = prep_string + state_have_arrow_str(time_state)

    # assign it to output
    axiom_str = axiom_str + prep_string

    # Comment or delete the next line once this function has been implemented.
    # Commented as per instructions
    # utils.print_not_implemented()

    #check putput by printing
    #print('axiom_generator_have_arrow_and_wumpus_alive'+ axiom_str)
    return axiom_str
############################################################################################################3



def initial_wumpus_axioms(xi, yi, width, height, heading='east'):
    """
    Generate all of the initial wumpus axioms

    xi,yi = initial location
    width,height = dimensions of world
    heading = str representation of the initial agent heading
    """
    axioms = [axiom_generator_initial_location_assertions(xi, yi)]
    axioms.extend(generate_pit_and_breeze_axioms(1, width, 1, height))
    axioms.extend(generate_wumpus_and_stench_axioms(1, width, 1, height))

    axioms.append(axiom_generator_at_least_one_wumpus(1, width, 1, height))
    axioms.append(axiom_generator_at_most_one_wumpus(1, width, 1, height))

    axioms.append(axiom_generator_only_in_one_location(xi, yi, 1, width, 1, height))
    axioms.append(axiom_generator_only_one_heading(heading))

    axioms.append(axiom_generator_have_arrow_and_wumpus_alive())

    return axioms


# -------------------------------------------------------------------------------
# Axiom Generators: Temporal Axioms (added at each time step)
# -------------------------------------------------------------------------------

def axiom_generator_location_OK(x, y, t):
    """
    Assert the conditions under which a location is safe for the Agent.
    (Hint: Are Wumpi always dangerous?)
    x,y := location
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # firstly mention the required prepositions
    sign_negation = '~'
    sign_disjunction = '|'
    sign_conjunction = '&'
    sign_bicondition = '<=>'

    left_bracket = '('
    right_bracket = ')'

    #create variables to store the imputs
    horizontal_axis = x
    vertical_axis = y
    time_state = t



    # create one preposition string
    prep_string = ''

    prep_string = prep_string + state_OK_str(horizontal_axis, vertical_axis, time_state) + sign_bicondition

    prep_string = prep_string + left_bracket

    prep_string = prep_string + sign_negation + pit_str(horizontal_axis, vertical_axis) + sign_conjunction

    prep_string = prep_string + left_bracket

    prep_string = prep_string + sign_negation + wumpus_str(horizontal_axis, vertical_axis) + sign_disjunction

    prep_string = prep_string + left_bracket

    prep_string = prep_string + wumpus_str(horizontal_axis, vertical_axis) + sign_conjunction

    prep_string = prep_string + sign_negation + state_wumpus_alive_str(time_state)

    prep_string = prep_string + right_bracket

    prep_string = prep_string + right_bracket + right_bracket

    # push the preposition to output statment

    axiom_str = axiom_str + prep_string

    #check statment by printing
    #print(axiom_str)

    #Returning the final output preposition statment
    return axiom_str

def generate_square_OK_axioms(t, xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_location_OK(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_location_OK')
    return filter(lambda s: s != '', axioms)


# -------------------------------------------------------------------------------
# Connection between breeze / stench percepts and atemporal location properties

def axiom_generator_breeze_percept_and_location_property(x, y, t):
    """
    Assert that when in a location at time t, then perceiving a breeze
    at that time (a percept) means that the location is breezy (atemporal)
    x,y := location
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # firstly mention the required prepositions
    sign_negation = '~'
    sign_disjunction = '|'
    sign_conjunction = '&'
    sign_bicondition = '<=>'
    sign_implication = '>>'

    # create one preposition string
    prep_string = ''

    left_bracket = '('
    right_bracket = ')'

    # create variables to store the imputs
    horizontal_axis = x
    vertical_axis = y
    time_state = t

    prep_string = prep_string + left_bracket

    prep_string = prep_string + state_loc_str(horizontal_axis, vertical_axis, time_state)

    prep_string = prep_string + right_bracket

    prep_string = prep_string + sign_implication + left_bracket + percept_breeze_str(time_state) + sign_bicondition

    prep_string = prep_string + breeze_str(horizontal_axis, vertical_axis)

    prep_string = prep_string + right_bracket

    # put prep statment as return statment
    axiom_str = axiom_str +prep_string

    #print and check the output
    #print('axiom_generator_breeze_percept_and_location_property' + axiom_str)

    #returning the final output as a required preposition statment
    return axiom_str

#######################----------------------------------------------------


def generate_breeze_percept_and_location_axioms(t, xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_breeze_percept_and_location_property(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_breeze_percept_and_location_property')
    return filter(lambda s: s != '', axioms)


def axiom_generator_stench_percept_and_location_property(x, y, t):
    """
    Assert that when in a location at time t, then perceiving a stench
    at that time (a percept) means that the location has a stench (atemporal)
    x,y := location
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # firstly mention the required prepositions
    sign_negation = '~'
    sign_disjunction = '|'
    sign_conjunction = '&'
    sign_bicondition = '<=>'
    sign_implication = '>>'

    # create one preposition string
    prep_string = ''

    left_bracket = '('
    right_bracket = ')'

    # create variables to store the imputs
    horizontal_axis = x
    vertical_axis = y
    time_state = t

    prep_string = prep_string + left_bracket + state_loc_str(horizontal_axis, vertical_axis, time_state)


    prep_string = prep_string + right_bracket


    prep_string = prep_string + sign_implication + left_bracket + percept_stench_str(time_state)


    prep_string = prep_string + sign_bicondition + stench_str(horizontal_axis, vertical_axis)

    prep_string = prep_string + right_bracket

    # Assign the prepositional statment to output string
    axiom_str = axiom_str + prep_string

    #check preposition statment by printing
    #print(axiom_str)

    #return the preposition statment as output
    return axiom_str
#########################################################################################################4

def generate_stench_percept_and_location_axioms(t, xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_stench_percept_and_location_property(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_stench_percept_and_location_property')
    return filter(lambda s: s != '', axioms)


# -------------------------------------------------------------------------------
# Transition model: Successor-State Axioms (SSA's)
# Avoid the frame problem(s): don't write axioms about actions, write axioms about
# fluents!  That is, write successor-state axioms as opposed to effect and frame
# axioms
#
# The general successor-state axioms pattern (where F is a fluent):
#   F^{t+1} <=> (Action(s)ThatCause_F^t) | (F^t & ~Action(s)ThatCauseNot_F^t)

# NOTE: this is very expensive in terms of generating many (~170 per axiom) CNF clauses!
def axiom_generator_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax):
    """
    Assert the condidtions at time t under which the agent is in
    a particular location (state_loc_str: L) at time t+1, following
    the successor-state axiom pattern.

    x,y := location
    t := time
    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # firstly mention the required prepositions
    sign_negation = '~'
    sign_disjunction = '|'
    sign_conjunction = '&'
    sign_bicondition = '<=>'
    sign_implication = '>>'

    # Agents location
    agent_cureent_loc = []
    # Take time in one variable
    time_lapse = t

    left_bracket = '('
    right_bracket = ')'

    # create variables to store the imputs
    horizontal_axis = x
    vertical_axis = y

    # create one preposition string
    prep_string = ''

    map_minimum_x = xmin
    map_minimum_y = ymin
    map_maximum_x = xmax
    map_maximum_y = ymax

    #creating the preposition statment here
    prep_string = prep_string + state_loc_str(horizontal_axis, vertical_axis, time_lapse + 1)

    prep_string = prep_string + sign_bicondition + left_bracket + left_bracket


    #checking left bounderry
    if agent_position_boundery_check(horizontal_axis - 1, vertical_axis, map_minimum_x, map_maximum_x, map_minimum_y, map_maximum_y):

        #append the value in array
        agent_cureent_loc.append(state_loc_str(horizontal_axis - 1, vertical_axis, time_lapse))

    #cheking the up value
    if agent_position_boundery_check(horizontal_axis, vertical_axis + 1, map_minimum_x, map_maximum_x, map_minimum_y, map_maximum_y):

        #append the value in array
        agent_cureent_loc.append(state_loc_str(horizontal_axis, vertical_axis + 1, time_lapse))

    #cheking the right value
    if agent_position_boundery_check(horizontal_axis + 1, vertical_axis, map_minimum_x, map_maximum_x, map_minimum_y, map_maximum_y):

        #append the right value in array
        agent_cureent_loc.append(state_loc_str(horizontal_axis + 1, vertical_axis, time_lapse))

    #checking the down value
    if agent_position_boundery_check(horizontal_axis, vertical_axis - 1, map_minimum_x, map_maximum_x, map_minimum_y, map_maximum_y):

        #appending the down value
        agent_cureent_loc.append(state_loc_str(horizontal_axis, vertical_axis - 1, time_lapse))

    prep_string = prep_string + left_bracket + sign_disjunction.join(agent_cureent_loc)

    prep_string = prep_string + right_bracket + sign_conjunction + action_forward_str(time_lapse)

    prep_string = prep_string + right_bracket + sign_disjunction

    prep_string = prep_string + left_bracket + state_loc_str(horizontal_axis, vertical_axis, time_lapse)

    prep_string = prep_string + sign_conjunction + sign_negation + action_forward_str(time_lapse)

    prep_string = prep_string + right_bracket + right_bracket

    # Assign prepositional statment as axiom statment

    axiom_str = axiom_str + prep_string


    # returning the prepositional output
    return axiom_str


def generate_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax, heading):
    """
    The full at_location SSA converts to a fairly large CNF, which in
    turn causes the KB to grow very fast, slowing overall inference.
    We therefore need to restric generating these axioms as much as possible.
    This fn generates the at_location SSA only for the current location and
    the location the agent is currently facing (in case the agent moves
    forward on the next turn).
    This is sufficient for tracking the current location, which will be the
    single L location that evaluates to True; however, the other locations
    may be False or Unknown.
    """
    axioms = [axiom_generator_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax)]
    if heading == 'west' and x - 1 >= xmin:
        axioms.append(axiom_generator_at_location_ssa(t, x - 1, y, xmin, xmax, ymin, ymax))
    if heading == 'east' and x + 1 <= xmax:
        axioms.append(axiom_generator_at_location_ssa(t, x + 1, y, xmin, xmax, ymin, ymax))
    if heading == 'south' and y - 1 >= ymin:
        axioms.append(axiom_generator_at_location_ssa(t, x, y - 1, xmin, xmax, ymin, ymax))
    if heading == 'north' and y + 1 <= ymax:
        axioms.append(axiom_generator_at_location_ssa(t, x, y + 1, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_at_location_ssa')
    return filter(lambda s: s != '', axioms)


# ----------------------------------
##################################################################11
def axiom_generator_have_arrow_ssa(t):
    """
    Assert the conditions at time t under which the Agent
    has the arrow at time t+1
    t := time
    """
    # firstly mention the required prepositions

    axiom_str = ''

    sign_negation = '~'
    sign_disjunction = '|'
    sign_conjunction = '&'
    sign_bicondition = '<=>'
    sign_implication = '>>'

    left_bracket = '('
    right_bracket = ')'

    # create one preposition string
    prep_string = ''

    # craete time lapse variable
    time_lapse = t
    time_lapse_one = time_lapse + 1

    prep_string = prep_string + state_have_arrow_str(time_lapse_one) + sign_bicondition

    prep_string = prep_string + left_bracket + sign_negation + action_shoot_str(time_lapse)

    prep_string = prep_string + sign_conjunction + state_have_arrow_str(time_lapse)

    prep_string= prep_string + right_bracket

    # assign the value to return type
    axiom_str = axiom_str + prep_string

    # Comment or delete the next line once this function has been implemented.
    # commenting as per the instructions
    # utils.print_not_implemented()
    #check by printing whether value is correct or not
    #print ('axiom_generator_have_arrow_ssa' + axiom_str)


    #return the final output
    return axiom_str


def axiom_generator_wumpus_alive_ssa(t):
    """
    Assert the conditions at time t under which the Wumpus
    is known to be alive at time t+1
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    sign_negation = '~'
    sign_disjunction = '|'
    sign_conjunction = '&'
    sign_bicondition = '<=>'
    sign_implication = '>>'

    # create one preposition string
    prep_string = ''

    # craete time lapse variable
    time_lapse = t
    time_lapse_one = time_lapse + 1

    left_bracket = '('
    right_bracket = ')'

    #create the prepared statment

    prep_string = prep_string+ state_wumpus_alive_str(time_lapse+1) + sign_bicondition

    prep_string = prep_string + left_bracket + sign_negation + percept_scream_str(time_lapse_one)

    prep_string = prep_string + sign_conjunction + state_wumpus_alive_str(time_lapse)

    prep_string = prep_string + right_bracket

    #assign value to the return statment
    axiom_str =  axiom_str + prep_string




    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()

    # reurn the final axiom preposition statment
    return axiom_str
####################################################################################################5


# ----------------------------------


def axiom_generator_heading_north_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be North at time t+1
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    sign_negation = '~'
    sign_disjunction = '|'
    sign_conjunction = '&'
    sign_bicondition = '<=>'
    sign_implication = '>>'

    #bracket statments
    left_bracket = '('
    right_bracket = ')'

    # create one preposition string
    prep_string = ''

    # craete time lapse variable
    time_lapse = t
    time_lapse_one = time_lapse + 1

    prep_string = prep_string + state_heading_north_str(time_lapse_one) + sign_bicondition + left_bracket + left_bracket

    prep_string = prep_string + state_heading_north_str(time_lapse) + sign_conjunction + sign_negation

    prep_string = prep_string + action_turn_right_str(time_lapse) + sign_conjunction

    prep_string = prep_string + sign_negation + action_turn_left_str(time_lapse) + right_bracket

    prep_string = prep_string + sign_disjunction + left_bracket

    prep_string = prep_string + state_heading_east_str(time_lapse) + sign_conjunction

    prep_string = prep_string + action_turn_left_str(time_lapse) + right_bracket

    prep_string = prep_string + sign_disjunction + left_bracket

    prep_string = prep_string + state_heading_west_str(time_lapse) + sign_conjunction + action_turn_right_str(time_lapse)

    prep_string = prep_string + right_bracket + right_bracket

    # Add the preposition statment to return statment
    axiom_str = axiom_str + prep_string

    # Comment or delete the next line once this function has been implemented.
    # commenting as per instructed

    #check whethet axiom string is correct or not
    #print('axiom_generator_heading_north_ssa' + axiom_str)

    # utils.print_not_implemented()
    #return the final output
    return axiom_str

def axiom_generator_heading_east_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be East at time t+1
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    sign_negation = '~'
    sign_disjunction = '|'
    sign_conjunction = '&'
    sign_bicondition = '<=>'
    sign_implication = '>>'

    # create one preposition string
    prep_string = ''

    # bracket statments
    left_bracket = '('
    right_bracket = ')'

    # craete time lapse variable
    time_lapse = t
    time_lapse_one = time_lapse + 1

    prep_string = prep_string + state_heading_east_str(time_lapse_one) + sign_bicondition + left_bracket + left_bracket

    prep_string = prep_string + state_heading_east_str(time_lapse) + sign_conjunction + sign_negation

    prep_string = prep_string + action_turn_right_str(time_lapse) + sign_conjunction + sign_negation

    prep_string = prep_string + action_turn_left_str(time_lapse) + right_bracket + sign_disjunction + left_bracket

    prep_string = prep_string + state_heading_south_str(time_lapse) + sign_conjunction + action_turn_left_str(time_lapse)

    prep_string = prep_string + right_bracket + sign_disjunction + left_bracket

    prep_string = prep_string + state_heading_north_str(time_lapse)

    prep_string = prep_string + sign_conjunction + action_turn_right_str(time_lapse) + right_bracket + right_bracket

    # Assign the prepositional statment to axiom string

    axiom_str = axiom_str + prep_string

    # Comment or delete the next line once this function has been implemented.
    # as instructed commented this line
    # utils.print_not_implemented()
    #to check whether string is correct or not
    #print('axiom_generator_heading_east_ssa' + axiom_str)

    #return the final output
    return axiom_str

#############################################################16


def axiom_generator_heading_south_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be South at time t+1
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    sign_negation = '~'
    sign_disjunction = '|'
    sign_conjunction = '&'
    sign_bicondition = '<=>'
    sign_implication = '>>'

    # create one preposition string
    prep_string = ''

    # bracket statments
    left_bracket = '('
    right_bracket = ')'

    # craete time lapse variable
    time_lapse = t
    time_lapse_one = time_lapse + 1

    prep_string =prep_string + state_heading_south_str(time_lapse_one) + sign_bicondition + left_bracket + left_bracket

    prep_string = prep_string + state_heading_south_str(time_lapse) + sign_conjunction + sign_negation

    prep_string = prep_string + action_turn_right_str(time_lapse) + sign_conjunction + sign_negation

    prep_string = prep_string + action_turn_left_str(time_lapse)

    prep_string = prep_string + right_bracket + sign_disjunction + left_bracket

    prep_string = prep_string+ state_heading_west_str(time_lapse) + sign_conjunction + action_turn_left_str(time_lapse)

    prep_string = prep_string + right_bracket + sign_disjunction + left_bracket

    prep_string = prep_string+  state_heading_east_str(time_lapse) + sign_conjunction

    prep_string = prep_string + action_turn_right_str(time_lapse) + right_bracket + right_bracket



    #assign the preposition statment value to axiom
    axiom_str = axiom_str + prep_string

    # Comment or delete the next line once this function has been implemented.
    #commented as per instructed
    #utils.print_not_implemented()

    #check whether output is correct or not
    #print ('axiom_generator_heading_south_ssa'+ axiom_str)

    #reurn the following output
    return axiom_str


def axiom_generator_heading_west_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be West at time t+1
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    sign_negation = '~'
    sign_disjunction = '|'
    sign_conjunction = '&'
    sign_bicondition = '<=>'
    sign_implication = '>>'

    # create one preposition string
    prep_string = ''

    # bracket statments
    left_bracket = '('
    right_bracket = ')'

    # craete time lapse variable
    time_lapse = t
    time_lapse_one = time_lapse + 1

    prep_string = prep_string + state_heading_west_str(time_lapse_one) + sign_bicondition + left_bracket + left_bracket

    prep_string = prep_string + state_heading_west_str(time_lapse) + sign_conjunction + sign_negation

    prep_string = prep_string + action_turn_right_str(time_lapse) + sign_conjunction + sign_negation

    prep_string = prep_string + action_turn_left_str(time_lapse)

    prep_string = prep_string + right_bracket + sign_disjunction + left_bracket

    prep_string = prep_string + state_heading_north_str(time_lapse) + sign_conjunction + action_turn_left_str(time_lapse)

    prep_string = prep_string + right_bracket + sign_disjunction + left_bracket

    prep_string = prep_string + state_heading_south_str(time_lapse) + sign_conjunction

    prep_string = prep_string + action_turn_right_str(time_lapse) + right_bracket + right_bracket

    # Assign preposition statment as return statment
    axiom_str = axiom_str + prep_string

    # Comment or delete the next line once this function has been implemented.
    # Commenting as per instructed
    # utils.print_not_implemented()
    #

    return axiom_str
############################################################################################6

def generate_heading_ssa(t):
    """
    Generates all of the heading SSAs.
    """
    return [axiom_generator_heading_north_ssa(t),
            axiom_generator_heading_east_ssa(t),
            axiom_generator_heading_south_ssa(t),
            axiom_generator_heading_west_ssa(t)]


def generate_non_location_ssa(t):
    """
    Generate all non-location-based SSAs
    """
    axioms = []  # all_state_loc_ssa(t, xmin, xmax, ymin, ymax)
    axioms.append(axiom_generator_have_arrow_ssa(t))
    axioms.append(axiom_generator_wumpus_alive_ssa(t))
    axioms.extend(generate_heading_ssa(t))
    return filter(lambda s: s != '', axioms)


# ----------------------------------

def axiom_generator_heading_only_north(t):
    """
    Assert that when heading is North, the agent is
    not heading any other direction.
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    sign_negation = '~'
    sign_disjunction = '|'
    sign_conjunction = '&'
    sign_bicondition = '<=>'
    sign_implication = '>>'

    # create one preposition string
    prep_string = ''

    # bracket statments
    left_bracket = '('
    right_bracket = ')'

    # craete time lapse variable
    time_lapse = t
    time_lapse_one = time_lapse + 1

    prep_string = prep_string + state_heading_north_str(time_lapse) + sign_bicondition + left_bracket


    prep_string = prep_string + sign_negation + state_heading_south_str(time_lapse)

    prep_string = prep_string + sign_conjunction + sign_negation + state_heading_west_str(time_lapse)

    prep_string = prep_string + sign_conjunction + sign_negation + state_heading_east_str(time_lapse)

    prep_string = prep_string + right_bracket

    # assigne the preposition statment to axiom_str
    axiom_str = axiom_str + prep_string

    # Comment or delete the next line once this function has been implemented.
    # commenting as per insructed
    # utils.print_not_implemented()

    #check whether output is correct or not
    #print('axiom_generator_heading_only_north' +axiom_str)

    #return the final preposition statment here
    return axiom_str

def axiom_generator_heading_only_east(t):
    """
    Assert that when heading is East, the agent is
    not heading any other direction.
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    sign_negation = '~'
    sign_disjunction = '|'
    sign_conjunction = '&'
    sign_bicondition = '<=>'
    sign_implication = '>>'

    # bracket statments
    left_bracket = '('
    right_bracket = ')'

    # create one preposition string
    prep_string = ''

    # craete time lapse variable
    time_lapse = t
    time_lapse_one = time_lapse + 1

    prep_string = prep_string + state_heading_east_str(time_lapse) + sign_bicondition + left_bracket

    prep_string = prep_string + sign_negation + state_heading_south_str(time_lapse) + sign_conjunction

    prep_string = prep_string + sign_negation + state_heading_west_str(time_lapse)

    prep_string = prep_string + sign_conjunction + sign_negation + state_heading_north_str(time_lapse)

    prep_string = prep_string + right_bracket

    # Add the preposition string to return statment
    axiom_str = axiom_str + prep_string



    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    #check the preposition statment
    #print('axiom_generator_heading_only_east' + axiom_str)


    #return the final output
    return axiom_str


def axiom_generator_heading_only_south(t):
    """
    Assert that when heading is South, the agent is
    not heading any other direction.
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    sign_negation = '~'
    sign_disjunction = '|'
    sign_conjunction = '&'
    sign_bicondition = '<=>'
    sign_implication = '>>'

    # create one preposition string
    prep_string = ''

    # craete time lapse variable
    time_lapse = t
    time_lapse_one = time_lapse + 1

    # bracket statments
    left_bracket = '('
    right_bracket = ')'

    #write preposition statment here
    prep_string = prep_string + state_heading_south_str(time_lapse) + sign_bicondition

    #assign the left bracket
    prep_string = prep_string + left_bracket

    prep_string = prep_string + sign_negation + state_heading_north_str(time_lapse)

    prep_string = prep_string + sign_conjunction + sign_negation + state_heading_west_str(time_lapse)

    prep_string = prep_string + sign_conjunction + sign_negation + state_heading_east_str(time_lapse)

    #assign ending bracket here
    prep_string = prep_string + right_bracket

    # append the preposition statment  in return statment
    axiom_str = axiom_str + prep_string

    # Comment or delete the next line once this function has been implemented.
    # commenting as mentioned in instruction
    # utils.print_not_implemented()

    #check whether statment is correct
    #print('axiom_generator_heading_only_south' + axiom_str)

    #return the axiom value
    return axiom_str

#submit final
def axiom_generator_heading_only_west(t):
    """
    Assert that when heading is West, the agent is
    not heading any other direction.
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    sign_negation = '~'
    sign_disjunction = '|'
    sign_conjunction = '&'
    sign_bicondition = '<=>'
    sign_implication = '>>'

    # create one preposition string
    prep_string = ''

    # bracket statments
    left_bracket = '('
    right_bracket = ')'

    # craete time lapse variable
    time_lapse = t
    time_lapse_one = time_lapse + 1

    prep_string = prep_string + state_heading_west_str(time_lapse)

    #addind doble implication
    prep_string = prep_string + sign_bicondition + left_bracket

    prep_string = prep_string + sign_negation + state_heading_south_str(time_lapse)

    prep_string = prep_string + sign_conjunction + sign_negation + state_heading_north_str(time_lapse)

    prep_string = prep_string + sign_conjunction + sign_negation + state_heading_east_str(time_lapse)

    #closing the prepositional statment
    prep_string = prep_string + right_bracket

    # Assign the prepositional statment to axiom string
    axiom_str = axiom_str + prep_string

    # Comment or delete the next line once this function has been implemented.
    # commenting as mentioned in instruction
    # utils.print_not_implemented()

    #print and check whether output is correct or not
    #print('axiom_generator_heading_only_west'+ axiom_str )

    #return the axiom string
    return axiom_str

##################################################################################10
def generate_heading_only_one_direction_axioms(t):
    return [axiom_generator_heading_only_north(t),
            axiom_generator_heading_only_east(t),
            axiom_generator_heading_only_south(t),
            axiom_generator_heading_only_west(t)]



def fetch_agent_action_type(agent_action):

    if agent_action == 'Action_List':
        return ['Forward', 'Grab', 'Shoot', 'Climb', 'TurnLeft', 'TurnRight', 'Wait']
    else :
        return ['forward', 'grab', 'shoot', 'climb', 'turnLeft', 'turnRight', 'wait']



def axiom_generator_only_one_action_axioms(t):
    """
    Assert that only one axion can be executed at a time.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    sign_negation = '~'
    sign_disjunction = '|'
    sign_conjunction = '&'
    sign_bicondition = '<=>'
    sign_implication = '>>'

    # create one preposition string
    prep_string = ''

    #fetch the action list
    agents_actions = fetch_agent_action_type('Action_List')

    # create the time in string
    time_String = str(t)

    # bracket statments
    left_bracket = '('
    right_bracket = ')'

    # craete time lapse variable
    time_lapse = t
    time_lapse_one = time_lapse + 1

    selected_axioms = []

    #enumerate give you the actions count and value
    for count, actions in enumerate(agents_actions):

        #apply the doble implication
        selected_step = actions + time_String + sign_bicondition + left_bracket

        #create one empty array
        mainatining_axioms = []

        #create one empty array
        remaining_axioms = []

        # enumerate give you the actions count and value
        for count_inner, actions_inner in enumerate(agents_actions):

            #if value are euqel then pass the condition
            if count != count_inner:
                remaining_axioms.append(sign_negation + actions_inner + time_String)


        #add conjunction - and condition between actions
        selected_step = selected_step + sign_conjunction.join(remaining_axioms)

        #close the preposition statment
        selected_step = selected_step + right_bracket

        #

        left_selected_step = left_bracket + selected_step

        left_selected_step_right = left_selected_step + right_bracket

        #appended axiom
        selected_axioms.append(left_selected_step_right)




    #add final action axioms with preposition string
    prep_string = prep_string + sign_conjunction.join(selected_axioms)

    # Append value with output return variable
    axiom_str = axiom_str + prep_string
    # Comment or delete the next line once this function has been implemented.
    # commenting as instructed in code
    # utils.print_not_implemented()

    # check whether preposition string is correct or not
    #print('axiom_generator_only_one_action_axioms' + prep_string)

    #return the final axiom statment here
    return axiom_str


def generate_mutually_exclusive_axioms(t):
    """
    Generate all time-based mutually exclusive axioms.
    """
    axioms = []

    # must be t+1 to constrain which direction could be heading _next_
    axioms.extend(generate_heading_only_one_direction_axioms(t + 1))

    # actions occur in current time, after percept
    axioms.append(axiom_generator_only_one_action_axioms(t))

    return filter(lambda s: s != '', axioms)

    # -------------------------------------------------------------------------------


