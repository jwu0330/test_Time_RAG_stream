"""
Web API 後端
使用 FastAPI 提供 RESTful API 接口
所有計時在後端進行，不受前端渲染影響
"""
import asyncio
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn

from main_parallel import ParallelRAGSystem
from config import Config, get_config_summary
from core.history_manager import HistoryManager

# 創建 FastAPI 應用
app = FastAPI(
    title="RAG 流式系統 API",
    description="支援向量儲存、流式中斷與續寫的 RAG 系統",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局系統實例
system: Optional[ParallelRAGSystem] = None
history_manager: Optional[HistoryManager] = None


# ==================== 請求/響應模型 ====================

class QueryRequest(BaseModel):
    """查詢請求"""
    query: str
    scenario_ids: Optional[List[str]] = None
    auto_classify: bool = True


class QueryResponse(BaseModel):
    """查詢響應"""
    query: str
    final_answer: str
    scenario_used: str
    matched_docs: List[str]
    knowledge_points: List[str]
    dimensions: Dict[str, str]
    dimension_details: Dict[str, dict]
    time_report: dict
    history_summary: dict


class HistoryResponse(BaseModel):
    """歷史記錄響應"""
    total_queries: int
    recent_queries: List[dict]
    knowledge_point_stats: Dict[str, int]
    dimension_stats: Dict[str, dict]


class ConfigResponse(BaseModel):
    """配置響應"""
    models: dict
    parameters: dict
    paths: dict
    dimensions: dict


# ==================== 啟動/關閉事件 ====================

@app.on_event("startup")
async def startup_event():
    """應用啟動時初始化系統"""
    global system, history_manager
    
    print("\n" + "="*60)
    print("🚀 RAG 流式系統 API 啟動中...")
    print("="*60)
    
    # 初始化系統
    system = ParallelRAGSystem()
    history_manager = HistoryManager()
    
    # 初始化文件向量
    print("\n📚 初始化文件向量...")
    await system.initialize_documents()
    
    print("\n✅ 系統初始化完成！")
    print(f"📡 API 服務運行於: http://{Config.API_HOST}:{Config.API_PORT}")
    print(f"📖 API 文檔: http://{Config.API_HOST}:{Config.API_PORT}/docs")
    print("="*60 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """應用關閉時清理資源"""
    print("\n🛑 RAG 流式系統 API 關閉中...")
    if history_manager:
        history_manager.save()
    print("✅ 資源已清理\n")


# ==================== API 端點 ====================

@app.get("/")
async def root():
    """根端點"""
    return {
        "message": "RAG 流式系統 API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "query": "/api/query",
            "history": "/api/history",
            "config": "/api/config",
            "health": "/api/health"
        }
    }


@app.get("/api/health")
async def health_check():
    """健康檢查"""
    return {
        "status": "healthy",
        "system_initialized": system is not None,
        "history_loaded": history_manager is not None
    }


@app.post("/api/query")
async def process_query(request: QueryRequest):
    """
    處理查詢請求 - 所有計時在後端進行
    從後端接收文字開始計時，到轉發出去為止
    """
    if system is None:
        raise HTTPException(status_code=503, detail="系統未初始化")
    
    try:
        # 記錄後端接收時間（計時起點）
        backend_receive_time = time.perf_counter()
        
        query = request.query
        print(f"\n{'='*70}")
        print(f"📥 後端接收查詢: {query}")
        print(f"⏱️  開始計時...")
        print(f"{'='*70}")
        
        # 使用 ParallelRAGSystem 的並行處理方法（內部已有詳細計時）
        result = await system.process_query(query)
        
        # 提取需要的資訊
        dimensions = result.get("dimensions", {})
        matched_docs = result.get("matched_docs", [])
        final_answer = result.get("final_answer", "抱歉，無法生成回答")
        scenario_number = result.get("scenario_number", 0)
        scenario_description = result.get("scenario_description", "")
        knowledge_points = result.get("knowledge_points", [])
        
        # 獲取詳細計時報告
        time_report = result.get("time_report", {})
        
        # 計算後端總處理時間（從接收到準備轉發）
        backend_total_time = time.perf_counter() - backend_receive_time
        
        print(f"\n{'='*70}")
        print(f"📤 後端準備轉發結果")
        print(f"⏱️  後端總處理時間: {backend_total_time:.3f}s")
        print(f"{'='*70}\n")
        
        # 返回詳細的響應格式（包含完整計時資訊）
        return {
            "answer": final_answer,
            "dimensions": dimensions,
            "matched_docs": matched_docs,
            "knowledge_points": knowledge_points,
            "scenario": f"第 {scenario_number} 種情境",
            "scenario_number": scenario_number,
            "scenario_description": scenario_description,
            "response_time": backend_total_time,
            "timing_details": {
                "backend_total": round(backend_total_time, 3),
                "stages": time_report.get("stages", {}),
                "thread_a": time_report.get("thread_a", {}),
                "thread_b": time_report.get("thread_b", {}),
                "timestamp": time_report.get("timestamp", "")
            }
        }
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"❌ API 錯誤:\n{error_detail}")
        raise HTTPException(status_code=500, detail=f"處理查詢時發生錯誤: {str(e)}")


@app.get("/api/history", response_model=HistoryResponse)
async def get_history(limit: int = 10):
    """
    獲取歷史記錄
    
    Args:
        limit: 返回的記錄數量（默認10）
    """
    if history_manager is None:
        raise HTTPException(status_code=503, detail="歷史管理器未初始化")
    
    try:
        recent_queries = history_manager.get_recent_history(limit)
        
        response = HistoryResponse(
            total_queries=len(history_manager.history),
            recent_queries=[q.to_dict() for q in recent_queries],
            knowledge_point_stats=history_manager.get_knowledge_point_stats(),
            dimension_stats={
                dim: dict(counter)
                for dim, counter in history_manager.get_dimension_stats().items()
            }
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取歷史記錄時發生錯誤: {str(e)}")


@app.delete("/api/history")
async def clear_history():
    """清空歷史記錄"""
    if history_manager is None:
        raise HTTPException(status_code=503, detail="歷史管理器未初始化")
    
    try:
        history_manager.clear()
        return {"message": "歷史記錄已清空"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清空歷史記錄時發生錯誤: {str(e)}")


@app.get("/api/config", response_model=ConfigResponse)
async def get_config():
    """獲取系統配置"""
    try:
        config_summary = get_config_summary()
        
        response = ConfigResponse(
            models=config_summary["models"],
            parameters=config_summary["parameters"],
            paths=config_summary["paths"],
            dimensions=Config.DIMENSIONS
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取配置時發生錯誤: {str(e)}")


@app.get("/api/dimensions")
async def get_dimensions():
    """獲取四向度定義"""
    return {
        "dimensions": Config.DIMENSIONS,
        "knowledge_points": Config.KNOWLEDGE_POINTS,
        "repetition_threshold": Config.REPETITION_THRESHOLD
    }


# ==================== 主函數 ====================

def start_server(host: str = None, port: int = None):
    """
    啟動 API 服務器
    
    Args:
        host: 主機地址（默認從配置讀取）
        port: 端口號（默認從配置讀取）
    """
    host = host or Config.API_HOST
    port = port or Config.API_PORT
    
    uvicorn.run(
        "web_api:app",
        host=host,
        port=port,
        reload=False,  # 生產環境設為 False
        log_level="info"
    )


if __name__ == "__main__":
    start_server()
