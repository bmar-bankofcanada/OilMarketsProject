from data_transformer import LabeledOilDatasets
from train_relevance_model import RelevanceModel
from categorize_raw_data import Categorizer

def finetune(model_path,model_name):
    oil_dataset = LabeledOilDatasets(file_path="data/500_manually_labeled.csv")
    data = oil_dataset.create_relevant_dataset()
    #Best production: "roberta-base" "bert-base-uncased" "distilbert-base-uncased" "microsoft/deberta-v3-base"
    model = RelevanceModel(
        transformer_model_name=model_path,
        dataset=data,
        id_label={0: "RELEVANT", 1: "NOT RELEVANT"},
        label_to_id={"RELEVANT": 0,"NOT RELEVANT":1}
    )
    model.fine_tune(output_dir=f"outputs/{model_name}",epochs=3)
    
if __name__=="__main__":
    is_finetune = False
    if is_finetune:
        finetune("google/electra-base-discriminator","electra-base")
    else:
        model = "models/Econ_RoBERTa-base"
        relevancy = Categorizer(model)
        test_categories = [
            {'text':'The oil supply is starting to degrade!','label':'relevant' },
            {'text':'Today Lisa Laflamme was let go by Bell.','label':'not relevant' },
            {'text':'What do you mean we want some natural gas?','label':'not relevant' },
            {'text':'The supply is lacking in Germany, because of the tensions with Russia.','label':'relevant' },
            {'text':'The need for Natural Gas has increased in Toronto.','label':'not relevant' },
            {'text':'The lack of demand in China has reduced the price of the barrel','label':'relevant' }
        ]
        for test in test_categories:
            result = relevancy.classify(test['text'])
            if result[0]['label'] == test['label'].upper():
                print(f"Correctly identify with a confidence level of {result[0]['score']}")
            else:
                print(f"Incorrectly identify with a confidence level of {result[0]['score']}")
        