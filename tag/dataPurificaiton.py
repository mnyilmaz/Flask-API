# excellde çoklu sütunları çekme

import pandas as pd

# Excel dosyasını oku
df = pd.read_excel('indexyeni.xlsx')

# 'Title', 'Category', 'Date' sütunlarını yeni bir DataFrame'e kopyala
new_df = pd.DataFrame(df[['Title', 'Description', 'Values']])

# Excel dosyasına kaydet
new_df.to_excel('indexyeni2.xlsx', index=False)

#Excel deki sütunların altındaki yazılar küçük harflere dönüştürüldü.
import pandas as pd

# Excel dosyasını yükleme
df = pd.read_excel("indexyeni.xlsx")

# "Title", "Description" ve "Values" sütunlarının isimleri
columns = ["Title", "Description", "Values"]

# Sütunlardaki tüm metinleri küçük harflere dönüştürme
for column in columns:
    df[column] = df[column].str.lower()

# Değiştirilmiş verileri Excel dosyasına kaydetme
df.to_excel("indexyeni.xlsx", index=False)


#%%
#Excellde ki Values sütunundaki yazıları rakama çeviriyor.
import pandas as pd

# Excel dosyasını oku
df = pd.read_excel('indexyeni.xlsx')

# "Values" sütununda bulunan metinleri arayarak sayılara dönüştür
df['Values'] = df['Values'].apply(lambda x: 0 if 'report a bug' in x else (1 if 'suggest a new future' in x else (2 if 'suggest improvement' in x else (3 if 'technical support' in x else x))))

# Excel dosyasına kaydet
df.to_excel('indexyeni.xlsx', index=False)

#Values sütunundaki kategorilerin (0-1-2-3) değerlerinin kaç adet barındırdığı gösterildi.
import pandas as pd

# Excel dosyasını yükleme
df = pd.read_excel("indexyeni.xlsx")

# "Values" sütunundaki her bir eşsiz değerin kaç adet tekrar ettiğini hesaplama
value_counts = df['Values'].value_counts()

# Sonucu ekrana yazdırma
print(value_counts)