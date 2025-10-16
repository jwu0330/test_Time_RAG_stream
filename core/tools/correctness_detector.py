"""
C (Correctness) - 正確性檢測工具
API 呼叫 #2 - 判斷用戶問題的表達是否正確
"""
import json
from openai import OpenAI
from config import Config, get_shared_client


class CorrectnessDetector:
    """C 值檢測器 - 判斷問題表達的正確性"""
    
    def __init__(self, api_key: str = None, timer=None):
        """
        初始化正確性檢測器
        
        Args:
            api_key: OpenAI API Key
            timer: 計時器（可選）
        """
        # 使用共享的 OpenAI client
        self.client = get_shared_client(api_key)
        self.timer = timer
    
    async def detect(self, query: str) -> int:
        """
        檢測問題表達是否正確
        
        Args:
            query: 用戶問題
            
        Returns:
            int: 0=正確, 1=不正確
        """
        import time
        t_start = time.perf_counter()
        
        print(f"\n🔍 C值檢測：開始分析查詢...")
        print(f"🤖 使用模型: {Config.CLASSIFIER_MODEL}")
        
        if self.timer:
            self.timer.start_stage("C值 API 調用（正確性檢測）", thread='C')
        
        # 簡化提示詞，減少處理時間
        prompt = f"""分析這句話：「{query}」

是否有明顯錯誤？

判斷：
- 疑問句/開放性問題 → 正確 (0)
- 明顯事實錯誤/邏輯錯誤 → 錯誤 (1)
- 預設為正確

返回 JSON: {{"correct": 0}} 或 {{"correct": 1}}"""
        
        try:
            t_api_start = time.perf_counter()
            print(f"📤 C值檢測：發送 API 請求...")
            
            response = self.client.chat.completions.create(
                model=Config.CLASSIFIER_MODEL,
                messages=[
                    {"role": "system", "content": "快速判斷正確性。預設正確。"},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0,
                max_tokens=20
            )
            
            t_api_end = time.perf_counter()
            api_duration = t_api_end - t_api_start
            print(f"📥 C值檢測：API 回應耗時 {api_duration:.3f} 秒")
            
            result = response.choices[0].message.content.strip()
            print(f"📝 C值檢測：API 回應內容: {result}")
            
            if self.timer:
                self.timer.stop_stage("C值 API 調用（正確性檢測）", thread='C')
            
            t_end = time.perf_counter()
            self._last_timing = t_end - t_start
            
            # 解析 JSON
            try:
                data = json.loads(result)
                c_value = data.get("correct", 0)
                print(f"✅ C值檢測：結果 = {c_value} ({['正確', '不正確'][c_value]})")
                print(f"⏱️  C值檢測總耗時: {self._last_timing:.3f} 秒")
                return c_value
            except json.JSONDecodeError as json_err:
                print(f"⚠️  C值檢測 JSON 解析失敗: {json_err}")
                print(f"   原始回應: {result}")
                return 0  # 默認為正確
            
        except Exception as e:
            t_end = time.perf_counter()
            error_duration = t_end - t_start
            print(f"❌ C值檢測 API 調用失敗: {e}")
            print(f"⏱️  C值檢測失敗耗時: {error_duration:.3f} 秒")
            if self.timer:
                self.timer.stop_stage("C值 API 調用（正確性檢測）", thread='C')
            self._last_timing = error_duration
            return 0  # 默認為正確
