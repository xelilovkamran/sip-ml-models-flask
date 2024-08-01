import requests


def test_analyze():
    url = 'http://127.0.0.1:5000/analyze/analyze-comment'
    test_comments = [
        "I love this product.",
        "This is absolutely terrible.",
        "I am very happy with my purchase.",
        "I hate this so much.",
        "Today is to be great, sir",
        "I love car",
        "Great job",
        "Run",
        "Love",
        "I am going to run",
        "I am going to love",
        "I am going to love this",
        "I am going to love car",
        "I am going to love this car",
        "I hate",
        "I hate car",
        "I hate this car",
        "I hate this product",
        "I hate this so much",
        "I hate to be great",
    ]

    for comment in test_comments:
        response = requests.post(url, json={'comment': comment})
        print(f"Comment: {comment}")
        print(f"Response: {response.json()}")


if __name__ == '__main__':
    test_analyze()
