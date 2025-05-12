{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
	  python313
	  python313Packages.isort

	  python313Packages.pygame-ce
	  SDL

	  python313Packages.flask
    sqlite

    # keep this line if you use bash
    pkgs.bashInteractive
  ];
}
