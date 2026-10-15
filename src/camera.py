import cv2

class Camera:
    def __init__(self, source=0):
        """
        Initialise la caméra.
        source=0 désigne la webcam intégrée par défaut.
        """
        print(f"Ouverture de la caméra (source {source})...")
        self.cap = cv2.VideoCapture(source)

        if not self.cap.isOpened():
            print("Erreur : Impossible d'accéder à la caméra.")

    def get_frame(self):
        """
        Lit une image (frame) depuis la webcam.
        Retourne (True, frame) si succès, (False, None) si échec.
        """
        ret, frame = self.cap.read()
        return ret, frame

    def release(self):
        """
        Libère la caméra pour la rendre disponible à d'autres applications.
        """
        self.cap.release()
        print("Caméra fermée.")