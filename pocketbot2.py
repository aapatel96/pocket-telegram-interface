##import urllib
##import telegram
##import tweepy
##
##bot = telegram.Bot(token='297497718:AAFEZdRe7tbkt6z2Brb4tepPPCn5uNkrLlA')
##
##updates = bot.getUpdates()
##print updates

'''
Have to change the set function to new reading Function so that you give /newReading <dueDate> <reading>
and it splits the readings and starts sending messages
'''

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job, JobQueue, RegexHandler,ConversationHandler,CallbackQueryHandler
import telegram.replykeyboardmarkup
import telegram.keyboardbutton
import telegram.ext
import logging
import json
import pocket
from pocket import Pocket
import os
import random
import time
import urllib2
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)




users = []
consumer_key="67229-58499186bd836a77ac726d5f"
redirect_uri="https://telegram.me/getpocket_bot"
request_token = Pocket.get_request_token(consumer_key=consumer_key, redirect_uri=redirect_uri)
print request_token

done_keyboard = telegram.replykeyboardmarkup.ReplyKeyboardMarkup([[telegram.KeyboardButton("done")]], resize_keyboard=True, one_time_keyboard=True)
random_listf_keyboard = telegram.replykeyboardmarkup.ReplyKeyboardMarkup([[telegram.KeyboardButton("random")],[telegram.KeyboardButton("listf")]], resize_keyboard=True)
pass_keyboard = telegram.replykeyboardmarkup.ReplyKeyboardMarkup([[telegram.KeyboardButton("pass")]], resize_keyboard=True)
inlineNextKeyboard1 = InlineKeyboardMarkup([[InlineKeyboardButton("next", callback_data='1')]])
inlineNextKeyboard2 = InlineKeyboardMarkup([[InlineKeyboardButton("previous", callback_data='2'),InlineKeyboardButton("next", callback_data='1')]])
inlineNextKeyboard3 = InlineKeyboardMarkup([[InlineKeyboardButton("previous", callback_data='2')]])


# Enable logging


CONFIRM,ADD,TYPING_CHOICE=range(3)


#classes

class User:
    def __init__(self,user_id):
        self.currentTask = None
        self.currentURL= None
        self.auth_url =None
        self.user_id = user_id
        self.user_credentials = None
        self.access_token= None
        self.currentList = None


class listStatus:
    def __init__(self):
        self.list= None
        self.currentIndex = None
        
    
class special:
    def __init__(self,uid,message):
        self.message = message
        self.id = uid



def find_user(users, user_id):
    """
    Returns the user object with given user_id

    Args:
         users:   The list of user instances to search through.
         user_id: The ID of the user to find.

    Returns:
            The 'user' object with user_id.
    """
    for i in range(len(users)):
        if users[i].user_id == user_id:
            return users[i]

    return None




def start(bot, update):

    update.message.reply_text("Yo")
    auth_url = Pocket.get_auth_url(code=request_token, redirect_uri=redirect_uri)
    ##userfind.auth_url= auth_url
    ##print auth_url
    update.message.reply_text("Please authorise the bot at the following url"+"\n"+"\n"+auth_url,disable_web_page_preview=True)
    
    time.sleep(2)
    ##update.message.reply_text("come back here and hit done when you have finished authorisation",reply_markup=done_keyboard)
    x = 1
    count = 0
    while x == 1:
        count = count +1
        print x
        try:
            user_credentials = Pocket.get_credentials(consumer_key=consumer_key, code=request_token)
            print user_credentials
            userfind.user_credentials =user_credentials
            
            print "x"
            x = 2
            print x
            print "hi"  
        except:
            continue
    print "hi"

    users.append(User(update.message.from_user.id))
    userfind = find_user(users,update.message.from_user.id)
    userfind.access_token =user_credentials['access_token']
    print userfind.access_token
    update.message.reply_text("You are all set! Try pressing random below to get a random article or list to skim your libray",reply_markup=random_listf_keyboard)
    
    return ConversationHandler.END

    
def help(bot, update):
    update.message.reply_text(' newtask <taskname:priority:duedate> to create a task'+ '\n'
                              + ' mytasks to show tasks'+'\n'+ ' newhabit <habitname:priority>'+'\n'+ ' myhabits to show tasks'+'\n'+ ' deltask <taskid> to delete task by task id (you can find this out using /mytasks command)'
                              +'fintask ,<taskid> to delete task by task id (you can find this out using /mytasks command'+ '\n' +'delthabit <habitid> to delete habit by habit id (you can find this out using /myhabits command)' +"/help to get command list")

def pressDone(bot,update):
    update.message.reply_text("Please press done",reply_markup=done_keyboard)
    return CONFIRM
