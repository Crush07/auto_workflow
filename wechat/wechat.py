import time
from wxauto import WeChat

def getMessageList():
    wx = WeChat()

    wx.ChatWith("文件传输助手")
    messages = wx.GetAllMessage()
    wx.Close()

    # 每一次获取消息都更新到文件夹的聊天文件中，对比是否有新消息
    with open("chat.txt", "r", encoding='utf-8') as f:
        oldMessageList = f.readlines()
    oldMessageStr = "".join(oldMessageList)

    currentAllMessageList = get_new_messages(messages)
    currentAllMessageStr = "&join;".join(currentAllMessageList)

    # current_messages写入到chat.txt文件中
    with open("chat.txt", "w", encoding='utf-8') as f:
        f.write(currentAllMessageStr)

    # 剩余消息
    newMessageStr = currentAllMessageStr.replace(oldMessageStr, "")
    newMessageList = newMessageStr.split("&join;")

    # 打印新消息
    for newMessage in newMessageList:
        print(newMessage)

def get_new_messages(messages):
    current_messages = []
    for message in messages:
        if message.attr == 'self' and message.type == "text":
            current_messages.append(message.content)
    return current_messages

def start_monitoring():
    while True:
        getMessageList()
        time.sleep(3)

if __name__ == "__main__":
    # 默认启动监控
    print("启动微信消息监控程序")
    
    try:
        start_monitoring()
    except KeyboardInterrupt:
        # 当用户在程序运行时按下Ctrl+C，Python会抛出这个异常，从而触发except块中的代码。
        print("\n程序被用户中断")

