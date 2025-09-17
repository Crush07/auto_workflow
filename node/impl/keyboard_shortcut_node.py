from loguru import logger
import pyautogui
import threading
# 使用相对导入
from ..base_action_node import BaseActionNode

# pyautogui.PAUSE = 1
# 快捷键节点类
class KeyboardShortcutNode(BaseActionNode):
    def __init__(self, shortcut=""):
        # 先初始化属性，再调用父类初始化
        self.shortcut = shortcut  # 快捷键拼接字符串
        super().__init__()
        logger.info(f"创建快捷键节点: {shortcut}")
    
    def execute(self):
        self.before_execute()
        """执行快捷键的内部方法"""
        if self.shortcut:
            # 转为小写
            lowerShortcut = self.shortcut.lower()
            if(lowerShortcut == "win+d"):
                # 特殊处理win+d
                logger.info(f"执行特殊快捷键: {self.shortcut}")
                pyautogui.keyDown("win")
                pyautogui.press("d")
                pyautogui.keyUp("win")
            else:
                # 解析并执行快捷键
                logger.info(f"执行快捷键: {self.shortcut}")
                pyautogui.hotkey(*lowerShortcut.split('+'))
        else:
            logger.warning(f"快捷键未设置")
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