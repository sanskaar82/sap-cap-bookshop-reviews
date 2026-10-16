import json
import urllib.request
import urllib.error
from collections import defaultdict

BASE_URL = "http://localhost:4004/odata/v4/catalog"

reviews = [
    {"rating": 5, "comment": "Excellent book", "book_ID": 1},
    {"rating": 4, "comment": "Very informative", "book_ID": 1},
    {"rating": 3, "comment": "Good overall", "book_ID": 2}
]


def post_review(review):
    request = urllib.request.Request(
        f"{BASE_URL}/Reviews",
        data=json.dumps(review).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request) as response:
        print(f"Review submitted: HTTP {response.status}")


def main():
    for review in reviews:
        post_review(review)

    request = urllib.request.Request(
        f"{BASE_URL}/Reviews",
        headers={"Accept": "application/json"}
    )

    with urllib.request.urlopen(request) as response:
        data = json.loads(response.read().decode("utf-8"))

    ratings_by_book = defaultdict(list)

    for review in data["value"]:
        book_id = review.get("book_ID")
        if book_id is not None:
            ratings_by_book[book_id].append(review["rating"])

    print("\nAverage rating per book:")

    for book_id, ratings in sorted(ratings_by_book.items()):
        average = sum(ratings) / len(ratings)
        print(
            f"Book ID: {book_id} | "
            f"Average rating: {average:.2f} | "
            f"Reviews: {len(ratings)}"
        )


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as error:
        print(f"HTTP error: {error.code}")
        print(error.read().decode("utf-8"))
    except urllib.error.URLError as error:
        print(f"Connection error: {error.reason}")