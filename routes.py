"""Created on 12-09-2019."""
import json
from flask import send_file, request, redirect, abort, jsonify
import core

def importRoutes(rootpath, app):
    """Add user routes to app."""
    @app.route(rootpath, methods=['GET', 'POST'])
    def index_or_upload_file():
        if request.method == 'GET':
            return send_file("./pages/index.html", mimetype='text/html')
        else:
            if 'fileToUpload' not in request.files:
                abort(404)
            else:
                file = request.files['fileToUpload']
                binary = file.read()
                modulesToUse = parseValues(request.args.get('values'))
                ident = core.run(binary, modulesToUse);
                return redirect("/"+ident, code=302)

    @app.route(rootpath+"favicon.ico", methods=['GET'])
    def get_favicon():
        return send_file("./images/favicon.png", mimetype='image/png')

    @app.route(rootpath+"listModules", methods=['GET'])
    def list_modules():
        return jsonify(core.getModules())

    @app.route(rootpath+"<hash>", methods=['GET'])
    def get_report(hash):
        report = core.viewReport(hash)
        if report is None:
            abort(404)
        return jsonify(report)


def parseValues(values):
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
        print("no modules")
    return modulesToUse