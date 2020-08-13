import json 
import markovify
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

markov_chain = None

def load_markov_chain():
    global markov_chain
    with open('Markov_SG_Subreddit_Politics.json', 'r') as f:
        model_json = json.load(f)
        
    markov_chain = markovify.Text.from_json(model_json)


def start(update, context):
    text = markov_chain.make_short_sentence(280)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
	
def respond(update, context):
    msg = update.message.text
    words = msg.split(' ')
    try:
        text = markov_chain.make_sentence(tuple(words))
    except KeyError:
        text = markov_chain.make_short_sentence(280)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def main():
    load_markov_chain()

    with open('env.txt', 'r') as f:
        API_TOKEN = f.read().split('=')[1].strip()
    
    updater = Updater(token=API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    respond_handler = MessageHandler(Filters.text & (~Filters.command), respond)
    dispatcher.add_handler(respond_handler)

    updater.start_polling()

if __name__=='__main__':
    main()