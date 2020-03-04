import pornstar
mydlib = pornstar.MyDlib()

picture = pornstar.read_image_as_a_frame("./me.jpg")
head = mydlib.get_face(picture)

#pornstar.save_a_frame_as_an_image("my_head.png", head)
pornstar.display(picture, head)
