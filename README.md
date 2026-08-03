# IWAC Vocabulary

RDF vocabulary for the [Islam West Africa Collection (IWAC)](https://islam.zmo.de/s/westafrica/), a digital archive of primary sources on Islam in West Africa hosted by the Leibniz-Zentrum Moderner Orient (ZMO).

## Overview

This vocabulary provides properties for:

- **AI Processing Provenance**: Track which AI models generated specific metadata (OCR, summaries, named entity recognition)
- **Sentiment Analysis**: Store multi-model sentiment analysis results, one property set per annotator model

## Vocabulary Details

| Field | Value |
|-------|-------|
| **Namespace URI** | `https://islam.zmo.de/ontology/iwac#` |
| **Prefix** | `iwac` |
| **Format** | Turtle (.ttl) |
| **Languages** | English, French |

## Properties

### AI Provenance (8 properties)

Used as value annotations to document which AI model generated specific metadata values.

| Property | Description |
|----------|-------------|
| `iwac:ocrModel` | AI model used for text extraction |
| `iwac:summaryModel` | AI model used for summarization |
| `iwac:nerModel` | AI model used for named entity recognition |
| `iwac:transcriptionModel` | AI model used for audio/video transcription |
| `iwac:sentimentModel` | AI model that produced a sentiment annotation |
| `iwac:processingDate` | Date when AI processing was performed |
| `iwac:confidence` | Confidence score (0-1) |
| `iwac:modelVersion` | Specific version of the AI model |

### Sentiment Analysis (54 properties)

Each annotator model has 6 properties:

| Property Pattern | Description |
|------------------|-------------|
| `iwac:{model}Centralite` | Centrality level of Islam/Muslims in the article |
| `iwac:{model}CentraliteJustification` | Explanation for centrality rating |
| `iwac:{model}Polarite` | Sentiment polarity toward Islam/Muslims |
| `iwac:{model}PolariteJustification` | Explanation for polarity rating |
| `iwac:{model}SubjectiviteScore` | Subjectivity level — a 1–5 integer in generation 1, a label in generation 2 |
| `iwac:{model}SubjectiviteJustification` | Explanation for subjectivity score |

Two generations of property sets coexist. They are never mixed: a run writes to
one generation's properties and leaves the other's values exactly as they are.

#### Generation 2 (2026-07 onwards) — 36 properties

Keyed by **model**. The property name *is* the provenance, and it has to be:
Omeka does not index value annotations, so a model recorded only in an
`iwac:sentimentModel` annotation would be invisible to every query. The
annotation was written on 2026-07-31 and dropped the same day for that reason;
`iwac:sentimentModel` survives in the ontology for historical values, and the
current pipeline does not write it.

| Property prefix | Model id | Authority item | Hugging Face column prefix |
|---|---|---|---|
| `iwac:gemini35FlashLite*` | `gemini-3.5-flash-lite` | 79617 | `gemini_3_5_flash_lite_` |
| `iwac:gpt56Luna*` | `gpt-5.6-luna` | 79610 | `gpt_5_6_luna_` |
| `iwac:mistralSmall2603*` | `mistral-small-2603` | 79614 | `mistral_small_2603_` |
| `iwac:qwen35A10b*` | `qwen/qwen3.5-122b-a10b` | 79616 | `qwen3_5_122b_a10b_` |
| `iwac:deepseekV4Flash0731*` | `deepseek/deepseek-v4-flash-0731` | 83261 | `deepseek_v4_flash_0731_` |

**Retired but populated (6 properties).** `iwac:deepseekV4Flash*`
(`deepseek/deepseek-v4-flash`, item 79613, HF prefix `deepseek_v4_flash_`) holds
a completed preview-era run — 11,482 articles — from before the slot was pinned
to the dated `0731` snapshot. It stays declared here and is never repointed, so
those values keep naming the exact model that produced them. `RETIRED_PANEL` in
`sentiment_core.py` is the source for this block, and `00_setup_properties.py`
emits it alongside the active panel: a generator that emitted only the live
panel would turn every panel revision into a silent proposal to delete its
predecessor's values.

Every member is its vendor's **high-volume tier**, which is what makes the panel
a panel rather than a quality ladder. **Three of the five are open weights** and
can be re-run locally — Mistral Small 4 and Qwen3.5 under Apache-2.0, DeepSeek
V4 Flash under MIT — with active parameter counts of 6.5B, 10B and 13B, inside a
factor of two of each other. For an archive that is the difference between an
annotation you can cite and one that can only be taken on trust.

Two slots were re-pointed on 2026-07-31 before anything was written to either:
`iwac:qwen35A3b*` (3B active, a quarter of the panel's other open-weights
members) and `iwac:gemini36Flash*` (at $1.50/$7.50 per 1M, five to seventeen
times the rest — an inter-model disagreement involving it could always be read
as "the expensive model knows better" rather than as two readings of the
construct). Both were dropped from this file at the time but survived in the
live vocabulary until 2026-08-03, because removing a property needs an admin-UI
upload and none had happened since. Their twelve properties were re-verified
empty and are removed by that upload.

Unlike generation 1, `Centralite` and `Polarite` are declared
`owl:ObjectProperty` here, which is what the pipeline has always actually
written — links into the controlled vocabulary, not strings.

#### Generation 1 (January–February 2026) — 18 properties

Keyed by **vendor**, and the values carry no `iwac:*Model` annotation — so the
property name alone does not identify the model. The campaign window was
verified from `o:modified`; the models were recovered from commit `07fb007`:

| Property prefix | Model | Hugging Face column prefix |
|---|---|---|
| `iwac:gemini*` | `gemini-3-flash-preview` (Gemini 3 Flash) | `gemini_3_flash_preview_` |
| `iwac:chatgpt*` | `gpt-5-mini` (GPT-5 mini) | `gpt_5_mini_` |
| `iwac:mistral*` | `ministral-14b-2512` (Ministral 3 14B) | `ministral_14b_2512_` |

On Hugging Face the columns are keyed by the **exact model id** (hyphens and
dots folded to underscores), not the vendor, so a later generation cannot
silently redefine what a column means.

The three models did not share a run configuration. Reproducing a value needs:
`gemini-3-flash-preview` — temperature 0.2, response schema, no thinking level;
`gpt-5-mini` — response schema only, no temperature, no reasoning effort;
`ministral-14b-2512` — temperature 0.2, response schema, **max_tokens 512**.
No model in the generation-1 campaign ran with any reasoning or thinking parameter.

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
   - **Label**: IWAC Ontology
   - **Namespace URI**: `https://islam.zmo.de/ontology/iwac#`
   - **Namespace prefix**: `iwac`
4. Click **Import**

### Updating an already-imported vocabulary

On `islam.zmo.de` this vocabulary is already installed as **vocabulary 10**, so
new properties are *added*, not re-imported: **Admin → Vocabularies → IWAC
Ontology → Update**, uploading the new `.ttl`. Omeka diffs the file and lists
what it will change before you commit.

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
it; it happened twice when the panel was revised on 2026-07-31 (the Qwen slot, then
the Gemini one), each time verifying 6 doomed properties held nothing.

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
"iwac:gemini35FlashLitePolarite": [{
  "type": "resource:item",
  "value_resource_id": 78039
}]
```

## Related Projects

- [Islam West Africa Collection](https://islam.zmo.de/s/westafrica/) - The digital archive
- [IWAC on Hugging Face](https://huggingface.co/datasets/fmadore/islam-west-africa-collection) - Dataset export
- [IWAC Sentiment Analysis](https://github.com/fmadore/IWAC-sentiment-analysis) - Sentiment analysis dashboard
- [IWAC AI Pipelines](https://github.com/fmadore/iwac-ai-pipelines) - AI processing workflows

## License

This vocabulary is licensed under [CC0 1.0 Universal](LICENSE).

## Author

[Frédérick Madore](https://frederickmadore.com/) - Leibniz-Zentrum Moderner Orient (ZMO), Berlin
