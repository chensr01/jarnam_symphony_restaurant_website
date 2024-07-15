"use strict"

// Sends a new request to update the reservation list
function getList() {
    let timeslotId = document.getElementById('reservationTime').value;
    console.log("Selected timeslot ID:", timeslotId);

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState !== 4) return
        updatePage(xhr)
    }

    // Add request parameters for the availability at a timeslot
    let url = `/restaurant/get-reservation/${encodeURIComponent(timeslotId)}/`;

    xhr.open("GET", url, true)
    xhr.send()
}

function updatePage(xhr) {
    if (xhr.status === 200) {
        // response.reservations
        let response = JSON.parse(xhr.responseText)
        updateList(response)
        return
    }

    if (xhr.status === 0) {
        displayError("Cannot connect to server")
        return
    }


    if (!xhr.getResponseHeader('content-type') === 'application/json') {
        displayError(`Received status = ${xhr.status}`)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}


function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}


function createTableElement(type, index, isReserved) {
    let tableClass = isReserved ? 'reser-table booked-table' : 'reser-table empty-table';
    let imageName = isReserved ? `${type}red.png` : `${type}.png`;
    let onClickAttribute = isReserved ? '' : `onclick="makeReservation('${type}-table-${index}')"`; // Note the corrected onclick attribute

    return `<div id="div-${type}-table-${index}" class="table-container">
                <img src="/static/images/${imageName}" alt="Table for ${type}" class="${tableClass}" ${onClickAttribute} id="${type}-table-${index}">
            </div>`;
}

function updateList(response) {
    let container = document.getElementById("tablesLayout");

    let tableCounts = { 'two': 8, 'four': 4, 'six': 2 };

    Object.keys(tableCounts).forEach(type => {
        for (let i = 1; i <= tableCounts[type]; i++) {
            let tableId = `${type}-table-${i}`;
            let isReserved = response.reservations.some(reservation => reservation.table === tableId);
            let divTableId = `div-${type}-table-${i}`;
            let existingTableD = document.getElementById(divTableId);
            let existingTable = document.getElementById(tableId);

            // Check if table exists
            if (!existingTableD) {
                // Generate table HTML if it does not exist
                let tableHTML = createTableElement(type, i, isReserved);
                container.insertAdjacentHTML('beforeend', tableHTML);
            } else {
                // Modify table HTML only if reservation status changes
                if ((isReserved && !existingTable.classList.contains('booked-table')) || (!isReserved && existingTable.classList.contains('booked-table'))) {
                    // let tableImg = existingTable.querySelector('img');
                    let newImageName = isReserved ? `${type}red.png` : `${type}.png`;
                    let newTableClass = isReserved ? 'reser-table booked-table' : 'reser-table empty-table';
                    // tableImg.src = `/static/images/${newImageName}`;
                    // tableImg.className = newTableClass;
                    existingTable.src = `/static/images/${newImageName}`;
                    existingTable.className = newTableClass;
                    if (isReserved) {
                        existingTable.removeAttribute('onclick');
                    } else {
                        existingTable.setAttribute('onclick', `makeReservation('${tableId}')`);
                    }
                }
            }
        }
    });
}


function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
}

function makeReservation(tableId) {
    let timeslotId = document.getElementById('reservationTime').value;
    let xhr = new XMLHttpRequest();
    xhr.open('POST', makeReservationURL, true); // Use the correct path to your Django view
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader('X-CSRFToken', getCSRFToken()); // Ensure you're obtaining the CSRF token correctly

    xhr.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE) {
            // if (this.status === 200) {
            //     // Successfully made a reservation, update the page
            //     updatePage(this);
            // } else {
            //     // Handle errors, such as displaying a message to the user
            //     displayError('Error making reservation.');
            // }
            let response = JSON.parse(this.responseText);
            if (this.status === 200) {
                Swal.fire({
                    title: 'Woohoo!',
                    text: response.success,
                    icon: 'success',
                    background: '#fcf6ee',
                    confirmButtonColor: '#cf964d',
                    confirmButtonText: "Can't Wait!"
                });
            } else {
                Swal.fire({
                    title: 'Oops!',
                    text: "Reservation Error: " + response.error,
                    icon: 'error',
                    background: '#fcf6ee',
                    confirmButtonColor: '#cf964d',
                    confirmButtonText: 'OK'
                });
            }
        }
    };

    // Send the request with the table ID and timeslot
    xhr.send(`table_id=${encodeURIComponent(tableId)}&timeslot_id=${encodeURIComponent(timeslotId)}&csrfmiddlewaretoken=${getCSRFToken()}`);
}


function deleteItem(id) {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState !== 4) return
        updatePage(xhr)
    }

    xhr.open("POST", deleteItemURL(id), true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhr.send(`csrfmiddlewaretoken=${getCSRFToken()}`)
}

function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}