import os
import json
import xgboost
import pandas as pd
import pickle as pkl
from utils import extract_model

# download model file from S3 into /tmp folder
extract_model(os.environ['MODEL_S3_URI'], '/tmp')
# LOAD MODEL
model = pkl.load(open('/tmp/xgboost-model', 'rb'))


def handler(event, context):
    # TRANSFORM DATA
    body = json.loads(event['body'])
    df = pd.DataFrame(body, index=[0])
    data = xgboost.DMatrix(df.values)

    # PREDICT
    prediction = model.predict(data)

    return {
        'prediction': str(prediction)
    }
