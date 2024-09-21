# 用于描述一个三维空间下的线框对象
# 本质上就是若干个结点，以及结点之间的连线

import numpy as np
from PIL import Image, ImageDraw, ImageFont

COLOR_OF_TEXT = (255, 0, 0)
COLOR_OF_LINE = (  0, 0, 0)

# node_coord_list: list of tuple
#       link_list: list of index integer pair
class LineFrameObject3D:
    def __init__(self, node_coord_list: list, link_list: list) -> None:
        self.node_coord_list = node_coord_list
        self.link_list       = link_list
        for index_x, index_y in self.link_list:
            assert 0 <= index_x < len(self.node_coord_list) # 做一些力所能及的一致性检查
            assert 0 <= index_y < len(self.node_coord_list)

    def get_xy_coord_projection(self): # 使用斜二侧画法进行测试绘图
        sln = (2 ** 0.5) / 4
        x_dir = np.array([1.0, 0.0])
        z_dir = np.array([0.0, 1.0])
        y_dir = np.array([sln, sln])
        node_coord_list_new = []
        for node_coord_3d in self.node_coord_list:
            coord_2d = (
                x_dir * node_coord_3d[0] +
                y_dir * node_coord_3d[1] +
                z_dir * node_coord_3d[2]) # 计算斜二侧画法下的坐标序列
            node_coord_list_new.append(tuple(coord_2d))
        return node_coord_list_new # 返回新的坐标序列
    
    def dump_data_into_image(self, img_height=600, line_width=2) -> Image:
        node_coord_2d_list = self.get_xy_coord_projection() # 先获取二维表示
        xmin = min([x for x, _ in node_coord_2d_list]) # 计算 xy 的取值范围
        xmax = max([x for x, _ in node_coord_2d_list])
        ymin = min([y for _, y in node_coord_2d_list])
        ymax = max([y for _, y in node_coord_2d_list])
        assert xmin < xmax and ymin < ymax
        delta_x   = xmax - xmin # 按照比例绘制图像
        delta_y   = ymax - ymin
        img_width = round(img_height / delta_y * delta_x) # 计算图片的宽度
        o_pos_x = (0.1 * img_width)
        o_pos_y = (0.1 * img_height)
        unit_xy = (0.8 * img_width) / (xmax - xmin)
        def get_canvas_pos(node_index): # 获得一个指定点在画布上的位置
            x_raw, y_raw = node_coord_2d_list[node_index]
            xpos = (x_raw - xmin) * unit_xy + o_pos_x
            ypos = (y_raw - ymin) * unit_xy + o_pos_y
            return round(xpos), img_height - round(ypos)
        image_now = Image.new("RGB", (img_width, img_height), "white") # 创建图片
        draw      = ImageDraw.Draw(image_now)
        for index_a, index_b in self.link_list: # 将线段绘制到图片上去
            pos_a = get_canvas_pos(index_a)
            pos_b = get_canvas_pos(index_b)
            draw.line([pos_a, pos_b], fill=COLOR_OF_LINE, width=line_width)
        # 将坐标信息绘制到屏幕上
        font = ImageFont.load_default()
        for index_now in range(len(self.node_coord_list)):
            coord_info = "(%g,%g,%g)" % tuple(self.node_coord_list[index_now])
            draw.text(get_canvas_pos(index_now), coord_info, fill=COLOR_OF_TEXT, font=font)
        return image_now
    
if __name__ == "__main__": # 测试代码
    lf_obj_3d = LineFrameObject3D(
        [
            (0.0, 0.0, 0.0), # 八个顶点
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (1.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
            (1.0, 0.0, 1.0),
            (0.0, 1.0, 1.0),
            (1.0, 1.0, 1.0),
        ],
        [
            (0, 1), # 十二条棱
            (0, 2),
            (0, 4),
            (1, 3),
            (1, 5),
            (2, 3),
            (2, 6),
            (3, 7),
            (4, 5),
            (4, 6),
            (5, 7),
            (6, 7)
        ]
    )
    lf_obj_3d.dump_data_into_image().save("test.png")