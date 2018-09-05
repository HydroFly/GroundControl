# HydroFlyGCS

Under development

## Instructions

To launch the console application, enter the following on a Unix/Linux command line:

```python
python3 main.py
```

## Important

Turn off QuickEdit in your terminal's settings. If QuickEdit is enabled, selecting any text temporarily freezes script execution, which could cause the user to inadvertantly freeze communication with the rocket.

## Using the app

In the center of the screen will be the rocket's telemetry. At the bottom, there is a status bar, command line, and above are results from commands to the GCS application.

Commands from the GCS command line are used to send commands to the rocket and to affect logging behavior of the Ground Control application.

For example, entering `launch` in the command line will simulate a rocket launch by increasing height at a constant rate.

## Logging

Logs are stored by default in a Logs folder in the same directory as the cloned project.

A log entry can be made anywhere in the application by calling `self.app.logger.log(message, logfile)`