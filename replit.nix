{ pkgs }: {
  deps = [
    pkgs.python311Full
    pkgs.nodejs_18
    pkgs.yarn
    pkgs.mongodb
    pkgs.ffmpeg
    pkgs.pkg-config
    pkgs.gcc
    pkgs.python311Packages.pip
    pkgs.python311Packages.setuptools
    pkgs.python311Packages.wheel
    pkgs.python311Packages.numpy
    pkgs.python311Packages.scipy
    pkgs.python311Packages.pandas
    pkgs.python311Packages.requests
    pkgs.python311Packages.pydantic
    pkgs.python311Packages.fastapi
    pkgs.python311Packages.uvicorn
    pkgs.python311Packages.pymongo
    pkgs.python311Packages.python-multipart
    pkgs.python311Packages.python-jose
    pkgs.python311Packages.passlib
    pkgs.python311Packages.python-dotenv
    pkgs.python311Packages.cryptography
    pkgs.python311Packages.nltk
    pkgs.openssl
    pkgs.curl
    pkgs.wget
    pkgs.git
  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.python311Full
      pkgs.openssl
      pkgs.gcc
    ];
    PYTHONPATH = "${pkgs.python311Full}/lib/python3.11/site-packages";
    LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.openssl
      pkgs.gcc
    ];
  };
}