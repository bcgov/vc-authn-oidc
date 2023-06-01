# Add assets to templates, like css, js or svg.
def add_asset(name):
    return open(f"api/templates/assets/{name}", "r").read()
