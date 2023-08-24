# Henri Augusto - Fresh-News Challenge

This is [Henri Augusto's](https://github.com/HenriAugusto) submission for the [Thoughtful Automation's fresh-news challenge](https://thoughtfulautomation.notion.site/RPA-Challenge-Fresh-news-fa3f504bb7824e1aa9c083906ca1bba7).

# How to test in VS Code

Open the command palette and run `Robocorp: Debug Robot`. It should give you the following options:

    1. <No Work item as input>
    2. run-1 - Output

Choose the second option so it runs with the preconfigured test itens. (`devdata\work-items-out\run-1\work-items.json`)

# Locators convention

- Locators that are only used in one place are defined in the function they're used.
- Locators used more than one place are defined as class variables.