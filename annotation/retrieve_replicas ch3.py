from pathlib import Path
from collections import defaultdict
from lxml import etree


# ======================
# PATHS (ИСПРАВЛЕНО)
# ======================

INPUT_FILES_PATH = Path(
    r'C:\Users\katya\Documents\PyCharmProjects\soviet_plays_PhD\plays_tei\Adult_Stalinist_Plays'
)

OUTPUT_FILES_PATH = Path(
    r'C:\Users\katya\Documents\PyCharmProjects\soviet_plays_PhD\Adult_Stalinist_Plays (Chapter 3)\speech_of_characters'
)


groups = {
    'bosses': [
        ('Макар Дубрава.xml', '#pavel'),  # Павел
        ('Московский характер.xml', '#potapov'),  # Потапов
        ('Рассвет над Москвой.xml', '#kapitolina_andreevna'),  # Капитолина Андреевна
        ('В одном городе.xml', '#ratnikov'),  # Ратников
        ('Глина и фарфор.xml', '#atvasar'),  # Атвасар
        ("Варвара Волкова.xml", '#volkov'),  # Волков
        ("Варвара Волкова.xml", '#volkova'),  # Волкова
        ("Беспокойная должность.xml", '#kolotuhin'),  # Колотухин
        ("Девицы-красавицы.xml", '#avdeev'),  # Авдеев
        ("Не называя фамилий.xml", '#karpo'),  # Карпо
        ("Шестьдесят часов.xml", '#bakurov'),  # Бакуров
        ('Свадьба с приданым.xml', '#pirogov'),  # Пирогов
        ('Калиновая роща.xml', '#romanuk'),  # Романюк
        ('Поют жаворонки.xml', '#pytlevanyi'),  # Пытлеваный
        ('Семья Аллана.xml', '#bairam'),  # Байрам
        ('На новой земле.xml', '#mavlon'),  # Мавлон
        ('Хлеб наш насущный.xml', '#tverdova'),  # Твердова
        ("Камни в печени.xml", '#kaliberov'),  # Калиберов
        ("Камни в печени.xml", '#goroshko'),  # Горошко
        ("Стрекоза.xml", '#nikifore'),  # Никифорэ Перадзе
        ("Новые времена.xml", '#agafonov'),  # Агафонов Василий Степанович — председатель колхоза
        ("Новые времена.xml", '#ivan_ivanovich'),  # Коровин Иван Иванович — член правления колхоза
    ],
    'vrediteli': [
        ('Великая сила.xml', '#milyagin'),  # Милягин
        ('Чужая тень.xml', '#okunev'),  # Окунев (иноагент)
        ('Беспокойная должность.xml', '#almazov'),  # Алмазов
        ('Беспокойная должность.xml', '#kolotuhin'),  # Колотухин
        ('Зеленая улица.xml', '#krutilin'),  # Крутилин
        ("Шестьдесят часов.xml", '#dvoinikov'),  # Двойников, полковник 42 года
        ("Шестьдесят часов.xml", '#gavrilov'),  # кодуктор Гаврилов
        ("Не называя фамилий.xml", '#jora'),  # Жора Поцелуйко
        ("Раки.xml", '#lopouhov'),  # Степан Феофанович Лопоухов – лицо номенклатурное
    ],
    "loznyi_geroi": [
        ("Опасный спутник.xml", '#korchemnyi'),  # Андрей Корчемный
        ("Не называя фамилий.xml", '#poema'),  # Поэма
        ("Не называя фамилий.xml", '#diana'),  # Диана Михайловна
        ("Не называя фамилий.xml", '#bella'),  # Бэлла
        ("Раки.xml", '#lenskii'),  # Ленский
        ("Раки.xml", '#aglaya_ivanovna'),  # Аглая Ивановна
        ("Раки.xml", '#serafima'),  # Серафима
    ],
    'historical_leaders': [
        ('Флаг адмирала.xml', '#ushakov'),  # Ушаков
        ('Борьба без линии фронта.xml', '#peter_kondor'),  # Петер Кондор
        ('Канун грозы.xml', '#prigorov'),  # Пригоров
        ('Канун грозы.xml', '#fedorov'),  # Федоров
        ('Потопленные камни.xml', '#djemal'),  # Джемал
        ('Заговор обреченных.xml', '#ganna'),  # Ганна Лихта
        ('Пролог.xml', "#lenin"),
    ],
    'intelligent': [
        ('Жизнь в цитадели.xml', '#professor_miilas'),  # Профессор Мийлас
        ('Жизнь в цитадели.xml', '#pisatel_lillak'),  # Писатель Лиллак
        ('Жизнь в цитадели.xml', '#arhitektor_vyarihein'),  # Архитектор Вярихейн
        ('Илья Головин.xml', '#golovin'),  # Головин
    ],
    'partorg': [
        ('Макар Дубрава.xml', '#makar'),  # Макар
        ('Макар Дубрава.xml', '#hmara'),  # Хмара
        ('Макар Дубрава.xml', '#orlov'),  # Орлов
        ('Макар Дубрава.xml', '#zinchenko'),  # Зинченко
        ('Московский характер.xml', '#grineva'),  # Гринева
        ('Московский характер.xml', '#krujkova'),  # Кружкова
        ('Московский характер.xml', '#polozova'),  # Полозов
        ('Московский характер.xml', '#drujinin'),  # Дружинин
        ('Рассвет над Москвой.xml', '#kurepin'),  # Курепин
        ('В одном городе.xml', '#petrov'),  # Петров
        ('В одном городе.xml', '#burmin'),  # Бурмин
        ('Глина и фарфор.xml', '#gauimaliet'),  # Гауймалиет
        ('Хлеб наш насущный.xml', '#zorina'),  # Зорина
        ('Хлеб наш насущный.xml', '#rogov'),  # Рогов
        ('Поют жаворонки.xml', '#palanevich'),  # Паланевич
        ('Поют жаворонки.xml', '#kruglik'),  # Круглик
        ('На новой земле.xml', '#adylov'),  # Адылов
        ('Свадьба с приданым.xml', '#muravev'),  # Муравьев
        ('Совесть.xml', '#arkadev'),  # Аркадьев
        ('Незабываемый 1919.xml','#stalin'),  # Сталин
        ('Победители.xml', '#muravev'),  # Муравьев
        ('Великая сила.xml', '#shibanov'),  # Шибанов
        ('Великая сила.xml', '#ostroumov'),  # Остроумов
        ("Варвара Волкова.xml", '#bondarenko'),  # Бондаренко
        ("Беспокойная должность.xml", '#petrov'),  # Петров
        ("Девицы-красавицы.xml", '#moroz'),  # Мороз
        ("Камни в печени.xml", '#kurbatov'),  # Курбатов (прокурор, а не парторг)
        ("Иначе жить нельзя.xml", "#milce"), # Карл Мильце, мастер, секретарь цеховой организации СЕПГ
        ("Иначе жить нельзя.xml", "#bauer"), # Юзеф Бауэр, служащий народной полиции
        ("Стрекоза.xml", '#georgii'),  # Георгий Челидзе
        ("Шестьдесят часов.xml", '#shcherbakova'),  # Щербакова, Плющевского РК партии
        ("Новые времена.xml", '#orehov'),  # Орехов Николай Данилович — секретарь райкома
    ],
    'peredovye': [
        ('Макар Дубрава.xml', '#gavrila'),  # Гаврила
        ('Макар Дубрава.xml', '#trofim'),  # Трофим
        ('Макар Дубрава.xml', '#galya'),  # Галя
        ('Макар Дубрава.xml', '#marfa'),  # Марфа
        ('Макар Дубрава.xml', '#olga'),  # Ольга
        ('Московский характер.xml', '#krivoshein'),  # Кривошеин
        ('Рассвет над Москвой.xml', '#anuta'),  # Анюта
        ('Рассвет над Москвой.xml', '#igor'),  # Игорь
        ('Рассвет над Москвой.xml', '#sanya'),  # Саня
        ('В одном городе.xml', '#klavdiya'),  # Клавдия
        ('Глина и фарфор.xml', '#skulte'),  # Скульте
        ('Совесть.xml', '#uliya'),  # Юлия
        ('Беспокойная должность.xml', '#gruzd'),  # Груздь (вдохновенный очеркист)
        ('Девицы-красавицы.xml', '#sergei'),  # Сергей
        ('Девицы-красавицы.xml', '#masha'),  # Маша
        ("Иначе жить нельзя.xml", "#ruddi"), # Рудди Мильце
        ("Не называя фамилий.xml", '#maksim'),  # Максим
        ("Не называя фамилий.xml", '#vasil'),  # Василь Нетудыхата
        ("Не называя фамилий.xml", '#galya'),  # Галя
        ("Стрекоза.xml", '#marine'),  # Маринэ Перадзе — бригадир, 22 лет
        ("Стрекоза.xml", '#georgii'),  # Георгий Челидзе
        ("Стрекоза.xml", '#makvala'),  # Маквала
        ("Шестьдесят часов.xml", '#voronov'),  # Воронов, начальник станции Разгон, 26 лет
        ("Шестьдесят часов.xml", '#kojun'),  # Кожун, механик водокачки, 22 лет
        ("Шестьдесят часов.xml", '#baushkina'),  # Баюшкина, дежурная по станции Разгон, 20 лет
        ("Опасный спутник.xml", '#dina'),  # Дина Богданова
        ('Хлеб наш насущный.xml', '#rogova'),  # Рогова
        ('Калиновая роща.xml', '#vetrovoi'),  # Ветровой
        ('Поют жаворонки.xml', '#nastya'),  # Настя
        ('Поют жаворонки.xml', '#mikola'),  # Микола
        ('Поют жаворонки.xml', '#katya'),  # Катя
        ('Поют жаворонки.xml', '#pavlina'),  # Павлина
        ('Семья Аллана.xml', '#alty'),  # Алты
        ('На новой земле.xml', '#dehkanbai'),  # Дехканбай
        ('На новой земле.xml', '#hafiza'),  # Хафиза
        ('Свадьба с приданым.xml', '#olga'),  # Ольга
        ('Свадьба с приданым.xml', '#maksim'),  # Максим
        ('Камни в печени.xml', '#ganna'),  # Ганна
        ("Новые времена.xml", '#aleksei'),  # Алексей — сын Агафонова, агроном
    ],
    'prot_na_zapade': [
        ('Голос Америки.xml', '#kidd'),  # Кидд
        ('Голос Америки.xml', '#makdonald'),  # Макдональд
        ('Русский вопрос.xml', '#smit'),  # Смит
    ],
    'uchenyi_patriot': [
        ('Великая сила.xml', '#pavel'),  # Павел Лавров
        ('Чужая тень.xml', '#trubnikov'),  # Трубников
        ('Зеленая улица.xml', '#aleksei'),  # Алексей
        ('Беспокойная должность.xml', '#orlova'),  # Орлова
        ("Новые времена.xml", '#suhov'),  # Сухов Сергей Дмитриевич — агроном, почвовед
        ("Опасный спутник.xml", '#selihov'),  # Николай Селихов
    ],
    'voennyi': [
        ('Победители.xml', '#vinogradov'),  # Виноградов
        ('Победители.xml', '#krivenko'),  # Кривенко
        ('Победители.xml', '#panteleev'),  # Пантелеев
        ('За тех, кто в море.xml', '#haritonov'),  # Харитонов
        ('За тех, кто в море.xml', '#maksimov'),  # Максимов
        ('За тех, кто в море.xml', '#borovskii'),  # Боровский
        ('За тех, кто в море.xml', '#shubin'),  # Шубин
        ('За тех, кто в море.xml', '#lishev'),  # Лишев
    ],
    'revolutsionery': [
        ('Пролог.xml', "#fedor"),
        ('Пролог.xml', "#marfa"),
        ('Пролог.xml', "#ivan"),
        ('Пролог.xml', "#sereja"),
        ('Пролог.xml', "#varvara"),
        ('Пролог.xml', "#filimonov"),  # переходящий солдат
        ('Европейская хроника.xml', "#lund"),
        ('Европейская хроника.xml', "#mariya"),
        ('Европейская хроника.xml', '#lune'),      # Люне
        ('Европейская хроника.xml', '#lund'),      # Лунд
        ('Европейская хроника.xml', '#mariya'),    # Мария Йенсен
        ('Европейская хроника.xml', '#einar'),     # Эйнар (командир партизан)
        ('Европейская хроника.xml', '#ionas'),     # Йонас (рыбак)
        ('Европейская хроника.xml', '#henni'),     # Хенни
        ('Европейская хроника.xml', '#gisted'),    # Гистэд (моряк)
        ('Европейская хроника.xml', '#eva'),       # Ева Лунд
        ('Золотая чума.xml', '#rigo'),        # Риго
        ('Золотая чума.xml', '#zhanton'),      # Жантон
        ('Золотая чума.xml', '#varlen'),      # Варлен
        ('Золотая чума.xml', '#dombrovskii'),  # Домбровский
        ('Золотая чума.xml', '#tumanovskaya'), # Тумановская
        ('Золотая чума.xml', '#madlen'),
    ],
    'vragi_revolutsii': [
        ('Незабываемый 1919.xml', "#deks"),  # Дэкс
        ('Незабываемый 1919.xml', "#egar"),  # Эгар
        ('Незабываемый 1919.xml', "#m-m_butkevich"),  # М-м Буткевич
        ('Заговор обреченных.xml', "#hristina"),  # Христина
        ('Заговор обреченных.xml', "#mak-hill"),  # Мак-Xилл
        ('Заговор обреченных.xml', "#kurtov"),  # Куртов
        ('Заговор обреченных.xml', "#kardinal"),  # Кардинал
        ('Заговор обреченных.xml', "#vastis"),  # Вастис
        ('Заговор обреченных.xml', "#reichel"),  # Рейчел
        ('Борьба без линии фронта.xml', "#tiit_kondor"),  # Тийт Кондор
        ('Борьба без линии фронта.xml', "#hans"),  # Ханс
        ('Канун грозы.xml', "#demchinov"),  # Демчинов
        ('Канун грозы.xml', "#eremin"),  # Еремин
        ('Канун грозы.xml', "#gammer"),  # Гаммер
        ('Канун грозы.xml', "#polozov"),  # Полозов
        ('Канун грозы.xml', "#ispravnik"),  # Исправник
        ('Канун грозы.xml', "#baron"),  # Барон
        ('Канун грозы.xml', "#chelz"),  # Чельз
        ('Канун грозы.xml', "#ministr"),  # Министр
        ('Канун грозы.xml', "#general-gubernator"),  # Генерал-губернатор
        ('Канун грозы.xml', "#treshchevkov"),  # Трещенков
        ('Потопленные камни.xml', "#sadah"),  # Садах
        ('Потопленные камни.xml', "#rait"),  # Райт
        ('Флаг адмирала.xml', "#orfano"),  # Орфано
        ('Флаг адмирала.xml', "#traubridj"),  # Траубридж
        ('Флаг адмирала.xml', "#nelson"),  # Нельсон
        ('Флаг адмирала.xml', "#ledi_gamilton"),  # Леди Гамильтон
        ('Флаг адмирала.xml', "#uord"),  # Уорд
        ('Флаг адмирала.xml', "#ferdinand"),  # Фердинанд
        ('Флаг адмирала.xml', "#karolina"),  # Каролина
        ('Флаг адмирала.xml', "#segur"),  # Сегюр
        ("Иначе жить нельзя.xml", "#franc"), # Франц Мильце
        ("Иначе жить нельзя.xml", "#huter"), # Хютер
        ('Пролог.xml', "#nikolai"),
        ('Пролог.xml', "#vitte"),
        ('Пролог.xml', "#skreblov"),
        ('Пролог.xml', "#belokopytov"),
        ('Пролог.xml', "#petrunkevich"),
        ('Пролог.xml', "#martyanov"),
        ('Пролог.xml', "#ignatii"),
        ('Пролог.xml', "#kruglov"),
        ('Европейская хроника.xml', "#appel"),
        ('Европейская хроника.xml', "#hog"),
        ('Золотая чума.xml', '#desek'),      # маркиз де Сек
        ('Золотая чума.xml', '#rothschild'),  # Ротшильд
    ],
    'zlo_na_zapade': [
        ('Голос Америки.xml', "#parkins"),  # Паркинс
        ('Голос Америки.xml', "#uiler"),  # Уилер
        ('Голос Америки.xml', "#hauston"),  # Хаустон
        ('Голос Америки.xml', "#butler"),  # Бутлер
        ('Русский вопрос.xml', '#guld'),  # Гульд
        ('Русский вопрос.xml', '#makferson'),  # Макферсон
    ],
}


