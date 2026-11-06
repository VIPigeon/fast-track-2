# Определение персонажей со стандартными именами
define p = Character("Вы (Владелец хламбарда)")
define бабушка = Character("Бабушка")
define куб = Character("Мужчина с квадратной головой")
define сектант = Character("Мужчина в балахоне")
define девочка = Character("Веселая девочка")
define сноб = Character("Коллекционер")

# Объявление изображений (спрайтов) с учетом размеров
image bg background = "background.png"

# Персонажи (размер 150x64, позиционируем по центру снизу)
image granny = "granny.png"
image girl = "girl.png"
image square = "square.png"
image snob = "snob.png"
image fan = "fan.png"

# Предметы (размер 64x64)
image hat = "hat.png"
image demon = "demon.png"
image teabag = "teabag.png"
image wallet = "wallet.png"
image sock = "sock.png"

init python:
    # Класс для предметов
    class Item:
        def __init__(self, id, name, img_tag):
            self.id = id
            self.name = name
            self.img_tag = img_tag


# Экран увеличенного слайдера для назначения цены
screen offer_slider(min_val, max_val, title_text):
    frame:
        xalign 0.5 yalign 0.5
        # Увеличили отступы рамки, чтобы окно стало больше и просторнее
        xpadding 30 ypadding 22
        background "#111111ee"
        
        vbox:
            spacing 12
            align (0.5, 0.5)
            
            text title_text size 14 color "#ffffff" xalign 0.5
            text "Цена: [slider_value]" size 16 color "#ffcc00" xalign 0.5
            
            bar:
                value VariableValue("slider_value", max_val, step=1)
                # value FieldValue(
                #     slider_adjustment,
                #     "value",
                #     range=max_val - min_val,
                #     step=1
                # )
                # Увеличили ширину ползунка с 150 до 230 пикселей
                xmaximum 230
                xminimum 230
                yalign 0.5
            
            text "Деньги: [player_money]" size 12 color "#aaaaaa" xalign 0.5
            # text "DEBUG: min=[min_val], max=[max_val]" xalign 0.5 yalign 0.1
            
            textbutton "OK":
                action Return()
                xalign 0.5
                padding (14, 6)
                background "#333333"

# Экран выбора предмета из инвентаря для продажи покупателю
screen inventory_choice(inventory, current_buyer_name):
    frame:
        xalign 0.5 yalign 0.5
        xpadding 25 ypadding 18
        background "#111111ee"
        
        vbox:
            spacing 10
            align (0.5, 0.5)
            
            text "[current_buyer_name] ждет товар:" size 14 color "#ffffff" xalign 0.5
            
            for it in inventory:
                textbutton "[it.name]":
                    action Return(it)
                    xalign 0.5
                    xminimum 200
                    padding (10, 5)
                    background "#333333"
            
            # При выборе "Ничего" возвращаем специальный шестой предмет-пустышку
            textbutton "Ничего не предлагать":
                action Return(Item("nothing", "Ничего", "none"))
                xalign 0.5
                xminimum 200
                padding (10, 5)
                background "#552222"

