"""
Loom Clone - Enregistreur d'écran avec webcam
Ce programme permet d'enregistrer votre écran et votre webcam simultanément
"""

import cv2
import numpy as np
import mss
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import threading
import time
from datetime import datetime
import os


class LoomClone:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Loom Clone - Enregistreur d'écran + Webcam")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        # Variables d'état
        self.is_recording = False
        self.paused = False
        self.cap = None
        self.out = None
        self.screen_capture = mss.mss()

        # Configuration
        self.webcam_size = (200, 150)  # Taille de la webcam dans la vidéo finale
        self.webcam_position = "bottom-right"  # Position de la webcam
        self.output_folder = "recordings"

        # Créer le dossier de sortie s'il n'existe pas
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        self.setup_ui()

    def setup_ui(self):
        """Créer l'interface utilisateur"""

        # Titre
        title_label = tk.Label(
            self.root,
            text="🎥 Loom Clone",
            font=("Arial", 20, "bold"),
            fg="#4A5FFF"
        )
        title_label.pack(pady=20)

        # Frame pour la prévisualisation
        preview_frame = tk.LabelFrame(
            self.root,
            text="Prévisualisation Webcam",
            font=("Arial", 12, "bold")
        )
        preview_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.preview_label = tk.Label(preview_frame)
        self.preview_label.pack(pady=10)

        # Frame pour les paramètres
        settings_frame = tk.LabelFrame(
            self.root,
            text="Paramètres",
            font=("Arial", 11, "bold")
        )
        settings_frame.pack(pady=10, padx=20, fill="x")

        # Position de la webcam
        position_label = tk.Label(settings_frame, text="Position de la webcam:")
        position_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.position_var = tk.StringVar(value="bottom-right")
        positions = ["top-left", "top-right", "bottom-left", "bottom-right"]
        position_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.position_var,
            values=positions,
            state="readonly",
            width=15
        )
        position_combo.grid(row=0, column=1, padx=10, pady=5)
        position_combo.bind('<<ComboboxSelected>>', self.update_position)

        # Frame pour les boutons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        # Bouton Démarrer
        self.start_button = tk.Button(
            button_frame,
            text="⚫ Démarrer l'enregistrement",
            command=self.start_recording,
            bg="#4A5FFF",
            fg="white",
            font=("Arial", 11, "bold"),
            width=25,
            height=2,
            relief="raised",
            cursor="hand2"
        )
        self.start_button.pack(pady=5)

        # Bouton Arrêter
        self.stop_button = tk.Button(
            button_frame,
            text="⬛ Arrêter l'enregistrement",
            command=self.stop_recording,
            bg="#FF4A4A",
            fg="white",
            font=("Arial", 11, "bold"),
            width=25,
            height=2,
            state="disabled",
            relief="raised",
            cursor="hand2"
        )
        self.stop_button.pack(pady=5)

        # Label de statut
        self.status_label = tk.Label(
            self.root,
            text="Prêt à enregistrer",
            font=("Arial", 10),
            fg="green"
        )
        self.status_label.pack(pady=5)

        # Démarrer la prévisualisation de la webcam
        self.start_preview()

    def start_preview(self):
        """Démarrer la prévisualisation de la webcam"""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Erreur", "Impossible d'ouvrir la webcam!")
            return

        self.update_preview()

    def update_preview(self):
        """Mettre à jour la prévisualisation de la webcam"""
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Redimensionner pour la prévisualisation
                frame = cv2.resize(frame, (300, 225))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Convertir en ImageTk
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)

                self.preview_label.imgtk = imgtk
                self.preview_label.configure(image=imgtk)

        # Mettre à jour toutes les 30ms
        if not self.is_recording or True:  # Toujours mettre à jour la prévisualisation
            self.root.after(30, self.update_preview)

    def update_position(self, event=None):
        """Mettre à jour la position de la webcam"""
        self.webcam_position = self.position_var.get()

    def start_recording(self):
        """Démarrer l'enregistrement"""
        if self.is_recording:
            return

        self.is_recording = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_label.config(text="🔴 Enregistrement en cours...", fg="red")

        # Démarrer l'enregistrement dans un thread séparé
        record_thread = threading.Thread(target=self.record, daemon=True)
        record_thread.start()

    def stop_recording(self):
        """Arrêter l'enregistrement"""
        if not self.is_recording:
            return

        self.is_recording = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Enregistrement terminé!", fg="green")

    def get_webcam_position(self, screen_width, screen_height):
        """Calculer la position de la webcam sur l'écran"""
        cam_w, cam_h = self.webcam_size
        margin = 20

        if self.webcam_position == "top-left":
            return (margin, margin)
        elif self.webcam_position == "top-right":
            return (screen_width - cam_w - margin, margin)
        elif self.webcam_position == "bottom-left":
            return (margin, screen_height - cam_h - margin)
        else:  # bottom-right
            return (screen_width - cam_w - margin, screen_height - cam_h - margin)

    def record(self):
        """Fonction principale d'enregistrement"""
        try:
            # Obtenir les dimensions de l'écran
            monitor = self.screen_capture.monitors[1]  # Monitor principal
            screen_width = monitor["width"]
            screen_height = monitor["height"]

            # Générer un nom de fichier unique
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.output_folder, f"loom_recording_{timestamp}.avi")

            # Configurer l'encodeur vidéo
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            fps = 20.0
            self.out = cv2.VideoWriter(
                output_file,
                fourcc,
                fps,
                (screen_width, screen_height)
            )

            if not self.out.isOpened():
                messagebox.showerror("Erreur", "Impossible de créer le fichier vidéo!")
                self.is_recording = False
                return

            while self.is_recording:
                # Capturer l'écran
                screen_img = self.screen_capture.grab(monitor)
                screen_frame = np.array(screen_img)
                screen_frame = cv2.cvtColor(screen_frame, cv2.COLOR_BGRA2BGR)

                # Capturer la webcam
                ret, webcam_frame = self.cap.read()

                if ret:
                    # Redimensionner la webcam
                    webcam_frame = cv2.resize(webcam_frame, self.webcam_size)

                    # Calculer la position
                    x, y = self.get_webcam_position(screen_width, screen_height)

                    # Ajouter un contour blanc à la webcam
                    border_size = 3
                    webcam_frame = cv2.copyMakeBorder(
                        webcam_frame,
                        border_size, border_size, border_size, border_size,
                        cv2.BORDER_CONSTANT,
                        value=[255, 255, 255]
                    )

                    # Superposer la webcam sur l'écran
                    cam_h, cam_w = webcam_frame.shape[:2]

                    # S'assurer que la position est valide
                    if y + cam_h <= screen_height and x + cam_w <= screen_width:
                        screen_frame[y:y+cam_h, x:x+cam_w] = webcam_frame

                # Écrire la frame
                self.out.write(screen_frame)

                # Contrôler le FPS
                time.sleep(1/fps)

            # Libérer les ressources
            self.out.release()

            messagebox.showinfo(
                "Succès",
                f"Enregistrement sauvegardé:\n{output_file}"
            )

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur pendant l'enregistrement:\n{str(e)}")
            self.is_recording = False
            if self.out:
                self.out.release()

    def on_closing(self):
        """Gérer la fermeture de l'application"""
        if self.is_recording:
            if messagebox.askokcancel("Quitter", "Un enregistrement est en cours. Voulez-vous vraiment quitter?"):
                self.is_recording = False
                time.sleep(0.5)  # Attendre la fin de l'enregistrement
                self.cleanup()
                self.root.destroy()
        else:
            self.cleanup()
            self.root.destroy()

    def cleanup(self):
        """Nettoyer les ressources"""
        if self.cap:
            self.cap.release()
        if self.out:
            self.out.release()
        cv2.destroyAllWindows()

    def run(self):
        """Démarrer l'application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


if __name__ == "__main__":
    app = LoomClone()
    app.run()
