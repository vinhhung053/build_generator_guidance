import transformers
import numpy as np
from bytetrie import ByteTrie


class Generator:
    def __init__(self, model_name):
        self.model = transformers.AutoModelForCausalLM.from_pretrained(model_name)
        self.tkz = transformers.AutoTokenizer.from_pretrained(model_name, use_fast=False)
        self.byte_tokens = [bytes(self.tkz.convert_tokens_to_string(['a', self.tkz.convert_ids_to_tokens(i)])[1:], encoding="utf8") for i in range(len(self.tkz))]

    def _tokenize_prefix(self, sentences, _token_trie):
        '''This is used to speed up the tokenization of long prompts without using the parser.'''
        token_ids = []
        token_byte_positions = []
        byte_string = bytes(sentences, encoding="utf8")
        # loop trying to decode a new token at each iteration
        pos = 0
        while True:

            # walk down the token trie looking for a unique token match
            trie = _token_trie
            valid_pos = -1
            valid_value = -1
            while True:
                if pos >= len(byte_string):
                    # 2 dong duoi em comment, du doan la bug cua tac gia
                    # if len(trie.children) > 0:
                    #     valid_pos = -1
                    break

                # check if we can keep going or are at a dead end
                if byte_string[pos:pos + 1] in trie.children:
                    trie = trie.children[byte_string[pos:pos + 1]]
                    pos += 1

                    # record the last valid token down this path as we go
                    if trie.value is not None:
                        valid_pos = pos
                        valid_value = trie.value
                else:
                    break  # we can't go any farther
            if valid_pos == -1:
                break
            else:
                token_ids.append(valid_value)
                token_byte_positions.append(valid_pos)
                pos = valid_pos

        return token_ids, token_byte_positions

    def encode(self, prompt):
        _token_trie = ByteTrie(self.byte_tokens, np.arange(len(self.byte_tokens)))
        _token_trie.match = True
        _token_trie.match_version = 0
        token_ids, token_byte_positions =  self._tokenize_prefix(prompt, _token_trie)
        return token_ids

    def decode(self, token_ids):
        sentences = [self.tkz.convert_tokens_to_string(['a', self.tkz.convert_ids_to_tokens(int(token_ids[i]))]) for i in
                  range(len(token_ids))]
        return sentences



