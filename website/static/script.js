$(document).ready(function() {
    function fetchData() {
        $.getJSON(thingspeakApiUrl, function(data) {
            if (data.feeds.length > 0) {
                let levels = [];
                let timestamps = [];
                let lastValue = parseFloat(data.feeds[data.feeds.length - 1].field1);
                let firstValue = parseFloat(data.feeds[0].field1);
                
                // Calculate consumption
                let consumption = firstValue - lastValue;
                let message = "";

                if (consumption > 1) {
                    message = "⚠️ Overuse detected! Reduce water consumption.";
                    $("#consumptionMessage").removeClass().addClass("danger");
                } else if (consumption > 0.5) {
                    message = "⚠️ High water usage. Consider conservation.";
                    $("#consumptionMessage").removeClass().addClass("warning");
                } else {
                    message = "✅ Water consumption is normal.";
                    $("#consumptionMessage").removeClass().addClass("normal");
                }

                $("#consumptionMessage").text(message);

                // Update current water level
                $("#waterLevel").text(lastValue + " cm");

                // Update water tank UI
                let fillPercentage = (lastValue / 12) * 100; // Assuming 50 cm max height
                $("#waterFill").css("height", fillPercentage + "%");

                // Populate chart data
                data.feeds.forEach(feed => {
                    levels.push(parseFloat(feed.field1));
                    timestamps.push(new Date(feed.created_at).toLocaleTimeString());
                });

                updateChart(levels, timestamps);
            }
        });
    }

    function updateChart(levels, timestamps) {
        let ctx = document.getElementById("waterChart").getContext("2d");
    
        // Destroy previous chart instance if it exists (prevents infinite resizing)
        if (window.waterChartInstance) {
            window.waterChartInstance.destroy();
        }
    
        // Create new chart instance with fixed size
        window.waterChartInstance = new Chart(ctx, {
            type: "line",
            data: {
                labels: timestamps,
                datasets: [{
                    label: "Water Level (cm)",
                    data: levels,
                    borderColor: "#3498db",
                    backgroundColor: "rgba(52, 152, 219, 0.3)",
                    fill: true
                }]
            },
            options: {
                responsive: false, // Prevents infinite resizing
                maintainAspectRatio: false,
                scales: {
                    y: {
                        min: 0, // Prevents excessive downward stretching
                        max: 50 // Adjust max value as needed
                    }
                }
            }
        });
    }
    

    // Fetch data every 10 seconds
    fetchData();
    setInterval(fetchData, 5000);
});
