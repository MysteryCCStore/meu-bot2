from telegram.ext import Updater, InlineQueryHandler, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from bot.cogs.modules.database import *
from bot.cogs.modules.pix_authentication import *
from bot.cogs.modules.pix_key_check import *
from bot.cogs.estatisticas import *
from bot.cogs.ban import *
from bot.cogs.add_cc import *
from bot.cogs.troca import *
from bot.cogs.tools import *
from bot.cogs.add_credits import *
from bot.cogs.add_pix_config import *
from bot.cogs.afilliate import *
from bot.cogs.add_groups import *
from bot.cogs.buy import *
from bot.cogs.cc_main import *
from bot.cogs.delete_account import *
from bot.cogs.dynamic_buttons import *
from bot.cogs.gift import *
from bot.cogs.history import *
from bot.cogs.mix import *
from bot.cogs.profile import *
from bot.cogs.scheduled_tasks import *
from bot.cogs.search import *
from bot.cogs.send import *
from bot.cogs.start import *
from bot.cogs.add_admin import *
from bot.cogs.flags import *
from bot.cogs.users import *
from bot.cogs.delete_card import *
from bot.cogs.backup import *
import json, logging, time, os

# Configuração de Log para ver erros no Discloud
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        with open('config/config.json', 'r', encoding="utf8") as file:
            config = json.loads(file.read())
            token_bot = config['token_bot']
    except Exception as e:
        logger.error(f"Erro ao ler config: {e}")
        return

    print('\nIniciando Bot...')
    
    # Criação única do Updater
    updater = Updater(token_bot, use_context=True)
    dp = updater.dispatcher

    # --- REGISTRO DE HANDLERS ---

    # Admins
    for command in add_admin_command:
        dp.add_handler(CommandHandler(command, add_admin, run_async=True))
    for command in remove_admin_command:
        dp.add_handler(CommandHandler(command, remove_admin, run_async=True))

    # Comandos Principais
    for command in send_command:
        dp.add_handler(CommandHandler(command, send, run_async=True))
        
    for command in start_command:
        # GARANTIA: O handler start está sendo registrado aqui explicitamente
        dp.add_handler(CommandHandler(command, start, run_async=True))

    for command in add_credits:
        dp.add_handler(CommandHandler(command, recarregar, run_async=True))
        
    for command in add_cc:
        dp.add_handler(CommandHandler(command, adicionar_cc, run_async=True))
        
    for command in card:
        dp.add_handler(CommandHandler(command, cartao, run_async=True))

    for command in edit_prices:
        dp.add_handler(CommandHandler(command, editar_precos, run_async=True))

    for command in gift_add:
        dp.add_handler(CommandHandler(command, adicionar_gift, run_async=True))
        
    for command in gift_gen_command:
        dp.add_handler(CommandHandler(command, gerar_gift, run_async=True))
        
    for command in create_table:
        dp.add_handler(CommandHandler(command, criar_mix, run_async=True))
        
    for command in menu_pix_command:
        dp.add_handler(CommandHandler(command, menu_pix, run_async=True))

    # Comandos Avulsos
    dp.add_handler(CommandHandler('configuracoes', flags))
    dp.add_handler(CommandHandler('notificaraqui', add_groups))
    dp.add_handler(CommandHandler('chk', chk))
    dp.add_handler(CommandHandler('separador', separador))
    dp.add_handler(CommandHandler('baixarusuarios', baixar_usuarios))
    dp.add_handler(CommandHandler('resaldo', resaldo))
    dp.add_handler(CommandHandler('deletarcartoes', delete_all_cards))
    dp.add_handler(CommandHandler('deletarccs', delete_all_cards))
    dp.add_handler(CommandHandler('backup', download_backup))
    dp.add_handler(CommandHandler('estatisticas', estatisticas))
    dp.add_handler(CommandHandler('relatorio', estatisticas))
    dp.add_handler(CommandHandler('usuario', usuario))
    dp.add_handler(CommandHandler('usuarios', pesquisarusuario))

    # Callback Queries (Botões)
    dp.add_handler(CallbackQueryHandler(delete_all_cards, pattern='delete_cards_yes'))
    dp.add_handler(CallbackQueryHandler(delete_card, pattern='remove_'))
    dp.add_handler(CallbackQueryHandler(ferramentas, pattern='ferramentas'))
    dp.add_handler(CallbackQueryHandler(edit_mp, pattern='edit_mp'))
    dp.add_handler(CallbackQueryHandler(edit_mp, pattern='default_mp'))
    dp.add_handler(CallbackQueryHandler(edit_mp, pattern='delete_mp'))
    dp.add_handler(CallbackQueryHandler(edit_gn, pattern='edit_gn'))
    dp.add_handler(CallbackQueryHandler(edit_gn, pattern='default_gn'))
    dp.add_handler(CallbackQueryHandler(edit_gn, pattern='delete_gn'))
    dp.add_handler(CallbackQueryHandler(edit_key, pattern='edit_key'))
    dp.add_handler(CallbackQueryHandler(edit_key, pattern='default_key'))
    dp.add_handler(CallbackQueryHandler(edit_key, pattern='delete_key'))
    dp.add_handler(CallbackQueryHandler(menu_pix, pattern='main_pix'))
    dp.add_handler(CallbackQueryHandler(menu_pix_criados, pattern='menu_pix_criados'))
    dp.add_handler(CallbackQueryHandler(add_key_pix_start, pattern='key_menu_pix'))
    dp.add_handler(CallbackQueryHandler(add_gn_pix_start, pattern='gn_menu_pix'))
    dp.add_handler(CallbackQueryHandler(add_mp_pix_start, pattern='mp_menu_pix'))
    dp.add_handler(CallbackQueryHandler(add_pix, pattern='menu_pix'))
    dp.add_handler(CallbackQueryHandler(add_key_pix0, pattern='criar_pix_key'))
    dp.add_handler(CallbackQueryHandler(recarregar, pattern='r_'))
    dp.add_handler(CallbackQueryHandler(confirmar_compra_mix, pattern='comprarmix_'))
    dp.add_handler(CallbackQueryHandler(comprar_mix, pattern='>'))
    dp.add_handler(CallbackQueryHandler(ban, pattern='ban_'))
    dp.add_handler(CallbackQueryHandler(unban, pattern='unban_'))
    dp.add_handler(CallbackQueryHandler(usuario, pattern='usuario_'))
    dp.add_handler(CallbackQueryHandler(menu, pattern='termos'))
    dp.add_handler(CallbackQueryHandler(cancelar_compra, pattern='cancelar_compra'))
    dp.add_handler(CallbackQueryHandler(preco_unitaria, pattern='cancelar_edicao1'))
    dp.add_handler(CallbackQueryHandler(preco_mix, pattern='cancelar_edicao2'))
    dp.add_handler(CallbackQueryHandler(unitaria, pattern='unitaria'))
    dp.add_handler(CallbackQueryHandler(adicionar_saldo, pattern='adicionar_saldo'))
    dp.add_handler(CallbackQueryHandler(aleatoria, pattern='aleatoria'))
    dp.add_handler(CallbackQueryHandler(baixar_historico, pattern='baixar_historico'))
    dp.add_handler(CallbackQueryHandler(encerrar_conta, pattern='encerrar_conta'))
    dp.add_handler(CallbackQueryHandler(menu, pattern='main'))
    dp.add_handler(CallbackQueryHandler(historico, pattern='m3'))
    dp.add_handler(CallbackQueryHandler(informacoes, pattern='m2'))
    dp.add_handler(CallbackQueryHandler(comprar, pattern='m1'))
    dp.add_handler(CallbackQueryHandler(mix, pattern='mix'))
    dp.add_handler(CallbackQueryHandler(afiliados, pattern='afiliados'))
    dp.add_handler(CallbackQueryHandler(encerrar_conta, pattern='encerrar_conta_sim'))
    dp.add_handler(CallbackQueryHandler(preco_mix, pattern='editar_mix'))
    dp.add_handler(CallbackQueryHandler(preco_unitaria, pattern='editar_unitaria'))
    dp.add_handler(CallbackQueryHandler(editar_precos, pattern='editar_precos'))
    dp.add_handler(CallbackQueryHandler(cancel, pattern='cancelar_criacao_pix_mp'))
    dp.add_handler(CallbackQueryHandler(send, pattern='delete_message'))
    dp.add_handler(CallbackQueryHandler(add_admin_button, pattern='add_admin_'))
    dp.add_handler(CallbackQueryHandler(remove_admin_button, pattern='rm_admin_'))
    dp.add_handler(CallbackQueryHandler(flags, pattern='flag_'))
    dp.add_handler(CallbackQueryHandler(search, pattern='search'))
    dp.add_handler(CallbackQueryHandler(troca, pattern='troca'))
    dp.add_handler(CallbackQueryHandler(estatisticas, pattern='stats_'))

    # Conversation Handlers (Pix)
    conv_handler_gn = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_gn_pix, pattern='criar_pix_gn')],
        states={
            STEP1: [MessageHandler(Filters.document & ~Filters.command, add_gn_pix2)],
            STEP2: [MessageHandler(Filters.text & ~Filters.command, add_gn_pix3)],
            STEP3: [MessageHandler(Filters.text & ~Filters.command, add_gn_pix4)],
            STEP4: [MessageHandler(Filters.text & ~Filters.command, add_gn_pix5)]
        },
        fallbacks=[CallbackQueryHandler(cancel, pattern='cancelar_criacao_pix_gn')],
    )

    conv_handler_mp = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_mp_pix, pattern='criar_pix_mp')],
        states={
            STEP1: [MessageHandler(Filters.text & ~Filters.command, add_mp_pix2)],
        },
        fallbacks=[CallbackQueryHandler(cancel, pattern='cancelar_criacao_pix_mp')],
    )

    conv_handler_key = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_key_pix1, pattern='pix_cpf'),
                      CallbackQueryHandler(add_key_pix1, pattern='pix_cnpj'),
                      CallbackQueryHandler(add_key_pix1, pattern='pix_email'),
                      CallbackQueryHandler(add_key_pix1, pattern='pix_telefone'),
                      CallbackQueryHandler(add_key_pix1, pattern='pix_aleatoria')],
        states={
            STEP1: [MessageHandler(Filters.text & ~Filters.command, add_key_pix2)],
        },
        fallbacks=[CallbackQueryHandler(cancel, pattern='cancelar_criacao_pix_key')],
    )

    dp.add_handler(conv_handler_gn)
    dp.add_handler(conv_handler_mp)
    dp.add_handler(conv_handler_key)

    # Job Queue (Tarefas Agendadas)
    j = updater.job_queue
    try:
        j.run_repeating(payment_checker, interval=120, first=120)
    except: pass
    try:
        j.run_repeating(scheduled_tasks, interval=3600, first=3600)
    except: pass
    try:
        j.run_repeating(backup_task, interval=43200, first=43200)
    except: pass

    # Outros Handlers
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_handler(MessageHandler(Filters.document.mime_type("text/plain"), bulk_ccs))
    dp.add_handler(MessageHandler(Filters.document.mime_type("application/vnd.sqlite3"), upload_backup))
    dp.add_handler(CallbackQueryHandler(dynamic_buttons))
    dp.add_handler(MessageHandler(Filters.caption & Filters.photo, send))
    dp.add_handler(MessageHandler(Filters.caption & Filters.video, send))
    dp.add_handler(MessageHandler(Filters.caption & Filters.document, send))
    dp.add_handler(MessageHandler(Filters.caption & Filters.audio, send))

    # INICIO DO BOT
    print("Polling iniciado...")
    updater.start_polling(poll_interval=1.0, timeout=20)
    updater.idle()

if __name__ == '__main__':
    main()