import time
from wxauto import WeChat
import os
import time
from loguru import logger

def getMessageList():
    try:
        logger.info("开始获取微信消息列表")
        wx = WeChat()

        wx.ChatWith("文件传输助手")
        messages = wx.GetAllMessage()
        wx.Close()
        logger.debug(f"获取到{len(messages)}条消息")

        # 使用绝对路径存储聊天记录
        chat_file_path = os.path.join(os.path.dirname(__file__), "chat.txt")
        
        # 每一次获取消息都更新到文件夹的聊天文件中，对比是否有新消息
        oldMessageStr = ""
        if os.path.exists(chat_file_path):
            with open(chat_file_path, "r", encoding='utf-8') as f:
                oldMessageList = f.readlines()
            oldMessageStr = "".join(oldMessageList)

        currentAllMessageList = get_new_messages(messages)
        currentAllMessageStr = "&join;".join(currentAllMessageList)

        # current_messages写入到chat.txt文件中
        with open(chat_file_path, "w", encoding='utf-8') as f:
            f.write(currentAllMessageStr)

        # 剩余消息
        newMessageStr = currentAllMessageStr.replace(oldMessageStr, "")
        newMessageList = newMessageStr.split("&join;")
        
        # 记录新消息
        for newMessage in newMessageList:
            if newMessage.strip():
                logger.info(f"新消息: {newMessage}")
    except Exception as e:
        logger.error(f"获取微信消息时出错: {e}")

def get_new_messages(messages):
    logger.debug("开始筛选新消息")
    current_messages = []
    for message in messages:
        if message.attr == 'self' and message.type == "text":
            current_messages.append(message.content)
    logger.debug(f"筛选出{len(current_messages)}条新消息")
    return current_messages

def start_monitoring():
    logger.info("开始微信消息监控")
    while True:
        getMessageList()
        time.sleep(3)

if __name__ == "__main__":
    # 默认启动监控
    logger.info("启动微信消息监控程序")
    
    try:
        start_monitoring()
    except KeyboardInterrupt:
        # 当用户在程序运行时按下Ctrl+C，Python会抛出这个异常，从而触发except块中的代码。
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序异常终止: {e}")

