
from utilz.vis import *
from collections import namedtuple
#
def Facenet():

    from facenet_pytorch import MTCNN
    import torch
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    mtcnn = MTCNN(keep_all=True, device=device)

    def get_boxes(frame):
        boxes, probs, landmarks = mtcnn.detect(frame, landmarks=True)
        #boxes, _ = mtcnn.detect(frame)
        return boxes, probs, landmarks

    def draw_boxes(frame,boxes,landmarks):
        frame_with_boxes = frame.copy()
        for box, landmark in zip(boxes, landmarks):
            x0,x1,y0,y1 = intr(box[0]),intr(box[2]),intr(box[1]),intr(box[3])
            dx = x1 - x0
            dy = y1 - y0
            if True:
                cv2.line(frame_with_boxes,(x0,y0),(x1,y0),(255,0,0),4)
                cv2.line(frame_with_boxes,(x0,y1),(x1,y1),(255,0,0),4)
                cv2.line(frame_with_boxes,(x0,y0),(x0,y1),(255,0,0),4)
                cv2.line(frame_with_boxes,(x1,y0),(x1,y1),(255,0,0),4)
        return frame_with_boxes

    return namedtuple(
        '_',
        'get_boxes draw_boxes')(
         get_boxes, draw_boxes
    )

if __name__ == '__main__':
    
    path = select_file()[0]
    img = zimread(path)
    F = Facenet()
    a,b,c = F.get_boxes(img)   
    d = F.draw_boxes(img,a,c) 
    CA()
    mi(d)
    spause()
    raw_enter()
#,b

#EOF
