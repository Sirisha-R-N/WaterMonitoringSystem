% Read water level over the past 1 minute from the Smart Water Monitoring channel
% and send alert if water level is below threshold

% === Channel ID to read data from ===
readChannelID = 2907494;

% === Water Level Field ID ===
waterLevelFieldID = 1;

% === Channel Read API Key ===
readAPIKey = '4GPY4B2SO5J9ADJI';  % Replace with your actual read API key

% === Tank configuration ===
tankHeight = 12;          % Tank height in cm
thresholdLevel = 3;       % Minimum acceptable water level in cm

% === Read water level data for the last 1 minute ===
waterLevel = thingSpeakRead(readChannelID, 'Fields', waterLevelFieldID, ...
    'NumMinutes', 1, 'ReadKey', readAPIKey);

% === Display current water level ===
disp(waterLevel)

% === Calculate water percentage ===
waterPercent = (waterLevel / tankHeight) * 100;
disp("Water Level Percentage:");
disp(waterPercent);

% === Provide the ThingSpeak alerts API key ===
alertApiKey = 'TAKX8VJzGKzK+89BoP3';  % Replace with your alert API key

% === Set the address for the HTTTP call ===
alertUrl = "https://api.thingspeak.com/alerts/send";

% === Set up header options ===
options = weboptions("HeaderFields", ["ThingSpeak-Alerts-API-Key", alertApiKey]);

% === Set the alert subject ===
alertSubject = sprintf("???? Water Level Alert");

% === Check if alert condition is met ===
if waterLevel < thresholdLevel
    % Compose alert body
    alertBody = sprintf("⚠️ Warning! High Water Consumption detected multiple times. Water supply will be cut soon");
    
    % === Try sending the alert ===
    try
        webwrite(alertUrl, "body", alertBody, "subject", alertSubject, options);
        disp("✅ Water level alert sent successfully.");
    catch someException
        fprintf("❌ Failed to send alert: %s\n", someException.message);
    end
else
    disp("✅ Water level is sufficient. No alert sent.");
end
