import cv2

def calculate_center(box):
    """Calculer le centre (cx, cy) d'une boîte de détection [x_min, y_min, x_max, y_max]."""
    x_min, y_min, x_max, y_max = box
    center_x = int((x_min + x_max) / 2)
    center_y = int((y_min + y_max) / 2)
    return center_x, center_y

def compute_robot_velocities(frame_width, frame_height, target_x, box_width):
    """
    Calcule les vitesses du robot sous forme de régulateur (Similaire à /cmd_vel sous ROS 2).
    
    Returns:
        linear_x (float): Vitesse linéaire (Avancer/Reculer en m/s)
        angular_z (float): Vitesse angulaire (Rotation gauche/droite en rad/s)
        status_text (str): Description textuelle de la commande
    """
    img_center_x = frame_width // 2
    
    # 1. Calcul de l'erreur d'alignement horizontal (en pixels)
    error_x = img_center_x - target_x
    
    # Gain proportionnel pour la rotation (Kp)
    # Si la cible est à gauche (target_x < center), error_x > 0 -> rotation positive (gauche)
    kp_angular = 0.003
    angular_z = error_x * kp_angular
    
    # Limiter la vitesse angulaire pour éviter les mouvements brusques
    angular_z = max(min(angular_z, 1.0), -1.0)
    
    # 2. Vitesse linéaire basée sur la taille (distance estimée)
    # Taille idéale de la boîte dans l'image : 200 pixels
    target_width = 200
    error_distance = target_width - box_width
    kp_linear = 0.002
    linear_x = error_distance * kp_linear
    linear_x = max(min(linear_x, 0.5), -0.5)
    
    # Texte de statut pour le debug
    if abs(error_x) < 30:
        rot_status = "ALIGNE"
    elif error_x > 0:
        rot_status = "TOURNER GAUCHE"
    else:
        rot_status = "TOURNER DROITE"

    return linear_x, angular_z, f"{rot_status} | Linear v={linear_x:.2f} m/s, Angular w={angular_z:.2f} rad/s"

def draw_target(frame, center_x, center_y, label=""):
    """Dessine le point central et les repères sur l'image."""
    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
    text = f"{label} ({center_x}, {center_y})"
    cv2.putText(frame, text, (center_x - 40, center_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame