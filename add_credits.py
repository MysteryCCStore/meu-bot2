from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.database import *
from bot.cogs.modules.mp_pix import pix as pix_mp_1, status as status_mp
from bot.cogs.modules.gn_pix import pix as pix_gn_1, status as status_gn
from bot.cogs.modules.qr import remove, qrimg
from bot.cogs.modules.pix_authentication import *
from bot.cogs.modules.adm_list import adm_list
from bot.cogs.modules.group_list import group_list
from bot.cogs.modules.support import *
from random import sample
import string, json
from bot.cogs.ban import *
import asyncio, time, os

# IMPORTANTE: Defina estados se for usar ConversationHandler
# Se seu bot não usava ConversationHandler antes, remova os imports acima e mantenha o resto.
# Para este fix, vamos focar em corrigir a lógica do texto.

def time_diference(start_time):
    try:
        start_time = float(start_time)
        elapsed_time_secs = time.time() - start_time
        # Correção: importar timedelta se não estiver no escopo global
        from datetime import timedelta
        msg = str(timedelta(seconds=round(elapsed_time_secs))).split(':')
        hora = msg[0]
        if int(hora) <= 1:
            return True
        else:
            return False
    except: 
        return False


def adicionar_saldo(update: Update, context: CallbackContext):
    verify = verify_default()
    keyboard = []
    texto2 = ''

    if verify == 'mp' or verify == 'gn' or verify == 'key':
        keyboard.append([InlineKeyboardButton(f'💵 Recarregar 10', callback_data='r_10'),
                        InlineKeyboardButton(f'💵 Recarregar 15', callback_data='r_15')])
        keyboard.append([InlineKeyboardButton(f'💵 Recarregar 20', callback_data='r_20'),
                        InlineKeyboardButton(f'💵 Recarregar 40', callback_data='r_40')])
        texto2 = '\n\nOu escolha um valor abaixo para poder gerar o pagamento!'

    keyboard.append([InlineKeyboardButton(f'◀︎ {button_main}', callback_data='main')])

    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=add_credits_info+texto2, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


