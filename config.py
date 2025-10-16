"""
系統配置文件
用於設定模型和系統參數
"""

class Config:
    """系統配置類"""
    
    # ==================== 共享 OpenAI Client ====================
    
    _openai_client = None
    
    @classmethod
    def get_openai_client(cls, api_key: str = None):
        """
        獲取共享的 OpenAI client（單例模式）
        
        Args:
            api_key: OpenAI API Key（可選）
            
        Returns:
            OpenAI client 實例
        """
        if cls._openai_client is None:
            from openai import OpenAI
            print("⚙️ 初始化共享 OpenAI client...")
            cls._openai_client = OpenAI(api_key=api_key) if api_key else OpenAI()
            print("✅ OpenAI client 初始化完成")
        return cls._openai_client
    
    # ==================== 模型配置 ====================
    
    # Embedding 模型
    # 選項: "text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"
    EMBEDDING_MODEL = "text-embedding-3-small"
    
    # 主要 LLM 模型（用於生成草稿和最終答案）
    # 選項: "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini"
    LLM_MODEL = "gpt-4o-mini"
    
    # 情境分類模型（用於 K/C/R 三維度判定）
    # 選項: "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o-mini"
    # 使用 gpt-4o-mini 獲得更快的響應速度
    CLASSIFIER_MODEL = "gpt-4o-mini"
    
    @classmethod
    def verify_model_config(cls):
        """驗證模型配置並打印"""
        print(f"\n{'='*60}")
        print(f"🤖 模型配置驗證")
        print(f"{'='*60}")
        print(f"  Embedding 模型: {cls.EMBEDDING_MODEL}")
        print(f"  主要 LLM 模型: {cls.LLM_MODEL}")
        print(f"  分類器模型: {cls.CLASSIFIER_MODEL}")
        print(f"{'='*60}")
        
        # 驗證是否使用 gpt-4o-mini
        if cls.CLASSIFIER_MODEL != "gpt-4o-mini":
            print(f"⚠️  警告：分類器模型不是 gpt-4o-mini，可能影響效能")
        else:
            print(f"✅ 分類器模型已正確設定為 gpt-4o-mini")
        
        if cls.LLM_MODEL != "gpt-4o-mini":
            print(f"⚠️  警告：主要 LLM 模型不是 gpt-4o-mini")
        else:
            print(f"✅ 主要 LLM 模型已正確設定為 gpt-4o-mini")
        
        print(f"{'='*60}\n")
    
    # ==================== 系統參數 ====================
    
    # 歷史紀錄保存數量
    HISTORY_SIZE = 10
    
    # 重複詢問閾值（連續詢問同一知識點超過此次數視為重複）
    REPETITION_THRESHOLD = 3
    
    # RAG 檢索參數
    RAG_TOP_K = 3  # 返回前 K 個最相關文件
    RAG_SIMILARITY_THRESHOLD = 0.7  # 相似度閾值
    
    # LLM 生成參數
    LLM_TEMPERATURE = 0.7  # 溫度參數（0-1，越高越隨機）
    LLM_MAX_TOKENS = 500  # 草稿最大 token 數
    LLM_FINAL_MAX_TOKENS = 200  # 最終答案最大 token 數（測試環境：約100字）
    
    # ==================== 儲存路徑 ====================
    
    # 向量儲存路徑
    VECTOR_STORAGE_PATH = "vectors.pkl"
    
    # 歷史紀錄儲存路徑
    HISTORY_STORAGE_PATH = "history.json"
    
    # 結果輸出目錄
    RESULTS_DIR = "results"
    
    # 文件目錄
    DOCS_DIR = "data/docs"
    
    # 情境目錄
    SCENARIOS_DIR = "data/scenarios"
    
    # ==================== 三維度定義 ====================
    
    DIMENSIONS = {
        "K": {
            "name": "知識點數量",
            "description": "這句話牽涉到的知識點數量",
            "values": ["零個", "一個", "多個"]
        },
        "C": {
            "name": "正確性",
            "description": "這句話的表達是否正確",
            "values": ["正確", "不正確"]
        },
        "R": {
            "name": "重複性",
            "description": "是否在同一知識點上重複詢問多次",
            "values": ["正常", "重複"],
            "threshold": REPETITION_THRESHOLD
        }
    }
    
    # ==================== 知識點映射 ====================
    
    # 文件到知識點的映射（IP 網路相關知識點）
    KNOWLEDGE_POINTS = {
        "01_IP位址.txt": "IP 位址",
        "02_IPv4.txt": "IPv4",
        "03_IPv6.txt": "IPv6",
        "04_多播位址.txt": "多播位址",
        "05_任播位址.txt": "任播位址",
        "06_廣播位址.txt": "廣播位址",
        "07_回送位址.txt": "回送位址",
        "08_公有位址.txt": "公有位址",
        "09_私有位址.txt": "私有位址",
        "10_Link-Local.txt": "Link-Local",
        "11_Global_Unicast.txt": "Global Unicast",
        "12_位址對映.txt": "位址對映",
        "13_Dual_Stack.txt": "Dual Stack",
        "14_CGNAT.txt": "CGNAT",
        "15_NAT.txt": "NAT",
        "16_PAT_NAPT.txt": "PAT / NAPT",
        "17_NAT64_DNS64.txt": "NAT64 / DNS64",
        "18_位址分配方式.txt": "位址分配方式",
        "19_靜態分配.txt": "靜態分配",
        "20_動態分配.txt": "動態分配",
        "21_DHCP.txt": "DHCP",
        "22_SLAAC.txt": "SLAAC",
        "23_Router_Advertisement.txt": "Router Advertisement (RA)",
        "24_子網劃分.txt": "子網劃分",
        "25_子網遮罩.txt": "子網遮罩",
        "26_超網.txt": "超網",
        "27_CIDR.txt": "CIDR",
        "28_VLSM.txt": "VLSM",
        "29_DNS.txt": "DNS",
        "30_DNS伺服.txt": "DNS 伺服",
        "31_DNS快取.txt": "DNS 快取",
        "32_遞迴解析.txt": "遞迴解析",
        "33_根伺服器.txt": "根伺服器",
        "34_TLD伺服器.txt": "TLD 伺服器",
        "35_授權伺服器.txt": "授權伺服器",
        "36_區域類型.txt": "區域類型",
        "37_A記錄.txt": "A 記錄",
        "38_AAAA記錄.txt": "AAAA 記錄",
        "39_NS記錄.txt": "NS 記錄",
        "40_MX記錄.txt": "MX 記錄",
        "41_CNAME記錄.txt": "CNAME 記錄",
        "42_Mail_Server.txt": "Mail Server",
        "43_另一網域名稱.txt": "另一網域名稱",
        "44_網路位址轉譯.txt": "網路位址轉譯",
        "45_IP位址管理.txt": "IP 位址管理"
    }
    
    # ==================== Web 界面配置 ====================
    
    # API 服務器配置
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    
    # CORS 設定
    CORS_ORIGINS = ["*"]  # 生產環境應該設定具體域名
    
    # 是否啟用流式輸出
    ENABLE_STREAMING = True


