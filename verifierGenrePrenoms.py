# Auteur : Emmanuel EL SAYED-PERIN (AD78)
# Email : eelsayedperin@yvelines.fr
# Date de mise à jour : 07/11/2024
# Description : Mise à jour du script permettant de déterminer le genre (féminin, masculin, épicène) d'une liste de personnes
# dans un fichier CSV source en fonction d'une liste de prénoms de référence. Le script est capable de s'adapter
# à la position des prénoms dans des colonnes variées, en posant la question à l'utilisateur.
# Ce script détermine le genre (féminin, masculin, épicène) d'une liste de personnes dans un fichier CSV.
# Le fichier source, contenant les prénoms dans une colonne spécifique, doit être au même endroit que ce script.
# Étapes :
# 1. Entrez le nom du fichier source CSV (ex. 'source.csv').
# 2. Indiquez le numéro de la colonne contenant les prénoms (ex. 5 pour la 5e colonne).
# 3. Donnez un nom pour le fichier de résultat.
# Le résultat est généré en ajoutant une colonne "genre" dans le fichier de sortie.
# Si le prénom n'est ni féminin, ni masculin, ni épicène, il est noté "à contrôler"

import csv
import os

print("Ce script permet de déterminer si une liste de personnes est de genre féminin, masculin, ou épicène, en fonction d'un fichier CSV source avec une colonne de prénoms spécifiée.")

def find_gender(name, female_set, male_set, epicene_set):
    """Détermine si un prénom est féminin, masculin, épicène ou inconnu."""
    name_parts = name.lower().split()  # Divise le nom complet
    for part in name_parts:
        if part in epicene_set:
            return 'épicène'
        elif part in male_set:
            return 'masculin'
        elif part in female_set:
            return 'féminin'
    return 'à contrôler'

# Obtenir le chemin du répertoire du script
script_dir = os.path.dirname(__file__)

# Obtenir les noms de fichiers et les informations sur la colonne des prénoms
source_file_name = input("Entrez le nom du fichier CSV à traiter (ex. 'source.csv') : ")
source_path = os.path.join(script_dir, source_file_name)
prenom_col_index = int(input("Entrez le numéro de la colonne contenant les prénoms (commence à 1) : ")) - 1
result_file_name = input("Nom du fichier de résultat : ")

# Lecture et écriture des fichiers
try:
    with open(source_path, 'r', encoding='utf-8') as source_file, \
         open('prenoms_feminins.csv', 'r', encoding='utf-8') as female_file, \
         open('prenoms_masculins.csv', 'r', encoding='utf-8') as male_file, \
         open(f'{result_file_name}.csv', 'w', newline='', encoding='utf-8') as output_file:

        source_reader = csv.reader(source_file, delimiter=';')
        output_writer = csv.writer(output_file, delimiter=';')

        # Conversion des prénoms de référence en ensembles
        female_set = {row[0].strip().lower() for row in csv.reader(female_file, delimiter=';')}
        male_set = {row[0].strip().lower() for row in csv.reader(male_file, delimiter=';')}
        epicene_set = female_set & male_set  # Prénoms présents dans les deux ensembles
        female_set -= epicene_set  # Exclure les épicènes de chaque ensemble
        male_set -= epicene_set

        # Parcourir chaque ligne
        for idx, source_row in enumerate(source_reader):
            if idx == 0:
                output_writer.writerow(source_row + ['genre'])
                continue

            # Extraire le prénom depuis la colonne spécifiée
            source_string = source_row[prenom_col_index].strip().lower()
            genre = find_gender(source_string, female_set, male_set, epicene_set)
            output_writer.writerow(source_row + [genre])

    print("Traitement terminé, fichier créé :", result_file_name)

except FileNotFoundError as e:
    print(f"Erreur : fichier non trouvé ({e})")
except IndexError:
    print("Erreur : L'index de colonne spécifié est hors des limites du fichier CSV.")

input("Appuyez sur Entrée pour terminer.")
