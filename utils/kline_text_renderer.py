import plotille

class MCPKlineRendererPro:
    def __init__(self, short_recent_data: list):
        self.data = short_recent_data
        self._preprocess()

    def _preprocess(self):
        self.close = [item['Close'] for item in self.data if item.get('Close') is not None]

    def render(self):
        if not self.close:
            return "⚠️ No K-line data available for rendering."

        fig = plotille.Figure()
        fig.width = 35
        fig.height = 20
        fig.color_mode = 'byte'

        fig.show_frame = False
        fig.show_grid = False
        fig.show_axes = False
        fig.xticks = []
        fig.yticks = []
        fig.x_label = ''
        fig.y_label = ''
        fig.title = ''
        fig.legend_location = None
        fig.show_origin = False
        fig.tick_character = ' '

        fig.set_x_limits(min_=0, max_=len(self.close)-1)
        min_y = min(self.close)
        max_y = max(self.close)
        fig.set_y_limits(min_=min_y * 0.998, max_=max_y * 1.002)

        for i in range(1, len(self.close)):
            x_segment = [i-1, i]
            y_segment = [self.close[i-1], self.close[i]]
            color = 46 if self.close[i] >= self.close[i-1] else 196
            fig.plot(x_segment, y_segment, lc=color)

        result = "\n📈 Pure Kline:\n"
        result += fig.show()
        result += f"\nHigh: ${max_y:.4f}  Low: ${min_y:.4f}\n"
        return result