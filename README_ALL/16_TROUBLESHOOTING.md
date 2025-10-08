# 故障排除指南

**📅 更新日期**: 2025-10-08  
**📚 版本**: 1.0

---

## 🔍 常見問題與解決方案

### 問題 1: `python: command not found` 或 `exit code 127`

**症狀**：
```bash
python main_parallel.py
# bash: python: command not found
# 或 exit code: 127
```

**原因**：系統中沒有 `python` 命令，只有 `python3`

**解決方案**：
```bash
# 使用 python3 而不是 python
python3 main_parallel.py

# 或使用快速測試腳本（會自動處理）
bash README_ALL/BASH_ALL/quick_test.sh
```

---

### 問題 2: 依賴安裝到用戶目錄而非虛擬環境

**症狀**：
```bash
# 看到警告
WARNING: The script xxx is installed in '/home/jim/.local/bin' which is not on PATH.
```

**原因**：使用了 `pip3 install --user` 而非在虛擬環境中安裝

**解決方案**：
```bash
# 清理並重新安裝到虛擬環境
bash README_ALL/BASH_ALL/cleanup_and_reinstall.sh
```

---

### 問題 3: `ModuleNotFoundError: No module named 'openai'`

**症狀**：
```python
ModuleNotFoundError: No module named 'openai'
```

**原因**：
1. 未激活虛擬環境
2. 虛擬環境中未安裝依賴

**解決方案**：
```bash
# 方案 1: 激活虛擬環境
source .venv/bin/activate
python3 main_parallel.py

# 方案 2: 重新安裝
bash README_ALL/BASH_ALL/cleanup_and_reinstall.sh
source .venv/bin/activate
python3 main_parallel.py

# 方案 3: 使用快速測試腳本（自動處理）
bash README_ALL/BASH_ALL/quick_test.sh
```

---

### 問題 4: OpenAI SDK 版本過舊

**症狀**：
```python
AttributeError: 'OpenAI' object has no attribute 'responses'
# 或其他與 Responses API 相關的錯誤
```

**原因**：OpenAI SDK 版本 < 1.54.0

**解決方案**：
```bash
# 在虛擬環境中升級
source .venv/bin/activate
pip install -U openai

# 檢查版本
python3 -c "import openai; print(openai.__version__)"
# 應該顯示 >= 1.54.0
```

---

### 問題 5: 未設定 API Key

**症狀**：
```python
openai.AuthenticationError: No API key provided
```

**原因**：未設定 `OPENAI_API_KEY` 環境變量

**解決方案**：
```bash
# 設定 API Key
export OPENAI_API_KEY='your-api-key-here'

# 驗證
echo $OPENAI_API_KEY

# 或使用 .env 文件
cp .env.example .env
# 編輯 .env 文件，填入 API Key
```

---

### 問題 6: 虛擬環境未激活

**症狀**：
- 提示符沒有顯示 `(.venv)`
- 運行程序時找不到模組

**檢查方法**：
```bash
# 檢查是否在虛擬環境中
echo $VIRTUAL_ENV
# 如果為空，表示未激活
```

**解決方案**：
```bash
# 激活虛擬環境
source .venv/bin/activate

# 確認激活成功
echo $VIRTUAL_ENV
# 應該顯示: /path/to/test_Time_RAG_stream/.venv
```

---

### 問題 7: Function Call 未返回結果

**症狀**：
```
⚠️  未收到工具調用，使用默認情境
```

**原因**：
1. API 模型不支持 function calling
2. Tool 定義格式錯誤
3. 網絡問題

**解決方案**：
```bash
# 1. 驗證 Function Call 功能
bash README_ALL/BASH_ALL/verify_function_call.sh

# 2. 檢查模型配置
# 編輯 config.py，確保使用支持的模型
CLASSIFIER_MODEL = "gpt-3.5-turbo"  # 或 gpt-4o-mini

# 3. 查看詳細錯誤
python3 main_parallel.py
# 查看控制台輸出的錯誤信息
```

---

### 問題 8: 向量文件損壞或不存在

**症狀**：
```
⚠️  首次啟動，需要調用 OpenAI API 生成向量
```

**原因**：
1. `vectors.pkl` 不存在
2. 向量文件損壞

**解決方案**：
```bash
# 刪除舊的向量文件，重新生成
rm vectors.pkl vectors.json

# 運行程序，會自動重新生成
python3 main_parallel.py
```

---

### 問題 9: 端口被占用（Web API）

**症狀**：
```
ERROR: [Errno 98] Address already in use
```

**原因**：端口 8000 已被其他程序占用

**解決方案**：
```bash
# 方案 1: 查找並關閉占用端口的程序
lsof -i :8000
kill -9 <PID>

# 方案 2: 使用其他端口
# 編輯 config.py
API_PORT = 8001  # 改為其他端口

# 或直接指定
python3 web_api.py --port 8001
```

---

### 問題 10: 權限錯誤

**症狀**：
```
Permission denied: '.venv/bin/activate'
```

**原因**：腳本沒有執行權限

**解決方案**：
```bash
# 添加執行權限
chmod +x README_ALL/BASH_ALL/*.sh

# 或直接使用 bash 執行
bash README_ALL/BASH_ALL/quick_test.sh
```

---

## 🔧 調試技巧

### 1. 檢查環境

```bash
# 檢查虛擬環境
echo $VIRTUAL_ENV

# 檢查 Python 版本
python3 --version

# 檢查已安裝的包
pip list | grep -E "openai|numpy|fastapi"

# 檢查 API Key
echo $OPENAI_API_KEY | head -c 10
```

### 2. 詳細錯誤信息

```python
# 在 Python 代碼中添加調試信息
import traceback

try:
    # 你的代碼
    pass
except Exception as e:
    print(f"錯誤: {e}")
    traceback.print_exc()
```

### 3. 測試 API 連接

```bash
# 測試 OpenAI API
python3 -c "
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{'role': 'user', 'content': 'Hello'}],
    max_tokens=10
)
print(response.choices[0].message.content)
"
```

---

## 📋 完整重置流程

如果遇到無法解決的問題，可以完全重置：

```bash
# 1. 備份重要數據
cp history.json history.json.backup
cp vectors.pkl vectors.pkl.backup

# 2. 刪除虛擬環境
rm -rf .venv

# 3. 清理用戶目錄的包
pip3 uninstall -y openai numpy fastapi uvicorn pydantic

# 4. 重新安裝
bash README_ALL/BASH_ALL/cleanup_and_reinstall.sh

# 5. 激活虛擬環境
source .venv/bin/activate

# 6. 設定 API Key
export OPENAI_API_KEY='your-api-key'

# 7. 測試
python3 main_parallel.py
```

---

## 🆘 獲取幫助

### 檢查清單

- [ ] 已激活虛擬環境（`echo $VIRTUAL_ENV` 有輸出）
- [ ] OpenAI SDK 版本 >= 1.54.0
- [ ] 已設定 `OPENAI_API_KEY`
- [ ] 使用 `python3` 而非 `python`
- [ ] 依賴已安裝在虛擬環境中

### 相關文檔

- [設置總結](15_SETUP_SUMMARY.md)
- [架構說明](13_RESPONSES_API_ARCHITECTURE.md)
- [遷移指南](14_MIGRATION_GUIDE.md)

### 快速測試命令

```bash
# 一鍵測試（自動處理大部分問題）
bash README_ALL/BASH_ALL/quick_test.sh
```

---

**還有問題？** 查看錯誤日誌並參考上述解決方案！ 🔍
