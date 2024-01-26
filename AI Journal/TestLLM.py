import requests
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration

def llm_model(image):
    processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
    model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b")

    img_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg'
    raw_image = image

    question = "how many dogs are in the picture?"
    inputs = processor(raw_image, question, return_tensors="pt")

    out = model.generate(**inputs)
    print(processor.decode(out[0], skip_special_tokens=True))

if __name__ == '__main__':
    url = 'https://media.newyorker.com/cartoons/63dc6847be24a6a76d90eb99/master/w_1160,c_limit/230213_a26611_838.jpg'
    image = Image.open(requests.get(url, stream=True).raw).convert('RGB')
    image.show()
    llm_model(image)