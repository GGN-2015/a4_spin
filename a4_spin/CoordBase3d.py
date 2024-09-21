# 坐标系变换过程
# 原始坐标系坐标 -> 相机坐标系坐标 -> 透视变换坐标 -> 二维平面坐标

# 相机坐标系
# x 向右，y 向上，z 向后（右手系）

MATH_EPS = 1e-8

import numpy as np

class CoordBase3d:
    def get_unit(self, np_arr) -> np.ndarray: # 此函数可以被构造函数调用
        norm = np.linalg.norm(np_arr)
        return np_arr / norm
    
    def __init__(self, x_dir: tuple, y_dir: tuple) -> None:
        self.x_dir = self.get_unit(np.array(x_dir))
        self.y_dir = self.get_unit(np.array(y_dir))
        assert np.dot(self.x_dir, self.y_dir) < MATH_EPS
        self.z_dir = self.get_unit(np.cross(self.x_dir, self.y_dir))

    def get_coord_base_matrix(self) -> np.ndarray:
        return np.column_stack((self.x_dir, self.y_dir, self.z_dir))
    
if __name__ == "__main__":
    coord_base_3d = CoordBase3d( # 获得坐标系矩阵
        (0.0, 1.0, 0.0),
        (1.0, 0.0, 0.0)
    )
    print(coord_base_3d.get_coord_base_matrix())