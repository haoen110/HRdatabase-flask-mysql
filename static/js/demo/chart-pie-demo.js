// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ["PPP Department", "Financial Department", "Official Department", "Peace Hotel", "Exhibition Center", "Support Department", "Property Department"],
    datasets: [{
      data: [68, 11, 22, 69, 34, 25, 23],
      backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745', '#a52a2a', 'cornsilk', 'deeppink'],
    }],
  },
});
