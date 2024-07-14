# import os
# import openai
# from config import apikey

# openai.api_key = apikey

# response = openai.Completion.create(
#   model="gpt-3.5-turbo-16k",
#   prompt="what is the capital of france?",
#   temperature=1,
#   max_tokens=256,
#   top_p=1,
#   frequency_penalty=0,
#   presence_penalty=0
# )

# ans = response[0]["text"]
# print(ans)

def load_dict_from_file(filename):
    """Read key-value pairs from a file and return as a dictionary."""
    my_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            # Strip whitespace and split by the colon
            key, value = line.strip().split('?')
            my_dict[key] = value
    return my_dict

# Specify the filename
filename = 'software.txt'

# Load the dictionary from the file
my_dict = load_dict_from_file(filename)

# Print the loaded dictionary
# print(my_dict)

with open(filename, 'a') as f:
    f.write(f'hello?ask\n')

print(my_dict)
