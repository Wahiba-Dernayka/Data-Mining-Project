import ttkbootstrap as tb
from ttkbootstrap.constants import *

# External modules (your own files)
from KMeansTab import KMeansTab
from AprioriTab import AprioriTab

if __name__ == "__main__":
    app = tb.Window(themename="solar")
    app.title("Data Mining Toolkit")
    # app.geometry("1020x760")

    notebook = tb.Notebook(app)
    notebook.pack(fill=BOTH, expand=YES)

    apriori_tab = tb.Frame(notebook)
    kmeans_tab = tb.Frame(notebook)
    notebook.add(apriori_tab, text="Apriori Algorithm")
    notebook.add(kmeans_tab, text="KMeans Clustering")

    AprioriTab(apriori_tab)
    KMeansTab(kmeans_tab)

    app.mainloop()
