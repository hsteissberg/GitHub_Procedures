# Preparing a table of GitHub issues

## Preliminary steps to be performed only once

* Generate a personal access token via the GitHub site
	* [Creating a personal access token - GitHub Docs](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token)
* Install the “Excel to Markdown Table” extension in Visual Studio code

## Download the issues list from GitHub
* Open a command prompt / terminal, e.g., iTerm on MacOS
* Change to the directory where you want to store the JSON file that will be created in the next step. 
    * Use the command “cd” to change directories and “pwd” to print the path of the current working directory.
* Run the following command, including the access token:
    * curl -u hsteissberg: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 "https://api.github.com/repos/LimnoTech/FRESCO/issues?per_page=100&state=all" > issues.json

## Generate the issues table using Excel for Windows and Power Query

* Create a new spreadsheet or open an existing file
* Select the Data tab
* Click the “Get Data” button
* Select “From File” and then “From JSON”
* Click the “To Table” button
* Accept the default settings and click OK
* At the top of the column, select the column expansion button [image:18895179-FDEA-4F7E-BEE6-99199000A194-97102-00015492898B9B36/9D4A91C4-C8F5-45FF-BDF7-7B14CFF0A8B4.png] to expand the column
* The following fields need to be included in the Issues spreadsheet:
    * number
    * title
    * user.login
    * labels.name
    * state
    * milestone.title
    * created_at
* Select the number, title, user, labels, state, milestone, and created_at items
* Expand the “user” column, select “login”, and click OK.
* Expand the “labels” column and expand the column. Select “Expand to Rows”. Then select “name”, and click OK.
* Expand the “milestone” column, select “title”, and click OK.
* Select the File tab and click “Close and Load” to load the data into the spreadsheet.
* Save the spreadsheet!

## Convert the spreadsheet table to a Markdown table - one for bugs and one for non-bugs

### Bugs

1. Filter the “labels” column, and select “bugs.”
2. Select all of the data in the Excel table
3. Copy the data
4. Open a new file in Visual Studio Code
5. Save the file as a Markdown file. This is important, as it affects the next step.
6. Paste the data into the data into the Markdown file using the keyboard shortcut for the Excel to Markdown Table extension:
    * On Windows: Shift—Alt-V
    * On MacOs: Shift-Option-V
7. Save the Markdown file.

### Non-bugs

* Repeat the above process, but select non-bug issues:
    * Select all fields
    * Deselect “bugs”
    * Follow steps 2 - 7 above.

