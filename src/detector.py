from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path="yolov8n.pt"):
        """
        Le constructeur (__init__) s'exécute automatiquement à la création de l'objet.
        Il permet de charger le modèle YOLO en mémoire une seule fois.
        """
        print(f"Chargement du modèle : {model_path}...")
        self.model = YOLO(model_path)

    def detect(self, image_path, save=True):
        """
        Cette méthode prend le chemin d'une image en entrée, 
        exécute la détection et retourne les résultats.
        """
        results = self.model(image_path, save=save ,conf=0.5 )
        return results