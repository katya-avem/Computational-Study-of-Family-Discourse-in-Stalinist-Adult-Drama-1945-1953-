# Annotation Guidelines

This directory contains the character annotations used for the computational
analysis of the adult Stalinist drama corpus (1945–1953).

The annotation consists of two complementary layers:

1. **Gender annotation**, used for the Z-score analysis;
2. **Character-type annotation**, used for the character-based TF-IDF analysis.

The annotations were created manually on the basis of the characters' roles
within the plays and their ideological and narrative functions.

## 1. Gender annotation

The files `female_characters.json` and `male_characters.json` contain the
manually annotated lists of female and male characters in the corpus.

These data were used to construct two gender-based subcorpora:

- all speech attributed to female characters;
- all speech attributed to male characters.

The resulting subcorpora were compared using Z-score-based lexical analysis.

The gender annotation was applied at the character level. Each character
included in the analysis was assigned to one of the two categories represented
in the annotation files.

The annotation files contain character names rather than the full textual
content of the plays. The original plays are not included in this repository.

## 2. Character-type annotation

For the TF-IDF analysis, characters were additionally classified according to
thirteen recurring ideological and narrative types identified through close
reading of the corpus and informed by existing scholarship on Socialist
Realist character types.

The thirteen categories are:

1. The “Misguided Manager”
2. The “Progressive Young Worker”
3. The “Party Official”
4. The “Patriotic Scientist”
5. The “Saboteur”
6. The “False Hero”
7. The “Misguided Intellectual”
8. The “Western Protagonist”
9. The “Western Antagonist”
10. The “Military Hero”
11. The “Revolutionary”
12. The “Historical Leader”
13. “Enemies of the Revolution”

The complete character-to-type assignment is provided in the accompanying
annotation file.

### 2.1 Principles of classification

Character types were assigned according to the character's function within
the play rather than solely according to occupation, age, gender, or social
status.

The classification therefore takes into account:

- the character's narrative and ideological function;
- their position within the central conflict of the play;
- their relationship to Soviet ideological values;
- their role in relation to other characters;
- the character's trajectory over the course of the play.

The categories are analytical rather than exhaustive descriptions of all
characters in the corpus. Characters were assigned to a type when their
function corresponded sufficiently closely to one of the recurring patterns
identified in the corpus.

### 2.2 Character types and analytical distinctions

Some categories require particular distinctions:

**The “Misguided Manager”** refers to an authority figure, typically a
factory director or collective-farm chairman, who is devoted to his work but
initially resists new ideas and must undergo ideological correction.

**The “Progressive Young Worker”** represents a younger, ideologically
conscious worker who advocates technological innovation, increased
production, education, and continuous labour for the benefit of the Soviet
state.

**The “Party Official”** is a Party representative who intervenes in the
central conflict and provides ideological or organisational guidance.

**The “Patriotic Scientist”** is an intellectual devoted to Soviet science
and technological progress.

**The “Saboteur”** includes foreign agents and spies as well as corrupt
Soviet characters involved in fraud, opportunism, or illicit enrichment through
personal connections.

**The “False Hero”** initially resembles a positive protagonist but is
eventually revealed to be morally deficient and unworthy of the status of an
honest Soviet citizen. This category is particularly associated with the late
Stalinist plays of 1952–1953.

**The “Misguided Intellectual”** is a member of the intelligentsia who remains
attached to bourgeois values or the cultural legacy of the imperial past and
has not fully embraced Soviet priorities.

**The “Western Protagonist”** and **“Western Antagonist”** occur primarily in
plays set in the United States. The former is sympathetic to the Soviet Union
or expresses opposition to the social order depicted in the play; the latter
opposes such characters.

**The “Military Hero”** represents Soviet soldiers or officers in plays
devoted to the Second World War and is characterised by courage, discipline,
and loyalty.

**The “Revolutionary”** represents revolutionary figures, particularly young
men or women struggling for social justice in historically oriented plays.

**The “Historical Leader”** occupies a position of political or military
command and represents leadership, strategic planning, and decisive action.

**Enemies of the Revolution** are antagonists in historically oriented plays
who oppose revolutionary forces or seek to eliminate revolutionary leaders.

## 3. Character-based corpora

For the TF-IDF analysis, speech was aggregated according to character type.

All speech belonging to characters assigned to the same category was merged
into a single analytical document. This produced thirteen character-type
documents, which were then compared using TF-IDF.

This approach makes it possible to examine lexical patterns associated with
ideological character types rather than treating the corpus only at the level
of individual plays.

## 4. Relationship between annotation and analysis

The annotation layers correspond to different analytical questions:

| Annotation | Analytical unit | Method | Purpose |
|---|---|---|---|
| Gender | Character | Z-score analysis | Identify gender-associated lexical patterns |
| Character type | Character | TF-IDF | Identify lexical patterns associated with ideological roles |

The annotations were therefore not intended to provide a single unified
classification of characters. They were created as separate analytical
dimensions that could be used to examine different aspects of the corpus.

## 5. Copyright and data availability

The original corpus consists of 46 Soviet plays written and staged between
1945 and 1953. The full texts are not distributed in this repository because
the source texts remain subject to copyright restrictions.

The annotation files contain character-level metadata and are provided as
research materials accompanying the computational analysis. They should not
be used to reconstruct or redistribute the copyrighted source texts.

The repository therefore provides the methodological and analytical materials
necessary to document the research workflow without distributing the original
plays.