Usage:

1. Before running the program, you will need to download the Cloud Health reports from the Monday board for the client
or clients whose resources you will be validating. Please check the reports for extraneous information - these reports
can NOT have any extra columns like "Notes" or other added comments (background colors are irrelevant, however). Once
the Cloud Health reports have been checked and/or tidied up, open File Explorer and add the Cloud Health reports
to the "cloudhealth" directory within the program's root directory (~/2wchval_vx.x.x/cloudhealth).

2. Right-click the Windows Start Menu icon and open the Terminal as an Administrator.

3. Navigate to the program's directory using the `cd` command.

4. Run the program by typing the file name of the executable (i.e. 2wchval_vx.x.x.exe - auto-complete by using the
`Tab` key is your friend here) and pressing Enter.

5. Interaction with the program happens in the GUI windows, not the console. It may take several seconds for the
initial GUI window to appear.

6. Be sure to double-check the Cloud Health report date before you enter it in the Date Entry window. Enter a four-digit
year, a two-digit month, and a two-digit day (ex. 2023, 04, 24 for April 24th, 2023). If you enter the date
incorrectly, the reports will not run properly.

7. Select the client or clients for whom you want to run the reports by left-clicking their name(s) in the Client
Selection window. No need to hold the Ctrl key when selecting multiple clients.

8. Only run reports for VNS Health if you know you have access to the MSO, MSO-Test, and Regulated accounts.

9. The Excel reports will be created in the "outputs" directory.