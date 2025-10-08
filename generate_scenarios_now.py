"""
立即生成 24 個情境文件
"""
import json
import os

# 創建目錄
os.makedirs("scenarios_24", exist_ok=True)

# 四向度的所有可能值
dimension_values = {
    "D1": ["零個", "一個", "多個"],
    "D2": ["有錯誤", "無錯誤"],
    "D3": ["非常詳細", "粗略", "未談及重點"],
    "D4": ["重複狀態", "正常狀態"]
}

scenario_id = 1

# 生成所有組合
for d1 in dimension_values["D1"]:
    for d2 in dimension_values["D2"]:
        for d3 in dimension_values["D3"]:
            for d4 in dimension_values["D4"]:
                # 創建情境
                scenario = {
                    "id": f"scenario_{scenario_id:02d}",
                    "scenario_number": scenario_id,
                    "name": f"{d1}+{d2}+{d3}+{d4}",
                    "dimensions": {
                        "D1": d1,
                        "D2": d2,
                        "D3": d3,
                        "D4": d4
                    },
                    "description": f"這是第 {scenario_id} 種情境",
                    "response_strategy": {
                        "tone": "友好、專業",
                        "structure": ["根據情境調整回答"],
                        "emphasis": ["提供準確信息"],
                        "length": "適中"
                    },
                    "prompt_template": f"""
【情境說明】
這是第 {scenario_id} 種情境。

四向度分析結果：
- D1 (知識點數量): {d1}
- D2 (表達錯誤): {d2}
- D3 (表達詳細度): {d3}
- D4 (重複詢問): {d4}

【回答指引】
請在回答開頭明確說明：「現在是第 {scenario_id} 種情境」

然後說明各向度的情況：
- 知識點數量：{d1}
- 表達錯誤：{d2}
- 表達詳細度：{d3}
- 重複詢問：{d4}

接著根據檢索到的教材內容，提供適當的回答。
"""
                }
                
                # 保存文件
                filename = f"scenarios_24/scenario_{scenario_id:02d}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(scenario, f, ensure_ascii=False, indent=2)
                
                print(f"✅ 生成: {filename} - {scenario['name']}")
                
                scenario_id += 1

# 生成索引文件
index = {
    "total_scenarios": 24,
    "description": "24 種情境組合（3×2×3×2=24）",
    "scenarios": []
}

for i in range(1, 25):
    with open(f"scenarios_24/scenario_{i:02d}.json", 'r', encoding='utf-8') as f:
        scenario = json.load(f)
        index["scenarios"].append({
            "id": scenario["id"],
            "number": scenario["scenario_number"],
            "name": scenario["name"],
            "dimensions": scenario["dimensions"]
        })

with open("scenarios_24/index.json", 'w', encoding='utf-8') as f:
    json.dump(index, f, ensure_ascii=False, indent=2)

print(f"\n✅ 共生成 24 個情境文件")
print(f"✅ 索引文件: scenarios_24/index.json")
print(f"\n所有情境已就緒，可以開始測試！")
