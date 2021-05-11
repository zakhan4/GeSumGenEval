from nltk.stem import *
from nltk import ngrams as ngram_splitter
import data.ngram_probs as ngram_probs
import re
import string
import os
import six
from somajo import SoMaJo


class GeRouge:
    """
    Class that computes ROUGE scores on German texts.

    Args:
        alpha: Weighting factor of Recall and Precision.
        stemming: Boolean. Defines whether stemming is used or not.
        split_compounds: Boolean. Defines whether compound words are split or not.
        use_pos: Boolean. Defines whether only certain POS-tags are used to calculate ROUGE
        minimal_mode: Boolean. Skip time consuming steps for quick calculation
    """
	
    def __init__(self, alpha = 0.5, stemming = True, split_compounds = True, minimal_mode = False):
        self.tokenizer = SoMaJo("de_CMC", split_camel_case = True, split_sentences=True)
        self.alpha = alpha
        self.stemming = stemming
        self.split_compounds = split_compounds
        self.stemmer = SnowballStemmer('german')
        self.minimal_mode = minimal_mode
        self.metrics = ["rouge-1", "rouge-2", "rouge-l"]
        self.stats = ["r", "p", "f"]
        self.AVAILABLE_METRICS = {
        "rouge-1": lambda hyp, ref: self.rouge_n(hyp, ref, 1),
        "rouge-2": lambda hyp, ref: self.rouge_n(hyp, ref, 2),
        "rouge-3": lambda hyp, ref: self.rouge_n(hyp, ref, 3),
        "rouge-4": lambda hyp, ref: self.rouge_n(hyp, ref, 4),
        "rouge-5": lambda hyp, ref: self.rouge_n(hyp, ref, 5),
        "rouge-l": lambda hyp, ref: self.rouge_l(hyp, ref),
    }

        self.remove_chars = ['²', '³', '“', '„', ',', '†', '‚', '‘', '–']
        self.remove_chars.extend(list(string.punctuation))
        self.replace_chars = [('ss', 'ß'), ('ä', 'ae'), ('ü', 'ue'), ('ö', 'oe')]
		

        self.stop = set()
        with open('data/GermanST_utf8.txt', 'r', encoding = 'utf-8') as f:
            for line in f:
                self.stop.add(line.strip())
        if not minimal_mode:
          self.smart_stop = set()
          with open('data/smart_stop.txt', 'r', encoding = 'cp1252') as f:
              for line in f:
                  word = line.strip().lower()
                  self.smart_stop.add(word)
                  for replace_char in self.replace_chars:
                      word = word.replace(replace_char[0], replace_char[1])
          self.lemmas = {}
          with open('data/baseforms_by_projekt_deutscher_wortschatz.txt', 'r', encoding = 'cp1252') as f:
              for line in f:
                  l = line.strip().split('\t')
                  l[0] = l[0].strip().lower()
                  l[1] = l[1].strip().lower()
                  for replace_char in self.replace_chars:
                      l[0] = l[0].replace(replace_char[0], replace_char[1])
                      l[1] = l[1].replace(replace_char[0], replace_char[1])
                  self.lemmas[l[0]] = l[1]

    def tokenize_sents(self, text):
        sents = self.tokenizer.tokenize_text([text])
        transformed_sents = [list(self.transform_sent(sent)) for sent in sents]
        transformed_sents = [[token for token in sent if token is not None and token != ''] for sent in transformed_sents]

        return transformed_sents

    def create_ngrams(self, transformed_sents, n = 1):
        ngrams_sents = [ngram_splitter(sent, n) for sent in transformed_sents if len(sent) >= n]
        ngrams = set([token for sent in ngrams_sents for token in sent])

        return ngrams

    def transform_sent(self, sent):
        for token in sent:
            token, splitted = self.transform_token(token.text, 'X')
            if splitted:
                for partial_token in token:
                    yield partial_token
            else:
                yield token

    def transform_token(self, token, pos):
        if not self.minimal_mode and token.lower().strip() in self.lemmas:
            token = self.lemmas[token.lower().strip()]

        compound_candidates = self.split_compound(token)
        if self.split_compounds and compound_candidates is not None and compound_candidates[0][0] > 0.5 and compound_candidates[0][1] != token:
            return_tokens = []
            for token in compound_candidates[0][1:]:
                if len(token) > 0:
                    tokens, splitted = self.transform_token(token, 'inner')
                    if splitted:
                        return_tokens.extend(tokens)
                    else:
                        return_tokens.append(tokens)
            return return_tokens, True
        else:
            token = token.lower().strip()

            for remove_char in self.remove_chars:
                token = token.replace(remove_char, '')
            for replace_char in self.replace_chars:
                token = token.replace(replace_char[0], replace_char[1])

            if (token in self.stop or
                    (not self.minimal_mode and token in self.smart_stop) or
                    bool(re.search(r'\d', token))):
                token = ''
            elif self.stemming:
                if not self.minimal_mode and token in self.lemmas:
                    token = self.lemmas[token]
                token = self.stemmer.stem(token)

            return token, False

    def rouge_n(self, summary, reference, n):
        reference_tokenized = self.tokenize_sents(reference)
        summary_tokenized = self.tokenize_sents(summary)
        return self.rouge_n_partial(reference_tokenized, summary_tokenized, n)

    def rouge_l(self, summary, reference):
        reference_tokenized = self.tokenize_sents(reference)
        summary_tokenized = self.tokenize_sents(summary)
        return self.computeL(summary_tokenized, reference_tokenized)

    def rouge_n_partial(self, reference_tokenized, summary_tokenized, n):
        if n < 1:
            return {"f": 0, "p": 0, "r": 0}
				
        reference = self.create_ngrams(reference_tokenized, n = n)
        summary = self.create_ngrams(summary_tokenized, n = n)
		
        if len(reference) == 0 or len(summary) == 0:
            return {"f": 0, "p": 0, "r": 0}

        matches = sum([sum([ngram_reference == ngram_summary for ngram_summary in summary]) for ngram_reference in reference])
        rouge_p = matches / len(summary)
        rouge_r = matches / len(reference)
        denominator = ((rouge_r * self.alpha) + (rouge_p * (1 - self.alpha)))
        if denominator != 0:
            rouge = (rouge_p * rouge_r) / denominator
        else:
            rouge = 0.0

        return {"f": rouge, "p": rouge_p, "r": rouge_r}

    def computeL(self, sys, ref):
        unionLCS = set()
        ref_size = sum([len(l) for l in ref])
        sys_size = sum([len(l) for l in sys])
        for r in ref:
            for s in sys:
                seq1 = GeRouge.lcs(r, s)
                seq2 = GeRouge.lcs(s, r)
                seq = seq1 if len(seq1) > len(seq2) else seq2
                unionLCS.update(seq)

        if ref_size > 0:
            rouge_r = len(unionLCS) / ref_size
        else:
            rouge_r = 0
        if sys_size > 0:
            rouge_p = len(unionLCS) / sys_size
        else:
            rouge_p = 0
        denominator = ((rouge_r * self.alpha) + (rouge_p * (1 - self.alpha)))
        if denominator != 0:
            rouge = (rouge_p * rouge_r) / denominator
        else:
            rouge = 0.0

        return {"f": rouge, "p": rouge_p, "r": rouge_r}

    def split_compound(self, word: str):
        """
        code adapted from: https://github.com/dtuggener/CharSplit
        Return list of possible splits, best first
        :param word: Word to be split
        :return: List of all splits
        """
        word = word.lower()

        # If there is a hyphen in the word, return part of the word behind the last hyphen
        if '-' in word:
            return [[1., '-'.join((word.split('-'))[:-1]).title(), word.split('-')[-1].title()]]

        scores = []  # Score for each possible split position
        # Iterate through characters, start at forth character, go to 3rd last
        for n in range(3, len(word) - 2):

            pre_slice = word[:n]

            # Cut of Fugen-S
            if pre_slice.endswith('ts') or pre_slice.endswith('gs') or pre_slice.endswith('ks') \
                    or pre_slice.endswith('hls') or pre_slice.endswith('ns'):
                if len(word[:n - 1]) > 2: pre_slice = word[:n - 1]

            # Start, in, and end probabilities
            pre_slice_prob = []
            in_slice_prob = []
            start_slice_prob = []

            # Extract all ngrams
            for k in range(len(word) + 1, 2, -1):

                # Probability of first compound, given by its ending prob
                if pre_slice_prob == [] and k <= len(pre_slice):
                    end_ngram = pre_slice[-k:]  # Look backwards
                    pre_slice_prob.append(ngram_probs.suffix.get(end_ngram, -1))  # Punish unlikely pre_slice end_ngram

                # Probability of ngram in word, if high, split unlikely
                in_ngram = word[n:n + k]
                in_slice_prob.append(ngram_probs.infix.get(in_ngram, 1))  # Favor ngrams not occurring within words

                # Probability of word starting
                if start_slice_prob == []:
                    ngram = word[n:n + k]
                    # Cut Fugen-S
                    if ngram.endswith('ts') or ngram.endswith('gs') or ngram.endswith('ks') \
                            or ngram.endswith('hls') or ngram.endswith('ns'):
                        if len(ngram[:-1]) > 2:
                            ngram = ngram[:-1]
                    start_slice_prob.append(ngram_probs.prefix.get(ngram, -1))

            if pre_slice_prob == [] or start_slice_prob == []: continue

            start_slice_prob = max(start_slice_prob)
            pre_slice_prob = max(pre_slice_prob)  # Highest, best preslice
            in_slice_prob = min(in_slice_prob)  # Lowest, punish splitting of good ingrams
            score = start_slice_prob - in_slice_prob + pre_slice_prob
            scores.append([score, word[:n].title(), word[n:].title()])

        scores.sort(reverse = True)
        if scores == []:
            scores = [[0, word.title(), word.title()]]
        return sorted(scores, reverse = True)
		
    def get_scores(self, hyps, refs, avg=False, ignore_empty=False):
        if isinstance(hyps, six.string_types):
            hyps, refs = [hyps], [refs]

        if ignore_empty:
            # Filter out hyps of 0 length
            hyps_and_refs = zip(hyps, refs)
            hyps_and_refs = [_ for _ in hyps_and_refs
                             if len(_[0]) > 0
                             and len(_[1]) > 0]
            
            hyps, refs = zip(*hyps_and_refs)

        assert(isinstance(hyps, type(refs)))
        assert(len(hyps) == len(refs))

        if not avg:
            return self._get_scores(hyps, refs)
        return self._get_avg_scores(hyps, refs)

    def _get_scores(self, hyps, refs):
        scores = []
        for hyp, ref in zip(hyps, refs):
            sen_score = {}

            for m in self.metrics:
                fn = self.AVAILABLE_METRICS[m]
                sc = fn(
                    hyp,
                    ref)
                sen_score[m] = {s: sc[s] for s in self.stats}

            scores.append(sen_score)
        return scores

    def _get_avg_scores(self, hyps, refs):
        scores = {m: {s: 0 for s in self.stats} for m in self.metrics}

        count = 0
        for (hyp, ref) in zip(hyps, refs):

            for m in self.metrics:
                fn = self.AVAILABLE_METRICS[m]
                sc = fn(hyp, ref)
                scores[m] = {s: scores[m][s] + sc[s] for s in self.stats}

            count += 1
        avg_scores = {
            m: {s: scores[m][s] / count for s in self.stats}
            for m in self.metrics
        }

        return avg_scores

    @staticmethod
    def lcs(a, b):
        lcsWords = []
        start = 0

        for word1 in a:
            for i in range(start, len(b)):
                word2 = b[i]
                if word1 == word2:
                    lcsWords.append(word2)
                    start = i + 1;

        return lcsWords

