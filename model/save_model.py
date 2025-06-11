from transformers import AutoModel, AutoTokenizer
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("jhgan/ko-sbert-nli")
model.save("/home/ys0660/25-1/Demo/model/jhgan-ko-sbert")
