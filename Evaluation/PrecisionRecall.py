import requests
from matplotlib import pyplot as plt


def precision_recall(con: dict, alg: dict, k: int = 11):
    url: str = "http://localhost:8000/apiv1/search/"
    body: dict = {
        "query": con["query"],
        "method": alg["method"],
        "k": 10,
    }

    if alg["method"] == "TF-IDF":
        body["similarity_method"] = alg["similarity_method"]

    recall_to_precision: dict = {
        'recall': [],
        'precision': []
    }

    for k in range(1, k):
        body["k"] = k
        response = requests.post(url, json=body)
        songs = response.json()["Songs"]
        relevant_songs = [song for song in songs if song['song_id'] in con['relevant_songs']]
        p_at_k: float = float(len(relevant_songs)) / float(k)
        r_at_k: float = float(len(relevant_songs)) / float(len(con['relevant_songs']))
        recall_to_precision['recall'].append(r_at_k)
        recall_to_precision['precision'].append(p_at_k)
        print(f"Precision at {k}: {p_at_k} | Recall at {k}: {r_at_k}")

    return recall_to_precision


def precision_recall_curve():
    queries = [
        {
            'query': 'Dimension Drum & Bass',
            'relevant_songs': [
                '60b88c30-d7be-4721-8c78-222a99c114c3',
                '71ed7a76-fa6d-45ce-ae4e-5a0349243ed2',
                'a3238477-3aa2-462c-95e9-785fca9a3b20',
                '4aab260c-10d7-42fa-b00d-ab9878ea85c3',
                'c0ef71ff-b334-4797-b9f2-68d79fb08b46'
            ]
        },
        {
            'query': 'Ray Volpe Dubstep',
            'relevant_songs': [
                '8b7c718f-4a01-4f5b-b1ab-bcdb2c0e39c4',
                '4f5e9a83-f829-431a-9143-7c98784f0ca0',
            ]
        },
        {
            'query': 'Dancefloor Drum & Bass',
            'relevant_songs': [
                'bbd49447-1967-4714-97df-ed9cfcf3fcc0',
                'fa8c3a82-3f9b-44cc-9f77-7225d0a7b4fa',
                '71ed7a76-fa6d-45ce-ae4e-5a0349243ed2',
                '517d2f9d-1bbb-4996-b802-5256a2fc63c3'
            ]
        },
        {
            'query': 'Deep vocals Flowdan',
            'relevant_songs': [
                '9e85507e-3f5f-4086-98b0-bdf50a1753ee',
                'b8e389e7-17c4-4eb8-b277-4aa967bb5cff',
                '48db9155-032c-4f80-ba01-144cc396a2bd'
            ]
        },
        {
            'query': 'popular song with good drop',
            'relevant_songs': [
                '55a38b09-1927-4c03-808b-a4b10b97589a',
                '4f5e9a83-f829-431a-9143-7c98784f0ca0',
                'd857fb59-f3b9-4aa4-bfea-fa010b366b31',
                '654d6788-4a52-4c0b-807c-04d672db032d'
            ]
        },
        {
            'query': 'Popular Jump Up',
            'relevant_songs': [
                '623a1acb-def2-46f5-ae06-365c5dc3fd87',
                '37375a25-d774-4ca9-b1ee-f293e0c65630',
                '35d26cf3-05b3-4abc-b954-1a9f68fd2764',
                '654d6788-4a52-4c0b-807c-04d672db032d'
            ]
        }
    ]

    configs = [
        {
            'method': 'TF-IDF',
            'similarity_method': 'Cosine'
        },
        {
            'method': 'LSI',
        }
    ]

    for config in configs:
        plt.figure()
        plt.title("Precision-Recall Curve: " + config['method'])
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        for q in queries:
            recall_to_precision = precision_recall(q, config, 11)
            plt.plot(list(recall_to_precision['recall']), list(recall_to_precision['precision']), label=q['query'], marker='o', linestyle='-')

        plt.legend()
        plt.show()
