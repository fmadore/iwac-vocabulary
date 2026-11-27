#!/usr/bin/env python3
"""Validate iwac-vocabulary.ttl, CITATION.cff, and README.md invariants."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, OWL, RDF, RDFS, XSD

ROOT = Path(__file__).resolve().parent.parent
TTL_PATH = ROOT / "iwac-vocabulary.ttl"
CFF_PATH = ROOT / "CITATION.cff"
README_PATH = ROOT / "README.md"

IWAC_URI = "https://islam.zmo.de/ontology/iwac#"
IWAC = Namespace(IWAC_URI)
VANN = Namespace("http://purl.org/vocab/vann/")

OMEKA_PROPERTY_TYPES = {
    RDF.Property,
    OWL.ObjectProperty,
    OWL.DatatypeProperty,
    OWL.SymmetricProperty,
    OWL.TransitiveProperty,
    OWL.FunctionalProperty,
    OWL.InverseFunctionalProperty,
}


def _heading_slug(heading: str) -> str:
    slug = heading.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug, flags=re.UNICODE)
    return re.sub(r"\s", "-", slug)


def validate() -> list[str]:
    errors: list[str] = []

    raw_ttl = TTL_PATH.read_text(encoding="utf-8")
    graph = Graph()
    try:
        graph.parse(data=raw_ttl, format="turtle")
    except Exception as exc:  # noqa: BLE001
        return [f"Turtle parse failed: {exc}"]

    # 1. Downstream contract checks (IWAC-docker update-vocabulary.sh & test_ontology.py)
    if f"@prefix iwac: <{IWAC_URI}> ." not in raw_ttl:
        errors.append(f"Missing exact prefix declaration: @prefix iwac: <{IWAC_URI}> .")
    if not re.search(r"^iwac: a owl:Ontology\b", raw_ttl, re.MULTILINE):
        errors.append("Missing line starting with 'iwac: a owl:Ontology'")
    if (IWAC[""], RDF.type, OWL.Ontology) not in graph:
        errors.append(f"{IWAC_URI} is not typed as owl:Ontology")
    if dict(graph.namespaces()).get("iwac") != IWAC[""]:
        errors.append("Prefix 'iwac' does not map to https://islam.zmo.de/ontology/iwac#")

    # 2. Ontology-level FAIR / LOV metadata
    ont = IWAC[""]
    for pred, name in [
        (RDFS.label, "rdfs:label"),
        (RDFS.comment, "rdfs:comment"),
        (DCTERMS.title, "dcterms:title"),
        (DCTERMS.description, "dcterms:description"),
    ]:
        langs = {o.language for o in graph.objects(ont, pred) if isinstance(o, Literal)}
        for req_lang in ("en", "fr"):
            if req_lang not in langs:
                errors.append(f"Ontology missing {name}@{req_lang}")

    creators = list(graph.objects(ont, DCTERMS.creator))
    if not creators or not all(isinstance(c, URIRef) for c in creators):
        errors.append("Ontology dcterms:creator must be an agent URI (e.g. ORCID)")

    licenses = list(graph.objects(ont, DCTERMS.license))
    if not licenses or not all(isinstance(lic, URIRef) for lic in licenses):
        errors.append("Ontology dcterms:license must be a URI")

    if graph.value(ont, VANN.preferredNamespacePrefix) != Literal("iwac"):
        errors.append('Ontology missing vann:preferredNamespacePrefix "iwac"')
    if graph.value(ont, VANN.preferredNamespaceUri) != Literal(IWAC_URI):
        errors.append(f'Ontology missing vann:preferredNamespaceUri "{IWAC_URI}"')

    version_info = graph.value(ont, OWL.versionInfo)
    if not isinstance(version_info, Literal) or not str(version_info).strip():
        errors.append("Ontology missing owl:versionInfo")

    version_iri = graph.value(ont, OWL.versionIRI)
    if not isinstance(version_iri, URIRef) or version_iri == ont:
        errors.append("Ontology missing distinct owl:versionIRI")

    # 3. Term-level checks
    typed_terms = {s for s in graph.subjects(RDF.type, None) if s != ont}
    if not typed_terms:
        errors.append("No vocabulary terms declared")

    for term in sorted(typed_terms, key=str):
        if not str(term).startswith(IWAC_URI):
            errors.append(
                f"Non-iwac typed subject {term} breaks IWAC-docker/tests/test_ontology.py"
            )
            continue

        local_name = str(term)[len(IWAC_URI) :]
        types = set(graph.objects(term, RDF.type))
        if not (types & OMEKA_PROPERTY_TYPES):
            errors.append(f"iwac:{local_name} has no Omeka-supported property type: {types}")

        for pred, name in [(RDFS.label, "rdfs:label"), (RDFS.comment, "rdfs:comment")]:
            langs = {o.language for o in graph.objects(term, pred) if isinstance(o, Literal)}
            for req_lang in ("en", "fr"):
                if req_lang not in langs:
                    errors.append(f"iwac:{local_name} missing {name}@{req_lang}")

        if (term, RDFS.isDefinedBy, ont) not in graph:
            errors.append(f"iwac:{local_name} missing rdfs:isDefinedBy iwac:")

        if local_name.endswith("Model") and OWL.ObjectProperty not in types:
            errors.append(f"iwac:{local_name} must be owl:ObjectProperty (links to authority item)")

        if local_name.endswith("Justification") and (term, RDFS.range, XSD.string) in graph:
            errors.append(
                f"iwac:{local_name} uses rdfs:range xsd:string instead of rdf:langString"
            )

        for parent in graph.objects(term, RDFS.subPropertyOf):
            if str(parent).startswith(IWAC_URI) and parent not in typed_terms:
                errors.append(f"iwac:{local_name} rdfs:subPropertyOf undeclared local term {parent}")

    # 4. 00_setup_properties.py ttl_terms() textual contract
    regex_terms = re.findall(r"^iwac:(\w+)\s+a\s+owl:", raw_ttl, re.MULTILINE)
    if len(regex_terms) != len(typed_terms):
        errors.append(
            f"Regex ^iwac:(\\w+)\\s+a\\s+owl: matched {len(regex_terms)} terms, "
            f"expected {len(typed_terms)} (00_setup_properties.py contract)"
        )

    # 5. CITATION.cff parity
    cff = yaml.safe_load(CFF_PATH.read_text(encoding="utf-8"))
    if not isinstance(cff, dict):
        errors.append("CITATION.cff did not parse to a mapping")
    elif version_info and str(cff.get("version")) != str(version_info):
        errors.append(
            f"CITATION.cff version ({cff.get('version')!r}) != owl:versionInfo ({str(version_info)!r})"
        )

    # 6. README internal anchors
    readme = README_PATH.read_text(encoding="utf-8")
    headings = {
        _heading_slug(m.group(1))
        for m in re.finditer(r"^#{1,6}\s+(.+)$", readme, re.MULTILINE)
    }
    for anchor in re.findall(r"\]\(#([^)]+)\)", readme):
        if anchor not in headings:
            errors.append(f"README.md contains broken internal anchor: #{anchor}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print("OK: iwac-vocabulary.ttl, CITATION.cff, and README.md passed all checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
