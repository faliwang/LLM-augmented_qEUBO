import openai
from openai import OpenAI

client = OpenAI(api_key = 'Your API key')


def get_openai_response(prompt, template, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
            model = model,
            # model = "gpt-4",
            # model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": template},
                {"role": "user", "content": prompt}
            ]
        )
    return response.choices[0].message.content


def solve_problem_base(problem_statement):
    #GPT is already tuned to solve such problems step-by-step, so we're instructing it not to.
    prompt = f"""The following is a math problem that needs to be solved:
      {problem_statement}.
      Do not solve it step by step but give the final answer.\n\n
      """
    #print(prompt)
    template = "You are a highly intelligent AI trained to solve reasoning problems and learn iteratively from feedback."
    response = get_openai_response(prompt, template, model="gpt-3.5-turbo")
    print(response)
    
    
def solve_problem_StepByStep(problem_statement):
    prompt = f"""The following is a math problem that needs to be solved:
    {problem_statement}.
      Please think step by step and answer the question with detailed
      explanations of each step involved in reaching the solution,
      and please give the final answer.\n\n
      """
    #print(prompt)
    template = "You are a highly intelligent AI trained to solve reasoning problems and learn iteratively from feedback."
    response = get_openai_response(prompt, template, model="gpt-3.5-turbo")
    print(response)


def solve_problem_with_executable(problem_statement):
    prompt = f"""The following is a math problem that needs to be solved:
        {problem_statement}.
        Please only output a formula executable that can be executed.
        Do not output any other text.
        If the formula uses functions such as sqrt, please use math.sqrt (python notation)
        \n\n
        """
    #print(prompt)
    template = "You are a highly intelligent AI trained to solve reasoning problems and learn iteratively from feedback."
    response = get_openai_response(prompt, template, model="gpt-3.5-turbo")
    return response
    #print(response)


def solve_problem_with_executable_2step(problem_statement):
    prompt = f"""The following is a math problem that needs to be solved:
        {problem_statement}.
        Please think step-by-step and return a formula that mirrors the steps.
        If the formula uses functions such as sqrt, please use math.sqrt (python notation)
        Do not use notation such as dollar signs, which are not python friendly.
        The final output should be formatted as:
        *** formula ***
        \n\n
        """
    #print(prompt)
    template = "You are a highly intelligent AI trained to solve reasoning problems and learn iteratively from feedback."
    full_response = get_openai_response(prompt, template, model="gpt-3.5-turbo")
    prompt2 = f"""Please extract out the terms in between two *** terms and
        only return that (do not include any other output):
        {full_response}"""
    response = get_openai_response(prompt2, template, model="gpt-3.5-turbo")
    return response, full_response
    #print(response)
    
    
def solve_problem_with_executable_2step_recourse(problem_statement, prev, issue):
    prompt = f"""The following is a math problem that needs to be solved:
        {problem_statement}.
        Please think step-by-step and return a formula that mirrors the steps.
        If the formula uses functions such as sqrt, please use math.sqrt (python notation)
        Do not use notation such as dollar signs, which are not python friendly.
        The final output should be formatted as:
        *** formula ***
        \n

        Your previous answer was: \"{prev}\", with had the following error: {issue}.
        """
    #print(prompt)
    template = "You are a highly intelligent AI trained to solve reasoning problems and learn iteratively from feedback."
    full_response = get_openai_response(prompt, template, model="gpt-3.5-turbo")
    prompt2 = f"""Please extract out the terms in between two *** terms and
        only return that (do not include any other output):
        {full_response}"""
    response = get_openai_response(prompt2, template, model="gpt-3.5-turbo")
    return response, full_response
    #print(response)
    
    
def prompt_with_error(prev_prompt, code, error_log, template):
    prompt_error_modify = f'''{prev_prompt}
    \n
    Your previous code is as follows:

    \n
    {code}
    \n

    After execution, the error log is as follows:

    \n
    {error_log}
    \n

    Please modify the previous code and regenerate the output.
    '''
    full_response = get_openai_response(prompt_error_modify, template, model = "gpt-4")


    return full_response


def prompt_with_prev_code(prev_prompt, code, result, template):
    prompt_error_modify = f'''{prev_prompt}
    \n
    Your previous code is as follows:

    \n
    {code}
    \n

    After execution, the result is as follows:

    \n
    {result}
    \n

    If the result is an error log, please modify the previous line of code and regenerate the output. If it is not an error log, please generate the next line of code.

    You need to formulate your output as only containing the executable python code.
    '''

    full_response = get_openai_response(prompt_error_modify, template, model = "gpt-4")


    return full_response