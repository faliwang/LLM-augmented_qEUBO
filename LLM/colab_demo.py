import os
import json
import math
import openai
from openai import OpenAI
import pandas

import re

from IPython import get_ipython
from IPython.utils.capture import capture_output
from LLM_utils import *

ipython = get_ipython() # run generated code

pattern = re.compile(r'```python\n(.*?)```', re.DOTALL)  # extract code from llm generation


problem2 = """
  At a restaurant, each adult meal costs $5.46 and kids eat free. If a group of
  1500 people came in and 749 were kids, what is the natural log of much
  would it cost for the group to eat?
  """

ans, ans_full = solve_problem_with_executable_2step(problem2)
for i in range(0,10):
    try:
        print(ans)
        print(eval(ans))
        break
    except Exception as e:
        print(e)
        ans, ans_full = solve_problem_with_executable_2step_recourse(problem2, ans, e)
        
# template = '''
# Setting: You are an autonomous agent designed to assist users in performing
# operations on pandas DataFrame using Python.

# Your goal is to understand the user's request, and provide Python code to
# fulfill the request.

# Your output will be directly executed in python, you need to help debug and
# modify the original answer if there is an error during execution.
# '''

# prompt_create = '''
# You need to write code to create a example of pandas dataframe include the name,
# age, and science score for 20 students in high school.

# The dataframe will be named DF1.

# Your output will be directly executed in python.

# The final output should be formulated as the executable code, as your output
# will be directly executed in python.

# '''

# error = -1
# try_times = 0

# code_total = ''
# code = ''
# results = []

# while try_times < 10:
#     if try_times == 0:
#         code = get_openai_response(prompt_create, template)
#     elif error == -1:     # no error
#         print("Regenerate code")
#         code = prompt_with_error(prompt_create, code_total, result, template)
#     else:                 # with error
#         print("Modify code")
#         code = prompt_with_error(prompt_create, code_total, err_result, template)
#         error = -1

#     try_times += 1


#     print("code: ",code)
#     code_snippets = pattern.findall(code)

#     if len(code_snippets) == 0:
#         exe_code = code
#     else:
#         exe_code = code_snippets[0].strip()

#     print("exe_code: ", exe_code)
#     with capture_output() as captured:
#         exe_result = ipython.run_cell(exe_code)
#         if exe_result.error_in_exec == None: # no error during running
#             result = captured.stdout
#             results.append(result)
#             code_total = code_total + '\n' + exe_code
#         else:  # error happen during running
#             err_result = exe_result
#             results.append(err_result)
#             error = 1


#     if exe_result.error_in_exec == None:
#         print(f'\n Total code: {code_total} \n')
#         break

# print(DF1)