# 創建全局配置實例
config = Config()

# 便捷函數
def get_shared_client(api_key: str = None):
    """獲取共享的 OpenAI client"""
    return Config.get_openai_client(api_key)


def update_config(**kwargs):
    """
    動態更新配置
    
    Args:
        **kwargs: 要更新的配置項
    
    Example:
        update_config(LLM_MODEL="gpt-4", RAG_TOP_K=5)
    """
    for key, value in kwargs.items():
        if hasattr(Config, key):
            setattr(Config, key, value)
        else:
            raise ValueError(f"未知的配置項: {key}")


def get_config_summary() -> dict:
    """
    獲取配置摘要
    
    Returns:
        配置摘要字典
    """
    return {
        "models": {
            "embedding": Config.EMBEDDING_MODEL,
            "llm": Config.LLM_MODEL,
            "classifier": Config.CLASSIFIER_MODEL
        },
        "parameters": {
            "history_size": Config.HISTORY_SIZE,
            "repetition_threshold": Config.REPETITION_THRESHOLD,
            "rag_top_k": Config.RAG_TOP_K,
            "temperature": Config.LLM_TEMPERATURE
        },
        "paths": {
            "vectors": Config.VECTOR_STORAGE_PATH,
            "history": Config.HISTORY_STORAGE_PATH,
            "results": Config.RESULTS_DIR
        }
    }
