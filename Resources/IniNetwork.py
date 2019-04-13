

import os

import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from collections import Counter
from langdetect import detect

from Resources import Summarizer
import summarizer_data_utils
import summarizer_model_utils



# load csv file using pandas.
file_path = './github_issues.csv'
data = pd.read_csv(file_path, encoding='utf-8')
data.shape()

# to make the transition from the amazon review example to this one as comfortable as possbile,
# we rename the columns.
data.rename(index = str, columns = {'issue_title':'Summary', 'body':'Text'}, inplace = True)

# let's see how long the texts and summaries are.
len_summaries = [len(summary) for i, summary in enumerate(data.Summary)]
len_texts = [len(text) for text in data.Text]
Counter(len_summaries).most_common(), Counter(len_texts).most_common()

# as I said before we can not use all of the training examples.
# to make training easier we will only use shorter texts (and summaries) of similar length.
indices = [ind for ind, text in enumerate(data.Text) if 100 < len(text) < 108]
raw_summaries = data.Summary[indices]
raw_texts = data.Text[indices]


# unfortunately the issues are in different languages.
# to make learning easier to the model we will only use english ones.
# for that we use langdetect.
# with sufficient resources that might not be a problem,
# but for our purposes it will be better.
en_raw_summaries=[]
en_raw_texts=[]

for (s,t) in zip(raw_summaries, raw_texts):
    try:
        lang = detect(t)
        if lang == 'en':
            en_raw_summaries.append(s)
            en_raw_texts.append(t)
    except:
        continue


for t, s in zip(en_raw_texts[:5], en_raw_summaries[:5]):
    print('Text:\n', t,)
    print('Summary:\n', s, '\n\n')



# preprocess the texts and summaries.
# we have the option to keep_most or not. in this case we do not want 'to keep most', i.e. we will only keep
# letters and numbers.
# (to improve the model, this preprocessing step should be refined)
processed_texts, processed_summaries, words_counted = summarizer_data_utils.preprocess_texts_and_summaries(
    en_raw_texts[:20000],
    en_raw_summaries[:20000],
    keep_most=False)



# create lookup dicts.
# most oft the words only appear only once.
# min_occureces set to 2 reduces our vocabulary by more than half.
specials = ["<EOS>", "<SOS>","<PAD>","<UNK>"]
word2ind, ind2word,  missing_words = summarizer_data_utils.create_word_inds_dicts(words_counted,
                                                                                  specials = specials,
                                                                                  min_occurences=2)
print(len(word2ind), len(ind2word), len(missing_words))

# the embeddings from tf.hub.
embed = hub.Module("https://tfhub.dev/google/Wiki-words-250/1")
emb = embed([key for key in word2ind.keys()])

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    sess.run(tf.tables_initializer())
    embedding = sess.run(emb)

embedding.shape()
np.save('./embeddings/my_embedding_github.npy', embedding)



# converts words in texts and summaries to indices
converted_texts, unknown_words_in_texts = summarizer_data_utils.convert_to_inds(processed_texts,
                                                                                word2ind,
                                                                                eos = False)


converted_summaries, unknown_words_in_summaries = summarizer_data_utils.convert_to_inds(processed_summaries,
                                                                                        word2ind,
                                                                                        eos = True,
                                                                                        sos = True)



# seems to have worked well.
for t, s in zip(converted_texts[:5], converted_summaries[:5]):
    print(summarizer_data_utils.convert_inds_to_text(t, ind2word),
          summarizer_data_utils.convert_inds_to_text(s, ind2word))
    print('\n\n')

# model hyperparameters
num_layers_encoder = 2
num_layers_decoder = 2
rnn_size_encoder = 500
rnn_size_decoder = 500

batch_size = 256
epochs = 200
clip = 5
keep_probability = 0.8
learning_rate = 0.0005
max_lr=0.005
learning_rate_decay_steps = 500
learning_rate_decay = 0.90


pretrained_embeddings_path = './embeddings/my_embedding_github.npy'
summary_dir = os.path.join('./tensorboard/github_issues')


use_cyclic_lr = True
inference_targets=True


# build graph and train the model
summarizer_model_utils.reset_graph()
summarizer = Summarizer.Summarizer(word2ind,
                                   ind2word,
                                   save_path='./models/github_issues/my_model',
                                   mode='TRAIN',
                                   num_layers_encoder = num_layers_encoder,
                                   num_layers_decoder = num_layers_decoder,
                                   rnn_size_encoder = rnn_size_encoder,
                                   rnn_size_decoder = rnn_size_decoder,
                                   batch_size = batch_size,
                                   clip = clip,
                                   keep_probability = keep_probability,
                                   learning_rate = learning_rate,
                                   max_lr=max_lr,
                                   learning_rate_decay_steps = learning_rate_decay_steps,
                                   learning_rate_decay = learning_rate_decay,
                                   epochs = epochs,
                                   pretrained_embeddings_path = pretrained_embeddings_path,
                                   use_cyclic_lr = use_cyclic_lr, )
#                                    summary_dir = summary_dir)

summarizer.build_graph()
summarizer.train(converted_texts[:18000],
                 converted_summaries[:18000],
                 validation_inputs=converted_texts[18000:],
                 validation_targets=converted_summaries[18000:])

# hidden training output.
# both train and validation loss decrease nicely



summarizer_model_utils.reset_graph()
summarizer = Summarizer.Summarizer(word2ind,
                                   ind2word,
                                   './models/github_issues/my_model',
                                   'INFER',
                                   num_layers_encoder = num_layers_encoder,
                                   num_layers_decoder = num_layers_decoder,
                                   batch_size = len(converted_texts[:50]),
                                   clip = clip,
                                   keep_probability = 1.0,
                                   learning_rate = 0.0,
                                   beam_width = 5,
                                   rnn_size_encoder = rnn_size_encoder,
                                   rnn_size_decoder = rnn_size_decoder,
                                   inference_targets = True,
                                   pretrained_embeddings_path = pretrained_embeddings_path)

summarizer.build_graph()
preds = summarizer.infer(converted_texts[:50],
                         restore_path =  './models/github_issues/my_model',
                         targets = converted_summaries[:50])