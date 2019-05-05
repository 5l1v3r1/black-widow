"""
Metodi e classi utili alla gestione di file e cartelle
"""

from app.env import DEBUG
from app.utils.helpers.logger import Log
import os, shutil, re

# @return true se il file contiene la stringa find
def file_contains(find, file):
    if (DEBUG): Log.info('CALLED: file_contains('+find+', '+file+')')
    if (not os.path.isfile(file)):
        return False
    with open(file) as f:
        s = f.read()
        return find in s
    return False

# @return string il contenuto del file
def read_file(file):
    if (DEBUG): Log.info('CALLED: read_file('+file+')')
    if (not os.path.isfile(file)):
        return ""
    with open(file) as f:
        content = f.read()
        if (type(content) != str):
            content = str(content.decode('utf-8'))
        return content.rstrip('\n')
    return ""


# @return true se il file contiene l'espressione regolare regex
def file_contains_regex(regex, file):
    if (DEBUG): Log.info('CALLED: file_contains_regex('+regex+', '+file+')')
    if (not os.path.isfile(file)):
        return False
    reg = re.compile(regex)
    f = open(file, 'r')
    text = f.read()
    f.close()
    matches = re.findall(reg, text)
    return len(matches) > 0


# Esegue il replace della stringa che trova, con la stringa replacer
# @param find la stringa da trovare
# @param replacer la stringa che andra' a sostituire la stringa trovata
# @param file il file in cui sovrascrivere find con replacer
# @return True se trova una stringa find, False altrimenti
def replace_in_file(find, replacer, file):
    if (DEBUG): Log.info('CALLED: replace_in_file('+find+', '+replacer+', '+file+')')
    if (find == replacer): return False
    if (not file_contains(find, file)): return False
    # Safely write the changed content, if found in the file
    with open(file, 'r') as f:
        t = f.read()
    with open(file, 'w') as f:
        s = t.replace(find, replacer)
        f.write(s)
    return  True


# Esegue il replace della regex che trova, con la stringa replacer
# @param regex l'espressione regolare da trovare
# @param replacer la stringa che andra' a sostituire la regex trovata
# @param file il file in cui sovrascrivere regex con replacer
# @return True se trova una regex equivalente ad una stringa diversa da
#         replacer, False altrimenti
def replace_in_file_regex(regex, replacer, file):
    if (DEBUG): Log.info('CALLED: replace_in_file_regex('+regex+', '+replacer+', '+file+')')
    if (not os.path.isfile(file)):
        with open(file, 'a') as f:
            f.close()
    with open(file, 'r') as f:
        content = f.read()
    content_new = re.sub(regex, replacer, content, flags = re.M)
    if (content != content_new):
        overwrite_file(content_new, file)
        return True
    return False

# Sovrascrive il contenuto del file con content
def overwrite_file(content, file):
    if (DEBUG): Log.info('CALLED: overwrite_file('+content+', '+file+')')
    with open(file, 'w') as f:
        f.write(str(content)+'\n')
        f.close()

# Appende content nel file
def append_in_file(content, file):
    with open(file, 'a') as f:
        f.write(str(content)+'\n')
        f.close()

# Se la cartella folder non esiste, la crea
def check_folder(folder):
    if (not os.path.isdir(folder)):
        os.makedirs(folder)

# Elimina tutti i files presenti nella cartella passata per argomento
def clean_folder(folder):
    if (DEBUG): Log.info('CALLED: clean_folder('+folder+')')
    if (os.path.isdir(folder)):
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if (file_path != folder):
                delete(file_path)
        return True
    return False

# Copia il file o la cartella "src", in "dest"
def copy(src, dest):
    if (DEBUG): Log.info('CALLED: copy('+src+', '+dest+')')
    dest_parent = os.path.dirname(dest)
    check_folder(dest_parent)
    if (os.path.exists(dest)):
        delete(dest)
    if (os.path.isdir(src)):
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)

# Muove il file o la cartella "src", in "dest"
def move(src, dest):
    if (DEBUG): Log.info('CALLED: move('+src+', '+dest+')')
    dest_parent = os.path.dirname(dest)
    check_folder(dest_parent)
    if (os.path.exists(dest)):
        delete(dest)
    shutil.move(src, dest)

# Elimina il file o la cartella passato per argomento
def delete(file):
    while (os.path.exists(file)):
        try:
            if os.path.isfile(file):
                os.remove(file)
                return True
            elif os.path.islink(file):
                os.unlink(file)
                return True
            elif os.path.isdir(file):
                shutil.rmtree(file)
                return True
        except:
            time.sleep(0.5)
    return False