from Uploader import upload, upload_directory
from Evaluation.PrecisionRecall import precision_recall_curve
import requests


def integrity_check():
    url = "http://localhost:8000/apiv1/integrity/"
    response = requests.get(url)
    print(response.json())


if __name__ == '__main__':
    integrity_check()
