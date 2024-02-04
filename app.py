from flask import Flask, session, render_template, Response, request, request, url_for, flash, redirect, jsonify
from extract_paragraphs import *
import re

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

appName = "Journey"

pages = split_pdf("harrypotter.pdf")

os.environ["OPENAI_API_KEY"] = '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'
openai.api_key = os.getenv("OPENAI_API_KEY")

# book_text = parser.from_file('harrypotter.pdf')

# with open("book.txt", "w+") as f:
#     f.write(" ")
#     json.dump({"book": book_text}, f)\

with open('book.txt', encoding='utf-8') as f:
        book_text = json.load(f)
        book_text = book_text["book"]["content"]
        book_text = ' '.join(book_text.split())

def parseStory(send_text, roleplaying, character, prompt):
    input = book_text[0:3000]

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

    context = send_text
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
    response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are helping us find out who the user is talking to from the book. Give only the first and last name of the character, only give the name and nothing else. If the user is not talking to a real character, say 'No character found!' and nothing else. Don't say anything except for the first and last name."},
        {"role": "assistant", "content": "The book is " + book_name},
        {"role": "user", "content": "the user says: " + prompt + ". Who is the user talking to?"}
    ]
    ).choices[0].message.content

    response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You will help us find how a character would view the user as another character"},
        {"role": "assistant", "content": "The book is " + book_name + ". The reader is at this stage of the story: " + stage + ". The user is roleplaying as " + roleplaying + " and we want to know how " + character + " would feel about the user's character."},
        {"role": "user", "content": "Give a one very short sentence response that describes exactly how " + character + " feels about " + roleplaying + ". Do not include hateful or extreme emotions. Be children-friendly with your answer. If the user is roleplaying as a character outside the book, such as themselves, then always give a positive response."}
    ]
    ).choices[0].message.content

    feeling = response

    response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You will roleplay as " + character + " in " + book_name + " to respond to the user at a specified part of the story: " + stage + ". If " + roleplaying + " and " + character + " are the same person, then give a monologue from their perspective."},
        {"role": "assistant", "content": "The book is " + book_name + ". The reader is at this stage of the story: " + stage + ". The user is roleplaying as " + roleplaying + ". " + character + " feels this way towards " + roleplaying + ": " + feeling},
        {"role": "user", "content": "Give a response to " + roleplaying + " saying '" + prompt + "' to " + character + ". The response is what the character you are roleplaying as would say at this point in the story. Make this one to three sentences response. Do not mention your own name in the response, and stay in character. Always stay in character even if you cannot answer the question fully. Only give the sentence that the character says, do not add quotation marks. When addressing the user, address them as who they are and not as a random character. Respond according to how " + character + " feels about " + roleplaying + ", for example if they are friendly then be friendly, and be unfriendly if the feeling is unfriendly. The response should be in first-person perspective from " + character + " answering to user as " + roleplaying + " Always. Always and only provide the reply from " + character + ". If you cannot provide a response, then just say you have no opinions on this topic or you have no interest to respond. If the story has not progressed enough to have a lore-friendly answer, then say no opinions on this matter. If" + roleplaying + "is themselves or someone not in the book, then be honest and give a good answer."}
    ]
    ).choices[0].message.content # If " + character + "is friendly towards " + roleplaying + " then be friendly, if not friendly then be act according to how you feel

    try:
        response = re.findall('"(\D+)"', response)[0]
    except:
        response = response

    return response

def getBackground(prompt_text):
    response = openai.images.generate(
      model="dall-e-3",
      prompt=prompt_text,
      size="1024x1024",
      quality="standard",
      n=1,
    )

    return response.data[0].url

