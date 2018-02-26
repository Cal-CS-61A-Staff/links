# CS 61A Link Server

This is a very simple shortlink server used by 61A for links.cs61a.org (as well as a similar internal link server).

It's typically designed to work with a Google Sheet, but you can use any publicly readable CSV file.

## Deploying

We deploy this using Dokku, but anything that can host a simple Flask server should be fine.

## Using with Google Sheets

1. Create a workbook with at least one sheet with headers `Shortlink`, `URL`, and `Creator`. Anything in other columns will be ignored. Make the sheet readable to anyone with a link.
2. Find the workbook ID: `https://docs.google.com/spreadsheets/d/$WORKBOOK_ID/edit`.
3. Set the `BASE_URL` env variable to `https://docs.google.com/spreadsheets/u/1/d/$WORKBOOK_ID/export?format=csv&id=1-$WORKBOOK_ID&gid=`.
4. For each sheet you want to use, find the sheet ID, which is the number after the `#` when the sheet is open.
5. Add all sheet IDs separated by commas to the `SHEETS` env variable.

## Important Things to Note

- When using Google Sheets as described above, the document will be world readable, so avoid putting sensitive information in the links themselves.
- Links do not refresh automatically. You need to go to `yourdomain.com/_refresh` to have the server re-fetch the sheets.
- All links will be at `yourdomain.com/<shortlink>`. You can see a preview of the link and the listed creator at `yourdomain.com/preview/<shortlink>`.
