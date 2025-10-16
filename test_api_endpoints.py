#!/usr/bin/env python3
"""
測試所有 API 端點
"""
import requests
import json

API_BASE = "http://localhost:8000"

def test_endpoint(name, url, method="GET", data=None):
    """測試單個端點"""
    print(f"\n{'='*60}")
    print(f"測試: {name}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        
        print(f"狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功")
            print(f"回應: {json.dumps(result, ensure_ascii=False, indent=2)[:500]}")
        else:
            print(f"❌ 失敗")
            print(f"錯誤: {response.text[:500]}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ 異常: {e}")
        return False

def main():
    """執行所有測試"""
    print("\n" + "="*60)
    print("🧪 API 端點測試")
    print("="*60)
    
    results = {}
    
    # 測試健康檢查
    results["health"] = test_endpoint(
        "健康檢查",
        f"{API_BASE}/api/health"
    )
    
    # 測試知識點數量
    results["knowledge_count"] = test_endpoint(
        "知識點數量",
        f"{API_BASE}/api/knowledge/count"
    )
    
    # 測試配置
    results["config"] = test_endpoint(
        "系統配置",
        f"{API_BASE}/api/config"
    )
    
    # 測試歷史記錄
    results["history"] = test_endpoint(
        "歷史記錄",
        f"{API_BASE}/api/history"
    )
    
    # 測試查詢（簡單測試）
    results["query"] = test_endpoint(
        "查詢測試",
        f"{API_BASE}/api/query",
        method="POST",
        data={"query": "什麼是 IPv4？"}
    )
    
    # 總結
    print("\n" + "="*60)
    print("📊 測試總結")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, success in results.items():
        status = "✅ 通過" if success else "❌ 失敗"
        print(f"{name:20s}: {status}")
    
    print(f"\n通過率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 所有測試通過！")
    else:
        print(f"\n⚠️  有 {total - passed} 個測試失敗")

if __name__ == "__main__":
    main()
