import torch.nn as nn
import numpy as np
from collections import deque

class PrefrontalCortex(nn.Module):

  @staticmethod
  def get_default_config():
    config = {
    }
    return config

  def __init__(self, name, config):
    super().__init__()
    self._name = name
    self._config = config
    self._wm = deque([],18)
    self.start = True
    self._build()
    self.last_action = None
    self.LEFT_BUTTON = 1
    self.RIGHT_BUTTON = 2
    self.grids = {
                  0: [8, 13, 7, 9],
                  self.LEFT_BUTTON:  [12, 17],
                  self.RIGHT_BUTTON:  [14, 19],
                 }

  def _build(self):
    pass

  def forward(self, what_where_obs_dict, mtl_out, bg_action, reward):
    #Given a positive reward
    # find overlap between representation of grids of target 
    #   and  representations  of grids of sample corresponding to last action button in (bg_action)
    #Given a negative reward
    # find overlap between representation of grids of target 
    #   and  representations  of grids of sample corresponding to the button other than the last action (bg_action)
    #Find the overlap of the overlap representation with last stored overlap representations (multiple tutoring sessions)
    # as the task representation
    #clear memory

    #IDEA 1
    #Create overlap of target location and left location, if either not found then zero
    #Create overlap of target location and right location, if either not found then zero
    #Send task representation + left overlap and right overlap to BG.

    #IDEA 2
    #If grid is of interest store in memory. 
    # Find the overlap of the current grid representation with the target area if found
    # If overlap overlaps with task representation send sample grid representation.

    if self.start and what_where_obs_dict != None:
      self.sample_input = np.zeros_like( what_where_obs_dict["fovea"])
      self._wm.append(self.sample_input)
      self.start = False
      
    if (what_where_obs_dict != None) and self.last_action in sum(self.grids.values(),[]):
      self._wm.append(what_where_obs_dict["fovea"])
    
    if bg_action != None:
      self.last_action = bg_action

      if bg_action < 3: 
        self._wm = deque([],18)
        self._wm.append(self.sample_input)
    
    # if (len(self._wm) > 18):
    #   self._wm.pop(0)
    
    flat_wm =  np.max(self._wm, axis=0)
    pfc_observation = { "full": flat_wm }
    pfc_action = bg_action


    pfc_observation = what_where_obs_dict
#    pfc_observation = self._wm # what_where_obs_dict
    # print("======> Agent: bg_action", bg_action)




    return pfc_observation, pfc_action

''' Alternate
  def forward(self, what_where_obs_dict, mtl_out, bg_action, reward):
    #Given a positive reward
    # find overlap between representation of grids of target 
    #   and  representations  of grids of sample corresponding to last action button in (bg_action)
    #Given a negative reward
    # find overlap between representation of grids of target 
    #   and  representations  of grids of sample corresponding to the button other than the last action (bg_action)
    #Find the overlap of the overlap representation with last stored overlap representations (multiple tutoring sessions)
    # as the task representation
    #clear memory

    #IDEA 1
    #Create overlap of target location and left location, if either not found then zero
    #Create overlap of target location and right location, if either not found then zero
    #Send task representation + left overlap and right overlap to BG.

    #IDEA 2
    #If grid is of interest store in memory. 
    # Find the overlap of the current grid representation with the target area if found
    # If overlap overlaps with task representation send sample grid representation.

    if (what_where_obs_dict != None):
      self._wm.append([what_where_obs_dict["fovea"], self.last_action])
    
    if bg_action != None:
      self.last_action = bg_action

      if bg_action < 3: 
        self.last_press_action = bg_action
    
    if reward != None:
      if reward>0:
        side_to_use = self.last_press_action
      elif reward<0:
        side_to_use = self.LEFT_BUTTON if self.last_press_action == self.RIGHT_BUTTON else self.RIGHT_BUTTON

      if reward>0 or reward<0:
        task_representation = []
        for grid in self.grids[side_to_use]:
          grid_repr = list(filter(lambda x: x[1]==grid, self._wm))[-1:]
          if len(grid_repr)>0:
            for target_grid in self.grids[0]:
              target_grid_repr = list(filter(lambda x: x[1]==target_grid, self._wm))[-1:]
              if len(target_grid_repr)>0:
                task_representation.append(overlap([grid_repr, target_grid_repr]))

        task_representation = overlap(task_representation)
        self.task_representation = overlap(task_representation, self.task_representation)
        if np.sum(self.task_representation) == 0:
          self.task_representation = task_representation

      

    # if (len(self._wm) > 18):
    #   self._wm.pop(0)
    
    pfc_action = bg_action


    pfc_observation = what_where_obs_dict
#    pfc_observation = self._wm # what_where_obs_dict
    # print("======> Agent: bg_action", bg_action)




    return pfc_observation, pfc_action
'''