def recarregar(update: Update, context: CallbackContext):
    with open('config/config.json', 'r', encoding="utf8") as file:
        config = json.loads(file.read())
        expiration_payment = config['expiration_payment_in_minutes']
        minimo = config['minimum_recharge']

    query = update.message
    tipo = 0
    
    # CORREÇÃO 1: Tratamento seguro do texto
    preco = None
    if query is None:
        query = update.callback_query
        tipo = 1
    else:
        # Pega o texto completo, ex: "/recarga 10"
        full_text = update.message.text
        # Tenta extrair o número
        parts = full_text.split()
        if len(parts) > 1:
            preco = parts[1]
        else:
            # Se não tem número, volta a pedir
            update.message.reply_text(text=pay_error_2, parse_mode='Markdown')
            return # Importante: para a execução aqui

    id_user = str(query.from_user['id'])
    user_nome = str(query.from_user['first_name'])
    asyncio.run(registrar_usuario(id_user, user_nome))

    # Se vier de callback, sobrescreve o preco
    try:
        if query.data is not None and query.data.startswith('r_'):
            preco = str(query.data).replace('r_', '')
    except:
        pass

    # Verificações finais
    grupos = group_list()
    
    if check_status(id_user):
        if preco is not None:
            verify = verify_default()
            if asyncio.run(check_config('pix'))[1] == '1' or not verify == '':
                try:
                    if preco.isnumeric():
                        if int(preco) >= int(minimo) and int(preco)<=100:
                            files = [f for f in os.listdir('temp') if os.path.isfile(os.path.join('temp', f))]
                            a = []
                            for file in files:
                                if id_user in file:
                                    try:
                                        with open('temp/'+str(file), 'r') as f:
                                            load = json.loads(f.read())
                                        criado_em = load['criado_em']
                                        if time_diference(str(criado_em)) == False:
                                            a.append('.')
                                    except:
                                        pass
                            
                            if not len(a) >= 2:

                                if verify == 'mp':
                                    if tipo == 0:
                                        update.message.reply_text(text=pay_info_alert, parse_mode='Markdown')
                                    else:
                                        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=pay_info_alert, parse_mode='Markdown')

                                    name = ''.join(sample(string.ascii_lowercase, 3))
                                    pay = pix_mp_1(f'R${preco},00', preco)
                                    id_p = pay[0]
                                    pix_id = pay[1]

                                    with open(f'temp/pix-{id_user}-{id_p}.json', 'w') as f:
                                        f.write(json.dumps({'tipo': 'mp', 'preco': preco, 'usuario': id_user, 'criado_em': time.time(), 'id_p': id_p}))

                                    if asyncio.run(check_config('qrcode'))[1] == '1':
                                        qrimg(pix_id, name)
                                        m = context.bot.send_photo(chat_id=id_user, photo=open(f'temp/{name}.png','rb'), caption=pay_info.format(expiration_payment, id_p, pix_id, preco), parse_mode='Markdown')
                                        remove(name)
                                    else:
                                        m = context.bot.send_message(chat_id=id_user, text=pay_info.format(expiration_payment, id_p, pix_id, preco), parse_mode='Markdown')

                                elif verify == 'gn':
                                    if tipo == 0:
                                        update.message.reply_text(text=pay_info_alert, parse_mode='Markdown')
                                    else:
                                        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=pay_info_alert, parse_mode='Markdown')

                                    name = ''.join(sample(string.ascii_lowercase, 3))
                                    pay = pix_gn_1(f'R${preco},00', preco)
                                    id_p = pay[0]
                                    pix_id = pay[1]
                                    if asyncio.run(check_config('qrcode'))[1] == '1':
                                        qrimg(pix_id, name)
                                        m = context.bot.send_photo(chat_id=id_user, photo=open(f'temp/{name}.png','rb'), caption=pay_info.format(expiration_payment, id_p, pix_id, preco), parse_mode='Markdown')
                                        remove(name)
                                    else:
                                        m = context.bot.send_message(chat_id=id_user, text=pay_info.format(expiration_payment, id_p, pix_id, preco), parse_mode='Markdown')

                                    with open(f'temp/pix-{id_user}-{id_p}.json', 'w') as f:
                                        f.write(json.dumps({'tipo': 'gn', 'preco': preco, 'usuario': id_user, 'criado_em': time.time(), 'id_p': id_p}))

                                elif verify == 'key':
                                    with open('config/config_pix.json', 'r') as f:
                                        chave = json.loads(f.read())['pix_key']
                                        suporte = support().replace('_', '\_')
                                    update.message.reply_text(text=f"🛍️ | *Comprar Saldo*\n\nMande o saldo para essa chave pix: {chave}\n\nDepois mande o comprovante para: {suporte}", parse_mode='Markdown')

                                else:
                                    if tipo == 1:
                                        update.message.reply_text(text=no_pix.format(support().replace('_', '\_')), parse_mode='Markdown')
                                    else:
                                        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=no_pix.format(support().replace('_', '\_')), parse_mode='Markdown')

                            else:
                                if tipo == 0:
                                    update.message.reply_text(text='Pare de flodar amigo! Caso realmente queira recarregar seu saldo, faça isso usando o pix gerado, ou aguarde para tentar novamente mais tarde!', parse_mode='Markdown')
                                else:
                                    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='Pare de flodar amigo! Caso realmente queira recarregar seu saldo, faça isso usando o pix gerado, ou aguarde para tentar novamente mais tarde!', parse_mode='Markdown')

                        else:
                            if tipo == 0:
                                update.message.reply_text(text=pay_error_2, parse_mode='Markdown')
                            else:
                                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=pay_error_2, parse_mode='Markdown')
                    else:
                        if tipo == 0:
                            update.message.reply_text(text='Por favor, envie um valor numérico válido.', parse_mode='Markdown')
                        else:
                            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='Por favor, envie um valor numérico válido.', parse_mode='Markdown')

                except Exception as e:
                    verify = verify_default()
                    print(f'Erro interno: {e}')
                    if not verify == '' or asyncio.run(check_config('pix'))[1] == '1':
                        if tipo == 0:
                            update.message.reply_text(text=pay_error_2, parse_mode='Markdown')
                        else:
                            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=pay_error_2, parse_mode='Markdown')
                    else:
                        if tipo == 0:
                            update.message.reply_text(text=no_pix.format(support().replace('_', '\_')), parse_mode='Markdown')
                        else:
                            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=no_pix.format(support().replace('_', '\_')), parse_mode='Markdown')
            else:
                if tipo == 0:
                    update.message.reply_text(text=no_pix.format(support().replace('_', '\_')), parse_mode='Markdown')
                else:
                    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=no_pix.format(support().replace('_', '\_')), parse_mode='Markdown')
        else:
            if tipo == 0:
                update.message.reply_text(text=pay_error_2, parse_mode='Markdown')
            else:
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=pay_error_2, parse_mode='Markdown')
    else:
        if tipo == 0:
            update.message.reply_text(text=denied_text(id_user), parse_mode='Markdown')
        else:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=denied_text(id_user), parse_mode='Markdown')