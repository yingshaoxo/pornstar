import pornstar
mydlib = pornstar.my_dlib

picture = pornstar.utils.read_image_as_a_frame("./me.jpg")
head = mydlib.get_face(picture)

#pornstar.save_a_frame_as_an_image("my_head.png", head)
pornstar.utils.display(picture, head)