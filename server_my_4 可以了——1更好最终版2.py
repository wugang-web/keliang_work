import rethinkdb as r
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

class SensorDataPlotter:
    def __init__(self, host, num_sensors):

        self.r = r.connect(host='127.0.0.1', port=28015).repl()
        self.data_queues = [deque(maxlen=100) for _ in range(num_sensors)]
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(20, 9)
        self.ax_play_pause = plt.axes([0.9, 0.8, 0.09, 0.05])
        self.btn_play_pause = plt.Button(self.ax_play_pause, 'Pause')
        self.hide_show_buttons = []
        self.lines = []  # 存储每个传感器对应的线条对象列表
        for i in range(num_sensors):
            ax_hide_show = plt.axes([0.9, 0.7 - i * 0.05, 0.09, 0.05])
            btn_hide_show = plt.Button(ax_hide_show, f'Hide {i + 1}')
            self.hide_show_buttons.append(btn_hide_show)
        self.btn_play_pause.on_clicked(self.play_pause)
        for i, btn_hide_show in enumerate(self.hide_show_buttons):
            btn_hide_show.on_clicked(lambda _, index=i: self.hide_show(index))
        self.paused = False
        self.hidden = [False] * num_sensors
        self.ax.tick_params(axis='x', rotation=45)
        self.fig.canvas.mpl_connect('scroll_event', self.zoom)
        self.xmin = None
        self.xmax = None
        self.ymin = None
        self.ymax = None
        self.last_frame_last_data_index = [-1] * num_sensors
        self.max_ids = []
        self.changefeeds = []


    def plot_sensor_data(self, table_names, batch_size):
        num_sensors = len(table_names)

        def update(frame):
            if not self.paused:
                for i in range(num_sensors):
                    cursor = list(r.db("test").table(table_names[i]).run(self.r))
                    # print(cursor)
                    if cursor:
                        min_timestamp = min(cursor, key=lambda x: x['timestamp'])['timestamp']
                        max_timestamp = max(cursor, key=lambda x: x['timestamp'])['timestamp']
                        b = list(r.db("test").table(table_names[i]).order_by('timestamp').run(self.r))
                        print(len(b))

                        cursor = list(r.db("test").table(table_names[i]).run(self.r))
                        min_timestamp = min(cursor, key=lambda x: x['timestamp'])['timestamp']

                        end_id = max(r.db("test").table(table_names[i]).run(self.r), key=lambda x: x['timestamp'])['timestamp']
                        print(min_timestamp,end_id)
                        results = r.db("test").table(table_names[i]).order_by('timestamp').filter(
                            lambda doc: (doc['timestamp'] >= min_timestamp) & (doc['timestamp'] <= end_id)).run(self.r)
                        result = list(results)
                        print(len(result))
                        timestamps = [data['timestamp'] for data in result]
                        data = [data['data'] for data in result]
                        legend_name = [data['legend_name'] for data in result]
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
                            print(recent_timestamps)
                            self.xmin = min(recent_timestamps)
                            self.xmax = max(recent_timestamps)

                self.ax.legend(loc='upper right', fontsize=12)

                if self.xmin and self.xmax and self.ymin and self.ymax:
                    self.ax.set_xlim(self.xmin, self.xmax)
                    self.ax.set_ylim(self.ymin, self.ymax)

                self.fig.canvas.draw()  # 强制图表更新

        anim = FuncAnimation(self.fig, update, frames=range(0, 500 // batch_size), interval=1)

        plt.show()

    def play_pause(self, event):
        self.paused = not self.paused
        if self.paused:
            self.btn_play_pause.label.set_text('Resume')
        else:
            self.btn_play_pause.label.set_text('Pause')

    def hide_show(self, index):
        self.hidden[index] = not self.hidden[index]
        if self.hidden[index]:
            self.hide_show_buttons[index].label.set_text(f'Show {index + 1}')
            self.lines[index].set_visible(False)
        else:
            self.hide_show_buttons[index].label.set_text(f'Hide {index + 1}')
            self.lines[index].set_visible(True)
        self.fig.canvas.draw()

    def zoom(self, event):
        if event.inaxes == self.ax:
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

    def close(self):
        r.connect().close()

plotter = SensorDataPlotter(host='localhost', num_sensors=11)
plotter.plot_sensor_data(table_names=['sin_data_500Hz', 'sin_data_1000Hz', 'sin_data_100Hz',
                                      'sin_data_500Hz', 'sin_data_1000Hz', 'sin_data_100Hz',
                                      'sin_data_500Hz', 'sin_data_1000Hz', 'sin_data_100Hz',
                                      'sin_data_500Hz','sin_data_500Hz'],
                         batch_size=10)
plotter.close()
