"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import fileinput
import string
from glob import glob

import pandas as pd  # type: ignore


def load_data(input_directory):
    """Funcion load_input"""
    sequence = []

    files = glob(f"{input_directory}/*")

    with fileinput.input(files=files) as f:
        for i, line in enumerate(f):
            # Skip header
            if i < 4:
                continue
            sequence.append((fileinput.filename(), line))

    return sequence


def line_preprocessing(sequence):
    """Line Preprocessing"""

    translation_table = str.maketrans(
        "",
        "",
        string.punctuation.replace(",", "")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace("/", ""),
    )

    sequence = [
        (
            k,
            v.translate(translation_table).lower().strip().split(),
        )
        for k, v in sequence
    ]
    return sequence


def convert_pandas(sequence):
    """Iterates over sequence of words and creates registries"""

    df = []

    registry = {
        "cluster": 0,
        "cantidad_de_palabras_clave": 0,
        "porcentaje_de_palabras_clave": 0,
        "principales_palabras_clave": [],
    }

    for _, v in sequence:
        if len(v) == 0:
            df.append(registry)

            registry = {
                "cluster": 0,
                "cantidad_de_palabras_clave": 0,
                "porcentaje_de_palabras_clave": 0,
                "principales_palabras_clave": [],
            }

            continue

        if v[0].isdigit():
            registry["cluster"] = int(v[0])
            registry["cantidad_de_palabras_clave"] = int(v[1])
            registry["porcentaje_de_palabras_clave"] = float(v[2].replace(",", "."))
            registry["principales_palabras_clave"].extend(v[3:])

        else:
            registry["principales_palabras_clave"].extend(v)

    for registry in df:
        sentences = []
        sentence = []

        for word in registry["principales_palabras_clave"]:
            sentence.append(word)

            if "," in word:
                sentences.append(" ".join(sentence) + " ")
                sentence = []

        if sentence:
            sentences.append(" ".join(sentence))

        registry["principales_palabras_clave"] = "".join(sentences)

    return pd.DataFrame(df)


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
            espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
            espacio entre palabra y palabra.


    """

    seq = load_data("files/input")
    seq = line_preprocessing(seq)
    df = convert_pandas(seq)

    return df


df = pregunta_01()
