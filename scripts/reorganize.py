"""
重組腳本 - 自動化移動和更新文件
"""
import os
import shutil

def main():
    base_dir = "/home/jim/code/python/test_Time_RAG_stream"
    
    # 定義要移動的核心模組
    core_modules = [
        "history_manager.py",
        "scenario_module.py", 
        "scenario_matcher.py"
    ]
    
    # 移動核心模組到 core/
    for module in core_modules:
        src = os.path.join(base_dir, module)
        dst = os.path.join(base_dir, "core", module)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"✅ 已複製: {module} -> core/{module}")
    
    # 移動測試文件到 tests/
    test_files = ["test_system.py", "test_d4_logic.py"]
    for test_file in test_files:
        src = os.path.join(base_dir, test_file)
        dst = os.path.join(base_dir, "tests", test_file)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"✅ 已複製: {test_file} -> tests/{test_file}")
    
    # 移動工具腳本到 scripts/
    script_files = ["RUN_TEST.py", "scenario_generator.py"]
    for script_file in script_files:
        src = os.path.join(base_dir, script_file)
        dst_name = "run_test.py" if script_file == "RUN_TEST.py" else script_file
        dst = os.path.join(base_dir, "scripts", dst_name)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"✅ 已複製: {script_file} -> scripts/{dst_name}")
    
    # 移動數據目錄
    data_items = [
        ("docs", "data/docs"),
        ("scenarios_24", "data/scenarios"),
        ("knowledge_relations.json", "data/knowledge_relations.json")
    ]
    
    for src_name, dst_path in data_items:
        src = os.path.join(base_dir, src_name)
        dst = os.path.join(base_dir, dst_path)
        if os.path.exists(src) and not os.path.exists(dst):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            print(f"✅ 已複製: {src_name} -> {dst_path}")
    
    # 重命名主程序
    src = os.path.join(base_dir, "main_parallel.py")
    dst = os.path.join(base_dir, "main_new.py")
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy2(src, dst)
        print(f"✅ 已複製: main_parallel.py -> main_new.py")
    
    print("\n✅ 文件重組完成！")
    print("\n下一步：")
    print("1. 更新 core/ 中的 import 路徑")
    print("2. 更新 config.py 路徑配置")
    print("3. 更新主程序和其他文件的 import")
    print("4. 測試驗證")

if __name__ == "__main__":
    main()
