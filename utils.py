class ColorUtils:
        Colors: dict = {
            "Green" : (32, 190, 32),
            "Green_Light" : (144, 238, 144),
            "Yellow" : (255, 173, 0),
            "Red" : (196, 26, 22),
            "Blue" : (0, 173, 239),
            "White" : (255, 255, 255)
        }
        
        @staticmethod
        def Reset_Color() -> None:
            print("\x1b[0m")
        
        @staticmethod
        def Set_Color(pColor: tuple[int, int, int]) -> None:
            print(f"\x1b[38;2;{pColor[0]};{pColor[1]};{pColor[2]}m")
        
        @staticmethod
        def Print_Colored(pColor: tuple[int, int, int], pText: str) -> str:
            print(f"\x1b[38;2;{pColor[0]};{pColor[1]};{pColor[2]}m", pText, "\x1b[0m")
            
        @staticmethod
        def Scan_Colored(pColor: tuple[int, int, int], pText: str) -> None:
            print(f"\x1b[38;2;{pColor[0]};{pColor[1]};{pColor[2]}m")
            s = input(pText)
            print("\x1b[0m")
            return s
        
        
        # def __init__(self) -> None:
        #     self.reset_io_color = lambda : print("\x1b[0m")
        #     self.set_io_color = lambda pColor : print(f"\x1b[38;2;{pColor[0]};{pColor[1]};{pColor[2]}m")
        #     self.ColorUtils.Print_Colored = lambda pColor, pText : print(f"\x1b[38;2;{pColor[0]};{pColor[1]};{pColor[2]}m", pText, "\x1b[0m")