def stringEight(userfind):
    string = ""
    startindex = userfind.currentList.currentIndex
    endindex =startindex+8
    print "++++++"
    print startindex

    if endindex >= len(userfind.currentList.list):
        endindex = len(userfind.currentList.list)
    print endindex
    print "++++++"
    print len(userfind.currentList.list)
    for i in xrange(startindex,endindex):
        print userfind.currentList.list[i].values()[17]
        print userfind.currentList.list[i].values()[11]
        print "============"
        if len(userfind.currentList.list[i].values()) == 20:
            title = userfind.currentList.list[i].values()[17].encode('utf-8').strip()
            url = userfind.currentList.list[i].values()[11].encode('utf-8').strip()           
            string = string +title+"\n"+url+"\n"+"\n"
        if len(userfind.currentList.list[i].values()) == 19:
            title = userfind.currentList.list[i].values()[16].encode('utf-8').strip()
            url = userfind.currentList.list[i].values()[10].encode('utf-8').strip()           
            string = string +title+"\n"+url+"\n"+"\n"
    if len(string) == 0:
        return None
    return string
def listf(bot,update):
    userfind = find_user(users,update.message.from_user.id)
    if userfind == None:
        update.message.reply_text("Please type /start and then resend command")
    pocket_instance = pocket.Pocket(consumer_key, userfind.access_token)
    r = Pocket.get(pocket_instance,state="unread",sort="newest")
    x =json.dumps(r[0])
    #print type(x)
    data = json.loads(x)
    #print type(data)
    dataValues = data.values()
    #print len(dataValues[4])
    articlesList = dataValues[4]
    ##print(articlesList.values())
    
    list2add = listStatus()
    list2add.list = articlesList.values()
    #print list2add.list[0].values()[11]
    #print list2add.list[0].values()[17]
    list2add.currentIndex = 0
    userfind.currentList = list2add
    userfind.currentList.currentIndex = 0

    string =stringEight(userfind)
    if string == None:
        update.message.reply_text("actually...you don't have shit in your pocket :P")
    if len(userfind.currentList.list) <=8:
         update.message.reply_text(string, disable_web_page_preview=True)
         return
    update.message.reply_text(string, disable_web_page_preview=True,reply_markup=inlineNextKeyboard1)

    
def nextButton(bot,update):
    query = update.callback_query.id
    queryObj = update.callback_query
    queryData = update.callback_query.data
    mid = queryObj.message.message_id
    print query
    print queryObj
    userfind = find_user(users,queryObj.from_user.id)
    print userfind
    if userfind == None:
        queryObj.message.reply_text("Please type /start and then resend command")
        return ConversationHandler.END
    print "hi"
    print queryData
    print str(queryData)
    if str(queryData) == "2":
        print "reached branch"
        userfind.currentList.currentIndex = userfind.currentList.currentIndex-8
        string = stringEight(userfind)
    if str(queryData) == "1":
        print "reached branch"
        userfind.currentList.currentIndex = userfind.currentList.currentIndex+8
        string = stringEight(userfind)
        
    if userfind.currentList.currentIndex+8 >len(userfind.currentList.list):
        keyboard = inlineNextKeyboard3
    elif userfind.currentList.currentIndex-8 <0:
        keyboard = inlineNextKeyboard1
    else:
        keyboard = inlineNextKeyboard2
        
##    x = "<b>"+userfind.currentList[userfind.currentIndex].values()[1].upper()+"</b>"+"\n\n"+userfind.currentList[userfind.currentIndex].values()[0]+"\n\n"+userfind.currentList[userfind.currentIndex].values()[2]

    bot.edit_message_text(text=string,
                      chat_id=queryObj.message.chat_id,
                      message_id=mid, disable_web_page_preview=True)
    bot.edit_message_reply_markup(chat_id =queryObj.message.chat_id,message_id=mid,reply_markup =keyboard,parse_mode='HTML')
    
def confirm(bot,update):
    userfind = find_user(users,update.message.from_user.id)
    if userfind == None:
        update.message.reply_text("Please type /start and then resend command")
        return ConversationHandler.END
    try:
        user_credentials = Pocket.get_credentials(consumer_key=consumer_key, code=request_token)
        print user_credentials
        userfind.user_credentials =user_credentials
        userfind.access_token =user_credentials['access_token']
        update.message.reply_text("You are all set! Try pressing random below to get a random article or list to skim your libray",reply_markup=random_listf_keyboard)
        return ConversationHandler.END
    except:
        update.message.reply_text("Please authorise this bot first:"+"\n"+"\n"+userfind.auth_url,reply_markup=done_keyboard)
        return CONFIRM

    us
