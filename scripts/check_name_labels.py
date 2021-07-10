import os
import xml.etree.ElementTree as ET
import sys
import re

ARCO = "Arco di Trionfo"
BERLINA = "Berlina Mosca"
CASA_ROSSINI = "Casa Rossini"
CATTEDRALE = "Cattedrale Santa Maria Assunta"
CENTRO_ARTI_VISIVE = "Centro Arti Visive Pescheria"
CHIESA_SAN_AGOSTINO = "Chiesa San Agostino"
FONTANA = "Fontana Piazza del Popolo"
PALAZZO_BAVIERA = "Palazzo Baviera"
PALAZZO_COMUNALE = "Palazzo Comunale"
PALAZZO_DUCALE = "Palazzo Ducale"
PALAZZO_OLIVIERI = "Palazzo Olivieri"
PALLA = "Palla di Pomodoro"
SEDE_POSTE = "Palazzo delle Poste"
PARROCCHIA_SANTA_MARIA = "Parrocchia Santa Maria"
PORTALE_SAN_DOMENICO = "Portale San Domenico"
ROCCA_COSTANZA = "Rocca Costanza"
SCULTURA_MEMORIA = "Scultura della Memoria"
SCULTURA_GARIBALDI = "Giuseppe Garibaldi"
SCULTURA_ROSSINI = "Gioachino Rossini"
SCULTURA_PERTICARI = "Giulio Perticari"
TEATRO_ROSSINI = "Teatro Rossini"
TEATRO_SPERIMENTALE = "Teatro Sperimentale"
VILLA_CAPRILE = "Villa Caprile"
VILLINO_RUGGERI = "Villino Ruggeri"

LABELS = [ARCO, BERLINA, CASA_ROSSINI, CATTEDRALE, CENTRO_ARTI_VISIVE, CHIESA_SAN_AGOSTINO, FONTANA, PALAZZO_BAVIERA,
          PALAZZO_COMUNALE, PALAZZO_DUCALE, PALAZZO_OLIVIERI, PALLA, SEDE_POSTE, PARROCCHIA_SANTA_MARIA,
          PORTALE_SAN_DOMENICO, ROCCA_COSTANZA, SCULTURA_MEMORIA, SCULTURA_GARIBALDI, SCULTURA_ROSSINI,
          SCULTURA_PERTICARI, TEATRO_ROSSINI, TEATRO_SPERIMENTALE, VILLA_CAPRILE, VILLINO_RUGGERI]

INPUT_PATH = "Dataset/"


def split_title(title):
    r"""
    Split text of the directory
    :param title: text to split
    :return: text with the tabulations
    """
    title = title[0].upper() + title[1:]
    folder = re.findall('[A-Z][^A-Z]*', title)
    result = ""
    for i, item in enumerate(folder):
        result += str(item) + (" " if (i + 1) != len(folder) else "")

    return result


def check_labels_on_more_objects():
    r"""
    Check if the label of the object is correct.
    """
    i = 7
    while True:
        try:
            labels_name = root[i][0]
            assert labels_name in LABELS
            i += 1

        except:
            break


argv = sys.argv

if len(argv) > 1:
    INPUT_PATH = (argv[1])

for dir in os.listdir(INPUT_PATH):
    count = 0

    for xml in os.listdir(INPUT_PATH + dir + "/annotations/"):
        num_file = len(os.listdir(INPUT_PATH + dir + "/annotations/"))
        tree = ET.parse(INPUT_PATH + dir + "/annotations/" + xml)
        root = tree.getroot()

        # Folder
        tag_folder = root[0]
        tag_folder.text = split_title(dir)

        # FIle name
        tag_file_name = root[1]

        # Path
        tag_path = root[2]
        tag_path.text = INPUT_PATH + dir + "/imgs/" + tag_file_name.text

        # Database
        tag_database = root[3][0]
        tag_database.text = "Cultural Heritage Pesaro"

        # Name classes
        tag_object = root[6]
        tag_name = tag_object[0]
        name = tag_name.text

        try:
            check_tag_object = root[7]

            if check_tag_object.tag == tag_object.tag:
                # File xml has more object of different classes
                print(f"File with more object. XML: {xml}, DIR: {dir}")
                check_labels_on_more_objects()

                count += 1
                if count == num_file:
                    print(f"--> Finished check file for {dir}", end="\n\n")

                with open(INPUT_PATH + dir + "/annotations/" + xml, "wb") as f:
                    f.write(ET.tostring(root))

                continue
        except:
            pass

        try:
            if dir == "arcoDiTrionfo":
                assert name == ARCO

            elif dir == "berlinaMosca":
                assert name == BERLINA

            elif dir == "casaRossini":
                assert name == CASA_ROSSINI

            elif dir == "cattedraleSantaMariaAssunta":
                assert name == CATTEDRALE

            elif dir == "centroArtiVisive":
                assert name == CENTRO_ARTI_VISIVE

            elif dir == "chiesaSanAgostino":
                assert name == CHIESA_SAN_AGOSTINO

            elif dir == "fontanaPiazza":
                assert name == FONTANA

            elif dir == "palazzoBaviera":
                assert name == PALAZZO_BAVIERA

            elif dir == "palazzoComunale":
                assert name == PALAZZO_COMUNALE

            elif dir == "palazzoDucale":
                assert name == PALAZZO_DUCALE

            elif dir == "palazzoOlivieri":
                assert name == PALAZZO_OLIVIERI

            elif dir == "pallaDiPomodoro":
                assert name == PALLA

            elif dir == "palazzoDellePoste":
                assert name == SEDE_POSTE

            elif dir == "parrocchiaSantaMaria":
                assert name == PARROCCHIA_SANTA_MARIA

            elif dir == "portaleSanDomenico":
                assert name == PORTALE_SAN_DOMENICO

            elif dir == "roccaCostanza":
                assert name == ROCCA_COSTANZA

            elif dir == "sculturaDellaMemoria":
                assert name == SCULTURA_MEMORIA

            elif dir == "statuaGioachinoRossini":
                assert name == SCULTURA_ROSSINI

            elif dir == "statuaGiulioPerticari":
                assert name == SCULTURA_PERTICARI

            elif dir == "statuaGiuseppeGaribaldi":
                assert name == SCULTURA_GARIBALDI

            elif dir == "teatroRossini":
                assert name == TEATRO_ROSSINI

            elif dir == "teatroSperimentale":
                assert name == TEATRO_SPERIMENTALE

            elif dir == "villaCaprile":
                assert name == VILLA_CAPRILE

            elif dir == "villinoRuggeri":
                assert name == VILLINO_RUGGERI

            else:
                raise Exception(f"Error: tag NAME: {name}, DIR:{dir}, FILE:{xml}")

        except Exception as e:
            raise Exception(Exception(f"Error: tag NAME: {name}, DIR:{dir}, FILE:{xml}"))

        # Save changes
        with open(INPUT_PATH + dir + "/annotations/" + xml, "wb") as f:
            f.write(ET.tostring(root))

        count += 1
        if count == num_file:
            print(f"--> Finished check file for {dir}", end="\n\n")

print("Finished check all files!")
