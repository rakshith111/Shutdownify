# Shutdownify

## This is an app developed for windows .You can time your pc to shutdown by setting the timer which takes in 3 entries for Hours, Minutes and Seconds

## Features

- Shuts the pc down after the given time

- If you want to cancel the set timer it can be done by clicking on the cancel button
- Once the timer is set it can be extended 
  - Two modes are available
    - Direct mode : Shuts down the pc for the chosen time immediately  
    - Manual mode : Adds the selected time to the input fields
- Turn Off your(Screen timeout) monitor earlier in case you might be away for a long time. (The previous value will reset before the pc shuts down)
- Supports Dark Blue theme

<h3><details>
  <summary>BETA features </summary>
  <h4>Flask webserver which runs locally on your pc and displays an ip and Use the app to remotely control the state of your pc</h4><br>
-> install requirements.txt<br>
-> run the apihandler.py<br>
-> Open the app and input ip and press check <br>
-> If status is green you're good to go else recheck ip <br>

</details></h3>

## Upcoming features
- Full Android support
  - A security feature
  - Support for simultaneous shutting down of many pc's from app
  - Add names for pcs
 
## Screenshots
![image](https://user-images.githubusercontent.com/36219488/197401333-6b99cd61-6f7a-488d-8a56-e3170a064cb4.png)
![image](https://user-images.githubusercontent.com/36219488/197401370-bc7d665d-2a0b-41e8-80dd-98070b20bd43.png)
![image](https://user-images.githubusercontent.com/36219488/197401393-1094f002-105e-4b57-88d0-0ad0cc6aa699.png)
![image](https://user-images.githubusercontent.com/36219488/197401421-a6267bd2-4514-4f08-bd7c-f0d07ec61d3e.png)

### [Releases](https://github.com/rakshith111/Shutdown-timer/releases)

<h4><details>
  <summary>Build it by yourself </summary>
  <code>pip install pyinstaller </code><br>
  Then run <br>
  <code>pyinstaller --onefile -w main.py -i shutdown.ico</code> <br>

</details></h4>

## WHY? 
  I was just tooo frustrated that I didnt have a shutdown timer and couldnt trust the one's I found online so i built one<br>
  Also wanted to see how far i can strech this one simple concept by integrating many features and extend its use for many people
  


