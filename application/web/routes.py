"""Created on 12-09-2019."""
from flask import send_file, request, redirect, abort, jsonify
from src.core import Core



def importRoutes(rootpath, app, config_object):
    """Add user routes to app."""

    controller = Core()

    @app.route(rootpath, methods=['GET', 'POST'])
    def index_or_upload_file():
        if request.method == 'GET':
            return send_file("pages/index.html", mimetype='text/html')
        else:
            if 'fileToUpload' not in request.files:
                abort(404)
            else:
                file = request.files['fileToUpload']
                binary = file.read()
                modulesToUse = _parseValues(request.args.get('values'))
                ident = controller.run(binary, modulesToUse);
                return redirect("/"+ident, code=302)

    @app.route(rootpath+"favicon.ico", methods=['GET'])
    def get_favicon():
        return send_file("images/favicon.png", mimetype='image/png')

    @app.route(rootpath+"listModules", methods=['GET'])
    def list_modules():
        return jsonify(controller.getModules())

    @app.route(rootpath+"<hash>", methods=['GET'])
    def get_report(hash):
        report = controller.viewReport(hash)
        if report is None:
            abort(404)
        return jsonify(report)

    @app.route(rootpath+"<hash>"+"/"+"<name>", methods=['GET'])
    def get_generated_file(hash, name):
        filepath  = controller.getFilePath(hash, name)
        if filepath is None:
            abort(404)
        return send_file(filepath, mimetype='application/octet-stream')


def _parseValues(values):
    modulesToUse = []
    try:
        unparserModulesToUse = values.split(",")
        for unparserModule in unparserModulesToUse:
            try:
                moduleStr = unparserModule.split(":")
                module = {}
                module["id"] = int(moduleStr[0])
                module["params"] = []
                args = moduleStr[1].split(" ")
                for arg in args:
                    module["params"].append(arg)
                modulesToUse.append(module)
            except:
                print("invalid module:" + unparserModule)
    except:
        print("no modulesOn")
    return modulesToUse