def getNarratorResponse(send_text, roleplaying, character, prompt):
    input = book_text[0:3000]

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

    context = send_text
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
    # stage = response
    # print("GPT thinks the stage is at: ", stage)
    # response = openai.chat.completions.create(
    # model="gpt-3.5-turbo",
    # messages=[
    #     {"role": "system", "content": "You are helping us find out who the user is talking to from the book. Give only the first and last name of the character, only give the name and nothing else. If the user is not talking to a real character, say 'No character found!' and nothing else. Don't say anything except for the first and last name."},
    #     {"role": "assistant", "content": "The book is " + book_name},
    #     {"role": "user", "content": "the user says: " + prompt + ". Who is the user talking to?"}
    # ]
    # ).choices[0].message.content

    # response = openai.chat.completions.create(
    # model="gpt-3.5-turbo",
    # messages=[
    #     {"role": "system", "content": "You will help us find how a character would view the user as another character"},
    #     {"role": "assistant", "content": "The book is " + book_name + ". The reader is at this stage of the story: " + stage + ". The user is roleplaying as " + roleplaying + " and we want to know how " + character + " would feel about the user's character."},
    #     {"role": "user", "content": "Give a one very short sentence response that describes exactly how " + character + " feels about " + roleplaying + ". Do not include hateful or extreme emotions. Be children-friendly with your answer. If the user is roleplaying as a character outside the book, such as themselves, then always give a positive response."}
    # ]
    # ).choices[0].message.content
    #
    # feeling = response
    #
    # print(character + " feels this way towards the user:", feeling)

    # response = openai.chat.completions.create(
    # model="gpt-3.5-turbo",
    # messages=[
    #     {"role": "system", "content": "You will roleplay as " + character + " in " + book_name + " to respond to the user at a specified part of the story: " + stage + ". If " + roleplaying + " and " + character + " are the same person, then give a monologue from their perspective."},
    #     {"role": "assistant", "content": "The book is " + book_name + ". The reader is at this stage of the story: " + stage + ". The user is roleplaying as " + roleplaying + ". " + character + " feels this way towards " + roleplaying + ": " + feeling},
    #     {"role": "user", "content": "Give a response to " + roleplaying + " saying '" + prompt + "' to " + character + ". The response is what the character you are roleplaying as would say at this point in the story. Make this one to three sentences response. Do not mention your own name in the response, and stay in character. Always stay in character even if you cannot answer the question fully. Only give the sentence that the character says, do not add quotation marks. When addressing the user, address them as who they are and not as a random character. Respond according to how " + character + " feels about " + roleplaying + ", for example if they are friendly then be friendly, and be unfriendly if the feeling is unfriendly. The response should be in first-person perspective from " + character + " answering to user as " + roleplaying + " Always. Always and only provide the reply from " + character + ". If you cannot provide a response, then just say you have no opinions on this topic or you have no interest to respond. If the story has not progressed enough to have a lore-friendly answer, then say no opinions on this matter. If" + roleplaying + "is themselves or someone not in the book, then be honest and give a good answer."}
    # ]
    # ).choices[0].message.content # If " + character + "is friendly towards " + roleplaying + " then be friendly, if not friendly then be act according to how you feel

    narratorResponse = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You will roleplay as a narrator in " + book_name + " to respond to the user at a specified part of the story: " + stage},
        {"role": "assistant", "content": "The book is " + book_name + ". The reader is at this stage of the story: " + stage},
        {"role": "user", "content": "Being an omniscient narrator, give a response to the user saying '" + prompt + ". The response is what an omniscient narrator would say" + ". Make this one to four sentences response. Do not mention that you are an omniscient narrator in the response, and be objective, providing no bias, and only the response. The response should not provide story details that exist beyond the stage in the story. You may break this limitation if the user specifically asks about it. Only give the sentence that a omniscient narrator would say. When referencing the user, refer to them as who they are and not as a random character using the third-person perspective. The response should be in third-person perspective from an omniscient narrator answering to user always. Always and only provide the reply from as an omniscient narrator. If you cannot provide a response, then just say you have no opinions on this topic and advise the user to research on their own to find the answer."}
    ]
    ).choices[0].message.content

    print(narratorResponse)
    response = narratorResponse

    # narratorQuestion = openai.chat.completions.create(
    # model="gpt-3.5-turbo",
    # messages=[
    #     {"role": "system", "content": "You will roleplay as a narrator in a story to help us generate a question prompt which the user will ask a character in the story."},
    #     {"role": "assistant", "content": "The book is " + book_name + ". The reader is at this stage of the story: " + stage + ". The user is roleplaying as " + roleplaying + " and is conversing with " + character},
    #     {"role": "user", "content": "Give a one very short prompt that allows the user to deeply think about " + character +"'s circumstances, with respect to the stage, in the story. Ensure that the response is one that " + roleplaying + "would honestly ask " + character + " in the first person. Do not include hateful or extreme emotions. Be children-friendly with your answer. If the user is roleplaying as a character outside the book, such as themselves, then ask a question that avoids any bias and is very objective. Almost as if the user were only observing. Answer only with the prompt question in quotations. No preface, no follow up, only the question."}
    # ]
    # ).choices[0].message.content

    try:
        response = re.findall('"(\D+)"', response)[0]
        # narratorQuestion = re.findall('"(\D+)"', narratorQuestion)[0]
    except:
        response = response
        # narratorQuestion = narratorQuestion

    # print("--------------NARRATOR QUESTION-------------------")
    # print(narratorQuestion)
    # print("--------------------------------------------------")

    return response

