import os
import re
from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords as nltk_stopwords

OUTPUT_ROWS_NUM = 100

BASE_FOLDER = r"C:\Users\katya\Documents\PyCharmProjects\soviet_plays_PhD\Adult_Stalinist_Plays (Chapter 3)\speech_of_characters_lemm"
PROPER_NOUNS_FOLDER = r"C:\Users\katya\Documents\PyCharmProjects\soviet_plays_PhD\Adult_Stalinist_Plays (Chapter 3)\proper_nouns"
XLSX_PATH = "tf_idf.xlsx"
CUSTOM_STOPWORDS_PATH = "custom_stopwords.txt"


# ------------------------
# 1. Стоп-слова
# ------------------------
def load_custom_stopwords(path):
    if not os.path.exists(path):
        print("Custom stopwords file not found.")
        return set()

    stopwords = set()

    with open(path, encoding='utf-8-sig') as f:
        for line in f:
            word = line.strip().lower()
            if word:
                stopwords.add(word)

    return stopwords


# ------------------------
# 2. Загрузка имён
# ------------------------
def load_proper_nouns(folder):
    proper_nouns = set()

    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder, filename)

            content = Path(filepath).read_text(encoding="utf-8").lower()

            # убираем грамматические пометки mystem {имя,фам,...}
            content = re.sub(r'{.*?}', '', content)

            words = content.split('\n')
            words = [w.strip() for w in words if w.strip()]

            proper_nouns.update(words)

    print(f"Loaded {len(proper_nouns)} proper nouns")
    return proper_nouns


# ------------------------
# 3. Удаление имён из текста
# ------------------------
def remove_proper_nouns_from_text(text, proper_nouns):
    lines = text.lower().split('\n')
    cleaned_lines = []

    for line in lines:
        words = line.split()
        words = [w for w in words if w not in proper_nouns]
        cleaned_lines.append(' '.join(words))

    return '\n'.join(cleaned_lines)


# ------------------------
# 4. Загрузка корпусов
# ------------------------
def load_corpora():
    corpora = {}

    for filename in os.listdir(BASE_FOLDER):
        if filename.endswith(".txt"):
            filepath = os.path.join(BASE_FOLDER, filename)

            content = Path(filepath).read_text(encoding="utf-8")

            doc_name = filename.replace(".txt", "")
            corpora[doc_name] = content

    print(f"Loaded {len(corpora)} documents")
    return corpora


# ------------------------
# 5. TF-IDF
# ------------------------
def calculate_tf_idf():
    corpora = load_corpora()
    proper_nouns = load_proper_nouns(PROPER_NOUNS_FOLDER)

    document_names = []
    documents = []

    for name, text in corpora.items():
        cleaned_text = remove_proper_nouns_from_text(text, proper_nouns)

        # --- отладка (можно потом убрать) ---
        before = len(text.split())
        after = len(cleaned_text.split())
        print(f"{name}: removed {before - after} tokens")

        document_names.append(name)
        documents.append(cleaned_text)

    # --- стоп-слова ---
    russian_stopwords = set(nltk_stopwords.words('russian'))
    custom_stopwords = load_custom_stopwords(CUSTOM_STOPWORDS_PATH)
    all_stopwords = sorted(russian_stopwords.union(custom_stopwords))

    print(f"NLTK stopwords: {len(russian_stopwords)}")
    print(f"Custom stopwords: {len(custom_stopwords)}")
    print(f"Total stopwords used: {len(all_stopwords)}")

    vectorizer = TfidfVectorizer(
        input='content',
        sublinear_tf=True,
        norm='l2',
        smooth_idf=True,
        use_idf=True,
        stop_words=all_stopwords,
        token_pattern=r"(?u)[\w-]+",
        max_df=0.9,
        min_df=1
    )

    X = vectorizer.fit_transform(documents)

    tfidf_df = pd.DataFrame(
        X.toarray(),
        index=document_names,
        columns=vectorizer.get_feature_names_out()
    )

    tfidf_df = tfidf_df.stack().reset_index()
    tfidf_df.columns = ["document", "term", "tf_idf"]

    result_df = (
        tfidf_df
        .sort_values(by=["document", "tf_idf"], ascending=[True, False])
        .groupby("document")
        .head(OUTPUT_ROWS_NUM)
    )

    result_df.to_excel(XLSX_PATH, index=False)
    print("TF-IDF saved to", XLSX_PATH)


# ------------------------
# 6. Запуск
# ------------------------
def main():
    calculate_tf_idf()


if __name__ == "__main__":
    main()