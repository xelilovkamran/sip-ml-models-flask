import requests


def test_analyze():
    url = 'http://127.0.0.1:5000/analyze/analyze-content-image'
    test_image_url = 'https://res.cloudinary.com/dvp7p1gol/image/upload/v1722452452/gp8jwkcw8fm4krp3grov.webp'
    test_comment = "I love"

    response = requests.post(
        url, json={'image_url': test_image_url, 'comment': test_comment})
    print(response.json())


if __name__ == '__main__':
    test_analyze()
