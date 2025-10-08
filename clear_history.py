#!/usr/bin/env python3
"""
清除歷史記錄腳本
"""
from core.history_manager import HistoryManager

if __name__ == "__main__":
    print("🧹 清除歷史記錄...")
    
    manager = HistoryManager()
    
    print(f"\n清除前：{len(manager.history)} 條記錄")
    print(f"知識點計數: {dict(manager.knowledge_point_counter)}")
    print(f"連續訪問: {list(manager.consecutive_access)}")
    
    manager.clear()
    
    print(f"\n清除後：{len(manager.history)} 條記錄")
    print(f"知識點計數: {dict(manager.knowledge_point_counter)}")
    print(f"連續訪問: {list(manager.consecutive_access)}")
    
    print("\n✅ 歷史記錄已完全清除！")
