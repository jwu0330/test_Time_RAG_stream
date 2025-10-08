"""
時間測量工具模組
用於精準記錄各階段執行時間
支援雙線程（Thread A: RAG, Thread B: Scenario）獨立計時
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
    """線程計時報告"""
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
    thread_a_report: Optional[ThreadTimingReport] = None  # 主線：RAG
    thread_b_report: Optional[ThreadTimingReport] = None  # 分支：情境判定
    total_time: float = 0.0
    timestamp: str = ""
    
    def to_dict(self) -> dict:
        """轉換為字典格式"""
        result = {
            "timestamp": self.timestamp,
            "stages": self.records,
            "total_time": round(self.total_time, 3)
        }
        
        # 添加線程詳細報告
        if self.thread_a_report:
            result["thread_a"] = self.thread_a_report.to_dict()
        if self.thread_b_report:
            result["thread_b"] = self.thread_b_report.to_dict()
        
        return result


class Timer:
    """計時器管理類 - 支援雙線程獨立計時"""
    
    def __init__(self):
        self.records: Dict[str, TimerRecord] = {}
        self.thread_a_records: Dict[str, TimerRecord] = {}  # Thread A (RAG)
        self.thread_b_records: Dict[str, TimerRecord] = {}  # Thread B (Scenario)
        self.start_time = time.perf_counter()
    
    def start_stage(self, stage_name: str, thread: Optional[str] = None):
        """
        開始某個階段的計時
        
        Args:
            stage_name: 階段名稱
            thread: 線程標識 ('A' 或 'B')，None 表示主流程
        """
        if thread == 'A':
            if stage_name not in self.thread_a_records:
                self.thread_a_records[stage_name] = TimerRecord(name=stage_name)
            self.thread_a_records[stage_name].start()
        elif thread == 'B':
            if stage_name not in self.thread_b_records:
                self.thread_b_records[stage_name] = TimerRecord(name=stage_name)
            self.thread_b_records[stage_name].start()
        else:
            if stage_name not in self.records:
                self.records[stage_name] = TimerRecord(name=stage_name)
            self.records[stage_name].start()
    
    def stop_stage(self, stage_name: str, thread: Optional[str] = None) -> float:
        """
        停止某個階段的計時
        
        Args:
            stage_name: 階段名稱
            thread: 線程標識 ('A' 或 'B')，None 表示主流程
            
        Returns:
            該階段的持續時間
        """
        if thread == 'A':
            if stage_name in self.thread_a_records:
                duration = self.thread_a_records[stage_name].stop()
                return duration
        elif thread == 'B':
            if stage_name in self.thread_b_records:
                duration = self.thread_b_records[stage_name].stop()
                return duration
        else:
            if stage_name in self.records:
                duration = self.records[stage_name].stop()
                return duration
        return 0.0
    
    def get_report(self) -> TimerReport:
        """生成完整報告"""
        report = TimerReport()
        report.timestamp = datetime.now().isoformat()
        
        # 主流程記錄
        for name, record in self.records.items():
            report.records[name] = round(record.duration, 3)
        
        # Thread A 報告
        if self.thread_a_records:
            thread_a_report = ThreadTimingReport(thread_name="Thread A (RAG)")
            thread_a_total = 0.0
            for name, record in self.thread_a_records.items():
                duration = round(record.duration, 3)
                thread_a_report.stages[name] = duration
                thread_a_total += duration
            thread_a_report.total_time = round(thread_a_total, 3)
            report.thread_a_report = thread_a_report
        
        # Thread B 報告
        if self.thread_b_records:
            thread_b_report = ThreadTimingReport(thread_name="Thread B (Scenario)")
            thread_b_total = 0.0
            for name, record in self.thread_b_records.items():
                duration = round(record.duration, 3)
                thread_b_report.stages[name] = duration
                thread_b_total += duration
            thread_b_report.total_time = round(thread_b_total, 3)
            report.thread_b_report = thread_b_report
        
        report.total_time = round(time.perf_counter() - self.start_time, 3)
        return report
    
    def print_report(self):
        """打印報告"""
        report = self.get_report()
        print("\n" + "="*70)
        print("⏱️  時間分析報告（雙線程）")
        print("="*70)
        
        # 主流程
        if report.records:
            print("\n【主流程】")
            for stage, duration in report.records.items():
                print(f"  {stage:30s}: {duration:6.3f}s")
        
        # Thread A
        if report.thread_a_report:
            print(f"\n【{report.thread_a_report.thread_name}】")
            for stage, duration in report.thread_a_report.stages.items():
                print(f"  {stage:30s}: {duration:6.3f}s")
            print(f"  {'Thread A 小計':30s}: {report.thread_a_report.total_time:6.3f}s")
        
        # Thread B
        if report.thread_b_report:
            print(f"\n【{report.thread_b_report.thread_name}】")
            for stage, duration in report.thread_b_report.stages.items():
                print(f"  {stage:30s}: {duration:6.3f}s")
            print(f"  {'Thread B 小計':30s}: {report.thread_b_report.total_time:6.3f}s")
        
        print("\n" + "-"*70)
        print(f"  {'總計（從後端接收到渲染完成）':30s}: {report.total_time:6.3f}s")
        print("="*70 + "\n")
