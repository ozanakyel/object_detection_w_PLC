import cv2
import time
import socket

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

#=============Object detection Copy===================

CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4
COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

class_names = []
with open(r"models\names\classes.txt", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]
    print('class_names=', class_names)
vc = cv2.VideoCapture('deneme.avi')

net = cv2.dnn.readNet("models\weight\yolov4-custom_best.weights", "models\cfg\yolov4-custom.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(608, 608), scale=1/255, swapRB=True)
#======================Object detection========================
def parse_data(data):
    data = data.split('#')
    print("data_split=",data)
    parsed_data={'terminal': data[0],
                 'bodyNo': data[1],
                 'assyNo': data[2],
                 'VehcStatus': data[3],
                 'Spek': data[4]}
    for k,v in parsed_data.items():
        print("key: " +k + " value: "+v)

    if parsed_data['VehcStatus']=="start":
        print("..........starta girdii........")
        cv2.destroyAllWindows()
        (grabbed, frame) = (None, None)
        (grabbed, frame) = vc.read()
        if not grabbed:
            print("görüntü okuyamadı")
            exit()
        print("görüntü okudu")
        start = time.time()
        classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        end = time.time()

        print("calasssessss:::", classes)
        print("boxes", boxes)

        start_drawing = time.time()
        for (classid, score, box) in zip(classes, scores, boxes):
            color = COLORS[int(classid) % len(COLORS)]
            label = "%s : %f" % (class_names[classid[0]], score)
            cv2.rectangle(frame, box, color, 2)
            cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        end_drawing = time.time()

        fps_label = "FPS: %.2f (excluding drawing time of %.2fms)" % (
        1 / (end - start), (end_drawing - start_drawing) * 1000)
        cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        frame = cv2.resize(frame, (800, 600))
        cv2.imshow("detections", frame)
        cv2.waitKey(1)
        if 39 in classes or str(39) in classes:
            conn.sendall(b'sisevarOK')
            print("şişeyi buldun hadi bakam aslan")
        else:
            conn.sendall(b'siseyokNG')
            print("şişe yok oturduğunuz yeri lütfen kontrol ediniz")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("host=",HOST)
    print("port=", PORT)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            print("data=",data)
            string_data= data.decode('utf-8')
            parse_data(string_data)

            #print("string data=",string_data)
            if not data:
                break
            #conn.sendall(data)