# pandas_1 — removed chapter report

`887a578b0a4b:content/pandas_1/pandas_1.ipynb` → dissolved into `content/polars_1/polars_1.ipynb`

**33 markdown cells · 34 code cells · ~1742 words of prose.** This chapter was not converted and not renamed. It was taken apart: some of it was carried into the host chapter and the rest was dropped with the concept it taught. It has no entry anywhere else, so this is the only record of what a reader loses.

Per section, *kept verbatim* counts sentences of eight words or more that survive word-for-word in the host chapter. A low count is not by itself a loss — prose was re-authored throughout — so the verdict is the judgement, not the number.

| section | sentences | kept verbatim | heading in host |
|---|---|---|---|
| `DataFrame`s and Indices | 0 | 0 | — |
| &nbsp;&nbsp;`DataFrame` | 4 | 2 | — |
| &nbsp;&nbsp;&nbsp;&nbsp;Using a List and Column Name(s) | 4 | 1 | — |
| &nbsp;&nbsp;&nbsp;&nbsp;From a Dictionary | 4 | 0 | — |
| &nbsp;&nbsp;&nbsp;&nbsp;From a `Series` | 4 | 0 | From a `Series` |
| &nbsp;&nbsp;Indices | 11 | 0 | — |
| `DataFrame` Attributes: Index, Columns, and Shape | 4 | 1 | — |
| Slicing in `DataFrame`s | 6 | 5 | — |
| &nbsp;&nbsp;Extracting data with `.head` and `.tail` | 3 | 3 | Extracting Data with `.head` and `.tail` |
| &nbsp;&nbsp;Label-based Extraction: Indexing with `.loc` | 21 | 0 | — |
| &nbsp;&nbsp;Integer-based Extraction: Indexing with `.iloc` | 16 | 0 | — |
| &nbsp;&nbsp;Context-dependent Extraction: Indexing with `[]` | 2 | 0 | — |
| &nbsp;&nbsp;&nbsp;&nbsp;A slice of row numbers | 1 | 0 | — |
| &nbsp;&nbsp;&nbsp;&nbsp;A list of column labels | 1 | 0 | — |
| &nbsp;&nbsp;&nbsp;&nbsp;A single-column label | 3 | 0 | — |
| Parting Note | 7 | 3 | Parting Note |

## Assets

- **images** — 8 deleted with the chapter: df_elections.png, df_series_index.png, index_comparison_1.png, index_comparison_2.png, locgraphic.png, non-uniqueindex.png, understand_data.png, uniqueindex.png
- **data** — elections.csv

## Summary

