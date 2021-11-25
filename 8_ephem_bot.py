import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import ephem
from datetime import date

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text("Привет, {}! Ты вызвал команду /start".format(update.message.from_user["username"]))
    update.message.reply_text("ты можешь со мной поболтать, либо узнать инфу о планете")
    update.message.reply_text("для этого используй команду /planet")
    logging.info("connect username: {}".format(update.message.from_user["username"]))
    print("connect username: {}".format(update.message.from_user["username"]))

def get_planet (update, context):
    listPlanets = []
    for planets in ephem._libastro.builtin_planets():
        if planets[1] == 'Planet':
            listPlanets.append(planets[2])
    if not context.args:
        update.message.reply_text("Пожалуйста введите название планеты на английском")
    elif len(context.args) > 1:
        update.message.reply_text("За 1 раз можно посмотеть информацию только по одной планете")
    elif not (str(context.args[0]).title() in listplanets):
        update.message.reply_text("указанной Вами планеты нет в списке:")
        listPlanetReply = ""
        for pl in listPlanets:
            listPlanetReply += pl
            listPlanetReply += "\n"
        update.message.reply_text(listPlanetReply)
    # можно и было бы и просто else указать, но я пока не уверен, все ли я предусмотрел
    # к тому же в данном случае корректнее все же проверять входящий параметр
    elif str(context.args[0]).title() in listPlanets:
        parameter = context.args[0]
        planetEphem = getattr(ephem, parameter)
        planet = planetEphem(date.today())
        # вываливается предупреждение DeprecationWarning: PY_SSIZE_T_CLEAN will be required for '#' formats
        # но судя по статье https://digitology.tech/docs/python_3/c-api/intro.html
        # это к разработчикам ephem
        update.message.reply_text("Планета {} находится в созвезии {}".format(parameter, ephem.constellation(planet)[1]))
    else:
        update.message.reply_text("Я так и не понял, что вы от меня хотите :-(")

def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)

def main():
    mybot = Updater(settings.API_KEY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", get_planet))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал")

    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()