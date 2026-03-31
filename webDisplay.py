import sys
import json
import time

class WebDisplay:
    def __init__(self, fps=15):
        self.fps = fps
        self.delay = 1.0 / fps if fps > 0 else 0
        self.is_web = True
        self.last_send_time = 0

    def initialize(self, state, isBlue=False):
        self.send_state(state, is_init=True)
        self.last_send_time = time.time()
        if self.delay > 0:
            time.sleep(self.delay)

    def update(self, state):
        if self.delay == 0:
            now = time.time()
            # Max ~30 FPS during turbo training to prevent flooding Websockets
            if now - self.last_send_time > 0.033:
                self.send_state(state, is_init=False)
                self.last_send_time = now
        else:
            self.send_state(state, is_init=False)
            time.sleep(self.delay)

    def finish(self):
        msg = {'type': 'finish'}
        print("__WEB_DISPLAY__:" + json.dumps(msg))
        sys.stdout.flush()

    def send_state(self, state, is_init):
        # Extract dynamic state (state is a GameStateData object)
        try:
            pacman_pos = state.agentStates[0].getPosition() if len(state.agentStates) > 0 else None
        except:
            pacman_pos = None

        data = {
            'type': 'init' if is_init else 'update',
            'score': state.score,
            'pacman': pacman_pos,
        }
        
        if is_init:
            walls = state.layout.walls
            data['width'] = walls.width
            data['height'] = walls.height
            data['walls'] = [[x, y] for x in range(walls.width) for y in range(walls.height) if walls[x][y]]
            
        # Food and capsules are sent every frame because they can be eaten
        food = state.food
        data['food'] = [[x, y] for x in range(food.width) for y in range(food.height) if food[x][y]]
        data['capsules'] = state.capsules

        try:
            data['pacmanDir'] = str(state.agentStates[0].configuration.direction)
        except:
            data['pacmanDir'] = 'Stop'

        ghost_states = []
        for g in state.agentStates[1:]:
            try:
                if g.configuration is not None:
                    pos = g.getPosition()
                    scared = g.scaredTimer > 0
                    gdir = str(g.configuration.direction)
                    ghost_states.append({'pos': pos, 'scared': scared, 'dir': gdir})
            except:
                pass
        data['ghostStates'] = ghost_states
        
        print("__WEB_DISPLAY__:" + json.dumps(data))
        sys.stdout.flush()
        
    def pause(self):
        pass

    def drawExpandedCells(self, cells):
        pass

    def clearExpandedCells(self):
        pass

    def updateDistributions(self, distributions):
        pass
