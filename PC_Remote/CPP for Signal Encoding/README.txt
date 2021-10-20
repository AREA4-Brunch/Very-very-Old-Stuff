FAILURE, 
It happens that generated hex codes and IR blaster signals are not equivalent to the reciever.

Program can be used to generate IR blaster signals, but you have to identify each signal
on reciever and hardcode the value it picks up instead of assuming it's the same as provided integer as intended.
Kinda acts as random IR signal generator based on seed you provide :(

========================================================================
Sources for encoding the IR in the Android App:

http://www.remotecentral.com/features/irdisp2.htm

https://rileymacdonald.ca/2017/10/14/tutorial-how-to-write-an-android-app-widget-to-control-your-television/

https://stackoverflow.com/questions/20244337/consumerirmanage-hasiremitter-always-returns-false-api-19/25518468#25518468

https://stackoverflow.com/questions/25771333/ir-hex-to-raw-ir-code-conversion
