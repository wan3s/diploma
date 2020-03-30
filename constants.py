ARTICLES_DIR_NAME = 'articles'
COLLECTIONS_FILE_NAME = 'collections.txt'
TF_FILE_NAME = 'terms_freqs.txt'
INTERMEDIATE_RESULTS_FILE_NAME = 'intermediate_result.txt'
CACHED_LEMMS_FILE_NAME = 'cached_lemms.txt'
SINONIMS_ARCHIVE_PATH = '180.zip'

SEARCH_MODEL_TFIDF = 'tfidf'
SEARCH_MODEL_VECT = 'vect'
SEARCH_MODEL_LANG = 'lang'

PARAM_UPDATE_COLLECTIONS = '--update-collections'
PARAM_SEARCH_MODEL_ARG = '--model='

LANG_MODEL_LAMBDA = 0.9

TXT_ETENSION = '.txt'
FILE_MODE_READ = 'r'
FILE_MODE_WRITE = 'w'

SPLIT_DOCS = '.'
SPLIT_WORDS = ' '
SPLIT_ASSOC = '$$$'

STOP_SESSION_KEY_WORD = 'stop'

ALLOWED_CHARS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

MIN_WEIGHT = {
    SEARCH_MODEL_TFIDF: 0.1,
    SEARCH_MODEL_VECT: 0.1,
    SEARCH_MODEL_LANG: 1.e-75
}

NOT_FOUND_ANSWERS = [
        'Даже незнаю, что ответить',
        'Попробуйте переформулировать запрос',
        'Затрудняюсь ответить'
    ]

WORDS_LIKELIHOOD_EPS = 1.e-40