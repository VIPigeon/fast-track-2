# Определение персонажей со стандартным цветом имён
define p = Character("Вы (Владелец ломбарда)")
define бабушка = Character("Советская бабушка")
define куб = Character("Мужчина с квадратной головой")
define сектант = Character("Сектант в балахоне")
define девочка = Character("Веселая девочка")
define сноб = Character("Сноб-коллекционер")

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
            self.img_tag = img_tag # тег картинки для отображения

# Экран кастомного слайдера для назначения цены
screen offer_slider(min_val, max_val, title_text):
    frame:
        xalign 0.5 yalign 0.5
        xpadding 20 ypadding 15
        background "#111111ee"
        
        vbox:
            spacing 10
            align (0.5, 0.5)
            
            text title_text size 14 color "#ffffff" xalign 0.5
            text "Цена: [slider_value]" size 16 color "#ffcc00" xalign 0.5
            
            bar:
                value VariableValue("slider_value", max_val, step=1)
                xmaximum 150
                xminimum 150
                yalign 0.5
            
            text "Деньги: [player_money]" size 12 color "#aaaaaa" xalign 0.5
            
            textbutton "OK":
                action Return()
                xalign 0.5
                padding (10, 5)
                background "#333333"

# Экран выбора предмета из инвентаря для продажи покупателю
screen inventory_choice(inventory, current_buyer_name):
    frame:
        xalign 0.5 yalign 0.5
        xpadding 20 ypadding 15
        background "#111111ee"
        
        vbox:
            spacing 8
            align (0.5, 0.5)
            
            text "[current_buyer_name] ждет товар:" size 14 color "#ffffff" xalign 0.5
            
            for it in inventory:
                textbutton "[it.name]":
                    action Return(it)
                    xalign 0.5
                    xminimum 180
                    padding (8, 4)
                    background "#333333"
            
            textbutton "Ничего не предлагать":
                action Return(None)
                xalign 0.5
                xminimum 180
                padding (8, 4)
                background "#552222"

