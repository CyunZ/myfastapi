from fastapi import APIRouter,Request
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from loguru import logger

AIChatRouter = APIRouter(prefix='/aichat',tags=['聊天机器人'])

model_name = "F:/aaaa/MyAI/Qwen/Qwen3-0.6B"
tokenizer = None
model = None
# load the tokenizer and the model
def loadAIModel():
    global tokenizer,model
    logger.info('开始加载模型')
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto"
    )
    logger.info('加载模型结束')

class ChatInfo(BaseModel):
    content:str = ''

@AIChatRouter.post('/chat')
async def chat(request:Request, chatInfo : ChatInfo):
    
    if chatInfo.content == '':
        return {'code':1,'msg':'消息内容不能为空'}
        

    messages = [
        {"role": "user", "content": chatInfo.content}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=True # Switches between thinking and non-thinking modes. Default is True.
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    # conduct text completion
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=32768
    )
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

    # parsing thinking content
    try:
        # rindex finding 151668 (</think>)
        index = len(output_ids) - output_ids[::-1].index(151668)
    except ValueError:
        index = 0

    thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
    content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")


    return  {'code':0,'thinkContent':thinking_content,'content':content}