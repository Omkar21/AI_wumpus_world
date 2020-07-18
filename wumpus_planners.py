# wumpus_planners.py
# ------------------
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

from wumpus_environment import *
from wumpus_kb import *
import search

#-------------------------------------------------------------------------------
# Distance fn
#-------------------------------------------------------------------------------

def manhattan_distance_with_heading(current, target):
    """
    Return the Manhattan distance + any turn moves needed
        to put target ahead of current heading
    current: (x,y,h) tuple, so: [0]=x, [1]=y, [2]=h=heading)
    heading: 0:^:north 1:<:west 2:v:south 3:>:east
    """
    md = abs(current[0] - target[0]) + abs(current[1] - target[1])
    if current[2] == 0:   # heading north
        # Since the agent is facing north, "side" here means
        # whether the target is in a row above or below (or
        # the same) as the agent.
        # (Same idea is used if agent is heading south)
        side = (current[1] - target[1])
        if side > 0:
            md += 2           # target is behind: need to turns to turn around
        elif side <= 0 and current[0] != target[0]:
            md += 1           # target is ahead but not directly: just need to turn once
        # note: if target straight ahead (curr.x == tar.x), no turning required
    elif current[2] == 1: # heading west
        # Now the agent is heading west, so "side" means
        # whether the target is in a column to the left or right
        # (or the same) as the agent.
        # (Same idea is used if agent is heading east)
        side = (current[0] - target[0])
        if side < 0:
            md += 2           # target is behind
        elif side >= 0 and current[1] != target[1]:
            md += 1           # target is ahead but not directly
    elif current[2] == 2: # heading south
        side = (current[1] - target[1])
        if side < 0:
            md += 2           # target is behind
        elif side >= 0 and current[0] != target[0]:
            md += 1           # target is ahead but not directly
    elif current[2] == 3: # heading east
        side = (current[0] - target[0])
        if side > 0:
            md += 2           # target is behind
        elif side <= 0 and current[1] != target[1]:
            md += 1           # target is ahead but not directly
    return md


#-------------------------------------------------------------------------------
# Plan Route
#-------------------------------------------------------------------------------

def plan_route(current, heading, goals, allowed):
    """
    Given:
       current location: tuple (x,y)
       heading: integer representing direction
       gaals: list of one or more tuple goal-states
       allowed: list of locations that can be moved to
    ... return a list of actions (no time stamps!) that when executed
    will take the agent from the current location to one of (the closest)
    goal locations
    You will need to:
    (1) Construct a PlanRouteProblem that extends search.Problem
    (2) Pass the PlanRouteProblem as the argument to astar_search
        (search.astar_search(Problem)) to find the action sequence.
        Astar returns a node.  You can call node.solution() to exract
        the list of actions.
    NOTE: represent a state as a triple: (x, y, heading)
          where heading will be an integer, as follows:
          0='north', 1='west', 2='south', 3='east'
    """

    # Ensure heading is a in integer form
    if isinstance(heading,str):
        heading = Explorer.heading_str_to_num[heading]

    if goals and allowed:
        prp = PlanRouteProblem((current[0], current[1], heading), goals, allowed)
        # NOTE: PlanRouteProblem will include a method h() that computes
        #       the heuristic, so no need to provide here to astar_search()
        node = search.astar_search(prp)
        if node:
            return node.solution()
    
    # no route can be found, return empty list
    return []

#-------------------------------------------------------------------------------

