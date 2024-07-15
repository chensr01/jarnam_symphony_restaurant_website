window.addEventListener('DOMContentLoaded', event => {
    // Check if the container exists
    if (document.querySelector('.list-hours')) {
        const listHoursArray = document.body.querySelectorAll('.list-hours li');
        const currentDayIndex = new Date().getDay();

        if (listHoursArray.length > 0 && listHoursArray[currentDayIndex]) {
            listHoursArray[currentDayIndex].classList.add('today');
        }
    }
});
