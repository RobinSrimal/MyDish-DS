from keras_wrapper.dataset import Dataset, saveDataset, loadDataset

from collections import Counter
from operator import add

import nltk
import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')

'''
Logic for dataset pre-processing. With new data, change the path to that data
in ['DATA_PATH'] and adjust other configurations accordingly.
'''


def build_dataset(params):
<<<<<<< HEAD

    if params['REBUILD_DATASET']:  # new dataset instance
        if(params['VERBOSE'] > 0):
            silence = False
            logging.info('Building ' + params['DATASET_NAME'] + ' dataset')
        else:
            silence = True

        base_path = params['DATA_PATH']
        ds = Dataset(params['DATASET_NAME'], base_path +
                     params.get('SUFFIX_DATASET', '/images'), silence=silence)

        # INPUT DATA
        # IMAGES
        ds.setInput(base_path+'/'+params['IMG_FILES']['train'], 'train',
                    type='raw-image', id=params['INPUTS_IDS_DATASET'][0],
                    img_size=params['IMG_SIZE'], img_size_crop=params['IMG_SIZE_CROP'])
        ds.setInput(base_path+'/'+params['IMG_FILES']['val'], 'val',
                    type='raw-image', id=params['INPUTS_IDS_DATASET'][0],
                    img_size=params['IMG_SIZE'], img_size_crop=params['IMG_SIZE_CROP'])
        ds.setInput(base_path+'/'+params['IMG_FILES']['test'], 'test',
                    type='raw-image', id=params['INPUTS_IDS_DATASET'][0],
                    img_size=params['IMG_SIZE'], img_size_crop=params['IMG_SIZE_CROP'])
        # Set train mean
        ds.setTrainMean(
            mean_image=params['MEAN_IMAGE'], data_id=params['INPUTS_IDS_DATASET'][0])

        # OUTPUT DATA
        if params['CLASSIFICATION_TYPE'] == 'single-label':

            # train split
            ds.setOutput(base_path + '/' + params['LABELS_FILES']['train'], 'train',
=======
    '''
    Function for structuring a dataset
    '''
    if params['REBUILD_DATASET']:  # new instance of the dataset
        if (params['VERBOSE'] > 0):
            silence = False
            logging.info('Building '+params['DATASET_NAME']+' dataset')
        else:
            silence = True

        base_path = params['DATA_PATH']  # path to data
        ds = Dataset(params['DATASET_NAME'],
                     base_path+params.get('SUFFIX_DATASET', '/images'),
                     silence=silence)

        # INPUT DATA / Images
        # Configs for training dataset
        ds.setInput(base_path+'/'+params['IMG_FILES']['train'], 'train',
                    type='raw-image', id=params['INPUTS_IDS_DATASET'][0],
                    img_size=params['IMG_SIZE'],
                    img_size_crop=params['IMG_SIZE_CROP'])

        # Configs for val dataset
        ds.setInput(base_path+'/'+params['IMG_FILES']['val'], 'val',
                    type='raw-image', id=params['INPUTS_IDS_DATASET'][0],
                    img_size=params['IMG_SIZE'],
                    img_size_crop=params['IMG_SIZE_CROP'])

        # Configs for test dataset
        df.setInput(base_path+'/'+params['IMG_FILES']['test'], 'test',
                    type='raw-image', id=params['INPUTS_IDS_MODEL'][0],
                    img_size=params['IMG_SIZE'],
                    img_size_crop=params['IMG_SIZE_CROP'])

        # Set train mean # check configs for clarification
        ds.setTrainMean(mean_image=params['MEAN_IMAGE'],
                        id=params['INPUTS_IDS_DATASET'][0])

        # Output data
        if params['CLASSIFICATION_TYPE'] == 'single-label':

            # train split
            ds.setOutput(base_path+'/'+params['LABEL_FILES']['train'], 'train',
>>>>>>> bc62d6b059748b310148f7d7d7c431fb8ac19765
                         type='categorical', id=params['OUTPUTS_IDS_DATASET'][0])
            # val split
            ds.setOutput(base_path + '/' + params['LABELS_FILES']['val'], 'val',
                         type='categorical', id=params['OUTPUTS_IDS_DATASET'][0])
            # test split
            ds.setOutput(base_path + '/' + params['LABELS_FILES']['test'], 'test',
                         type='categorical', id=params['OUTPUTS_IDS_DATASET'][0])

        elif params['CLASSIFICATION_TYPE'] == 'multi-label':

            # Convert list of ingredients into classes
            logging.info(
                'Preprocessing list of ingredients for assigning vocabulary as image classes.')
            [classes, word2idx, idx2word] = convertIngredientsList2BinaryClasses(base_path,
                                                                                 params['LABELS_FILES'],
                                                                                 params['CLASSES_PATH'],
                                                                                 type_list=params.get('LABELS_TYPE_LIST', 'identifiers'))
<<<<<<< HEAD
            # Insert them as outputs
            ds.setOutput(classes['train'], 'train', type='categorical',
                         id=params['OUTPUTS_IDS_DATASET'][0])
            ds.setOutput(classes['val'], 'val', type='categorical',
                         id=params['OUTPUTS_IDS_DATASET'][0])
            ds.setOutput(classes['test'], 'test', type='categorical',
=======

            # Insert them as outputs
            ds.setOutput(classes['train'], 'train', type='binary',
                         id=params['OUTPUTS_IDS_DATASET'][0])
            ds.setOutput(classes['val'], 'val', type='binary',
                         id=params['OUTPUTS_IDS_DATASET'][0])
            ds.setOutput(classes['test'], 'test', type='binary',
>>>>>>> bc62d6b059748b310148f7d7d7c431fb8ac19765
                         id=params['OUTPUTS_IDS_DATASET'][0])

            # Insert vocabularies
            ds.extra_variables['word2idx_binary'] = word2idx
            ds.extra_variables['idx2word_binary'] = idx2word

            if 'Food_and_Ingredients' in params['DATASET_NAME']:

                # train split
                ds.setOutput(base_path + '/' + params['LABELS_FILES_FOOD']['train'], 'train',
                             type='categorical', id=params['OUTPUTS_IDS_DATASET'][1])
                # val split
                ds.setOutput(base_path + '/' + params['LABELS_FILES_FOOD']['val'], 'val',
                             type='categorical', id=params['OUTPUTS_IDS_DATASET'][1])
                # test split
                ds.setOutput(base_path + '/' + params['LABELS_FILES_FOOD']['test'], 'test',
                             type='categorical', id=params['OUTPUTS_IDS_DATASET'][1])

<<<<<<< HEAD
        # Dataset is downloaded, can be used again by storing in the defined path.
=======
        # We have finished loading the dataset, now we can store it for using it in the future
>>>>>>> bc62d6b059748b310148f7d7d7c431fb8ac19765
        saveDataset(ds, params['STORE_PATH'])

    else:
        # We can easily recover it with a single line
        ds = loadDataset(params['STORE_PATH'] +
                         '/Dataset_'+params['DATASET_NAME']+'.pkl')

    return ds


def convertIngredientsList2BinaryClasses(base_path, data, multilabels, type_list='identifiers'):

    repeat_imgs = 1

    ing_list = []
    counter = Counter()
    with open(base_path+'/'+multilabels) as f:
        for pos_ing, line in enumerate(f):
            # read ingredients
            if type_list == 'identifiers':
                ing = line.rstrip('\n').split(',')
                ing = map(lambda x: x.lower(), ing)
                ing_list.append(ing)
            elif type_list == 'words':
                ing = line.rstrip('\n')
                ing = ing.lower()
                ing_list.append(ing)
                ing = [ing]
            counter.update(ing)

    vocab_count = counter.most_common()

    vocabulary = {}
    list_words = []
    for i, (word, count) in enumerate(vocab_count):
        vocabulary[word] = i
        list_words.append(word)
    len_vocab = len(vocabulary)

    # Preprocess each data split
    classes = dict()
<<<<<<< HEAD
    for set_name, file in data.items():
=======
    for set_name, file in data.iteritems():
>>>>>>> bc62d6b059748b310148f7d7d7c431fb8ac19765
        classes[set_name] = []
        with open(base_path+'/'+file) as f:
            for idx_img, line in enumerate(f):
                classes[set_name].append(np.zeros((len_vocab,)))
                if type_list == 'identifiers':
                    pos_ing = int(line.rstrip('\n'))
                    ings = ing_list[pos_ing]
                elif type_list == 'words':
                    ings = line.rstrip('\n').split(',')

                # insert all ingredients
                for w in ings:
                    if w in vocabulary.keys():
                        classes[set_name][-1][vocabulary[w]] = 1

    inv_vocabulary = {v: k for k, v in vocabulary.items()}
    return [classes, vocabulary, inv_vocabulary]
