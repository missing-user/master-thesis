# %%
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import matplotlib

plt.rcParams.update({
    "font.family": "sans-serif",  # use serif/main font for text elements
    "text.usetex": True,     # use inline math for ticks
    "pgf.rcfonts": False,    # don't setup fonts from rc parameters
    "pgf.texsystem": "pdflatex",
    # Make the legend/label fonts a little smaller
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.facecolor" : "FFFFFF"
})
def set_cmap(cycles:int|list=4):
    if isinstance(cycles, list) and len(cycles) > 0:
        assert sum(cycles) > 0
        scaling = 1/(1-0.5/len(cycles))
        midevalpoints = [i/len(cycles) * scaling for i in range(len(cycles))] 
        evalpoints = []
        for i, cat in zip(midevalpoints, cycles):
            ministep = 0.5/len(cycles)/cat
            for j in range(cat):
                evalpoints.append(i + ministep*j)
    else:
      evalpoints = [i/cycles for i in range(cycles)]
      if cycles == 2:
          evalpoints = [0, 0.7]

    plt.rcParams['axes.prop_cycle'] = matplotlib.cycler(color=[plt.cm.plasma(e) for e in evalpoints])
    plt.rcParams['image.cmap'] = 'plasma'
    return plt.rcParams['axes.prop_cycle']
set_cmap(6)

# %%
def plot_from_csv(filename, title:str, do_fit=True):
    # Load file
    df = pd.read_csv(filename)
    filename = filename.split("/")[-1]
    
    # Assume first column is x, others are y-series
    x_label = df.columns[0]
    y_labels = df.columns[1:]
    x_vals = df[x_label].values

    plt.figure(figsize=(6, 4))
    
    for i, y_label in enumerate(y_labels):
        y_vals = df[y_label].values
        plt.scatter(x_vals, y_vals, s=4, label=y_label)

        if do_fit:
            try:
                reg = linregress(x_vals, y_vals)
                plt.axline(
                    xy1=(0, reg.intercept),
                    slope=reg.slope,
                    color="k" if len(y_labels) == 1 else plt.rcParams["axes.prop_cycle"].by_key()["color"][i],
                    label=f"{y_label} fit: $R^2$={reg.rvalue**2:.3f}"
                )
            except Exception as e:
                print(f"Skipping linear fit for {y_label}: {e}")
        
    plt.xlabel(x_label)
    plt.ylabel(" / ".join(y_labels) if len(y_labels) == 1 else "Values")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


# %%
plot_from_csv("L_REGCOIL_vs_Lgradb.csv", title=r"$L_{REGCOIL}$_vs_$L^*_{\nabla_B}$.csv")

# %%
plot_from_csv("QUASR_coil_distance_vs_L_REGCOIL.csv", title=r"QUASR_coil_distance_vs_$L_{REGCOIL}$.csv")

# %%
plot_from_csv("QUASR_coil_distance_vs_Lgradb.csv", title=r"QUASR_coil_distance_vs_$L^*_{\nabla_B}$.csv")
