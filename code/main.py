from application import*

def main():
    app:Application = Application()
    app.InitiateApplication()
    app.Run()
    app.TerminateApplication()

if __name__ == "__main__":
    main()