# Computational Study of Family Discourse in Stalinist Adult Drama (1945–1953)

## Overview

This repository contains research materials and source code accompanying a study of the ideological functions of family and kinship in late Stalinist Soviet drama. The research was presented at the Digital Humanities conference DH2026 in Daejeon, South Korea.

The project examines how Soviet adult drama of the late Stalinist period represented family relations and incorporated the language of kinship into broader ideological discourses. It explores the relationship between the private family and the concept of the Soviet collective as a *Great Family*, as well as the ways in which family vocabulary was distributed across different character types, gender groups, and thematic structures.

The study is based on a corpus of 46 plays written and published between 1945 and 1953. It combines corpus construction and text processing with manual character annotation and several computational methods, including TF-IDF analysis, Z-score-based analysis of character speech, and Latent Dirichlet Allocation (LDA) topic modelling.

This repository provides the scripts, annotation files, and analytical results used in the study.

## Research Questions

The project addresses the following questions:

- How does late Stalinist drama transform the family from a private sphere of social relations into an ideological model of social organisation?
- How does kinship vocabulary vary across different ideological character types?
- How do male and female characters differ in their use of kinship vocabulary and language associated with social and institutional roles?
- How is family discourse embedded within the broader thematic structures of late Stalinist adult drama?

## Corpus

The corpus consists of 46 Soviet plays for adult audiences written and published between 1945 and 1953. The texts were digitised from printed editions, corrected, encoded according to TEI principles, and lemmatised before the computational analysis.

The corpus was assembled from Soviet drama publications and periodicals, including *Sovetskaia dramaturgiia* and *Teatr*. These sources provide access to dramatic texts that circulated within the institutional and literary framework of late Stalinist Soviet culture.

The original texts of the plays are protected by copyright and are therefore not included in this repository. However, the repository provides selected derived textual materials used in the analysis, including character speech extracts and lemmatised text collections organised according to the analytical classification.

## Methodology

The study combines close reading and computational text analysis. Different methods were selected to address different dimensions of family discourse and to account for the heterogeneity of adult dramatic texts.

### Character Annotation

Characters were manually classified according to two annotation schemes, each designed for a specific analytical task:

- **Character types:** characters were classified into 13 recurring ideological and narrative types. This classification provides the basis for comparing the characteristic vocabulary and ideological positioning of different groups of characters.
- **Gender:** characters were additionally classified into female and male groups to enable a comparative analysis of gender-specific patterns in character speech.

### TF-IDF Analysis

TF-IDF analysis was used to identify characteristic vocabulary across the 13 character-type subcorpora. This approach makes it possible to examine how different character types are linguistically distinguished and how their vocabulary reflects particular ideological positions, social roles, and relationships to the family.

### Z-Score-Based Analysis

Z-score-based analysis was applied to character speech to identify lexical patterns that distinguish female and male characters. The analysis focuses on differences in the vocabulary used by the two groups, including kinship terms and words associated with institutional and social relations.

### Topic Modelling

Latent Dirichlet Allocation (LDA) was used to identify broader thematic structures within the corpus. Topic modelling makes it possible to investigate how family discourse relates to other recurring themes and ideological concerns in late Stalinist adult drama.

### LDA Grid Search and Model Selection

A systematic grid search was conducted to identify an appropriate LDA model configuration. Multiple models were trained using different numbers of topics and random seeds. Their performance was evaluated using the C_v coherence measure.

The grid search results were compared to assess the stability and interpretability of the resulting topic structures and to select the final model. A separate script was used to train the selected model and generate the topic keywords and distributions analysed in the study.

## Repository Structure

The repository contains the following files and directories:

- **`data/`** — corpus metadata and documentation:
  - **`metadata.csv`** — metadata for all plays included in the dissertation corpus, covering all four subcorpora.
  - **`README.md`** — documentation describing the corpus, its composition, sources, and organisation.

- **`presentation/`** — slides from the presentation *Computational Study of Family Discourse in Stalinist Adult Drama (1945–1953)*, delivered at the DH2026 conference in Daejeon, South Korea.

- **`src/`** — source code and scripts used for corpus preparation and computational analysis:
  - **`txt_to_xml.py`** — script for converting plain-text plays into XML files and assisting with their structural annotation.
  - **`cut_into_segments.py`** — script for dividing plays into text segments of approximately 1,000 words.
  - **`tfidf/`** — scripts for TF-IDF analysis.
  - **`z_analysis/`** — scripts for Z-score-based analysis of character speech.
  - **`lda/`** — scripts for LDA grid search, model evaluation, and training of the selected model.

- **`annotation/`** — JSON files containing manual character annotations, including the classification of characters into 13 types and the gender-based classification.

- **`results/`** — outputs and derived textual materials from the computational analyses:
  - **`male_and_female_lines/`** — character speech extracts separated into female and male subcorpora, used for the gender-based lexical analysis.
  - **`speech_of_characters_lemmatized/`** — lemmatised character speech organised into 13 character-type subcorpora, used for the analysis of characteristic vocabulary.
  - **`tfidf/`** — results of TF-IDF analysis.
  - **`z_analysis/`** — results of Z-score-based analysis.
  - **`lda/`** — LDA model outputs, including coherence scores, selected model parameters, topic keywords, and topic distributions.

## Software and Dependencies

The analytical workflow was implemented in Python. The repository contains the scripts used to process the corpus, perform the computational analyses, and generate the results.

A list of software dependencies and installation instructions can be added here.

## Reproducibility and Copyright

The repository provides the annotation data, analytical scripts, and derived results supporting the research. Since the original dramatic texts are subject to copyright restrictions, they are not redistributed here.

The scripts and annotation files are intended to document the analytical workflow and make the computational procedures and research results more transparent.