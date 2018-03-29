import os
import sys
import time
import logging
from preprocess import get_trimmed_glove_vectors, load_vocab, \
        get_processing_word

class Config():
    def __init__(self, load=True):
        # directory for training outputs
        if not os.path.exists(self.dir_output):
            os.makedirs(self.dir_output)

        # create instance of logger
        self.logger = getLogger(self.path_log)

        # load if requested (default)
        if load:
            self.load()

    def load(self):
        # 1. vocabulary
        self.vocab_words = load_vocab(self.filename_words)
        self.vocab_tags = load_vocab(self.filename_tags)
        self.vocab_chars = load_vocab(self.filename_chars)

        self.nwords = len(self.vocab_words)
        self.nchars = len(self.vocab_chars)
        self.ntags = len(self.vocab_tags)

        # 2. get processing functions that map str -> id
        self.processing_word = get_processing_word(self.vocab_words,
                                                   self.vocab_chars, lowercase=True, chars=self.use_chars)
        self.processing_tag = get_processing_word(self.vocab_tags,
                                                  lowercase=False, allow_unk=False)

        # 3. get pre-trained embeddings
        self.embeddings = (get_trimmed_glove_vectors(self.filename_trimmed)
                           if self.use_pretrained else None)


        # general config

    dir_output = "results/test/"
    dir_model = dir_output + "model.weights/"
    path_log = dir_output + "log.txt"

    # embeddings
    dim_word = 300
    dim_char = 100

    # glove files
    filename_glove = "../glove.6B/glove.6B.{}d.txt".format(dim_word)
    # trimmed embeddings (created from glove_filename with build_data.py)
    filename_trimmed = "../glove.6B.{}d.trimmed.npz".format(dim_word)
    use_pretrained = True

    # dataset
    filename_dev = "CoNLL2003/eng/eng.testa.iob"
    filename_test = "CoNLL2003/eng/eng.testb.iob"
    filename_train = "CoNLL2003/eng/eng.train.iob"

    # filename_dev = filename_test = filename_train = "data/test.txt" # test

    max_iter = None  # if not None, max number of examples in Dataset

    # vocab (created from dataset with build_data.py)
    filename_words = "words.txt"
    filename_tags = "tags.txt"
    filename_chars = "chars.txt"

    # training
    train_embeddings = False
    nepochs = 15
    dropout = 0.5
    batch_size = 20
    lr_method = "adam"
    lr = 0.001
    lr_decay = 0.9
    clip = -1  # if negative, no clipping
    nepoch_no_imprv = 3

    # model hyperparameters
    hidden_size_char = 100  # lstm on chars
    hidden_size_lstm = 300  # lstm on word embeddings

    # NOTE: if both chars and crf, only 1.6x slower on GPU
    use_crf = True  # if crf, training is 1.7x slower on CPU
    use_chars = True  # if char embedding, training is 3.5x slower on CPU

def getLogger(filename):
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(
            '%(asctime)s:%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(handler)

    return logger