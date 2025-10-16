// RAG 流式系統 - 前端 JavaScript

// 配置
const API_BASE = 'http://localhost:8000';
let queryCount = 0;
let totalResponseTime = 0;
let chatHistory = []; // 儲存對話歷史

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 頁面載入完成');
    checkAPIStatus();
    setupInputHandlers();
    loadChatHistory(); // 載入歷史對話
    loadKnowledgeCount();
});

// 檢查 API 狀態
async function checkAPIStatus() {
    try {
        const response = await fetch(`${API_BASE}/api/health`);
        if (response.ok) {
            console.log('✅ API 連接成功');
        }
    } catch (error) {
        showError('無法連接到 API 服務器，請確保後端正在運行 (python3 web_api.py)');
    }
}

// 設置輸入處理
function setupInputHandlers() {
    const input = document.getElementById('userInput');
    const charCount = document.getElementById('charCount');

    // 字數統計
    input.addEventListener('input', () => {
        const length = input.value.length;
        charCount.textContent = `${length} / 500`;
        
        // 自動調整高度
        input.style.height = 'auto';
        input.style.height = input.scrollHeight + 'px';
    });

    // Enter 發送
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

// 發送範例問題
function sendExample(text) {
    document.getElementById('userInput').value = text;
    sendMessage();
}

// 發送訊息
async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();

    if (!message) {
        console.log('訊息為空，不發送');
        return;
    }

    console.log('📤 發送訊息:', message);

    // 清空輸入
    input.value = '';
    input.style.height = 'auto';
    document.getElementById('charCount').textContent = '0 / 500';

    // 移除歡迎訊息
    const welcome = document.querySelector('.welcome-message');
    if (welcome) {
        console.log('移除歡迎訊息');
        welcome.remove();
    }

    // 顯示用戶訊息
    console.log('顯示用戶訊息');
    addMessage('user', message);

    // 顯示載入動畫
    const loadingId = showLoading();

    // 禁用發送按鈕
    const sendBtn = document.getElementById('sendBtn');
    sendBtn.disabled = true;
    sendBtn.textContent = '處理中...';

    try {
        const startTime = Date.now();

        console.log('🔄 調用 API...');
        // 調用 API
        const response = await fetch(`${API_BASE}/api/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: message })
        });

        const endTime = Date.now();
        const responseTime = ((endTime - startTime) / 1000).toFixed(2);

        console.log(`⏱️ API 響應時間: ${responseTime}s`);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ API 錯誤:', errorText);
            throw new Error(`API 請求失敗: ${response.status}`);
        }

        const data = await response.json();
        console.log('✅ 收到回應:', data);

        // 移除載入動畫
        removeLoading(loadingId);

        // 顯示回答
        console.log('顯示助手回答');
        addMessage('assistant', data.answer, {
            dimensions: data.dimensions,
            matched_docs: data.matched_docs,
            response_time: responseTime,
            scenario: data.scenario
        });

        // 更新統計
        updateStats(responseTime);

    } catch (error) {
        console.error('❌ 錯誤:', error);
        removeLoading(loadingId);
        showError('發生錯誤：' + error.message);
    } finally {
        // 啟用發送按鈕
        sendBtn.disabled = false;
        sendBtn.textContent = '發送 📤';
    }
}

// 添加訊息（保存到歷史）
function addMessage(type, content, meta = null) {
    console.log(`➕ 添加${type}訊息:`, content.substring(0, 50) + '...');
    
    // 保存到歷史
    chatHistory.push({ type, content, meta });
    saveChatHistory();
    
    // 顯示到 DOM
    addMessageToDOM(type, content, meta);
    
    console.log('✅ 訊息已添加並保存');
}

// 顯示載入動畫
function showLoading() {
    const messagesDiv = document.getElementById('messages');
    const loadingDiv = document.createElement('div');
    const loadingId = 'loading-' + Date.now();
    loadingDiv.id = loadingId;
    loadingDiv.className = 'message message-assistant';
    loadingDiv.innerHTML = `
        <div class="loading">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
        </div>
    `;
    messagesDiv.appendChild(loadingDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    return loadingId;
}

// 移除載入動畫
function removeLoading(loadingId) {
    const loadingDiv = document.getElementById(loadingId);
    if (loadingDiv) loadingDiv.remove();
}

// 顯示錯誤
function showError(message) {
    const messagesDiv = document.getElementById('messages');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = '❌ ' + message;
    messagesDiv.appendChild(errorDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    // 3 秒後自動移除
    setTimeout(() => errorDiv.remove(), 5000);
}

// 更新統計
function updateStats(responseTime) {
    queryCount++;
    totalResponseTime += parseFloat(responseTime);
    const avgTime = (totalResponseTime / queryCount).toFixed(2);

    document.getElementById('responseTime').textContent = `${responseTime}s`;
    document.getElementById('sessionStats').innerHTML = `
        查詢次數: <strong>${queryCount}</strong><br>
        平均響應: <strong>${avgTime}s</strong>
    `;
}

// 載入知識點總數
async function loadKnowledgeCount() {
    try {
        const res = await fetch(`${API_BASE}/api/knowledge/count`);
        if (!res.ok) return;
        const data = await res.json();
        const countEl = document.getElementById('knowledgeCount');
        if (countEl) countEl.textContent = data.count;
    } catch (e) {
        console.warn('讀取知識點數量失敗:', e);
    }
}

// 保存對話歷史到 localStorage
function saveChatHistory() {
    try {
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
        localStorage.setItem('queryCount', queryCount);
        localStorage.setItem('totalResponseTime', totalResponseTime);
        console.log('💾 對話歷史已保存');
    } catch (error) {
        console.error('保存歷史失敗:', error);
    }
}

// 載入對話歷史
function loadChatHistory() {
    try {
        const savedHistory = localStorage.getItem('chatHistory');
        const savedQueryCount = localStorage.getItem('queryCount');
        const savedTotalTime = localStorage.getItem('totalResponseTime');

        if (savedHistory) {
            chatHistory = JSON.parse(savedHistory);
            queryCount = parseInt(savedQueryCount) || 0;
            totalResponseTime = parseFloat(savedTotalTime) || 0;

            console.log(`📚 載入 ${chatHistory.length} 條歷史對話`);

            // 移除歡迎訊息
            const welcome = document.querySelector('.welcome-message');
            if (welcome && chatHistory.length > 0) {
                welcome.remove();
            }

            // 重新顯示所有對話
            chatHistory.forEach(msg => {
                addMessageToDOM(msg.type, msg.content, msg.meta);
            });

            // 更新統計
            if (queryCount > 0) {
                const avgTime = (totalResponseTime / queryCount).toFixed(2);
                document.getElementById('responseTime').textContent = `${avgTime}s`;
                document.getElementById('sessionStats').innerHTML = `
                    查詢次數: <strong>${queryCount}</strong><br>
                    平均響應: <strong>${avgTime}s</strong>
                `;
            }
        }
    } catch (error) {
        console.error('載入歷史失敗:', error);
    }
}

// 清除對話
function clearChat() {
    if (confirm('確定要清除所有對話記錄嗎？')) {
        console.log('🗑️ 清除對話');
        
        // 清除變數
        chatHistory = [];
        queryCount = 0;
        totalResponseTime = 0;

        // 清除 localStorage
        localStorage.removeItem('chatHistory');
        localStorage.removeItem('queryCount');
        localStorage.removeItem('totalResponseTime');

        // 清除 DOM
        const messagesDiv = document.getElementById('messages');
        messagesDiv.innerHTML = `
            <div class="welcome-message">
                <h2>👋 歡迎使用 RAG 流式系統</h2>
                <p>我可以回答關於 IP 位址、網路協定和 DNS 系統的問題</p>
                
                <div class="example-queries">
                    <div class="example-query" onclick="sendExample('什麼是 IPv4 和 IPv6？')">
                        <strong>💡 基礎問題</strong>
                        什麼是 IPv4 和 IPv6？
                    </div>
                    <div class="example-query" onclick="sendExample('NAT 和 PAT 有什麼不同？')">
                        <strong>🔍 比較問題</strong>
                        NAT 和 PAT 有什麼不同？
                    </div>
                    <div class="example-query" onclick="sendExample('請說明 DNS 解析的完整流程')">
                        <strong>📖 深入問題</strong>
                        請說明 DNS 解析的完整流程
                    </div>
                </div>
            </div>
        `;

        // 重置統計
        document.getElementById('responseTime').textContent = '-';
        document.getElementById('sessionStats').innerHTML = `
            查詢次數: <strong>0</strong><br>
            平均響應: <strong>-</strong>
        `;

        console.log('✅ 對話已清除');
    }
}

// 添加訊息到 DOM（不保存到歷史）
function addMessageToDOM(type, content, meta = null) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${type}`;

    let metaHTML = '';
    if (meta) {
        const dimensionsHTML = meta.dimensions ? `
            <div class="dimensions">
                <span class="badge badge-primary">K: ${meta.dimensions.K !== undefined ? meta.dimensions.K : '未知'}</span>
                <span class="badge badge-success">C: ${meta.dimensions.C !== undefined ? meta.dimensions.C : '未知'}</span>
                <span class="badge badge-warning">R: ${meta.dimensions.R !== undefined ? meta.dimensions.R : '未知'}</span>
            </div>
        ` : '';

        metaHTML = `
            <div class="message-meta">
                <span>⏱️ ${meta.response_time}s</span>
                <span>📄 ${meta.matched_docs?.length || 0} 個文件</span>
                ${meta.scenario ? `<span>🎯 ${meta.scenario}</span>` : ''}
            </div>
            ${dimensionsHTML}
        `;
    }

    const displayContent = content || '(空內容)';

    messageDiv.innerHTML = `
        <div class="message-content">
            ${displayContent.replace(/\n/g, '<br>')}
            ${metaHTML}
        </div>
    `;

    messagesDiv.appendChild(messageDiv);
    
    setTimeout(() => {
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }, 100);
}
