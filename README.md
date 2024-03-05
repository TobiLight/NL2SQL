## NL2SQL: Natural Language to SQL Translator
This repository implements an NL2SQL system that translates natural language questions in English into corresponding SQL queries. This allows users to query relational databases using intuitive language, improving accessibility and reducing the need for manual SQL expertise.

### Features
- Translate natural language questions to valid SQL statements.
- Currently supports English language input.
- Handles complex queries, supports aggregation functions


### Technologies
- **[Google Gemini](https://ai.google.dev/docs/gemini_api_overview)** - Generative AI model
- **[FastAPI](https://fastapi.tiangolo.com)** - Web server
- **[Prisma ORM](https://prisma-client-py.readthedocs.io/en/stable/)** - For querying data easily
- **[PostgreSQL]()** - Data Storage