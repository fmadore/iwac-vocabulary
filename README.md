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

### AI Provenance (7 properties)

Used as value annotations to document which AI model generated specific metadata values.

| Property | Description |
|----------|-------------|
| `iwac:ocrModel` | AI model used for text extraction |
| `iwac:summaryModel` | AI model used for summarization |
| `iwac:nerModel` | AI model used for named entity recognition |
| `iwac:transcriptionModel` | AI model used for audio/video transcription |
| `iwac:processingDate` | Date when AI processing was performed |
| `iwac:confidence` | Confidence score (0-1) |
| `iwac:modelVersion` | Specific version of the AI model |

### Sentiment Analysis (18 properties)

Each annotator model has 6 properties:

| Property Pattern | Description |
|------------------|-------------|
| `iwac:{model}Centralite` | Centrality level of Islam/Muslims in the article |
| `iwac:{model}CentraliteJustification` | Explanation for centrality rating |
| `iwac:{model}Polarite` | Sentiment polarity toward Islam/Muslims |
| `iwac:{model}PolariteJustification` | Explanation for polarity rating |
| `iwac:{model}SubjectiviteScore` | Subjectivity score (1-5) |
| `iwac:{model}SubjectiviteJustification` | Explanation for subjectivity score |

#### Which model produced which values

The generation-1 property sets are keyed by **vendor**, and sentiment values
carry no `iwac:*Model` annotation — so the property name alone does not identify
the model. The corpus was annotated in January–February 2026 (campaign window
verified from `o:modified`) by:

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

> **Adding a model:** define a new property set named for the model
> (`iwac:mistralSmall4Centralite`, …). Never reuse a vendor slot for a different
> model — that is what made generation 1 ambiguous. The canonical panel lives in
> [`iwac_common/sentiment_panel.py`](https://github.com/fmadore/IWAC-Hugging-Face)
> in the Hugging Face export repository.

## Usage with Omeka S

### Import Vocabulary

1. Navigate to **Admin → Vocabularies → Import new vocabulary**
2. Upload `iwac-vocabulary.ttl`
3. Set:
   - **Label**: IWAC Ontology
   - **Namespace URI**: `https://islam.zmo.de/ontology/iwac#`
   - **Namespace prefix**: `iwac`
4. Click **Import**

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

## Related Projects

- [Islam West Africa Collection](https://islam.zmo.de/s/westafrica/) - The digital archive
- [IWAC on Hugging Face](https://huggingface.co/datasets/fmadore/islam-west-africa-collection) - Dataset export
- [IWAC Sentiment Analysis](https://github.com/fmadore/IWAC-sentiment-analysis) - Sentiment analysis dashboard
- [IWAC AI Pipelines](https://github.com/fmadore/iwac-ai-pipelines) - AI processing workflows

## License

This vocabulary is licensed under [CC0 1.0 Universal](LICENSE).

## Author

[Frédérick Madore](https://frederickmadore.com/) - Leibniz-Zentrum Moderner Orient (ZMO), Berlin
