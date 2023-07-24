import csv
import random
import nltk

# NLTK stopwords listesini indir
nltk.download('stopwords')

# Türkçe stopwords listesini al
turkish_stopwords = set(nltk.corpus.stopwords.words('turkish'))

# Kaç kez çoğaltmak istediğinizi burada belirtin
duplicate_count = 2

duplicated_rows = []  # burada listeyi tanımlayın

with open('adim10.csv', 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)

    # Sütun başlıklarını al
    headers = reader.fieldnames

    # İlk verileri yazdır
    with open('step11.csv', 'w', newline='', encoding='utf-8') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=headers)
        writer.writeheader()
        for row in reader:
            for header in headers:
                row[header] = row[header].lower().encode('utf-8').decode('utf-8')
                # Stopwords'leri çıkar
                row[header] = ' '.join([word for word in row[header].split() if word not in turkish_stopwords])
            writer.writerow(row)

            for i in range(duplicate_count):
                # Çoğaltılmış satırı oluştur
                duplicated_row = {}
                for header in headers:
                    if header == 'Description':
                        duplicated_row[header] = row[header]
                    elif header == 'Title':
                        duplicated_row[header] = row[header]
                    else:
                        if row[header]:
                            duplicated_row[header] = row[header]
                        else:
                            duplicated_row[header] = ''

                duplicated_rows.append(duplicated_row)

        # Kopyalanan satırları rastgele karıştır
        random.shuffle(duplicated_rows)

        # Rastgele karıştırılmış satırları dosyaya yazdır
        with open('step11.csv', 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            for row in duplicated_rows:
                for header in headers:
                    row[header] = row[header].lower().encode('utf-8').decode('utf-8')
                    # Stopwords'leri çıkar
                    row[header] = ' '.join([word for word in row[header].split() if word not in turkish_stopwords])
                writer.writerow(row)