class PlanRouteProblem(search.Problem):
    def __init__(self, initial, goals, allowed):
        """ Problem defining planning of route to closest goal
        Goal is generally a location (x,y) tuple, but state will be (x,y,heading) tuple
        initial = initial location, (x,y) tuple
        goals   = list of goal (x,y) tuples
        allowed = list of state (x,y) tuples that agent could move to """
        self.initial = initial # initial state
        self.goals = goals     # list of goals that can be achieved
        self.allowed = allowed # the states we can move into

    def h(self,node):
        """
        Heuristic that will be used by search.astar_search()
        """
        "*** YOUR CODE HERE ***"

        #we are already given with the manhatten distance method
        #Take a limiting variable which limit max distance
        max_possible_distance = 10000000

        #write goal states
        possible_goal_states = self.goals

        #find agents states here:
        agent_conditions = node.state

        #Looping over the goal states

        for prob_goal_points in possible_goal_states:
            #calculate the manhatten distance
            perpendicular_distance = manhattan_distance_with_heading(agent_conditions, prob_goal_points)

            #Check calculated manhatten distance should be less than threshold
            if max_possible_distance > perpendicular_distance:

                #if its less than max
                max_possible_distance = perpendicular_distance

        #return the final value of max_possible_distance
        return max_possible_distance

        #commenting the pass val
        #pass


    def direction_assign(self, direction):

        if direction == 'left':
            return ['TurnLeft']
        if direction == 'right':
            return ['TurnRight']
        if direction == 'forward':
            return ['Forward']




    def actions(self, state):
        """
        Return list of allowed actions that can be made in state
        """
        "*** YOUR CODE HERE ***"

        #create variable who can store the state value
        direction_point = state[2]

        #direction list
        direction_list = [0, 1, 2, 3]

        #define agent gold state
        agent_gold_goal = self.goals

        #assign variable to numbers
        num_zero = 0
        num_one = 1
        num_two = 2
        num_three = 3

        actions = None

        #find the agents allowed states
        agents_location_allowed = self.allowed

        #maximum move in west direction
        west_move_condition = 100000

        right_move_condition = 0

        left_move_condition = 0

        #define the states to reuse
        condition_zero = state[0]
        condition_one = state[1]
        condition_two = state[2]

        agent_move_forward = state
        agent_turn_right = state
        agent_turn_left = state

        #Assign max distance values

        max_possible_foeward_distance = 100000

        max_possible_right_distance = 100000

        max_possible_left_distance = 100000

        #possible final action type
        final_action_way = []




        # condition for west direction
        if direction_point == direction_list[num_one]:

            #state change right val
            agent_turn_right = (condition_zero, condition_one, condition_two - num_one)

            #state change left val
            agent_turn_left = (condition_zero, condition_one, condition_two + num_one)

            #state change forward val
            agent_move_forward = (condition_zero - num_one, condition_one, condition_two)

        # condition for south direction
        elif direction_point == direction_list[num_two]:

            #state change right val
            agent_turn_right = (condition_zero, condition_one, condition_two - num_one)

            #state change left val
            agent_turn_left = (condition_zero, condition_one, condition_two + num_one)

            #state change forward val
            agent_move_forward = (condition_zero, condition_one - num_one, condition_two)

            #condition for north direction
        elif direction_point == direction_list[num_zero]:

            #state change right val
            agent_turn_right = (condition_zero, condition_one, num_three)

            #state change left val
            agent_turn_left = (condition_zero, condition_one, condition_two + num_one)

            #state change forward val
            agent_move_forward = (condition_zero, condition_one + num_one, condition_two)




        #condition for east direction
        elif direction_point == direction_list[num_three]:

            #state change right val
            agent_turn_right = (condition_zero, condition_one, condition_two - num_one)

            #state change left val
            agent_turn_left = (condition_zero, condition_one, num_zero)

            #state change forward val
            agent_move_forward = (condition_zero + num_one, condition_one, condition_two)



        #checking for the gold location
        for goal_gold_points in agent_gold_goal:

            #check if fetching location allowed or not
            if (agent_move_forward[num_zero], agent_move_forward[num_one]) in agents_location_allowed:

                #Calculating manhatten distance in west move direction
                west_move_condition = manhattan_distance_with_heading(agent_move_forward, goal_gold_points)

            #calculating right move direction with mahatten distance
            right_move_condition = right_move_condition + manhattan_distance_with_heading(agent_turn_right, goal_gold_points)

            #calculated the left move direction with manhatten distance
            left_move_condition = left_move_condition + manhattan_distance_with_heading(agent_turn_left, goal_gold_points)

            #comparing with maximun right distance
            if max_possible_right_distance > right_move_condition:
                #assigning to max val
                max_possible_right_distance = right_move_condition

            #comparing with maximum forward distance
            if max_possible_foeward_distance > west_move_condition:
                #assigning to max value
                max_possible_foeward_distance = west_move_condition

            #comparing with maximum left value
            if max_possible_left_distance > left_move_condition:
                #assigning to max val
                max_possible_left_distance = left_move_condition



        if max_possible_right_distance <= max_possible_left_distance and max_possible_right_distance <= max_possible_foeward_distance :

                #deciding final action as right move
                final_action_way = self.direction_assign ('right')


        elif max_possible_foeward_distance <= max_possible_left_distance and max_possible_foeward_distance <= max_possible_right_distance :

                #deciding final move as forward move
                final_action_way = self.direction_assign('forward')

        elif max_possible_left_distance <= max_possible_foeward_distance and max_possible_left_distance <= max_possible_right_distance:

                #deciding final move as left move
                final_action_way = self.direction_assign('left')


        #returing the finalized selected action value
        return final_action_way

        #commenting the pass val
        #pass



    def result(self, state, action):
        """
        Return the new state after applying action to state
        """
        "*** YOUR CODE HERE ***"




        # create variable who can store the state value
        direction_point = state[2]

        #create one list to store the agents plan of movement
        agent_plan_list = [0, 4, 5]

        #new state after adopting the perticular action
        adopted_action_state = state

        #finding the action decisions
        action_decision = proposition_bases_actions.index(action)

        # assign variable to numbers
        num_zero = 0
        num_one = 1
        num_two = 2
        num_three = 3

        # define the states to reuse
        condition_zero = state[0]


        condition_one = state[1]


        condition_two = state[2]

        # direction list
        direction_list = [0, 1, 2, 3]

        # state condition when agent turns left
        if action_decision == agent_plan_list[num_one]:

            # state adopted after turning left
            adopted_action_state = (condition_zero, condition_one, condition_two + num_one)

            # check state[two] value less than three or not
            if adopted_action_state[num_two] > num_three:

                # assign to adopted state
                adopted_action_state = (condition_zero, condition_one, num_zero)

        # state condition when agent move in forward direction
        elif action_decision == agent_plan_list[num_zero]:


            #state for north direction face
            if direction_point == direction_list[num_zero]:

                #assign to the adopted state
                adopted_action_state = (condition_zero, condition_one + num_one, condition_two)

            # state for east direction face
            elif direction_point == direction_list[num_three]:

                #assign to adopted state
                adopted_action_state = (condition_zero + num_one, condition_one, condition_two)

            # state for the west direction face
            elif direction_point == direction_list[num_one]:

                #assign to adopted state
                adopted_action_state = (condition_zero - num_one, condition_one, condition_two)

            # state for south direction face
            elif direction_point == direction_list[num_two]:

                #assign to adopted state
                adopted_action_state = (condition_zero, condition_one - num_one, condition_two)



                # state condition when agent turns right
        elif action_decision == agent_plan_list[num_two]:

            #assign variable
            condition_third = condition_two - num_one

            # assign to adopted state
            adopted_action_state = (condition_zero, condition_one, condition_third)

            #comparing second step with zero value
            if adopted_action_state[num_two] < num_zero:

                #add the values in action state
                adopted_action_state = (condition_zero, condition_one, num_three)




        #returning the final state
        return adopted_action_state

        #pass

    def goal_test(self, state):
        """
        Return True if state is a goal state
        """
        "*** YOUR CODE HERE ***"
        # define the states to reuse
        condition_zero = state[0]
        condition_one = state[1]
        condition_two = state[2]

        state_zero = state[0]
        state_one = state[1]

        #assign goal points
        goal_points = self.goals

        if (condition_zero, condition_one) in goal_points:
            return True
        else:
            return False