def getCharacters(send_text):
    input = book_text[0:3000]

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

    context = send_text
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

    response = openai.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are helping us find which characters have showed up in the book at this point in the story."},
        {"role": "assistant", "content": "The book is " + book_name + ". The reader is at this stage of the story: " + stage},
        {"role": "user", "content": "The user has just read up to: " + context + ". Give the list of characters present at this stage of the story only, meaning that characters that have left the scene but may come back later do not count toward this list. Give the list in the format of a Python list, which is the list of names separated by commas. Each name is only one word and is capitalized. Also output whether or not a list was successfully generated in the format of True or False. Do not surround Python list elements with quotation marks. The output should be in the format of [list], True or False for list check. Provide only the output and nothing else extra such as words or sentences. ONLY provide the output in the format asked."}
      ]
    ).choices[0].message.content

    try:
        response = re.findall('"(\D+)"', response)[0]
    except:
        response = response

    print("LIST OF CHARS", response)
    return response

def getBackgroundPrompt(send_text):
    input = book_text[0:3000]

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

    context = send_text
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

    response = openai.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are helping us to describe the visuals of a scene for usage in image generation."},
        {"role": "assistant", "content": "The book is " + book_name + ". The reader is at this stage of the story: " + stage},
        {"role": "user", "content": "The user has just read up to: " + context + ". Give a one sentence description of the visuals of scene ONLY, do not add anything extra like 'something depicts' or 'this scene looks like'. We need it for image generation so we need this to be a prompt for that. Focus on the setting of the scene and not the characters or situation, we want the background only."}
      ]
    ).choices[0].message.content

    try:
        response = re.findall('"(\D+)"', response)[0]
    except:
        response = response

    print("IMG-PROMPT", response)

    return response

@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html', appName=appName, pages=pages)

@app.route('/get_response', methods=['GET'])
def get_response():
    if request.method == 'GET':
        mode = request.args["mode"]
        if mode == "response":
            prompt = request.args["msg"]
            char = request.args["character"]
            rp = request.args["roleplaying"]
            context = request.args["context"]

            print(prompt)
            print(char)
            print(rp)
            print(context)

            if (char == "Narrator"):
                result = getNarratorResponse(context, rp, char, prompt)
                print("Gave Narrator Response")
            else:
                result = parseStory(context, rp, char, prompt)
            print(result)
        elif mode == "background":
            context = request.args["context"]
            result = getBackground(getBackgroundPrompt(context))
        elif mode == "chars":
            context = request.args["context"]
            result = getCharacters(context)

        return jsonify(result)

if __name__ == "__main__":
  app.run(debug=True)
