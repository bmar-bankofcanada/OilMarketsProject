from transformers import pipeline

class Categorizer():

    def __init__(self,model) -> None:
        self.classifier = pipeline("sentiment-analysis",model=model)

    def classify(self,text):
        return self.classifier(text)