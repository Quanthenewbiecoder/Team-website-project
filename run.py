from app import create_app

app = create_app()

if __name__ == '__main__':
    app = create_app()
    '''
    # Print routes using the app's url_map, not the blueprint's
    print("Available routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")
    '''
    app.run(debug=True)