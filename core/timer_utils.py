"""
時間測量工具模組
用於精準記錄各階段執行時間
支援四個並行分支獨立計時：
- Thread A: RAG 檢索
- Thread C: D2 表達錯誤判定 (API)
- Thread D: D3 表達詳細度判定 (API)
- Thread E: D4 知識點檢測 (API)

注：D1 不再是獨立線程，改為從 D4 的二進制編碼本地計算
"""
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TimerRecord:
    """單次計時記錄"""
    name: str
    start_time: float = 0.0
    end_time: float = 0.0
    duration: float = 0.0
    
    def start(self):
        """開始計時"""
        self.start_time = time.perf_counter()
    
    def stop(self):
        """停止計時"""
        self.end_time = time.perf_counter()
        self.duration = self.end_time - self.start_time
        return self.duration


@dataclass
class ThreadTimingReport:
    """並行線程計時報告"""
    thread_name: str
    stages: Dict[str, float] = field(default_factory=dict)
    total_time: float = 0.0
    
    def to_dict(self) -> dict:
        """轉換為字典格式"""
        return {
            "thread_name": self.thread_name,
            "stages": self.stages,
            "total_time": round(self.total_time, 3)
        }


@dataclass
class TimerReport:
    """完整計時報告"""
    records: Dict[str, float] = field(default_factory=dict)
    thread_a_report: Optional[ThreadTimingReport] = None  # Thread A: RAG 檢索
    thread_b_report: Optional[ThreadTimingReport] = None  # Thread B: D1 判定
    thread_c_report: Optional[ThreadTimingReport] = None  # Thread C: D2 判定
    thread_d_report: Optional[ThreadTimingReport] = None  # Thread D: D3 判定
    thread_e_report: Optional[ThreadTimingReport] = None  # Thread E: D4 判定
    total_time: float = 0.0
    timestamp: str = ""
    
    def to_dict(self) -> dict:
        """轉換為字典格式"""
        result = {
            "timestamp": self.timestamp,
            "stages": self.records,
            "total_time": round(self.total_time, 3)
        }
        
        # 添加所有線程詳細報告
        if self.thread_a_report:
            result["thread_a"] = self.thread_a_report.to_dict()
        if self.thread_b_report:
            result["thread_b"] = self.thread_b_report.to_dict()
        if self.thread_c_report:
            result["thread_c"] = self.thread_c_report.to_dict()
        if self.thread_d_report:
            result["thread_d"] = self.thread_d_report.to_dict()
        if self.thread_e_report:
            result["thread_e"] = self.thread_e_report.to_dict()
        
        return result


