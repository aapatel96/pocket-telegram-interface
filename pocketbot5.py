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
import pymongo


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


client = pymongo.MongoClient(os.environ['MONGODB_URI'])

db = client.get_default_database()

users = db['users']
lists = db['lists']

consumer_key="67229-58499186bd836a77ac726d5f"
redirect_uri="https://telegram.me/getpocket_bot"
request_token = Pocket.get_request_token(consumer_key=consumer_key, redirect_uri=redirect_uri)
print request_token

done_keyboard = telegram.replykeyboardmarkup.ReplyKeyboardMarkup([[telegram.KeyboardButton("done")]], resize_keyboard=True, one_time_keyboard=True)
random_listf_keyboard = telegram.replykeyboardmarkup.ReplyKeyboardMarkup([[telegram.KeyboardButton("random")],[telegram.KeyboardButton("list")]], resize_keyboard=True)
pass_keyboard = telegram.replykeyboardmarkup.ReplyKeyboardMarkup([[telegram.KeyboardButton("pass")]], resize_keyboard=True)
inlineNextKeyboard1 = InlineKeyboardMarkup([[InlineKeyboardButton("next", callback_data='next')],[InlineKeyboardButton("filter", callback_data='filter')]])
inlineNextKeyboard2 = InlineKeyboardMarkup([[InlineKeyboardButton("previous", callback_data='previous'),InlineKeyboardButton("next", callback_data='next')],[InlineKeyboardButton("filter", callback_data='filter')]])
inlineNextKeyboard3 = InlineKeyboardMarkup([[InlineKeyboardButton("previous", callback_data='previous')],[InlineKeyboardButton("filter", callback_data='filter')]])

filtersKeyboard1 = InlineKeyboardMarkup([[InlineKeyboardButton("next", callback_data='next')],
                                        [InlineKeyboardButton("state", callback_data='state'),InlineKeyboardButton("content type", callback_data='content type'),InlineKeyboardButton("sort by", callback_data='sort')],
                                        [InlineKeyboardButton("reset", callback_data='reset')],[InlineKeyboardButton("hide filters", callback_data='hide')]])

filtersKeyboard2 = InlineKeyboardMarkup([[InlineKeyboardButton("next", callback_data='next'),InlineKeyboardButton("previous", callback_data='previous')],
                                        [InlineKeyboardButton("state", callback_data='state'),InlineKeyboardButton("content type", callback_data='content type'),InlineKeyboardButton("sort by", callback_data='sort')],
                                        [InlineKeyboardButton("reset", callback_data='reset')],[InlineKeyboardButton("hide filters", callback_data='hide')]])


filtersKeyboard3 = InlineKeyboardMarkup([[InlineKeyboardButton("previous", callback_data='previous')],
                                        [InlineKeyboardButton("state", callback_data='state'),InlineKeyboardButton("content type", callback_data='content type'),InlineKeyboardButton("sort by", callback_data='sort')],
                                        [InlineKeyboardButton("reset", callback_data='reset')],[InlineKeyboardButton("hide filters", callback_data='hide')]])

stateKeyboard = InlineKeyboardMarkup([[InlineKeyboardButton("unread", callback_data='unread')],
                                      [InlineKeyboardButton("archive", callback_data='archive')],
                                      [InlineKeyboardButton("all", callback_data='all')],
                                      [InlineKeyboardButton("cancel", callback_data='cancel')]])

contentKeyboard = InlineKeyboardMarkup([[InlineKeyboardButton("image", callback_data='image')],
                                        [InlineKeyboardButton("video", callback_data='video')],
                                        [InlineKeyboardButton("article", callback_data='article')],
                                        [InlineKeyboardButton("cancel", callback_data='cancel')]])

sortKeyboard = InlineKeyboardMarkup([[InlineKeyboardButton("newest first", callback_data='newest')],
                                    [InlineKeyboardButton("oldest first", callback_data='oldest')],
                                    [InlineKeyboardButton("alphabetical", callback_data='title')],
                                    [InlineKeyboardButton("by url", callback_data='site')],
                                    [InlineKeyboardButton("cancel", callback_data='cancel')]])




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
        self.pocketInstance = None
        self.currentList = None
        self.filterstatus = None
        self.filters = {"state":"all","favorite":None,"tag":None,"contentType":None,
                        "sort":"newest","detailType":None,"search":None,"domain":None,
                        "domain":None,"since":None,"count":None,"offset":None}


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

def process(userfind,r):
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
        return None
    if len(userfind.currentList.list) <=8:
         update.message.reply_text(string, disable_web_page_preview=True)
         return
    return string



def updateList(list):

    pocket_instance = userfind.pocketInstance
    r = userfind.currentList.list = Pocket.get(userfind.pocketInstance,state=userfind.filters["state"],contentType=userfind.filters["contentType"],sort=userfind.filters["sort"])
    x =json.dumps(r[0])
    print type(x)
    #print type(x)
    data = json.loads(x)
    print data
    #print type(data)
    dataValues = data.values()
    #print len(dataValues[4])
    articlesList = dataValues[4]
    ##print(articlesList.values())
    
    list2add = listStatus()
    try:
        list2add.list = articlesList.values()
        #print list2add.list[0].values()[11]
        #print list2add.list[0].values()[17]
        list2add.currentIndex = 0

        userfind.currentList= list2add
        return
    except:
        return -1

