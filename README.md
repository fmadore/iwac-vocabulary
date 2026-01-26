# IWAC Vocabulary

RDF vocabulary for the [Islam West Africa Collection (IWAC)](https://islam.zmo.de/s/westafrica/), a digital archive of primary sources on Islam in West Africa hosted by the Leibniz-Zentrum Moderner Orient (ZMO).

## Overview

This vocabulary provides properties for:

- **AI Processing Provenance**: Track which AI models generated specific metadata (OCR, summaries, named entity recognition)
- **Sentiment Analysis**: Store multi-model sentiment analysis results (Gemini, ChatGPT, Mistral)

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

Each of three AI models (Gemini, ChatGPT, Mistral) has 6 properties:

| Property Pattern | Description |
|------------------|-------------|
| `iwac:{model}Centralite` | Centrality level of Islam/Muslims in the article |
| `iwac:{model}CentraliteJustification` | Explanation for centrality rating |
| `iwac:{model}Polarite` | Sentiment polarity toward Islam/Muslims |
| `iwac:{model}PolariteJustification` | Explanation for polarity rating |
| `iwac:{model}SubjectiviteScore` | Subjectivity score (1-5) |
| `iwac:{model}SubjectiviteJustification` | Explanation for subjectivity score |

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
