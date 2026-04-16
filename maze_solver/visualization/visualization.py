import matplotlib.pyplot as plt
import numpy as np
from math import pi
import pandas as pd


def plot_step_metrics(df):
    plt.figure(figsize=(12, 6))
    for algo in df["algorithm"].unique():
        algo_data = df[df["algorithm"] == algo]
        avg_time = np.mean([steps for steps in algo_data["steps times"]], axis=0)
        avg_memory = np.mean([steps for steps in algo_data["steps memory"]], axis=0)
        plt.plot(avg_time, label=f"{algo} Time")
        plt.plot(avg_memory, label=f"{algo} Memory")
    plt.xlabel("Steps")
    plt.ylabel("Average Time (s) / Memory (KB)")
    plt.title("step-by-step performance")
    plt.legend()
    plt.show()


def plot_radar_chart(df):
    """
    cree un graphique en radar pour comparer les algorithmes
    args:
    df: dataframe contenant les métriques à comparer, avec une colonne 'algorithm' 'time' 'memory' et 'path_length'
    """


categories = ["time", "memory", "path_length"]
num_vars = len(categories)
# normalisation des donnees
df_normalized = df.groupby("algorithm")[categories].mean()  # moyenne par algorithme
max_values = df_normalized.max().max()  # valeur max pour la normalisation globale
df_normalized = df_normalized / max_values
# creation du graphique
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, polar=True)

# angles pour chaque categorie
angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
angles += angles[:1]  # pour fermer le cercle

# trace pour chaque categorie
for algorithme in df["algorithm"].unique():
    values = df_normalized.loc[algorithme].values.tolist()
    values += values[:1]  # pour fermer le cercle
    ax.plot(angles, values, marker="o", label=algorithme)
    ax.fill(angles, values, alpha=0.25)  # remplissage de la surface
    # configuration du graphique
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    ax.set_rlabels_position(0)
    plt.xticks(angles[:-1], categories)  # ajoout des labels pour chaque categorie
    plt.yticks(
        [0, 0.25, 0.5, 0.75, 1], ["0%", "25%", "50%", "75%", "100%"]
    )  # ajout des labels pour les valeurs radiales
    ax.grid(True)
    plt.title("Comparaison des algorithmes de recherche (normalisé)")
    plt.legend(
        loc="upper right", bbox_to_anchor=(1.3, 1.1)
    )  # legende a lexterieur du graphique
    plt.tight_layout()  # ajustement pour eviterde couper la legende
    plt.show()


def plot_performance_comparison(stats):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    metrics = ["time", "memory", "path_length"]
    for i, metric in enumerate(metrics):
        means = stats[(metric, "mean")]
        stds = stats[(metric, "std")]

        axes[i].bar(stats.index, means, yerr=stds, capsize=5)
        axes[i].set_title(f"{metric} Comparison")
        axes[i].set_ylabel(metric)
        axes[i].set_xticks("algorithm")
        axes[i].grid(True)
    plt.tight_layout()
    plt.show()


def plot_boxplots(df):
    import seaborn as sns

    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    sns.boxplot(x="algorithm", y="time", data=df, ax=axes[0], palette="Set3")
    axes[0].set_title("Boxplot of time", fontsize=14)
    axes[0].set_xlabel("Algorithm")
    axes[0].set_ylabel("Time")
    axes[0].grid(True, linestyle="--", alpha=0.6)

    sns.boxplot(x="algorithm", y="memory", data=df, ax=axes[1], palette="Set3")
    axes[1].set_title("Boxplot of memory", fontsize=14)
    axes[1].set_xlabel("Algorithm")
    # axes[1].set_ylabel[0,40])
    axes[1].set_ylabel("Memory (KB)")
    axes[1].grid(True, linestyle="--", alpha=0.6)

    sns.boxplot(x="algorithm", y="path_length", data=df, ax=axes[2], palette="Set3")
    axes[2].set_title("Boxplot of path length", fontsize=14)
    axes[2].set_xlabel("Algorithm")
    axes[2].set_ylabel("Path Length")
    axes[2].grid(True, linestyle="--", alpha=0.6)

    # plt.tight_layout()
    plt.show()

    def plot_pie_chart(stats):
        metrics = ["time", "memory", "path_length"]
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        for i, metric in enumerate(metrics):
            means = stats[(metric, "mean")]
            axes[i].pie(means, labels=stats.index, autopct="%1.1f%%", startangle=140)
            axes[i].set_title(f"{metric} Distribution")
