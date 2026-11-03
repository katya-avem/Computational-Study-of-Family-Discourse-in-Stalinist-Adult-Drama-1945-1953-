import os
import re
from pathlib import Path

# Задаем исходные пути к папкам с пьесами
SOURCE_THAW = Path(
    r"C:\soviet_plays_PhD\Adult_Thaw_Plays (Chapter 4)\04_lemmatize"
)
SOURCE_STALIN = Path(
    r"C:\soviet_plays_PhD\Adult_Stalinist_Plays (Chapter 3)\04_lemmatize"
)

# Корневая папка для сохранения сегментов
BASE_OUTPUT_DIR = Path(
    r"C:\soviet_plays_PhD\cut_into_segments"
)

OUTPUT_THAW_DIR = BASE_OUTPUT_DIR / "Thaw"
OUTPUT_STALIN_DIR = BASE_OUTPUT_DIR / "Stalinism"

# Основные параметры нарезки
TARGET_WORD_COUNT = 1000  # Целевое количество слов в сегменте
MIN_REMAINING = 500  # Порог для "хвоста": если меньше, объединяем с предыдущим


def split_text_into_segments(words, target_count=1000, min_remaining=500):
    """Разбивает список слов на сегменты с учетом минимального остатка."""
    total_words = len(words)
    if total_words == 0:
        return []

    # Если весь файл меньше порога объединения + целевого размера
    if total_words < target_count + min_remaining:
        return [" ".join(words)]

    segments = []
    i = 0
    while i < total_words:
        remaining = total_words - i

        # Если оставшийся кусочек слишком маленький, присоединяем его к последнему сегменту
        if remaining < target_count + min_remaining and segments:
            segments[-1] += " " + " ".join(words[i:])
            break
        else:
            segment_words = words[i : i + target_count]
            segments.append(" ".join(segment_words))
            i += target_count

    return segments


def clean_play_name(filename_str):
    """Удаляет расширения (.xml.txt, .txt, .xml) и очищает имя."""
    clean_name = re.sub(
        r"(\.xml)?\.txt$", "", filename_str, flags=re.IGNORECASE
    )
    clean_name = re.sub(r"\.xml$", "", clean_name, flags=re.IGNORECASE)
    return clean_name.strip()


def process_folder(source_dir, output_dir, label):
    """Обрабатывает одну папку (включая все вложенные подпапки) и сохраняет сегменты."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # rglob("*.txt") рекурсивно ищет во всех вложенных подпапках
    txt_files = list(source_dir.rglob("*.txt"))

    if not txt_files:
        print(
            f"[{label}] В папке {source_dir} и её подпапках не найдено .txt файлов."
        )
        return

    print(
        f"=== [{label}] Найдено файлов: {len(txt_files)}. Начинаем обработку... ==="
    )

    for file_path in txt_files:
        play_name = clean_play_name(file_path.name)

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        words = text.split()
        if not words:
            print(f"  Пропущен пустой файл: {file_path.name}")
            continue

        segments = split_text_into_segments(
            words,
            target_count=TARGET_WORD_COUNT,
            min_remaining=MIN_REMAINING,
        )

        for idx, segment_content in enumerate(segments, start=1):
            out_filename = f"{play_name}_{idx}.txt"
            out_path = output_dir / out_filename

            with open(out_path, "w", encoding="utf-8") as out_f:
                out_f.write(segment_content)

        print(
            f"  Пьеса '{play_name}': слов — {len(words)}, сегментов — {len(segments)}"
        )

    print(f"Готово! Сегменты для [{label}] сохранены в: {output_dir}\n")


def process_all_plays():
    # 1. Обработка Оттепели
    process_folder(SOURCE_THAW, OUTPUT_THAW_DIR, "Оттепель")

    # 2. Обработка Сталинизма (включая все подпапки)
    process_folder(SOURCE_STALIN, OUTPUT_STALIN_DIR, "Сталинизм")


if __name__ == "__main__":
    process_all_plays()