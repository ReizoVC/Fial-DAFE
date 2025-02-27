from PyQt5 import QtWidgets
from controllers.habit_manager_app import SplashScreenApp
import UI.bg_rc  
import threading
import time

def check_notifications(manager):
    while True:
        manager.check_and_send_notifications()
        time.sleep(60)  # Verificar cada minuto

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    splash = SplashScreenApp()
    splash.show()

    # Iniciar el hilo para verificar notificaciones
    manager = splash.manager
    notification_thread = threading.Thread(target=check_notifications, args=(manager,))
    notification_thread.daemon = True
    notification_thread.start()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()