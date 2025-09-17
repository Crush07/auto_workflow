from loguru import logger
import os
import time
import pyautogui
# 从pyscreeze导入ImageNotFoundException异常类
from pyscreeze import ImageNotFoundException
from ..base_action_node import BaseActionNode
from ..for_loop_node import ForLoopNode


# 单次屏幕识别方法（从pyscreeze复制并修改，移除while循环）
def locateOnScreenOnce(image, **kwargs):
    """执行单次屏幕识别，不进行循环查找
    从pyscreeze的locateOnScreen方法修改而来，只识别一次屏幕
    """
    try:
        # 截取整个屏幕
        screenshotIm = pyautogui.screenshot(region=None)
        retVal = pyautogui.locate(image, screenshotIm, **kwargs)
        try:
            screenshotIm.fp.close()
        except AttributeError:
            # Windows上的截图不会有fp，因为它们来自ImageGrab而不是文件
            # Linux上的截图fp会被设置为None，因为文件已被解除链接
            pass
        return retVal
    except ImageNotFoundException:
        return None

# 内部的点击动作节点
class ClickAction(BaseActionNode):
    def __init__(self, parent_node):
        super().__init__()
        self.parent_node = parent_node
        self.found = False
    
    def execute(self):
        try:
            # 使用我们新创建的单次识别方法替代pyautogui.locateOnScreen
            locals = locateOnScreenOnce(self.parent_node.image_path, confidence=0.95)
            if locals:
                x, y, width, height = locals
                
                # 计算图像中心点坐标
                center_x = x + width // 2
                center_y = y + height // 2
                
                pyautogui.moveTo(center_x, center_y, duration=0.3)
                # 根据click_count执行连续点击
                if self.parent_node.click_count > 1:
                    pyautogui.click(clicks=self.parent_node.click_count, interval=0.3)
                else:
                    pyautogui.click(interval=0.3)
                
                # 记录点击次数和成功信息
                logger.info(f"点击次数: {self.parent_node.click_count}")
                logger.success(f"成功点击按钮: {self.parent_node.get_description()} (尝试次数: {self.parent_node.attempt_count})")
                self.found = True
            else:
                # 未找到图像
                status_msg = f"第{self.parent_node.attempt_count}次尝试未找到按钮，正在继续查找..."
                if self.parent_node.attempt_count % 5 == 0:  # 每5次尝试显示一次详细错误信息
                    status_msg += f" (未找到匹配图像)"
                logger.info(status_msg)
            
        except FileNotFoundError as e:
            logger.error(f"错误: 图像文件不存在: {e}")
            self.found = True  # 文件不存在，停止尝试
        except Exception as e:
            # 其他错误
            status_msg = f"第{self.parent_node.attempt_count}次尝试发生错误: {str(e)}"
            logger.error(status_msg)
            
        # 添加短暂延迟，避免过于频繁地查找
        time.sleep(2)

# 点击按钮节点类
class ButtonClickNode(ForLoopNode):
    def __init__(self, image_path="", click_count=1):
        # 先初始化属性，再调用父类初始化
        self.image_path = image_path  # 按钮图片位置
        self.click_count = max(1, click_count)  # 连续点击次数，至少为1
        self.attempt_count = 0  # 尝试次数计数
        
        # 调用父类构造函数，设置循环次数为10次
        super().__init__(loop_count=10, is_infinite=False)
        
        # 创建点击动作并添加到循环中
        self.click_action = ClickAction(self)
        self.add_action(self.click_action)
        logger.info(f"创建按钮点击节点: {self.get_description()}")
    
    def to_dict(self):
        """转换为字典格式以便保存"""
        # 调用父类的to_dict方法获取基础信息
        result = super().to_dict()
        # 添加按钮点击特有的属性
        result.update({
            "type": "button",
            "image_path": self.image_path,
            "click_count": self.click_count
        })
        return result
    
    @classmethod
    def from_dict(cls, data):
        """从字典格式创建对象"""
        node = cls(
            image_path=data.get("image_path", ""),
            click_count=data.get("click_count", 1)
        )
        return node
    
    def get_description(self):
        """获取动作描述"""
        filename = os.path.basename(self.image_path) if self.image_path else "未设置"
        if self.click_count > 1:
            return f"点击按钮 {filename} ({self.click_count}次)"
        else:
            return f"点击按钮: {filename}"
    
    # 重写父类方法，确保before_execute和after_execute被调用
    def execute(self):
        self.before_execute()
        
        if not self.image_path or not os.path.exists(self.image_path):
            logger.error(f"错误: 图像文件不存在或路径为空")
            self.after_execute()
            return
        
        logger.info(f"开始查找按钮: {self.get_description()}")
        
        # 重置状态
        self.attempt_count = 0
        self.click_action.found = False
        
        # 执行循环查找
        while self.attempt_count < self.loop_count and not self.click_action.found:
            self.attempt_count += 1
            # 执行一次循环
            for action in self.actions:
                action.execute()
                time.sleep(0.1)  # 短暂延迟
            
        if self.attempt_count >= self.loop_count and not self.click_action.found:
            logger.warning(f"达到最大尝试次数({self.loop_count})，停止查找按钮")
            
        self.after_execute()