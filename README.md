# Henri Augusto - Fresh-News Challenge

This is [Henri Augusto's](https://github.com/HenriAugusto) submission for the [Thoughtful Automation's fresh-news challenge](https://thoughtfulautomation.notion.site/RPA-Challenge-Fresh-news-fa3f504bb7824e1aa9c083906ca1bba7).

# Running with Robocloud's Cloud Workers

This sections descibres aspects that different when executing the robot in Robocloud's Cloud Workers vs Self-Hosted Workers/Locally.

At first I've had success running the robot i a couple of Self-Hosted workers but couldn't manage to run the robot in any Cloud Worker.

I would get errors such as:

```
Message: unknown error: Chrome failed to start: exited abnormally.
2023-08-31 19:34:08:    (unknown error: DevToolsActivePort file doesn't exist)
2023-08-31 19:34:08:    (The process started from chrome location /home/worker/.cache/selenium/chrome/linux64/116.0.5845.96/chrome is no longer running, so ChromeDriver is assuming that Chrome has crashed.)
```

I've pinpointed the error to `RPA.Browser.Selenium`'s `open_browser()` method.

After a lot of trial and error, experimenting with different parameters for `open_browser()` and also different chromedriver versions in `conda.yaml`, I've managed to get the robot running in the Cloud Workers by exchanging `open_browser()` for `open_chrome_browser()` in `BrowserInitializer`.

Aftwerwards i've start receiving errors like this:

```
'utf-8' codec can't decode byte 0x92 in position 292: invalid start byte
```

Which were solved by specifying which encoding to use when reading and writing to the CSV in the `DataManager` class. The offending characters were and U+2018 (‘) and U+2019 (’)

This  robot would run sucessfully on

- Cloud Workers (Preview)
- Cloud Workers (Ubuntu 18.04 Legacy)

but not on

- Cloud Workers
- Cloud Workers (early access)

Cecause in those 2 the following error appears while interacting with the search button:

```
element not interactable
```


Further investigation is required.

I've already tried adding `python-chromedriver-binary=114.0.5735.16.0` to `conda.yaml` in hope it's a versioning issue but with no success.

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