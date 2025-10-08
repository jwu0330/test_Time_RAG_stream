"""
時間測量工具模組
用於精準記錄各階段執行時間
"""
import time
from typing import Dict, List
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
class TimerReport:
    """完整計時報告"""
    records: Dict[str, float] = field(default_factory=dict)
    total_time: float = 0.0
    timestamp: str = ""
    
    def to_dict(self) -> dict:
        """轉換為字典格式"""
        return {
            "timestamp": self.timestamp,
            "stages": self.records,
            "total_time": round(self.total_time, 3)
        }


class Timer:
    """計時器管理類"""
    
    def __init__(self):
        self.records: Dict[str, TimerRecord] = {}
        self.start_time = time.perf_counter()
    
    def start_stage(self, stage_name: str):
        """開始某個階段的計時"""
        if stage_name not in self.records:
            self.records[stage_name] = TimerRecord(name=stage_name)
        self.records[stage_name].start()
    
    def stop_stage(self, stage_name: str) -> float:
        """停止某個階段的計時"""
        if stage_name in self.records:
            duration = self.records[stage_name].stop()
            return duration
        return 0.0
    
    def get_report(self) -> TimerReport:
        """生成完整報告"""
        report = TimerReport()
        report.timestamp = datetime.now().isoformat()
        
        for name, record in self.records.items():
            report.records[name] = round(record.duration, 3)
        
        report.total_time = round(time.perf_counter() - self.start_time, 3)
        return report
    
    def print_report(self):
        """打印報告"""
        report = self.get_report()
        print("\n" + "="*50)
        print("⏱️  時間分析報告")
        print("="*50)
        for stage, duration in report.records.items():
            print(f"  {stage:20s}: {duration:6.3f}s")
        print("-"*50)
        print(f"  {'總計':20s}: {report.total_time:6.3f}s")
        print("="*50 + "\n")
