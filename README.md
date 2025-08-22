# LangChain-Trip-Planner-Agent-Demo

Using OpenInference and OpenTelemetry to send traces from your LangChain agent app to Signoz

## Getting Started
First, install all the necessary dependencies for the backend:

*Optional*
Create Python virtual env:
```bash
python -m venv myenv && \
source myenv/bin/activate
```
Then:
```bash
pip install -r requirements.txt
```

Install all the necessary dependencies for the frontend:
```bash
cd frontend && \
npm install
```

Next create a .env file with the following(in root directory):
```bash
OPENAI_API_KEY=<your-openai-api-key>
SIGNOZ_INGESTION_KEY=<your-signoz-ingestion-key>
```

Run the demo apis backend:
```bash
uvicorn apis:app --reload
```

Run the fastapi backend:
```bash
uvicorn main:app --reload --port 8001
```

Run the frontend:
```bash
cd frontend && \
npm start
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result and interact with the application.

## After using the application, you should be able to view traces in your SigNoz Cloud platform:

### Traces

<img width="1112" height="104" alt="langchain-trace" src="https://github.com/user-attachments/assets/953817ad-7940-4a60-9286-c39937d9e67e" />
<img width="1443" height="760" alt="langchain-detailed-trace" src="https://github.com/user-attachments/assets/2ad1cc2c-67de-4f74-8558-8d2587158b55" />


## You can also create custom dashboards using these traces and span attributes:
### Import Dashboard
Go to the **Dashboards** tab in SigNoz.

Click on **+ New Dashboard**

Go to **Import JSON**
<img width="1510" height="788" alt="dashboard_import" src="https://github.com/user-attachments/assets/8ea7f75f-fee6-4cca-8dd8-1f0a76096ca2" />

Import the **langchain-dashboard.json** file from the repo.

Your dashboard should now be imported and look something like this:
<img width="1450" height="761" alt="Screenshot 2025-08-21 at 11 22 12 AM" src="https://github.com/user-attachments/assets/8c84888e-10e5-4b28-ac2a-5673146e883c" />
