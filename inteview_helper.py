"""
This script will take a resume and a list of questions, and have gpt help the interviewee prepare for the interview,
by analyzing the question and the resume and coaching the interviewee on how to approach answering the question.
"""

import os
import sys
import json
from langchain.llms import OpenAI
from langchain import PromptTemplate

# This is the prompt template that will be used to generate the prompt for gpt
template = """
I am helping someone prepare for an interview. I have their resume and a question they will be asked. I will provide
a sample answer to the question a list of points they should cover in their answer. I will also provide a list of
points they should avoid in their answer. 

resume: {resume}

question: {question}
"""

prompt = PromptTemplate(template=template, input_variables=["resume", "question"])
llm = OpenAI(temperature=0.0, model_name="text-davinci-003")

# Load the questions
question_filename = "Data/Questions.txt"
with open(question_filename, "r") as f:
    # make a list with each line as an element
    question_list = f.readlines()
    # get rid of elements that don't begin with "*"
    question_list = [question for question in question_list if question[0] == "*"]

# Load the resume
resume_filename = "Data/Resume.txt"
response_filename = "Data/Response.json"
with open(resume_filename, "r") as f:
    resume = f.read()
responses = {}
# Get GPT response for each question in the list
for question in question_list:
    response = llm(prompt.format(resume=resume, question=question))
    print(f'Question: {question}\n')
    print(f'Response: {response}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
    responses[question] = response
    with open(response_filename, "w") as f:
        json.dump(responses, f, indent=4)
    # Save response to a well formatted text file
    with open("Data/Response.txt", "w") as f:
        for q, r in responses.items():
            f.write(f'Question: {q}\n')
            f.write(f'Response: {r}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')







