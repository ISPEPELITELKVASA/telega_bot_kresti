
from telegram import ForceReply, Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram.ext import (
    ApplicationBuilder,
    ConversationHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,)
from PIL import Image
from random import *
import tictactoe as tic_tac_toe


MENU_1, MENU_2, WAIT_CODE = range(0, 3)
f_draw = [0,1,2,3,4,5,6,7,8]
win_coord = ((0,1,2), (0,4,8), (0,3,6), (1,4,7), (2,5,8), (2,4,6), (3,4,5), (6,7,8) )

def draw(f_draw2):
    global mat
    mat = '-' * 29 + '\n'
    for i in range(3):
        mat += '   |   ' + str(f_draw2[0+i*3]) + '   |   ' + str(f_draw2[1+i*3]) + '   |   ' + str(f_draw2[2+i*3]) + '   |   ' + '\n'
        mat += '-' * 29 + '\n'
    return mat
    
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')
 
async def game_w_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global mat
    user_data = context.user_data
    user_data['matrix'] = [x for x in range(9)]
    mat = draw(user_data['matrix'])
    query = update.callback_query  
    keyboard = [
        [InlineKeyboardButton(' ', callback_data='0'),
         InlineKeyboardButton(' ', callback_data='1'),
         InlineKeyboardButton(' ', callback_data='2')],
        [InlineKeyboardButton(' ', callback_data='3'),
         InlineKeyboardButton(' ', callback_data='4'),
         InlineKeyboardButton(' ', callback_data='5')],
        [InlineKeyboardButton(' ', callback_data='6'),
         InlineKeyboardButton(' ', callback_data='7'),
         InlineKeyboardButton(' ', callback_data='8')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.answer()
    await query.from_user.send_message(mat, reply_markup=reply_markup)
    
    
    return MENU_2

def check_win(matrix):
    for coords in win_coord:
        if matrix[coords[0]] == matrix[coords[1]] == matrix[coords[2]]:
            return matrix[coords[0]]
    return False

def check_double(matrix):
    X = False
    O = False
    # тут можно вместо o,X оставить одну переменную
    for coords in win_coord:
        if matrix[coords[0]] == matrix[coords[1]] and type(matrix[coords[2]]) == int:
            if matrix[coords[0]] == 'X': X = matrix[coords[2]]
            elif matrix[coords[0]] == 'O': O = matrix[coords[2]]
        elif matrix[coords[1]] == matrix[coords[2]] and type(matrix[coords[0]]) == int:
            if matrix[coords[1]] == 'X': X = matrix[coords[0]]
            elif matrix[coords[1]] == 'O': O = matrix[coords[0]]
        elif matrix[coords[0]] == matrix[coords[2]] and type(matrix[coords[1]]) == int:
            if matrix[coords[0]] == 'X': X = matrix[coords[1]]
            elif matrix[coords[0]] == 'O': O = matrix[coords[1]]
    return X, O

def check_once(matrix):
    O = False
    c = False
    print(matrix)
    for coords in win_coord:
        print(coords)
        if matrix[coords[0]] == 'O' and type(matrix[coords[1]]) == int and type(matrix[coords[2]]) == int:
            O = 'O'
            c = coords[1]
            break
        elif matrix[coords[1]] == 'O' and type(matrix[2]) == int and type(matrix[coords[0]]) == int: 
            O = 'O'
            c = coords[0]
            break
        elif matrix[coords[2]] == 'O' and type(matrix[coords[1]]) == int and type(matrix[coords[0]]) == int:
            O = 'O'
            c = coords[0]
            break
        else:
            continue
    return O, c

def first_hod(matrix):
    fh_h = randint(0,8)
    x = True
    while x:
        if type(matrix[fh_h]) == str:
            fh_h = randint(0,8)
            continue
        else:
            x = False 
    return fh_h

def nichya(matrix):
    for x in matrix:
        if type(x) == int:
            return False
    return True

async def win(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    w_w = "Победил" + str(check_win(context.user_data['matrix']))
    await update.callback_query.edit_message_text(text=w_w)
    return ConversationHandler.END

async def nich_ya(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    w_w = "Ничья"
    await update.callback_query.edit_message_text(text=w_w)
    return ConversationHandler.END

async def hodd1_b(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_data = context.user_data
    matrix = user_data['matrix']
    matrix[int(query.data)] = 'X'
    
    if check_win(matrix):
        await win(update, context)
        print('WIN')
    elif nichya(matrix):
        await nich_ya(update, context)
        print('ничья')
        
    else:
        res = check_double(matrix)
        if res[1]:
            # Ставим ноль на позицию res[1]
            matrix[res[1]] = 'O'
        elif res[0]:
            matrix[res[0]] = 'O'
        else:
            wh_h = check_once(matrix)
            if wh_h[0]:
                matrix[wh_h[1]] = 'O'
            else:
                wh_h = first_hod(matrix)
                matrix[wh_h] = 'O'
        
    mat = draw(matrix)
    keyboard = []
    for n in range(len(matrix)):
        if n % 3 == 0: keyboard.append([])
        if type(matrix[n]) == int:
            keyboard[-1].append(InlineKeyboardButton(' ', callback_data=str(matrix[n])))
        else:
            keyboard[-1].append(InlineKeyboardButton(str(matrix[n]), callback_data=str(matrix[n])))
            
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=mat, reply_markup=reply_markup)

    await query.answer()
    print(matrix)

    if check_win(matrix):
        await win(update, context)
        return ConversationHandler.END
    elif nichya(matrix):
        return ConversationHandler.END
    
    user_data['matrix'] = matrix
    return MENU_2

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    return ConversationHandler.END
    
async def game_w_friend(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print('game_w_friend')
    user_id = update.effective_user.id
    text = f"Ваш код: {user_id}\n" \
                "Введите код друга:"
    await update.effective_message.reply_text(text=text)
    return WAIT_CODE

async def create_buttons(matrix) -> None:
    keyboard = []
    for n in range(len(matrix)):
        if n % 3 == 0: keyboard.append([])
        if type(matrix[n]) == int:
            keyboard[-1].append(InlineKeyboardButton(' ',
                        callback_data="A" + str(matrix[n])))
        else:
            keyboard[-1].append(InlineKeyboardButton(str(matrix[n]),
                        callback_data="A" + str(matrix[n])))
            
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

async def waiting_friend(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    friend_id = update.effective_message.text # user_id противника
    user_id = update.effective_user.id

    if friend_id.isdigit():
        friend_id = int(friend_id)
        friend = context.application.user_data.get(friend_id)
        if friend and friend.get("session_with") == user_id:
            r = randint(0,1)
            cross, zero = (user_id, friend_id) if bool(r) else (friend_id, user_id)
            print('start game')

            session_game = tic_tac_toe.SessionGame(cross, zero)
            context.application.user_data[zero]["session_game"] = session_game
            context.application.user_data[cross]["session_game"] = session_game

            reply_markup = await create_buttons(session_game.matrix)

            (context.application.user_data[cross]["session_game_message"],
             context.application.user_data[zero]["session_game_message"]) = (
                await context.bot.send_message(chat_id=cross,
                                           text="Играйте",
                                           reply_markup=reply_markup),
                await context.bot.send_message(chat_id=zero,
                                           text="Играйте",
                                           reply_markup=reply_markup)
                )
            
            # context.application.user_data[cross]["session_game_message"]
            # await context.application.user_data[cross]["session_game_message"].edit_text(text='NEW')
        else:
            context.user_data['session_with'] = int(friend_id)
            text = "Ожидайте, пока друг активирует ваш код."
            await update.effective_message.reply_text(text=text)
    return ConversationHandler.END

async def clickbutton(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_data = context.user_data
    query = update.callback_query
    btn_num = int(query.data[1])
    session_game: tic_tac_toe.SessionGame = user_data.get("session_game")
    ids=session_game.get_ids()
    if session_game: 
        print('играется', btn_num, )
        move = session_game.move(btn_num, user_id=user_id)
        if move:
            message_cross: Message = context.application.user_data[session_game.cross]["session_game_message"] 
            message_zero: Message = context.application.user_data[session_game.zero]["session_game_message"]
            reply_markup = await create_buttons(session_game.matrix)
            await message_cross.edit_reply_markup(reply_markup=reply_markup)
            await message_zero.edit_reply_markup(reply_markup=reply_markup)
        else:
            print('нельзя ходить')
        win_check = session_game.check_win()
        if win_check:
            message_cross: Message = context.application.user_data[session_game.cross]["session_game_message"] 
            message_zero: Message = context.application.user_data[session_game.zero]["session_game_message"]
            text = "победа " + str(win_check)
            await message_cross.edit_text(text=text)
            await message_zero.edit_text(text=text)
            context.application.user_data[ids[0]]["session_game"] = None
            context.application.user_data[ids[1]]["session_game"] = None
            context.application.user_data[ids[0]]["session_with"] = None
            context.application.user_data[ids[0]]["session_game_message"] = None
            context.application.user_data[ids[1]]["session_with"] = None
            context.application.user_data[ids[1]]["session_game_message"] = None
        else:
            print('Никто не выиграл')
        nichya_f = session_game.nichya()
        if not win_check and nichya_f:
            message_cross: Message = context.application.user_data[session_game.cross]["session_game_message"] 
            message_zero: Message = context.application.user_data[session_game.zero]["session_game_message"]
            await message_cross.edit_text(text='Ничья')
            await message_zero.edit_text(text='Ничья')
            context.application.user_data[ids[0]]["session_game"] = None
            context.application.user_data[ids[1]]["session_game"] = None
            context.application.user_data[ids[0]]["session_with"] = None
            context.application.user_data[ids[0]]["session_game_message"] = None
            context.application.user_data[ids[1]]["session_with"] = None
            context.application.user_data[ids[1]]["session_game_message"] = None
        else:
            print('Ничьи нема')
    else:
        print('ошибка')
        # изменяем сообщение в котором нажата кнопка и сообщаем что игра невозможна.
    print(ids, context.application.user_data)
            
        

# В САМОМ КОНЦЕ ИГРЫ ПРИ НИЧЬЕ ИЛИ ПОБЕДЕ ОДНОГО ИГРОКА ИЗМЕНИТЬ ДВУМ ИГРОКАМ:
# user_data['session_game'] = None

async def startgame_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("start")
    keyboard =  [
        [InlineKeyboardButton('Играть с ботом', callback_data="9"),
         InlineKeyboardButton('Играть с другом', callback_data='10')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите с кем играть", reply_markup=reply_markup)
    return MENU_1

def main():
    # 7905012820:AAHisQIBdLZLUslt-LjLKFTeyS-XF7xnji4
    app = ApplicationBuilder().token("YOUR TOKEN").build()

    app.add_handler(CallbackQueryHandler(clickbutton,
                                pattern="|".join([f"^A{n}$" for n in range(0, 9)])))
    startgame = ConversationHandler(
            entry_points=[CommandHandler("start", startgame_2)],
            states = {
                MENU_1: [
                    CallbackQueryHandler(game_w_bot, pattern="^" + str('9') + "$"),
                    CallbackQueryHandler(game_w_friend, pattern="^" + str('10') + "$")
                ],
                MENU_2: [
                    CallbackQueryHandler(hodd1_b, pattern='^' + str('0') + '$'),
                    CallbackQueryHandler(hodd1_b, pattern='^' + str('1') + '$'),
                    CallbackQueryHandler(hodd1_b, pattern='^' + str('2') + '$'),
                    CallbackQueryHandler(hodd1_b, pattern='^' + str('3') + '$'),
                    CallbackQueryHandler(hodd1_b, pattern='^' + str('4') + '$'),
                    CallbackQueryHandler(hodd1_b, pattern='^' + str('5') + '$'),
                    CallbackQueryHandler(hodd1_b, pattern='^' + str('6') + '$'),
                    CallbackQueryHandler(hodd1_b, pattern='^' + str('7') + '$'),
                    CallbackQueryHandler(hodd1_b, pattern='^' + str('8') + '$')
                ],
                WAIT_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, waiting_friend)]
        },
            fallbacks=[CommandHandler("cancel", cancel),
                    CommandHandler("start_game", startgame_2)]
    )

    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(startgame)

    app.run_polling()

if __name__ == "__main__":
    main()