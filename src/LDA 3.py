#LDA_на_токенах

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import nltk
import spacy
import matplotlib.cm as cm
import pandas as pd
import gensim
from gensim import corpora
from gensim.models import LdaModel, CoherenceModel
from nltk.corpus import stopwords

# nltk.download('punkt')
# nltk.download('stopwords')

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from gensim import corpora
from gensim.models import LdaModel, CoherenceModel
import multiprocessing


def read_texts(folder):
    texts, filenames = [], []
    for file_path in Path(folder).glob('*.txt'):
        with file_path.open('r', encoding='utf-8') as f:
            tokens = f.read().split()  # тексты уже лемматизированы
            texts.append(tokens)
        filenames.append(file_path.stem.strip().lower())
    return texts, filenames


def get_topic_distribution(texts, dictionary, lda_model):
    dists = []
    for text in texts:
        bow = dictionary.doc2bow(text)
        topic_dist = lda_model.get_document_topics(bow, minimum_probability=0.0)
        topic_dist = [prob for _, prob in sorted(topic_dist)]
        dists.append(topic_dist)
    return dists


def plot_lda_topics(lda_model, num_words=15):
    num_topics = lda_model.num_topics
    topics = lda_model.show_topics(num_topics=num_topics, num_words=num_words, formatted=False)

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()

    for i, (topic_id, topic) in enumerate(topics):
        words, weights = zip(*topic)
        axes[i].barh(words, weights, color='#4B8BBE')
        axes[i].invert_yaxis()
        axes[i].set_title(f"Topic {topic_id + 1}")

        print(f"\nTopic {topic_id + 1}:")
        for w, p in topic:
            print(f"{w:<20} {p:.4f}")

    plt.tight_layout()
    plt.show()


def main():
    PLAYS_FOLDER = r"C:\Users\katya\Documents\PyCharmProjects\soviet_plays_PhD\Adult_Stalinist_Plays (Chapter 3)\stalinist_plays_lemm"
    METADATA_PATH = r"C:\Users\katya\Documents\PyCharmProjects\soviet_plays_PhD\dataframe.csv"

    # -----------------------
    # 1. Чтение текстов
    # -----------------------
    texts, filenames = read_texts(PLAYS_FOLDER)

    # -----------------------
    # 2. Чтение метаданных
    # -----------------------
    metadata = pd.read_csv(METADATA_PATH, encoding='utf-8')
    metadata['filename'] = metadata['filename'].astype(str).str.strip().str.lower()
    metadata['year'] = pd.to_numeric(metadata['year'], errors='coerce')
    metadata = metadata.dropna(subset=['year'])

    metadata['decade'] = (metadata['year'] // 10) * 10

    df = pd.DataFrame({'filename': filenames, 'tokens': texts})
    merged = pd.merge(df, metadata, on='filename', how='inner')

    print(f"Совпало файлов: {len(merged)}")

    if merged.empty:
        raise ValueError("Нет совпадений с метаданными!")
    domain_stopwords = {
        "стрекоза", "поэма", "мол", "диана", "да-да", "аркадиевич", "коль", "горка", "ль", "ежели", "-а"
    }

    merged['tokens'] = merged['tokens'].apply(
        lambda tokens: [t for t in tokens if t not in domain_stopwords]
    )
    # -----------------------
    # 3. LDA
    # -----------------------
    dictionary = corpora.Dictionary(merged['tokens'])
    dictionary.filter_extremes(no_below=5, no_above=0.5)

    corpus = [dictionary.doc2bow(text) for text in merged['tokens']]

    lda_model = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=4,
        passes=25,
        iterations=500,
        alpha='auto',
        eta='auto',
        random_state=89
    )

    coherence_model = CoherenceModel(
        model=lda_model,
        texts=merged['tokens'],
        dictionary=dictionary,
        coherence='c_v'
    )

    print("Coherence Score:", coherence_model.get_coherence())

    # -----------------------
    # 4. График топиков
    # -----------------------
    plot_lda_topics(lda_model)

    # -----------------------
    # 5. Распределение по десятилетиям
    # -----------------------
    topic_dists = get_topic_distribution(merged['tokens'], dictionary, lda_model)
    topic_array = np.array(topic_dists)

    merged_topics = merged.copy()
    for i in range(4):
        merged_topics[f'Topic_{i + 1}'] = topic_array[:, i]

    decade_distribution = merged_topics.groupby('decade')[
        [f'Topic_{i + 1}' for i in range(4)]
    ].mean()

    colors = cm.get_cmap('tab10', 4).colors

    plt.figure(figsize=(10, 6))
    x = np.arange(len(decade_distribution.index))
    width = 0.2

    print("\nКоличество пьес по десятилетиям:")

    decade_counts = merged['decade'].value_counts().sort_index()

    for decade, count in decade_counts.items():
        print(f"{decade}-е годы: {count} пьес")

    for i in range(4):
        plt.bar(
            x + i * width,
            decade_distribution.iloc[:, i],
            width=width,
            color=colors[i],
            label=f'Topic {i + 1}'
        )

    plt.xticks(x + width * 1.5, decade_distribution.index)
    plt.xlabel("Decade")
    plt.ylabel("Average topic proportion")
    plt.title("Topic distribution by decade")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # -----------------------
    # 6. Распределение по пьесам
    # -----------------------
    merged_topics_sorted = merged_topics.sort_values('year')

    plt.figure(figsize=(10, len(merged_topics_sorted) * 0.25))

    bottom = np.zeros(len(merged_topics_sorted))

    for i in range(4):
        values = merged_topics_sorted[f'Topic_{i + 1}']
        plt.barh(
            merged_topics_sorted['filename'],
            values,
            left=bottom,
            color=colors[i],
            label=f'Topic {i + 1}'
        )
        bottom += values

    plt.xlabel("Topic proportion")
    plt.title("Topic composition per play — Late Stalinism")
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()