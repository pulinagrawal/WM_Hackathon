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
    self._wm = deque([],12)
    self._wm_fovea = deque([],12)
    self._wm_peripheral = deque([],12)
    self._wm_gaze = deque([],12)
    self._build()

  def _build(self):
    pass

  def forward(self, what_where_obs_dict, mtl_out, bg_action):
    if (what_where_obs_dict != None):
      if "full" in what_where_obs_dict:
        self._wm.append(what_where_obs_dict["full"])
      else:
        self._wm_fovea.append(what_where_obs_dict["fovea"])
        self._wm_peripheral.append(what_where_obs_dict["peripheral"])
        self._wm_gaze.append(what_where_obs_dict["gaze"])
    
    # if (len(self._wm) > 18):
    #   self._wm.pop(0)
    
    pfc_action = bg_action
    pfc_observation = what_where_obs_dict

    if (what_where_obs_dict != None):
      if "full" in what_where_obs_dict:
        flat_wm =  np.mean(self._wm, axis=0)
        pfc_observation = { "full": flat_wm }
      else:
        flat_fovea = np.mean(self._wm_fovea, axis=0)
        flat_peripheral = np.mean(self._wm_peripheral, axis=0)
        flat_gaze = np.mean(self._wm_gaze, axis=0)
        pfc_observation = { "fovea": flat_fovea, "peripheral": flat_peripheral, "gaze": flat_gaze }

#    pfc_observation = what_where_obs_dict
#    pfc_observation = self._wm # what_where_obs_dict
    # print("======> Agent: bg_action", bg_action)




    return pfc_observation, pfc_action