def randomL(bot,update):
    userfind = find_user(users,update.message.from_user.id)
    if userfind == None:
        update.message.reply_text("Please type /start and then resend command")
    pocket_instance = pocket.Pocket(consumer_key, userfind.access_token)
    r = Pocket.get(pocket_instance,state="unread")
    x =json.dumps(r[0])
    data = json.loads(x)
    dataValues = data.values()
    articlesList = dataValues[4]
    randomInt =random.randint(0,len(dataValues[4])-1)
    update.message.reply_text(articlesList.values()[randomInt]["resolved_url"],reply_markup=random_listf_keyboard)
    fileObj = open("json.txt","w")
    fileObj.write(x)
    

def checkText(bot,update):
    userfind = find_user(users,update.message.from_user.id)
    if userfind == None:
        update.message.reply_text("Please type /start and then resend command")
    
    try:
        urllib2.urlopen(str(update.message.text))
    except:
        update.message.reply_text("not a valid url")
        return ConversationHandler.END

    userfind.currentURL = update.message.text
    update.message.reply_text("Are there any tags for this url?(split them with commas)")
    update.message.reply_text("You can hit pass if there are none",reply_markup=pass_keyboard)
    return ADD
def parsetagsadd(bot,update):
    userfind = find_user(users,update.message.from_user.id)
    if userfind == None:
        update.message.reply_text("Please type /start and then resend command")
    tags = update.message.text.split(",")
    tagsPure = []
    for i in tags:
        tag = i
        if i[-1] == " ":
            tag = tag[:-1]
        if i[0] == " ":
            tag = tag[1:]         
        tagsPure.append(tag)
    tagsPure = list(set(tagsPure))
    print tagsPure
    tagsStr= ",".join(tagsPure)
    pocket_instance = pocket.Pocket(consumer_key, userfind.access_token)
    pocket_instance.add(userfind.currentURL,tags=tagsStr)
    update.message.reply_text("Article added!!")
    
    return ConversationHandler.END
    
    
def passf(bot,update):
    userfind = find_user(users,update.message.from_user.id)
    if userfind == None:
        update.message.reply_text("Please type /start and then resend command")
    update.message.reply_text("All good! Your article was saved")
    pocket_instance = pocket.Pocket(consumer_key, userfind.access_token)
    pocket_instance.add(userfind.currentURL)
    update.message.reply_text("All good! Your article was saved")
    return ConversationHandler.END
    

def cancel(bot, update):
    print "r"
    userfind = find_user(users,update.message.from_user.id)
    if userfind == None:
        update.message.reply_text("Please type /start and then resend command")
        return ConversationHandler.END
    logger.info("User %s canceled the conversation." % update.message.from_user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')
    userfind.currentTask = None
    return ConversationHandler.END
    
 
def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    TOKEN = "390620520:AAExWtZNavGPtKGiGrEA2rsqcsFU4-NfWKg"
    updater = Updater(TOKEN)
    PORT = int(os.environ.get('PORT', '5000'))
    # job_q= updater.job_queue

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(RegexHandler('^random$', randomL))
    #task handling
    
##    dp.add_handler(RegexHandler('^unread$', unread))
##    dp.add_handler(RegexHandler('^archive$', archive))
##    dp.add_handler(RegexHandler('^archive$', archive))
    dp.add_handler(RegexHandler('^list$', listf))
    dp.add_handler(RegexHandler('^top five$', listf))
    dp.add_handler(CallbackQueryHandler(nextButton))

    onboarding = ConversationHandler(
    entry_points=[CommandHandler("start",start)],
    states={


        CONFIRM: [RegexHandler('^(done)$',
                                confirm),
                    MessageHandler(Filters.text,
                                   pressDone)
                  ],
        
        TYPING_CHOICE: [RegexHandler('^cancel$', cancel),
                        MessageHandler(Filters.text,
                               start),                        
                ],     
    },

    fallbacks=[RegexHandler('^cancel$', cancel)]
    )

    dp.add_handler(onboarding)

    add_article = ConversationHandler(
    entry_points=[MessageHandler(Filters.text,checkText)],
    states={


        ADD: [RegexHandler('^(pass)$',
                                passf),
                    MessageHandler(Filters.text,
                                   parsetagsadd)
                  ],
        
        TYPING_CHOICE: [RegexHandler('^cancel$', cancel),
                        MessageHandler(Filters.text,
                               start),                        
                ],     
    },

    fallbacks=[RegexHandler('^cancel$', cancel)]
    )

    dp.add_handler(add_article)

    

    #easter egg




    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
##    updater.start_webhook(listen="0.0.0.0",
##                      port=PORT,
##                      url_path=TOKEN)
##    updater.bot.set_webhook("https://smaugbot.herokuapp.com/" + TOKEN)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
