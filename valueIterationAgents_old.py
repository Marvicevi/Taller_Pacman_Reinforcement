# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations

        #**********************************
        #self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        # All the states start with the value of zero
        self.values = util.Counter() # A Counter is a dict with default 0
        states = mdp.getStates()

        # For each state, update with new value in new_values.
        for i in range(0,iterations):
            new_values = util.Counter()
            for state in states:
                action = self.getAction(state) # Pick the best action using the policy.
                if action is not None:
                    # Get the value from the state, using the maximun utility from the best q-state.
                    new_values[state] = self.getQValue(state, action)

            self.values = new_values
        #**********************************

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        # **********************************

        total = 0
        transStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)

        for tranStateAndProb in transStatesAndProbs:
            tstate = tranStateAndProb[0]
            prob = tranStateAndProb[1]
            reward = self.mdp.getReward(state, action, tstate)
            value = self.getValue(tstate)
            total += prob * (reward + self.discount * value)

        return total

        # **********************************



        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.

           V_{k+1}(s) = max[a] Q*(s,a)
        """
        # **********************************
        if self.mdp.isTerminal(state):
            return None
        else:
            actions = self.mdp.getPossibleActions(state)
            max_value = self.getQValue(state, actions[0])
            max_action = actions[0]

            for action in actions:
                value = self.getQValue(state, action)
                if max_value <= value:
                    max_value = value
                    max_action = action

            return max_action

        util.raiseNotDefined()

        # **********************************

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
