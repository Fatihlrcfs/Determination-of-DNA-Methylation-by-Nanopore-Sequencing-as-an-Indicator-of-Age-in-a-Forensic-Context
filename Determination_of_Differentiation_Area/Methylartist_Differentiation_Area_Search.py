#differentiation_area_search#

import re

def read_compare_file(file_path):
    # compare.txt dosyasini okuyarak verileri bir liste olarak donduren fonksiyon
    data = []
    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            chr, start, end = line.strip().split('\t')
            data.append((chr, int(start), int(end)))
    return data

def read_example_file(file_path, example_name):
    # ornek.tsv dosyasini okuyarak verileri bir liste olarak donduren fonksiyon
    data = []
    with open(file_path, 'r') as file:
        header = file.readline().strip().split('\t')
        pattern = f"Methylation_{example_name}"
        methylation_idx = [i for i, header_item in enumerate(header) if re.search(pattern, header_item)]
        for line in file:
            items = line.strip().split('\t')
            if len(methylation_idx) > 0:
                chr, pos_start, pos_end = items[:3]
                strand = items[-1]  # Son elemani alarak strand bilgisini aliyoruz
                methylation = items[methylation_idx[0]]  # Sadece ilgili metilasyon degerini aliyoruz
                data.append((chr, int(pos_start), int(pos_end), float(methylation), strand))
    return data

def calculate_average_methylation(fragment, example_data):
    # Belirtilen fragmentteki (Chr, Start, End) ornek.tsv verilerine gore metilasyon ortalama ve nokta sayisi hesaplama
    total_methylation = 0
    num_points = 0
    for data in example_data:
        chr, pos_start, pos_end, methylation, strand = data
        if chr == fragment[0] and (pos_start >= fragment[1] or pos_end >= fragment[1]) and (pos_start <= fragment[2] or pos_end <= fragment[2]):
            total_methylation += methylation
            num_points += 1
    
    if num_points > 0:
        average_methylation = total_methylation / num_points
    else:
        average_methylation = 0
    
    return num_points, average_methylation

def main():
    compare_file_path = 'compare.txt'
    output_file_path = 'output.txt'  # Bu satirda output dosyasinin adini tanimliyoruz

    # compare.txt dosyasini okuyarak verileri aliyoruz
    compare_data = read_compare_file(compare_file_path)

    example_files = sorted(['age21bc15_method_differentiate.tsv',
                            'age24bc09_method_differentiate.tsv',
                            'age26bc18_method_differentiate.tsv',
                            'age27bc05_method_differentiate.tsv',
                            'age29bc07_method_differentiate.tsv',
                            'age31bc16_method_differentiate.tsv',
                            'age31single_method_differentiate.tsv',
                            'age33bc21_method_differentiate.tsv',
                            'age35bc22_method_differentiate.tsv',
                            'age38bc13_method_differentiate.tsv',
                            'age39single_method_differentiate.tsv',
                            'age43bc10_method_differentiate.tsv',
                            'age43single_method_differentiate.tsv',
                            'age45bc14_method_differentiate.tsv',
                            'age48single_method_differentiate.tsv',
                            'age53bc19_method_differentiate.tsv',
                            'age54bc17_method_differentiate.tsv',
                            'age56bc10_method_differentiate.tsv',
                            'age58bc11_method_differentiate.tsv',
                            'age61single_method_differentiate.tsv',
                            'age63bc20_method_differentiate.tsv',
                            'age76bc08_method_differentiate.tsv',
                            'age77bc06_method_differentiate.tsv',
                           ])

    # Her bir ornek.tsv dosyasini analiz edip sonuclari birlestirme
    with open(output_file_path, 'w') as outfile:
        outfile.write("Chr\tStart\tEnd\t")
        for example_file in example_files:
            outfile.write(f"{example_file}_Nucleotide_Count\t{example_file}_Methylation_Average\t")
        outfile.write("\n")

        for fragment in compare_data:
            fragment_chr, fragment_start, fragment_end = fragment
            outfile.write(f"{fragment_chr}\t{fragment_start}\t{fragment_end}\t")
            for example_file in example_files:
                example_name = re.search(r'age\d+', example_file).group(0)  # ornek ismi cikariliyor
                example_file_path = f'{example_file}'
                try:
                    example_data = read_example_file(example_file_path, example_name)
                    num_points, average_methylation = calculate_average_methylation(fragment, example_data)
                    outfile.write(f"{num_points}\t{average_methylation:.2f}\t")
                except FileNotFoundError:
                    outfile.write("\t\t")  # Dosya bulunamadiysa bosluklari yazdir
            outfile.write("\n")

if __name__ == "__main__":
    main()

