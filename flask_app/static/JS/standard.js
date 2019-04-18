//The following JavaScript has to be below the main body of code, as it is calling Divs/elements that need to exist already
            function fillStation(thePlace){
                //create unique IDs for the select elements
                var id = "Station" + thePlace;
                //Make first option "default" to " - - - - "
                var text = "<br><select id=" + id + " name=" + id + ">";
                //loop through and add an option for each Station
                for (var i=0; i<stations.length; i++){
                    var name = stations[i]['name'];
                    var num = stations[i]['number'];
                    text += "<option value=" + num + ">" + name + "</option>";
                }
                text += "</select>";
                //append text body to the Div
                document.getElementById(thePlace).innerHTML += text;
            }

            //function to fill select boxes with options for time - in 5 minute increments
            function fillTime(thePlace) {
                //create unique ID for both collect time and drop off time
                var id = "Select" + thePlace;

                var text = "<br><select id=" + id + " name =" + id +">";

                //loop through for hours / 5min increments
                //JS time is "1" and not "01" for single digit hrs/mins - therefore extra handling required for specific values
                for (var i=0; i<=23; i++){
                    for (var j=0; j<56; j+=5){
                        if (i==0 && j==0){
                            var time = "0:00";
                        }else if (i == 0){
                            if (j==5){
                                var time = "0" + ":" + "05";
                            }
                            else{
                                var time = "0" + ":" + j;
                              }
                        }else if (j==0){
                            var time = i + ":" + "00";
                        }else if (j==5){
                            var time = i + ":" + "05";
                        }else{
                            var time = i + ":" + j;
                        }
                        text += "<option value=" + time + ">" + time + "</option>";
                    }
                }
                text += "</select>";
                document.getElementById(thePlace).innerHTML += text;
            }

            //invoke functions to fill the 2 select boxes for stations and 2 select boxes for times.
            fillTime("collectTime");
            fillTime("dropTime");
            fillStation("selectFrom");
            fillStation("selectTo");

            //function to auto-select boxes to current time (nearest 10) and drop off time (+30)
            function autoTimeDrop(value1, value2){
            document.getElementById('SelectcollectTime').value = value1;
            document.getElementById('SelectdropTime').value = value2;

        }

            //create a new date Object.  Create hour and minute variables from this.
            var today = new Date();
            var hrs = today.getHours();
            var mins = today.getMinutes();

            //function to "correct" the hours / minutes to the nearest 10 minute interval (in the future)
            //takes hours and minutes as arguments
            function correctMin(hrs, mins){

            //convert hours and mins to string format.  autoTimeDrop() takes strings ass arguments
            var strHrs = hrs.toString();
            var strMins = mins.toString();

            //hours to be used to the "dropoff" time select dropdown
            var add30Hrs = hrs;

            // new value that time will be set to and "selected" for dropdown (string format)
            var newmins = "";

            //the following lines of code assess the hrs/mins values, and change the dropdown to the next 10min interval.
            if (strMins.length == 1){
                newmins = "10";
            }
            else{
                switch (strMins[0]){
                    case "1":
                      newmins = "20"; break;
                    case "2":
                      newmins = "30"; break;
                    case "3":
                      newmins = "40"; break;
                    case "4":
                      newmins = "50"; break;
                    case "5":
                      newmins = "00";
                      hrs = hrs +1;
		      add30Hrs = add30Hrs+1; break;
                    }
            }

            //variable that will store the "drop-off" MINS value (add half a hour -- limit for free bike journey)
            var add30Mins = parseInt(newmins) + 30;

            //create string value to pass into function (current time)
            var value1 = hrs + ":" + newmins;

            //if 30mins is added, but total mins goes above 50 mins, we need to increase hour by 1 and take 60 away from mins
            if (add30Mins > 50){
                add30Hrs = add30Hrs + 1;
                add30Mins = add30Mins - 60;
                if (add30Mins==0){
                    add30Mins="00";
                }
                if (add30Hrs==24){
                    add30Hrs="0";
                }
            }

            //create string value to pass into function (collect in 30 mins time)
            var value2 = add30Hrs + ":" + add30Mins;

            //invoke the function to auto-select the 2 time dropdowns (collect time / drop-off time)
            autoTimeDrop(value1, value2);
            }
            //invoke function to change time to a multiple of 10
            correctMin(hrs, mins)

            function updateChart(stationId, stationName){
              // Delete an existing chart if it is present
              if ($("canvas").length){
                $("canvas").remove();
              }

              // Add canvas
              $("div#chart_container").append("<canvas id=\"analytics_chart\" width=\"315px\" height=\"315px\"></canvas>");

              // API call to get JSON
              var base = "/api/station_occupancy_weekly/";
              var url = base + stationId;

              var jsonData = $.ajax({
                url: url,
                dataType: 'json',
              }).done(function (data) {

              // Get data from json
              var mean_available_bikes = JSON.parse(data["mean_available_bikes"]);
              var mean_available_stands = JSON.parse(data["mean_available_stands"]);
              var bikesData = [mean_available_bikes["available_bikes"]["Mon"],
                                                mean_available_bikes["available_bikes"]["Tue"],
                                                mean_available_bikes["available_bikes"]["Wed"],
                                                mean_available_bikes["available_bikes"]["Thurs"],
                                                mean_available_bikes["available_bikes"]["Fri"],
                                                mean_available_bikes["available_bikes"]["Sat"],
                                                mean_available_bikes["available_bikes"]["Sun"]];
              var standsData = [mean_available_stands["available_bike_stands"]["Mon"],
                                                mean_available_stands["available_bike_stands"]["Tue"],
                                                mean_available_stands["available_bike_stands"]["Wed"],
                                                mean_available_stands["available_bike_stands"]["Thurs"],
                                                mean_available_stands["available_bike_stands"]["Fri"],
                                                mean_available_stands["available_bike_stands"]["Sat"],
                                                mean_available_stands["available_bike_stands"]["Sun"]];

              // Create the chart.js data structure
              var chartData = {
                labels: ["Mon", 'Tue', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Mean Bicycle Availability',
                    data: bikesData,
                    backgroundColor: 'rgba(255, 99, 132, 0.3)'
                },

                  {
                    label: 'Mean Stand Availability',
                    data: standsData,
                    backgroundColor: 'rgba(0, 99, 255, 0.3)'
                  }]
              };

              // Get the context of the canvas element we want to select
              var ctx = document.getElementById('analytics_chart').getContext('2d');
              ctx.fillStyle = "black";

              // Instantiate a new chart
              analyticsChart = new Chart(ctx, {
                type:'bar',
                data: chartData,
                options: {
                  responsive: false,
                  scales: {
                    xAxes: [{ stacked: true }],
                    yAxes: [{ stacked: true }]
                  },
                  title: {
                    display: true,
                    text: stationName
                  }
                }
              });
            });
          }

          // Display Weather info
          function weatherInfo(){

            // API call to get JSON
            var url = "/api/current_weather";

            var jsonData = $.ajax({
              url: url,
              dataType: 'json',
            }).done(function (data) {

              // Get weather forcast data from json
              var weatherInfo = data[0]["weather_main"];

              // This function is from coderwall.com - It is converting a datetime to UNIX
              Date.prototype.getUnixTime = function() { return this.getTime()/1000|0 };
              if(!Date.now) Date.now = function() { return new Date(); }
              Date.time = function() { return Date.now().getUnixTime(); }

              // Get sunset and sunrise time data from json
              var sunsetTime = data[0]["sys_sunset"];
              var sunriseTime = data[0]["sys_sunrise"];

              // Convert sunset and sunrise time data to unix time
              var sunsetToUnix = new Date(sunsetTime).getUnixTime();
              var sunriseToUnix = new Date(sunriseTime).getUnixTime();

              var temp = Math.round((data[0]["main_temp"] - 273.15));
              var wind = data[0]["wind_speed"];

              // displaying Temperature
              var displayTemp = ("Today's Temp: " + temp + " ºC");
              //document.getElementById("wind_temp").innerHTML = displayTemp;

              // Displaying Wind Speed
              var displayWind = ("Wind Speed: " + wind + " kph!")
              document.getElementById("wind_temp").innerHTML = displayTemp + "<p>" + displayWind;

              // This switch statement reads the data from the json file and returns
              // the matched value with an image and statement describing the current weather
              switch (weatherInfo) {
                case "Clouds":
                  var clouds = document.createElement("img");
                  clouds.src = "/static/clouds.png";
                  var src = document.getElementById("weather_image");
                  src.appendChild(clouds);
                  var comment = "The Forecast Predicts Cloudy!";
                  document.getElementById("weather_heading").innerHTML = comment;
                  break;

                case "Fog":
                  var fog = document.createElement("img");
                  fog.src = "/static/fog.png";
                  var src = document.getElementById("weather_image");
                  src.appendChild(fog);
                  var comment = "The Forecast Predicts Fog!";
                  document.getElementById("weather_heading").innerHTML = comment;
                  break;

                case "Drizzle":
                  var drizzle = document.createElement("img");
                  drizzle.src = "/static/drizzle.png";
                  var src = document.getElementById("weather_image");
                  src.appendChild(drizzle);
                  var comment = "It Is Drizzling Right Now!";
                  document.getElementById("weather_heading").innerHTML = comment;
                  break;

                case "Mist":
                  var mist = document.createElement("img");
                  mist.src = "/static/mist.png";
                  var src = document.getElementById("weather_image");
                  src.appendChild(mist);
                  var comment = "The Forecast Predicts Mist!";
                  document.getElementById("weather_heading").innerHTML = comment;
                  break;

                case "Rain":
                  var rain = document.createElement("img");
                  rain.src = "/static/rain.png";
                  var src = document.getElementById("weather_image");
                  src.appendChild(rain);
                  var comment = "It Is Raining Right Now!";
                  document.getElementById("weather_heading").innerHTML = comment;
                  break;

                case "Snow":
                  var snow = document.createElement("img");
                  snow.src = "/static/snow.png";
                  var src = document.getElementById("weather_image");
                  src.appendChild(snow);
                  var comment = "It Is Snowing Right Now!";
                  document.getElementById("weather_heading").innerHTML = comment;
                  break;
                
                case "Haze":
                    var haze = document.createElement("img");
                    haze.src = "/static/fog.png";
                    var src = document.getElementById("weather_image");
                    src.appendChild(haze);
                    var comment = "It's fairly hazy out!";
                    document.getElementById("weather_heading").innerHTML = comment;
                      break;
                      

                case "Clear":
                  var currentTime = new Date();
                  var time = currentTime.getTime()/1000;
                  console.log(sunsetToUnix);
                  console.log(time)
                  if (time >= sunsetToUnix && time <= sunriseToUnix){
                    var clear = document.createElement("img");
                    clear.src = "/static/clear_moon.png";
                    var src = document.getElementById("weather_image");
                    src.appendChild(clear);
                    var comment = "Clear Skies Tonight!";
                    document.getElementById("weather_heading").innerHTML = comment;
                    break;
                  }
                  else if (time >= sunriseToUnix && time <= sunsetToUnix) {
                    var clear = document.createElement("img");
                    clear.src = "/static/clear_sun.png";
                    var src = document.getElementById("weather_image");
                    src.appendChild(clear);
                    var comment = "Today Will Be a Sunny Day!";
                    document.getElementById("weather_heading").innerHTML = comment;
                    break;
                  }

                default:
                  var weather = "Sorry, No Weather Today";
                  document.getElementById("weather_heading").innerHTML = weather;
              }
            });
          }

          // When page loads weather function is called
          window.onload=weatherInfo();
