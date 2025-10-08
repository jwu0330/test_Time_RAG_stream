"""
Function Tools 定義
用於 OpenAI Responses API 的 function/tool call
"""

# 情境分類工具定義
CLASSIFY_SCENARIO_TOOL = {
    "type": "function",
    "function": {
        "name": "classify_scenario",
        "description": "根據用戶問題和歷史對話，判定當前情境編號（1-24）。僅返回情境編號，不包含任何解釋或額外文字。",
        "parameters": {
            "type": "object",
            "properties": {
                "scenario_id": {
                    "type": "integer",
                    "description": "情境編號，範圍 1-24",
                    "minimum": 1,
                    "maximum": 24
                }
            },
            "required": ["scenario_id"],
            "additionalProperties": False
        },
        "strict": True
    }
}


def get_classify_scenario_tool():
    """
    獲取情境分類工具定義
    
    Returns:
        dict: 工具定義
    """
    return CLASSIFY_SCENARIO_TOOL


def create_classification_prompt(query: str, history: list, dimensions: dict) -> str:
    """
    創建情境分類的提示詞（極簡版，降低延遲）
    
    Args:
        query: 用戶問題
        history: 歷史對話記錄
        dimensions: 四向度定義
        
    Returns:
        str: 提示詞
    """
    # 簡化歷史（只取最近2條，只顯示問題）
    history_text = "無"
    if history and len(history) > 0:
        recent = history[-2:] if len(history) >= 2 else history
        history_items = []
        for item in recent:
            if hasattr(item, 'to_dict'):
                item_dict = item.to_dict()
            else:
                item_dict = item
            query_text = item_dict.get('query', '')
            if query_text:
                history_items.append(query_text)
        if history_items:
            history_text = "; ".join(history_items)
    
    # 極簡提示詞（直接說明，不要計算規則）
    prompt = f"""分析問題並返回情境編號（1-24）。

問題: {query}
歷史: {history_text}

快速判斷：
- 知識點數量（0/1/多個）
- 表達錯誤（有/無）
- 詳細度（粗略/詳細）
- 重複詢問（是/否）

直接返回情境編號。"""
    
    return prompt


def parse_tool_call_result(tool_call) -> int:
    """
    解析工具調用結果，提取情境編號
    
    Args:
        tool_call: 工具調用對象
        
    Returns:
        int: 情境編號（1-24）
    """
    import json
    
    try:
        # 解析工具調用的參數
        if hasattr(tool_call, 'function'):
            arguments = tool_call.function.arguments
            if isinstance(arguments, str):
                args_dict = json.loads(arguments)
            else:
                args_dict = arguments
            
            scenario_id = args_dict.get('scenario_id')
            
            # 驗證範圍
            if scenario_id and 1 <= scenario_id <= 24:
                return scenario_id
            else:
                print(f"⚠️  情境編號超出範圍: {scenario_id}，使用默認值 14")
                return 14  # 默認值：一個 + 無錯誤 + 粗略 + 正常狀態
        
        print("⚠️  無法解析工具調用結果，使用默認值 14")
        return 14
        
    except Exception as e:
        print(f"❌ 解析工具調用結果時出錯: {e}")
        return 14  # 默認值
