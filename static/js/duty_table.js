document.addEventListener('DOMContentLoaded', function () {
    const table = document.getElementById('duty-table');
    const dutyCells = document.querySelectorAll('.duty-cell');

    dutyCells.forEach(cell => {
        cell.addEventListener('contextmenu', (event) => {
            event.preventDefault();
            const color = prompt('blue)');
            cell.style.backgroundColor = color;
        });
    });

    table.addEventListener('contextmenu', (event) => {
        event.preventDefault();
        const newColumn = prompt('Введите название новой комнаты');
        if (newColumn) {
            const newTh = document.createElement('th');
            newTh.textContent = newColumn;
            table.querySelector('thead tr').appendChild(newTh);

            const newCells = document.createElement('td');
            newCells.classList.add('duty-cell');
            table.querySelectorAll('tbody tr').forEach(row => {
                row.appendChild(newCells.cloneNode());
            });
        }
    });
});