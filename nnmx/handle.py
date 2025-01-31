"""
███╗   ██╗███╗   ██╗███╗   ███╗██╗  ██╗
████╗  ██║████╗  ██║████╗ ████║╚██╗██╔╝
██╔██╗ ██║██╔██╗ ██║██╔████╔██║ ╚███╔╝
██║╚██╗██║██║╚██╗██║██║╚██╔╝██║ ██╔██╗
██║ ╚████║██║ ╚████║██║ ╚═╝ ██║██╔╝ ██╗
╚═╝  ╚═══╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝

2025 by FOSSIL @ https://github.com/fossil-org
more info at https://github.com/fossil-org/nnmx
misuse of this software is strictly prohibited.

type 'exit' to exit nnmx

"""

class Handle:
    def run(self):
        from pathlib import Path
        from os import walk, system
        from os.path import join, exists, getsize
        from importlib import import_module as im
        from inspect import signature

        import readline

        from .internal import (
        list_known_wifis,
        scan_wifis,
        connect_to_wifi,
        disconnect_wifi,
        check_wifi_password
        )

        loc = Path(__file__).parent / "bin"

        size = 0
        for dirpath, dirnames, filenames in walk(loc):
            for f in filenames:
                fp = join(dirpath, f)
                if exists(fp):
                    size += getsize(fp)
        size /= 1024
        size_mb = size / 1024
        disp_size = f"{size}kB"
        disp_size_mb = f"{size_mb}mB"

        print(__doc__)

        while True:
            try: src = input("nnmx $ ").strip()
            except (KeyboardInterrupt, EOFError): exit()

            command, *args = src.split(" ")
            try:
                match command:
                    case "":
                        continue
                    case "exit":
                        break
                    case "clear":
                        system("clear")
                    case "list":
                        print("\n".join(list_known_wifis()))
                    case "scan":
                        print("scanning...")
                        print("\n".join(list(set(scan_wifis()))))
                    case "connect":
                        connect_to_wifi(args[0], check_wifi_password(args[0]) if args[0] in list_known_wifis() else args[1])
                    case "disconnect":
                        disconnect_wifi()
                        print("disconnected from wifi network")
                    case "password":
                        print(check_wifi_password(args[0]))
                    case _:
                        print(f"unknown command: '{command}'")
            except IndexError:
                print("not enough arguments")
            except Exception as err:
                print(f"error: {err}")

def main():
    Handle().run()

if __name__ == "__main__":
    main()