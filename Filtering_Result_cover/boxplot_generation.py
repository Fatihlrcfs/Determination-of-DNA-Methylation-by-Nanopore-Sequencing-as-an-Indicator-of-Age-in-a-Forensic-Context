#promising area boxplot generation with extending end#

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Veri dosyalarını yukle
veriler_df = pd.read_csv('lncRNAs_methylation_5sample.csv')
koordinatlar_df = pd.read_csv('lncRNAs.tsv', sep='\t')

# Genisletilmis koordinatlar icin sutunları hazırla
koordinatlar_df['expanded_start'] = koordinatlar_df['start'] - 1
koordinatlar_df['expanded_end'] = koordinatlar_df['end'] + 1

# Her bir genisletilmis koordinat icin boxplot ve nokta daglım grafiÄŸi ciz
for index, koordinat in koordinatlar_df.iterrows():
    chr = koordinat['chr']
    start = koordinat['expanded_start']
    end = koordinat['expanded_end']
    
    # Filtreleme
    plot_data = veriler_df[(veriler_df['Pos_start'] >= start) & 
                           (veriler_df['Pos_end'] <= end) & 
                           (veriler_df['Chr'] == chr)]
    
    # Grafik cizimi
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=plot_data, x='Yas', y='Methylation', palette="Set3")
    sns.stripplot(data=plot_data, x='Yas', y='Methylation', color='black', size=5, jitter=True, alpha=0.6)
    
    # Baslıklar ve etiketler
    plt.title(f'Chr {chr} Expanded Coordinates: {start}-{end} Methylation Levels')
    plt.xlabel('Age')
    plt.ylabel('Methylation')
    
    # Grafik dosyası olarak kaydet
    grafik_dosyasi = f'boxplot_chr{chr}_{start}_{end}.png'
    plt.savefig(grafik_dosyasi)
    plt.close()

# islemin tamamlandıgını bildir
print("Boxplotlar ve nokta daglım grafikleri cizildi ve kaydedildi.")

