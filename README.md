<h1 style="text-align: center;">How Conservative and Liberal News Media See Current Economic Condition: CNN vs. Fox News</h1>

### Introduction 
Economic conditions are not only shaped by objective indicators such as inflation, employment, or growth, but also by how these indicators are interpreted and communcated to the public. News media play a central role in shaping public perceptions of economy, influencing consumer confidence and politiccal attitutes. This report examines how liberal and conservative news media differ in their portrayal of the U.S. economic situations, focusing on a comparative case study of CNN and Fox News. CNN is commonly associated with a liberal-leaning audience, while Fox News is widely regarded as representing conservative viewpoints. 

The economic news articles were scraped direclty from CNN and Fox News websites (around 500 articles for each are used for analysis). Each article processed using **AWS Bedrock Nova** for automatic categorization and sentiment analysis, classifying it by topic (e.g., inflation, taxes, employment, housing, energy, financial markets) and sentiment (positive or negative). The data were stored in **AWS S3**, and, as an additional feature, a Streamlit dashboard was created to explore topic-level distribution and overall economic sentiment. Querying and processing for the dashboard were facilitated through **AWS Athena** and **AWS Lambda functions**. 

---

### Data source: Web Scarping

![Description of figure](path/to/figure.png)
---

### Methods

We processed a collection of news articles for economic relevance and sentiment using AWS Bedrock with the Nova Micro foundation model. 

1. Filtering for Economic Relavance
Each article title was first analyzed to determine if it was related to economic topics to make sure each artile is about economic related subject.   

---

### Results

---

### Cost