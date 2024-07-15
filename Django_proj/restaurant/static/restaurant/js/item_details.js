document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('reviewForm');
    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            submitReview();
        });
    } else {
        console.error("Could not find the review form element.");
    }

    loadReviews();
    setInterval(loadReviews, 5000);
});



function submitReview() {
    console.log("Submitting review...");
    const selectedRating = document.querySelector('input[name="rating"]:checked');
    if (!selectedRating) {
        console.warn("No rating selected.");
        alert('Please select a rating before submitting.');
        return;
    }
    const rating = selectedRating.value;
    const comment = document.getElementById('comment').value;
    console.log(`Rating: ${rating}, Comment: ${comment}`);

    const xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        console.log(`XHR state: ${xhr.readyState}, Status: ${xhr.status}`);
        if (xhr.readyState !== 4) return;

        if (xhr.status === 200) {
            console.log("Review submitted successfully.");
            loadReviews();
            document.getElementById('comment').value = '';
            document.querySelectorAll('input[name="rating"]').forEach(input => {
                input.checked = false;
            });
        } else {
            console.error("Failed to submit review.");
            alert('An error occurred while submitting the review.');
        }
    };

    xhr.open('POST', submitReviewUrl, true);
    xhr.setRequestHeader('X-CSRFToken', getCSRFToken());
    xhr.setRequestHeader('Content-Type', 'application/json');
    const data = JSON.stringify({ rating: rating, comment: comment });
    xhr.send(data);
}

function loadReviews() {
    const xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (xhr.readyState !== 4) return;

        if (xhr.status === 200) {
            const data = JSON.parse(xhr.responseText);
            const commentsSection = document.getElementById('comments-section');
            const averageRatingSpan = document.getElementById('average-rating');
            const starabilityResult = document.getElementById('starability-result');
            const numericRatingElement = document.getElementById('numeric-rating');
            if (numericRatingElement) {
                numericRatingElement.textContent = data.average_rating_decimal;
            }

            if (starabilityResult) {
                starabilityResult.setAttribute('data-rating', data.average_rating_integer.toString());
            } else {
                console.error("Starability rating display element not found.");
            }

            commentsSection.innerHTML = ''; 
            data.reviews.forEach(review => {
                const reviewDiv = document.createElement('div');
                reviewDiv.className = 'comment'; 
                reviewDiv.innerHTML = `
                    <div class="comment-header">
                        <strong class="comment-author">${review.created_by}</strong>
                        <span class="comment-date">${review.creation_time}</span>
                    </div>
                    <div class="comment-body">
                        ${review.comment}
                    </div>
                    <div class="comment-rating">Rating: ${review.rating} stars</div>
                `;
                commentsSection.appendChild(reviewDiv);
            });
        }else {
            console.error("Failed to load reviews: Status = " + xhr.status);
            alert('Failed to load reviews.');
        }
    };

    xhr.open('GET', getReviewsUrl, true);
    xhr.setRequestHeader('X-CSRFToken', getCSRFToken());
    xhr.send();
}



function getCSRFToken() {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; csrftoken=`);
    if (parts.length === 2) {
        const token = parts.pop().split(';').shift();
        console.log(`CSRF Token found: ${token}`);
        return token;
    }
    console.warn("CSRF token not found in cookies.");
    return ''; // Return an empty string when the csrftoken is not found in cookies
}


