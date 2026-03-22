fetch("/tasks/stats/")
.then(response => response.json())
.then(data => {

var ctx = document.getElementById('taskChart');

new Chart(ctx, {
type: 'doughnut',
data: {

labels: ['Completed', 'Pending'],

datasets: [{
data: [data.completed, data.pending]
}]

}

});

});