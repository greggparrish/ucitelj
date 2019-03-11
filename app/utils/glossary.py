import os
from time import time
import json

from app import app


def format_glossary(a_id, glossary):
    json_gloss = {'article_id': a_id,
                  'timestamp': int(time()),
                  'paragraphs': glossary
                  }
    return json_gloss


def write_json_glossary(article_id, glossary):
    jg = format_glossary(article_id, glossary)
    g_dir = os.path.join(app.root_path, 'static/public/glossaries/')
    fn = '{}{}.json'.format(g_dir, article_id)
    with open(fn, 'w') as f:
        json.dump(jg, f)
    return jg
