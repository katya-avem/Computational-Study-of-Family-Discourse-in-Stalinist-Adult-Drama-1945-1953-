# Late Stalinist Soviet Drama Corpus (1945–1953)

This repository contains a digitised and annotated corpus of Soviet plays written for adult audiences during the late Stalinist period (1945–1953). The corpus was compiled for the study of representations of family relations and broader social models projected by Soviet theatre during the period.

## Corpus

The corpus consists of **46 plays** comprising **454,235 tokens**. The average play contains approximately 9,900 tokens.

The corpus was compiled from two principal sources:

* ***Teatr*** — a major Soviet theatre journal that published and discussed contemporary drama. The corpus includes 17 plays selected on the basis of their publication or discussion in the journal, including plays initially published in excerpts.
* ***Sovetskaia dramaturgiia* (Soviet Dramaturgy)** — an annual collection of Stalin Prize-winning plays. The corpus includes 29 plays from the late Stalinist period. The series ceased publication after Stalin's death; consequently, no volume for 1952 was issued.

The year of a *Sovetskaia dramaturgiia* volume does not necessarily correspond to the year in which a play was written or received the Stalin Prize. For example, plays awarded the Stalin Prize in 1951 were published in a volume that appeared in print in **1952**. The corpus metadata therefore records the publication source separately from the historical period of the plays.

Together, these sources provide a historically bounded corpus of plays that were widely circulated, critically discussed, and/or institutionally endorsed within the Soviet cultural system.

The complete list of plays, authors, dates, and sources is provided in the corpus metadata file.

### Corpus statistics

| Property            |                              Value |
| ------------------- | ---------------------------------: |
| Period covered      |                          1945–1953 |
| Number of plays     |                                 46 |
| Total tokens        |                            454,235 |
| Average play length |                      ~9,875 tokens |
| Main sources        | *Teatr*; *Sovetskaia dramaturgiia* |
| Language            |                            Russian |

## Digitisation and preprocessing

The plays were digitised from printed editions because no suitable digital versions of the texts were available.

The preprocessing pipeline consisted of the following stages:

1. **Digitisation and OCR**
   Printed plays were scanned and converted into machine-readable text using OCR.

2. **OCR correction**
   OCR output was manually checked and corrected to remove recognition errors and restore the original text.

3. **TEI encoding**
   The corrected texts were encoded according to **TEI (Text Encoding Initiative)** principles. Dramatic structure and speaker information were preserved in the markup.

4. **Removal of stage directions**
   Stage directions were removed from the analytical text in order to focus the computational analysis on spoken dialogue.

5. **Lemmatisation**
   The corpus was lemmatised using **Mystem**, accessed through the Python package **`pymystem3`**. The resulting lemmas were used as normalised word forms for computational analysis of the Russian-language corpus.

The resulting corpus combines machine-readable texts with structured metadata and annotation, allowing computational analysis to be integrated with close reading and manual annotation.


## Annotation

The repository contains manually created annotations used in the computational analysis. These include information about characters and their attributes, as well as classifications used for the analysis of social and dramatic roles.

Gender information, for example, is stored separately for female and male characters and is used by the Z-test analysis.

## Computational analysis

The preprocessed corpus was used for a range of computational methods, including:

* TF–IDF analysis;
* Z-score / Z-test analysis of character-related vocabulary;
* topic modelling;
* manual annotation of characters and dramatic roles.

The structured TEI corpus makes it possible to combine quantitative analysis with qualitative interpretation of individual plays and characters.

## Citation

If you use this corpus or its annotations in your research, please cite the repository and the associated dissertation/project:

> Kolevatova, Ekaterina. *The Path of the Soviet Family from Late Stalinism to the Thaw*. LMU Munich.

## License

The original literary works included in this corpus remain subject to
copyright held by their respective rights holders.

The TEI encoding, annotations, and metadata created for this project are
licensed under a Creative Commons Attribution 4.0 International License
(CC BY 4.0).

The code in this repository is released under the MIT License.
