import dlib
import os
import numpy as np
import bz2
import shutil
import urllib.request
from PIL import Image
import cv2
import math

from . import  utils

DLIB_USE_CNN = False
try:
    import dlib.cuda as cuda

    if cuda.get_num_devices() >= 1:
        if dlib.DLIB_USE_CUDA:
            DLIB_USE_CNN = True
except Exception as e:
    print(e)

class MyDlib:
    def __init__(self):
        print("Dlib is loading")

        if DLIB_USE_CNN:
            dlib_cnn_face_detector_path = os.path.join(
                utils.ROOT_DIR, "mmod_human_face_detector.dat")
            if not os.path.exists(dlib_cnn_face_detector_path):
                self.download_cnn_face_detector(dlib_cnn_face_detector_path)
            self.face_detector = dlib.cnn_face_detection_model_v1(dlib_cnn_face_detector_path)
        else:
            self.face_detector = dlib.get_frontal_face_detector()

        dlib_shape_predictor_path = os.path.join(
            utils.ROOT_DIR, "shape_predictor_68_face_landmarks.dat")
        if not os.path.exists(dlib_shape_predictor_path):
            self.download_dlib_shape_predictor(dlib_shape_predictor_path)
        self.face_predictor = dlib.shape_predictor(
            dlib_shape_predictor_path)
        print("Dlib loading completed")

        self.last_frame = np.array([])

    def download_cnn_face_detector(self, save_to):
        """Download dlib cnn face detector from network.
        """
        try:
            bz2_file = save_to + ".bz2"
            if not os.path.exists(bz2_file):
                with urllib.request.urlopen(
                        "https://github.com/davisking/dlib-models/raw/master/mmod_human_face_detector.dat.bz2") as resp, open(
                    bz2_file, 'wb') as out:
                    shutil.copyfileobj(resp, out)
            with open(bz2_file, "rb") as stream:
                compressed_data = stream.read()
            obj = bz2.BZ2Decompressor()
            data = obj.decompress(compressed_data)
            with open(save_to, "wb") as stream:
                stream.write(data)
        except Exception as e:
            print(e)
            print("\n" * 5)
            print("You may have to use VPN to use this module!")
            print("\n" * 5)

    def download_dlib_shape_predictor(self, save_to):
        """Download dlib shape predictor from Releases.
        """
        try:
            bz2_file = save_to + ".bz2"
            if not os.path.exists(bz2_file):
                with urllib.request.urlopen(
                        "https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2") as resp, open(
                    bz2_file, 'wb') as out:
                    shutil.copyfileobj(resp, out)
            with open(bz2_file, "rb") as stream:
                compressed_data = stream.read()
            obj = bz2.BZ2Decompressor()
            data = obj.decompress(compressed_data)
            with open(save_to, "wb") as stream:
                stream.write(data)
        except Exception as e:
            print(e)
            print("\n" * 5)
            print("You may have to use VPN to use this module!")
            print("\n" * 5)

    def call_face_detector(self, image, upsample_num_times=0):
        detections = self.face_detector(image, upsample_num_times)
        if DLIB_USE_CNN:
            rects = dlib.rectangles()
            rects.extend([d.rect for d in detections])
            return rects
        else:
            return detections

    def _adjust_gamma(self, image, gamma=1.0):
        # build a lookup table mapping the pixel values [0, 255] to
        # their adjusted gamma values
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")

        # apply gamma correction using the lookup table
        return cv2.LUT(image, table)

    def add_image_to_the_top_of_another(self, background_img, top_img, x, y, overlay_size=None):
        if overlay_size is not None:
            top_img = cv2.resize(
                top_img.copy(), overlay_size)

        if (background_img.shape[2] == 4):  # png with transparency
            backgound_Image = Image.fromarray(background_img, mode="RGBA")
        else:
            backgound_Image = Image.fromarray(background_img, mode="RGB")

        if (top_img.shape[2] == 4):  # png with transparency
            object_Image = Image.fromarray(top_img, mode="RGBA")
        else:
            object_Image = Image.fromarray(top_img, mode="RGB")

        if (top_img.shape[2] == 4):  # png with transparency
            backgound_Image.paste(object_Image, box=(x, y), mask=object_Image)
        else:
            backgound_Image.paste(object_Image, box=(x, y))

        return np.array(backgound_Image).astype(np.uint8)

    def add_a_mask_to_face(self, frame, mask_image):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.call_face_detector(gray_frame)
        if len(faces) > 0:  # face found
            for face in faces:
                x = face.left()
                y = face.top()
                w = face.right() - x
                h = face.bottom() - y

                y = y - int(h * 0.05)
                h = int(h * 1.05)

                frame = self.add_image_to_the_top_of_another(
                    frame, mask_image, x, y, (w, h))
            return frame
        else:  # no face at all
            raise Exception("No face found!")

    def get_face(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.call_face_detector(gray_frame)
        assert len(faces) > 0, "We need al least one face!"

        face = faces[0]
        x = face.left()
        y = face.top()
        w = face.right()
        h = face.bottom()

        image = Image.fromarray(frame, mode="RGB")
        your_face = image.crop((x, y, w, h))

        return np.array(your_face).astype(np.uint8)

    def face_swap(self, original_face, new_face):
        def extract_index_nparray(nparray):
            index = None
            for num in nparray[0]:
                index = num
                break
            return index

        # decrease the size to speed up the processing
        new_face_gray = cv2.cvtColor(new_face, cv2.COLOR_BGR2GRAY)
        original_face_gray = cv2.cvtColor(original_face, cv2.COLOR_BGR2GRAY)

        mask = np.zeros_like(new_face_gray)
        original_face_new_face = np.zeros_like(original_face)  # create an empty image with the size of original image

        # face detection for the second image
        faces = self.call_face_detector(new_face_gray)
        if len(faces) != 1:
            raise Exception("The second image should have a face! And only one face!")
        landmarks = self.face_predictor(new_face_gray, faces[0])
        landmarks_points = []
        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            landmarks_points.append((x, y))
            # cv2.circle(new_face, (x, y), 3, (0, 0, 255), -1) # we don't need to draw points at the face

        points = np.array(landmarks_points, np.int32)
        convexhull = cv2.convexHull(points)  # caculate the face area according to a bunch of points
        # cv2.polylines(new_face, [convexhull], True, (255, 0, 0), 3) # draw a border line for face
        cv2.fillConvexPoly(mask, convexhull, 255)  # get the mask of the second image face
        face_image_1 = cv2.bitwise_and(new_face, new_face, mask=mask)  # get the second image face

        # Delaunay triangulation
        rect = cv2.boundingRect(convexhull)
        subdiv = cv2.Subdiv2D(rect)
        subdiv.insert(landmarks_points)
        triangles = subdiv.getTriangleList()  # get a bunch of triangles
        triangles = np.array(triangles, dtype=np.int32)  # convert it to int

        indexes_triangles = []
        for t in triangles:
            pt1 = (t[0], t[1])
            pt2 = (t[2], t[3])
            pt3 = (t[4], t[5])

            index_pt1 = np.where((points == pt1).all(axis=1))
            index_pt1 = extract_index_nparray(index_pt1)

            index_pt2 = np.where((points == pt2).all(axis=1))
            index_pt2 = extract_index_nparray(index_pt2)

            index_pt3 = np.where((points == pt3).all(axis=1))
            index_pt3 = extract_index_nparray(index_pt3)

            if index_pt1 is not None and index_pt2 is not None and index_pt3 is not None:
                triangle = [index_pt1, index_pt2, index_pt3]
                indexes_triangles.append(triangle)

        # face detection for the first image
        faces2 = self.call_face_detector(original_face_gray)
        if len(faces2) == 0:
            # raise Exception("The first image should have at least one face!")
            if (self.last_frame.size != 0):
                frame = self.last_frame
            else:
                white = np.zeros(
                    (new_face.shape[0], new_face.shape[1], 3), dtype=np.uint8)
                white.fill(255)
                frame = white
            return frame
        # if len(faces2) != 1:
        #    #raise Exception("The first image should have at least one face!")
        #    raise Exception("The first image should have a face! And only one face!")
        convexhull2_list = []
        for face in faces2:
            landmarks = self.face_predictor(original_face_gray, face)
            landmarks_points2 = []
            for n in range(0, 68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                landmarks_points2.append((x, y))
                # cv2.circle(original_face, (x,y), 3, (0,255,0), -1) # we don't need to draw points at the face

            points2 = np.array(landmarks_points2, np.int32)
            convexhull2 = cv2.convexHull(points2)  # get the area of first face by a bunch of points
            convexhull2_list.append(convexhull2)

            # Triangulation of both faces
            for triangle_index in indexes_triangles:
                # Triangulation of the second face
                tr1_pt1 = landmarks_points[triangle_index[0]]
                tr1_pt2 = landmarks_points[triangle_index[1]]
                tr1_pt3 = landmarks_points[triangle_index[2]]
                triangle1 = np.array([tr1_pt1, tr1_pt2, tr1_pt3], np.int32)

                rect1 = cv2.boundingRect(triangle1)
                (x, y, w, h) = rect1
                cropped_triangle = new_face[y: y + h, x: x + w]
                cropped_tr1_mask = np.zeros((h, w), np.uint8)

                points = np.array([[tr1_pt1[0] - x, tr1_pt1[1] - y],
                                   [tr1_pt2[0] - x, tr1_pt2[1] - y],
                                   [tr1_pt3[0] - x, tr1_pt3[1] - y]], np.int32)

                cv2.fillConvexPoly(cropped_tr1_mask, points, 255)
                cropped_triangle = cv2.bitwise_and(cropped_triangle, cropped_triangle,
                                                   mask=cropped_tr1_mask)

                # cv2.line(new_face, tr1_pt1, tr1_pt2, (0, 0, 255), 2)
                # cv2.line(new_face, tr1_pt3, tr1_pt2, (0, 0, 255), 2)
                # cv2.line(new_face, tr1_pt1, tr1_pt3, (0, 0, 255), 2)

                # Triangulation of first face
                tr2_pt1 = landmarks_points2[triangle_index[0]]
                tr2_pt2 = landmarks_points2[triangle_index[1]]
                tr2_pt3 = landmarks_points2[triangle_index[2]]
                triangle2 = np.array([tr2_pt1, tr2_pt2, tr2_pt3], np.int32)

                rect2 = cv2.boundingRect(triangle2)
                (x, y, w, h) = rect2
                cropped_triangle2 = original_face[y: y + h, x: x + w]
                cropped_tr2_mask = np.zeros((h, w), np.uint8)

                points2 = np.array([[tr2_pt1[0] - x, tr2_pt1[1] - y],
                                    [tr2_pt2[0] - x, tr2_pt2[1] - y],
                                    [tr2_pt3[0] - x, tr2_pt3[1] - y]], np.int32)

                # cv2.fillConvexPoly(cropped_tr2_mask, points2, 255)
                # cropped_triangle2 = cv2.bitwise_and(cropped_triangle2, cropped_triangle2,
                #                                    mask=cropped_tr2_mask)

                # cv2.line(original_face, tr2_pt1, tr2_pt2, (0, 0, 255), 2)
                # cv2.line(original_face, tr2_pt3, tr2_pt2, (0, 0, 255), 2)
                # cv2.line(original_face, tr2_pt1, tr2_pt3, (0, 0, 255), 2)

                # Warp triangles
                # We convert the first image triangle to second inage triangle. warpAffine() is the key function for doing that
                points = np.float32(points)
                points2 = np.float32(points2)
                M = cv2.getAffineTransform(points, points2)
                warped_triangle = cv2.warpAffine(cropped_triangle, M, (w, h), flags=cv2.INTER_NEAREST,
                                                 borderValue=(0, 0, 0))

                # Reconstructing destination face
                target_index = np.any(warped_triangle != [0, 0, 0], axis=-1)
                original_face_new_face[y: y + h, x: x + w][target_index] = warped_triangle[target_index]

                # cv2.imshow("piece", warped_triangle) # keep press esc to see the generating process dynamiclly
                # cv2.imshow("how we generate the new face", original_face_new_face)
                # cv2.waitKey(0)

        # Face swapped (putting 1st face into 2nd face)
        seamlessclone = original_face
        for convexhull2_element in convexhull2_list:
            original_face_face_mask = np.zeros_like(original_face_gray)
            original_face_head_mask = cv2.fillConvexPoly(original_face_face_mask, convexhull2_element, 255)
            original_face_face_mask = cv2.bitwise_not(original_face_head_mask)

            original_face_head_noface = cv2.bitwise_and(seamlessclone, seamlessclone, mask=original_face_face_mask)
            result = cv2.add(original_face_head_noface, original_face_new_face)

            # (x, y, w, h) = cv2.boundingRect(convexhull2)
            # center_face2 = (int((x + x + w) / 2), int((y + y + h) / 2))
            # seamlessclone = cv2.seamlessClone(result, original_face, original_face_head_mask, center_face2, cv2.NORMAL_CLONE)

            (x, y, w, h) = cv2.boundingRect(original_face_head_mask)
            real_new_face = original_face_new_face[y: y + h, x: x + w]
            center_face2 = (int((x + x + w) / 2), int((y + y + h) / 2))
            real_new_face_mask = original_face_head_mask[y: y + h, x: x + w]
            seamlessclone = cv2.seamlessClone(real_new_face, seamlessclone, real_new_face_mask, center_face2,
                                              cv2.NORMAL_CLONE)  # (new_face, the_target_image, mask_of_new_face_at_target_image, the_center_point_of_new_face_at_the_target_image, cv2.MIXED_CLONE)

        # cv2.imshow("first_img", original_face)
        # cv2.imshow("second_img", new_face)
        # cv2.imshow("raw_combine", result)
        # cv2.imshow("with seamlessclone", seamlessclone)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        return seamlessclone

    def face_slimming(self, image):
        def landmark_dec_dlib_fun(img_src):
            img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)

            land_marks = []

            rects = self.call_face_detector(img_gray, 0)

            for i in range(len(rects)):
                land_marks_node = np.matrix(
                    [[p.x, p.y] for p in self.face_predictor(img_gray, rects[i]).parts()])
                land_marks.append(land_marks_node)

            return land_marks

        def localTranslationWarp(srcImg, startX, startY, endX, endY, radius):
            '''
            方法： Interactive Image Warping 局部平移算法
            '''

            ddradius = float(radius * radius)
            copyImg = np.zeros(srcImg.shape, np.uint8)
            copyImg = srcImg.copy()

            # 计算公式中的|m-c|^2
            ddmc = (endX - startX) * (endX - startX) + \
                   (endY - startY) * (endY - startY)
            H, W, C = srcImg.shape
            for i in range(W):
                for j in range(H):
                    # 计算该点是否在形变圆的范围之内
                    # 优化，第一步，直接判断是会在（startX,startY)的矩阵框中
                    if math.fabs(i - startX) > radius and math.fabs(j - startY) > radius:
                        continue

                    distance = (i - startX) * (i - startX) + \
                               (j - startY) * (j - startY)

                    if (distance < ddradius):
                        # 计算出（i,j）坐标的原坐标
                        # 计算公式中右边平方号里的部分
                        ratio = (ddradius - distance) / (ddradius - distance + ddmc)
                        ratio = ratio * ratio

                        # 映射原位置
                        UX = i - ratio * (endX - startX)
                        UY = j - ratio * (endY - startY)

                        # 根据双线性插值法得到UX，UY的值
                        value = BilinearInsert(srcImg, UX, UY)
                        # 改变当前 i ，j的值
                        copyImg[j, i] = value

            return copyImg

        def BilinearInsert(src, ux, uy):
            # 双线性插值法
            w, h, c = src.shape
            if c == 3:
                x1 = int(ux)
                x2 = x1 + 1
                y1 = int(uy)
                y2 = y1 + 1

                part1 = src[y1, x1].astype(np.float) * (float(x2) - ux) * (float(y2) - uy)
                part2 = src[y1, x2].astype(np.float) * (ux - float(x1)) * (float(y2) - uy)
                part3 = src[y2, x1].astype(np.float) * (float(x2) - ux) * (uy - float(y1))
                part4 = src[y2, x2].astype(np.float) * \
                        (ux - float(x1)) * (uy - float(y1))

                insertValue = part1 + part2 + part3 + part4

                return insertValue.astype(np.int8)

        src = image

        landmarks = landmark_dec_dlib_fun(src)

        # 如果未检测到人脸关键点，就不进行瘦脸
        if len(landmarks) == 0:
            # raise Exception("No face was been detected!")
            if (self.last_frame.size != 0):
                frame = self.last_frame
            else:
                white = np.zeros(
                    (image.shape[0], image.shape[1], 3), dtype=np.uint8)
                white.fill(255)
                frame = white
            return frame

        for landmarks_node in landmarks:
            left_landmark = landmarks_node[3]
            left_landmark_down = landmarks_node[5]

            right_landmark = landmarks_node[13]
            right_landmark_down = landmarks_node[15]

            endPt = landmarks_node[30]

            # 计算第4个点到第6个点的距离作为瘦脸距离
            r_left = math.sqrt(
                (left_landmark[0, 0] - left_landmark_down[0, 0]) * (left_landmark[0, 0] - left_landmark_down[0, 0]) +
                (left_landmark[0, 1] - left_landmark_down[0, 1]) * (left_landmark[0, 1] - left_landmark_down[0, 1]))

            # 计算第14个点到第16个点的距离作为瘦脸距离
            r_right = math.sqrt((right_landmark[0, 0] - right_landmark_down[0, 0]) * (
                    right_landmark[0, 0] - right_landmark_down[0, 0]) +
                                (right_landmark[0, 1] - right_landmark_down[0, 1]) * (
                                        right_landmark[0, 1] - right_landmark_down[0, 1]))

            # 瘦左边脸
            thin_image = localTranslationWarp(
                src, left_landmark[0, 0], left_landmark[0, 1], endPt[0, 0], endPt[0, 1], r_left)
            # 瘦右边脸
            thin_image = localTranslationWarp(
                thin_image, right_landmark[0, 0], right_landmark[0, 1], endPt[0, 0], endPt[0, 1], r_right)

        # 显示
        # cv2.imshow('original', src)
        # cv2.imshow('thin', thin_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return thin_image
