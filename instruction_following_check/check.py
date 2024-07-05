# coding=utf-8
# Copyright 2024 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Binary of evaluating instruction following. See README.md."""

import collections
import dataclasses
import json
import os
from typing import Dict, Optional, Sequence, Union

from absl import app
from absl import flags
from absl import logging

# import instructions_registry
from . import instructions_registry


# def test_instruction_following_strict(
def check_correctness_instruction_following(
    inp,
    # prompt_to_response,
    response,
):
  """Tests response to see if instrutions are followed."""
  #response = prompt_to_response[inp.prompt]
  instruction_list = inp['instruction_id_list']
  is_following_list = []

  for index, instruction_id in enumerate(instruction_list):
    instruction_cls = instructions_registry.INSTRUCTION_DICT[instruction_id]
    instruction = instruction_cls(instruction_id)

    instruction.build_description(**inp['kwargs'][index])
    args = instruction.get_instruction_args()
    if args and "prompt" in args:
      instruction.build_description(prompt=inp['question'])

    if response.strip() and instruction.check_following(response):
      is_following_list.append(True)
    else:
      is_following_list.append(False)

    return all(is_following_list)
#   return OutputExample(
#       key=inp.key,
#       instruction_id_list=inp.instruction_id_list,
#       prompt=inp.prompt,
#       response=response,
#       follow_all_instructions=all(is_following_list),
#       follow_instruction_list=is_following_list,
#   )


