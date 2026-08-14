import os
from collections import Counter
import math
from tqdm import tqdm
import re

import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords

from pymystem3 import Mystem
m = Mystem()

# --- STOPWORDS ---
russian_stopwords = set(stopwords.words("russian"))
custom_stopwords = {"это", "тот", "такой", "весь", "сам", "ещё", "э", "ой", "хоч", "гос", "-", "вастис", "хо-хо", "эммочка", "жаньки", "вай", "сей", "иваныч", "мишенька", "почему", "баторий", "бэллочка", "андрюша", "тбилиси", "ваш"}
all_stopwords = russian_stopwords | custom_stopwords

# --- PATHS ---
path_female = os.path.join("output", "female.txt")
path_male   = os.path.join("output", "male.txt")
path_names  = r"C:\Users\katya\Documents\PyCharmProjects\soviet_plays_PhD\Adult_Stalinist_Plays (Chapter 3)\proper_nouns"

# --- FUNCTIONS ---

# Чтение имен из папки
def read_names_from_folder(folder_path):
    names = set()
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), encoding="utf-8") as f:
                text = f.read().lower()
                words = re.findall(r'\b[а-яёА-ЯЁ-]+\b', text)
                names.update(words)
    return names

# Чтение текста и очистка слов
def read_and_clean_words(filepath, names_set):
    with open(filepath, encoding="utf-8") as f:
        text = f.read().lower()
    # Убираем все символы, кроме букв и дефисов
    words = re.findall(r'\b[а-яё-]+\b', text)
    # Убираем имена собственные
    words = [w for w in words if w not in names_set]
    return words

# Лемматизация через Mystem
def lemmatize_words(words):
    text = ' '.join(words)
    lemmas = m.lemmatize(text)
    # Убираем пустые строки и пробелы
    return [w for w in lemmas if w.strip() and re.match(r'[а-яё-]+$', w)]

# Z-score
def compute_z_score(f1, f2, n1, n2):
    p = (f1 + f2) / (n1 + n2)
    sigma = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    return (f1 / n1 - f2 / n2) / sigma if sigma != 0 else 0

# --- READ NAMES ---
print("Читаем имена собственные...")
names_set = read_names_from_folder(path_names)

# --- READ, CLEAN AND LEMMATIZE WORDS ---
print("Читаем женские реплики...")
words_female = lemmatize_words(read_and_clean_words(path_female, names_set))

print("Читаем мужские реплики...")
words_male = lemmatize_words(read_and_clean_words(path_male, names_set))

# --- COUNT FREQUENCIES ---
counter_female = Counter(words_female)
counter_male = Counter(words_male)

n1 = len(words_female)
n2 = len(words_male)

# --- ALL UNIQUE WORDS (STOPWORDS REMOVED) ---
all_words = {w for w in counter_female | counter_male if w not in all_stopwords}

# --- Z-ANALYSIS ---
results = []
for word in tqdm(all_words, desc="Calculating Z-scores"):
    f1 = counter_female.get(word, 0)
    f2 = counter_male.get(word, 0)
    z = compute_z_score(f1, f2, n1, n2)
    results.append((word, f1, f2, z))

# --- SORT BY |Z| ---
results.sort(key=lambda x: abs(x[3]), reverse=True)

# --- SAVE RESULTS ---
with open("z_analysis_results_gender_mystem.tsv", "w", encoding="utf-8") as out:
    out.write("word\tfreq_female\tfreq_male\tz_score\n")
    for word, f1, f2, z in results:
        out.write(f"{word}\t{f1}\t{f2}\t{z:.3f}\n")

# --- VISUALIZATION ---
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("z_analysis_results_gender_mystem.tsv", sep="\t")
df = df[(df['freq_female'] + df['freq_male']) >= 5]

top_female = df[df['z_score'] > 0].sort_values(by="z_score", ascending=False).head(30)
top_male = df[df['z_score'] < 0].sort_values(by="z_score").head(30)

def plot_z_words(df, title, color):
    plt.figure(figsize=(8, 10))
    plt.barh(df['word'], df['z_score'], color=color)
    plt.xlabel("Z-score")
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

plot_z_words(top_female, "Keywords characteristic of FEMALE lines", color="darkred")
plot_z_words(top_male, "Keywords characteristic of MALE lines", color="navy")