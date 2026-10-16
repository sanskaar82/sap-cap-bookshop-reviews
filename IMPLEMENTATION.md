# SAP CAP Bookshop – Implementation Details

## 1. Overview

This document describes my implementation of the Reviews functionality
for the SAP CAP Bookshop application as part of the assigned homework.

The original project README.md contains the project introduction,
prerequisites, and assignment instructions. This document focuses
specifically on the changes I implemented.

## 2. Files Modified and Added

| File | Changes |
|---|---|
| `db/schema.cds` | Added the Reviews entity and its association with Books. |
| `srv/cat-service.cds` | Exposed Reviews through CatalogService. |
| `srv/cat-service.js` | Added rating validation before creating a review. |
| `reviews.py` | Added a Python script to submit reviews and calculate average ratings. |

## 3. Reviews Entity

I added a `Reviews` entity in `db/schema.cds`.

The entity contains:
- `ID`: Unique identifier for each review.
- `rating`: Rating given to a book.
- `comment`: Textual feedback about the book.
- `book`: Association linking the review to a book.

The entity uses the CAP `managed` aspect for standard creation and
modification metadata.

## 4. Exposing Reviews Through the OData Service

I updated `srv/cat-service.cds` to expose the Reviews entity through
the existing `CatalogService`.

The Reviews endpoint is:

`http://localhost:4004/odata/v4/catalog/Reviews`

This allows clients to submit and retrieve reviews through the service.

## 5. Rating Validation

I implemented a `before('CREATE', Reviews)` handler in
`srv/cat-service.js`.

Before a review is created, the handler checks that the rating is
an integer between 1 and 5, inclusive.

Invalid ratings are rejected with HTTP 400 and the message:

`Rating must be an integer between 1 and 5`

This prevents reviews with invalid ratings from being created.

## 6. Python Script for Reviews

I created `reviews.py` to interact with the Catalog OData service.

The script performs the following operations:

1. Submits three sample reviews using HTTP POST requests.
2. Retrieves the reviews from the OData service.
3. Groups the reviews by book ID.
4. Calculates the average rating for each book.
5. Prints the average rating and number of reviews for each book.

The script uses Python's built-in `urllib` library for HTTP requests
and `json` for processing JSON responses.

## 7. Testing and Results

### Valid Reviews

I ran the Python script while the CAP server was running.

All three sample reviews were successfully submitted, returning
HTTP 201 responses.

### Invalid Rating

I tested a review with a rating of 6.

The service rejected the request with HTTP 400 and returned the
rating validation error.

### Average Rating Calculation

The script produced the following output when run against a database
containing the three sample reviews:

    Review submitted: HTTP 201
    Review submitted: HTTP 201
    Review submitted: HTTP 201

    Average rating per book:
    Book ID: 1 | Average rating: 4.50 | Reviews: 2
    Book ID: 2 | Average rating: 3.00 | Reviews: 1

## 8. How to Run

### Start the CAP Server

From the project directory, run:

    npx cds watch

### Run the Python Script

Open a second terminal in the project directory and run:

    python reviews.py

On Windows, you can alternatively use:

    py reviews.py

The CAP server must remain running while the Python script executes.

## 9. Summary

The Bookshop application has been extended with review management,
rating validation, and average-rating calculation.

The implementation demonstrates the use of CDS entities and
associations, CAP service handlers, OData endpoints, HTTP requests,
and Python-based data processing.
