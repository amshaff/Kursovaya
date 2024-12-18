from aiohttp import ClientSession, TCPConnector, ClientError
from json import dumps


async def get_token(auth_token) -> str:
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': '3955780d-5882-4a6d-8e49-6f6bbab9b420',
        'Authorization': f'Basic {auth_token}'
    }

    payload={
        'scope': 'GIGACHAT_API_PERS'
    }
    
    try:
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            async with session.post(url, data=payload, headers=headers) as response:
                response.raise_for_status()  # Вызывает исключение для статусов 4xx и 5xx
                
                data = await response.json()
                return data.get("access_token")
            
    except ClientError as e:
        print(f"Ошибка клиента: {e}")
        raise  # Повторно выбрасываем исключение, если нужно
    
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        raise  # Повторно выбрасываем исключение, если нужно
            

async def send_to_rephrase(text, auth_token):
    
    url = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'
    
    headers = {
        'Authorization': f'Bearer {await get_token(auth_token)}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    
    data = {
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": text + "\nПерефразируй это и пришли в ответ только перефразированный текст. ",
            }
        ],
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1,
        "update_interval": 0
    }
    
    try:
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            async with session.post(url, headers=headers, data=dumps(data)) as response:
                response.raise_for_status()
                return await response.json()

    except ClientError as e:
        print(f"Ошибка клиента: {e}")
        raise  # Повторно выбрасываем исключение, если нужно
    
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        raise  # Повторно выбрасываем исключение, если нужно
