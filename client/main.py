from app import App

def main():
    """
    Main function to initialize and run the application.
    Handles any unexpected exceptions to provide user-friendly feedback.
    """
    try:
        app = App()
        app.run()
    except Exception as e:
        # Log the exception details for debugging purposes (replace with a proper logger in production)
        print(f"An error occurred while running the application: {e}")

if __name__ == "__main__":
    main()
