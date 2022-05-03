from data_read import string_read
from typing import Dict, List, Tuple
import logging
import json

from allennlp.common.file_utils import cached_path
from allennlp.data.dataset_readers.dataset_reader import DatasetReader
from allennlp.data.fields import AdjacencyField, MetadataField, SequenceLabelField
from allennlp.data.fields import Field, TextField
from allennlp.data.token_indexers import SingleIdTokenIndexer, TokenIndexer
from allennlp.data.tokenizers import Token
from allennlp.data.instance import Instance

from data_read import string_read

logger = logging.getLogger(__name__)

'''
Note: 
This piece of code is heavily borrowed from an existing repo in AllenNLP for reading Semantic_Dependencies data in  
SemEval 2015 Task 18 format, see https://github.com/allenai/allennlp-models/blob/f233052df9feb03f636007dd25c0a3b8d4b546d6/allennlp_models/structured_prediction/dataset_readers/semantic_dependencies.py#L127
'''


def parse(json_object):  # simple iterator for a json_object
    for entry in json_object:
        if entry:
            yield parse_entry(entry)


def parse_entry(entry):   # retrieving processed inputs consisting of lists
    sentence_id = entry[0]
    sentence_string = entry[1]
    AMR = entry[3]
    #print(AMR)
    token_list, token_seq_label, adjacency_list, adjacency_label_list = string_read(AMR) # string_read is the function
    # called from data_read.py, where we parse the AMR-input into lists of tuples of indices and lists of seq_labels.
    return sentence_id, sentence_string, token_list, token_seq_label, adjacency_list, adjacency_label_list


@DatasetReader.register("ULF")
class UnscopedLogicalFormDatasetReader(DatasetReader):
    """
    Reads a file in the ULF annotation format, see https://www.cs.rochester.edu/u/gkim21/ulf/resources/
    Registered as a `DatasetReader` with name "ULF".

    The following codes are heavily borrowed from a known repo of AllenNLP (see heading note). We simply altered the input to match
    the format in ULF and create a iterator that yields a similar instance that describes an annotated graph, with an
    adjacency_field and several seq_label_fields.
    """

    def __init__(
            self,
            token_indexers: Dict[str, TokenIndexer] = None,
            skip_when_no_arcs: bool = True,
            **kwargs,
    ) -> None:
        '''
        this part is directly borrowed to match the format
        '''
        super().__init__(**kwargs)
        self._token_indexers = token_indexers or {"tokens": SingleIdTokenIndexer()}
        self._skip_when_no_arcs = skip_when_no_arcs

    def _read(self, file_path: str):
        # if `file_path` is a URL, redirect to the cache
        file_path = cached_path(file_path)

        logger.info("Reading semantic dependency parsing data from: %s", file_path)

        with open(file_path) as f:
            json_object = json.load(f)
            for sentence_id, sentence_string, token_list, token_tags, arcs, arc_tags in \
                    parse(json_object):
                if self._skip_when_no_arcs and not arcs:
                    continue
                yield self.text_to_instance(sentence_id, sentence_string, token_list, token_tags, arcs, arc_tags)
            # result = token_list, token_seq_label, adjacency_list, adjacency_label_list

    def text_to_instance(
            self,  # type: ignore
            sentence_id: int,  # metadata_field input
            sentence_string: str,  # metadata_field input
            tokens: List[str],  # TextField input
            token_tags: List[str] = None,  # Seq_label_field input
            arc_indices: List[Tuple[int, int]] = None,  # adjacency_field_input
            arc_tags: List[str] = None,  # a seq_label_field input for adjacency_field
    ) -> Instance:

        fields: Dict[str, Field] = {}
        token_field = TextField([Token(t) for t in tokens], self._token_indexers)
        fields["tokens"] = token_field
        fields["metadata"] = MetadataField({"tokens": tokens, "id": sentence_id, "string": sentence_string})
        if token_tags is not None:
            #print(token_tags)
            #print(token_field)
            fields["token_tags"] = SequenceLabelField(token_tags, token_field, label_namespace="tokens")
        if arc_indices is not None and arc_tags is not None:
            #print(arc_indices)
            #print(type(token_field))
            #print(arc_tags)
            fields["arc_tags"] = AdjacencyField(arc_indices, token_field, arc_tags)

        return Instance(fields)


