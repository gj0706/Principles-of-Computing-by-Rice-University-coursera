"""
Cookie Clicker Simulator
"""
import simpleplot
import math
# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._current_time = 0.0
        self._current_cookies = 0.0
        self._cookies_per_sec = 1.0
        self._total_cookies = 0.0
        self._history = [(0.0, None, 0.0, 0.0 )]
        
        
    def __str__(self):
        """
        Return human readable state
        """
        return "Time: " + \
        str(self.get_time()) + "\nCurrent number of cookies: " + \
        str(self.get_cookies()) + "\ncookies_per_sec: " +\
        str(self.get_cps()) + "\nTotal cookies made: " +\
        str(self._total_cookies) + "History: " +\
        str(self.get_history())
                
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cookies_per_sec
    
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history


    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_cookies >= cookies:
            return 0.0
        else:
            return math.ceil((cookies - self._current_cookies) / self._cookies_per_sec)
   
   
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0:
            pass
        else:
            self._current_time += time
            self._current_cookies += self._cookies_per_sec * time
            self._total_cookies += self._cookies_per_sec * time
         
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies < cost:
            pass
        else:
            self._current_cookies -= cost
            self._cookies_per_sec += additional_cps
            self._history.append((self.get_time(), item_name,
                            cost, self._total_cookies))
        
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    new_build_info = build_info.clone()
    clicker = ClickerState()
    
    while duration >= 0:                
        item = strategy(clicker.get_cookies(),
                      clicker.get_cps(),
                      clicker.get_history(), 
                      duration,
                      new_build_info)
        # Check the current time and break out of the loop if the
        # Duration has been passed                      
        if item == None:
            break
        time_wait = clicker.time_until(new_build_info.get_cost(item))       
        # Call the strategy function to determine which item to buy next.        
        # Determine how much time must elapse until it is possible to purchase
        #the item.
        if time_wait > duration:
            break
        else:
            clicker.wait(time_wait)
            clicker.buy_item(item, new_build_info.get_cost(item), new_build_info.get_cps(item))
            new_build_info.update_item(item)
            duration -= time_wait
                          
    # after the loop, if time left, allow cookies to accumulate for the time left
    clicker.wait(duration)         
       
    return clicker
  

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"


def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None


def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    build_cheap = build_info.clone()
    item_list = build_cheap.build_items()
    cost_list = map(build_cheap.get_cost, item_list)
    cheapest_index = cost_list.index(min(cost_list))
    cheapest_item = item_list[cheapest_index]
    
    if cost_list[cheapest_index] > cookies + cps * time_left:
        return None
    else:
        return cheapest_item
    

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    build_expensive = build_info.clone()
    item_list = build_expensive.build_items()
    cost_list = map(build_expensive.get_cost, item_list)
    expensive_index = cost_list.index(min(cost_list))
    expensive_item = item_list[expensive_index]
    
    if cost_list[expensive_index] > cookies + cps * time_left:
        return None
    else:
        return expensive_item


def strategy_best(cookies, cps, history, time_left, build_info):
    """
    Return strategy that has the highest ratio of cps/cost
    """
    build_best = build_info.clone()
    item_list = build_best.build_items()
    cost_list = map(build_info.get_cost, item_list)
    cps_list = map(build_info.get_cps, item_list)
    ratio_list = []
    for idx in range(len(item_list)):
        ratio = cps_list[idx] / cost_list[idx]
        ratio_list.append(ratio)
    best = ratio_list.index(max(ratio_list))
 
    return item_list[best]
    
    
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)
##
def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
#    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
#    run_strategy("Expensive", SIM_TIME, strategy_expensive)
#    run_strategy("Best", SIM_TIME, strategy_best)
#    
run()
    
 
    
    
    
    
    
    
    
