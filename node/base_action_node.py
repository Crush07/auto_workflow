# 基础动作节点类
class BaseActionNode:

    # id，全局唯一
    id = None
    # 前置动作node，类型是BaseActionNode
    pre_action_node = []
    # 后置动作node，类型是BaseActionNode
    post_action_node = []

    def __init__(self):
        pass

    def before_execute(self):
        """在执行动作前调用"""
        for node in self.pre_action_node:
            node.execute()
        pass
    
    def execute(self):
        """执行动作"""
        pass

    def after_execute(self):
        """在执行动作后调用"""
        for node in self.post_action_node:
            node.execute()
        pass
    
    def to_dict(self):
        """转换为字典格式以便保存"""
        return {
            "type": "base"
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典格式创建对象"""
        return cls()
    
    def get_description(self):
        """获取动作描述"""
        return "基础动作"