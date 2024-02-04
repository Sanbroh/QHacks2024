from tika import parser # pip install tika
import os
import openai
import json
import re

os.environ["OPENAI_API_KEY"] = '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'
openai.api_key = os.getenv("OPENAI_API_KEY")

# book_text = parser.from_file('hamlet.pdf')
#
# with open("book.txt", "w+") as f:
#     f.write(" ")
#     json.dump({"book": book_text}, f)

with open('book.txt') as f:
    book_text = json.load(f)
    book_text = book_text["book"]["content"]
    book_text = ' '.join(book_text.split())

input = book_text[0:5000]

response = openai.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are helping us to find the name of the book based on the prompt."},
    {"role": "assistant", "content": input},
    {"role": "user", "content": "What book is this? Give only the book title and nothing else."}
  ]
).choices[0].message.content

book_name = response
print("Book Name: ", book_name)

context = book_text[225000:226000]
print("Stage of the reader: ", context)

response = openai.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are helping us find the which part of the book the user is at based on the prompt."},
    {"role": "assistant", "content": "The book is " + book_name},
    {"role": "user", "content": "The user has just read up to: " + context + ". Which part of the book is this? Give a one sentence summary that you can understand if I were to ask you to describe the story later, so make it concise and understandable. Only describe this scene."}
  ]
).choices[0].message.content

stage = response
print("GPT thinks the stage is at: ", stage)

# response = openai.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are helping us find which characters have showed up in the book at this point in the story."},
#     {"role": "assistant", "content": "The book is " + book_name + ". The reader is at this stage of the story: " + stage},
#     {"role": "user", "content": "The user has just read up to: " + context + ". Give the list of characters present at this stage of the story only, meaning that characters that have left the scene but may come back later do not count toward this list. Give the list in the format of a Python list, which is the list of names separated by commas."}
#   ]
# ).choices[0].message.content

response = openai.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are helping us to describe the visuals of a scene for usage in image generation."},
    {"role": "assistant", "content": "The book is " + book_name + ". The reader is at this stage of the story: " + stage},
    {"role": "user", "content": "The user has just read up to: " + context + ". Give a one sentence description of the visuals of scene ONLY, do not add anything extra like 'something depicts' or 'this scene looks like'. We need it for image generation so we need this to be a prompt for that. Focus on the setting of the scene and not the characters or situation, we want the background only."}
  ]
).choices[0].message.content

# prompt = "How did you get the elder wand?"
#
# response = openai.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are helping us find out who the user is talking to from the book. Give only the first and last name of the character, only give the name and nothing else. If the user is not talking to a real character, say 'No character found!' and nothing else. Don't say anything except for the first and last name."},
#     {"role": "assistant", "content": "The book is " + book_name},
#     {"role": "user", "content": "the user says: " + prompt + ". Who is the user talking to?"}
#   ]
# ).choices[0].message.content
#
# roleplaying = "Severus Snape" # Themselves and not a character in the book
# print("The user is roleplaying as ", roleplaying)
#
# character = "Dumbledore"
# print("The user is talking to ", character)
#
# print(roleplaying + " says to " + character + ": ", prompt)
#
# response = openai.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You will help us find how a character would view the user as another character"},
#     {"role": "assistant", "content": "The book is " + book_name + ". The reader is at this stage of the story: " + stage + ". The user is roleplaying as " + roleplaying + " and we want to know how " + character + " would feel about the user's character."},
#     {"role": "user", "content": "Give a one very short sentence response that describes exactly how " + character + " feels about " + roleplaying + ". Do not include hateful or extreme emotions. Be children-friendly with your answer. If the user is roleplaying as a character outside the book, such as themselves, then always give a positive response."}
#   ]
# ).choices[0].message.content
#
# feeling = response
# print(character + " feels this way towards the user: ", feeling)
#
# response = openai.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You will roleplay as " + character + " in " + book_name + " to respond to the user at a specified part of the story: " + stage + ". If " + roleplaying + " and " + character + " are the same person, then give a monologue from their perspective."},
#     {"role": "assistant", "content": "The book is " + book_name + ". The reader is at this stage of the story: " + stage + ". The user is roleplaying as " + roleplaying + ". " + character + " feels this way towards " + roleplaying + ": " + feeling},
#     {"role": "user", "content": "Give a response to " + roleplaying + " saying '" + prompt + "' to " + character + ". The response is what the character you are roleplaying as would say at this point in the story. Make this one to three sentences response. Do not mention your own name in the response, and stay in character. Always stay in character even if you cannot answer the question fully. Only give the sentence that the character says, do not add quotation marks. When addressing the user, address them as who they are and not as a random character. Respond according to how " + character + " feels about " + roleplaying + ", for example if they are friendly then be friendly, and be unfriendly if the feeling is unfriendly. The response should be in first-person perspective from " + character + " answering to user as " + roleplaying + " Always. Always and only provide the reply from " + character + ". If you cannot provide a response, then just say you have no opinions on this topic or you have no interest to respond. If the story has not progressed enough to have a lore-friendly answer, then say no opinions on this matter. If" + roleplaying + "is themselves or someone not in the book, then be honest and give a good answer."}
#   ]
# ).choices[0].message.content # If " + character + "is friendly towards " + roleplaying + " then be friendly, if not friendly then be act according to how you feel

# response = openai.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a DnD DM that is telling a story based on the book provided to you, and will mimic different characters in the book. You will help the user roleplay as a character (either as an existing character or roleplaying as themselves) in the book."},
#     {"role": "assistant", "content": input},
#     {"role": "user", "content": "The user is roleplaying as " + roleplaying + ". " + "The user is currently on this page, roleplay starts here at this point of the story: " + stage + ". Here is what the user is saying: " + prompt + ". If the story has not yet reached this character tell them that they need to keep reading as the narrator. If the user is asking a character a question, respond to them as that character unless they are roleplaying the character."}
#   ]
# ).choices[0].message.content
try:
    response = re.findall('"(\D+)"', response)[0]
except:
    response = response

print("'" + response + "'")
