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
    self._wm = deque([], 36)
    self._build()

  def _build(self):
    pass

  def forward(self, what_where_obs_dict, mtl_out, bg_action):
    if (what_where_obs_dict != None):
      self._wm.append(what_where_obs_dict["full"])
    
    # if (len(self._wm) > 18):
    #   self._wm.pop(0)
    
    pfc_action = bg_action

    flat_wm =  np.max(self._wm, axis=0)
    pfc_observation = { "full": flat_wm }

#    pfc_observation = what_where_obs_dict
#    pfc_observation = self._wm # what_where_obs_dict
    # print("======> Agent: bg_action", bg_action)




    return pfc_observation, pfc_action
