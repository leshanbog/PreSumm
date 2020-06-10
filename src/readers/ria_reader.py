import json
import re
from typing import Dict

from bs4 import BeautifulSoup
from allennlp.data.dataset_readers.dataset_reader import DatasetReader
from allennlp.data.tokenizers.tokenizer import Tokenizer
from allennlp.data.token_indexers.token_indexer import TokenIndexer
from allennlp.data.tokenizers import WordTokenizer
from allennlp.data.tokenizers.word_splitter import SimpleWordSplitter

from readers.summarization_reader import SummarizationReader


def parse_ria_json(path):
    with open(path, "r", encoding="utf-8") as r:
        pat = '{\"text\": \"(.*)\", \"title\": \"(.*)\"}' 
        i = 0
        for line in r:
            #data = json.loads(line.strip())
            data = re.search(pat, line.strip())

            title = data.group(2).lower().strip()
            clean_text = data.group(1).lower().replace('\xa0', ' ').replace('\n', ' ').strip()
#            clean_text = BeautifulSoup(text, 'html.parser').text.replace('\xa0', ' ').replace('\n', ' ')
            if not clean_text or not title or clean_text.count(' ') < 3 or title.count(' ') < 3:
                continue
            if i % 300 == 0:
                print(clean_text)
                print(title)
            i += 1
            yield clean_text, title


@DatasetReader.register("ria")
class RIAReader(SummarizationReader):
    def __init__(self,
                 tokenizer: Tokenizer = None,
                 source_token_indexers: Dict[str, TokenIndexer] = None,
                 target_token_indexers: Dict[str, TokenIndexer] = None,
                 source_max_tokens: int = 400,
                 target_max_tokens: int = 100,
                 separate_namespaces: bool = False,
                 target_namespace: str = "target_tokens",
                 save_copy_fields: bool = False,
                 save_pgn_fields: bool = False) -> None:
        if not tokenizer:
            tokenizer = WordTokenizer(word_splitter=SimpleWordSplitter())
        super().__init__(
            tokenizer=tokenizer,
            source_token_indexers=source_token_indexers,
            target_token_indexers=target_token_indexers,
            source_max_tokens=source_max_tokens,
            target_max_tokens=target_max_tokens,
            separate_namespaces=separate_namespaces,
            target_namespace=target_namespace,
            save_copy_fields=save_copy_fields,
            save_pgn_fields=save_pgn_fields
        )

    def parse_set(self, path):
        return parse_ria_json(path)
