import cv2
import numpy as np
import os
import argparse

def draw_box_3d(image, corners, color=(0, 0, 255)):
    ''' Draw 3d bounding box in image
        corners: (8,2) array of vertices for the 3d box in following order:
            1 -------- 0
           /|         /|
          2 -------- 3 .
          | |        | |
          . 5 -------- 4
          |/         |/
          6 -------- 7
    '''

    face_idx = [[0, 1, 5, 4],
                [1, 2, 6, 5],
                [2, 3, 7, 6],
                [3, 0, 4, 7]]
    for ind_f in range(3, -1, -1):
        f = face_idx[ind_f]
        for j in range(4):
            cv2.line(image, (corners[f[j], 0], corners[f[j], 1]),
                     (corners[f[(j + 1) % 4], 0], corners[f[(j + 1) % 4], 1]), color, 2, lineType=cv2.LINE_AA)
        if ind_f == 0:
            cv2.line(image, (corners[f[0], 0], corners[f[0], 1]),
                     (corners[f[2], 0], corners[f[2], 1]), color, 1, lineType=cv2.LINE_AA)
            cv2.line(image, (corners[f[1], 0], corners[f[1], 1]),
                     (corners[f[3], 0], corners[f[3], 1]), color, 1, lineType=cv2.LINE_AA)

    return image

# Calculates Rotation Matrix given euler angles.
def euler_to_rotation(theta) :

    R_x = np.array([[1,         0,                  0                   ],
                    [0,         np.cos(theta[0]), -np.sin(theta[0]) ],
                    [0,         np.sin(theta[0]),  np.cos(theta[0])  ]
                    ])

    R_y = np.array([[np.cos(theta[1]),    0,      np.sin(theta[1])  ],
                    [0,                   1,      0                   ],
                    [-np.sin(theta[1]),   0,      np.cos(theta[1])  ]
                    ])

    R_z = np.array([[np.cos(theta[2]),    -np.sin(theta[2]),    0],
                    [np.sin(theta[2]),     np.cos(theta[2]),     0],
                    [0,                     0,                      1]
                    ])

    R = np.dot(R_z, np.dot( R_y, R_x ))

    return R
"""
This matrix are specific for the camera configuration in the SDF world

    <horizontal_fov>1.57</horizontal_fov>
    <width>800</width>
    <height>600</height>

If any of them is changed, you have to change the projection matrix
"""
projMatrix = np.array([
    [0.99975, 0, 0, 0],
    [0, 1.333, 0, 0 ],
    [0, 0, -1.00002, -0.02],
    [0, 0, -1, 0]
])


# Arg Parser to set the dataset path
parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, required=True, help='Segmentation Dataset Path')
args = parser.parse_args()

# dataset path
path = args.path

# paths of images folders
imageDir = os.path.join(path, "images")
boxesDir = os.path.join(path, "boxes")

imagesPaths = sorted(os.listdir(imageDir))
boxesPaths = sorted(os.listdir(boxesDir))

imagesPaths = [os.path.join(imageDir, path) for path in imagesPaths]
boxesPaths = [os.path.join(boxesDir, path) for path in boxesPaths]

for imagePath, boxesPath in zip(imagesPaths, boxesPaths):
    boxesFile = open(boxesPath)
    boxesLines = boxesFile.readlines()

    image = cv2.imread(imagePath)
    width, height = image.shape[1], image.shape[0]

    del boxesLines[0]
    for box in boxesLines:
        box = box.split(',')
        label = float(box[0])
        x     = float(box[1])
        y     = float(box[2])
        z     = float(box[3])
        w     = float(box[4])
        h     = float(box[5])
        l     = float(box[6])
        roll  = float(box[7])
        pitch = float(box[8])
        yaw   = float(box[9])

        # get the rotation matrix
        R = euler_to_rotation([roll, pitch, yaw])

        # get the 8 vertices of the box (the corners) in model coordinates
        x_corners = [w / 2, -w / 2, -w / 2, w / 2, w / 2, -w / 2, -w / 2, w / 2]
        y_corners = [h/2, h/2, h/2, h/2, -h/2, -h/2, -h/2, -h/2]
        z_corners = [l / 2, l / 2, -l / 2, -l / 2, l / 2, l / 2, -l / 2, -l / 2]
        # concatinate them
        corners = np.array([x_corners, y_corners, z_corners], dtype=np.float32)

        # transform the corners to the 3D camera coordinates by applying the rotation then addin the position
        corners_3d = np.dot(R, corners)
        corners_3d = corners_3d + np.array([x,y,z], dtype=np.float32).reshape(3, 1)
        corners_3d = corners_3d.transpose(1, 0)

        # convert the 3d points to 4d homogenous points to apply the projection matrix
        pts_3d_homo = np.concatenate([corners_3d, np.ones((corners_3d.shape[0], 1), dtype=np.float32)], axis=1)

        # projection
        pts_2d = np.dot(projMatrix, pts_3d_homo.transpose(1, 0)).transpose(1, 0)
        # devide by w component of the homogenous coord.
        pts_2d = pts_2d[:, :2] / pts_2d[:, 2:]
        pts_2d = pts_2d.astype(np.float32)

        # convert from [-1,1] to [0,1] range
        pts_2d = pts_2d.clip(-1,1)
        xx = (pts_2d[:,0] + 1) / 2
        yy = (1 - pts_2d[:,1]) / 2
        xx = xx.clip(0,1)
        yy = yy.clip(0,1)
        # convert to screen coord
        pts_2d = np.array([xx,yy], dtype=np.float32).T
        pts_2d *= (width, height)
        pts_2d = pts_2d.astype(np.int32)

        image = draw_box_3d(image, pts_2d)


    print("")
    cv2.imshow("image", image)
    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()
        break