from aws_cdk import App
from .lambda_function.stack import IngestionLambdaStack


app = App()

IngestionLambdaStack(app, "LambdaIngestionStack", image_name="budget-guard")

app.synth()
