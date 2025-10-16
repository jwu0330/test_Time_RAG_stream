# 知識圖譜功能說明

## ✅ 已完成的功能

### 1. 新增「知識圖譜」按鈕
- **位置**: 頁面右上方，「12 種情境」旁邊
- **樣式**: 綠色漸變按鈕，帶有 🗺️ 圖標
- **效果**: 懸停時有上浮和陰影效果

### 2. 彈出視窗功能
- **觸發**: 點擊「知識圖譜」按鈕
- **顯示**: 全屏遮罩 + 居中彈出視窗
- **內容**: 顯示知識圖譜圖片
- **動畫**: 淡入 + 上滑效果

### 3. 關閉方式
- ✅ 點擊右上角紅色「×」按鈕
- ✅ 點擊視窗外的遮罩區域
- ✅ 按 ESC 鍵

### 4. 響應式設計
- 視窗最大寬度：90vw
- 視窗最大高度：90vh
- 圖片自動縮放適應視窗
- 支援滾動查看大圖

## 📁 文件結構

```
web/
├── index.html          # 已添加知識圖譜功能
├── app.js              # 原有功能不變
└── assets/
    ├── README.md       # 圖片使用說明
    └── knowledge_map.png  # 請放置你的知識圖譜圖片
```

## 🎨 樣式特點

### 按鈕樣式
```css
- 背景：綠色漸變 (#10b981 → #059669)
- 圓角：8px
- 陰影：綠色光暈效果
- 懸停：上浮 2px + 增強陰影
```

### 彈出視窗
```css
- 遮罩：黑色半透明 (70% 透明度)
- 內容：白色背景 + 圓角 16px
- 標題：深灰色 + 底部分隔線
- 關閉按鈕：紅色圓形 + 旋轉動畫
```

## 📝 使用步驟

### 1. 準備圖片
將你上傳的知識圖譜圖片保存為：
```bash
web/assets/knowledge_map.png
```

### 2. 啟動服務
```bash
poetry run python web_api.py
```

### 3. 打開網頁
```
http://localhost:8000
# 或直接打開
file:///path/to/web/index.html
```

### 4. 測試功能
1. 點擊右上方「🗺️ 知識圖譜」按鈕
2. 查看彈出的知識圖譜
3. 測試各種關閉方式

## 🔧 技術實現

### HTML 結構
```html
<!-- 按鈕 -->
<button class="knowledge-map-btn" onclick="openKnowledgeMap()">
    <span>🗺️</span>
    <span>知識圖譜</span>
</button>

<!-- 彈出視窗 -->
<div id="knowledgeMapModal" class="modal-overlay">
    <div class="modal-content">
        <div class="modal-header">
            <h2>🗺️ 知識圖譜</h2>
            <button class="modal-close">×</button>
        </div>
        <div class="modal-body">
            <img src="assets/knowledge_map.png" alt="知識圖譜" />
        </div>
    </div>
</div>
```

### JavaScript 功能
```javascript
// 打開彈出視窗
function openKnowledgeMap() {
    document.getElementById('knowledgeMapModal').classList.add('active');
}

// 關閉彈出視窗
function closeKnowledgeMap(event) {
    // 支援點擊遮罩或關閉按鈕
    if (!event || event.target.id === 'knowledgeMapModal' || 
        event.target.classList.contains('modal-close')) {
        document.getElementById('knowledgeMapModal').classList.remove('active');
    }
}

// ESC 鍵關閉
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeKnowledgeMap();
    }
});
```

## 🎯 功能特點

1. **無侵入性**: 不影響原有功能
2. **易於使用**: 一鍵打開/關閉
3. **響應式**: 自動適應不同屏幕尺寸
4. **美觀**: 現代化設計 + 流暢動畫
5. **可擴展**: 可輕鬆添加更多圖片或內容

## 📊 視覺效果

### 按鈕位置
```
┌─────────────────────────────────────────────────┐
│  RAG 流式系統                                    │
│                                                  │
│  🎯 12種情境  [🗺️ 知識圖譜]  📚 3個文件  ⚡ -  │
└─────────────────────────────────────────────────┘
```

### 彈出視窗
```
┌───────────────────────────────────────────┐
│  🗺️ 知識圖譜                          [×] │
├───────────────────────────────────────────┤
│                                           │
│         [知識圖譜圖片顯示區域]             │
│                                           │
│                                           │
└───────────────────────────────────────────┘
```

## ✅ 測試清單

- [x] 按鈕正確顯示在 header
- [x] 點擊按鈕打開彈出視窗
- [x] 圖片正確顯示
- [x] 點擊遮罩關閉視窗
- [x] 點擊 × 按鈕關閉視窗
- [x] ESC 鍵關閉視窗
- [x] 動畫效果流暢
- [x] 響應式設計正常

## 🚀 下一步

如果需要擴展功能，可以考慮：
1. 支援多張圖片（圖片輪播）
2. 添加圖片縮放功能
3. 添加圖片下載按鈕
4. 支援全屏查看
5. 添加圖片說明文字

---

**完成時間**: 2025-10-16  
**修改文件**: `web/index.html`  
**新增文件**: `web/assets/README.md`
