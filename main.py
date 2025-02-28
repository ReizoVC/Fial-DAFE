from PyQt5 import QtWidgets
from controllers.habit_manager_app import SplashScreenApp
import UI.bg_rc  

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    splash = SplashScreenApp()
    splash.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()