#-------------------------------------------------------------------------------

def test_PRP(initial):
    """
    The 'expected initial states and solution pairs' below are provided
    as a sanity check, showing what the PlanRouteProblem soluton is
    expected to produce.  Provide the 'initial state' tuple as the
    argument to test_PRP, and the associate solution list of actions is
    expected as the result.
    The test assumes the goals are [(2,3),(3,2)], that the heuristic fn
    defined in PlanRouteProblem uses the manhattan_distance_with_heading()
    fn above, and the allowed locations are:
        [(0,0),(0,1),(0,2),(0,3),
        (1,0),(1,1),(1,2),(1,3),
        (2,0),            (2,3),
        (3,0),(3,1),(3,2),(3,3)]
    
    Expected intial state and solution pairs:
    (0,0,0) : ['Forward', 'Forward', 'Forward', 'TurnRight', 'Forward', 'Forward']
    (0,0,1) : ['TurnRight', 'Forward', 'Forward', 'Forward', 'TurnRight', 'Forward', 'Forward']
    (0,0,2) : ['TurnLeft', 'Forward', 'Forward', 'Forward', 'TurnLeft', 'Forward', 'Forward']
    (0,0,3) : ['Forward', 'Forward', 'Forward', 'TurnLeft', 'Forward', 'Forward']
    """
    return plan_route((initial[0],initial[1]), initial[2],
                      # Goals:
                      [(2,3),(3,2)],
                      # Allowed locations:
                      [(0,0),(0,1),(0,2),(0,3),
                       (1,0),(1,1),(1,2),(1,3),
                       (2,0),            (2,3),
                       (3,0),(3,1),(3,2),(3,3)])


