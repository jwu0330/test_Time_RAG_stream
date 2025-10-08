#!/bin/bash
# 驗證 Responses API function call 功能

echo "🔍 驗證 Responses API Function Call 功能"
echo "=========================================="
echo ""

# 創建臨時測試腳本
cat > /tmp/test_function_call.py << 'EOF'
import os
from openai import OpenAI

client = OpenAI()

# 測試 function call
tools = [{
    "type": "function",
    "function": {
        "name": "classify_scenario",
        "description": "判定情境編號",
        "parameters": {
            "type": "object",
            "properties": {
                "scenario_id": {
                    "type": "integer",
                    "description": "情境編號（1-24）",
                    "minimum": 1,
                    "maximum": 24
                }
            },
            "required": ["scenario_id"],
            "additionalProperties": False
        },
        "strict": True
    }
}]

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是情境分析助手。"},
            {"role": "user", "content": "請判定：什麼是機器學習？這是第幾種情境？"}
        ],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "classify_scenario"}},
        temperature=0,
        max_tokens=50
    )
    
    message = response.choices[0].message
    if message.tool_calls:
        import json
        tool_call = message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        print(f"✅ Function Call 成功！")
        print(f"   返回情境編號: {args.get('scenario_id')}")
    else:
        print("⚠️  未收到 tool call")
        
except Exception as e:
    print(f"❌ 錯誤: {e}")
    import traceback
    traceback.print_exc()
EOF

# 執行測試
python3 /tmp/test_function_call.py

# 清理
rm /tmp/test_function_call.py

echo ""
echo "✅ 驗證完成"
