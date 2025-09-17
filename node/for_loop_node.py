import time
from loguru import logger
# 使用相对导入
from .base_action_node import BaseActionNode

# For循环节点类
class ForLoopNode(BaseActionNode):
    def __init__(self, loop_count=1, is_infinite=False):
        # 先初始化属性，再调用父类初始化
        self.loop_count = max(1, loop_count)  # 循环次数，至少为1
        self.is_infinite = is_infinite  # 是否无限循环
        self.actions = []  # 一次循环内要执行的动作列表
        
        super().__init__()
        logger.info(f"创建循环节点: {self.get_description()}")
        
    def add_action(self, action_node):
        """添加一个要在循环中执行的动作节点"""
        if isinstance(action_node, BaseActionNode) and action_node not in self.actions:
            self.actions.append(action_node)
    
    def remove_action(self, action_node):
        """移除一个在循环中执行的动作节点"""
        if action_node in self.actions:
            self.actions.remove(action_node)
    
    def execute(self):
        """执行循环动作"""
        logger.info(f"开始执行循环节点: {self.get_description()}")
        
        # 执行前置动作
        self.before_execute()
        
        # 循环执行动作列表中的所有动作
        current_loop = 0
        while self.is_infinite or current_loop < self.loop_count:
            current_loop += 1
            logger.info(f"循环执行第 {current_loop} 次")
            
            # 执行一次循环内的所有动作
            for action in self.actions:
                logger.debug(f"在循环第{current_loop}次中执行动作: {action.get_description()}")
                action.execute()
                time.sleep(0.1)  # 短暂延迟，避免执行过快
            
            # 如果不是无限循环，并且已达到循环次数，退出循环
            if not self.is_infinite and current_loop >= self.loop_count:
                break
        
        # 执行后置动作
        self.after_execute()
        logger.info(f"循环节点执行完成: {self.get_description()}")
    
    def to_dict(self):
        """转换为字典格式以便保存"""
        return {
            "type": "for_loop",
            "loop_count": self.loop_count,
            "is_infinite": self.is_infinite,
            "actions": [action.to_dict() for action in self.actions]
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典格式创建对象"""
        # 注意：这里简化了实现，实际使用时需要根据action的type创建对应的节点实例
        node = cls(
            loop_count=data.get("loop_count", 1),
            is_infinite=data.get("is_infinite", False)
        )
        # actions需要在外部添加，因为需要知道具体的节点类型
        return node
    
    def get_description(self):
        """获取动作描述"""
        if self.is_infinite:
            return f"无限循环节点 (包含 {len(self.actions)} 个动作)"
        else:
            return f"循环节点 (循环 {self.loop_count} 次，包含 {len(self.actions)} 个动作)"