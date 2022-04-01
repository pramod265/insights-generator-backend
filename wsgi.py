from main import app
import pip

if __name__ == "__main__":

    if hasattr(pip, 'main'):
        pip.main(['install', 'pandas-profiling'])
    else:
        pip._internal.main(['install', 'pandas-profiling'])
    
    # app.debug=True
    app.run()