# ======================
# CHECKS
# ======================

def check_duplicate_characters(groups):
    print("\n[CHECK] duplicate characters")

    characters_files = defaultdict(set)

    for group_name in groups:
        for text_name, character_id in groups[group_name]:
            characters_files[character_id].add((text_name, group_name))

    for character_id, character_items in characters_files.items():
        if len(character_items) > 1:
            print(f"WARNING: character {character_id} is used more than once - {character_items}")


def check_files(speech_by_text_by_character, groups):
    print("\n[CHECK] files")

    all_files = set(speech_by_text_by_character.keys())
    used_files = set([text_name for group_name in groups for text_name, _ in groups[group_name]])

    diff = used_files - all_files
    if diff:
        raise Exception(f"ERROR: files {diff} are not present")

    diff = all_files - used_files
    if diff:
        print(f"WARNING: files {diff} are not used!")


def check_characters(speech_by_text_by_character, groups):
    print("\n[CHECK] characters")

    characters_by_text_in_groups = defaultdict(set)
    for group_name in groups:
        for text_name, character_id in groups[group_name]:
            characters_by_text_in_groups[text_name].add(character_id)

    for text_name, speech_by_character in speech_by_text_by_character.items():
        file_characters = set(speech_by_character.keys())
        expected_characters = characters_by_text_in_groups[text_name]

        missing = expected_characters - file_characters
        if missing:
            raise Exception(f"ERROR: characters {missing} are not present in {text_name}")

        unused = file_characters - expected_characters
        if unused:
            print(f"WARNING: file {text_name} has unused characters {unused}")


