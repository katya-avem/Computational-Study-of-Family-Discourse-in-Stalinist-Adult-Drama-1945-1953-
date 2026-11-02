import multiprocessing
import math
import re
from pathlib import Path

import matplotlib.pyplot as plt
import nltk
import pandas as pd
from gensim import corpora
from gensim.models import CoherenceModel, LdaModel
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)

# ---------------------------------------------------------------------
# Paths and model settings
# ---------------------------------------------------------------------
PROJECT_DIR = Path(
    r"C:\Users\katya\Documents\PyCharmProjects\soviet_plays_PhD"
)
PATH_THAW = PROJECT_DIR / "cut_into_segments" / "Thaw"
PATH_STALIN = PROJECT_DIR / "cut_into_segments" / "Stalinism"
METADATA_PATH = PROJECT_DIR / "dataframe.csv"
OUTPUT_DIR = (
    PROJECT_DIR
    / "Adult_Thaw_Plays (Chapter 4)"
    / "lda_grid_search_results"
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TOPIC_RANGE = range(4, 21)
RANDOM_SEEDS = [11, 83, 113, 265, 497, 599]
PASSES = 100
ITERATIONS = 500
NO_BELOW = 5
NO_ABOVE = 0.5
TOP_N_WORDS = 15


def get_stopwords():
    """Return Russian and project-specific stopwords."""
    russian_stopwords = set(stopwords.words("russian"))
    domain_stopwords = {
        "мол", "да-да", "об", "б", "коль", "пока", "под", "ежели",
        "-а", "ль", "ага", "этак", "эдакий", "ну-ка", "шо", "пан",
        "мож", "сюда", "здравствовать", "спасибо", "все-таки",
        "пожалуйста", "пусть", "ах", "ох", "о", "мак", "ладно", "эх",
        "вон", "какой-то", "всё", "все", "ничто", "нечто", "сей",
        "еще", "ещё", "здравствуйте", "что-то", "ныне", "пред",
        "вообще",
    }
    return russian_stopwords.union(domain_stopwords)


def normalize_play_name(value):
    """Normalize a CSV filename or a segment-derived play name for matching."""
    name = Path(str(value).strip()).name
    # Remove known source extensions in either filename form:
    # "Play.xml.txt", "Play.xml", and "Play.txt" all normalize to "Play".
    name = re.sub(r"\.txt$", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\.xml$", "", name, flags=re.IGNORECASE)
    return name.strip().casefold()


def load_metadata(metadata_path):
    """Load metadata and build a strict, unambiguous play-name lookup."""
    if not metadata_path.exists():
        raise FileNotFoundError(
            f"Metadata CSV was not found: {metadata_path}"
        )

    # utf-8-sig handles CSV files saved with a UTF-8 BOM.
    df = pd.read_csv(metadata_path, encoding="utf-8-sig")

    required_columns = {"filename", "year"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        raise ValueError(
            "The metadata CSV is missing required column(s): "
            + ", ".join(sorted(missing_columns))
        )

    df = df.copy()
    df["normalized_filename"] = df["filename"].map(normalize_play_name)

    empty_names = df[df["normalized_filename"].eq("")]
    if not empty_names.empty:
        raise ValueError(
            "The metadata CSV contains an empty filename value."
        )

    duplicated = df[
        df["normalized_filename"].duplicated(keep=False)
    ].sort_values("normalized_filename")
    if not duplicated.empty:
        details = duplicated[["filename", "year"]].to_string(index=False)
        raise ValueError(
            "More than one metadata row maps to the same normalized play "
            "name. Please resolve these duplicates before running LDA:\n"
            f"{details}"
        )

    return df.set_index("normalized_filename", drop=False)


def get_play_and_segment_id(segment_path):
    """Remove only the final numeric segment suffix from a segment filename."""
    stem = segment_path.stem
    match = re.fullmatch(r"(.+)_([0-9]+)", stem)
    if not match:
        raise ValueError(
            "Could not identify the final segment number in filename "
            f"'{segment_path.name}'. Expected a name such as 'Play_1.txt'."
        )
    return match.group(1), int(match.group(2))


def validate_year(value, csv_filename, segment_path):
    """Return a valid integer year or raise an informative error."""
    if pd.isna(value) or str(value).strip() == "":
        raise ValueError(
            f"Year is missing in dataframe.csv for '{csv_filename}', "
            f"required by segment '{segment_path.name}'."
        )
    try:
        year = int(float(value))
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(
            f"Invalid year value {value!r} in dataframe.csv for "
            f"'{csv_filename}', required by segment '{segment_path.name}'."
        ) from exc

    if year < 1800 or year > 2100:
        raise ValueError(
            f"Year {year} is outside the expected range for "
            f"'{csv_filename}' (segment '{segment_path.name}')."
        )
    return year


def load_segment_corpus(folder_path, subcorpus_label, all_stopwords, metadata):
    """Load pre-segmented text files and attach metadata from dataframe.csv."""
    if not folder_path.exists():
        raise FileNotFoundError(
            f"Segment folder does not exist: {folder_path}"
        )

    segment_files = sorted(folder_path.glob("*.txt"))
    if not segment_files:
        raise FileNotFoundError(
            f"No .txt segment files were found in: {folder_path}"
        )

    texts = []
    rows = []
    unmatched_names = []

    for segment_path in segment_files:
        segment_play_name, segment_number = get_play_and_segment_id(
            segment_path
        )
        normalized_name = normalize_play_name(segment_play_name)

        if normalized_name not in metadata.index:
            unmatched_names.append(
                f"{segment_path.name} -> {segment_play_name}"
            )
            continue

        meta_row = metadata.loc[normalized_name]
        year = validate_year(
            meta_row["year"], meta_row["filename"], segment_path
        )

        raw_text = segment_path.read_text(encoding="utf-8")
        tokens = [
            token.lower()
            for token in raw_text.split()
            if token.lower() not in all_stopwords
        ]

        if not tokens:
            raise ValueError(
                f"Segment contains no tokens after stopword removal: "
                f"{segment_path}"
            )

        texts.append(tokens)
        rows.append(
            {
                "segment_id": segment_path.stem,
                "segment_number": segment_number,
                "play_name": str(meta_row["filename"]),
                "year": year,
                "decade": (year // 10) * 10,
                "subcorpus": subcorpus_label,
                "source": meta_row.get("source", ""),
                "audience_type": meta_row.get("audience type", ""),
                "period": meta_row.get("period", ""),
                "segment_path": str(segment_path),
            }
        )

    if unmatched_names:
        examples = "\n".join(f"  - {name}" for name in unmatched_names[:30])
        remaining = len(unmatched_names) - min(len(unmatched_names), 30)
        extra = f"\n  ... and {remaining} more" if remaining else ""
        raise ValueError(
            f"{len(unmatched_names)} segment file(s) could not be matched "
            "to the 'filename' column in dataframe.csv. No default year "
            "will be assigned. Check spelling and filename normalization:\n"
            f"{examples}{extra}"
        )

    if len(texts) != len(segment_files):
        raise RuntimeError(
            f"Internal loading mismatch for {subcorpus_label}: "
            f"found {len(segment_files)} files but loaded {len(texts)}."
        )

    print(
        f"{subcorpus_label}: loaded {len(texts)} pre-segmented text files "
        f"from {folder_path}"
    )
    return texts, pd.DataFrame(rows)


def run_grid_search(texts, dictionary, corpus):
    """Train each K/seed combination and calculate c_v coherence."""
    results = []
    total_runs = len(TOPIC_RANGE) * len(RANDOM_SEEDS)
    current_run = 0

    for k in TOPIC_RANGE:
        for seed in RANDOM_SEEDS:
            current_run += 1
            print(
                f"[{current_run}/{total_runs}] Training LDA: "
                f"K={k}, seed={seed}...",
                end=" ",
                flush=True,
            )

            model = LdaModel(
                corpus=corpus,
                id2word=dictionary,
                num_topics=k,
                passes=PASSES,
                iterations=ITERATIONS,
                alpha="auto",
                eta="auto",
                random_state=seed,
            )
            coherence_model = CoherenceModel(
                model=model,
                texts=texts,
                dictionary=dictionary,
                coherence="c_v",
            )
            score = coherence_model.get_coherence()
            print(f"c_v = {score:.4f}")
            results.append(
                {"num_topics": k, "seed": seed, "coherence": score}
            )

    return pd.DataFrame(results)


def print_top_words(model, dictionary, top_n=TOP_N_WORDS):
    """Print the highest-weighted words for every topic to the console."""
    print("\nTOP WORDS FOR EACH TOPIC")
    print("=" * 72)
    for topic_id in range(model.num_topics):
        terms = model.get_topic_terms(topic_id, topn=top_n)
        words = [
            dictionary[word_id]
            for word_id, _ in terms
        ]
        print(f"Topic {topic_id + 1}: " + ", ".join(words))
    print("=" * 72)


def plot_coherence_results(results, output_dir):
    """Plot mean, standard deviation, and maximum coherence for each K."""
    grouped = (
        results.groupby("num_topics")["coherence"]
        .agg(["mean", "std", "max"])
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.errorbar(
        grouped["num_topics"],
        grouped["mean"],
        yerr=grouped["std"].fillna(0),
        marker="o",
        capsize=4,
        label="Mean coherence ± SD",
    )
    ax.plot(
        grouped["num_topics"],
        grouped["max"],
        marker="s",
        linestyle="--",
        label="Maximum coherence",
    )
    ax.set_xlabel("Number of topics (K)")
    ax.set_ylabel("c_v coherence")
    ax.set_title("LDA grid search: coherence by number of topics")
    ax.set_xticks(grouped["num_topics"])
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(
        output_dir / "01_coherence_by_topic_count.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close(fig)


def plot_topic_words(model, dictionary, output_dir, top_n=TOP_N_WORDS):
    """Save a chart and CSV containing the top words for each topic."""
    n_topics = model.num_topics
    n_cols = 3
    n_rows = math.ceil(n_topics / n_cols)
    fig, axes = plt.subplots(
        n_rows, n_cols, figsize=(18, n_rows * 4.5), squeeze=False
    )
    rows = []

    for topic_id in range(n_topics):
        terms = model.get_topic_terms(topic_id, topn=top_n)
        words = [dictionary[word_id] for word_id, _ in terms]
        weights = [weight for _, weight in terms]
        for rank, (word, weight) in enumerate(zip(words, weights), start=1):
            rows.append(
                {
                    "topic": topic_id + 1,
                    "rank": rank,
                    "word": word,
                    "weight": weight,
                }
            )
        ax = axes.flat[topic_id]
        ax.barh(words[::-1], weights[::-1])
        ax.set_title(f"Topic {topic_id + 1}")
        ax.set_xlabel("Word weight")
        ax.tick_params(axis="y", labelsize=8)

    for ax in list(axes.flat)[n_topics:]:
        ax.set_visible(False)

    fig.suptitle(f"Top {top_n} words in each LDA topic", fontsize=15)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(
        output_dir / "02_top_words_by_topic.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close(fig)
    pd.DataFrame(rows).to_csv(
        output_dir / "best_model_topic_words.csv",
        index=False,
        encoding="utf-8-sig",
    )


def get_topic_probabilities(model, corpus, metadata_df):
    """Return per-segment topic probabilities alongside segment metadata."""
    probability_rows = []
    for bow, (_, meta_row) in zip(corpus, metadata_df.iterrows()):
        topic_distribution = dict(
            model.get_document_topics(bow, minimum_probability=0)
        )
        row = meta_row.to_dict()
        for topic_id in range(model.num_topics):
            row[f"topic_{topic_id + 1}"] = topic_distribution.get(topic_id, 0.0)
        probability_rows.append(row)
    return pd.DataFrame(probability_rows)


def plot_dominant_topic_distribution(topic_df, output_dir):
    """Plot the proportion of segments assigned to each dominant topic."""
    topic_columns = [
        column for column in topic_df.columns
        if re.fullmatch(r"topic_\d+", column)
    ]
    topic_df = topic_df.copy()
    topic_df["dominant_topic"] = (
        topic_df[topic_columns].to_numpy().argmax(axis=1) + 1
    )
    distribution = pd.crosstab(
        topic_df["subcorpus"],
        topic_df["dominant_topic"],
        normalize="index",
    )
    distribution.to_csv(
        output_dir / "topic_distribution_by_subcorpus.csv",
        encoding="utf-8-sig",
    )
    ax = distribution.plot(
        kind="bar", stacked=True, figsize=(12, 7), width=0.7
    )
    ax.set_xlabel("Subcorpus")
    ax.set_ylabel("Proportion of segments")
    ax.set_title("Dominant topic distribution by subcorpus")
    ax.legend(title="Topic", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.tick_params(axis="x", rotation=0)
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(
        output_dir / "03_dominant_topic_distribution.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close(fig)


def plot_average_topic_trajectory(topic_df, output_dir):
    """Plot mean topic probability by decade and subcorpus."""
    topic_columns = [
        column for column in topic_df.columns
        if re.fullmatch(r"topic_\d+", column)
    ]
    averages = (
        topic_df.groupby(["subcorpus", "decade"], as_index=False)[topic_columns]
        .mean()
        .sort_values(["subcorpus", "decade"])
    )
    averages.to_csv(
        output_dir / "average_topic_probability_by_decade.csv",
        index=False,
        encoding="utf-8-sig",
    )

    n_topics = len(topic_columns)
    n_cols = 2
    n_rows = math.ceil(n_topics / n_cols)
    fig, axes = plt.subplots(
        n_rows, n_cols, figsize=(14, n_rows * 3.8), squeeze=False
    )

    for topic_index, topic_column in enumerate(topic_columns):
        ax = axes.flat[topic_index]
        for subcorpus, group in averages.groupby("subcorpus"):
            ax.plot(
                group["decade"],
                group[topic_column],
                marker="o",
                label=subcorpus,
            )
        ax.set_title(f"Topic {topic_index + 1}")
        ax.set_xlabel("Decade")
        ax.set_ylabel("Mean topic probability")
        ax.grid(True, alpha=0.3)
        ax.legend()

    for ax in list(axes.flat)[n_topics:]:
        ax.set_visible(False)

    fig.suptitle("Average topic trajectory by decade and subcorpus", fontsize=15)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(
        output_dir / "04_average_topic_trajectory_by_decade.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close(fig)


def plot_topic_trajectories_by_play(topic_df, output_dir):
    """Plot each play's mean topic probabilities, ordered by publication year."""
    topic_columns = [
        column for column in topic_df.columns
        if re.fullmatch(r"topic_\d+", column)
    ]
    play_level = (
        topic_df.groupby(
            ["subcorpus", "play_name", "year", "decade"],
            as_index=False,
        )[topic_columns]
        .mean()
        .sort_values(["year", "play_name"])
    )
    play_level.to_csv(
        output_dir / "topic_probabilities_by_play.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # Create one figure per topic so play-level patterns remain inspectable.
    for topic_index, topic_column in enumerate(topic_columns, start=1):
        fig, ax = plt.subplots(figsize=(max(12, len(play_level) * 0.22), 7))
        for subcorpus, group in play_level.groupby("subcorpus"):
            group = group.sort_values(["year", "play_name"])
            ax.plot(
                range(len(group)),
                group[topic_column],
                marker="o",
                linestyle="-",
                linewidth=1,
                markersize=3,
                label=subcorpus,
            )
        ax.set_xlabel("Individual plays (ordered by year; see CSV for labels)")
        ax.set_ylabel("Mean topic probability across a play's segments")
        ax.set_title(f"Topic {topic_index}: play-level trajectory")
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(
            output_dir / f"05_topic_{topic_index:02d}_by_play.png",
            dpi=250,
            bbox_inches="tight",
        )
        plt.close(fig)


def main():
    print("Loading metadata and pre-segmented corpora...")
    all_stopwords = get_stopwords()
    metadata = load_metadata(METADATA_PATH)

    texts_thaw, meta_thaw = load_segment_corpus(
        PATH_THAW, "Thaw", all_stopwords, metadata
    )
    texts_stalin, meta_stalin = load_segment_corpus(
        PATH_STALIN, "Stalinism", all_stopwords, metadata
    )

    all_texts = texts_thaw + texts_stalin
    df_meta = pd.concat([meta_thaw, meta_stalin], ignore_index=True)

    print(
        f"Total segments loaded: {len(all_texts)} "
        f"(Stalinism: {len(texts_stalin)}, Thaw: {len(texts_thaw)})"
    )
    print(f"Unique plays represented: {df_meta['play_name'].nunique()}")
    print("Building dictionary...")
    dictionary = corpora.Dictionary(all_texts)
    dictionary.filter_extremes(no_below=NO_BELOW, no_above=NO_ABOVE)
    corpus = [dictionary.doc2bow(text) for text in all_texts]

    if not dictionary:
        raise ValueError(
            "The dictionary is empty after filtering. Check the corpus and "
            "NO_BELOW / NO_ABOVE settings."
        )

    print(f"Dictionary size after filtering: {len(dictionary)}")
    print("Starting LDA grid search...")
    results = run_grid_search(all_texts, dictionary, corpus)
    results.to_csv(
        OUTPUT_DIR / "lda_coherence_grid_search_results.csv",
        index=False,
        encoding="utf-8-sig",
    )
    df_meta.to_csv(
        OUTPUT_DIR / "segment_metadata.csv",
        index=False,
        encoding="utf-8-sig",
    )
    plot_coherence_results(results, OUTPUT_DIR)

    best_row = results.loc[results["coherence"].idxmax()]
    best_k = int(best_row["num_topics"])
    best_seed = int(best_row["seed"])
    best_score = float(best_row["coherence"])

    print("\n" + "=" * 72)
    print(
        f"BEST CONFIGURATION: K={best_k}, seed={best_seed}, "
        f"passes={PASSES}, c_v={best_score:.4f}"
    )
    print("=" * 72)

    best_model = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=best_k,
        passes=PASSES,
        iterations=ITERATIONS,
        alpha="auto",
        eta="auto",
        random_state=best_seed,
    )
    best_model.save(str(OUTPUT_DIR / "best_lda_model"))
    dictionary.save(str(OUTPUT_DIR / "best_lda_dictionary"))

    print_top_words(best_model, dictionary)
    plot_topic_words(best_model, dictionary, OUTPUT_DIR)

    topic_df = get_topic_probabilities(best_model, corpus, df_meta)
    topic_df.to_csv(
        OUTPUT_DIR / "segment_topic_probabilities.csv",
        index=False,
        encoding="utf-8-sig",
    )
    plot_dominant_topic_distribution(topic_df, OUTPUT_DIR)
    plot_average_topic_trajectory(topic_df, OUTPUT_DIR)
    plot_topic_trajectories_by_play(topic_df, OUTPUT_DIR)

    print("\nAnalysis completed. All results were saved to:")
    print(OUTPUT_DIR)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