This chapter was two-thirds about the Index, and the Index has no counterpart in Polars, so course staff dissolved it rather than convert it. Its surviving third — building a `DataFrame` from a list, a dictionary and a `Series`, the attributes section, `.head`/`.tail`, and `[]` extraction — now opens `polars_1`. What a reader loses outright is the Index itself (S6), label-based extraction with `.loc` (S10, the chapter's largest section at 21 sentences), and the `.loc`-versus-`.iloc` comparison that S11 was built around. Six of the eight deleted images exist only to draw an index, so they die with the concept; `df_elections.png` and `understand_data.PNG` are still used by `intro_lec`, which owns its own copies (verified — both paths resolve). The chapter's `elections.csv` was byte-identical to the copy `polars_2` still ships (md5 `47b93a15`, 187 rows), so no data was lost. The whole chapter is recoverable from git at `4f842ef7`.

## Sections

<a id="s1"></a>
### S1 · `DataFrame`s and Indices

0 sentences, 0 kept verbatim, host heading: —

**Became:** The parent heading became `DataFrame`s and `Series` in `polars_1`.
**Reader loses:** The framing only. The old title put the Index beside the `DataFrame` as a co-equal structure; the new one pairs the `DataFrame` with the `Series`, which is the pairing Polars actually has.

<a id="s2"></a>
### S2 · `DataFrame`

4 sentences, 2 kept verbatim, host heading: —

**Became:** The opening `DataFrame` section, whose `pd.read_csv` of `elections` now opens `polars_1` as its own subsection, *From a CSV File*.
**Reader loses:** Nothing. The two sentences defining a row as a record and a column as an attribute survive word for word.

<a id="s3"></a>
### S3 · Using a List and Column Name(s)

4 sentences, 1 kept verbatim, host heading: —

**Became:** *From a List of Rows*.
**Reader loses:** Nothing of substance. Both the single-column and the two-column construction survive; only the `columns=` keyword spelling changes.

<a id="s4"></a>
### S4 · From a Dictionary

4 sentences, 0 kept verbatim, host heading: —

**Became:** *From a Dictionary of Columns*.
**Reader loses:** The contrast. The pandas section showed two dictionary forms, one keyed by column and one built row-wise, and said the second was the more common. Polars takes a dictionary of columns only, so the comparison goes with it.

<a id="s5"></a>
### S5 · From a `Series`

4 sentences, 0 kept verbatim, host heading: From a `Series`

**Became:** *From a `Series`* — the one heading that survives unchanged.
**Reader loses:** The index premise. The pandas version turned on the two `Series` sharing row labels ("Notice how our indices, or row labels, are the same") and offered `pd.DataFrame(s_a)` and `s_b.to_frame()`. A Polars `Series` has a name, not an index, so the alignment lesson has no subject.

<a id="s6"></a>
### S6 · Indices

11 sentences, 0 kept verbatim, host heading: —

**Became:** Nothing. Deleted outright.
**Reader loses:** The entire concept: setting an index at read time, `set_index` and `reset_index`, reverting to the default integers, and the point that index values need be neither unique nor numeric — with the two diagrams (`uniqueindex.png`, `non-uniqueindex.png`) that illustrated it. Eleven sentences, none reused. This is the single largest deletion on the branch and it is deliberate: Polars has no row label index.

<a id="s7"></a>
### S7 · `DataFrame` Attributes: Index, Columns, and Shape

4 sentences, 1 kept verbatim, host heading: —

**Became:** *`DataFrame` Attributes: `columns`, `dtypes`, and `shape`*.
**Reader loses:** `DataFrame.index`, one of the three attributes the section existed to name. It gains `.dtypes` in its place. The sentence about column names being unique survives.

<a id="s8"></a>
### S8 · Slicing in `DataFrame`s

6 sentences, 5 kept verbatim, host heading: —

**Became:** *Extracting Data from a `DataFrame`*.
**Reader loses:** Its roadmap. Five of six sentences survive, but the numbered list they lead into — `.head`/`.tail`, `.loc`, `.iloc`, `[]` — is now `.head`/`.tail`, `[]`, `filter`/`select`, and row positions. Two of the four promised methods do not exist in Polars.

<a id="s9"></a>
### S9 · Extracting data with `.head` and `.tail`

3 sentences, 3 kept verbatim, host heading: Extracting Data with `.head` and `.tail`

**Became:** *Extracting Data with `.head` and `.tail`*, intact.
**Reader loses:** Nothing. All three sentences survive verbatim.

<a id="s10"></a>
### S10 · Label-based Extraction: Indexing with `.loc`

21 sentences, 0 kept verbatim, host heading: —

**Became:** Nothing. Deleted outright.
**Reader loses:** Label-based extraction in full: the row-and-column argument pair, single values against slices against lists, the inclusive string slice `'Year':'Popular vote'` that pandas allows and Python does not, the `:` shorthand, and the rule that a scalar column argument yields a `Series` while a one-element list yields a `DataFrame`. Twenty-one sentences and `locgraphic.png`, the annotated diagram the section was built on. No equivalent exists: `.loc` addresses rows by label.

<a id="s11"></a>
### S11 · Integer-based Extraction: Indexing with `.iloc`

16 sentences, 0 kept verbatim, host heading: —

**Became:** Partly *Working with Row Positions* and *Selecting Columns by Position*.
**Reader loses:** The comparison. The section taught `.iloc` against `.loc` — that `.iloc` slicing is exclusive where `.loc` is inclusive, and the closing guidance on when to reach for which. With `.loc` gone the contrast has one side, so sixteen sentences reduce to positional helpers with no counterpart to be compared against.

<a id="s12"></a>
### S12 · Context-dependent Extraction: Indexing with `[]`

2 sentences, 0 kept verbatim, host heading: —

**Became:** *Extraction with `[]`*.
**Reader loses:** The "context-dependent" framing and the three-way enumeration it introduced. Polars still overloads `[]`, but the chapter no longer presents that overloading as the operator's defining oddity.

<a id="s13"></a>
### S13 · A slice of row numbers

1 sentences, 0 kept verbatim, host heading: —

**Became:** Folded into *Extraction with `[]`*.
**Reader loses:** Nothing of substance; slicing rows with `[]` survives.

<a id="s14"></a>
### S14 · A list of column labels

1 sentences, 0 kept verbatim, host heading: —

**Became:** Folded into *Extraction with `[]`*.
**Reader loses:** Nothing of substance; selecting a list of columns survives, alongside a new positional form.

<a id="s15"></a>
### S15 · A single-column label

3 sentences, 0 kept verbatim, host heading: —

**Became:** Folded into *Extraction with `[]`*.
**Reader loses:** The punchline that a single column label returns a `Series` rather than a `DataFrame`, and the remark that `[]` is far more common in practice than the accessors. The `Series`-versus-`DataFrame` distinction still holds in Polars, so this one is a candidate to restore.

<a id="s16"></a>
### S16 · Parting Note

7 sentences, 3 kept verbatim, host heading: Parting Note

**Became:** *Parting Note*.
**Reader loses:** Nothing. Three of seven sentences survive verbatim, including the documentation-literacy passage; only the library name and the pointer to the next chapter change.

