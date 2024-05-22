#Pairplot_generation#
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Verilerinizi 'combined_common_results.tsv' dosyasÄ±ndan okuma
data = pd.read_csv('combined_common_results.tsv', sep='\t')

# SÃ¼tun adlarÄ±nÄ± temizleyin
data.columns = [col.strip() for col in data.columns]

# Ä°lgilendiÄŸiniz metodlarÄ±n listesini oluÅŸturun
methods = ['deepsignal', 'nanopolish', 'megalodon', 'remora']

# FigÃ¼r ve eksenleri baÅŸlatÄ±n
fig, axes = plt.subplots(len(methods), len(methods), figsize=(20, 20))

# Create a color palette with a distinct color for each method
colors = sns.color_palette('hsv', len(methods))

# Plot each pair of methods
for i, method1 in enumerate(methods):
    for j, method2 in enumerate(methods):
        ax = axes[j, i]  # Swap i and j for the correct orientation
        if i == j:  # Diagonal: Plot the KDE
            sns.kdeplot(data[method1], ax=ax, shade=True, color=colors[i])
        elif i < j:  # Upper triangle: Scatter plot
            ax.scatter(data[method1], data[method2], marker='+', color=colors[i], alpha=0.6)
            ax.scatter(data[method2], data[method1], marker='+', color=colors[j], alpha=0.6)
        else:  # Lower triangle: Scatter plot
            ax.scatter(data[method1], data[method2], marker='+', color=colors[i], alpha=0.6)
            ax.scatter(data[method2], data[method1], marker='+', color=colors[j], alpha=0.6)
        # Set axis labels with increased font size for better readability
        ax.set_xlabel(method1 if i < len(methods) - 1 else '', fontsize=14)
        ax.set_ylabel(method2 if i > 0 else '', fontsize=14)

# Adjust layout
plt.tight_layout()

# Add a legend to the plot with method-color mapping
legend_labels = {method: color for method, color in zip(methods, colors)}
handles = [plt.Rectangle((0,0),1,1, color=legend_labels[method]) for method in methods]
legend = plt.legend(handles, methods, title='Methods', bbox_to_anchor=(1.05, 1), loc=2)

# Save the plot to a file
plt.savefig('final_custom_pairplot_with_labels.png')

# Show the plot
plt.show()
