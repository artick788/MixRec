import requests
from matplotlib import pyplot as plt


def precision_recall(con: dict, alg: dict):
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

    for k in range(1, con['k'] + 1):
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
    cases = [
        {
            'query': 'Sub Focus',
            'relevant_songs': [
                'a0cd6988-43fe-4e39-8ba9-c917330580b9',
                '3e6b3e61-457c-41f8-92c3-1411bcf22568',
                'bd28eac0-2a69-4feb-b644-c403d9459551',
                '8b5b6e8b-5dc5-4a73-9268-7b5cf3d37eb9',
                '72186678-c880-4f25-b5fe-a452b2091c42',
                'c6aca6f6-7f27-4165-8ffb-3b10098c04bc',
                '171120ee-360e-438a-8de0-fdae8ad665c0'
            ],
            'k': 7
        },
        {
            'query': 'Ray Volpe Dubstep 11A',
            'relevant_songs': [
                '8b7c718f-4a01-4f5b-b1ab-bcdb2c0e39c4',
                '4f5e9a83-f829-431a-9143-7c98784f0ca0',
            ],
            'k': 3
        },
        {
            'query': 'Dancefloor Drum & Bass',
            'relevant_songs': [
                'bbd49447-1967-4714-97df-ed9cfcf3fcc0',
                'fa8c3a82-3f9b-44cc-9f77-7225d0a7b4fa',
                '71ed7a76-fa6d-45ce-ae4e-5a0349243ed2',
                '517d2f9d-1bbb-4996-b802-5256a2fc63c3'
            ],
            'k': 4
        },
        {
            'query': 'Deep vocals Flowdan',
            'relevant_songs': [
                '9e85507e-3f5f-4086-98b0-bdf50a1753ee',
                'b8e389e7-17c4-4eb8-b277-4aa967bb5cff',
                '48db9155-032c-4f80-ba01-144cc396a2bd'
            ],
            'k': 6
        },
        {
            'query': 'popular song with good drop 8B',
            'relevant_songs': [
                '55a38b09-1927-4c03-808b-a4b10b97589a',
                '4f5e9a83-f829-431a-9143-7c98784f0ca0',
                'd857fb59-f3b9-4aa4-bfea-fa010b366b31',
                '654d6788-4a52-4c0b-807c-04d672db032d'
            ],
            'k': 5
        },
        {
            'query': 'Popular Jump Up',
            'relevant_songs': [
                '623a1acb-def2-46f5-ae06-365c5dc3fd87',
                '37375a25-d774-4ca9-b1ee-f293e0c65630',
                '35d26cf3-05b3-4abc-b954-1a9f68fd2764',
                '654d6788-4a52-4c0b-807c-04d672db032d'
            ],
            'k': 4
        },
        {
            'query': 'popular sing along good vocals',
            'relevant_songs': [
                '9e85507e-3f5f-4086-98b0-bdf50a1753ee',
                'b02e41a0-2b01-46a9-a765-384f629ce239',
                '1ded55f8-5f6d-44ee-9c14-dada3db918de',
                'f0f2cdd3-36d9-49f3-815f-0ba36ece33cc',
                'f3711769-a787-487e-bf46-c7ca9fe1b9f8'
            ],
            'k': 11
        }
    ]

    configs = [
        {
            'method': 'TF-IDF',
            'similarity_method': 'Cosine'
        },
        {
            'method': 'LSI',
        },
        {
            'method': 'TF-IDF',
            'similarity_method': 'Euclidean'
        },
        {
            'method': 'TF-IDF',
            'similarity_method': 'Manhattan'
        },
    ]

    for config in configs:
        plt.figure()
        title = "Precision-Recall Curve: " + config['method']
        if 'similarity_method' in config:
            title += " (" + config['similarity_method'] + ")"
        plt.title(title)
        plt.xlabel("Recall")
        plt.ylabel("Precision")

        avg_precision_config = []
        avg_recall_config = []
        for case in cases:
            recall_to_precision = precision_recall(case, config)
            plt.plot(list(recall_to_precision['recall']), list(recall_to_precision['precision']), label=case['query'], marker='o', linestyle='-')

            avg_precision_case = sum(recall_to_precision['precision']) / len(recall_to_precision['precision'])
            avg_recall_case = sum(recall_to_precision['recall']) / len(recall_to_precision['recall'])
            avg_precision_config.append(avg_precision_case)
            avg_recall_config.append(avg_recall_case)

        plt.legend()
        plt.show()

        avg_precision = sum(avg_precision_config) / len(avg_precision_config)
        avg_recall = sum(avg_recall_config) / len(avg_recall_config)

        print("Averages for " + config['method'] + ":")
        print("Average Precision: " + str(avg_precision))
        print("Average Recall: " + str(avg_recall))




