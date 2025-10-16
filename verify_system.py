#!/usr/bin/env python3
"""
系統驗證腳本
檢查所有核心模組是否正常
"""

def verify_imports():
    """驗證所有核心模組可以正常導入"""
    print("🔍 驗證系統模組...\n")
    
    errors = []
    
    # 測試核心模組
    tests = [
        ("main_parallel", "ResponsesRAGSystem"),
        ("core.vector_store", "VectorStore"),
        ("core.rag_module", "RAGRetriever"),
        ("core.scenario_classifier", "ScenarioClassifier"),
        ("core.dimension_classifier", "DimensionClassifier"),
        ("core.ontology_manager", "OntologyManager"),
        ("core.history_manager", "HistoryManager"),
        ("config", "Config"),
    ]
    
    for module_name, class_name in tests:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print(f"✅ {module_name}.{class_name}")
        except Exception as e:
            error_msg = f"❌ {module_name}.{class_name}: {e}"
            print(error_msg)
            errors.append(error_msg)
    
    print("\n" + "="*60)
    if errors:
        print(f"❌ 發現 {len(errors)} 個錯誤")
        for error in errors:
            print(f"  {error}")
    else:
        print("✅ 所有模組驗證通過！")
    print("="*60)
    
    return len(errors) == 0

def verify_files():
    """驗證關鍵文件存在"""
    print("\n🔍 驗證關鍵文件...\n")
    
    from pathlib import Path
    
    base_dir = Path(__file__).parent
    
    required_files = [
        "main_parallel.py",
        "web_api.py",
        "config.py",
        "core/scenario_classifier.py",
        "core/dimension_classifier.py",
        "core/ontology_manager.py",
        "core/tools/knowledge_detector.py",
        "core/tools/correctness_detector.py",
        "core/tools/repetition_checker.py",
        "data/scenarios/scenarios_12.json",
        "data/ontology/knowledge_ontology.txt",
    ]
    
    missing = []
    
    for file_path in required_files:
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (不存在)")
            missing.append(file_path)
    
    print("\n" + "="*60)
    if missing:
        print(f"❌ 缺少 {len(missing)} 個文件")
    else:
        print("✅ 所有關鍵文件存在！")
    print("="*60)
    
    return len(missing) == 0

def main():
    print("\n" + "="*60)
    print("🚀 系統整合驗證")
    print("="*60 + "\n")
    
    imports_ok = verify_imports()
    files_ok = verify_files()
    
    print("\n" + "="*60)
    if imports_ok and files_ok:
        print("🎉 系統整合完成！所有驗證通過！")
    else:
        print("⚠️  系統整合存在問題，請檢查上述錯誤")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
