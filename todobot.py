
import operation
import logging
from config import TOKEN
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

BUTTON, ADD, SEARCH, ALL, COMMENT = range(5)

ADD='✏️ Записать задачу'
SEARCH='🔍 Найти задачу'
ALL='📃 Посмотреть весь список'
GO='✅ Продолжить работу'
EXIT='🚪 Выйти'

def start(update, _):
    reply_keyboard = [[ADD,SEARCH,ALL,EXIT]]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Привет! Этот бот поможет следить за своими делами. Выберите функцию ниже', reply_markup=markup_key)    
    return BUTTON

def button(update, _):
    user = update.message.from_user
    text = update.message.text
    keyboard_remove = ReplyKeyboardRemove()
    logger.info("Пользователь %s выбрал операцию %s",  user.first_name, text)
    if text == ADD:
        update.message.reply_text('Напишите задачу', reply_markup=keyboard_remove)
        return ADD
    if text == SEARCH:
        update.message.reply_text('Напишите слово, которое может быть в задаче', reply_markup=keyboard_remove)
        return SEARCH
    if text == ALL:
        return ALL
    if text == GO:
        return start(update, _)
    if text == EXIT:
        update.message.reply_text(f'До встречи, {update.effective_user.first_name}', reply_markup=keyboard_remove)
        return cancel()

def add(update, _):
    global list_add
    list_add = []
    text = update.message.text
    list_add.append(text)
    logger.info("Добавлена задача: ", list_add)
    update.message.reply_text('Добавьте комментарий к задаче: ')
    return COMMENT

def comment(update, _):
    text = update.message.text
    list_add.append(text)
    logger.info("Добавлен комментарий: ", list_add)
    operation.write_csv(list_add)
    update.message.reply_text('Задача добавлена')
    reply_keyboard = [[GO,EXIT]]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Что дальше?', reply_markup=markup_key)     
    return BUTTON

def search(update, _):
    user = update.message.from_user
    text = update.message.text
    result = operation.search_csv(text)
    logger.info("Пользователь %s ищет %s",  user.first_name, text)  
    res = "\n\n".join(result)
    if result == 'Ничего не нашлось':
        update.message.reply_text(result)
    else:
        update.message.reply_text(f'Нашел задачу:\n\n{res}')
    reply_keyboard = [[GO,EXIT]]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Что дальше?', reply_markup=markup_key)      
    return BUTTON

def all(update, _):
    search_text=operation.read_csv()
    res = '\n\n'.join(str(l) for l in search_text)
    update.message.reply_text(f'Список задач: \n\n{res}')
    reply_keyboard = [[GO,EXIT]]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Что дальше?', reply_markup=markup_key)      
    return BUTTON


def cancel(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s отменил разговор.", user.first_name)
    update.message.reply_text(
        'Пиши, если понадобится моя помощь!', 
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END  
 

if __name__ == '__main__':
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            BUTTON: [MessageHandler(Filters.text, button)],
            ADD: [MessageHandler(Filters.text, add)],
            SEARCH: [MessageHandler(Filters.text, search)],
            ALL: [MessageHandler(Filters.text, all)],
            COMMENT: [MessageHandler(Filters.text, comment)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )


dispatcher.add_handler(conv_handler)


updater.start_polling()
updater.idle()