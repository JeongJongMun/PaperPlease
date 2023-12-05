from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os, base64

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY", None) 

llm = ChatOpenAI(temperature=0,
                 model_name="gpt-4-vision-preview",
                 api_key=OPEN_AI_API_KEY,
                 max_tokens=256)

# 이미지를 base64로 인코딩하는 함수
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def get_all_image_url(url):
    # 경로 안의 모든 이미지 경로 가져오기
    # image_dir = "./images"
    img_path_list = []
    possible_img_extension = ['.jpg', '.jpeg', '.JPG', '.bmp', '.png'] # 이미지 확장자들

    for (root, dirs, files) in os.walk(url):
        if len(files) > 0:
            for file_name in files:
                if os.path.splitext(file_name)[1] in possible_img_extension:
                    img_path = root + '/' + file_name
                    
                    # 경로에서 \를 모두 /로 바꿔줘야함
                    img_path = img_path.replace('\\', '/') # \는 \\로 나타내야함 
                    img_path_list.append(encode_image(img_path)) # llm에 넣기 위해 encode까지 수행
    
    return img_path_list

def get_all_content(img_path_list):
    contents = []
    for num, i in enumerate(img_path_list):
        result = llm.invoke(
            [
                HumanMessage(
                    content=[
                        {"type": "text", "text": "What is this image showing"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{i}"
                            },
                        }
                    ]
                ),
            ]
        )

        contents.append(result.content)
        
        return contents