class Timer:
    """計時器管理類 - 支援四個並行分支獨立計時（Thread A, C, D, E）"""
    
    def __init__(self):
        self.records: Dict[str, TimerRecord] = {}
        self.thread_a_records: Dict[str, TimerRecord] = {}  # Thread A: RAG 檢索
        self.thread_b_records: Dict[str, TimerRecord] = {}  # Thread B: 保留（不再使用）
        self.thread_c_records: Dict[str, TimerRecord] = {}  # Thread C: D2 判定
        self.thread_d_records: Dict[str, TimerRecord] = {}  # Thread D: D3 判定
        self.thread_e_records: Dict[str, TimerRecord] = {}  # Thread E: D4 判定
        self.start_time = time.perf_counter()
    
    def start_stage(self, stage_name: str, thread: Optional[str] = None):
        """
        開始某個階段的計時
        
        Args:
            stage_name: 階段名稱
            thread: 線程標識 ('A', 'B', 'C', 'D', 'E')，None 表示主流程
        """
        if thread == 'A':
            if stage_name not in self.thread_a_records:
                self.thread_a_records[stage_name] = TimerRecord(name=stage_name)
            self.thread_a_records[stage_name].start()
        elif thread == 'B':
            if stage_name not in self.thread_b_records:
                self.thread_b_records[stage_name] = TimerRecord(name=stage_name)
            self.thread_b_records[stage_name].start()
        elif thread == 'C':
            if stage_name not in self.thread_c_records:
                self.thread_c_records[stage_name] = TimerRecord(name=stage_name)
            self.thread_c_records[stage_name].start()
        elif thread == 'D':
            if stage_name not in self.thread_d_records:
                self.thread_d_records[stage_name] = TimerRecord(name=stage_name)
            self.thread_d_records[stage_name].start()
        elif thread == 'E':
            if stage_name not in self.thread_e_records:
                self.thread_e_records[stage_name] = TimerRecord(name=stage_name)
            self.thread_e_records[stage_name].start()
        else:
            if stage_name not in self.records:
                self.records[stage_name] = TimerRecord(name=stage_name)
            self.records[stage_name].start()
    
    def stop_stage(self, stage_name: str, thread: Optional[str] = None) -> float:
        """
        停止某個階段的計時
        
        Args:
            stage_name: 階段名稱
            thread: 線程標識 ('A', 'B', 'C', 'D', 'E')，None 表示主流程
            
        Returns:
            該階段的持續時間
        """
        if thread == 'A':
            if stage_name in self.thread_a_records:
                return self.thread_a_records[stage_name].stop()
        elif thread == 'B':
            if stage_name in self.thread_b_records:
                return self.thread_b_records[stage_name].stop()
        elif thread == 'C':
            if stage_name in self.thread_c_records:
                return self.thread_c_records[stage_name].stop()
        elif thread == 'D':
            if stage_name in self.thread_d_records:
                return self.thread_d_records[stage_name].stop()
        elif thread == 'E':
            if stage_name in self.thread_e_records:
                return self.thread_e_records[stage_name].stop()
        else:
            if stage_name in self.records:
                return self.records[stage_name].stop()
        return 0.0
    
    def get_report(self) -> TimerReport:
        """生成完整報告"""
        report = TimerReport()
        report.timestamp = datetime.now().isoformat()
        
        # 主流程記錄
        for name, record in self.records.items():
            report.records[name] = round(record.duration, 3)
        
        # Thread A 報告（RAG 檢索）
        if self.thread_a_records:
            thread_a_report = ThreadTimingReport(thread_name="Thread A（RAG 檢索）")
            thread_a_total = 0.0
            for name, record in self.thread_a_records.items():
                duration = round(record.duration, 3)
                thread_a_report.stages[name] = duration
                thread_a_total += duration
            thread_a_report.total_time = round(thread_a_total, 3)
            report.thread_a_report = thread_a_report
        
        # Thread B 報告（不再使用，D1 改為本地計算）
        # if self.thread_b_records:
        #     thread_b_report = ThreadTimingReport(thread_name="Thread B（D1 知識點數量）")
        #     thread_b_total = 0.0
        #     for name, record in self.thread_b_records.items():
        #         duration = round(record.duration, 3)
        #         thread_b_report.stages[name] = duration
        #         thread_b_total += duration
        #     thread_b_report.total_time = round(thread_b_total, 3)
        #     report.thread_b_report = thread_b_report
        
        # Thread C 報告（D2 判定）
        if self.thread_c_records:
            thread_c_report = ThreadTimingReport(thread_name="Thread C（D2 表達錯誤）")
            thread_c_total = 0.0
            for name, record in self.thread_c_records.items():
                duration = round(record.duration, 3)
                thread_c_report.stages[name] = duration
                thread_c_total += duration
            thread_c_report.total_time = round(thread_c_total, 3)
            report.thread_c_report = thread_c_report
        
        # Thread D 報告（D3 判定）
        if self.thread_d_records:
            thread_d_report = ThreadTimingReport(thread_name="Thread D（D3 表達詳細度）")
            thread_d_total = 0.0
            for name, record in self.thread_d_records.items():
                duration = round(record.duration, 3)
                thread_d_report.stages[name] = duration
                thread_d_total += duration
            thread_d_report.total_time = round(thread_d_total, 3)
            report.thread_d_report = thread_d_report
        
        # Thread E 報告（D4 判定）
        if self.thread_e_records:
            thread_e_report = ThreadTimingReport(thread_name="Thread E（D4 重複詢問）")
            thread_e_total = 0.0
            for name, record in self.thread_e_records.items():
                duration = round(record.duration, 3)
                thread_e_report.stages[name] = duration
                thread_e_total += duration
            thread_e_report.total_time = round(thread_e_total, 3)
            report.thread_e_report = thread_e_report
        
        report.total_time = round(time.perf_counter() - self.start_time, 3)
        return report
    
    def print_report(self):
        """打印報告"""
        report = self.get_report()
        print("\n" + "="*70)
        print("⏱️  時間分析報告（四個並行分支 + RAG）")
        print("="*70)
        
        # 主流程
        if report.records:
            print("\n【主流程 - 總體時間】")
            for stage, duration in report.records.items():
                print(f"  {stage:35s}: {duration:6.3f}s")
        
        # 計算並行處理的最大時間
        parallel_times = []
        
        # Thread A（RAG 檢索）
        if report.thread_a_report:
            print(f"\n【{report.thread_a_report.thread_name}】")
            for stage, duration in report.thread_a_report.stages.items():
                print(f"  {stage:35s}: {duration:6.3f}s")
            print(f"  {'─' * 45}")
            print(f"  {'小計':35s}: {report.thread_a_report.total_time:6.3f}s")
            parallel_times.append(report.thread_a_report.total_time)
        
        # Thread B（不再使用，D1 改為本地計算）
        # if report.thread_b_report:
        #     print(f"\n【{report.thread_b_report.thread_name}】")
        #     for stage, duration in report.thread_b_report.stages.items():
        #         print(f"  {stage:35s}: {duration:6.3f}s")
        #     print(f"  {'─' * 45}")
        #     print(f"  {'小計':35s}: {report.thread_b_report.total_time:6.3f}s")
        #     parallel_times.append(report.thread_b_report.total_time)
        
        # Thread C（D2 判定）
        if report.thread_c_report:
            print(f"\n【{report.thread_c_report.thread_name}】")
            for stage, duration in report.thread_c_report.stages.items():
                print(f"  {stage:35s}: {duration:6.3f}s")
            print(f"  {'─' * 45}")
            print(f"  {'小計':35s}: {report.thread_c_report.total_time:6.3f}s")
            parallel_times.append(report.thread_c_report.total_time)
        
        # Thread D（D3 判定）
        if report.thread_d_report:
            print(f"\n【{report.thread_d_report.thread_name}】")
            for stage, duration in report.thread_d_report.stages.items():
                print(f"  {stage:35s}: {duration:6.3f}s")
            print(f"  {'─' * 45}")
            print(f"  {'小計':35s}: {report.thread_d_report.total_time:6.3f}s")
            parallel_times.append(report.thread_d_report.total_time)
        
        # Thread E（D4 判定）
        if report.thread_e_report:
            print(f"\n【{report.thread_e_report.thread_name}】")
            for stage, duration in report.thread_e_report.stages.items():
                print(f"  {stage:35s}: {duration:6.3f}s")
            print(f"  {'─' * 45}")
            print(f"  {'小計':35s}: {report.thread_e_report.total_time:6.3f}s")
            parallel_times.append(report.thread_e_report.total_time)
        
        # 顯示並行效率
        if parallel_times:
            max_parallel = max(parallel_times)
            total_sequential = sum(parallel_times)
            efficiency = (1 - max_parallel / total_sequential) * 100 if total_sequential > 0 else 0
            
            print("\n" + "─"*70)
            print(f"  {'並行處理最大時間':35s}: {max_parallel:6.3f}s")
            print(f"  {'若順序執行需要':35s}: {total_sequential:6.3f}s")
            print(f"  {'並行效率提升':35s}: {efficiency:6.1f}%")
        
        print("\n" + "="*70)
        print(f"  {'🎯 總計時間':35s}: {report.total_time:6.3f}s")
        print("="*70 + "\n")
