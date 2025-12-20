# Steps to reproduce
 0. Set up AWS credentials, download python libraries, install streamlit
 1. Set up an S3 bucket
 2. Run the scraping scripts
 3. Run the athena setup script
 4. Deploy the lambda function, invoke it
 5. Edit streamlit_dash.py so the data sources point to your bucket
 6. Run the streamlit app, to explore the results interactively!
