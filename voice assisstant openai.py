import openai
import pyttsx3
import speech_recognition as sr
import random

#set OpenAi key

openai.api_key ="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"
model_id= 'gpt-3.5-turbo'

#Initialize the text -to -speech engine
engine= pyttsx3.init()

#change speech rate

engine.setProperty('rate',180)

#get the available

voices= engine.getProperty('voices')

#choose a voice based on the voice id
engine.setProperty('voice', voices[0].id)

#counter just for rhe interacting purpose 
interaction_counter=0

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except:
            print("")
           # print("skipping unknown error")
           
           
def ChatGPT_conversation(conversation):
    response= openai.ChatCompletion.create(
        model = model_id,
        messages = conversation
    )
    
    api_usage = response['usage']
    print('Total token consumed :{0}'.format(api_usage['total_tokens']))
    conversation.append({'role': response.choices[0].message.role,'content':response.choices[0].message.content})
    return conversation

def speak_text(text):
    engine.say(text)
    engine.runAndWait()
    
#starting conversation

conversation =[]
conversation.append({'role': 'user','content':'Please, Act like friday AI form Iron man, make a 1 sentence phrase introducing yourself without saying something that sound like this chat its already'

})
conversation =ChatGPT_conversation(conversation)
print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))
speak_text(conversation[-1]['content'].strip())

def activate_assistant():
    starting_chat_phrase =["Yes sir , how may I assist you ?",
                           "Yes,What can I do for you?",
                           "How can I help you , sir ?",
                           "Friday here , how can I help you today?,"
                           "Yes,What can I do for you today?,"
                           "Yes sir, What's on your mind?",
                           "Friday ready to assist , what can I do for you?",
                           "At you command, sir. How may I help you today?",
                           "Yes, sir .How may I be of assistance to you right now?",
                           "Yes boss, I'm listening.What can I do for you , sir?",
                           "how can i assist you today, sir?",
                           "Yes, sir . How can I make your day easier ?",
                           "Yes boss , What's the plan?",
                           "Yes, What's on your mind ,sir?"]
    continued_chat_phrases= ["yes ","yes,sir","yes,boss","I'm all ears"]
    random_chat =" "
    if(interaction_counter==1):
        random_chat = random.choice(starting_chat_phrase)
    else:
        random_chat = random.choice(continued_chat_phrases)
        
    return random_chat





def append_to_log(text):
    with open("chat_log.txt","a") as f:
        f.write(text+ "\n")
        
while True:
    #wait for user to say "siri"
    
    print("Say 'Friday' to start ....")
    recognizer =sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            transcription =recognizer.recognize_google(audio)
            if "siri" in transcription.lower():
                interaction_counter+=1
                
                #record audio
                filename ="input.wav"
                
                readyTowork =activate_assistant()
                speak_text(readyTowork)
                print(readyTowork)
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    source.pause_threshold=1
                    audio = recognizer.listen(source,phrase_time_limit=None, timeout=None)
                    with open(filename, "wb") as f:
                        f.write (audio.get_to_wav_data())
                        
                        #transcribe audio to text
                        
                text = transcribe_audio_to_text(filename)
                
                if text:
                    print(f"you said:{text}")
                    append_to_log(f"You: {text}\n")
                    
                    #generate responed using the chatGpt
                    
                    print(f"Friday says:{conversation}")
                    
                    prompt =text
                    conversation.append({'role':'user','content':prompt})
                    conversation =ChatGPT_conversation(conversation)
                    print('{0}:{1}\n',format(conversation[-1]['role'].strip(), conversation[-1]['content']))
                    
                    append_to_log(f"Friday: {conversation[-1]['content'].strip()}\n")
                    
                    #read response using the text to speech
                    
                    speak_text(conversation[-1]['content'].strip())
                    
        except Exception as e:
            continue
            
            #print("An error occured : {}".format(e))