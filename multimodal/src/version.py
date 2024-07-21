__version__ = "0.0.1"


@keras_export("keras.version")
def version():
    return __version__