label start:
    $ player_money = 100
    $ inventory = []
    
    # Показываем фон
    scene bg background
    
    p "Мой скромный ломбард открыт. В кармане ровно 100 рублей. Посмотрим, кто сегодня зайдет..."
    
    # ==========================================
    # ЭТАП 1: 3 ПРОДАВЦА
    # Структура: (ключ, id_предмета, название, мин_цена, спрайт_персонажа, спрайт_предмета)
    # ==========================================
    $ sellers = [
        ("бабушка", "demon", "Фигурка демона", 20, "granny", "demon"),
        ("куб", "sock", "Левый носок", 10, "square", "sock"),
        ("сектант", "tea", "Б/у чайный пакетик", 5, "fan", "teabag"),
        ("девочка", "tinkoff", "Кошелек Тинькофф", 30, "girl", "wallet"),
        ("сноб", "hat", "Квадратная шляпа", 50, "snob", "hat")
    ]
    
    $ renpy.random.shuffle(sellers)
    $ current_sellers = sellers[:3]
    
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
            бабушка "Внучек, купи греховную вещицу, сырость в суставах унимает!"
        elif s_key == "куб":
            куб "Я геометрически совершенен. Этот предмет тоже имеет углы."
        elif s_key == "сектант":
            сектант "Энергия космоса течет сквозь этот артефакт..."
        elif s_key == "девочка":
            девочка "Привет-привет! Классный ломбард! Купишь штучку?"
        elif s_key == "сноб":
            сноб "Уберите свои засаленные руки. Посмотрите на изыск."

        p "Он(а) предлагает предмет."

        label purchase_attempts:
            if attempts <= 0:
                hide expression s_sprite
                $ renpy.say(current_seller_char, "Ну и ладно, пойду в другой ломбард!")
                jump seller_loop

            if player_money < 1:
                p "У меня совсем не осталось денег... Придется отказаться."
                hide expression s_sprite
                $ renpy.say(current_seller_char, "Эх, бедняк...")
                jump seller_loop

            $ slider_value = 1
            call screen offer_slider(1, player_money, "Предложите цену")
            $ offered_price = slider_value

            if offered_price >= min_price:
                $ player_money -= offered_price
                $ inventory.append(Item(item_id, item_name, item_sprite))
                hide expression s_sprite
                p "Я покупаю предмет за [offered_price] руб."
                $ renpy.say(current_seller_char, "Идеально! Сделка века.")
                jump seller_loop
            else:
                $ attempts -= 1
                $ renpy.say(current_seller_char, "Мало! (Попыток: " + str(attempts) + ")")
                jump purchase_attempts

    label buyers_phase:
        scene bg background
        p "Первая волна посетителей ушла. Теперь пришло время покупателей."

    # ==========================================
    # ЭТАП 2: 2 ПОКУПАТЕЛЯ
    # Структура: (ключ, желаемый_id, макс_цена, спрайт_персонажа)
    # ==========================================
    $ buyers = [
        ("бабушка", "tea", 150, "granny"),
        ("куб", "hat", 300, "square"),
        ("сектант", "demon", 500, "fan"),
        ("девочка", "sock", 200, "girl"),
        ("сноб", "tinkoff", 400, "snob")
    ]
    
    $ renpy.random.shuffle(buyers)
    $ current_buyers = buyers[:2]

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
            сектант "Духи подсказали, что у тебя есть то, что мне нужно..."
        elif b_key == "девочка":
            девочка "Йоу! Показывай витрину, я ищу сокровища!"
        elif b_key == "сноб":
            сноб "Надеюсь, у вас тут не сплошной хлам. Покажите ассортимент."

        if len(inventory) == 0:
            p "К сожалению, у меня пока ничего нет на продажу..."
            hide expression b_sprite
            $ renpy.say(current_buyer_char, "Жаль, пустая трата времени.")
            jump buyer_loop

        call screen inventory_choice(inventory, b_name_str)
        $ selected_item = _return

        if selected_item is None:
            hide expression b_sprite
            $ renpy.say(current_buyer_char, "Ну как хочешь.")
            jump buyer_loop
        else:
            python:
                item_obj = selected_item
                is_desired = (item_obj.id == desired_item_id)
                trade_attempts = 3

            if not is_desired:
                hide expression b_sprite
                if b_key == "бабушка":
                    бабушка "И зачем мне этот срам?"
                elif b_key == "куб":
                    куб "Это не соответствует форме."
                elif b_key == "сектант":
                    сектант "Темные силы недовольны."
                elif b_key == "девочка":
                    девочка "Фу, вообще не прикольно."
                elif b_key == "сноб":
                    сноб "Какая пошлость."
                
                p "Не угадал с товаром."
                jump buyer_loop
            else:
                if b_key == "бабушка":
                    бабушка "Ой, то что надо! Сколько просишь?"
                elif b_key == "куб":
                    куб "То, что нужно. Назови цену."
                elif b_key == "сектант":
                    сектант "Священный артефакт! Какова цена?"
                elif b_key == "девочка":
                    девочка "Вау, офффигенно! За сколько отдашь?"
                elif b_key == "сноб":
                    сноб "Любопытно. Назовите вашу цену."

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
        p "Рабочий день в ломбарде окончен. Пора подводить финансовые итоги."
        
        $ final_score = player_money
        "Итого у вас на руках: [final_score] рублей."

        if final_score < 100:
            p "Я ушел в минус... Кажется, бизнес в ломбарде — это не моё."
        elif final_score >= 100 and final_score <= 300:
            p "Я заработал немного сверху. Неплохо для начала."
        elif final_score > 300 and final_score <= 800:
            p "Отличный результат! Неплохо раскрутился на странных вещицах."
        else:
            p "Я настоящий гений коммерции! Мой ломбард лучший в городе!"

        return