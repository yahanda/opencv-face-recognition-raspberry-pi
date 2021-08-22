# opencv-face-recognition-raspberry-pi
Real-time face recognition project with OpenCV and Python

# Installation
## Create recognizer model
1. Clone this repository
    ```
    git clone https://github.com/yahanda/opencv-face-recognition-raspberry-pi.git
    cd opencv-face-recognition-raspberry-pi
    ```
1. Run `01_face_dataset.py` to create dataset
    ```
    python 01_face_dataset.py
    ```
1. Run `02_face_training.py` to train and save the model into `app/trainer/trainer.yml`
    ```
    python 02_face_training.py
    ```
1. Edit `app/trainer/label.txt` manually to set the names related to ids. For example, if Ichiro: id=1, Jiro: id=2, set as follows:
    ```
    None
    Ichiro
    Jiro
    ```

1. Run `03_face_recognition.py` to predict faces
    ```
    python 03_face_recognition.py
    ```

## Build and push Docker image
- Run the following command
    ```
    cd <cloned-folder>
    docker build -t opencv-facerecognition .
    docker tag opencv-facerecognition <your-container-registry>/opencv-facerecognition:<tag>
    docker push <your-container-registry>/opencv-facerecognition:<tag>
    ```

## Deploy the IoT Edge module
- Deploy the container image to IoT Edge device
    - If you want to map exposed ports on the container to a port on the host device, use the **HostConfig.PortBindings** parameter in IoT Edge deployment manifest:
        ```
        {
            "HostConfig": {
                "PortBindings": {
                    "80/tcp": [
                        {
                        "HostPort": "[Host port]"
                        }
                    ]
                }
            }
        }
        ```
    - For example, if you exposed port 80 inside the module and want to map that to port 8080 of the host device, the create options would look like the following:
        ```
        {
            "HostConfig": {
                "PortBindings": {
                    "80/tcp": [
                        {
                        "HostPort": "8080"
                        }
                    ]
                }
            }
        }
        ```
- Test an inference model
    - After you've deployed the module, you can test the inference endpoint using curl command as follows:
        ```
        curl -X POST http://<iot-edge-host>:<port>/image -F imageData=@<image-file>
        ```
    - An example is:
        ```
        curl -X POST http://localhost:8080/image -F imageData=@test01.jpg
        {"created":"2021-08-22T14:03:26.143822","predictions":[{"boundingBox":{"height":"407","left":"2805","top":"1165","width":"407"},"confidence":"39","id":"Yasu"}]}
        ```