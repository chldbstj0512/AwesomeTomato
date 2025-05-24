from transformers import AutoModel, AutoTokenizer

model_id = "jhgan/ko-sbert-nli"
save_dir = "/home/ys0660/25-1/Demo/model"

# 모델과 토크나이저 다운로드 및 저장
model = AutoModel.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)

model.save_pretrained(save_dir)
tokenizer.save_pretrained(save_dir)