# ======================
# PARSING
# ======================

def parse_text(file):
    parser = etree.XMLParser(encoding='utf-8', recover=True)
    tree = etree.parse(file, parser=parser)

    etree.strip_elements(tree, 'stage', 'speaker', with_tail=False)

    speech_by_character = defaultdict(list)

    for item in tree.iter('sp'):
        who = item.get('who')

        if not who:
            print(f"WARNING: missing 'who' in {file.name}")
            continue

        etree.strip_tags(item, 'l', 'lg', 'p')

        if item.text:
            speech_by_character[who].append(item.text.strip() + '\n')

    return speech_by_character


def parse_texts():
    speech_by_text_by_character = {}

    print("\n[INFO] Reading files...")

    for file in INPUT_FILES_PATH.rglob('*.xml'):  # ← РЕКУРСИВНО
        speech_by_text_by_character[file.name] = parse_text(file)

    print(f"[INFO] Loaded {len(speech_by_text_by_character)} files")

    return speech_by_text_by_character


# ======================
# MAIN
# ======================

def main(groups):
    speech_by_text_by_character = parse_texts()

    check_duplicate_characters(groups)
    check_files(speech_by_text_by_character, groups)
    check_characters(speech_by_text_by_character, groups)

    speech_by_group = defaultdict(list)

    print("\n[INFO] Collecting speech...")

    for group_name in groups:
        for text_name, character_id in groups[group_name]:
            speech_by_group[group_name].extend(
                speech_by_text_by_character[text_name][character_id]
            )

    # создаём папку (с родителями)
    OUTPUT_FILES_PATH.mkdir(parents=True, exist_ok=True)

    print("\n[INFO] Writing files...")

    for group_name in groups:
        file_path = OUTPUT_FILES_PATH / f"{group_name}.txt"

        with file_path.open(mode='w', encoding='utf-8') as file:
            file.writelines(speech_by_group[group_name])

        print(f"[OK] {file_path}")

    print("\nDONE")


# ======================
# RUN
# ======================

if __name__ == '__main__':
    main(groups)