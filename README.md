# Henri Augusto - Fresh-News Challenge

This is [Henri Augusto's](https://github.com/HenriAugusto) submission for the [Thoughtful Automation's fresh-news challenge](https://thoughtfulautomation.notion.site/RPA-Challenge-Fresh-news-fa3f504bb7824e1aa9c083906ca1bba7).

# Running in Robocloud

I've managed to run the code from tthe Robocloud successfully in two different machines using Self-hosted workers. Yet all of the Cloudworkers are getting errors while trying to call Selenium's `open_browser`.

```
Exception: WebDriverException
Message: unknown error: Chrome failed to start: crashed.
  (unknown error: DevToolsActivePort file doesn't exist)
  (The process started from chrome location /home/worker/.cache/selenium/chrome/linux64/116.0.5845.96/chrome is no longer running, so ChromeDriver is assuming that Chrome has crashed.)
  ```

  You can try to run the robot in a self-hosted machine  or through VS code (see next section for VS Code)

# How to test in VS Code

Open the command palette and run `Robocorp: Debug Robot`. It should give you the following options:

    1. <No Work item as input>
    2. run-1 - Output

Choose the second option so it runs with the preconfigured test itens. (`devdata\work-items-out\run-1\work-items.json`)

# Developer Remarks

## Error Recovery

All results in the CSV file are written and loaded by the `DataManager` class.
Our main task checks for every results if it was previously written to the file before writing, i.e. ignores any result processed in previous executions

## Logging

A `Log` class is provided which acts as an interface. Changing, removing or adding logging strategies can be done without changing the client code.

## Locators convention

- Locators that are only used in one place are defined in the function they're used.
- Locators used more than one place are defined as class variables.