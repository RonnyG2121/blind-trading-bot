#!/usr/bin/python

import finanzas
import telebot
import threading
# importo el archibo mi_conf.py donde tengo mi token del bot, y la constante mi_token
from mi_conf import TOKEN, MI_CHAT_ID
# importo de function_registro.py la funcion registro()
from function_registro import registro

bot = telebot.TeleBot(TOKEN)  # instancio el bot y le paso el token


@bot.message_handler(commands=["start"])  # manejador del comando start
def cmd_start(message):
    # funcion que contiene las acciones del bot cuando convoquen start
    var_comando = message.text
    respuesta = "200"
    registro(message.chat.id, respuesta,
             var_comando, message.from_user.username)
    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(
        message.chat.id, f" 🇻🇪 Hola {message.from_user.first_name}, Bienvenido a Blind 🧑‍🦯 trading Bot ")
    bot.reply_to(message, text=f"""<i><b><u> El siguiente menú, muestra los comandos disponibles</u></b></i>
    <b><i>/start</i></b> ➡️ Menú de inicio
    <b><i>/p</i></b> ➡️ Precio del activo (enviame /p espacio el ticker o par).
    <b><i> /ayuda </i></b> ➡️ Te muestro con ejemplo como hacer una consulta vpalida.
    
    """, parse_mode="html")


@bot.message_handler(commands=["ayuda"])
def cmd_ayuda(message):
    # funcion que contiene las acciones del bot cuando convoquen ayuda
    var_comando = message.text
    respuesta = "200"
    registro(message.chat.id, respuesta,
             var_comando, message.from_user.username)
    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(message, text=f"""<i><b><u>Bienvenido a la ayuda</u></b></i>
    🦮 Permiteme guiarte.
    <i><b><u>Para las criptomonedas sigue este formato</u></b></i>
    <b><i>/p BTC-USD</i></b> ➡️ Bitcoin contra el dólar 
    <b><i>/p LTC-USD</i></b> ➡️ Litecoin contra el Dölar
    <b><i>/p BNB-USD</i></b> ➡️ Binancecoin contra el Dölar
    <i><b><u>Para las acciones</u></b></i>
    <b><i>/p TSLA</i></b> ➡️ Para Tsla
    <b><i>/p AAPL</i></b> ➡️ Para la manzana
    <i><b><u>Para los mercados de futuro</u></b></i>
    <b><i>/p GC=F</i></b> ➡️ para el oro
    <b><i>/p BZ=F</i></b> ➡️ para el petróleo Brent
""", parse_mode="html")


@bot.message_handler(commands=["p"])  # manejador del comando p de precio
def cmd_ultimopreciobtc(message):
    # contiene las accione del comando /p
    var_comando = message.text
    var_comando = var_comando.split()
    respuesta = "200"
    registro(message.chat.id, respuesta,
             var_comando, message.from_user.username)
    activo = var_comando[1].upper()
    temporalidad = var_comando[2].lower() if len(var_comando) > 2 else "1d"
    match temporalidad:
        case "5m":
            mensaje_temporalidad = F"¡Los datos suministrados son en temporalidad 5 minutos!"
        case "15m":
            mensaje_temporalidad = F"¡Los datos suministrados son en temporalidad 15 minutos!"
        case "1h":
            mensaje_temporalidad = F"¡Los datos suministrados son en temporalidad 1 hora!"
        case "1d":
            mensaje_temporalidad = F"¡Los datos suministrados son en temporalidad diaria!"
        case "1wk":
            mensaje_temporalidad = F"¡Los datos suministrados son en temporalidad  semanal!"
        case "1mo":
            mensaje_temporalidad = F"¡Los datos suministrados son en temporalidad mensual!"
        case _:
            bot.reply_to(message, text="""
                Temporalidad no válida. Las temporalidades soportadas son:
                * 5m: 5 minutos
                * 15m: 15 minutos
                * 1h: 1 hora
                * 1d: diaria
                * 1wk: semanal
                * 1mo: mensual
                """)
            return
    pa = finanzas.PrecioActual(activo, temporalidad)
    if isinstance(pa, (int, float)):
        superior, media, inferior = finanzas.BandasBollinger(activo, temporalidad)
        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, text=f"""El precio de {activo}, es:
        {pa}.
        La Ma de 7 es: {finanzas.Ma7(activo, temporalidad)},
        la Ma de 21 es: {finanzas.Ma21(activo, temporalidad)},
        la Ma de 30 es: {finanzas.Ma30(activo, temporalidad)},
        la Ma de 50 es: {finanzas.Ma50(activo, temporalidad)},
        la Ma de 100 es: {finanzas.Ma100(activo, temporalidad)}
        y la Ema de 200 es: {finanzas.Ema200(activo, temporalidad)}
        <i>Las Bandas de Bollinger</i>
        Superior: {round(superior[-1], 2)}
        Media: {round(media[-1], 2)}
        Inferior: {round(inferior[-1], 2)}.
        {mensaje_temporalidad}
        """, parse_mode="html")
    else: # Si pa no es un número, asume que es un mensaje de error
        bot.reply_to(message, text=f"Error al obtener el precio de {activo}, por favor verifica el activo y vuelve a intentarlo.")

@bot.message_handler(commands=["log"])  # manejador del comando log
def cmd_log(message):
    # contiene las accione del comando log
    var_comando = message.text
    if message.chat.id == MI_CHAT_ID:
        respuesta = "200"
        registro(message.chat.id, respuesta,
                 var_comando, message.from_user.username)
        bot.send_chat_action(message.chat.id, "upload_document")
        archibo_log = open("registro_ID.txt", "rb")
        bot.send_document(message.chat.id, archibo_log)
    else:
        respuesta = "404"
        registro(message.chat.id, respuesta,
                 var_comando, message.from_user.username)
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, "Comando no disponible")

# respondiendo a los mensajes de texto que no son comandos


# manejador de todo lo que no esta permitido
@bot.message_handler(content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact'])
def bot_mensajes_texto(message):
    # Gestiona los mensajes de texto recibidos
    if message.text and message.text.startswith("/"):
        registro(message.chat.id, "404", message.text,
                 message.from_user.username)
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, "Comando no disponible")
    else:
        registro(message.chat.id, "404", message.text,
                 message.from_user.username)
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, "Comando no disponible")


def recibir_mensajes():
    # Bucle infinito que comprueba si hay nuevos mensajes en el bot
    bot.infinity_polling()

# MAIN ########################################################


def main():
    # Por cada nuevo comando que agrego, se debe agregar el comando, y este rige el orden de los mismos.
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Menu Inicio"),
        telebot.types.BotCommand(
            "/p", "Dvuelve el precio del activo y las Ema de 7, 21, 30, 50, 100 y las Bandas de Bollinger"),
        telebot.types.BotCommand(
            "/ayuda", "Muestra ejemplos de las consultas"),
    ])

    print('Iniciando " Bot"')
    hilo_bot = threading.Thread(name="hilo_bot", target=recibir_mensajes)
    hilo_bot.start()
    print('Bot iniciado')
    bot.send_message(MI_CHAT_ID, "Elvin Vargas Bot, iniciado con éxito😁")


if __name__ == "__main__":
    main()
