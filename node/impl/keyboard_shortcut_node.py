import pyautogui
import threading
import pyautogui
# 使用相对导入
from ..base_action_node import BaseActionNode

# pyautogui.PAUSE = 1
# 快捷键节点类
class KeyboardShortcutNode(BaseActionNode):
    def __init__(self, shortcut=""):
        super().__init__()
        self.shortcut = shortcut  # 快捷键拼接字符串
    
    def execute(self):
        self.before_execute()
        """执行快捷键的内部方法"""
        if self.shortcut:
            # 转为小写
            lowerShortcut = self.shortcut.lower()
            if(lowerShortcut == "win+d"):
                # 特殊处理win+d
                pyautogui.keyDown("win")
                pyautogui.press("d")
                pyautogui.keyUp("win")
            else:
                # 解析并执行快捷键
                pyautogui.hotkey(*lowerShortcut.split('+'))
            # 打印日志
            print(f"执行快捷键: {self.shortcut}")
        self.after_execute()
    
    def to_dict(self):
        """转换为字典格式以便保存"""
        return {
            "type": "keyboard",
            "shortcut": self.shortcut
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典格式创建对象"""
        return cls(data.get("shortcut", ""))
    
    def get_description(self):
        """获取动作描述"""
        return f"快捷键: {self.shortcut}"