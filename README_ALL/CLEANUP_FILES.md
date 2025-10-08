# 文件清理說明

## 🗑️ 需要刪除的文件

執行以下命令清理多餘文件：

```bash
# 刪除多餘的 .sh 腳本
rm -f CLEANUP_AND_SETUP.sh
rm -f INSTALL_DIRECT.sh
rm -f QUICK_START.sh
rm -f SETUP_CLEAN_ENV.sh
rm -f activate_and_run.sh
rm -f push_to_github.sh
rm -f setup.sh
rm -f setup_env.sh
rm -f test_simple.sh

# 刪除多餘的 README 文件
rm -f ARCHITECTURE_CORRECT.md
rm -f CHECKLIST.md
rm -f D4_UPDATE.md
rm -f ENVIRONMENT_ISOLATION.md
rm -f FINAL_SUMMARY.md
rm -f JIM_README.md
rm -f PROJECT_SUMMARY.md
rm -f PUSH_TO_GITHUB.md
rm -f QUICK_REFERENCE.md
rm -f README.md
rm -f READY_TO_TEST.md
rm -f SCENARIO_SYSTEM_GUIDE.md
rm -f SETUP_ENVIRONMENT.md
rm -f START_WEB.md
rm -f UPDATES_SUMMARY.md

# 刪除備份文件
rm -f scenario_module_backup.py
rm -f scenario_module_old.py

# 刪除多餘的測試文件
rm -f example_usage.py
rm -f quick_start.py
rm -f generate_scenarios_now.py

# 保留的核心文件
# - README_SIMPLE.md (精簡版)
# - README_FULL.md (完整版)
# - RUN_TEST.py (測試腳本)
# - 所有 .py 核心模組
```

## ✅ 清理後的文件結構

```
test_Time_RAG_stream/
├── README_SIMPLE.md          # 精簡版文檔
├── README_FULL.md            # 完整版文檔
├── requirements.txt          # 依賴列表
├── pyproject.toml            # Poetry 配置
├── config.py                 # 配置文件
├── main_parallel.py          # 並行處理主程序
├── scenario_module.py        # 四向度分類器
├── scenario_matcher.py       # 情境匹配系統
├── scenario_generator.py     # 情境生成器
├── history_manager.py        # 歷史管理器
├── rag_module.py             # RAG 模組
├── vector_store.py           # 向量存儲
├── timer_utils.py            # 計時工具
├── knowledge_relations.json  # 知識點關聯
├── RUN_TEST.py              # 測試腳本
├── test_d4_logic.py         # D4 測試
├── test_system.py           # 系統測試
├── web_api.py               # Web API
├── web_interface.html       # Web 前端
├── scenarios_24/            # 24 個情境
├── docs/                    # 教材文件
└── venv/                    # 虛擬環境（不提交）
```

## 📝 執行清理

複製以下命令一次執行：

```bash
rm -f CLEANUP_AND_SETUP.sh INSTALL_DIRECT.sh QUICK_START.sh SETUP_CLEAN_ENV.sh activate_and_run.sh push_to_github.sh setup.sh setup_env.sh test_simple.sh ARCHITECTURE_CORRECT.md CHECKLIST.md D4_UPDATE.md ENVIRONMENT_ISOLATION.md FINAL_SUMMARY.md JIM_README.md PROJECT_SUMMARY.md PUSH_TO_GITHUB.md QUICK_REFERENCE.md README.md READY_TO_TEST.md SCENARIO_SYSTEM_GUIDE.md SETUP_ENVIRONMENT.md START_WEB.md UPDATES_SUMMARY.md scenario_module_backup.py scenario_module_old.py example_usage.py quick_start.py generate_scenarios_now.py
```