#-------------------------------------------------------------------------------
# Plan Shot
#-------------------------------------------------------------------------------

def plan_shot(current, heading, goals, allowed):
    """ Plan route to nearest location with heading directed toward one of the
    possible wumpus locations (in goals), then append shoot action.
    NOTE: This assumes you can shoot through walls!!  That's ok for now. """
    if goals and allowed:
        psp = PlanShotProblem((current[0], current[1], heading), goals, allowed)
        node = search.astar_search(psp)
        if node:
            plan = node.solution()
            plan.append(action_shoot_str(None))
            # HACK:
            # since the wumpus_alive axiom asserts that a wumpus is no longer alive
            # when on the previous round we perceived a scream, we
            # need to enforce waiting so that itme elapses and knowledge of
            # "dead wumpus" can then be inferred...
            plan.append(action_wait_str(None))
            return plan

    # no route can be found, return empty list
    return []

#-------------------------------------------------------------------------------

class PlanShotProblem(search.Problem):
    def __init__(self, initial, goals, allowed):
        """ Problem defining planning to move to location to be ready to
              shoot at nearest wumpus location
        NOTE: Just like PlanRouteProblem, except goal is to plan path to
              nearest location with heading in direction of a possible
              wumpus location;
              Shoot and Wait actions is appended to this search solution
        Goal is generally a location (x,y) tuple, but state will be (x,y,heading) tuple
        initial = initial location, (x,y) tuple
        goals   = list of goal (x,y) tuples
        allowed = list of state (x,y) tuples that agent could move to """
        self.initial = initial # initial state
        self.goals = goals     # list of goals that can be achieved
        self.allowed = allowed # the states we can move into

        #write the allowed possible shots
        allowed_possible_shoot = self.allowed

        #write the allowed possible location
        allowed_possible_locations = self.allowed

        #assigning the variables
        num_zero = 0

        num_one = 1

        num_two = 2

        num_three = 3



        #this code is specifically to shoot the wumpus

        #firstly iterate over all shoting points
        for possible_shoots in allowed_possible_shoot:

            #then iterate over all possible locations
            for allowed_location in allowed_possible_locations:

                #here we can write
                possible_shoot_1 = possible_shoots[num_one]

                possible_shoot_0 = possible_shoots[num_zero]

                allowed_location_0 = allowed_location[num_zero]

                allowed_location_1 = allowed_location[num_one]


                # when agents face on west
                if possible_shoot_1 ==allowed_location_1 and possible_shoot_0 > allowed_location_0:

                    #agent will shooot in west direction
                    self.shot_at.append((possible_shoot_0, possible_shoot_1, num_one))

                # when agents face on east
                elif possible_shoot_1 < allowed_location_1 and possible_shoot_0 < allowed_location_0:

                    #agent will shoot in east direction
                    self.shot_at.append((possible_shoot_0, possible_shoot_1, num_three))

            #when the agents face is on north
                elif possible_shoot_1 < allowed_location_1 and possible_shoot_0 == allowed_location_0 :

                    #agent will shoot in north direction
                    self.shot_at.append((possible_shoot_0, possible_shoot_1, num_zero))


                #when agents face on south
                elif possible_shoot_1 > allowed_location_1 and possible_shoot_0 == allowed_location_0:

                    #agent will get shooted in south direction
                    self.shot_at.append((possible_shoot_0, possible_shoot_1, num_two))




    def h(self,node):
        """
        Heuristic that will be used by search.astar_search()
        """
        "*** YOUR CODE HERE ***"
        # we are already given with the manhatten distance method
        # Take a limiting variable which limit max distance
        max_possible_distance = 10000000

        #write possible locations
        possible_agent_points = node.state

        #find the shoot points
        possible_shoot_point = self.shot_at

        for wumpus_points in possible_shoot_point:

            #Calculating manhatten distance as its block structure
            distance_travel_agent = manhattan_distance_with_heading(possible_agent_points, wumpus_points)

            probable_distance = distance_travel_agent

            #comparing with maximum distance
            if max_possible_distance > probable_distance:

                #convert max distance to calculated one
                max_possible_distance = probable_distance

        #returning the maximium distance value
        return max_possible_distance
        #pass

    def direction_assign(self, direction):

        if direction == 'left':
            return ['TurnLeft']

        if direction == 'right':
            return ['TurnRight']

        if direction == 'forward':
            return ['Forward']


    def actions(self, state):
        """
        Return list of allowed actions that can be made in state
        """
        "*** YOUR CODE HERE ***"

        #create the variable with max possible distance
        max_possible_distance = 100000
        forward_action_decide = []

        #push the state value after actions

        new_action_point = state

        #check whether agent changed position or not
        is_agent_state_changed = False

        # check shot values for each agents
        point_shot_val = self.shot_at

        # create variable who can store the state value
        direction_point = state[2]

        #Assign max distance values

        max_possible_foeward_distance = 100000

        max_possible_right_distance = 100000

        max_possible_left_distance = 100000

        west_move_condition = 100000

        right_move_condition = 0

        left_move_condition = 0

        # direction list
        direction_list = [0, 1, 2, 3]

        #assign numbers to variable for multiple use
        num_zero = 0
        num_one = 1
        num_two = 2
        num_three = 3

        negate_one = -1

        #the agents allowed states
        allowed_agent_state = self.allowed

        # define the states to reuse
        condition_zero = state[0]
        condition_one = state[1]
        condition_two = state[2]

        #fetch the state values

        for shot_points in point_shot_val:
            # define the states to reuse
            condition_shoot_zero = shot_points[0]

            condition_shoot_one = shot_points[1]

            condition_shoot_two = shot_points[2]

            #comparing state and shoot conditions
            if (condition_zero, condition_one) == (condition_shoot_zero, condition_shoot_one):
                #finding the difference in state and shots
                state_shot_diff = condition_two - condition_shoot_two

                #checking if difference is -1
                if state_shot_diff == negate_one:
                    #taking turn left decision
                    forward_action_decide = self.direction_assign('left')
                else:
                    #Taking turn right decision
                    forward_action_decide = self.direction_assign('right')

                #assigning state change boolean condition to trur
                is_agent_state_changed = True

        #if the agant state is not changes
        if not is_agent_state_changed:


            agent_move_forward = state

            agent_turn_right = state

            agent_turn_left = state

            #condition for north direction
            if direction_point == direction_list[num_zero]:
                #state right
                agent_turn_right = (condition_zero, condition_one, num_three)

                #state left
                agent_turn_left = (condition_zero, condition_one, condition_two + num_one)

                #state move forward
                agent_move_forward = (condition_zero, condition_one + num_one, condition_two)

                # condition for south direction

            elif direction_point == direction_list[num_two]:

                #state move forward
                agent_move_forward = (condition_zero, condition_one - num_one, condition_two)

                #state move right
                agent_turn_right = (condition_zero, condition_one, condition_two - num_one)

                #state move left
                agent_turn_left = (condition_zero, condition_one, condition_two + num_one)

            # condition for east direction

            elif direction_point == direction_list[num_three]:

                #state move right
                agent_turn_right = (condition_zero, condition_one, condition_two - num_one)

                #state move left
                agent_turn_left = (condition_zero, condition_one, num_zero)

                #state move forward
                agent_move_forward = (condition_zero + num_one, condition_one, condition_two)

            #condition for west direction

            elif direction_point == direction_list[num_one]:

                #state move right
                agent_turn_right = (condition_zero, condition_one, condition_two - num_one)

                #satte move left
                agent_turn_left = (condition_zero, condition_one, condition_two + num_one)

                #state move forward
                agent_move_forward = (condition_zero - num_one, condition_one, condition_two)







            for shoot_value in point_shot_val:

                if (agent_move_forward[num_zero], agent_move_forward[num_one]) in allowed_agent_state:
                    #calculating the manhatten distance by given method
                    west_move_condition = manhattan_distance_with_heading(agent_move_forward, shoot_value)

                #calculating and adding right hand distance
                right_move_condition = right_move_condition + manhattan_distance_with_heading(agent_turn_right, shoot_value)

                #Calculating and adding left hand distance
                left_move_condition =  left_move_condition + manhattan_distance_with_heading(agent_turn_left, shoot_value)






                #cmparing right move with max right move value
                if max_possible_right_distance > right_move_condition:
                    #if max distance is more
                    max_possible_right_distance = right_move_condition

                #cmparing forward move with max forward move value
                if max_possible_foeward_distance > west_move_condition:
                    #if max distance is more
                    max_possible_foeward_distance = west_move_condition

                #comparing left move with max left move
                if max_possible_left_distance > left_move_condition:
                    #if max distance is more
                    max_possible_left_distance = left_move_condition


            #Cheking for left state
            if max_possible_left_distance <= max_possible_foeward_distance and max_possible_left_distance <= max_possible_right_distance:
                #decide urn left
                forward_action_decide = self.direction_assign('left')

            #Checking for forward state
            elif max_possible_foeward_distance <= max_possible_left_distance and max_possible_foeward_distance <= max_possible_right_distance :
                #decide move forward
                forward_action_decide = self.direction_assign('forward')

            #checking for right move state
            elif max_possible_right_distance <= max_possible_left_distance and max_possible_right_distance <= max_possible_foeward_distance:
                #decide turn right
                forward_action_decide = self.direction_assign('right')

        #return the final state
        return forward_action_decide




        #pass

    def result(self, state, action):
        """
        Return the new state after applying action to state
        """
        "*** YOUR CODE HERE ***"

        # direction list
        direction_list = [0, 1, 2, 3]

        # create variable who can store the state value
        direction_point = state[2]

        #save the state value fter taking the new action
        dev_shot_actions = state

        #select the action decision
        action_decision = proposition_bases_actions.index(action)

        num_zero = 0
        num_one = 1
        num_two = 2
        num_three = 3


        # define the states to reuse
        condition_zero = state[0]

        condition_one = state[1]

        condition_two = state[2]

        # create one list to store the agents plan of movement
        agent_plan_list = [0, 4, 5]

        #When action is forward
        if action_decision == agent_plan_list[num_zero]:

            # state change in west direction
            if direction_point == direction_list[num_one]:

                dev_shot_actions = (condition_zero - num_one, condition_one, condition_two)

            # state change in south direction
            elif direction_point == direction_list[num_two]:

                dev_shot_actions = (condition_zero, condition_one - num_one, condition_two)

            #state change in north direction
            elif direction_point == direction_list[num_zero]:

                dev_shot_actions = (condition_zero, condition_one + num_one, condition_two)



             #state change in east direction
            elif direction_point == direction_list[num_three]:
                dev_shot_actions = (condition_zero + num_one, condition_one, condition_two)


        #when action is to turn right
        elif action_decision == agent_plan_list[num_two]:

            dev_shot_actions = (condition_zero, condition_one, condition_two - num_one)

            if dev_shot_actions[num_two] < num_zero:

                dev_shot_actions = (condition_zero, condition_one, num_three)



         #When action is to turn the agent in left
        elif action_decision == agent_plan_list[num_one]:

            dev_shot_actions = (condition_zero, condition_one, condition_two + num_one)

            if dev_shot_actions[num_two] > num_three:
                dev_shot_actions = (condition_zero, condition_one, num_zero)

        return dev_shot_actions

        #pass

    #changes made by omkar kulkarni
    def goal_test(self, state):
        """
        Return True if state is a goal state
        """
        "*** YOUR CODE HERE ***"

        # define the states to reuse
        condition_zero = state[0]

        condition_one = state[1]

        condition_two = state[2]

        #assign shot ponts value
        point_shot_val = self.shot_at

        #check it conditionally
        if state in point_shot_val:
            #returning as true
            return True
        else:
            #returnig it as False
            return False

