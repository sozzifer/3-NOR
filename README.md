gcloud builds submit --tag gcr.io/stat4002/exploring-data  --project=stat4002

gcloud run deploy --image gcr.io/stat4002/exploring-data --platform managed  --project=stat4002 --allow-unauthenticated