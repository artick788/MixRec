import requests
from matplotlib import pyplot as plt


def precision_recall(query, total_relevant_songs):
    url: str = "http://localhost:8000/apiv1/search/"
    body: dict = {
        "query": query,
        "method": "TF-IDF",
        "k": 10,
        "similarity_method": "Cosine"
    }

    recall_to_precision: dict = {}

    for k in range(1, 11):
        body["k"] = k
        response = requests.post(url, json=body)
        songs = response.json()["Songs"]
        relevant_songs = [song for song in songs if
                          song["artist"].find("Dimension") != -1 and song['genre'] == "Drum & Bass"]
        p_at_k: float = float(len(relevant_songs)) / float(k)
        r_at_k: float = float(len(relevant_songs)) / float(total_relevant_songs)
        recall_to_precision[r_at_k] = p_at_k
        print(f"Precision at {k}: {p_at_k} | Recall at {k}: {r_at_k}")

    return recall_to_precision


def precision_recall_curve():
    query1 = "Dimension Drum & Bass"
    recall_to_precision = precision_recall(query1, 5)


    plt.figure()
    plt.title("Precision-Recall Curve")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.plot(list(recall_to_precision.keys()), list(recall_to_precision.values()), label=query1)
    plt.legend()
    plt.show()
