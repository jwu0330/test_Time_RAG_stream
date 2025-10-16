# 簡單介面切換功能

## ✅ 實現方式

在header中添加兩個切換按鈕：
- **💬 對話** - 顯示對話介面
- **🗺️ 知識圖譜** - 顯示知識圖譜

## 📸 效果展示

### Header 按鈕組
```
┌──────────────────────────────────────────────────────┐
│ ● RAG 流式系統    [💬 對話] [🗺️ 知識圖譜]   🎯📚⚡  │
└──────────────────────────────────────────────────────┘
```

### 對話模式（預設）
```
┌─────────────────────────────────────────────┐
│ [💬 對話] 🗺️ 知識圖譜                       │
├──────────┬──────────────────────────────────┤
│ 側邊欄   │  對話區域                        │
│          │                                  │
│ 系統資訊 │  訊息顯示                        │
│          │                                  │
│          │  輸入框                          │
└──────────┴──────────────────────────────────┘
```

### 知識圖譜模式
```
┌─────────────────────────────────────────────┐
│ 💬 對話 [🗺️ 知識圖譜]                       │
├─────────────────────────────────────────────┤
│                                             │
│         知識圖譜圖片（全屏顯示）             │
│                                             │
│                                             │
└─────────────────────────────────────────────┘
```

## 🎨 設計特點

### 1. 按鈕樣式
- **未選中**: 透明背景，白色文字
- **選中**: 白色背景，紫色文字，帶陰影
- **懸停**: 半透明白色背景

### 2. 切換效果
- 點擊按鈕立即切換
- 按鈕狀態同步更新
- 側邊欄自動隱藏/顯示

### 3. 響應式
- 圖片自動適應容器大小
- 支援滾動查看大圖

## 🔧 技術實現

### CSS 關鍵樣式
```css
/* 按鈕組 */
.view-switcher {
    display: flex;
    gap: 10px;
    background: rgba(255, 255, 255, 0.2);
    padding: 4px;
    border-radius: 10px;
}

/* 選中狀態 */
.view-btn.active {
    background: white;
    color: #667eea;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 知識圖譜視圖 */
.chat-container.show-map .chat-area {
    display: none;
}

.chat-container.show-map .knowledge-map-view {
    display: block;
}
```

### JavaScript 切換邏輯
```javascript
function switchView(view) {
    const chatContainer = document.querySelector('.chat-container');
    const viewBtns = document.querySelectorAll('.view-btn');
    const sidebar = document.querySelector('.sidebar');
    
    // 更新按鈕狀態
    viewBtns.forEach(btn => btn.classList.remove('active'));
    event.target.closest('.view-btn').classList.add('active');
    
    if (view === 'map') {
        // 顯示知識圖譜
        chatContainer.classList.add('show-map');
        sidebar.style.display = 'none';
    } else {
        // 顯示對話介面
        chatContainer.classList.remove('show-map');
        sidebar.style.display = 'block';
    }
}
```

## 📝 使用步驟

### 1. 準備圖片
將知識圖譜圖片保存為：
```
web/assets/knowledge_map.png
```

### 2. 打開網頁
```bash
# 方式1: 啟動API服務
poetry run python web_api.py

# 方式2: 直接打開HTML
open web/index.html
```

### 3. 切換介面
- 點擊「💬 對話」→ 顯示對話介面
- 點擊「🗺️ 知識圖譜」→ 顯示知識圖譜

## ✨ 優點

1. **簡單直觀**: 一鍵切換，無需彈出視窗
2. **全屏顯示**: 知識圖譜佔滿整個區域
3. **狀態清晰**: 按鈕高亮顯示當前模式
4. **無侵入性**: 不影響原有對話功能
5. **易於擴展**: 可輕鬆添加更多視圖

## 🎯 與彈出視窗的區別

| 特性 | 簡單切換 | 彈出視窗 |
|------|---------|---------|
| **顯示方式** | 全屏替換 | 覆蓋遮罩 |
| **操作步驟** | 1步（點擊按鈕） | 2步（打開+關閉） |
| **空間利用** | 100% | ~90% |
| **適用場景** | 需要長時間查看 | 快速查看 |
| **實現複雜度** | 簡單 | 中等 |

## 📂 修改的文件

- ✅ `web/index.html` - 添加切換按鈕和知識圖譜視圖
- ✅ CSS樣式 - 按鈕和視圖切換樣式
- ✅ JavaScript - 切換邏輯

## 🔄 未來擴展

可以輕鬆添加更多視圖：
```html
<button class="view-btn" onclick="switchView('stats')">
    <span>📊</span>
    <span>統計</span>
</button>
```

---

**完成時間**: 2025-10-16  
**實現方式**: 簡單介面切換（無彈出視窗）