def stringEight(listr):
    try:
        user = users.find_one({"user_id":update.message.from_user.id})
        ##print userDB
    except:
        update.message.reply_text("You are not registered. Press /start and then resend command2")
        return ConversationHandler.END
    string = ""
    startindex = listr['index']
    endindex =startindex+8
    if endindex >= len(listr['list']):
        endindex = len(listr['list'])

    for i in xrange(startindex,endindex):
        title = listr['list'][i]["resolved_title"].encode('utf-8').strip()
        url = listr['list'][i]["resolved_url"].encode('utf-8').strip()           
        string = string +title+"\n"+url+"\n"+"\n"

    if len(string) == 0:
        return None
    return string

def start(bot, update):
    update.message.reply_text("Hi")
    auth_url = Pocket.get_auth_url(code=request_token, redirect_uri=redirect_uri)
    ##userfind.auth_url= auth_url
    ##print auth_url
    update.message.reply_text("Please authorise the bot at the following url"+"\n"+"\n"+auth_url,disable_web_page_preview=True)
    time.sleep(2)
    update.message.reply_text("come back here and hit done when you have finished authorisation",reply_markup=done_keyboard)
    user = {
            "user_id":update.message.chat.id,
            "user_credentials":None,
            "access_token":None,
            "currentTask":None,
            "currentURL":None,
            "auth_url":auth_url,
            "currentList":None,
            "filterstatus":None,
            "list_ids":[]
    }
    users.insert_one(user)
    return CONFIRM


def confirm(bot,update):
    try:
        user = users.find_one({"user_id":update.message.from_user.id})
        ##print userDB
    except:
        update.message.reply_text("You are not registered. Press /start and then resend command2")
        return ConversationHandler.END
    try:
        user_credentials = Pocket.get_credentials(consumer_key=consumer_key, code=request_token)
        access_token =user_credentials['access_token']
        pocketInstance = pocket.Pocket(consumer_key, access_token)
        users.update({"user_id":update.message.chat.id},{"$set":{"access_token":access_token,"user_credentials":user_credentials}})
        update.message.reply_text("You are all set! Try pressing random below to get a random article or list to skim your libray",reply_markup=random_listf_keyboard)
        del pocketInstance
        return ConversationHandler.END
    except:
        update.message.reply_text("Please authorise this bot first:"+"\n"+"\n"+user['auth_url'],reply_markup=done_keyboard)
        return CONFIRM
    
def help(bot, update):
    update.message.reply_text(' newtask <taskname:priority:duedate> to create a task'+ '\n'
                              + ' mytasks to show tasks'+'\n'+ ' newhabit <habitname:priority>'+'\n'+ ' myhabits to show tasks'+'\n'+ ' deltask <taskid> to delete task by task id (you can find this out using /mytasks command)'
                              +'fintask ,<taskid> to delete task by task id (you can find this out using /mytasks command'+ '\n' +'delthabit <habitid> to delete habit by habit id (you can find this out using /myhabits command)' +"/help to get command list")

def pressDone(bot,update):
    update.message.reply_text("Please press done",reply_markup=done_keyboard)
    return CONFIRM


def listf(bot,update):
    try:
        user = users.find_one({"user_id":update.message.from_user.id})
        ##print userDB
    except:
        update.message.reply_text("You are not registered. Press /start and then resend command2")
        return ConversationHandler.END

    pocket_instance = pocket.Pocket(consumer_key, user['access_token'])
    r = Pocket.get(pocket_instance,state="all")
    x =json.dumps(r[0])
    data = json.loads(x)
    articlesList = data['list'].values()

    uid = randint(10000,99999)
    while uid in user['uids']:
        uid = randint(10000,99999)

    list2add = {
                "user_id":update.message.chat.id,
                "list":articlesList,
                "list_id":uid,
                "index":0
            }


    lists.insert_one(list2add)
    string=stringEight(list2add)
    users.update({"user_id":update.message.chat.id},{"$push":{"list_ids":uid}})
    if string == None:
        update.message.reply_text("actually...you don't have shit in your pocket :P")

    if len(articlesList) <=8:
         update.message.reply_text("LIST"+str(uid)+'\n'+'\n'+string, disable_web_page_preview=True)
         return
    update.message.reply_text("LIST"+str(uid)+'\n'+'\n'+string, disable_web_page_preview=True,reply_markup=inlineNextKeyboard1)


