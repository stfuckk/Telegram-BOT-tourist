from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from weather import get_weather
from guide import get_guide_list
from travel_tips import get_travel_tip
from currency import exchange_currency
import random
from datetime import datetime

TOKEN = open("TOKEN.txt").read().split()[0]

keyboard = ReplyKeyboardMarkup([
    [KeyboardButton('/help')],
    [KeyboardButton('/about')],
    [KeyboardButton('/tip')]
], resize_keyboard=True)


# обработчик команды /start
async def start(update, context) -> None:
    result = f'***Привет! Я диня - бот, который предоставит полезную информацию для твоего путешествия!***\n' \
             f'Напиши /help, чтобы узнать мои команды, так же, ты можешь воспользоваться клавиатурой.'
    await update.message.reply_text(result, reply_markup=keyboard, parse_mode="Markdown")
    log(update, context, result)


# обработчик команды /help
async def help(update, context) -> None:
    result = f'Мои команды:\n' \
             f'***/weather [город]*** - получить прогноз погоды для заданного города;\n' \
             f'***/guide [место]*** - получить список интересных мест для заданного места\n' \
             f'***/tip*** - получить случайный совет для путешествия\n' \
             f'***/currency [кол-во рублей] [страна(eng only)]*** ' \
             f'- обменять рубли на валюту заданной страны'
    await update.message.reply_text(result, parse_mode="Markdown")
    log(update, context, result)


# обработчик команды /about
async def about(update, context) -> None:
    result = f'***Учебный проект по созданию чат-бота в telegram,\nv1.0-stable***'
    await update.message.reply_text(result, parse_mode="Markdown")
    log(update, context, result)


# обработчик на случай неизвестной команды
async def echo(update, context) -> None:
    # обработка try, чтобы избежать выбрасывания exception в случае редактирования сообщения пользователем
    try:
        result = f'Я не понимаю, что вы говорите. Попробуйте другую команду из ***/help***.'
        await update.message.reply_text(result, parse_mode="Markdown")
        log(update, context, result)
    except:
        return


# обработчики основных команд
# weather
async def weather(update, context):
    try:
        city = update.message.text.split()[1]
    except IndexError:
        result = 'Напишите команду в виде "***/weather [город]***", пожалуйста.'
        await update.message.reply_text(result, parse_mode="Markdown")
        log(update, context, result)
        return

    weather_data = await get_weather(city)
    await update.message.reply_text(weather_data, parse_mode="Markdown")
    log(update, context, weather_data)


# guide
async def guide(update, context) -> None:
    try:
        place = ' '.join(update.message.text.split()[1:])
    except IndexError:
        result = 'Напишите команду в виде "***/guide [место]***", пожалуйста.'
        await update.message.reply_text(result, parse_mode="Markdown")
        log(update, context, result)
        return

    await update.message.reply_text('***Ищу интересные места!***', parse_mode="Markdown")
    guide_data = await get_guide_list(place)
    if isinstance(guide_data, str):
        await update.message.reply_text(guide_data, parse_mode="Markdown")
        log(update, context, guide_data)
    else:
        random.shuffle(guide_data)
        k = 0
        result = ''
        if len(guide_data) > 5:
            for showplace in guide_data:
                k += 1
                result += showplace + '\n\n'
                await update.message.reply_text(showplace, parse_mode="Markdown", disable_web_page_preview=True)
                if k == 5:
                    log(update, context, result)
                    return
        else:
            for showplace in guide_data:
                result += showplace + '\n\n'
                await update.message.reply_text(showplace, parse_mode="Markdown", disable_web_page_preview=True)
                log(update, context, result)


# tip
async def tip(update, context) -> None:
    random_tip = await get_travel_tip()
    await update.message.reply_text(random_tip, parse_mode="Markdown")
    log(update, context, random_tip)


# currency
async def currency(update, context):
    try:
        rub_count = float(update.message.text.split()[1])
        country = ' '.join(update.message.text.split()[2:])
    except:
        result = 'Напишите команду в виде "***/currency [кол-во рублей] [страна(eng only)]***", пожалуйста.'
        await update.message.reply_text(result, parse_mode="Markdown")
        log(update, context, result)
        return

    result = await exchange_currency(rub_count, country)
    await update.message.reply_text(result, parse_mode="Markdown")
    log(update, context, result)


# ------------Логирование-------------

def log(update, context, bot_message) -> None:
    chat_id = update.message.chat_id
    user = update.message.from_user.username
    message = (update.message.text)
    bot_message = bot_message.replace('*', '')
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    with open(f'C:/logs/{chat_id}.log', 'a+', encoding='utf-8') as log_file:
        log_file.write(f'[{current_time}] User: > {message}\n'
                       f'[{current_time}] Bot:  > {bot_message}\n\n')


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('about', about))

    # /weather
    application.add_handler(CommandHandler('weather', weather))

    # /guide
    application.add_handler(CommandHandler('guide', guide))

    # /tip
    application.add_handler(CommandHandler('tip', tip))

    # /currency
    application.add_handler(CommandHandler('currency', currency))

    application.add_handler(MessageHandler(filters.TEXT, echo))
    application.run_polling(print('Бот готов к работе!'))


if __name__ == '__main__':
    main()