label start:
    $ player_money = 100
    $ inventory = []
    
    # Показываем фон
    scene bg background
    
    p "Мой скромный хламбард открыт. В кармане ровно 100 рублей. Посмотрим, кто сегодня зайдет..."
    
    # Полный список всех 5 персонажей с их параметрами продавцов
    $ master_sellers = [
        ("бабушка", "demon", "Фигурка демона", 30, "granny", "demon"),
        ("куб", "sock", "Левый носок", 20, "square", "sock"),
        ("сектант", "tea", "Б/у чайный пакетик", 10, "fan", "teabag"),
        ("девочка", "tinkoff", "Кошелек Тинькофф", 15, "girl", "wallet"),
        ("сноб", "hat", "Квадратная шляпа", 50, "snob", "hat")
    ]
    
    # Перемешиваем весь список один раз (гарантирует уникальность персонажей)
    $ renpy.random.shuffle(master_sellers)
    
    # Первые 3 персонажа — продавцы
    $ current_sellers = master_sellers[:3]
    # Оставшиеся 2 персонажа — покупатели
    $ remaining_buyers_keys = [item[0] for item in master_sellers[3:]]
    
    python:
        seller_objects = {
            "бабушка": бабушка,
            "куб": куб,
            "сектант": сектант,
            "девочка": девочка,
            "сноб": сноб
        }
        seller_display_names = {
            "бабушка": "Советская бабушка",
            "куб": "Мужчина с квадратной головой",
            "сектант": "Сектант в балахоне",
            "девочка": "Веселая девочка",
            "сноб": "Сноб-коллекционер"
        }
        
        buyers_data_dict = {
            "бабушка": ("tea", 50, "granny"),
            "куб": ("hat", 500, "square"),
            "сектант": ("demon", 999, "fan"),
            "девочка": ("sock", 200, "girl"),
            "сноб": ("tinkoff", 400, "snob")
        }

    label seller_loop:
        python:
            if len(current_sellers) == 0:
                renpy.jump("buyers_phase")
            
            s_data = current_sellers.pop(0)
            s_key = s_data[0]
            item_id = s_data[1]
            item_name = s_data[2]
            min_price = s_data[3]
            s_sprite = s_data[4]
            item_sprite = s_data[5]
            
            current_seller_char = seller_objects[s_key]
            attempts = 3

        # Показываем фон и персонажа на экране 267x150
        scene bg background
        show expression s_sprite at center
        with dissolve

        if s_key == "бабушка":
            бабушка "Внучек, купи эту проклятую игрушку. Уверена, какие-нибудь сектанты ее оценят"
        elif s_key == "куб":
            куб "Хочу продать ЛЕВЫЙ носок!"
        elif s_key == "сектант":
            сектант "Продам чайный пакетик. Я им почти не пользовался"
        elif s_key == "девочка":
            девочка "Привет-привет! Этот кошелек мне не нужен, потому что такого банка больше нет — а значит, хранить там деньги нельзя"
        elif s_key == "сноб":
            сноб "Эта квадратная шляпа не налезет ни на одну голову. Может, тебе нужно?."

        p "Предлагает предмет: [item_name]"

        label purchase_attempts:
            if attempts <= 0:
                hide expression s_sprite
                $ renpy.say(current_seller_char, "Ну и ладно, пойду в другой хламбард!")
                jump seller_loop

            if player_money < 1:
                p "У меня совсем не осталось денег... Придется отказаться."
                hide expression s_sprite
                $ renpy.say(current_seller_char, "Эх, бедняк...")
                jump seller_loop

            $ slider_value = 1

            # "DEBUG: player_money = [player_money]"
            # "DEBUG: slider_value = [slider_value]"
            # $ renpy.restart_interaction()

            $ slider_value = 1
            # я сдаюсь  
            # call screen reset_slider(1, player_money, "")

            call screen offer_slider(1, player_money, "Предложите цену")
            $ offered_price = slider_value

            if offered_price >= min_price:
                $ player_money -= offered_price
                $ inventory.append(Item(item_id, item_name, item_sprite))
                hide expression s_sprite
                p "Я покупаю предмет за [offered_price] руб."

                $ renpy.say(current_seller_char, "Продано!")
                if s_key == "бабушка":
                    $ renpy.say(current_seller_char, "На самом деле мне 16")
                jump seller_loop
            else:
                $ attempts -= 1
                $ renpy.say(current_seller_char, "Мало! (Терпение: " + str(attempts) + ")")
                jump purchase_attempts

    label buyers_phase:
        scene bg background
        p "Первая волна посетителей ушла. Сейчас придут еще два человека в качестве покупателей"

    python:
        current_buyers = []
        for b_key in remaining_buyers_keys:
            b_info = buyers_data_dict[b_key]
            current_buyers.append((b_key, b_info[0], b_info[1], b_info[2]))

    label buyer_loop:
        python:
            if len(current_buyers) == 0:
                renpy.jump("game_end")
            
            b_data = current_buyers.pop(0)
            b_key = b_data[0]
            desired_item_id = b_data[1]
            max_payout = b_data[2]
            b_sprite = b_data[3]
            
            current_buyer_char = seller_objects[b_key]
            b_name_str = seller_display_names[b_key]

        scene bg background
        show expression b_sprite at center
        with dissolve

        if b_key == "бабушка":
            бабушка "Внучек, а есть ли у тебя что-нибудь интересное?"
        elif b_key == "куб":
            куб "Приветствую. Покажи свои товары. Есть ли что-то стоящее?"
        elif b_key == "сектант":
            сектант "Йоу"
        elif b_key == "девочка":
            девочка "Привет! Что у вас есть?"
        elif b_key == "сноб":
            сноб "Я ищу раритетный хлам. У вас одна попытка."

        if len(inventory) == 0:
            p "К сожалению, у меня пока нет предметов на продажу..."
            hide expression b_sprite
            $ renpy.say(current_buyer_char, "Жаль, пустая трата времени.")
            jump buyer_loop

        call screen inventory_choice(inventory, b_name_str)
        $ selected_item = _return

        python:
            item_obj = selected_item
            # Проверяем, выбрал ли игрок шестой предмет ("nothing")
            is_nothing = (item_obj.id == "nothing")
            is_desired = (not is_nothing and item_obj.id == desired_item_id)
            trade_attempts = 3

        # Если игрок выбрал "Ничего не предлагать" (шестой предмет)
        if is_nothing:
            hide expression b_sprite
            $ renpy.say(current_buyer_char, "Эх, ну не очень-то и хотелось.")
            jump buyer_loop

        if not is_desired:
            hide expression b_sprite
            if b_key == "бабушка":
                бабушка "meh"
            elif b_key == "куб":
                куб "Не, я не смогу этим прикрыть свою ужасную голову"
            elif b_key == "сектант":
                сектант "Я конечно должен его взять, но и ты не офигевай."
            elif b_key == "девочка":
                девочка "Не, из этого куклу не сделаешь"
            elif b_key == "сноб":
                сноб "В этом нет коллекционной ценности"
            
            p "Не угадал с товаром."
            jump buyer_loop
        else:
            if b_key == "бабушка":
                бабушка "Молодешь недооценивает ПОТЕНЦИАЛ ЧАЙНОГО ПАКЕТИКА. Этот можно еще использовать и использовать"
            elif b_key == "куб":
                куб "Да эта шляпа идеально подходит под мою голову!"
            elif b_key == "сектант":
                сектант "Да это же демон старения! Он не должен был оказаться в этом месте... Я его должен взять"
            elif b_key == "девочка":
                девочка "Этот носок идеально подходит для моего кукольного спектакля"
            elif b_key == "сноб":
                сноб "Да это же раритетный кошелек! Таких больше не выпускают"

            label selling_trade:
                if trade_attempts <= 0:
                    hide expression b_sprite
                    $ renpy.say(current_buyer_char, "Слишком дорого! Я ухожу.")
                    jump buyer_loop

                $ slider_value = 50
                call screen offer_slider(1, 1000, "Назначьте цену продажи")
                $ ask_price = slider_value

                if ask_price <= max_payout:
                    $ player_money += ask_price
                    $ inventory.remove(item_obj)
                    hide expression b_sprite
                    $ renpy.say(current_buyer_char, "По рукам!")
                    p "Я продал предмет за [ask_price] руб. Осталось денег: [player_money]."
                    jump buyer_loop
                else:
                    $ trade_attempts -= 1
                    $ renpy.say(current_buyer_char, "Дорого! (Попыток: " + str(trade_attempts) + ")")
                    jump selling_trade

    # ==========================================
    # ЭТАП 3: ФИНАЛ И ИТОГИ
    # ==========================================
    label game_end:
        scene bg background
        p "Рабочий день в хламбарде окончен. Пора подводить финансовые итоги."
        
        $ final_score = player_money
        $ player_money = 100
        "Итого у вас на руках: [final_score] рублей."

        if final_score < 100:
            p "Я ушел в минус... Кажется, бизнес в хламбарде — это не моё."
        elif final_score >= 100 and final_score <= 150:
            p "Я заработал немного сверху. Неплохо для начала."
        elif final_score > 150 and final_score <= 500:
            p "Отличный результат! Неплохо раскрутился на мусоре."
        else:
            p "Я настоящий гений! Мой хламбард лучший в городе!"

        return