#-------------------------------------------------------------------------------

def test_PSP(initial = (0,0,3)):
    """
    The 'expected initial states and solution pairs' below are provided
    as a sanity check, showing what the PlanShotProblem soluton is
    expected to produce.  Provide the 'initial state' tuple as the
    argumetn to test_PRP, and the associate solution list of actions is
    expected as the result.
    The test assumes the goals are [(2,3),(3,2)], that the heuristic fn
    defined in PlanShotProblem uses the manhattan_distance_with_heading()
    fn above, and the allowed locations are:
        [(0,0),(0,1),(0,2),(0,3),
        (1,0),(1,1),(1,2),(1,3),
        (2,0),            (2,3),
        (3,0),(3,1),(3,2),(3,3)]
    
    Expected intial state and solution pairs:
    (0,0,0) : ['Forward', 'Forward', 'TurnRight', 'Shoot', 'Wait']
    (0,0,1) : ['TurnRight', 'Forward', 'Forward', 'TurnRight', 'Shoot', 'Wait']
    (0,0,2) : ['TurnLeft', 'Forward', 'Forward', 'Forward', 'TurnLeft', 'Shoot', 'Wait']
    (0,0,3) : ['Forward', 'Forward', 'Forward', 'TurnLeft', 'Shoot', 'Wait']
    """
    return plan_shot((initial[0],initial[1]), initial[2],
                     # Goals:
                     [(2,3),(3,2)],
                     # Allowed locations:
                     [(0,0),(0,1),(0,2),(0,3),
                      (1,0),(1,1),(1,2),(1,3),
                      (2,0),            (2,3),
                      (3,0),(3,1),(3,2),(3,3)])
    
#-------------------------------------------------------------------------------

##final submit 2
