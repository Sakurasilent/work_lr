"""
多模态演示es查询服务
不涉及es的创建
本地测试
"""
from functools import lru_cache
from transformers import BertTokenizer, ErnieModel,ErnieForMaskedLM
from elasticsearch import  Elasticsearch
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger

logger.add("es_search_{time:YYYY-MM-DD}.log", rotation="00:00", enqueue=True)
app = FastAPI()

es = Elasticsearch('http://127.0.0.1:9200',
                #    ca_certs=False,
                   verify_certs=False
                   )

@lru_cache()# 同一个模型避免重复家在
def vec_model(model_path):
    """获取词向量模型与分词器
    Args:
        model_path (_type_): 模型路径 
                             ernie-3.0-base-zh 模型地址
    Returns:
        model: 嵌入模型
        tokenizer:分词分词器
    """
    logger.info("model loadding")
    tokenizer = BertTokenizer.from_pretrained(model_path)
    model = ErnieModel.from_pretrained(model_path)
    model.eval()
    logger.info("model loadding end")
    return model, tokenizer

from esconfig import MODEL_PATH
model,tokenzier = vec_model(MODEL_PATH)

def text2vec(text, model=None, tokenizer=None, dtype='list', flatten=True):
    """文本转换为向量
    Args:
        text (_type_): 用户问题
        model (_type_, optional): 嵌入模型.
        tokenizer (_type_, optional): 分词器
        dtype (str, optional): 返回类型 Defaults to 'list'.
        flatten (bool, optional): 向量拉平. Defaults to True.

    Returns:
        _type_: _description_
    """
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    vec = output[1]
    if flatten:
        vec = vec.flatten()
    if dtype == 'list':
        vec = vec.tolist()
    return vec

def get_query(query_vector):
    """实时拼接 查询 vector

    Args:
        query_vector (_type_): _description_
    """
    script_query={
    "query":{
        "script_score":{
            "query":{"match_all":{}}, #可替换具体的查询
            "script":{
                "source": "cosineSimilarity(params.query_vector, 'prompt_vector') + 1.0",
                "params":{
                    "query_vector":query_vector
                }
            }
        }
    }
}
    return script_query
from esconfig import HOLD_VALUE
from esconfig import INDEX_NAME

@app.post("/api/isDemoCase")
async def isDemoCase(request: Request):
    """es通过question进行查询
    如果最高的相似度超过 阀值 返回 true 否则false

    Args:
        index_name (_type_): 索引名
        question (_type_): 句子嵌入
    Returns:
        _type_: _description_
    """

    json_post_question=await request.json()
    question=json_post_question.get("question","")
    if not question or not isinstance(question, str):
        content = {"status": "error", "message": "question 不能为空或格式不正确"}
        return JSONResponse(content=content, status_code=400)
    try:
        response = es.search(index=INDEX_NAME,
                            body=get_query(text2vec(
                                text=question,
                                model=model,
                                tokenizer=tokenzier)))

        if response["hits"]["hits"][0]["_score"]>HOLD_VALUE:
            content={
                "status":"success",
                "isDemoCase":True
            }
            return JSONResponse(content=content)
        
        else:
            content={
                "status":"success",
                "isDemoCase":False
            }
            return JSONResponse(content=content)
       
    except Exception as e:
        logger.error(e)
        content = {"status": "error", "message": "es查询失败"}
        return JSONResponse(content=content, status_code=401)

@app.post("/api/getMEdiaInfoAndSuggentions")
async def getMEdiaInfoAndSuggentions(request:Request):
    """
    获取演示case存储地址与类型，并且推荐相关问题
    Args:
        question (_type_): _description_
    """
    logger.info("getMEdiaInfoAndSuggentions...")
    json_post_question = await request.json()
    question=json_post_question.get("question","")
    
    if not question or not isinstance(question, str):
        content = {"status": "error", "message": "question 不能为空或格式不正确"}
        return JSONResponse(content=content, status_code=400)
    
    try:
        response = es.search(index=INDEX_NAME,body=get_query(text2vec(text=question,model=model,tokenizer=tokenzier)))
        if response["hits"]["hits"] and response["hits"]["hits"][0]["_score"]>HOLD_VALUE:
            content={
                "status":"success",
                "media":{
                    "url":response["hits"]["hits"][0]["_source"]["url"],
                    "type":response["hits"]["hits"][0]["_source"]["media_type"]
                },
                "suggestions":response["hits"]["hits"][1]["_source"]["suggestions"]
            }
            return JSONResponse(content=content)
        else:
            content={
                "status":"error",
                "message":"es没有查询结构,不是演示case"
            }
            return JSONResponse(content=content)
    except Exception as e:
        logger.error(e)
        return JSONResponse(content={"status": "error", "message": "es查询失败"},
                            status_code=401)
    
if __name__=="__main__":

    # question="这只是一个测试"


    # index_name="multi_modal_search"
    # response = isDemoCase(question=question,
    #               index_name=index_name)
    # print(response)
    # a,b,c=getMEdiaInfoAndSuggentions(question)
    # print(a,b,c)
    # print(response)
    # print(len(response["hits"]["hits"]))
    # print("-----")
    # print(response["hits"]["hits"])

    pass



