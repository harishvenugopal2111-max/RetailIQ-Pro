import pandas as pd
from sklearn.cluster import KMeans

def customer_segmentation():

    df = pd.read_csv("data/clean_superstore.csv")

    customer = (
        df.groupby("Customer ID")
        .agg({
            "Sales":"sum",
            "Profit":"sum",
            "Quantity":"sum"
        })
    )

    model = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10
    )

    customer["Cluster"] = model.fit_predict(customer)

    return customer
