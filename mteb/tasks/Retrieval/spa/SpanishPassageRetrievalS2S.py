from __future__ import annotations

import datasets

from mteb.abstasks.TaskMetadata import TaskMetadata

from ....abstasks.AbsTaskRetrieval import AbsTaskRetrieval


class SpanishPassageRetrievalS2S(AbsTaskRetrieval):
    metadata = TaskMetadata(
        name="SpanishPassageRetrievalS2S",
        description="Test collection for passage retrieval from health-related Web resources in Spanish.",
        reference="https://mklab.iti.gr/results/spanish-passage-retrieval-dataset/",
        dataset={
            "path": "jinaai/spanish_passage_retrieval",
            "revision": "9cddf2ce5209ade52c2115ccfa00eb22c6d3a837",
            "trust_remote_code": True,
        },
        type="Retrieval",
        category="s2s",
        modalities=["text"],
        eval_splits=["test"],
        eval_langs=["spa-Latn"],
        main_score="ndcg_at_10",
        date=None,
        domains=None,
        task_subtypes=None,
        license=None,
        annotations_creators=None,
        dialect=None,
        sample_creation=None,
        bibtex_citation=r"""
@inproceedings{10.1007/978-3-030-15719-7_19,
  abstract = {This paper describes a new test collection for passage retrieval from health-related Web resources in Spanish. The test collection contains 10,037 health-related documents in Spanish, 37 topics representing complex information needs formulated in a total of 167 natural language questions, and manual relevance assessments of text passages, pooled from multiple systems. This test collection is the first to combine search in a language beyond English, passage retrieval, and health-related resources and topics targeting the general public.},
  address = {Cham},
  author = {Kamateri, Eleni
and Tsikrika, Theodora
and Symeonidis, Spyridon
and Vrochidis, Stefanos
and Minker, Wolfgang
and Kompatsiaris, Yiannis},
  booktitle = {Advances in Information Retrieval},
  editor = {Azzopardi, Leif
and Stein, Benno
and Fuhr, Norbert
and Mayr, Philipp
and Hauff, Claudia
and Hiemstra, Djoerd},
  isbn = {978-3-030-15719-7},
  pages = {148--154},
  publisher = {Springer International Publishing},
  title = {A Test Collection for Passage Retrieval Evaluation of Spanish Health-Related Resources},
  year = {2019},
}
""",
    )

    def load_data(self, **kwargs):
        if self.data_loaded:
            return

        query_rows = datasets.load_dataset(
            name="queries",
            split="test",
            **self.metadata_dict["dataset"],
        )
        corpus_rows = datasets.load_dataset(
            name="corpus.sentences",
            split="test",
            **self.metadata_dict["dataset"],
        )
        qrels_rows = datasets.load_dataset(
            name="qrels.s2s",
            split="test",
            **self.metadata_dict["dataset"],
        )

        self.queries = {"test": {row["_id"]: row["text"] for row in query_rows}}
        self.corpus = {"test": {row["_id"]: row for row in corpus_rows}}
        self.relevant_docs = {
            "test": {
                row["_id"]: dict.fromkeys(row["text"].split(" "), 1)
                for row in qrels_rows
            }
        }

        self.data_loaded = True
