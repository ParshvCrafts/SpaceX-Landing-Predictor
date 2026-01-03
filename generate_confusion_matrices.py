"""
Generate Confusion Matrices for Original ML Models
Based on the results from Machine Learning Prediction.ipynb
"""

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
import os

# Set the style for all plots
plt.style.use('dark_background')

# Create output directory
output_dir = 'webapp/images/eda'
os.makedirs(output_dir, exist_ok=True)

# Custom color palette matching the website theme
colors = {
    'success': '#00D4AA',
    'failure': '#EF4444',
    'primary': '#0066FF',
    'secondary': '#A855F7',
}

# Load the datasets (same as original notebook)
print("Loading datasets...")
df_part2 = pd.read_csv('Datasets/dataset_part_2.csv')
df_part3 = pd.read_csv('Datasets/dataset_part_3.csv')

# Get target variable
Y = df_part2['Class'].values

# Features (one-hot encoded from part 3)
X = df_part3.values

# Train/test split with same random_state as original notebook
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define models with same hyperparameters as original notebook (from GridSearchCV results)
models = {
    'Logistic Regression': LogisticRegression(C=1, penalty='l2', solver='lbfgs', max_iter=1000),
    'SVM (Sigmoid)': SVC(C=31.62, gamma=0.0316, kernel='sigmoid'),
    'Decision Tree': DecisionTreeClassifier(criterion='entropy', max_depth=16, splitter='random', random_state=42),
    'KNN (k=10)': KNeighborsClassifier(n_neighbors=10, algorithm='auto', p=1)
}

def plot_confusion_matrix(y_true, y_pred, model_name, accuracy, filename):
    """Create a styled confusion matrix plot"""
    cm = confusion_matrix(y_true, y_pred)

    fig, ax = plt.subplots(figsize=(8, 6))

    # Create heatmap
    sns.heatmap(cm, annot=True, fmt='d', cmap='RdYlGn', center=0.5,
                xticklabels=['Failure', 'Success'],
                yticklabels=['Failure', 'Success'],
                ax=ax, cbar=True,
                annot_kws={'size': 20, 'weight': 'bold'},
                linewidths=2, linecolor='white')

    ax.set_xlabel('Predicted', fontsize=14, color='white')
    ax.set_ylabel('Actual', fontsize=14, color='white')
    ax.set_title(f'{model_name}\nAccuracy: {accuracy:.1f}%', fontsize=16, fontweight='bold', color='white', pad=15)

    ax.set_facecolor('#0A0A14')
    fig.patch.set_facecolor('#0A0A14')

    # Add metrics text
    tn, fp, fn, tp = cm.ravel()
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    metrics_text = f'Precision: {precision:.2f} | Recall: {recall:.2f} | F1: {f1:.2f}'
    ax.text(0.5, -0.12, metrics_text, transform=ax.transAxes,
            ha='center', fontsize=11, color='white')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/{filename}', dpi=150, facecolor='#0A0A14', bbox_inches='tight')
    plt.close()

    return cm, accuracy

print("\nTraining models and generating confusion matrices...")

results = {}
for name, model in models.items():
    print(f"\n{name}:")
    model.fit(X_train_scaled, Y_train)
    y_pred = model.predict(X_test_scaled)
    accuracy = (y_pred == Y_test).mean() * 100

    # Generate filename
    filename = f"cm_{name.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('=', '')}.png"

    cm, acc = plot_confusion_matrix(Y_test, y_pred, name, accuracy, filename)
    results[name] = {'cm': cm, 'accuracy': acc, 'predictions': y_pred}

    print(f"  Accuracy: {accuracy:.1f}%")
    print(f"  Saved: {filename}")

# Create a combined comparison chart
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
axes = axes.flatten()

for idx, (name, data) in enumerate(results.items()):
    cm = data['cm']
    acc = data['accuracy']

    sns.heatmap(cm, annot=True, fmt='d', cmap='RdYlGn', center=0.5,
                xticklabels=['Fail', 'Success'],
                yticklabels=['Fail', 'Success'],
                ax=axes[idx], cbar=False,
                annot_kws={'size': 16, 'weight': 'bold'},
                linewidths=1, linecolor='white')

    axes[idx].set_xlabel('Predicted', fontsize=11, color='white')
    axes[idx].set_ylabel('Actual', fontsize=11, color='white')
    axes[idx].set_title(f'{name}\n{acc:.1f}% Accuracy', fontsize=12, fontweight='bold', color='white')
    axes[idx].set_facecolor('#0A0A14')

fig.patch.set_facecolor('#0A0A14')
fig.suptitle('Original ML Models - Confusion Matrices Comparison', fontsize=16, fontweight='bold', color='white', y=1.02)
plt.tight_layout()
plt.savefig(f'{output_dir}/confusion_matrices_comparison.png', dpi=150, facecolor='#0A0A14', bbox_inches='tight')
plt.close()
print("\nSaved: confusion_matrices_comparison.png")

# Create accuracy comparison bar chart
fig, ax = plt.subplots(figsize=(12, 6))

model_names = list(results.keys())
accuracies = [results[name]['accuracy'] for name in model_names]
colors_bar = [colors['success'] if acc >= 80 else colors['primary'] for acc in accuracies]

bars = ax.bar(model_names, accuracies, color=colors_bar, edgecolor='white', linewidth=0.5)

ax.set_ylabel('Accuracy (%)', fontsize=14, color='white')
ax.set_title('Original ML Models - Accuracy Comparison', fontsize=16, fontweight='bold', color='white')
ax.set_facecolor('#0A0A14')
fig.patch.set_facecolor('#0A0A14')
ax.set_ylim(0, 110)
ax.grid(True, alpha=0.2, axis='y')

# Add value labels
for bar, acc in zip(bars, accuracies):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
            f'{acc:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold', color='white')

# Highlight best model
best_idx = np.argmax(accuracies)
bars[best_idx].set_edgecolor('#FFD700')
bars[best_idx].set_linewidth(3)
ax.text(best_idx, accuracies[best_idx] + 8, 'BEST', ha='center', fontsize=10,
        fontweight='bold', color='#FFD700')

plt.xticks(rotation=15, ha='right')
plt.tight_layout()
plt.savefig(f'{output_dir}/model_accuracy_comparison.png', dpi=150, facecolor='#0A0A14', bbox_inches='tight')
plt.close()
print("Saved: model_accuracy_comparison.png")

print("\nAll confusion matrices generated successfully!")
print(f"\nBest Model: {model_names[best_idx]} with {accuracies[best_idx]:.1f}% accuracy")
