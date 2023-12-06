from generator import Generator

# setup model and input
model_name_hugging_face = "mesolitica/llama-1b-hf-32768-fpf"
input_sentences = "childrenn i was young i want onebyonehihi"
# input_sentences = "When i was young i want C2H2O3"

generator = Generator(model_name_hugging_face)
token_ids = generator.encode(input_sentences)
sentences = generator.decode(token_ids)


print(input_sentences)
print(token_ids)
print(sentences)

# input_sentences = "When i was young i want onebyonehihi"
# token_ids = [10401, 474, 471, 4123, 474, 864, 697, 1609, 650, 2918, 2918]
# sentences = ['aWhen', 'a i', 'a was', 'a young', 'a i', 'a want', 'a one', 'aby', 'aone', 'ahi', 'ahi']