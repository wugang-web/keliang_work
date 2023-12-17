import rethinkdb as r  # 导入rethinkdb模块
import matplotlib.pyplot as plt  # 导入matplotlib中的pyplot模块
from matplotlib.animation import FuncAnimation  # 从matplotlib的animation模块中导入FuncAnimation类
from collections import deque  # 导入collections模块中的deque类
import sys
import os

class SensorDataPlotter:  # 定义SensorDataPlotter类
    def __init__(self, host, num_sensors):  # 初始化方法，传入host和num_sensors参数
        # 连接到RethinkDB服务器
        self.r = r.connect(host=host, port=28015).repl()
        # 创建一个长度为100的双向队列列表，用于存储传感器数据
        self.data_queues = [deque(maxlen=100) for _ in range(num_sensors)]
        # 创建图形和子图对象
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(20, 9)
        # 创建暂停/播放按钮
        self.ax_play_pause = plt.axes([0.9, 0.8, 0.09, 0.05])
        self.btn_play_pause = plt.Button(self.ax_play_pause, 'Pause')
        self.hide_show_buttons = []  # 隐藏/显示按钮列表
        self.lines = []  # 存储每个传感器对应的线条对象列表
        for i in range(num_sensors):
            # 创建隐藏/显示按钮
            ax_hide_show = plt.axes([0.9, 0.7 - i * 0.05, 0.09, 0.05])
            btn_hide_show = plt.Button(ax_hide_show, f'Hide {i + 1}')
            self.hide_show_buttons.append(btn_hide_show)
        # 将按钮的点击事件绑定到相应的方法
        self.btn_play_pause.on_clicked(self.play_pause)
        for i, btn_hide_show in enumerate(self.hide_show_buttons):
            btn_hide_show.on_clicked(lambda _, index=i: self.hide_show(index))
        # 初始化参数
        self.paused = False
        self.hidden = [False] * num_sensors
        self.ax.tick_params(axis='x', rotation=45)
        self.fig.canvas.mpl_connect('scroll_event', self.zoom)
        self.xmin = None
        self.xmax = None
        self.ymin = -2
        self.ymax = 2
        self.last_frame_last_data_index = [-1] * num_sensors
        self.max_ids = []
        self.changefeeds = []

    def plot_sensor_data(self, table_names, batch_size):  # 绘制传感器数据的方法，传入table_names和batch_size参数
        num_sensors = len(table_names)

        def update(frame):  # 更新方法，传入帧参数
            if not self.paused:  # 如果未暂停，则执行更新操作
                for i in range(num_sensors):
                    # 获取传感器数据
                    cursor = list(r.db("test").table(table_names[i]).run(self.r))
                    if cursor:
                        # 获取最小和最大时间戳
                        min_timestamp = min(cursor, key=lambda x: x['timestamp'])['timestamp']
                        max_timestamp = max(cursor, key=lambda x: x['timestamp'])['timestamp']
                        # 计算传感器数据长度
                        b = list(r.db("test").table(table_names[i]).order_by('timestamp').run(self.r))

                        # 重新获取最小时间戳
                        cursor = list(r.db("test").table(table_names[i]).run(self.r))
                        min_timestamp = min(cursor, key=lambda x: x['timestamp'])['timestamp']

                        # 获取最大时间戳
                        end_id = max(r.db("test").table(table_names[i]).run(self.r), key=lambda x: x['timestamp'])[
                            'timestamp']
                        # 通过时间戳筛选数据
                        results = r.db("test").table(table_names[i]).order_by('timestamp').filter(
                            lambda doc: (doc['timestamp'] >= min_timestamp) & (doc['timestamp'] <= end_id)).run(self.r)
                        result = list(results)
                        timestamps = [data['timestamp'] for data in result]
                        data = [data['data'] for data in result]
                        legend_name = [data['legend_name'] for data in result]
                        # 将数据加入到队列中
                        self.data_queues[i].extend(zip(timestamps, data, legend_name))
                        self.last_frame_last_data_index[i] = end_id

                for i in range(num_sensors):
                    if not self.hidden[i]:
                        recent_data = list(self.data_queues[i])
                        recent_timestamps = [data[0] for data in recent_data]
                        recent_values = [data[1] for data in recent_data]
                        recent_legend_name = [data[2] for data in recent_data]

                        # 如果该传感器的线条还没有被绘制，则创建一个新的线条对象
                        if i >= len(self.lines):
                            line, = self.ax.plot(recent_timestamps, recent_values, label=recent_legend_name[0],
                                                 color=f'C{i}')
                            self.lines.append(line)
                        else:
                            # 否则，只更新线条的数据点
                            line = self.lines[i]
                            line.set_xdata(recent_timestamps)
                            line.set_ydata(recent_values)

                        # 更新x轴范围
                        if recent_timestamps:
                            self.xmin = min(recent_timestamps)
                            self.xmax = max(recent_timestamps)

                self.ax.legend(loc='upper right', fontsize=12)

                if self.xmin and self.xmax and self.ymin and self.ymax:
                    self.ax.set_xlim(self.xmin, self.xmax)
                    self.ax.set_ylim(self.ymin, self.ymax)

                self.fig.canvas.draw()  # 强制图表更新

        # 创建动画对象
        anim = FuncAnimation(self.fig, update, frames=range(0, 500 // batch_size), interval=10)

        plt.show()  # 显示图表

    def play_pause(self, event):  # 播放/暂停方法，传入事件参数
        self.paused = not self.paused
        if self.paused:
            self.btn_play_pause.label.set_text('Resume')  # 如果暂停，则设置按钮文本为"Resume"
        else:
            self.btn_play_pause.label.set_text('Pause')  # 如果播放，则设置按钮文本为"Pause"

    def hide_show(self, index):  # 隐藏/显示方法，传入索引参数
        self.hidden[index] = not self.hidden[index]
        if self.hidden[index]:
            self.hide_show_buttons[index].label.set_text(f'Show {index + 1}')  # 如果隐藏，则设置按钮文本为"Show"
            self.lines[index].set_visible(False)
        else:
            self.hide_show_buttons[index].label.set_text(f'Hide {index + 1}')  # 如果显示，则设置按钮文本为"Hide"
            self.lines[index].set_visible(True)
        self.fig.canvas.draw()

    def zoom(self, event):  # 缩放方法，传入事件参数
        if event.inaxes == self.ax:  # 如果事件发生在子图上
            self.fig.canvas.toolbar.push_current()
            xmin, xmax = self.ax.get_xlim()
            ymin, ymax = self.ax.get_ylim()
            scale_factor = 1.2 if event.button == 'up' else 0.8
            new_xmin = xmin * scale_factor
            new_xmax = xmax * scale_factor
            new_ymin = ymin * scale_factor
            new_ymax = ymax * scale_factor
            self.ax.set_xlim(new_xmin, new_xmax)
            self.ax.set_ylim(new_ymin, new_ymax)
            self.xmin = new_xmin
            self.xmax = new_xmax
            self.ymin = new_ymin
            self.ymax = new_ymax
            self.fig.canvas.draw()

    def close(self):  # 关闭方法
        r.connect().close()


if __name__ == "__main__":
    # 构建配置文件的完整路径
    file_path = r"./config.txt"

    # 读取配置文件内容
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 解析配置文件内容
    config = {}
    for line in lines:
        if "=" in line:
            key, value = line.strip().split("=")
            config[key.strip()] = value.strip()

    # 使用配置文件中的值
    database_host = config.get('hostname')
    num_sensors = int(config.get('num_sensors'))
    table_names = eval(config.get('table_names'))
    print(database_host,type(database_host))

    # 创建SensorDataPlotter对象
    plotter = SensorDataPlotter(host=database_host, num_sensors=num_sensors)

    # 调用plot_sensor_data方法
    plotter.plot_sensor_data(table_names=table_names,
                             batch_size=10)

    plotter.close()  # 关闭连接
