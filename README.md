<h1 style="text-align: center;">How Conservative and Liberal News Media See Current Economic Condition: CNN vs. Fox News</h1>

### Introduction 
Economic conditions are not only shaped by objective indicators such as inflation, employment, or growth, but also by how these indicators are interpreted and communcated to the public. News media play a central role in shaping public perceptions of economy, influencing consumer confidence and politiccal attitutes. This report examines how liberal and conservative news media differ in their portrayal of the U.S. economic situations, focusing on a comparative case study of CNN and Fox News. CNN is commonly associated with a liberal-leaning audience, while Fox News is widely regarded as representing conservative viewpoints. 

The economic news articles were scraped direclty from CNN and Fox News websites . Each article processed using **AWS Bedrock Nova** for automatic categorization and sentiment analysis, classifying it by topic (e.g., inflation, taxes, employment, housing, energy, financial markets) and sentiment (positive or negative). The data were stored in **AWS S3**, and, as an additional feature, a Streamlit dashboard was created to explore topic-level distribution and overall economic sentiment. Querying and processing for the dashboard were facilitated through **AWS Athena** and **AWS Lambda functions**. 

---

### Data source: Web Scraping
We scraped CNN and Fox News using a two-stage web-scraping process: first, we collected news links using the websites' search engines, and then we scraped the full articles using these links. We used two main Python Libraries for this process, Selemium and BeautifulSoup. This section explain the scraping logic for each news outlet separately. 

#### 1. CNN Article Scraping  
What makes it possible to scrape economic-related articles from CNN is its dynamic search link. By searching for the keyword 'economy' on CNN's search engine, the following link appears:
https://edition.cnn.com/search?q=economy&from=0&size=10&page=1&sort=newest&types=article&section=
Key details: 
    • `q=economy` - search term 
    • `size=10` - up to 10 results per page 
    • `sort=newest` - most recent articles 
    • `types=article` - excluding video, galleries 

Using 52 keywords, up to 100 article links and headlines per keyword were scraped. Since CNN’s search engine relies on JavaScript, the scraping was performed using the Selenium package.
![](C:/Users/Enkhsaikhan/Data-engineering-scrap/figs_report/pic1.png)
![](C:/Users/Enkhsaikhan/Data-engineering-scrap/figs_report/pic2.png)

After collecting the news links, the full articles were scraped using BeautifulSoup.
![](C:/Users/Enkhsaikhan/Data-engineering-scrap/figs_report/pic3.png)

#### 2. Fox News
The same method is applied to 

---

### Methods

We processed a collection of news articles for economic relevance and sentiment using AWS Bedrock with the Nova Micro foundation model. 

1. Filtering for Economic Relavance  
Each article title was first analyzed to determine if it was related to economic topics to make sure each artile is about economic related subject.   

2. Topic Categorization  
Filtered articles are further sorted into more specific subjects such as inflation, crypto, trade, or markets. This step is guided by the article content and keyword-based or model-based categorization. 

3. Sentiment Analysis  
For each filtered article, the get_sentiment(text) function uses the same AWS Nova Micro model to classify the article’s tone as POSITIVE or NEGATIVE. The system prompt instructs the model to assess sentiment in relation to the U.S. economy, though the articles themselves may originate from any source. Sentiment results are mapped numerically (1 = positive, 0 = negative) and stored alongside article metadata.

---

### Results

---

### Cost