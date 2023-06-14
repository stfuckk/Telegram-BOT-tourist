from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from weather import get_weather
#from guide import get_guide_list

TOKEN = open("TOKEN.txt").read().split()[0]


# обработчик команды /start
async def start(update, context) -> None:
    keyboard = ReplyKeyboardMarkup([
        [KeyboardButton('/help')],
        [KeyboardButton('/about')]
    ], resize_keyboard=True)
    await update.message.reply_text(
        f'**Привет! Я диня - бот, который предоставит полезную информацию для твоего путешествия!**\n'
        f'Напиши /help, чтобы узнать мои команды, так же, ты можешь воспользоваться клавиатурой.',
        reply_markup=keyboard, parse_mode="Markdown")


# обработчик команды /help
async def help(update, context) -> None:
    await update.message.reply_text(f'Мои команды:\n'
                                    f'**/weather [город]** - получить прогноз погоды для заданного города;\n'
                                    f'**/guide [место] ** - получить список интересных мест для заданного места.'
                                    f'(напишите "город страна" для точного поиска)\n', parse_mode="Markdown")


# обработчик команды /about
async def about(update, context) -> None:
    await update.message.reply_text(f'**Учебный проект по созданию чат-бота в telegram,\nv1.0-stable**',
                                    parse_mode="Markdown")


# обработчик на случай неизвестной команды
async def echo(update, context) -> None:
    # обработка try, чтобы избежать выбрасывания exception в случае редактирования сообщения пользователем
    try:
        await update.message.reply_text(f'Я не понимаю, что вы говорите. Попробуйте другую команду из **/help**.',
                                        parse_mode="Markdown")
    except:
        return

# обработчики основных команд
# weather
async def weather(update, context) -> None:
    try:
        city = update.message.text.split()[1]
    except IndexError:
        await update.message.reply_text('Напишите команду в виде "**/weather [город]**", пожалуйста.',
                                        parse_mode="Markdown")
        return
    weather_data = await get_weather(city)
    await update.message.reply_text(weather_data, parse_mode="Markdown")


# guide
async def guide(update, context) -> None:
    try:
        place = update.message.text.split()[1:]
    except IndexError:
        await update.message.reply_text('Напишите команду в виде "**/guide [место]**", пожалуйста.',
                                        parse_mode="Markdown")
        return
    guide_data = await get_guide_list(place)
    await update.message.reply_text(guide_data, parse_mode="Markdown")


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('about', about))

    # /weather
    application.add_handler(CommandHandler('weather', weather))

    # /

    application.add_handler(MessageHandler(filters.TEXT, echo))
    application.run_polling(print('Бот готов к работе!'))


if __name__ == '__main__':
    main()