def menuButtons(bot,update):

    x=1
    query = update.callback_query.id
    queryObj = update.callback_query
    queryData = update.callback_query.data
    mid = queryObj.message.message_id
    try:
        user = users.find_one({"user_id":queryObj.message.from_user.id})
        ##print userDB
    except:
        update.message.reply_text("You are not registered. Press /start and then resend command2")
        return ConversationHandler.END

    message=update.callback_query.message.text
    messageComponents=message.split('\n')
    list_id_line = messageComponents[0]
    list_id= list_id_line[4:]
    intlist_id = int(list_id)
    listfind = lists.find_one({'user_id':queryObj.message.chat.id,"list_id":intlist_id})
    if listfind == None:
        queryObj.message.reply_text("Either I misplaced this note... or you did some crazy black magic to get here")
        return

    if str(queryData) == "previous":
        lists.update({'user_id':queryObj.message.chat.id,"list_id":intlistid},{"$inc":{"index":-8}})
        listfind = lists.find_one({'user_id':queryObj.message.chat.id,"list_id":intlist_id})
    if str(queryData) == "next":
        lists.update({'user_id':queryObj.message.chat.id,"list_id":intlistid},{"$inc":{"index":+8}})
        listfind = lists.find_one({'user_id':queryObj.message.chat.id,"list_id":intlist_id})
        
    if listfind['currentIndex']+8 >len(listfind['list']):
        keyboard = inlineNextKeyboard3
    elif listfind['currentIndex']-8 <0:
        keyboard = inlineNextKeyboard1
    else:
        keyboard = inlineNextKeyboard2
            
    string = stringEight(listfind)


    bot.edit_message_text(text="LIST"+str(uid)+'\n'+'\n'+string,
                      chat_id=queryObj.message.chat_id,
                      message_id=mid, disable_web_page_preview=True)
    bot.edit_message_reply_markup(chat_id =queryObj.message.chat_id,message_id=mid,reply_markup =keyboard,parse_mode='HTML')


def randomL(bot,update):
    try:
        user = users.find_one({"user_id":update.message.from_user.id})
        print user
        ##print userDB
    except:
        update.message.reply_text("You are not registered. Press /start and then resend command2")
        return ConversationHandler.END

    pocket_instance = pocket.Pocket(consumer_key, user['access_token'])
    r = Pocket.get(pocket_instance,state="unread")
    x =json.dumps(r[0])
    data = json.loads(x)
    articlesList = data['list'].values() ##dataValues
    string = ''
    for i in len(xrange(5)):
        randomInt =random.randint(0,len(articlesList)-1)
        string = articlesList[randomInt]["resolved_title"]+'\n'+articlesList[randomInt]["resolved_url"]+'\n'+'\n'

    update.message.reply_text(string,reply_markup=random_listf_keyboard,disable_web_page_preview=True)
##    fileObj = open("json.txt","w")
##    fileObj.write(x)
    

def checkText(bot,update):
    try:
        user = users.find_one({"user_id":update.message.from_user.id})
        ##print userDB
    except:
        update.message.reply_text("You are not registered. Press /start and then resend command2")
        return ConversationHandler.END
    
    try:
        urllib2.urlopen(str(update.message.text))
    except:
        update.message.reply_text("not a valid url")
        return ConversationHandler.END

    users.update({"user_id":update.message.chat.id},{"$set":{"currentURL":update.message.text}})
    update.message.reply_text("Are there any tags for this url?(split them with commas)")
    update.message.reply_text("You can hit pass if there are none",reply_markup=pass_keyboard)
    return ADD

def parsetagsadd(bot,update):
    try:
        user = users.find_one({"user_id":update.message.from_user.id})
        ##print userDB
    except:
        update.message.reply_text("You are not registered. Press /start and then resend command2")
        return ConversationHandler.END

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
    pocket_instance = pocket.Pocket(consumer_key, user['access_token'])
    pocket_instance.add(user['currentURL'],tags=tagsStr)
    users.update({"user_id":update.message.chat.id},{"$set":{"currentURL":None}})
    update.message.reply_text("Article added!!",reply_markup=random_listf_keyboard)    
    return ConversationHandler.END
    
    
def passf(bot,update):
    userfind = find_user(users,update.message.from_user.id)
    if userfind == None:
        update.message.reply_text("Please type /start and then resend command")
    update.message.reply_text("All good! Your article was saved")
    pocket_instance = pocket.Pocket(consumer_key, user['access_token'])
    pocket_instance.add(userfind.currentURL)
    update.message.reply_text("All good! Your article was saved",reply_markup=random_listf_keyboard)
    return ConversationHandler.END
    

def cancel(bot, update):
    print "r"
    userfind = find_user(users,update.message.from_user.id)
    if userfind == None:
        update.message.reply_text("Please type /start and then resend command")
        return ConversationHandler.END
    logger.info("User %s canceled the conversation." % update.message.from_user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')
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
    dp.add_handler(RegexHandler('^list$', listf))
    dp.add_handler(CallbackQueryHandler(menuButtons))
    onboarding = ConversationHandler(
    entry_points=[CommandHandler("start",start)],
    states={


        CONFIRM: [RegexHandler('^(done)$',
                                confirm),
                    MessageHandler(Filters.text,
                                   pressDone)
                  ],
        
        TYPING_CHOICE: [RegexHandler('^cancel$', cancel),                        
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
                ],     
    },

    fallbacks=[RegexHandler('^cancel$', cancel)]
    )

    dp.add_handler(add_article)

    

    #easter egg



    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    
    updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
    updater.bot.set_webhook("https://telegrampocketbot.herokuapp.com/" + TOKEN)
    
    ##updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
