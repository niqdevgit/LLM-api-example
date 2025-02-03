# LLM-api-example

## Usage:  

### notebook
run the notebook code from the root of this repo. 
create venv, for pip

### backend
- Clone this repo
- pip install fastapi uvicorn transformers torch requests
- pip install fastapi[all] 
- See requirements.txt 
- Have your api key on .env
- Run server: uvicorn main:app --reload

### frontend
- cd to frontend folder
- npm install web-vitals
- npm install axios
- npm start

## Note⚠️
The Groq API needed a credit card, so i was not able to fully test this code. It should work, if not make pull request :)