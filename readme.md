# remotive-contract-jobs

[https://remotive.com/](https://remotive.com/) has a job board for remote jobs but, the filtering on this page isn't great.

Specifically, I wanted to find only jobs open for contractors and freelancers. So this scraper pulls down the most recent page and filters out the roles that are contract.

## running it

Just run `run.sh`. The scraper is configured to store all responses in a local cache to avoid loading the remotive.com if you adjust the scraping content.

Output will be placed in `output/jobs.csv`.

## usage

I imported the export into Airtable where I can manage the walkthrough status.

![Example of putting the data in Airtable](./example.png)

## next steps

Building an upload function to update the Airtable table with new entries and notify myself, automating the process.