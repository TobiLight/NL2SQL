## NL2SQL: Natural Language to SQL Translator
This project aims to develop an AI-powered backend API that translates natural language descriptions into valid SQL queries.

### Description
Writing complex SQL queries can be challenging, especially for non-technical users. NL2SQL aims to bridge this gap by providing an easy-to-use API that allows users to express their data analysis needs in natural language and receive the corresponding SQL query. This can improve data accessibility for various user groups and streamline data analysis workflows.


### Project Goals
- **Democratize Data Access**: Empower non-technical users to access and analyze data without learning SQL.
- **Enhance Efficiency**: Improve data analysis workflow for technical users by simplifying query formulation.
- **Reduce Errors**: Eliminate errors associated with manual SQL coding.


### Features
- Translate natural language questions to valid SQL statements.
- Currently supports ONLY English language input.
- Handles complex queries, supports aggregation functions


### Technical Approach
- **Natural Language Processing (NLP)**: Google Gemini is utilized for its advanced NLP capabilities to understand the intent and meaning behind user queries expressed in natural language.
- **Data Acquisition & Preprocessing**: A curated dataset of natural language queries paired with corresponding SQL translations is used to train and refine the agent.
- **SQL Generation**: The agent translates the user's natural language query into a well-structured and functional SQL statement suitable for data retrieval.


### Challenges
- Limited training data availability
- Handling complex natural language queries
- Ensuring accuracy and efficiency of the NLP model


### Project installation & Startup
1. Create a virtual environment
	- ```python3 -m venv .env``` 
2. Activate the virtual environment
	- ```source venv/bat/activate``` - Windows/Linux
3. Install project dependencies using ```pip3 install -r requirements.txt```
4. Set environment variables in an .env file with these:
	- JWT_SECRET_KEY
	- JWT_ALGORITHM
	- JWT_ACCESS_TOKEN_EXPIRE_MINUTES
	- GOOGLE_API_KEY
5. To start the application, run ```python3 -m app.main```


### Technologies Used
- **[Google Gemini](https://ai.google.dev/docs/gemini_api_overview)** - Generative AI model
- **[FastAPI](https://fastapi.tiangolo.com)** - Web server
- **[Prisma ORM](https://prisma-client-py.readthedocs.io/en/stable/)** - For querying data
- **[PostgreSQL]()** - Data Storage


### Team
Oluwatobiloba Light - [Twitter/X](https://x.com/0xTobii)