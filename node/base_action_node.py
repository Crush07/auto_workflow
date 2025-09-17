# 基础动作节点类
from loguru import logger
import uuid
import time

class BaseActionNode:

    # id，全局唯一
    id = None
    # 前置动作node，类型是BaseActionNode
    pre_action_node = []
    # 后置动作node，类型是BaseActionNode
    post_action_node = []

    def __init__(self):
        # 生成全局唯一ID
        self.id = str(uuid.uuid4())
        logger.info(f"创建节点: {self.get_description()} (ID: {self.id})")

    def before_execute(self):
        """在执行动作前调用"""
        logger.info(f"执行节点前置动作: {self.get_description()} (ID: {self.id})")
        for node in self.pre_action_node:
            logger.info(f"执行前置节点: {node.get_description()} (ID: {node.id})")
            node.execute()
        
    def execute(self):
        """执行动作"""
        logger.info(f"执行节点: {self.get_description()} (ID: {self.id})")

    def after_execute(self):
        """在执行动作后调用"""
        for node in self.post_action_node:
            logger.info(f"执行后置节点: {node.get_description()} (ID: {node.id})")
            node.execute()
        logger.info(f"完成节点执行: {self.get_description()} (ID: {self.id})")
    
    def to_dict(self):
        """转换为字典格式以便保存"""
        data = {
            "id": self.id,
            "type": "base",
            "pre_action_nodes": [node.id for node in self.pre_action_node],
            "post_action_nodes": [node.id for node in self.post_action_node]
        }
        logger.info(f"转换节点为字典: {self.get_description()} (ID: {self.id})")
        return data
    
    @classmethod
    def from_dict(cls, data):
        """从字典格式创建对象"""
        node = cls()
        if "id" in data:
            node.id = data["id"]
        logger.info(f"从字典创建节点: {node.get_description()} (ID: {node.id})")
        return node
    
    def get_description(self):
        """获取动作描述"""
        return "基础动作"