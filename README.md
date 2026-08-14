# IWAC Vocabulary

RDF vocabulary for the [Islam West Africa Collection (IWAC)](https://islam.zmo.de/s/westafrica/), a digital archive of primary sources on Islam in West Africa hosted by the Leibniz-Zentrum Moderner Orient (ZMO).

## Overview

This vocabulary provides properties for:

- **AI Processing Provenance**: Track which AI models generated specific metadata (OCR, summaries, named entity recognition)
- **Sentiment Analysis**: Store multi-model sentiment analysis results, one property set per annotator model

## Vocabulary Details

| Field | Value |
|-------|-------|
| **Namespace URI** | `https://islam.zmo.de/ontology/iwac#` (non-dereferenceable; the file is the canonical copy) |
| **Prefix** | `iwac` |
| **Format** | Turtle (.ttl) |
| **Languages** | English, French |
| **Version** | 1.3 (`owl:versionInfo`), modified 2026-08-14 |
| **Properties in this file** | **32** — 8 provenance + 24 sentiment |
| **Properties installed on `islam.zmo.de`** | **74** (vocabulary 10) |

> **The file and the live archive have not converged yet.** `iwac-vocabulary.ttl`
> was trimmed to 32 properties on 2026-08-07 and its Google slot re-pointed to
> Gemma 4 31B on 2026-08-14; neither *vocabulary update* has been performed, so
> Omeka still declares all 74 and none of Gemma's six. The 48 surplus
> declarations are empty shells — the generation-1 values were deleted
> separately through the item API, the rest were never written, and every one is
> verified at 0 items. See
> [Updating an already-imported vocabulary](#updating-an-already-imported-vocabulary).
>
> Counts below verified against the live API on **2026-08-14**.

## Properties

### AI Provenance (8 properties)

Used as value annotations to document which AI model generated specific metadata values.

| Property | Description |
|----------|-------------|
| `iwac:ocrModel` | AI model used for text extraction |
| `iwac:summaryModel` | AI model used for summarization |
| `iwac:nerModel` | AI model used for named entity recognition |
| `iwac:transcriptionModel` | AI model used for audio/video transcription |
| `iwac:sentimentModel` | AI model that produced a sentiment annotation — **legacy**, see [Generation 2](#generation-2-2026-07-onwards--24-properties) |
| `iwac:processingDate` | Date when AI processing was performed |
| `iwac:confidence` | Confidence score (0-1) |
| `iwac:modelVersion` | Specific version of the AI model |

These are live and in use: `iwac:ocrModel` and `iwac:summaryModel` are written on
every OCR and summary run. A query cannot see them (annotations are unindexed),
but a `GET` on any article shows them — e.g. item 2233 carries
`iwac:summaryModel` → `GPT-5.6 Luna` on both its French and English
`bibo:shortDescription`.

### Sentiment Analysis (24 properties)

Each annotator model has 6 properties:

| Property Pattern | Description |
|------------------|-------------|
| `iwac:{model}Centralite` | Centrality level of Islam/Muslims in the article |
| `iwac:{model}CentraliteJustification` | Explanation for centrality rating |
| `iwac:{model}Polarite` | Sentiment polarity toward Islam/Muslims |
| `iwac:{model}PolariteJustification` | Explanation for polarity rating |
| `iwac:{model}SubjectiviteScore` | Subjectivity level — a 1–5 integer in generation 1, a label in generation 2 |
| `iwac:{model}SubjectiviteJustification` | Explanation for subjectivity score |

**Only generation 2 carries values.** The vendor-keyed generation-1 sets and the
retired DeepSeek preview were emptied on the live archive on 2026-08-07 and
dropped from this file; their *declarations* survive on Omeka until the pending
vocabulary update runs. See [Generation 1](#generation-1-januaryfebruary-2026--archived-on-hugging-face)
below for where that campaign now lives.

#### Generation 2 (2026-07 onwards) — 24 properties

Keyed by **model**. The property name *is* the provenance, and it has to be:
Omeka does not index value annotations, so a model recorded only in an
`iwac:sentimentModel` annotation would be invisible to every query. The
annotation was written on 2026-07-31 and dropped the same day for that reason;
`iwac:sentimentModel` survives in the ontology for historical values, and the
current pipeline does not write it.

| Property prefix | Model id | Authority item | Hugging Face column prefix |
|---|---|---|---|
| `iwac:gpt56Luna*` | `gpt-5.6-luna` | 79610 | `gpt_5_6_luna_` |
| `iwac:mistralSmall2603*` | `mistral-small-2603` | 79614 | `mistral_small_2603_` |
| `iwac:deepseekV4Flash0731*` | `deepseek/deepseek-v4-flash-0731` | 83261 | `deepseek_v4_flash_0731_` |
| `iwac:gemma431bIt*` | `google/gemma-4-31b-it` | 111663 | — (declared here, not yet installed) |

##### Population (live, 2026-08-14)

The annotated universe is **12,305** of the 12,356 `bibo:Article` items — the
Français and Anglais ones. The other 51 (Ewé, Kabiyè, Dendi, no language) are
skipped deliberately: the prompt is French, and a French-prompted model returns
confident but unusable output for them rather than failing visibly.

| Property prefix | Centralité | Polarité | Subjectivité | …Justification (C / P / S) |
|---|---:|---:|---:|---|
| `iwac:gpt56Luna*` | 12,305 | 12,305 | **12,015** | 12,305 / 12,305 / 12,305 |
| `iwac:mistralSmall2603*` | 12,305 | 12,305 | **12,051** | 12,305 / 12,305 / 12,305 |
| `iwac:deepseekV4Flash0731*` | 12,305 | 12,305 | **11,816** | 12,305 / 12,305 / 12,304 |
| `iwac:gemma431bIt*` | — | — | — | not installed yet |

**"Complete" is per property, not per model.** The writer omits any field the
model left empty, so all three active members are complete on centralité and
polarité and short on subjectivité — by different amounts, and for different
reasons. Never infer a missing score from a present justification: DeepSeek has
12,304 subjectivité justifications against 11,816 scores, so ~488 articles carry
the reasoning with no score attached.

The three shortfalls are **not** comparable to each other. A model that declines
to score objectivity on an article it judged `Non abordé` is not disagreeing
about objectivity — it is saying the article is not about Islam. Condition on
centralité before aligning models, never on the subjectivité nulls.

**The Google slot has never held a value, and on 2026-08-14 it changed occupant
rather than contents.** It was `iwac:gemini35FlashLite*` from 2026-07-31,
declared on Omeka and verified at 0 items on the day of the swap; this file now
declares `iwac:gemma431bIt*` instead, so the pending vocabulary update adds
Gemma's six and drops Flash-Lite's six. Because Flash-Lite never ran, nothing is
mixed and generation 2 is unchanged by the substitution. Neither prefix has a
Hugging Face column on either dataset repo — do not write code expecting a
`gemini_3_5_flash_lite_*` one, and `gemma_4_31b_it_*` will not exist until a run
produces values and the uploader's panel is extended to carry them.

Every member is its vendor's **high-volume tier**, which is what makes the panel
a panel rather than a quality ladder — and it is why the Google slot moved: at
$0.30/$2.50 per 1M, Flash-Lite was the panel's remaining cost outlier at roughly
four times a DeepSeek pass, where Gemma sits at $0.09/$0.34. **Three of the four
are now open weights** and can be re-run locally — Gemma 4 31B and Mistral
Small 4 under Apache-2.0, DeepSeek V4 Flash under MIT — though at 31B (dense),
6.5B and 13B active parameters the spread is a factor of five where the previous
pair sat inside a factor of two, so an agreement figure among them does slightly
more to measure model size than it used to. For an archive the trade is still
worth it: it is the difference between an annotation you can cite and one that
can only be taken on trust.

Gemma is routed through **OpenRouter**, never `GEMINI_API_KEY`: it is
free-of-charge on the Gemini API with no paid tier, and Google's pricing page
states that free-tier content is used to improve its products — unacceptable when
the request body is a whole archival article.

`Centralite`, `Polarite` and `SubjectiviteScore` are `owl:ObjectProperty` here,
which is what the pipeline actually writes — links into the controlled
vocabulary, not strings. The generation-1 declarations called two of the three
`owl:DatatypeProperty`, which never matched.

**Four** slots were declared and never written, and this file drops all
twenty-four of their properties: `iwac:qwen35A3b*` (3B active, a quarter of the
other open-weights members) and `iwac:gemini36Flash*` (at $1.50/$7.50 per 1M,
five to seventeen times the rest — an inter-model disagreement involving it
could always be read as "the expensive model knows better" rather than as two
readings of the construct), both re-pointed on 2026-07-31; then
`iwac:qwen35A10b*`, dropped 2026-08-05 on serving grounds — OpenRouter listed
five endpoints for it against DeepSeek's 22, one without structured-output
support, putting its median call at 104 s where the rest of the panel sat at
4–6 s; and now `iwac:gemini35FlashLite*`, replaced by Gemma on 2026-08-14.

Gemma was checked against that Qwen precedent before being declared, because it
is the same shape of risk: OpenRouter lists **19** endpoints for
`google/gemma-4-31b-it`, **16** of which support structured outputs, so
`require_parameters` leaves a deep pool rather than Qwen's four. Its median call
is nevertheless ~72 s — slower than DeepSeek — so the corpus pass is a matter of
days, not hours.

#### Generation 1 (January–February 2026) — archived on Hugging Face

Keyed by **vendor**, and the values carried no `iwac:*Model` annotation — so the
property name alone did not identify the model. **Deleted from Omeka on
2026-08-07** (all 18 verified at 0 items) after the values were confirmed present
on the Hugging Face full mirror, which is now their only copy:

| Former property prefix | Model | Hugging Face column prefix |
|---|---|---|
| `iwac:gemini*` | `gemini-3-flash-preview` (Gemini 3 Flash) | `gemini_3_flash_preview_` |
| `iwac:chatgpt*` | `gpt-5-mini` (GPT-5 mini) | `gpt_5_mini_` |
| `iwac:mistral*` | `ministral-14b-2512` (Ministral 3 14B) | `ministral_14b_2512_` |

Those columns are frozen in the uploader's panel with `omeka_prefix=None`, so
`hub_merge` preserves what the uploader no longer emits. Nothing re-derives them.

The three models did not share a run configuration, and reading the archived
columns needs it: `gemini-3-flash-preview` — temperature 0.2, response schema, no
thinking level; `gpt-5-mini` — response schema only, no temperature, no reasoning
effort; `ministral-14b-2512` — temperature 0.2, response schema, **max_tokens
512**, the only model with an output cap. No model in the campaign ran with any
reasoning or thinking parameter. The campaign window was verified from
`o:modified` and the models recovered from commit `07fb007`.

`iwac:deepseekV4Flash*` (the April preview, item 79613) was deleted the same day.
Its 11,482 annotations were never exported to Hugging Face and are gone — a
deliberate choice, and not to be confused with `iwac:deepseekV4Flash0731*`, which
is a different run rather than a newer copy of the same one.

> **Adding a model:** define a new property set named for the model, never for
> its vendor — reusing a vendor slot is what made generation 1 ambiguous. Do not
> hand-write the Turtle: the panel is defined once in
> [`AI_sentiment_analysis/sentiment_core.py`](https://github.com/fmadore/iwac-ai-pipelines)
> (`PANEL`), and `00_setup_properties.py --emit-ttl` generates this file's
> property blocks from it. That script cannot create them in Omeka — see below
> for why — so the upload is a manual step, and `--verify` is what keeps the
> file and the live instance from drifting.

## Usage with Omeka S

### Import Vocabulary

1. Navigate to **Admin → Vocabularies → Import new vocabulary**
2. Upload `iwac-vocabulary.ttl`
3. Set:
   - **Label**: IWAC ontology
   - **Namespace URI**: `https://islam.zmo.de/ontology/iwac#`
   - **Namespace prefix**: `iwac`
4. Click **Import**

The namespace URI is an identifier, not a download link — it does not resolve
(`404`). Fetch the vocabulary from this repository instead:

```bash
curl -fsSO https://raw.githubusercontent.com/fmadore/iwac-vocabulary/main/iwac-vocabulary.ttl
```

### Updating an already-imported vocabulary

On `islam.zmo.de` this vocabulary is already installed as **vocabulary 10**
(label *IWAC ontology*), so new properties are *added*, not re-imported: **Admin
→ Vocabularies → IWAC ontology → Update**, uploading the new `.ttl`. Omeka diffs
the file and lists what it will change before you commit.

**The REST API cannot do this on Omeka S 4.2.x.** `PropertyAdapter::hydrate()`
never reads `o:vocabulary`, so `POST /api/properties` always fails validation
with "A vocabulary must be set" — the hydration exists only on `develop`.
(`PATCH /api/vocabularies/10` *can* add properties, but the same hydrate
**removes every property absent from the request**, without the admin UI's diff
preview. Avoid it.)

Adding a property is safe. **Removing one deletes every value stored under it
across the archive** — and Omeka treats "absent from the uploaded file" as
removal. Always pre-flight:

```bash
python AI_sentiment_analysis/00_setup_properties.py --verify
```

That compares the `.ttl` against the live vocabulary and, for anything the file
would delete, **counts the values that would be destroyed** — refusing if any is
non-empty. It checks rather than offering an override flag, because an operator
asserting "those are empty" is the step that gets skipped on the day it is
wrong. Retiring a never-used property is legitimate and the pre-flight will pass
it.

#### Pending: the 2026-08-07 trim and the Gemma swap (not yet uploaded)

This file currently stages the largest such change so far. As of **2026-08-14**
the pre-flight reports:

```
Installed in Omeka       74
Declared in the .ttl     32
Would be added            6
Would be DELETED         48
✓ Safe to upload — 6 additions, 48 deletions — all verified empty.
```

The 6 additions are Gemma's. The 48 deletions break down as **18** generation-1
(`iwac:gemini*`, `iwac:chatgpt*`, `iwac:mistral*`), **6** DeepSeek April preview
(`iwac:deepseekV4Flash*`), and **24** never-written (`iwac:gemini36Flash*`,
`iwac:qwen35A3b*`, `iwac:qwen35A10b*`, `iwac:gemini35FlashLite*`). An independent
per-property count over the item API agrees: all 48 are at 0 items.

Emptying the values and removing the declarations are **two separate steps**.
The first was done on 2026-08-07 through the item API; the second is this
vocabulary update, and it is still outstanding. Until someone runs it, Omeka
keeps listing 48 properties that can never hold anything and none of the six
Gemma needs — the first is harmless, but the second means `01_sentiment_analysis`
cannot annotate with Gemma at all: `resolve_property_ids` fails loudly on the
missing terms rather than writing a partial set. Either way, a property list read
from the live API is not the vocabulary this file describes. Re-run `--verify`
immediately before uploading; a green result from last week is not a green result
today.

> **The pre-flight is blind to value annotations.** It counts with Omeka's
> `property[type]=ex` item filter, which does not see annotation values — the
> same indexing gap that pushed generation-2 provenance into property names. So
> the eight AI-provenance properties above will report "empty" whatever they
> actually hold, and `iwac:ocrModel` and `iwac:summaryModel` are written on
> every OCR and summary run. Never let a green pre-flight authorise deleting an
> annotation property; those eight are cheap to keep and must stay in the file.

### Value Annotations Example

```json
"bibo:content": [{
  "@value": "Le président de la République...",
  "@annotation": {
    "iwac:ocrModel": [{"@value": "Gemini 2.5 Pro"}],
    "iwac:processingDate": [{"@value": "2026-01-15"}]
  }
}]
```

Generation-2 sentiment values carry **no** annotation. The model is in the
property name, which is the only layer an Omeka query can reach, and the value
is a link into the controlled vocabulary:

```json
"iwac:gemma431bItPolarite": [{
  "type": "resource:item",
  "value_resource_id": 78039
}]
```

## Repository contents

| File | What it is |
|---|---|
| [`iwac-vocabulary.ttl`](iwac-vocabulary.ttl) | The vocabulary. Generated from `PANEL`; do not hand-edit the sentiment blocks. |
| [`CITATION.cff`](CITATION.cff) | Citation metadata. |
| [`LICENSE`](LICENSE) | CC0 1.0 Universal. |

## Related Projects

- [Islam West Africa Collection](https://islam.zmo.de/s/westafrica/) — the digital archive (French UI: [`/s/afrique_ouest/`](https://islam.zmo.de/s/afrique_ouest/))
- [IWAC on Hugging Face](https://huggingface.co/datasets/fmadore/islam-west-africa-collection) — dataset export; the sentiment columns are the values stored under these properties
- [IWAC AI Pipelines](https://github.com/fmadore/iwac-ai-pipelines) — the code that writes them, and where `00_setup_properties.py` lives
- [IWAC Sentiment Analysis](https://github.com/fmadore/IWAC-sentiment-analysis) — inter-model agreement dashboard

## Citation

See [`CITATION.cff`](CITATION.cff), or:

> Madore, Frédérick (2026). *IWAC Vocabulary: an RDF vocabulary for AI processing
> provenance and sentiment annotation in the Islam West Africa Collection*.
> https://github.com/fmadore/iwac-vocabulary

## License

[CC0 1.0 Universal](LICENSE) — public domain dedication. Reuse the property
definitions freely, with or without attribution. This covers the vocabulary
only; the annotations stored under it in the IWAC dataset are
[CC-BY-NC-SA-4.0](https://huggingface.co/datasets/fmadore/islam-west-africa-collection).

## Author

[Frédérick Madore](https://frederickmadore.com/) ([ORCID 0000-0003-0959-2092](https://orcid.org/0000-0003-0959-2092)),
University of Bayreuth. The IWAC archive is hosted by the Leibniz-Zentrum
Moderner Orient (ZMO), Berlin.
