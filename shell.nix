{ 
  pkgs ? import (fetchTarball 
    https://github.com/NixOS/nixpkgs/archive/d3ba49889a76539ea0f7d7285b203e7f81326ded.tar.gz
  ) {}
}:

pkgs.mkShell {
  buildInputs = with pkgs; [
    terraform_0_15
  ];

  shellHook = ''
    if [[ -f ".env" ]]; then
      source .env
    fi
  '';
}