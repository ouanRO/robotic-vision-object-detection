import cv2
from camera import Camera
from detector import ObjectDetector
from utils import calculate_center, draw_target, compute_robot_velocities

def main():
    detector = ObjectDetector(model_path="yolov8n.pt")
    cam = Camera(source=0)

    print("=== Simulation Pré-ROS 2 : Contrôleur Vitesse ===")
    print("Appuie sur 'q' pour quitter.")

    while True:
        ret, frame = cam.get_frame()
        if not ret:
            print("Erreur de lecture de la caméra.")
            break

        height, width, _ = frame.shape
        img_center_x = width // 2
        img_center_y = height // 2

        # Inférence YOLO
        results = detector.detect(frame, save=False)
        annotated_frame = results[0].plot()

        # Viseur au centre
        cv2.line(annotated_frame, (img_center_x - 15, img_center_y), (img_center_x + 15, img_center_y), (255, 255, 255), 2)
        cv2.line(annotated_frame, (img_center_x, img_center_y - 15), (img_center_x, img_center_y + 15), (255, 255, 255), 2)

        linear_v = 0.0
        angular_w = 0.0
        status = "RECHERCHE CIBLE..."

        result = results[0]
        if len(result.boxes) > 0:
            box = result.boxes[0]
            coords = box.xyxy[0].tolist()
            class_id = int(box.cls[0])
            class_name = result.names[class_id]

            box_width = coords[2] - coords[0]
            cx, cy = calculate_center(coords)
            annotated_frame = draw_target(annotated_frame, cx, cy, label=class_name)

            # Calcul des vitesses vectorielles (v, w)
            linear_v, angular_w, status = compute_robot_velocities(width, height, cx, box_width)

        # Dashboard / Télémétrie
        cv2.rectangle(annotated_frame, (0, 0), (width, 40), (0, 0, 0), -1)
        cv2.putText(annotated_frame, f"CMD_VEL: {status}", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.imshow("Robot Vision - Pre-ROS 2 Simulation", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()