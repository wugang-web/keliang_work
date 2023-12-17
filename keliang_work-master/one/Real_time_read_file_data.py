import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sys


class Application(tk.Frame):
    def __init__(self, master=None, txt='Sine_Wave_output.txt'):
        super().__init__(master)
        self.master = master
        self.pack()
        self.txt = txt
        self.create_widgets()

    def create_widgets(self):
        # 创建画布和坐标轴
        self.fig, self.ax = plt.subplots(figsize=(6, 4))

        # 设置弹窗的位置
        popup_x = 1500  # 加向右
        popup_y = 400
        self.master.geometry(f"+{popup_x}+{popup_y}")
        # 设置窗口标题
        self.master.title(self.txt)
        # 创建画布控件
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack()

        # 启动定时器
        self.update_chart()

    def update_chart(self):
        try:
            # 读取文件内容
            data = np.loadtxt(self.txt)

            # 生成时间戳
            timestamps = np.arange(len(data))

            # 清除原有图形
            self.ax.clear()

            # 绘制新图形
            self.ax.plot(timestamps, data, '-')

            # 在每个点上添加文本标签
            for x, y in zip(timestamps, data):
                self.ax.text(x, y, f'{y:.2f}', fontsize=0, ha='center', va='bottom')

            # 显示网格线
            self.ax.grid(True)
            self.ax.set_xlabel('Timestamp')
            self.ax.set_ylabel('Data')
            self.ax.set_title(self.txt)


            # 更新画布
            self.canvas.draw()

        except Exception as e:
            # 处理异常，避免程序崩溃
            pass
            # print(f"Error: {e}")

        # 下一次更新的时间间隔（单位是毫秒）
        interval = 1  # 设置为50毫秒

        # 启动下一次定时器
        self.master.after(interval, self.update_chart)


if __name__ == '__main__':
    # 获取命令行参数
    if len(sys.argv) > 1:
        txt_file = sys.argv[1]
    else:
        txt_file = 'Sine_Wave_output.txt'

    root = tk.Tk()
    app = Application(master=root, txt=txt_file)
    app.mainloop()
